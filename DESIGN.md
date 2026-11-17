---
name: NORA · NEXUS-404
description: Puente de mando holográfico para una estación de escape room compartida.
colors:
  bg: "#03060c"
  surface: "#0a1322"
  raised: "#112038"
  line: "#1c3352"
  text: "#e6f2ff"
  muted: "#8ea7c4"
  lime: "#c6f36b"
  blue: "#6ef2ff"
  warning: "#ffb547"
  error: "#ff7a86"
typography:
  body:
    fontFamily: '"Chakra Petch", "Segoe UI", Arial, sans-serif'
    fontSize: "16px"
    lineHeight: 1.5
  message:
    fontFamily: '"Chakra Petch", "Segoe UI", Arial, sans-serif'
    fontSize: "1.0625rem"
    lineHeight: 1.7
  title:
    fontFamily: '"Chakra Petch", "Segoe UI", Arial, sans-serif'
    fontSize: "1.625rem"
    fontWeight: 650
    lineHeight: 1.15
    letterSpacing: ".035em"
  timer:
    fontFamily: '"JetBrains Mono", ui-monospace, Consolas, monospace'
    fontSize: "2.125rem"
    fontWeight: 500
    letterSpacing: "-.03em"
rounded:
  control: "8px"
  message: "12px"
  block: "5px"
spacing:
  compact: "8px"
  control: "12px"
  regular: "16px"
  section: "24px"
  page: "32px"
components:
  button-primary:
    backgroundColor: "{colors.lime}"
    textColor: "{colors.bg}"
    rounded: "{rounded.control}"
    padding: "10px 16px"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.text}"
    rounded: "{rounded.control}"
    padding: "10px 16px"
  button-danger:
    backgroundColor: "transparent"
    textColor: "{colors.error}"
    rounded: "{rounded.control}"
    padding: "10px 16px"
  input:
    backgroundColor: "{colors.bg}"
    textColor: "{colors.text}"
    rounded: "{rounded.control}"
    padding: "12px"
  panel:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.message}"
    padding: "24px"
---

# Design System: NORA · NEXUS-404

## Overview

**Creative North Star: "Puente de mando holográfico"**

La pantalla es el puente de NEXUS-404 visto a través de cristal: paneles translúcidos con soportes de esquina HUD flotan sobre un espacio 3D vivo (campo estelar en perspectiva y un planeta en malla que rota con la estación en órbita). NORA habla por un canal de radio: sus respuestas llegan como transmisión que se decodifica; la tripulación transmite al instante. Referencias: interfaces FUI de *The Expanse*, *Prometheus* y Star Citizen.

El estado de la partida cambia el mundo entero: crucero en cian, alerta roja bajo dos minutos y salto hiperespacial en lima al restaurar la trayectoria.

**Key Characteristics:**
- Paneles de cristal (`--glass`) con soportes de esquina; el fondo 3D se ve a través.
- Chakra Petch para interfaz y lectura; JetBrains Mono para datos, canales y reloj.
- Cian para NORA, lima para la tripulación y las acciones, ámbar y rojo para alertas.
- Estados explícitos en texto; todo efecto se apaga con movimiento reducido.

## Colors

Cian (`blue`) identifica a NORA, su núcleo y el mundo en crucero. Lima marca a la tripulación, las acciones primarias y la victoria. Ámbar señala bloqueos y avisos; rojo (`error`) la alerta de tiempo y errores. El vacío (`bg`) y el cristal translúcido organizan la profundidad. Los valores normativos están en el frontmatter.

## Typography

Fuentes locales en `web/fonts/` (OFL), servidas por el propio servidor para respetar la CSP `'self'` y funcionar sin red. Chakra Petch (400/600/700) para títulos, cuerpo y mensajes; JetBrains Mono (variable) para reloj, etiquetas de canal, bloques binarios y registro. Etiquetas en mayúsculas con espaciado amplio; mensajes a 17px (18px desde 1500px, 16px en móvil).

## Layout

Contenedor de hasta 1680px con altura del viewport (mínimo 640px). Cabecera HUD, espacio de trabajo y pie forman una columna con separación de 12px entre paneles. Chat y recursos en proporción 2.35:1 (barra lateral mínima de 330px). Los mensajes de la tripulación se alinean a la derecha y los de NORA a la izquierda; los del sistema, centrados. Hasta 1250px desaparece la telemetría decorativa; hasta 1000px el estado de conexión; hasta 700px el contenido se apila.

## Elevation & Depth

Tres planos: el canvas 3D (`web/space.js`), la atmósfera de nebulosa y viñeta, y los paneles de cristal. Una capa de líneas de barrido muy tenue cubre la pantalla. Los resplandores (`--glow-*`) se reservan para elementos vivos: NORA, cursor de transmisión, reloj, acciones.

## Shapes

Esquinas casi rectas (2px). El botón primario tiene cortes diagonales en dos esquinas. NORA usa burbuja con esquina superior izquierda recta y borde cian; la tripulación, esquina superior derecha recta y borde lima. Los paneles llevan soportes de esquina dibujados con gradientes.

## Components

- Arranque: la mascota de ACECOM con la pantalla de su laptop encendida y una secuencia de carga de ~3 s; se salta con cualquier tecla o clic y solo aparece una vez por pestaña.
- Cabecera: mascota con pantalla "404", título con glitch ocasional, telemetría decorativa y reloj con anillo de progreso.
- Núcleo de NORA: anillos en 3D CSS alrededor de un corazón luminoso; acelera mientras se recibe señal.
- Chat: el mensaje de la tripulación aparece al instante (estado "enviando") y se confirma con la respuesta del servidor. La respuesta de NORA se materializa y se decodifica carácter a carácter (`web/transmission.js`) con ruido de glifos y cursor; lectores de pantalla reciben el texto completo de una vez.
- Recursos: bóveda con escáner mientras el registro está bloqueado; bloques binarios que aparecen escalonados al liberarse.
- Estados: alerta roja bajo 2 minutos (marcos, reloj y planeta en rojo); victoria con salto hiperespacial y todo en lima.

## Do's and Don'ts

### Do
- Do acompañar el color de estado con texto explícito.
- Do mantener legibles los mensajes sobre el cristal: el fondo 3D es atmósfera, no contenido.
- Do conservar foco visible, campo de escritura y desplazamiento independiente del chat.
- Do respetar `prefers-reduced-motion`: sin arranque, transmisión instantánea y escena 3D estática.

### Don't
- Don't mostrar información del registro antes de la autorización del servidor.
- Don't cargar recursos externos: la CSP solo permite `'self'`.
- Don't usar animación o sonido como requisito para entender un estado.

El expediente de la tripulación amplía el sistema de recursos: un atajo textual desde el chat abre el desplegable de misión y lleva el foco a su cabecera. Los cuatro artículos reutilizan divisores, cuerpo legible y firma azul. También existen en impresión con fondo blanco.
