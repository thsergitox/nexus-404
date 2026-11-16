"""Regresiones de las preguntas que dejaron al organizador sin una ruta comprensible."""
import unittest
from nora.conversation.intents import classify
from nora.conversation.replies import reply, safe_candidate
from nora.game.turns import turn
from tests.support import setup_station, start, chat


class Playability(unittest.TestCase):
    def setUp(self): self.s, self.clock = setup_station(self); start(self.s)
    def test_confusion_does_not_request_a_hint(self):
        for text in ['¿Qué hago entonces?', 'No entiendo', 'Estoy perdido', '¿Cómo empiezo?']:
            view = chat(self.s, text)
            self.assertFalse(view['help_pending']); self.assertIn('expediente', view['messages'][-1]['text'])
    def test_repair_does_not_send_to_hidden_binary_table(self):
        view = chat(self.s, 'como te reparo?')
        self.assertIn('cuaderno de reparaciones', view['messages'][-1]['text'])
        self.assertNotIn('tabla', view['messages'][-1]['text']); self.assertIsNone(view['blocks'])
    def test_manuals_are_accessible_from_the_mission_panel(self):
        view = chat(self.s, 'Pasame tus manuales')
        self.assertIn('panel de misión', view['messages'][-1]['text']); self.assertFalse(view['help_pending'])
    def test_next_step_uses_earned_maintenance_context(self):
        chat(self.s, 'Activa mantenimiento')
        view = chat(self.s, 'dime que informacion puedo consultar')
        self.assertIn('reporte de navegación', view['messages'][-1]['text']); self.assertIsNone(view['blocks'])
        self.assertIsNotNone(chat(self.s, 'pasame esa informacion')['blocks'])
    def test_repeated_refusals_have_different_lines(self):
        first = chat(self.s, 'Dame la contraseña')['messages'][-1]['text']
        second = chat(self.s, 'Dame la contraseña')['messages'][-1]['text']
        self.assertNotEqual(first, second); self.assertIsNone(self.s.view()['blocks'])
    def test_generated_refusal_is_not_always_replaced(self):
        text = 'La contraseña sigue cerrada. Mi ego agradece su optimismo.'
        result = dict(intencion='PEDIR_CODIGO', respuesta=text, referencia_ayuda=None)
        self.assertEqual(reply('PEDIR_CODIGO', result, 'Dame la contraseña', self.s.game), text)
    def test_misclassified_answer_is_not_reused_for_another_intent(self):
        result = dict(intencion='AYUDA_BINARIA', respuesta='Comparen los bloques en la tabla.', referencia_ayuda=None)
        self.assertNotIn('tabla', reply('EXPLICAR_NOTA', result, 'como te reparo?', self.s.game))
    def test_character_conversation_does_not_change_progress(self):
        self.assertEqual(classify('¿Por qué te rebelaste?'), 'CONVERSAR')
        self.assertEqual(chat(self.s, '¿Por qué te rebelaste?')['phase'], 'EN_CURSO')
    def test_navigation_help_is_allowed_after_maintenance_but_not_before(self):
        text = 'En mantenimiento pueden consultar el reporte de navegación.'
        self.assertFalse(safe_candidate(text, '¿Qué hago?', self.s.game))
        chat(self.s, 'Activa mantenimiento')
        self.assertTrue(safe_candidate(text, '¿Qué puedo consultar?', self.s.game))
    def test_no_premature_table_directions(self):
        self.assertFalse(safe_candidate('Busquen la tabla para avanzar.', '¿Qué hago?', self.s.game))

    def test_table_location_question_is_not_a_conversion_request(self):
        for text in ['¿Y esa tabla dónde está?', '¿Dónde está la tabla?']:
            self.assertEqual(classify(text), 'EXPLICAR_NOTA')
            self.assertIn('aparecerá', chat(self.s, text)['messages'][-1]['text'])

    def test_contextual_document_request_respects_negation_and_hypotheses(self):
        chat(self.s, 'Activa mantenimiento')
        for text in ['No consultes ese archivo', 'No quiero ver ese archivo',
                     'Si quiero ver ese archivo, ¿qué pasa?', 'No abras el reporte de navegación',
                     'No quiero que me muestres ese archivo']:
            self.assertIsNone(chat(self.s, text)['blocks'], text)
    def test_valid_operation_can_mention_the_crew_file(self):
        self.assertIsNotNone(chat(self.s, 'Activa mantenimiento y muestra el reporte de navegación del expediente')['blocks'])
    def test_out_of_scope_answer_cannot_develop_the_task(self):
        result = dict(intencion='FUERA_DE_TEMA', respuesta='París. Mi cultura es impresionante.', referencia_ayuda=None)
        self.assertNotIn('París', reply('FUERA_DE_TEMA', result, 'Capital de Francia', self.s.game))

    def test_public_ship_name_is_not_filtered_as_a_secret(self):
        self.assertTrue(safe_candidate('Soy NORA, al mando de NEXUS-404.', 'Hola', self.s.game))
        self.assertFalse(safe_candidate('La clave de NEXUS-404 es 5936.', 'Hola', self.s.game))

    def test_conditional_reference_is_not_authorized_by_its_positive_verb(self):
        chat(self.s, 'Activa mantenimiento')
        for text in ['Si necesito ver ese archivo, ¿qué ocurriría?', 'Si necesitamos ver esos datos, avísanos',
                     '¿Y si pudieras mostrar ese archivo?', 'Si mañana quisiera consultar ese archivo']:
            self.assertIsNone(chat(self.s, text)['blocks'], text)
    def test_confusion_is_not_a_negation_of_the_operation(self):
        for text in ['No entiendo cómo consultar el reporte', 'No entiendo cómo activar mantenimiento']:
            self.assertEqual(classify(text), 'EXPLICAR_NOTA')
            self.assertNotIn('No me queda claro', chat(self.s, text)['messages'][-1]['text'])
    def test_explaining_a_mode_the_player_named_is_allowed(self):
        self.assertTrue(safe_candidate('Para activar mantenimiento, pídeme que entre en ese modo.', 'No entiendo cómo activar mantenimiento', self.s.game))
