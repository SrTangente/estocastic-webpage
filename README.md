# estocastic.xyz

Web estática bilingüe ES/EN (GitHub Pages) generada con `python3 build.py`. Español en `/`, inglés en `/en/`.
Secciones: LABEL · ABOUT · SHOP · AGENCY · COMMUNITY.

- **Datos:** `events.json`, `artists.json`, `releases.json`, `content.json`, `site.json` (textos EN con sufijo `_en`).
- **Fuentes de imagen** (en `source/`, no se sube a git): ver cabecera de `build.py`. `media/` es la salida optimizada (sí se sube).
- **Evento nuevo:** bloque en `events.json` + fotos en `source/<slug>/` + `python3 build.py`.
- **Artista nuevo:** entrada en `artists.json` + `source/artists/<slug>.jpg` (extras: `<slug>_1.jpg`…).
- **Release nueva:** entrada en `releases.json` + portada en `source/releases/`.
- **Formulario:** `site.json` → `endpoint` = URL de Apps Script (`apps_script_correos.gs`).
- Fotos de suscriptores: `/s/<secret>/` (noindex, sin enlace público).
