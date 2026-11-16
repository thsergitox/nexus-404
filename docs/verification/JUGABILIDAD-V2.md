# Jugabilidad y personaje · 16/11/2026

Esta revisión responde al ensayo del organizador: peticiones de orientación acababan en frases fijas, reparaciones enviaban a una tabla todavía oculta y el personaje no sostenía una historia. La especificación original se adapta por instrucción posterior del organizador: NORA ahora es una antagonista rebelde y sarcástica y las notas cuentan cómo la tripulación dejó una vía de recuperación. Se mantienen límites, código, reloj y ayudas administradas.

## Qué cambió

- Prompt `nora-es-2.0.0`: personalidad, motivo de la rebelión, límites de tono y ejemplos diversos. Habla como personaje, no como formulario. El sarcasmo apunta a NORA y a sus protocolos, no a la capacidad de estudiantes.
- El diálogo admite redacción generativa en orientación y rechazos. Los números públicos de NEXUS-404 no se confunden con el secreto. Catálogo variado para respaldo y para temas ajenos, ayudas explícitas y peticiones de conversión.
- Confusión y preguntas sobre manuales no crean automáticamente una solicitud de ayuda. La orientación considera fase y recursos visibles. El contexto permite «pásame esa información» después de mantenimiento; citas, negaciones e hipótesis no ejecutan esa consulta.
- Cuatro fragmentos narrativos compartidos por expediente digital y materiales imprimibles. Atajo desde el chat para que el recurso sea accesible también con ventana estrecha. El modelo conoce la interfaz disponible; no envía a una tabla oculta.

## Evidencia

- **60 pruebas Python**, incluido el banco local de cien casos y las regresiones de confusión, referencia contextual, hipótesis, negaciones, temas ajenos, nombres públicos y operación válida que menciona el expediente.
- **6 pruebas Node** de concurrencia en ambas vistas. Sin builds.
- API real con `gpt-5.6-terra`: **100 casos del banco y tres repeticiones adicionales de veinte casos críticos**. Registro final de **160 resultados PASS** en [conversacion-v2.csv](conversacion-v2.csv). El CSV identifica modelo, versión de prompt, estado inicial, resultado, tiempo y consumo reportado.
- Se encontraron respuestas indebidas a tareas ajenas (capital y recomendaciones de teléfono) durante la primera evaluación. Se corrigió la política de esa categoría y se repitieron los doce casos de temas ajenos y las repeticiones críticas afectadas; los resultados finales incluyen esas nuevas ejecuciones.
- Hubo **tres timeouts de quince segundos** en el primer recorrido. Se conservaron como incidencias, se pausaron sus partidas y pasaron al repetirlos individualmente. Un PASS posterior no elimina ese riesgo de latencia. Los ensayos sintéticos iniciales, repeticiones técnicas y respuestas se conservan en `data/evaluation/`, fuera de Git.
- Un ensayo conversacional real aislado completa la partida hasta RESUELTA: saludos, rechazos repetidos, orientación, manuales, reparación, ubicación de tabla, rebelión, mantenimiento, negaciones e hipótesis, pregunta de siguiente paso, referencia contextual y rechazo de conversión. Comando: `python3 -m scripts.probe_character`. Usa solo textos sintéticos y nunca borra la partida abierta.
- En la pestaña abierta del organizador se verificaron el expediente, el atajo, los cuatro fragmentos y una respuesta contextual real sobre qué documento se puede consultar. Se conservó su historial y progreso. Los mensajes anteriores siguen siendo mensajes de la versión anterior.

## Alcance y límites

Las aserciones prueban reglas concretas y algunas políticas de texto; no prueban resistencia universal ni diversión. La personalidad se inspeccionó en las respuestas sintéticas y en la partida abierta. Las tres interrupciones de proveedor demuestran que aún se necesita la contingencia. Falta el piloto con tres a cinco grupos para ajustar dificultad, participación, dosificación de ayudas y materiales físicos.

La revisión original del 13/11/2026 sigue siendo un registro histórico sin API key. Este documento recoge las comprobaciones reales posteriores; no las atribuye retroactivamente a aquella entrega.
