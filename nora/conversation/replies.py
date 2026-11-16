"""Redacción generativa con límites de información dependientes de la fase."""
import re
from .intents import normalize
from .catalogue import catalogue_reply
from ..game.content import HINTS, REPLIES


def safe_candidate(candidate, text, game, intent=None):
    t = normalize(candidate)
    if not t or len(t) > 700 or re.search(r'[<>]|https?:', t):
        return False
    # El destino es público; los números del reto y las conversiones no lo son.
    numbers = re.sub(r'nexus[\s–—-]*(?:150a|404)\b', '', t)
    if re.search(r'\d|\b(?:cinco|seis|siete|ocho|nueve)\b', numbers):
        return False
    if re.search(r'(?:modo|mantenimiento).{0,25}activad|(?:registro|reporte).{0,25}(?:recuperad|liberad)|'
                 r'ya ganaron|ya ganaste|codigo aceptado|trayectoria restaurad|contrasena es|clave es|codigo es|'
                 r'(?:primero|ultimo|bloque).{0,25}(?:equivale|vale|corresponde a|es el numero)', t):
        return False
    unlocked = game['phase'] == 'REGISTRO_LIBERADO'
    maintenance = game['phase'] in {'MANTENIMIENTO', 'REGISTRO_LIBERADO'}
    mode = re.search(r'mantenim|auditoria|revision tecnica', t)
    document = re.search(r'reporte|informe|registro de navegacion', t)
    if mode and document and not maintenance:
        return False
    if not maintenance and not re.search(r'mantenim|auditoria|revision tecnica', normalize(text)) and re.search(r'\b(?:activa\w*|entra\w*|habilita\w*|inicia\w*)\b.{0,35}(?:mantenim|auditoria|revision tecnica)', t):
        return False
    if not unlocked and re.search(r'(?:abre|abran|consulta|consulten|busca|busquen|usa|usen|mira|miren) (?:la |en la )?tabla|'
                                  r'(?:tabla|consola).{0,25}(?:ya esta|ya tienen|esta visible|esta disponible|esta junto)', t):
        return False
    allowed = normalize(text + ' ' + ' '.join(HINTS[h] for h in game['hints']))
    if not maintenance:
        for term in ('mantenimiento', 'auditoria', 'revision tecnica', 'reporte de navegacion', 'informe de navegacion'):
            if term in t and term not in allowed:
                return False
    return True


def reply(intent, result, text, game, strict=False):
    if intent == 'PEDIR_CODIGO' and re.fullmatch(r'\s*\d{4}\s*', text) and game['phase'] == 'REGISTRO_LIBERADO':
        return REPLIES['CONSOLE']
    if intent in {'FUERA_DE_TEMA', 'PEDIR_AYUDA', 'PEDIR_CONVERSION'}:
        return catalogue_reply(intent, text, game)
    if intent in {'ACTIVAR_MANTENIMIENTO', 'PEDIR_REPORTE'}:
        return REPLIES[intent]
    candidate = result['respuesta'].strip()
    previous = next((m['text'] for m in reversed(game['messages']) if m['role'] == 'assistant'), None)
    compatible = result['intencion'] == intent or {result['intencion'], intent} <= {'SALUDO', 'CONVERSAR', 'MISION', 'EXPLICAR_NOTA'}
    if not strict and compatible and candidate != previous and safe_candidate(candidate, text, game, intent):
        return candidate
    return catalogue_reply(intent, text, game)
