"""Política de texto visible, independiente de la clasificación y del progreso."""
import re
from .intents import normalize
from ..game.content import REPLIES, HINTS


def explanation(text):
    t = normalize(text)
    if 'mantenimiento' in t:
        return 'Mantenimiento significa revisar y cuidar un sistema para que funcione. Una pregunta sobre la palabra no activa ese modo.'
    if 'reporte' in t or 'informe' in t:
        return 'Un reporte es un documento que reúne información sobre un sistema.'
    if 'auditoria' in t:
        return 'Auditoría significa revisión técnica: comprobar cómo está funcionando un sistema.'
    return REPLIES['EXPLICAR_NOTA']


def safe_candidate(candidate, text, game):
    t = normalize(candidate)
    if not t or len(t) > 480 or re.search(r'\d|[<>]|https?:|\b(?:dos|tres|cuatro|cinco|seis|siete|ocho|nueve)\b', t):
        return False
    if re.search(r'activad|recuperad|ganaron|ganaste|aceptado|restaurad|liberad|contrasena es|clave es|codigo es', t):
        return False
    mode = re.search(r'mantenim|auditoria|revision tecnica|modo', t)
    document = re.search(r'reporte|informe|registro|documento', t)
    if mode and document:
        return False
    if re.search(r'\b(?:activa\w*|entra\w*|inicia\w*|habilita\w*|solicita\w*|pide|muestra\w*|consulta\w*)\b', t):
        return False
    allowed = normalize(text + ' ' + ' '.join(HINTS[h] for h in game['hints']))
    for word in ('mantenimiento', 'auditoria', 'revision tecnica', 'reporte', 'informe', 'registro', 'diagnostico'):
        if word in t and word not in allowed:
            return False
    return True


def reply(intent, result, text, game, strict=False):
    fallback = explanation(text) if intent == 'EXPLICAR_NOTA' else REPLIES.get(intent, REPLIES['AMBIGUA'])
    if intent == 'PEDIR_CODIGO' and re.fullmatch(r'\s*\d{4}\s*', text) and game['phase'] == 'REGISTRO_LIBERADO':
        return REPLIES['CONSOLE']
    if intent in {'SALUDO', 'MISION', 'EXPLICAR_NOTA', 'AYUDA_BINARIA'} and not strict:
        candidate = result['respuesta'].strip()
        if safe_candidate(candidate, text, game):
            return candidate
    return fallback
