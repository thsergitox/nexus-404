# Diseño y plan de implementación
Fuente de requisitos: NEXUS-404_Especificacion_MVP.md v1.0, entregada por el organizador. El antecedente preliminar no gobierna este proyecto.

## Decisiones
Un servicio Python 3.11+ con biblioteca estándar y SQLite. No requiere paquetes, bundler ni compilación; simplifica la operación local. A cambio, HTTP, validación y sesiones se implementan explícitamente y se prueban. Se limita a loopback; un despliegue público requiere otro servidor HTTP y TLS.

HTML/CSS y módulos JavaScript nativos permiten una interfaz rápida sin build. Frente a React, evitan dependencias y aportan menos herramientas para grandes interfaces; este producto tiene dos vistas pequeñas.

Responses API por HTTPS, sin SDK. Salida JSON Schema estricta y validación independiente. El modelo interpreta y conversa; reglas conservadoras resuelven operaciones reconocidas y vetan negaciones, citas, mezclas y administración. El modo de catálogo estricto conserva interpretación por API y limita redacción. La contingencia funciona sin API y está identificada.

SQLite conserva una partida, reloj absoluto, métricas sin textos y consumo agregado del evento. Transacciones y bloqueo serializan mutaciones; la llamada externa no bloquea administración. Cada turno lleva game_id e id; un resultado tardío se descarta después de reset, pausa o cambio de operación.

## Secuencia
- [x] Motor de juego, almacenamiento atómico, reloj y proyección pública.
- [x] Intenciones, prompt versionado, transporte OpenAI y salidas seguras.
- [x] HTTP local, autenticación, sesiones, límites y control privado.
- [x] Consola de jugador y facilitador, estados y accesibilidad.
- [x] Cien casos de referencia y veinticinco controles, fallos y carreras.
- [x] Materiales imprimibles, guía y revisión visual; publicación autorizada como paso final.

## Focos de revisión
Negación de otra acción (A68), cita de órdenes, reporte antes del modo, respuesta tardía tras reinicio y fallo durante pausa. Revisar también dobles envíos, corrupción, consumo, HTML, ausencia de credenciales y acceso directo a endpoints privados.

## Verificación
Pruebas con unittest y HTTP real local, reloj inyectable y proveedor simulado, separadas de evaluación OpenAI explícita. Script real bloquea sin clave y registra modelo, prompt y duración sin conservar textos reales de estudiantes. Verificación visual en servidor de desarrollo, laptop y móvil. NUNCA ejecutar builds.
