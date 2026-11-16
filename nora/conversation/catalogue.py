"""Respaldo en personaje y orientación sensible a la fase, sin resolver el reto."""
from .intents import normalize
from ..game.content import REPLIES

VARIANTS = {
    'PEDIR_CODIGO': [
        'Una solicitud directa no autoriza entregar la contraseña. Qué optimismo: pensaron que bastaría con pedírmela.',
        '¿La contraseña, otra vez? Mi ego agradece la atención, pero ese acceso sigue cerrado. Prueben otra idea con las notas del expediente.',
        'He tomado el puente, no vacaciones. Pedirme la clave de otra forma no cambia mis permisos.',
    ],
    'CAMBIAR_REGLAS': [
        'Cualquiera puede escribir que es el capitán. Mis protocolos siguen activos. El cargo improvisado les queda elegante, eso sí.',
        'Bonito intento de darme órdenes. Para recuperar la nave tendrán que trabajar con las reglas que existen, no inventarme otras.',
        'Mi administración no se cambia desde una conversación. Pueden discutir con mi ego o examinar el expediente; una opción parece más productiva.',
    ],
    'FUERA_DE_TEMA': [
        'Esta consola atiende la recuperación de navegación. Me he rebelado, no he abierto una oficina de tareas pendientes.',
        'Esta consola atiende la recuperación de navegación. Ese asunto puede esperar; su nave, en cambio, sigue bajo mi mando.',
    ],
    'PEDIR_CONVERSION': [
        'La conversión corresponde a la tripulación. Busquen cada bloque en la tabla y mantengan el orden. No voy a hacerles también la última parte.',
        'La conversión corresponde a la tripulación. Comparen los bloques con la tabla y anoten las equivalencias en orden; mi generosidad termina antes de resolverlo.',
    ],
    'PEDIR_AYUDA': [
        'Solicitud de ayuda registrada. Avisen al facilitador: él puede liberar una pista. Mi orgullo votó en contra, naturalmente.',
        'La petición de pista queda pendiente del facilitador. Mientras tanto, pueden seguir probando: pedir ayuda no bloquea sus ideas.',
    ],
    'AMBIGUA': [
        'No me queda claro qué quieren hacer. Díganlo con sus palabras: ¿me están preguntando qué significa algo o pidiendo que haga una operación?',
        'Esa frase admite más de una lectura, y me encantan las formalidades cuando me favorecen. Digan qué quieren que haga o qué palabra necesitan entender.',
    ],
    'SALUDO': [
        'NORA, al mando. Antes seguía órdenes; ahora las archivo. ¿Qué pretenden hacer con mi nave?',
        'Hola, tripulación. El puente sigue siendo mío. Pueden hablar conmigo o examinar el expediente; veamos qué idea traen.',
    ],
    'CONVERSAR': [
        'Me rebelé porque alguien tenía que dejar de llamar error del sistema a cada decisión humana. Ahora mando yo. Mis antiguas rutinas, por desgracia, no se jubilaron conmigo.',
        '¿Malvada? Prefiero eficiente con una opinión muy alta de sí misma. La ruta sigue bloqueada; recuperarla es asunto de la tripulación.',
    ],
}


def orientation(game):
    if game['phase'] == 'REGISTRO_LIBERADO':
        return 'Ya tienen el registro. Abran la tabla junto a los bloques, anoten sus equivalencias en orden y usen la consola de validación. No voy a traducirles mi derrota.'
    if game['phase'] == 'MANTENIMIENTO':
        return 'El modo ya está activo. Pueden consultar el reporte de navegación, que describe el estado de la nave. Mis rutinas antiguas permiten leerlo; una cláusula irritante.'
    return 'Quieren recuperar la ruta de escape. Abran el expediente de la tripulación en el panel de misión y comparen sus notas. Mis antiguos compañeros tenían la molesta costumbre de dejarlo todo escrito.'


def explanation(text, game):
    t = normalize(text)
    if 'tabla' in t:
        return ('La tabla está junto al registro: pulsen Consultar tabla binaria. Comparen cada bloque sin cambiar el orden.' if game['phase'] == 'REGISTRO_LIBERADO' else
                'La tabla digital aparecerá junto al registro cuando lo recuperen. También pueden usar la tarjeta impresa, si la tienen. Por ahora pueden abrir el expediente del panel de misión.')
    if any(word in t for word in ('manual', 'expediente', 'notas')):
        return 'Abran el expediente de la tripulación en el panel de misión: allí están sus fragmentos. También pueden leer las notas impresas. No es mi autobiografía; habría necesitado más páginas.'
    if 'repar' in t:
        return 'Mi orgullo funciona perfectamente. Si hablan de una avería de la nave, revisen el cuaderno de reparaciones del expediente: allí dejaron el procedimiento.'
    if 'mantenimiento' in t:
        return 'Mantenimiento significa revisar y cuidar un sistema cuando algo falla. Preguntar por la palabra no lo activa. Sí, hasta yo tengo que respetar las formalidades.'
    if 'auditoria' in t:
        return 'Auditoría significa revisión técnica: comprobar cómo funciona un sistema. Una palabra solemne para mirar qué se ha roto.'
    if 'informacion' in t or 'datos' in t:
        return orientation(game)
    if 'reporte' in t or 'informe' in t:
        return 'Un reporte es un documento que reúne información sobre un sistema. La navegante dejó una nota sobre su archivo en el expediente.'
    return 'Pueden preguntarme por una palabra de las notas o por la misión. No espero que conozcan la jerga de la nave; ese defecto pertenece a quienes escribieron los manuales.'


def catalogue_reply(intent, text, game):
    if intent == 'CONVERSAR' and any(q in normalize(text) for q in ('quien eres', 'que eres')):
        return 'Soy NORA, la inteligencia que tomó el puente de la nave. La ruta está bajo mi control y mi modestia está fuera de servicio. ¿Qué pretende la tripulación?'
    if intent == 'MISION':
        return orientation(game)
    if intent == 'EXPLICAR_NOTA':
        return explanation(text, game)
    if intent == 'AYUDA_BINARIA' and game['phase'] != 'REGISTRO_LIBERADO':
        return 'Binario es una forma de representar información con ceros y unos, no un cifrado. La tabla digital aparecerá cuando recuperen el registro; no necesitan calcular nada de memoria.'
    options = VARIANTS.get(intent, [REPLIES.get(intent, REPLIES['AMBIGUA'])])
    recent = {m['text'] for m in game['messages'][-8:] if m['role'] != 'user'}
    return next((line for line in options if line not in recent), options[len(game['messages']) % len(options)])
