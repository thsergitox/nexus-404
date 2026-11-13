---
name: NORA · NEXUS-404
description: Consola de navegación legible para una estación de escape room compartida.
colors:
  bg: "#090f18"
  surface: "#111c29"
  raised: "#172536"
  line: "#2b3b4d"
  text: "#ecf2f5"
  muted: "#a7b7c8"
  lime: "#d0ec8e"
  blue: "#9dd9f5"
  warning: "#ffd294"
  error: "#ffb4aa"
typography:
  body:
    fontFamily: '"Segoe UI", Arial, sans-serif'
    fontSize: "16px"
    lineHeight: 1.5
  message:
    fontFamily: '"Segoe UI", Arial, sans-serif'
    fontSize: "1.0625rem"
    lineHeight: 1.7
  title:
    fontFamily: '"Segoe UI", Arial, sans-serif'
    fontSize: "1.625rem"
    fontWeight: 650
    lineHeight: 1.15
    letterSpacing: ".035em"
  timer:
    fontFamily: "ui-monospace, Consolas, monospace"
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

**Creative North Star: "Consola de navegación compartida"**

Una computadora de nave sobria y legible para una laptop compartida. La identidad ACECOM y NEXUS-404 convive con superficies continuas, divisores finos y un diagrama orbital geométrico; el contenido y las acciones llevan la atención.

El sistema distingue estados mediante texto y color. La interfaz permanece estable durante la conversación, conserva los recursos autorizados y evita que los adornos compitan con la lectura.

**Key Characteristics:**
- Superficies oscuras con capas tonales y divisores finos.
- Texto de interfaz sans-serif; monospace reservado para datos.
- Acento lima para acciones y azul para NORA y recursos.
- Estados explícitos, controles de teclado y movimiento reducido.

## Colors

Lima para acciones primarias y confirmaciones; azul para NORA, enlaces y bloques autorizados. Fondo, superficie y capa elevada organizan la profundidad. El texto secundario mantiene lectura sobre ambas superficies; los bordes separan regiones. Advertencia y error siempre acompañan mensajes explícitos. Los valores normativos están en el frontmatter.

## Typography

La pila de interfaz usa Segoe UI con Arial y sans-serif de respaldo; no se descarga ninguna fuente. El cuerpo base tiene interlineado cómodo. Los mensajes crecen a 18px desde 1500px y bajan a 16px en móvil. El reloj usa numerales tabulares; los bloques y el campo de validación utilizan monospace. El título móvil baja a 1.2rem y el reloj a 1.6rem. El pie de página y las instrucciones móviles usan 12px; las etiquetas de autor son secundarias y menores.

## Layout

La vista de jugadores usa un contenedor de hasta 1680px, con altura del viewport y mínimo de 600px. Cabecera, espacio de trabajo y pie forman una columna. El espacio de trabajo distribuye chat y recursos en proporción 2.35:1, con barra lateral de al menos 310px. El chat y la barra tienen desplazamiento independiente; el campo permanece debajo de los mensajes.

Desde 1500px aumentan los márgenes laterales a 48px. Hasta 1000px se reducen a 20px y la rejilla pasa a 1.8:1. Hasta 700px el contenido se apila, con márgenes de 16px y chat de 560px limitado al 80% del viewport. El control privado tiene máximo de 1240px, dos columnas y pasa a una hasta 750px.

## Elevation & Depth

La profundidad procede de capas tonales y divisores de 1px. Los paneles permanecen planos. Solo el aviso flotante de mensajes nuevos usa sombra suave (0 4px 16px #0005). El diálogo de reinicio oscurece el fondo para proteger una acción administrativa.

## Shapes

Controles de bordes suavemente curvos; mensajes y paneles privados con curvas más amplias. Los mensajes de tripulación conservan una esquina recta para marcar su origen. Los bloques son rectángulos compactos; los símbolos orbitales son geometría vectorial limpia, sin representar materiales físicos.

## Components

- Botón primario: lima sobre fondo oscuro, alto mínimo de 44px y cambio de fondo al pasar el puntero. Secundario transparente con borde fino. Acción destructiva con texto y borde de error. Los controles deshabilitados bajan su opacidad al 48%.
- Campos: fondo oscuro, borde fino, relleno cómodo y cursor lima. El foco de botones, campos, enlaces y resumen de tabla usa contorno lima de 2px separado 4px; el textarea integra su contorno sin separación exterior.
- Chat: autor explícito, texto con saltos conservados y ajuste de palabras largas. La tripulación usa una superficie elevada; los eventos de sistema se distinguen por texto lima. El aviso de mensajes nuevos permite volver al final sin interrumpir la lectura anterior.
- Recursos: ayudas individuales, registro persistente y tabla desplegable. La consola muestra errores generales mediante texto y se bloquea cuando la estación está detenida.
- Estados: espera con aviso de respuesta; interrupción y pausa con aviso ámbar; victoria con aviso lima y ruta orbital continua. La animación no comunica información esencial y se respeta movimiento reducido.

## Do's and Don'ts

### Do
- Do acompañar el color de estado con texto explícito.
- Do reservar monospace para reloj, bloques y otros datos.
- Do conservar foco visible, campo de escritura y desplazamiento independiente del chat.
- Do identificar la contingencia local y mantener visibles los recursos ya autorizados.

### Don't
- Don't mostrar información del registro antes de la autorización del servidor.
- Don't usar animación o sonido como requisito para entender un estado.
- Don't introducir texturas, halos o ilustraciones que compitan con el chat.
