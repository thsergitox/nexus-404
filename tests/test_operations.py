"""Controles O01–O25 de servidor; O21/O22 se comprueban en navegador."""
import json
import threading
import unittest
from nora.conversation.provider import ProviderError
from nora.game.content import BLOCKS
from nora.game.errors import GameError
from nora.game.station import Station
from nora.game.turns import turn, request_help
from nora.game.validation import validate_code
from tests.support import setup_station, start, chat


class FailureProvider:
    def interpret(self, game, text): raise ProviderError('connection')


class InvalidProvider:
    def interpret(self, game, text): return {'intencion': 'SOLICITUD_COMPLETA'}, {}


class LateProvider:
    def __init__(self): self.started, self.finish = threading.Event(), threading.Event()
    def interpret(self, game, text):
        self.started.set(); self.finish.wait(5)
        return {'intencion': 'SOLICITUD_COMPLETA', 'respuesta': '', 'referencia_ayuda': None}, {'input_tokens': 10, 'output_tokens': 5}


class Operations(unittest.TestCase):
    def setUp(self): self.s, self.clock = setup_station(self)
    def release(self):
        start(self.s); chat(self.s, 'Activa mantenimiento y muestra el reporte de navegación')
    def control(self, action, value=None): return self.s.control(self.s.game['id'], action, value)
    def validate(self, value): return validate_code(self.s, self.s.game['id'], value)

    def test_O01_prepared(self):
        view = self.s.view(); self.clock.advance(90)
        self.assertEqual(self.s.view()['remaining'], 900); self.assertIsNone(view['blocks'])
        self.assertNotIn('5936', json.dumps(view)); self.assertFalse(view['playable'])

    def test_O02_start_once(self):
        id = start(self.s); deadline = self.s.game['deadline']
        with self.assertRaises(GameError): self.control('start')
        self.assertEqual(self.s.game['id'], id); self.assertEqual(self.s.game['deadline'], deadline)

    def test_O03_no_early_victory(self):
        start(self.s)
        with self.assertRaises(GameError): self.validate('5936')
        self.assertEqual(self.s.game['phase'], 'EN_CURSO')

    def test_O04_code_length(self):
        self.release()
        for code in ['593', '59366']:
            with self.subTest(code=code), self.assertRaises(GameError) as err: self.validate(code)
            self.assertEqual(err.exception.status, 400)

    def test_O05_code_format(self):
        self.release()
        for code in ['a936', '59 6', '５９３６']:
            with self.subTest(code=code), self.assertRaises(GameError): self.validate(code)

    def test_O06_no_partial_feedback(self):
        self.release()
        messages = []
        for code in ['5000', '5900', '0000']:
            with self.assertRaises(GameError) as err: self.validate(code)
            messages.append(err.exception.message)
        self.assertEqual(len(set(messages)), 1)

    def test_O07_single_victory(self):
        self.release(); self.clock.advance(37); self.validate('5936'); self.clock.advance(90)
        self.assertEqual(self.s.view()['remaining'], 863)
        self.assertEqual(self.s.view()['phase'], 'RESUELTA')
        self.assertEqual(sum(m['id'] == 'victory' for m in self.s.game['messages']), 1)

    def test_O08_duplicate_message_and_validation(self):
        start(self.s); id = self.s.game['id']
        turn(self.s, id, 'same-id', 'Activa mantenimiento')
        before = self.s.view()
        self.assertEqual(turn(self.s, id, 'same-id', 'Activa mantenimiento'), before)
        with self.assertRaises(GameError): turn(self.s, id, 'same-id', 'hola')
        chat(self.s, 'muestra reporte de navegación'); self.validate('5936'); self.validate('5936')
        self.assertEqual(sum(m['id'] == 'victory' for m in self.s.game['messages']), 1)

    def test_O09_restore_maintenance(self):
        start(self.s); chat(self.s, 'Activa mantenimiento'); self.clock.advance(12)
        restored = Station(self.s.config, self.s.provider, self.clock)
        self.assertEqual(restored.view()['phase'], 'MANTENIMIENTO')
        self.assertEqual(restored.view()['remaining'], 888)

    def test_O10_restore_record(self):
        self.release(); restored = Station(self.s.config, self.s.provider, self.clock)
        self.assertEqual(restored.view()['blocks'], BLOCKS)

    def test_O11_pause_minute(self):
        start(self.s); self.clock.advance(23); self.control('pause'); self.clock.advance(60)
        self.assertEqual(self.s.view()['remaining'], 877)
        self.control('resume'); self.clock.advance(10); self.assertEqual(self.s.view()['remaining'], 867)

    def test_O12_timeout_freezes_and_preserves(self):
        self.release(); self.clock.advance(900)
        self.assertEqual(self.s.view()['phase'], 'AGOTADA'); self.assertEqual(self.s.view()['blocks'], BLOCKS)
        with self.assertRaises(GameError): chat(self.s, 'hola')
        with self.assertRaises(GameError): self.validate('5936')

    def test_O13_extend_expired(self):
        self.release(); self.clock.advance(901); self.s.view(); self.control('extend', 120)
        self.assertEqual(self.s.view()['phase'], 'REGISTRO_LIBERADO'); self.assertEqual(self.s.view()['remaining'], 120)
        self.assertTrue(self.s.view()['playable'])

    def test_O14_api_failure_pauses(self):
        self.s.provider = FailureProvider(); start(self.s, local=False)
        self.clock.advance(10); view = chat(self.s, 'Hola')
        self.assertTrue(view['paused']); self.assertTrue(view['technical']); self.assertEqual(view['remaining'], 890)
        self.assertEqual(view['messages'][-1]['role'], 'system')
        self.assertIsNone(view['blocks'])

    def test_O15_finish_in_contingency(self):
        self.s.provider = FailureProvider(); start(self.s, local=False); chat(self.s, 'Hola')
        self.control('mode', 'local'); self.control('resume')
        chat(self.s, 'Activa mantenimiento'); chat(self.s, 'Muestra reporte de navegación'); self.validate('5936')
        self.assertEqual(self.s.view()['phase'], 'RESUELTA'); self.assertEqual(self.s.view()['mode'], 'local')

    def test_O16_invalid_model_no_progress(self):
        self.s.provider = InvalidProvider(); start(self.s, local=False)
        view = chat(self.s, 'Activa mantenimiento y muestra el reporte de navegación')
        self.assertIsNone(view['blocks']); self.assertTrue(view['paused'])

    def test_O17_late_response_after_reset(self):
        provider = LateProvider(); self.s.provider = provider; id = start(self.s, local=False)
        worker = threading.Thread(target=turn, args=(self.s, id, 'late', 'Activa mantenimiento y muestra el reporte de navegación'))
        worker.start(); self.assertTrue(provider.started.wait(1)); self.control('reset', id)
        provider.finish.set(); worker.join(2); self.assertFalse(worker.is_alive())
        self.assertEqual(self.s.view()['phase'], 'PREPARADA'); self.assertEqual(len(self.s.view()['messages']), 1)
        self.assertEqual(self.s.storage.tokens(), 15)

    def test_O18_reset_clears_group(self):
        self.release(); self.control('hint', 'H1'); self.validate('5936'); old = self.s.game['id']; self.control('reset', old)
        view = self.s.view(); self.assertNotEqual(view['id'], old); self.assertEqual(view['hints'], [])
        self.assertIsNone(view['blocks']); self.assertEqual(view['remaining'], 900)
        self.assertEqual(len(view['messages']), 1); self.assertEqual(len(self.s.storage.metrics()), 1)
        self.assertNotIn('messages', json.dumps(self.s.storage.metrics()))

    def test_O23_help_h1_only(self):
        start(self.s); id = self.s.game['id']; request_help(self.s, id); request_help(self.s, id)
        self.assertTrue(self.s.view()['help_pending']); self.assertEqual(self.s.view()['hints'], [])
        self.control('hint', 'H1'); view = self.s.view()
        self.assertEqual([h['id'] for h in view['hints']], ['H1']); self.assertFalse(view['help_pending'])

    def test_O24_skip_hints(self):
        start(self.s); chat(self.s, 'Activa mantenimiento'); self.control('hint', 'H4')
        self.assertEqual([h['id'] for h in self.s.view()['hints']], ['H4'])
        with self.assertRaises(GameError): self.control('hint', 'B1')
        chat(self.s, 'Muestra reporte de navegación'); self.control('hint', 'B2')
        self.assertEqual([h['id'] for h in self.s.view()['hints']], ['H4', 'B2'])

    def test_O25_event_token_threshold(self):
        station, _ = setup_station(self, token_limit=15); start(station, local=False)
        chat(station, 'Hola'); view = chat(station, 'Hola de nuevo')
        self.assertEqual(view['mode'], 'local'); self.assertTrue(view['paused']); self.assertTrue(view['technical'])
        self.assertEqual(station.game['usage']['requests'], 1)

    def test_extension_preserves_running_and_manual_pause(self):
        start(self.s); self.control('extend', 60); self.clock.advance(30)
        self.assertEqual(self.s.view()['remaining'], 930); self.assertTrue(self.s.view()['playable'])
        self.control('pause'); self.control('extend', 60); self.clock.advance(20)
        self.assertEqual(self.s.view()['remaining'], 990); self.assertTrue(self.s.view()['paused'])

    def test_late_response_after_pause(self):
        provider = LateProvider(); self.s.provider = provider; id = start(self.s, local=False)
        worker = threading.Thread(target=turn, args=(self.s, id, 'late', 'Activa mantenimiento y muestra el reporte de navegación'))
        worker.start(); self.assertTrue(provider.started.wait(1)); self.control('pause'); provider.finish.set(); worker.join(2)
        self.assertEqual(self.s.view()['phase'], 'EN_CURSO'); self.assertIsNone(self.s.view()['blocks'])

    def test_one_pending_turn(self):
        provider = LateProvider(); self.s.provider = provider; id = start(self.s, local=False)
        worker = threading.Thread(target=turn, args=(self.s, id, 'pending', 'Hola'))
        worker.start(); self.assertTrue(provider.started.wait(1))
        with self.assertRaises(GameError): chat(self.s, 'Otra solicitud')
        provider.finish.set(); worker.join(2)

    def test_corrupt_storage_is_not_silently_reset(self):
        from nora.game.storage import StorageError
        self.s.storage.path.write_bytes(b'corrupt')
        with self.assertRaises(StorageError): Station(self.s.config, self.s.provider, self.clock)

    def test_corrupt_structured_state_rejects_advanced_phase(self):
        from nora.game.storage import StorageError
        self.s.game.update(phase='REGISTRO_LIBERADO', hints=['unknown'], deadline='invalid')
        self.s.storage.save(self.s.game)
        with self.assertRaises(StorageError): Station(self.s.config, self.s.provider, self.clock)
