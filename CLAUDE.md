# esτocasτic — estocastic.xyz

Web del colectivo de música electrónica esτocasτic (Barcelona). Estática y bilingüe: **ES en `/`, EN en `/en/`**. Alojada en GitHub Pages (rama `main`, raíz, `CNAME` estocastic.xyz). Dominio en Namecheap. El HTML publicado está en el repo y lo genera Python: **no se edita a mano, se edita `build.py`/JSON/`assets/` y se ejecuta `python3 build.py`**.

Idioma de trabajo con el dueño (Sewa): español, mensajes cortos y directos.

## Cómo funciona
- `build.py` (Python + Pillow) genera todas las páginas desde `site.json`, `events.json`, `artists.json`, `releases.json`, `content.json`, `links.json`. Textos EN con sufijo `_en`; los textos de interfaz están en los diccionarios `T["es"]`/`T["en"]` de `build.py`.
- `assets/style.css`, `assets/app.js` (menú, lightbox), `assets/bg.js` (fondo generativo + color variable del logo).
- `source/` (**gitignorada**) = originales; `media/` = salida optimizada (**sí se sube**). Estructura de `source/` en la cabecera de `build.py`. Para ver el sitio en local: `python3 build.py && python3 -m http.server 8000`.
- `media_base` en `site.json`: vacío = mismas rutas del dominio; más adelante puede apuntar a `https://media.estocastic.xyz` (Cloudflare R2).
- Despliegue: commit + `git push origin main`; Pages tarda 1–2 min. Los commits de Claude llevan el trailer `Co-Authored-By`.
- Secretos: nunca guardar tokens en el repo ni pegarlos en mensajes de commit.

## Secciones (menú, en este orden)
LABEL · ABOUT · SHOP · AGENCY · EVENTS · COMMUNITY, más `/linktree/` (bio de Instagram, sin enlace en el menú) y un enlace "✉ CONTACTO" en la barra.
- **Label:** releases ordenadas de más nueva a más vieja (campo `date`), más radio (PNC). Portadas en `source/releases/` (hi-res, 1200 px de salida).
- **About:** solo definición + manifiesto (`content.json`).
- **Shop:** "pronto" (Instagram como CTA).
- **Agency:** tarjetas solo con el nombre del artista (sin rol). Ficha por artista: bio, retrato 4:5, extras, botones SoundCloud e Instagram (`links`) y mixes (`links_extra`).
- **Events:** muro de carteles. El cartel de un evento con fotos enlaza a `/community/<slug>/`; los demás se abren en lightbox (zoom al pasar el ratón / clic).
- **Community:** fotos y vídeo de los eventos que ya tienen (Yin Gathering). Vídeo: `events.json` → `video` (src, crédito); archivo en `media/<slug>/video.mp4`. El aviso de retirada de fotos va **en el pie de página**, no bajo el título.

## Decisiones tomadas (respetar)
- Todos los eventos ya han pasado. **Yang Alchemy se canceló: no debe aparecer en ningún sitio** (`"cancelled": true` en `events.json`; no mostrar "cancelado").
- **Sin subtítulos/introducciones innecesarias** bajo los títulos de página (Label, Agency, Events, Community). Solo lo imprescindible.
- Contacto accesible en toda la web (nav + pie). Actualmente `estocastic.sound@gmail.com`; cambiará a `contact@estocastic.xyz` cuando exista el reenvío (cambiar `contact` en `site.json`).
- Linktree: SoundCloud, Instagram, Contacto y Web (primero). No incluye "Label · Mixes".
- Fondo generativo `bg.js`: ondas que se aplanan junto al cursor y con ripples al clic; respeta `prefers-reduced-motion`. Color del logo y símbolo por visita: ~50 % el morado original, resto aleatorio; clic en el símbolo cambia de color; se guarda en `sessionStorage`.
- Imágenes siempre en alta resolución desde los originales (carpetas MIXTAPES, CARTELES, FOTACAS del usuario y la exportación de Instagram), nunca desde el press kit PDF (ahí están comprimidas). Carteles en 5/7 con `object-fit: contain`; retratos de artista 4:5 `cover`.
- Galería exclusiva de fotos analógicas en `/s/<secret>/` (noindex): oculta hasta que `site.json` tenga `endpoint` (Apps Script, ver `apps_script_correos.gs`) o se construya con `--with-gate`.

## Identidades (no confundir)
Gato = **Akagat** (@ak__gat) · Clim = **KLIM** (@klimthe_roland) · Juangui = **Neøpreno** (@juangui.222) · Sewa = **Tangente** (@tangente.py). SoundCloud: aka-gat, klimtheroland, borauricular, senoentrecoseno. Invitados que han tocado: Avsluta, Myrcene, Colell (no están en Agency).

## Pendientes
1. **Presskit por artista:** enlace "Presskit ↗" a una carpeta de Drive pública (fotos, vídeos, PDF presskit, tech rider). El usuario prepara las carpetas; luego añadir el enlace en `artists.json` y mostrarlo en la ficha.
2. Reenvío `contact@estocastic.xyz` (Namecheap email forwarding solo funciona con DNS de Namecheap; con Cloudflare, Email Routing) y cambiar `contact` en `site.json`.
3. Cloudflare R2 (`media.estocastic.xyz`, 10 GB gratis) antes del primer evento con muchas fotos; límite de GitHub Pages ≈ 1 GB.
4. Activar la galería exclusiva: endpoint de Apps Script; página de privacidad y nombre legal del responsable (`controller` en `site.json`).
5. Cartel de Hangar48 (17 may) y Hangar48/Siroco (5 sep) solo existen en 4:5 desde Instagram; pedir originales.
6. Instagram bio → `estocastic.xyz/linktree`.
7. Posible: añadir invitados (Avsluta, Myrcene, Colell) a Agency; fotos del fotógrafo de Yin Gathering (sin crédito conocido).
