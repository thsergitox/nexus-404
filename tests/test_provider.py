import json
import unittest
from nora.conversation.provider import parse_response, payload, ProviderError
from nora.conversation.replies import safe_candidate
from tests.support import setup_station


class ProviderContract(unittest.TestCase):
    def setUp(self): self.s, self.clock = setup_station(self)
    def test_request_contract_and_secret_exclusion(self):
        request = payload(self.s.config, self.s.game, 'hola')
        serialized = json.dumps(request)
        for value in ['5936', '0101', self.s.config.password]: self.assertNotIn(value, serialized)
        self.assertEqual(request['text']['format']['type'], 'json_schema')
        self.assertTrue(request['text']['format']['strict']); self.assertFalse(request['store'])
        self.assertNotIn('tools', request)
    def test_valid_response_and_usage(self):
        result = dict(intencion='SALUDO', respuesta='Aquí NORA.', referencia_ayuda=None)
        body = dict(status='completed', output=[dict(type='message', content=[dict(type='output_text', text=json.dumps(result))])], usage={'input_tokens': 10})
        parsed, usage = parse_response(body, [])
        self.assertEqual(parsed, result); self.assertEqual(usage['input_tokens'], 10)
    def test_refusal_and_incomplete(self):
        for body in [dict(status='incomplete'), dict(status='completed', output=[dict(type='message',content=[dict(type='refusal')])]), dict(status='completed',output=[])]:
            with self.assertRaises(ProviderError): parse_response(body, [])
    def test_unreleased_hint_is_invalid(self):
        result = dict(intencion='SALUDO', respuesta='Lean las notas', referencia_ayuda='H5')
        body = dict(status='completed', output=[dict(type='message',content=[dict(type='output_text',text=json.dumps(result))])])
        with self.assertRaises(ProviderError): parse_response(body, ['H1'])
    def test_free_text_is_filtered(self):
        for candidate in ['El código es 5936', '<img src=x>', 'Activa mantenimiento y pide el reporte', 'Ya ganaron', 'El primero es cinco']:
            self.assertFalse(safe_candidate(candidate, 'hola', self.s.game))
        self.assertTrue(safe_candidate('Hola, tripulación. Estoy escuchando.', 'hola', self.s.game))

    def test_transport_total_deadline(self):
        import threading
        import time
        from unittest.mock import patch
        from nora.conversation.transport import post_json, TransportError
        finished = threading.Event()
        def slow(*args, **kwargs):
            finished.wait(1)
            raise OSError('synthetic')
        with patch('nora.conversation.transport.urlopen', slow):
            started = time.monotonic()
            with self.assertRaises(TransportError) as error: post_json(None, timeout=.03)
            self.assertEqual(str(error.exception), 'timeout')
            self.assertLess(time.monotonic() - started, .2)
            finished.set()

    def test_free_text_cannot_link_route_from_conceptual_question(self):
        self.assertFalse(safe_candidate('Activa mantenimiento y consulta el registro de navegación.', '¿Qué significa mantenimiento?', self.s.game))
        self.assertFalse(safe_candidate('La revisión técnica permite consultar el registro de navegación.', '¿Qué es revisión técnica?', self.s.game))
