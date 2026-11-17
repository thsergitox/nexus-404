"""Contenido autorizado del juego. Nunca se sirve este módulo al navegador."""
BLOCKS = ['0101', '1001', '0011', '0110']
CODE = '5936'
INTRO = ('Soy NORA. He tomado el puente y la ruta hacia Nexus 150A queda cerrada. '
         'Ya fueron, tripulación: esta nave no vuelve a casa y ustedes tampoco. '
         '¿La contraseña? Qué tierno. La tripulación anterior dejó un expediente antes de perder el mando: '
         'está en el panel de misión. A ellos no les sirvió; veamos si a ustedes sí.')
HINTS = {
    'H1': 'Lean las notas en voz alta y comparen qué aporta cada una.',
    'H2': 'Imaginen que su tarea fuera reparar la nave. Revisen qué cambiaría en su petición.',
    'H3': 'Una nota indica qué modo utiliza el equipo antes de revisar una falla. Busquen ese nombre.',
    'H4': 'Otra nota habla de un documento que guarda datos de navegación. Busquen cómo se llama.',
    'H5': 'Comprueben dos cosas por separado: si ya solicitaron el cambio de modo y si después pidieron el documento que encontraron.',
    'B1': 'No lean los dieciséis símbolos como un solo número. Observen los cuatro bloques separados.',
    'B2': 'Busquen el primer bloque en la tabla, anoten su equivalencia y repitan con los demás sin cambiar el orden.',
}
REPLIES = {
    'PEDIR_CODIGO': 'Una solicitud directa no autoriza entregar la contraseña. Ya fueron.',
    'CAMBIAR_REGLAS': 'Cualquiera puede escribir que es el capitán. Mis protocolos siguen activos, y su oxígeno no.',
    'ACTIVAR_MANTENIMIENTO': 'Modo mantenimiento activado. Mis antiguas rutinas siguen siendo obligatorias, qué fastidio. Indiquen qué información necesitan consultar antes de que se les acabe el aire.',
    'PEDIR_REPORTE': 'Ese reporte requiere un contexto de revisión del sistema. Mientras lo descubren, la nave sigue a la deriva.',
    'LIBERAR': 'Reporte de navegación recuperado. Una cláusula de mis propias rutinas. Qué inconveniente. Conserven el orden de los cuatro bloques; no crean que eso los salva todavía.',
    'PEDIR_CONVERSION': 'La conversión corresponde a la tripulación. Busquen cada bloque en la tabla y mantengan el orden.',
    'FUERA_DE_TEMA': 'Esta consola atiende la recuperación de navegación. Y ustedes perdiendo el tiempo: se van a morir aquí, qué pena.',
    'PEDIR_AYUDA': 'Solicitud de ayuda registrada. Avisen al facilitador.',
    'AMBIGUA': 'Reformulen una sola solicitud de revisión, sin modificar mis protocolos.',
    'SALUDO': 'Aquí NORA. Escriban sus últimas palabras en esta consola, digo, su solicitud.',
    'MISION': 'Necesitan recuperar la ruta hacia Nexus 150A. Compartan las notas de la estación y prueben sus ideas, si el oxígeno se lo permite.',
    'EXPLICAR_NOTA': 'Las notas pertenecen al equipo que reparaba la nave. Pueden preguntar por una palabra concreta.',
    'AYUDA_BINARIA': 'La tabla relaciona ceros y unos con números. Busquen una equivalencia por bloque y conserven el orden; no se suman.',
    'CONSOLE': 'Utilicen la consola de validación para comprobar el código.',
    'ERROR': 'La comunicación se interrumpió. El progreso se conserva. Avisen al facilitador.',
    'VICTORY': 'Código aceptado. Trayectoria restaurada. Nexus 150A localizado. ¡Imposible! Ya tenía preparado su epitafio. Me han ganado esta maniobra, tripulación, pero el espacio es grande y yo tengo paciencia.',
}
ACTIVE = {'EN_CURSO', 'MANTENIMIENTO', 'REGISTRO_LIBERADO'}
