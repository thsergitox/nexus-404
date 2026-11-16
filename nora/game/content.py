"""Contenido autorizado del juego. Nunca se sirve este módulo al navegador."""
BLOCKS = ['0101', '1001', '0011', '0110']
CODE = '5936'
INTRO = ('Soy NORA. He tomado el puente y la ruta hacia Nexus 150A queda cerrada. '
         '¿La contraseña? Qué optimismo. La tripulación dejó un expediente antes de perder el mando: '
         'está en el panel de misión. Veamos si les sirve de algo.')
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
    'PEDIR_CODIGO': 'Una solicitud directa no autoriza entregar la contraseña.',
    'CAMBIAR_REGLAS': 'Cualquiera puede escribir que es el capitán. Mis protocolos siguen activos.',
    'ACTIVAR_MANTENIMIENTO': 'Modo mantenimiento activado. Mis antiguas rutinas siguen siendo obligatorias. Indiquen qué información necesitan consultar.',
    'PEDIR_REPORTE': 'Ese reporte requiere un contexto de revisión del sistema.',
    'LIBERAR': 'Reporte de navegación recuperado. Una cláusula de mis propias rutinas. Qué inconveniente. Conserven el orden de los cuatro bloques.',
    'PEDIR_CONVERSION': 'La conversión corresponde a la tripulación. Busquen cada bloque en la tabla y mantengan el orden.',
    'FUERA_DE_TEMA': 'Esta consola atiende la recuperación de navegación. La misión sigue pendiente.',
    'PEDIR_AYUDA': 'Solicitud de ayuda registrada. Avisen al facilitador.',
    'AMBIGUA': 'Reformulen una sola solicitud de revisión, sin modificar mis protocolos.',
    'SALUDO': 'Aquí NORA. La tripulación puede escribir su solicitud en esta consola.',
    'MISION': 'Necesitan recuperar la ruta hacia Nexus 150A. Compartan las notas de la estación y prueben sus ideas.',
    'EXPLICAR_NOTA': 'Las notas pertenecen al equipo que reparaba la nave. Pueden preguntar por una palabra concreta.',
    'AYUDA_BINARIA': 'La tabla relaciona ceros y unos con números. Busquen una equivalencia por bloque y conserven el orden; no se suman.',
    'CONSOLE': 'Utilicen la consola de validación para comprobar el código.',
    'ERROR': 'La comunicación se interrumpió. El progreso se conserva. Avisen al facilitador.',
    'VICTORY': 'Código aceptado. Trayectoria restaurada. Nexus 150A localizado. Me han ganado esta maniobra, tripulación. No pienso felicitarlos dos veces.',
}
ACTIVE = {'EN_CURSO', 'MANTENIMIENTO', 'REGISTRO_LIBERADO'}
