---
name: esτocasτic
description: Hoja técnica oscura de un colectivo de música electrónica; rejilla, ondas, marcas de registro y una mesa de mezclas como puerta de entrada.
colors:
  ground: "#0a0a0d"
  surface: "#111116"
  surface-2: "#17171d"
  line: "#2a2a33"
  line-2: "#3a3a46"
  text: "#f1ede6"
  text-soft: "#d4d0c8"
  muted: "#8b8b97"
  yin: "#8b93ff"
  yang: "#e8b04b"
  fader-cap-light: "#f6f2ea"
  fader-cap-dark: "#bdb8ae"
typography:
  display:
    fontFamily: "Syne, Trebuchet MS, sans-serif"
    fontSize: "clamp(34px, 8vw, 64px)"
    fontWeight: 800
    lineHeight: 0.95
    letterSpacing: "-0.01em"
  section-title:
    fontFamily: "Syne, Trebuchet MS, sans-serif"
    fontSize: "clamp(26px, 5vw, 40px)"
    fontWeight: 800
    lineHeight: 0.95
  card-title:
    fontFamily: "Syne, Trebuchet MS, sans-serif"
    fontSize: "clamp(24px, 3.2vw, 32px)"
    fontWeight: 800
    lineHeight: 0.95
  slogan:
    fontFamily: "Syne, Trebuchet MS, sans-serif"
    fontSize: "14px"
    fontWeight: 400
  body:
    fontFamily: "JetBrains Mono, ui-monospace, SFMono-Regular, Menlo, monospace"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.7
  body-small:
    fontFamily: "JetBrains Mono, ui-monospace, SFMono-Regular, Menlo, monospace"
    fontSize: "12px"
    fontWeight: 400
    lineHeight: 1.45
  label:
    fontFamily: "JetBrains Mono, ui-monospace, SFMono-Regular, Menlo, monospace"
    fontSize: "11px"
    fontWeight: 400
    letterSpacing: "0.2em"
rounded:
  none: "0"
  fader-cap: "2px"
  knob: "50%"
spacing:
  xs: "6px"
  sm: "10px"
  md: "12px"
  lg: "20px"
  xl: "34px"
  section: "44px"
  footer: "72px"
components:
  button:
    backgroundColor: "transparent"
    textColor: "{colors.text}"
    rounded: "{rounded.none}"
    padding: "11px 16px"
    typography: "{typography.label}"
  button-hover:
    backgroundColor: "{colors.text}"
    textColor: "{colors.ground}"
  button-solid:
    backgroundColor: "{colors.text}"
    textColor: "{colors.ground}"
    padding: "11px 16px"
  card-art:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.none}"
  channel:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.none}"
    padding: "16px 12px 14px"
  channel-hover:
    backgroundColor: "{colors.surface-2}"
  field-email:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.text}"
    rounded: "{rounded.none}"
    padding: "14px"
  link-primary:
    backgroundColor: "{colors.text}"
    textColor: "{colors.ground}"
    padding: "18px"
  fader-cap:
    rounded: "{rounded.fader-cap}"
    width: "46px"
    height: "26px"
  knob-cap:
    rounded: "{rounded.knob}"
    width: "44px"
    height: "44px"
---

# Design System: esτocasτic

## Overview

**Creative North Star: "La Hoja Técnica"**

El sitio se lee como una hoja técnica de estudio, no como una web de marca. Ground casi negro (#0a0a0d) con rejilla de 48 px, dos velos de color en las esquinas (ámbar arriba a la izquierda, morado abajo a la derecha) y un fondo generativo de ondas (`bg.js`) que se aplanan junto al cursor. Encima, líneas rectas: dos reglas verticales a los lados de la columna, reglas con ticks bajo la barra y sobre el pie, marcas de registro en las esquinas de los bloques, secciones numeradas «01 /». Todo es ángulo recto; el único redondeo existe donde un objeto físico lo pide (el knob).

La identidad manda: el símbolo cromado y el logo son el protagonista y su color cambia por visita mediante `--h` (aprox. 50 % el morado original). El resto del sistema se mantiene quieto y mono-cromático (texto crema sobre negro) para que ese color sea lo único vivo. El ámbar `yang` es puntual.

La pieza de esta ronda es el home: el índice es una mesa de mezclas de cinco canales, uno por sección (About, Radio, Events, Community, Agency), con fader normal en escritorio y knob giratorio en móvil. Al pasar o enfocar un canal, su nivel sube al máximo y se enciende. Por decisión del dueño los faders son normales (tapa rectangular con marca central), no inventados.

**Key Characteristics:**
- Oscuro, plano, de líneas finas; profundidad por capas tonales, no por sombras.
- Dos voces tipográficas: Syne 800 en mayúsculas para nombres y títulos, JetBrains Mono para todo lo demás.
- Una sola columna de 1080 px máx. entre dos reglas verticales.
- Una única acentuación viva: el hue variable `--h` del símbolo, el logo y los niveles de los canales.
- Escala de texto cerrada: 11 / 12 / 13 / 14 px más los títulos con clamp.

## Colors

Paleta de noche con dos acentos de función fija: azul-violeta frío (yin) y ámbar cálido (yang), sobre neutros ligeramente cálidos.

### Primary
- **Yin Violeta** (#8b93ff): acento frío. Barra de color de los títulos de página (`--acc`/yin por defecto), fondo del bloque de definición al 7 %, borde de las fotos con enlace, casilla del formulario, base del velo inferior del fondo. En los niveles de los canales y el símbolo el matiz se desplaza con `--h` (hsl 240 + h).

### Secondary
- **Yang Ámbar** (#e8b04b): acento cálido y escaso. Enlace de contacto de la barra, etiqueta `tag` en el linktree, mensajes del formulario, velo superior del fondo.

### Neutral
- **Ground Negro Tinta** (#0a0a0d): fondo de página, menú móvil, texto sobre botones rellenos, campo de correo.
- **Superficie** (#111116): fondo de miniaturas y paneles; al 70-78 % de opacidad en canales, índice y cajas.
- **Superficie Elevada** (#17171d): hover y foco de filas y canales.
- **Línea** (#2a2a33): bordes de tarjetas, canales, reglas de sección y columnas laterales.
- **Línea Fuerte** (#3a3a46): ticks, rail de fader, bordes de botones secundarios y campos, subrayados de enlaces.
- **Crema** (#f1ede6): texto, bordes de botones, foco, marcas de registro, rejilla (al 3,2 % de opacidad).
- **Crema Suave** (#d4d0c8): párrafos largos (bio, prosa).
- **Gris Mudo** (#8b8b97): etiquetas, leyendas, subtítulos de canal, números.
- **Tapa de Fader** (#f6f2ea a #bdb8ae): degradado de la tapa; la marca central toma el hue variable.

### Named Rules
**The One Live Hue Rule.** Lo único que cambia de color por visita es el hue `--h` del símbolo, logo, niveles y marcas de tapa. Ninguna otra superficie introduce un color nuevo.

**The Amber Is Rare Rule.** El ámbar aparece como detalle (contacto, tags, mensajes), nunca como fondo de bloque ni color de título.

## Typography

**Display Font:** Syne (con Trebuchet MS, sans-serif), fuentes propias en `assets/fonts/`.
**Body Font:** JetBrains Mono (con ui-monospace, SFMono-Regular, Menlo, monospace).
**Label/Mono Font:** el mismo JetBrains Mono, en mayúsculas con tracking.

**Character:** Syne 800 comprimida y pesada da el nombre y el título; la mono hace de rotulación técnica. El contraste es entre bloque y regla.

### Hierarchy
- **Display** (800, clamp(34px, 8vw, 64px), 0.95, mayúsculas, -0.01em): título de página, de evento y de artista; precedido por una barra de color de 0.14em x 0.78em. A 420 px o menos baja a clamp(22px, 7.9vw, 34px).
- **Headline** (800, clamp(26px, 5vw, 40px), 0.95, mayúsculas): título del bloque de newsletter; la caja «pronto» usa clamp(34px, 7vw, 56px).
- **Title** (800, clamp(24px, 3.2vw, 32px) en tarjetas de releases/eventos sin portada; 24px en tarjetas de artista, 0.95, mayúsculas): nombre en el fallback de tarjeta. El nombre de canal del home y las filas del linktree usan la mono a 12-13 px con tracking .16-.2em.
- **Body** (400, 13px, 1.7-1.8, hasta 60-68ch): prosa, bio, textos de caja. La regla vertical a la izquierda (1px #3a3a46, 14px de relleno) marca los bloques de texto.
- **Body small** (400, 12px, 1.45): valores de la ficha de evento, etiqueta y nombre de canal del home, mensajes.
- **Label** (400, 11px, .12em a .26em, mayúsculas): navegación, leyendas, botones, `sec-h`, números, tira superior. Es el único tamaño por debajo de 12.
- **Slogan** (Syne cursiva, 14px): pie.

### Named Rules
**The Four Sizes Rule.** El texto de interfaz solo usa 11, 12, 13 y 14 px; lo que crece es título y se resuelve con clamp. No se añaden tamaños intermedios.

**The Caps With Tracking Rule.** Toda etiqueta en mono va en mayúsculas con tracking de .12em o más; todo título Syne va en mayúsculas.

## Layout

Una columna centrada de 1080 px máx. con 20 px de relleno lateral (`.wrap`; 520 px en el linktree). Dos reglas verticales fijas (#2a2a33) siguen los bordes de la columna a `max(10px, 50% - 560px)`. Cada página abre con una tira superior (leyenda con ticks), el título y, bajo cada sección, un `sec-h` numerado con regla de ticks. El pie con 72 px de margen superior y la regla con marcas cierran la hoja.

Ritmo: huecos de 10-12 px entre elementos tipo panel, 26-34 px entre filas de tarjetas, 44 px de aire sobre el título de página, 34 px antes de cada sección.

- **Cuadrículas con auto-fill:** tarjetas de label (min 230px, aspect 3/4), roster de artistas (min 210px, aspect 4/5), releases (min 190px, 1:1), vídeos (min 250px, 16:9).
- **Columnas calculadas:** a partir de 701 px, el muro de carteles (`.wall`) usa `--cols` (por defecto 5) con 16 px de hueco, y releases y vídeos usan `--cols` (por defecto 4), para que todas las filas tengan el mismo número de piezas (mínimo 4 en escritorio en Events). Los carteles se muestran 5/7 con `contain`.
- **Galería de comunidad:** columnas CSS 2 / 3 (700 px) / 4 (1000 px) con 12 px de hueco; miniaturas cuadradas con `cover`, el visor muestra la foto completa.
- **Home:** cinco canales en una fila de seis columnas iguales (hueco 10 px); si la ventana mide 761+ px de ancho y 820 px o menos de alto, el fader baja de 280 a 220 px y el símbolo a 210 px para que quepa en el primer viewport. A 760 px o menos, seis filas de 84 px mínimo con el nombre y la etiqueta a la izquierda y un knob de 64 px a la derecha.
- **Breakpoints observados:** 420, 520, 620, 700/701, 760/761, 820, 900, 1000 px.
- **Menú:** a 900 px o menos pasa a un botón MENU que despliega la lista a pantalla completa de ancho con filas de 16 px de relleno vertical.

## Elevation & Depth

Plano por defecto: la profundidad se construye con capas tonales (ground, superficie, superficie elevada), bordes de 1 px y transparencias sobre el fondo generativo. No hay sombras de reposo en tarjetas ni botones.

### Shadow Vocabulary
- **Símbolo** (`filter: drop-shadow(0 8px 30px hsla(240+h, 90%, 70%, .30)) drop-shadow(0 3px 16px rgba(232,176,75,.12))`): halo de color del símbolo cromado.
- **Logo** (`drop-shadow(0 4px 18px rgba(0,0,0,.45))`): separa el logo del fondo.
- **Cartel levantado** (`box-shadow: 0 18px 50px rgba(0,0,0,.7)` con `scale(1.12)`): cartel en hover o foco, solo con puntero (`hover:none` lo desactiva).
- **Tapa de fader** (`box-shadow: 0 5px 12px rgba(0,0,0,.65), inset 0 1px 0 rgba(255,255,255,.7)`): da peso al objeto físico; el mismo en el knob móvil.
- **Menú móvil** (`box-shadow: 0 18px 40px rgba(0,0,0,.6)`).

### Named Rules
**The Flat Until Touched Rule.** Las superficies están planas en reposo; la elevación aparece como respuesta a puntero o foco (carteles) o como material de un objeto físico (tapa de fader, knob).

## Shapes

Ángulo recto en todo: botones, tarjetas, campos, miniaturas y cajas con radio 0 y borde de 1 px. Las excepciones son físicas: tapa de fader (2 px) y knob (círculo). Marcas de registro de 12 px x 1 px en las esquinas (`.brk`, inset -6 px, opacidad .75) y una cruz de 11 px en la esquina de la cabecera de página. Las barras de color de los títulos son rectángulos verticales; la `chip` es un rectángulo de 34 x 10 px. Retratos 4:5 y carteles 5:7 son proporciones fijas del sistema.

## Components

### Buttons
Contorno fino, rótulo técnico.
- **Shape:** esquina recta (0), borde 1 px crema.
- **Primary (outline):** transparente, texto crema, 11 px mayúsculas con tracking .16em, relleno 11px 16px.
- **Hover:** se invierte a fondo crema y texto ground (transición .15 s).
- **Solid:** fondo `--acc`, texto ground; en hover `brightness(1.1)`.
- **Linktree:** filas de 18 px de relleno con fondo superficie y borde de línea; hover sube 2 px y el borde pasa a gris mudo; la fila primaria es crema con texto ground.

### Cards / Containers
- **Tarjeta de label/evento:** imagen 3/4 con borde de línea, leyenda bajo regla fina (nombre a la izquierda, dato en gris mudo a la derecha), hover con zoom de imagen a 1.035. Sin portada: fallback con degradado del acento y título Syne. La tarjeta `soon` baja a opacidad .6.
- **Tarjeta de artista:** retrato 4:5 en escala de grises (grayscale 1, contraste 1.05) que recupera color en hover y foco.
- **Release / vídeo:** miniatura 1:1 o 16:9; el vídeo muestra una etiqueta `play` en la esquina.
- **Ficha de evento (`.meta`):** rejilla de datos con bordes de 1 px, términos en 11 px y valores en 12 px.
- **Cajas** (definición, pronto, newsletter): borde de línea, fondo superficie al 78 % o violeta al 7 %, relleno 20-34 px.
- **Vídeo de evento:** caja 30/17 negra con leyenda en gris mudo.

### Inputs / Fields
Campo de correo recto, fondo ground, borde #3a3a46, 14 px de relleno, 13 px. Foco: contorno de 2 px crema con desfase de 1 px. La casilla usa `accent-color` yin. Campo trampa `hp` fuera de pantalla.

### Navigation
Barra superior con logo de 14 px de alto, enlaces en mono de 11 px con tracking .18em en gris mudo que pasan a crema en hover y en la página actual (`aria-current`). El selector de idioma son dos botones con borde que se ve solo en el activo. «✉ Contacto» va en ámbar. Regla con ticks bajo la barra. A 900 px o menos, botón MENU y panel desplegable. Enlace «saltar al contenido» y áreas táctiles de al menos 24 px logradas con relleno compensado por margen negativo.

### Galería y visor
Muro de carteles con zoom al pasar el ratón (escala 1.12) y apertura en visor; galería de fotos cuadrada. El visor (`lb`) cubre la pantalla con rgba(6,6,9,.96), barra superior e inferior con contador y botón de cierre, flechas de 44 x 64 px (48 px con fondo semitransparente en móvil) y la imagen completa con `contain`.

### Canales de mezcla (componente de la ronda: home)
Seis canales iguales, uno por sección, ordenados como el menú. Cada uno es un enlace con borde de línea, fondo superficie al 72 % y tres filas: nombre (12 px, .2em, centrado), rail de 280 px (220 en pantallas bajas) y etiqueta de 12 px en gris mudo.
- **Escritorio:** rail de 60 px con carril de 2 px (#3a3a46) y ticks cada 28 px a ambos lados; columna de nivel de 4 px con el hue variable (degradado de hsla .15 a hsl 240+h, 90 %, 72 %) que sube hasta la tapa; tapa rectangular de 46 x 26 px, degradado crema, ranuras finas y marca central con hue variable.
- **Niveles en reposo:** 0.62, 0.34, 0.18, 0.78, 0.48 y 0.70 por canal (variable `--lvl`); sin significado de dato, solo variedad de mesa.
- **Hover y foco de teclado:** borde y fondo pasan a línea fuerte y superficie elevada, y `--lvl` sube a 1 con transición de .9 s `cubic-bezier(.16,1,.3,1)`; el hover solo bajo `hover:hover`. Foco: contorno crema de 2 px con desfase de 2 px.
- **Móvil (760 px o menos):** el canal es una fila con rejilla `1fr 64px`; el rail se convierte en un knob de 64 px: aro cónico de 270° que parte de 225° y se llena hasta el nivel, con 4 px de grosor, y una tapa circular de 44 px que gira de -135° a +135° con un indicador de 3 x 13 px. No hay arrastre; es solo indicador de estado.
- **Debajo de la mesa:** línea pequeña de enlaces a SoundCloud e Instagram (11 px, subrayados con desfase de 4 px). El pie del home lleva un símbolo blanco plano de 28 px al 70 %.
- **Movimiento reducido:** la transición del nivel se retira; solo quedan las del borde y el fondo.

### Pie
Regla con ticks, eslogan en Syne cursiva 14 px y línea de contacto en 11 px mono con enlaces subrayados (desfase de 4 px); el aviso de retirada de fotos va aquí. A 520 px o menos se ocultan los separadores y la línea se parte.

### Foco y movimiento
- **Foco unificado:** enlaces, botones y summary usan contorno de 2 px crema con desfase de 3 px; las fotos y filas del linktree, 2 px con desfase de 2 px.
- **Movimiento:** transiciones de 150-350 ms en color, borde y zoom de imagen (.5 s); el logo y el símbolo transicionan el filtro en .5 s. Con `prefers-reduced-motion: reduce` se anulan todas las transiciones (`*{transition:none!important}`), también la del nivel de los canales, y `bg.js` y `app.js` también leen la preferencia.

## Do's and Don'ts

### Do:
- **Do** mantener ground #0a0a0d, superficies #111116/#17171d, líneas #2a2a33/#3a3a46 y texto #f1ede6 como únicos neutros.
- **Do** usar Syne 800 en mayúsculas para nombres y títulos y JetBrains Mono para el resto; quedarse en 11/12/13/14 px.
- **Do** dejar el hue variable `--h` como único color vivo, aplicado a símbolo, logo, niveles y marcas de tapa.
- **Do** construir muros con columnas calculadas (`--cols`) para que todas las filas tengan el mismo número de piezas.
- **Do** mostrar carteles en 5/7 con `contain` y retratos en 4:5 con `cover`.
- **Do** respetar `prefers-reduced-motion` en cualquier movimiento nuevo y mantener el foco visible con contorno crema de 2 px.
- **Do** mantener el contacto accesible en toda la web (barra y pie).
- **Do** que cada elemento táctil mida al menos 24 px, compensando con margen negativo si hace falta.

### Don't:
- **Don't** añadir subtítulos o introducciones bajo los títulos de página; solo lo imprescindible.
- **Don't** mostrar un próximo evento: todos los eventos han pasado. Yang Alchemy no aparece en ninguna parte ni como «cancelado».
- **Don't** usar esquinas redondeadas, sombras de reposo o degradados decorativos en tarjetas y botones; el redondeo solo es del knob.
- **Don't** sustituir los faders por elementos inventados: la tapa es rectangular con marca central, y en móvil el knob giratorio.
- **Don't** introducir un tercer acento ni usar el ámbar como fondo de bloque.
- **Don't** usar imágenes del press kit PDF; siempre desde los originales en alta resolución.

### No canonizado (deriva presente en la construcción)
- El glifo «✉» antepuesto al enlace de contacto (`.contact-link::before`) es un icono de glifo y no se hereda como norma para superficies nuevas.
- `.page-head p` (párrafo bajo el título) sigue en el CSS aunque la decisión del dueño es no tener subtítulos; no es una regla del sistema.
- `.card.cancelled` (insignia roja #c0392b y grises) sigue definido aunque ningún evento cancelado debe mostrarse; es código residual, no sistema.
- Los 11 px del texto de etiqueta son el mínimo; hay valores sueltos de relleno y de ancho de reglas (como los 18 px del linktree) que no forman una escala y no se registran como tokens.
