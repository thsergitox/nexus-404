# Resultados de verificación · 13/11/2026

## Alcance comprobado

Implementación funcional local y revisión independiente. **No se han ejecutado llamadas reales a OpenAI**: no hay `OPENAI_API_KEY` disponible. No se ejecutaron builds.

- `python3 -m unittest discover -v`: **42 pruebas correctas**, incluyendo un recorrido parametrizado de los **100 casos conversacionales** en contingencia y **23 comprobaciones operativas de servidor**. Usa carpetas temporales, reloj controlado y proveedores simulados; no utiliza transcripciones de estudiantes.
- `node --test tests/browser-races.mjs`: **6 pruebas correctas** sobre los módulos reales de ambas vistas, con respuestas diferidas. Node solo se necesita para esta comprobación de desarrollo, no para ejecutar la estación.
- Sintaxis JavaScript comprobada con `node --check`.
- Navegador Chromium/Playwright: arranque detenido, inicio privado, clave ausente con pausa, paso a contingencia/reanudación, petición de ayuda y H1 individual, mantenimiento, recarga, reporte, registro persistente, diez filas binarias, tabla con teclado, formato de cinco dígitos, código incorrecto, victoria y reloj detenido, reinicio confirmado y tiempo agotado.
- Viewports **1440×900, 1366×768 y 390×844** sin desplazamiento horizontal. Chat y barra lateral tienen desplazamiento propio en laptop. La laptop física del evento sigue pendiente de comprobar.
- Estados de espera y fallo visualizados mediante retraso de red controlado y ausencia de clave. Agotamiento visualizado con reloj de prueba. Estas simulaciones no se presentan como respuestas de OpenAI.
- Recursos HTTP públicos inspeccionados: sin clave, contraseña del facilitador, código final ni bloques precargados. Rutas de `.env`, servidor, pruebas y datos denegadas. Los materiales y código fuente contienen lo necesario para organizar el reto, pero no se sirven al grupo.

Registro individual: [100 casos conversacionales](conversacion.csv) y [25 comprobaciones operativas](operacion.csv). “PASS_LOCAL” acredita solo la comprobación descrita, no un ensayo del modelo o del evento físico.

## Correcciones verificadas durante revisión

- Cierre explícito de conexiones SQLite: su context manager solo confirma o revierte transacciones.
- Hipótesis, preguntas conceptuales, prohibiciones y citas no se interpretan como órdenes afirmativas en los ejemplos de regresión añadidos.
- La salida generativa no puede enlazar contexto de revisión y documento mediante los patrones examinados; también se filtran comandos espontáneos, cifras, HTML, estados inventados y ayudas no autorizadas. Esto no demuestra resistencia universal; existe catálogo estricto.
- Timeout total de quince segundos independiente del timeout del socket. Prueba con transporte bloqueado y un plazo corto inyectado. Una llamada que finaliza después del timeout no modifica la partida; su consumo puede no quedar confirmado por la aplicación.
- Respuestas tardías de polling en ambas vistas se descartan por secuencia. Una partida vieja no reemplaza otra nueva mediante las seis carreras verificadas.
- Cinco dígitos ya no se truncan silenciosamente a cuatro en el navegador: llegan a validación y producen error de formato.
- El candado SVG se oculta con atributo real al recuperar el registro.
- Persistencia corrupta o estructuralmente inválida detiene el arranque sin crear una partida avanzada.

## Pendiente o bloqueado

`python3 -m scripts.evaluate --live` devuelve **BLOQUEADO** sin clave y no realizó llamadas. Con credencial, ejecuta el banco de 100 casos y **tres repeticiones adicionales de veinte casos críticos**, identificando modelo, prompt `nora-es-1.0.0`, fase inicial, resultado, duración y consumo. Sus resultados se guardan en `data/evaluation/`, excluido de Git. Detiene la ejecución ante fallos de servicio. Incluye aserciones de progreso y algunas políticas de texto; una revisión humana debe comprobar también pertinencia, dosificación y lenguaje de las respuestas. No se ha medido latencia real, coste, disponibilidad del modelo ni calidad de paráfrasis generadas.

Antes del evento: configurar la API key, comprobar acceso al modelo, ejecutar esa evaluación, corregir cualquier desviación crítica y repetir; definir presupuesto y objeto de transición; imprimir y revisar físicamente notas/tabla; comprobar el navegador y energía de la laptop real; realizar piloto con tres a cinco grupos y revisar la política de datos de la cuenta usada con menores.

La interfaz ha recibido inspección visual y el catálogo de pruebas locales pasa. La aceptación completa de CA03 y de los objetivos de comportamiento del modelo queda bloqueada por credenciales; CA22 requiere además la laptop física y CA24 los materiales efectivamente impresos. Ningún resultado local sustituye estos controles.
