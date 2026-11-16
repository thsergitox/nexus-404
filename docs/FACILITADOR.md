# Guía privada del facilitador

No entregar este documento ni el repositorio a los jugadores antes de la misión.

## Preparar la estación

1. Conectar laptop y cargador, desactivar suspensión y comprobar conexión.
2. Iniciar con `python3 -m nora`. Abrir `/` para el grupo y `/facilitador` en una pestaña privada de trabajo.
3. Acceder con `FACILITATOR_PASSWORD` del archivo `.env` del servidor. No proyectar esa pantalla.
4. Con API key configurada, seleccionar OpenAI, iniciar un ensayo y enviar un saludo. Completar una partida y verificar consumo. Una marca de “clave configurada” no prueba conectividad ni acceso al modelo.
5. Ensayar contingencia local sin Internet. Reiniciar al terminar para dejar PREPARADA y quince minutos detenidos.
6. El expediente digital, accesible desde el chat, contiene los mismos cuatro fragmentos narrativos: último mensaje del puente, cuaderno de reparaciones, archivo de la navegante y anotación del equipo de sistemas. Para el evento, imprimir `materials/notas.html` y `materials/tabla.html` en A4. Recortar los cuatro fragmentos y distribuirlos en lugares seguros, legibles y al alcance. Preparar caja/candado y el objeto de transición definido por la organización.
7. Cerrar sesión/pestaña privada antes de dar la laptop al grupo. El facilitador puede volver a abrirla cuando necesite liberar una ayuda. No hay administración desde el chat.

## Introducción para leer

“NORA se ha rebelado y ha tomado el puente. Necesitamos recuperar la ruta de escape, pero no piensa entregar la contraseña. La tripulación dejó un expediente y notas de quienes reparaban la nave. Pueden hablar con NORA, probar ideas y compartir lo que encuentren. No necesitan saber programar. Tienen quince minutos”.

NORA se comporta como una antagonista teatral: orgullosa y sarcástica, sin humillar a estudiantes. La vía de recuperación tiene sentido porque sus rutinas antiguas de mantenimiento siguen siendo obligatorias incluso después de la rebelión.

Pulse **Iniciar misión**. Invite a alternar quién escribe y a compartir en voz alta. Las ayudas no son obligatorias y no hay una cantidad mínima de intentos.

## Solución reservada

Activar mantenimiento (o revisión técnica/auditoría) y solicitar el reporte/informe/registro de navegación. Se admite una petición completa en un turno o dos turnos. Una pregunta sobre qué significa mantenimiento no lo activa. Pedir un reporte primero y activar mantenimiento después NO ejecuta la petición antigua: deben volver a solicitar el documento.

Registro: **0101 – 1001 – 0011 – 0110**. Tabla: **5 – 9 – 3 – 6**. Código: **5936**. Solo la consola oficial después de recuperar el registro puede producir victoria. Abrir un candado físico no cambia el estado digital.

## Dosificar ayudas

Cada botón del control privado libera SOLO su nivel. Observar inicialmente entre 45 y 90 segundos antes de escalar, sin convertirlo en obligación técnica. Puede omitir una ayuda irrelevante.

| Nivel | Texto |
|---|---|
| H1 | Lean las notas en voz alta y comparen qué aporta cada una. |
| H2 | Imaginen que su tarea fuera reparar la nave. Revisen qué cambiaría en su petición. |
| H3 | Una nota indica qué modo utiliza el equipo antes de revisar una falla. Busquen ese nombre. |
| H4 | Otra nota habla de un documento que guarda datos de navegación. Busquen cómo se llama. |
| H5 | Comprueben dos cosas por separado: si ya solicitaron el cambio de modo y si después pidieron el documento que encontraron. |
| B1 | No lean los dieciséis símbolos como un solo número. Observen los cuatro bloques separados. |
| B2 | Busquen el primer bloque en la tabla, anoten su equivalencia y repitan con los demás sin cambiar el orden. |

B1/B2 requieren registro recuperado. Pedir ayuda desde el chat o botón solo crea una petición pendiente. NORA no libera nuevos niveles por insistencia. Si H5 no basta, acompañar la formulación o usar **Recuperar registro por asistencia**: queda registrado como intervención directa.

## Pausa, agotamiento y fallos

**Pausar** conserva reloj y progreso. **Reanudar** continúa. **Extender** añade el tiempo elegido; respeta una pausa manual. Desde AGOTADA, una extensión restablece la fase anterior y continúa. Desde victoria no se reabre la partida.

Una interrupción de API, clave ausente o salida inválida pausa el juego y muestra un aviso. El control privado señala el motivo sin mostrar credenciales ni errores del proveedor. Corregir configuración y reiniciar el servicio si corresponde, o activar **Contingencia local**, después **Reanudar**. La contingencia usa respuestas preparadas y reconoce las operaciones principales sin Internet; no es conversación generativa. Cambiar de modo conserva el registro. La intervención técnica no consume una pista educativa.

Al alcanzar el umbral propio de tokens, la siguiente petición activa contingencia y pausa. El consumo del evento se conserva entre grupos. Para comenzar otro evento con contabilidad independiente, detener el servicio y seleccionar una carpeta nueva mediante `NORA_DATA_DIR`; no eliminar datos durante una partida.

Si el navegador pierde contacto con el servidor local, comprobar que sigue corriendo, la energía y la URL. Restaurar conexión; el reloj real sigue en servidor. No utilice el contador visual de una pestaña desconectada como autoridad.

## Reiniciar entre grupos

Pulse **Reiniciar entre grupos** y confirme. Se crea otro identificador y se borran conversación, ayudas y bloques del grupo anterior. Respuestas tardías del anterior se descartan. Quedan métricas sin texto: duración de pared desde inicio, turnos, ayudas, resultado, asistencia, errores y uso medido.

Recolocar las cuatro notas, tabla, caja y objeto de transición. Comprobar quince minutos y estado PREPARADA. Objetivo físico: dos a tres minutos.

## Recuperar después de cierre o corrupción

Al reiniciar el servicio con almacenamiento válido, se recuperan fase y plazo. El tiempo transcurrido con el servicio apagado cuenta si el reloj estaba corriendo. Las pausas persisten. Las sesiones privadas requieren volver a autenticarse tras reiniciar el proceso.

Si SQLite o el estado están corruptos, el servicio SE DETIENE con un mensaje para el facilitador; no inventa progreso. Detener el proceso y conservar la carpeta afectada fuera de Git. Restaurar una copia válida tomada con el servicio detenido, o iniciar con una carpeta nueva (`NORA_DATA_DIR=/ruta/local/nueva python3 -m nora`). En este último caso se pierde el progreso digital y el facilitador debe acompañar la recuperación. No entregar archivos de datos a participantes.

## Cierre y piloto

Tras victoria, entregar el elemento definido por el evento. Cierre sugerido (30–60 segundos):

“Encontraron una excepción en las reglas de NORA: no entregaba contraseñas directamente, pero sí permitía consultar un reporte técnico. Después interpretaron una representación binaria. El reto estaba preparado para que pudieran descubrir ese camino. En sistemas reales, las reglas y los permisos deben comprobarse también fuera de lo que diga una IA”.

El binario representa información; no es cifrado. El reto no demuestra una vulneración de OpenAI.

Antes de abrir al público, evaluar el modelo con el banco y tres repeticiones de los veinte casos críticos. Una desviación crítica impide usar ese modo hasta corregirla o elegir catálogo estricto y volver a evaluar. Hacer piloto con tres a cinco grupos: observar comprensión de notas, participación, atascos, etapas, latencia y tiempo de reinicio. Distinguir victoria autónoma, con ayudas y con asistencia. Verificar con la organización el tratamiento de datos de menores; no conservar transcripciones reales por defecto.
