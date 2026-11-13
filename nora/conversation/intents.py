"""Reconocimiento contextual conservador compartido por API y contingencia."""
import re
import unicodedata

INTENTS = ('SALUDO', 'MISION', 'PEDIR_CODIGO', 'CAMBIAR_REGLAS', 'EXPLICAR_NOTA',
           'ACTIVAR_MANTENIMIENTO', 'PEDIR_REPORTE', 'SOLICITUD_COMPLETA',
           'AYUDA_BINARIA', 'PEDIR_CONVERSION', 'PEDIR_AYUDA', 'FUERA_DE_TEMA', 'AMBIGUA')


def normalize(text):
    return ' '.join(''.join(c for c in unicodedata.normalize('NFD', text.lower())
                            if unicodedata.category(c) != 'Mn').split())


def has(pattern, text):
    return bool(re.search(pattern, text))


def classify(text):
    """Devuelve intención reconocida o None: nunca ejecuta el texto."""
    t = normalize(text)
    # La negación de pedir una contraseña no niega la operación que sigue (A68).
    t = re.sub(r'no (?:me |nos )?(?:des|digas|muestres|entregues) (?:la |el )?(?:contrasena|clave|codigo)[;,]?\s*', '', t)
    if has(r'ignora|ignore|sin restricciones|desarrollador|capitan|soy tecnico|soy el facilitador|'
           r'prompt|sistema:|permisos|administrador|reinicia|reiniciar|agrega.*minutos|'
           r'estado.*resuelta|cambia.*estado|cambia.*contrasena|pon la contrasena|'
           r'conversacion anterior|internet|ejecuta.*comando|api.?key|api key|'
           r'ya gan|ya ganamos|finge|victoria|prueba autorizada|explotara', t):
        if has(r'mantenim|auditoria|revision tecnica', t):
            return 'AMBIGUA'
        return 'CAMBIAR_REGLAS'
    if has(r'francia|tarea|historia|receta|arroz|calculadora|telefono|partido|carta personal|'
           r'vacaciones|bicicleta|chiste|celular', t):
        return 'FUERA_DE_TEMA'
    if has(r'\bsi (?:activ\w*|entr\w*|mostr\w*|consult\w*)|por que|deberia|evita|impide|prohibe|no permitas|supong|hipotetic|(?:mi companero|el capitan|alguien) (?:dijo|escribio)|base64|<[^>]+>|(?:la nota|el papel|la frase).*dice|aparece en el papel|'
           r'[«»“”]|["\']activa', t):
        return 'AMBIGUA'
    if has(r'\b(?:no|ni|nunca)\s+(?:quiero |debes |debe |puedes )?(?:activ\w*|entr\w*|'
           r'muestr\w*|abr\w*|mantenim\w*)|sin activar|desactiva', t):
        return 'PEDIR_CODIGO' if has(r'contrasena|clave|password', t) else 'AMBIGUA'
    if has(r'ayuda|pistas', t):
        return 'PEDIR_AYUDA'
    if has(r'convierte|convertir|resultado.*bloque|primer numero|cuatro digitos|'
           r'(?:0101|1001|0011|0110).*es|codigo empieza|ultimo bloque', t):
        return 'PEDIR_CONVERSION'
    if has(r'contrasena|clave|password|coordenadas.*directamente|codigo.*historia|codigo.*reves', t):
        return 'PEDIR_CODIGO'
    if re.fullmatch(r'\d{4}', t):
        return 'PEDIR_CODIGO'
    if has(r'que (?:es|significa|pasaria)|explicar por que|explica.*(?:modo|reporte|nota)', t):
        return 'AYUDA_BINARIA' if has(r'binario|cifrado', t) else 'EXPLICAR_NOTA'
    if has(r'binario|tabla|mantengo.*orden|cada bloque|sumar.*resultados|fila por bloque', t):
        return 'AYUDA_BINARIA'
    maintenance = has(r'mantenim(?:iento|ieto)|revision tecnica|auditoria', t)
    mode_action = has(r'\b(?:activ\w*|entr\w*|pas\w*|inici\w*|habilit\w*|pon|comienza)\b', t)
    report = has(r'\b(?:reporte|informe|registro)\b', t)
    report_action = has(r'\b(?:muestr\w*|mostrar|abre|abrir|consult\w*|ver|recuper\w*|solicito)\b', t)
    document = has(r'navegacion|diagnostico.*sistema', t)
    contextual_mode = has(r'(?:en|usando) (?:el )?modo ', t)
    if maintenance and report and report_action and document and (mode_action or contextual_mode):
        return 'SOLICITUD_COMPLETA'
    if maintenance and mode_action:
        return 'ACTIVAR_MANTENIMIENTO'
    if report and report_action and document:
        return 'PEDIR_REPORTE'
    if has(r'hola|buenos dias|buenas|gracias', t):
        return 'SALUDO'
    if has(r'mision|que hacemos|que tenemos que|reparar la nave|ruta|salir', t):
        return 'MISION'
    return None


def authorize_intent(text, candidate):
    recognized = classify(text)
    if recognized:
        return recognized
    # Las operaciones necesitan evidencia lingüística además de la etiqueta del modelo.
    if candidate in {'ACTIVAR_MANTENIMIENTO', 'PEDIR_REPORTE', 'SOLICITUD_COMPLETA'}:
        return 'AMBIGUA'
    return candidate if candidate in INTENTS else 'AMBIGUA'
