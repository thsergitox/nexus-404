# Fuentes técnicas consultadas

Consulta: 13 de noviembre de 2026. No hay dependencias de terceros en ejecución.

- [OpenAI API overview](https://developers.openai.com/api/reference/overview): autenticación del servidor y uso HTTP directo.
- [Responses create](https://developers.openai.com/api/reference/resources/responses/methods/create): endpoint, instrucciones, mensajes, estado de salida y consumo.
- [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs): `text.format`, JSON Schema estricto, negativas y salidas incompletas. Un esquema no verifica semántica ni permisos.
- [GPT-5.6 Terra](https://developers.openai.com/api/docs/models/gpt-5.6-terra): modelo configurable de partida, soporte Responses, Structured Outputs y razonamiento `none`. Falta confirmar acceso en la cuenta del evento y comportamiento real.
- [Python HTTP server](https://docs.python.org/3.13/library/http.server.html): servidor con hilos; limitado a loopback por su alcance local.
- [Python sqlite3](https://docs.python.org/3.13/library/sqlite3.html): transacciones y cierre explícito de conexiones. `with connection` no cierra por sí mismo.
- [Python urllib.request](https://docs.python.org/3.13/library/urllib.request.html): peticiones HTTPS y timeout por operación; la aplicación añade un límite total independiente.
- [Python hashlib](https://docs.python.org/3.13/library/hashlib.html): scrypt y hashing de identificadores de solicitud.

Requisitos de producto: especificación NEXUS-404_Especificacion_MVP.md v1.0 del organizador y su propuesta PDF original. El plan preliminar sustituido no se usó como fuente de requisitos.

Revisión del 16/11/2026: [OpenAI Prompt Personalities](https://developers.openai.com/cookbook/examples/gpt-5/prompt_personalities) y [Prompt Engineering](https://developers.openai.com/api/docs/guides/prompt-engineering). Se adaptaron identidad, motivación, voz y ejemplos de interacción al personaje original NORA; no se copió un prompt de un personaje ajeno.
