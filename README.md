# NORA · NEXUS-404

Estación de escape room de ACECOM para cinco estudiantes de secundaria. Una laptop, quince minutos, cuatro notas y una conversación con una computadora de navegación.

**Servicio local funcional, sin compilación ni dependencias externas.** La conversación principal está conectada a Responses API desde el servidor. Sin API key se puede ensayar el recorrido en contingencia local, identificada explícitamente.

## Arranque

Requiere Python **3.11 o superior**, con SQLite, y un navegador moderno. No se ejecuta ningún build.

```bash
git clone https://github.com/thsergitox/nexus-404.git
cd nexus-404
python3 -m nora setup
python3 -m nora
```

Abra [la consola del grupo](http://localhost:4040) y, en otra pestaña, [el control privado](http://localhost:4040/facilitador). `setup` genera una contraseña aleatoria en `.env`, con permiso 600, sin imprimirla. Consulte `FACILITATOR_PASSWORD` localmente para iniciar sesión. `setup` nunca reemplaza un archivo existente. Puede partir de `.env.example` si prefiere configurar una credencial propia de al menos 16 caracteres.

En el control privado: seleccione el modo de comunicación, presente la misión y pulse **Iniciar misión**. La vista del grupo no tiene controles de administración. Antes de ceder la laptop, cierre la pestaña privada y su sesión.

## OpenAI

Configure `OPENAI_API_KEY` en `.env` o en el entorno **del servidor**, nunca en JavaScript del navegador ni en el chat. Reinicie el servicio después de cambiar configuración. Las variables del entorno tienen prioridad sobre `.env`. El lector de `.env` acepta `NOMBRE=valor` literal: no use `export`, comillas ni comentarios al final del valor.

`OPENAI_MODEL=gpt-5.6-terra` es el punto de partida configurable, documentado con soporte Responses y Structured Outputs. La disponibilidad en su cuenta, latencia, adecuación al español y coste **requieren comprobación real**. La configuración usa `reasoning.effort=none`; otro modelo debe admitir ese parámetro y salida estructurada, o requiere adaptar `nora/conversation/provider.py`.

El servidor solicita JSON Schema estricto, valida el resultado y controla todos los cambios de estado. Solo permite redacción generativa breve para conversación admitida; los eventos críticos utilizan mensajes aprobados. Las operaciones principales se reconocen por intención y contexto, sin exigir una oración exacta. Las formulaciones no reconocidas se piden reformular de manera conservadora.

`NORA_STRICT_CATALOG=1` conserva la interpretación mediante OpenAI y selecciona todas las respuestas visibles desde catálogo. Ante un fallo se pausa el reloj; el facilitador puede activar contingencia y **Reanudar**. No se cambia silenciosamente a respuestas locales para simular una llamada real.

## Consumo y datos

`EVENT_TOKEN_LIMIT=0` significa **sin límite propio configurado**. El organizador puede elegir un umbral de tokens de entrada + salida por evento. Se mide consumo reportado por API, también en respuestas inválidas que incluyen usage. Al siguiente turno después de alcanzar el umbral se pausa y pasa a contingencia. Una petición en curso puede exceder el umbral; las llamadas sin respuesta pueden tener consumo no confirmado. No es un tope monetario exacto. Revise tarifas y límites de su cuenta y mida el piloto antes de estimar el presupuesto.

`data/station.sqlite3` conserva la partida y el plazo en servidor. Recargar no reinicia el reloj. Reiniciar elimina conversación y ayudas del grupo y conserva solo métricas sin texto libre y consumo agregado. No hay nombres, cuentas, telemetría ni logs de conversación por defecto. Los mensajes enviados a OpenAI salen de la laptop; el organizador debe revisar la política de datos de su cuenta antes de trabajar con menores. `store=false` no constituye una garantía sobre todas las políticas de retención del proveedor.

`.env`, `data/`, capturas de ensayo y cachés están excluidos de Git. El servidor sirve únicamente recursos web enumerados: no publica código Python, pruebas, datos, materiales o documentos con solución. El repositorio fuente sí contiene la solución del reto; no entregue su enlace a participantes antes de jugar.

## Verificación

```bash
python3 -m unittest discover -v
# Opcional: Node 22+ para las carreras de actualización del navegador
node --test tests/browser-races.mjs
python3 -m scripts.evaluate --live
```

El comando unittest verifica las reglas y los 100 casos en contingencia, contratos HTTP/OpenAI y fallos con proveedores simulados. El comando evaluate **hace llamadas con coste**: ejecuta el banco y repite tres veces veinte casos críticos; guarda resultados sintéticos en `data/evaluation/`. Requiere clave y detiene la evaluación ante un fallo de servicio. No confunda pruebas simuladas con una evaluación del modelo real. Véase [el informe de verificación](docs/verification/RESULTADOS.md).

## Operación y materiales

- [Guía del facilitador](docs/FACILITADOR.md): preparación, ayudas, contingencia, reinicio y recuperación.
- [Cuatro notas imprimibles](materials/notas.html): abrir en navegador e imprimir en A4 al 100 %.
- [Tabla binaria imprimible](materials/tabla.html): las diez equivalencias, sin destacar la combinación.
- [Diseño y decisiones técnicas](docs/IMPLEMENTATION.md): arquitectura y tradeoffs.

El servicio escucha exclusivamente en `127.0.0.1`. Está pensado para una estación local, **no para exponer este servidor HTTP en Internet**. La autenticación usa contraseña comprobada en servidor, sesión opaca con expiración, cookie HttpOnly/SameSite, límite de intentos y comprobación de origen/Host. Una persona con acceso al sistema operativo puede leer archivos locales: la vista privada no sustituye el control físico de la laptop. No ejecute dos instancias contra la misma carpeta de datos.

Pendiente antes del evento: configurar y evaluar OpenAI, comprobar la laptop y los materiales físicos reales, definir presupuesto/objeto de transición y realizar el piloto de tres a cinco grupos.
