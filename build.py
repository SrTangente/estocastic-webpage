#!/usr/bin/env python3
"""Genera estocastic.xyz (ES en /, EN en /en/).

Secciones: LABEL · ABOUT · SHOP · AGENCY · COMMUNITY.
Datos:   site.json, events.json, artists.json, releases.json, content.json
Fuentes: source/ (no se sube a git):
   source/<evento>/*.jpg            fotos del evento       -> /community/<evento>/
   source/posters/<evento>.jpg      cartel (opcional)
   source/artists/<slug>[_N].jpg    retrato y fotos extra  -> /agency/<slug>/
   source/releases/<cover>.jpg      portadas del label
   source/radio/<thumb>.jpg         miniaturas de radio
   source/fiestas/NN.jpg            carteles de fiestas (muro de COMMUNITY)
   source/about/group.jpg           foto de grupo
Uso: python3 build.py
"""
import base64, html, json, sys
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
def load(name, default):
    p = ROOT / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default
SITE, EVENTS = load("site.json", {}), load("events.json", [])
ARTISTS, RELEASES, CONTENT = load("artists.json", []), load("releases.json", []), load("content.json", {})
LINKS = load("links.json", [])
SRC = ROOT / "source"
import hashlib
def av(name):
    """Versión (hash corto) de un archivo de assets/ para que el navegador no use una copia vieja."""
    f = ROOT / "assets" / name
    return hashlib.md5(f.read_bytes()).hexdigest()[:8] if f.exists() else "0"
SHOW_GATE = bool(SITE.get("endpoint")) or "--with-gate" in sys.argv  # sin endpoint no se muestra el formulario
EXTS = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}
MB = SITE.get("media_base", "").rstrip("/")  # "" = mismo dominio; luego "https://media.estocastic.xyz"
esc = html.escape
LANGS = ("es", "en")
SECTIONS = ["label", "about", "shop", "agency", "events", "community"]

T = {
 "es": dict(html="es", menu="Menú",
   events_kicker="Eventos · Events — 05", events_intro="", events_desc="Carteles y fotos de las fiestas de esτocasτic.",
   community_kicker="Comunidad · Community — 06", community_intro="",
   community_desc="Fotos y vídeo de las fiestas de esτocasτic.", takedown="Si apareces en alguna foto y prefieres que la quitemos, escríbenos a {c}.", photos_h="Fotos", events_h="Eventos", fiestas_alt="Cartel de fiesta esτocasτic",
   label_kicker="Label — 01", label_intro="", label_desc="Mixes y radio de esτocasτic.",
   mixes_h="Mixes", radio_h="Radio", listen="Escuchar", watch="Ver",
   about_kicker="About — 02", about_desc="Manifiesto de esτocasτic.", manifesto_h="Manifiesto", parties_h="Fiestas", contact_h="Contacto",
   shop_kicker="Shop — 03", shop_desc="Tienda de esτocasτic.", shop_h="Pronto", shop_text="Estamos preparando la tienda. Síguenos para enterarte cuando abra.", shop_cta="Avisadme →",
   agency_kicker="Agency — 04", agency_intro="", agency_desc="Artistas de esτocasτic.",
   back_roster="← Volver a Agency", book="Contratar artista", artist_ph="Retrato de",
   soon="Pronto", soon_ph="Fotos pronto", cancelled="Cancelado", empty="Las fotos llegarán pronto.", date="Fecha", place="Lugar", time="Horario", fmt="Formato", photos="Fotos", photo="Foto",
   ev_desc="Fotos de {t} — esτocasτic. {v}.", crumb_ex="archivo analógico", photo_alt="foto", poster="Cartel",
   gate_kicker="Acceso · Access", gate_text="Una selección de fotos analógicas de los dos días. Deja tu correo y entra: te avisaremos de vez en cuando de novedades y próximas fechas de esτocasτic.",
   gate_open="Entrar al archivo analógico →", email_ph="correo@ejemplo.com", email_aria="Correo electrónico",
   consent="Acepto recibir comunicaciones de esτocasτic (novedades y próximos eventos). Puedo darme de baja cuando quiera.", submit="Entrar →",
   fine="Responsable: {ctl}. Finalidad: enviarte la newsletter y darte acceso a las fotos. Legitimación: tu consentimiento. Derechos de acceso, rectificación y supresión (y baja): {c}.",
   close="Cerrar ✕", prev="Anterior", next="Siguiente", dl="Descargar ↓", viewer="Visor de fotos", route="Ruta", skip="Saltar al contenido", nav_main="Principal", video="Vídeo", links="Enlaces", events="Eventos",
   m_email="Revisa el correo.", m_consent="Debes aceptar para continuar.", m_na="Formulario no disponible ahora mismo.", m_fail="No se ha podido enviar. Inténtalo de nuevo.",
   symbol="Símbolo de esτocasτic", home_title="esτocasτic — Colectivo de música electrónica · Barcelona", home_desc="Colectivo y label de música electrónica en Barcelona. Mixes, radio, artistas y fiestas. Let waveforms collapse.", home_sub_photos="Fotos de las fiestas",
   subs=dict(label="Mixes · Radio", about="Manifiesto", shop="Pronto", agency="Artistas", events="Carteles · Fiestas", community="Fotos · Vídeo")),
 "en": dict(html="en", menu="Menu",
   events_kicker="Events · Eventos — 05", events_intro="", events_desc="esτocasτic party posters and photos.",
   community_kicker="Community · Comunidad — 06", community_intro="",
   community_desc="Photos and video from esτocasτic parties.", takedown="If you appear in a photo and would rather we take it down, write to {c}.", photos_h="Photos", events_h="Events", fiestas_alt="esτocasτic party poster",
   label_kicker="Label — 01", label_intro="", label_desc="esτocasτic mixes and radio.",
   mixes_h="Mixes", radio_h="Radio", listen="Listen", watch="Watch",
   about_kicker="About — 02", about_desc="esτocasτic manifesto.", manifesto_h="Manifesto", parties_h="Parties", contact_h="Contact",
   shop_kicker="Shop — 03", shop_desc="esτocasτic shop.", shop_h="Soon", shop_text="We're preparing the shop. Follow us to know when it opens.", shop_cta="Notify me →",
   agency_kicker="Agency — 04", agency_intro="", agency_desc="esτocasτic artists.",
   back_roster="← Back to Agency", book="Book artist", artist_ph="Portrait of",
   soon="Soon", soon_ph="Photos soon", cancelled="Cancelled", empty="Photos coming soon.", date="Date", place="Place", time="Time", fmt="Format", photos="Photos", photo="Photo",
   ev_desc="Photos from {t} — esτocasτic. {v}.", crumb_ex="analog archive", photo_alt="photo", poster="Poster",
   gate_kicker="Access · Acceso", gate_text="A selection of analog photos from both days. Leave your email and step in: we'll let you know now and then about news and upcoming esτocasτic dates.",
   gate_open="Enter the analog archive →", email_ph="you@example.com", email_aria="Email address",
   consent="I agree to receive communications from esτocasτic (news and upcoming events). I can unsubscribe at any time.", submit="Enter →",
   fine="Controller: {ctl}. Purpose: sending you the newsletter and giving you access to the photos. Legal basis: your consent. Rights of access, rectification and erasure (and unsubscribing): {c}.",
   close="Close ✕", prev="Previous", next="Next", dl="Download ↓", viewer="Photo viewer", route="Breadcrumb", skip="Skip to content", nav_main="Main", video="Video", links="Links", events="Events",
   m_email="Check your email address.", m_consent="You need to accept to continue.", m_na="The form is not available right now.", m_fail="Could not send. Please try again.",
   symbol="esτocasτic symbol", home_title="esτocasτic — Electronic music collective · Barcelona", home_desc="Electronic music collective and label in Barcelona. Mixes, radio, artists and parties. Let waveforms collapse.", home_sub_photos="Party photos",
   subs=dict(label="Mixes · Radio", about="Manifesto", shop="Soon", agency="Artists", events="Posters · Parties", community="Photos · Video")),
}
ARIA_PAGE, ARIA_TRUE, BLANK = ' aria-current="page"', ' aria-current="true"', ' target="_blank" rel="noopener"'  # (compat. Python < 3.12)
def pre(L): return "" if L == "es" else "/en"
def loc(d, key, L):
    return d.get(f"{key}_en", d.get(key, "")) if L == "en" else d.get(key, "")
def ensure(p): p.parent.mkdir(parents=True, exist_ok=True); return p

# ---------- imágenes ----------
def newer(dest, src): return dest.exists() and dest.stat().st_mtime >= src.stat().st_mtime
def find(subdir, stem):
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        p = SRC / subdir / f"{stem}{ext}"
        if p.exists(): return p
def out_img(subdir, stem, maxdim, q=84, dest_sub=None):
    """Optimiza source/<subdir>/<stem> -> media/<dest_sub or subdir>/<stem>.jpg ; devuelve URL o None."""
    p = find(subdir, stem)
    if not p: return None
    d = dest_sub or subdir
    dest = ROOT / "media" / d / f"{stem}.jpg"
    if not newer(dest, p):
        im = ImageOps.exif_transpose(Image.open(p)).convert("RGB")  # sin EXIF/GPS
        im.thumbnail((maxdim, maxdim), Image.LANCZOS)
        im.save(ensure(dest), "JPEG", quality=q, optimize=True, progressive=True)
    return f"{MB}/media/{d}/{stem}.jpg"

def dims(url):
    """' width=".." height=".."' de una imagen ya optimizada en media/ (evita saltos de maquetación)."""
    try:
        with Image.open(ROOT / (url[len(MB):] if MB and url.startswith(MB) else url).lstrip("/")) as im: return f' width="{im.width}" height="{im.height}"'
    except OSError: return ""

SZ_CARD = "(max-width:520px) 100vw, 240px"   # tarjetas (Label, Agency, Community)
SZ_WALL = "(max-width:520px) 50vw, (max-width:700px) 33vw, calc(min(100vw, 1040px) / {cols})"    # muro de carteles (Events)

def wall_cols(n, lo=4, hi=8, ideal=5):
    """Columnas del muro de carteles en escritorio: el divisor de n (entre lo y hi) más cercano a `ideal`,
    para que todas las filas lleven el mismo número de carteles. Si no hay (n primo, etc.), la
    última fila incompleta que deje menos huecos (mínimo `lo` por fila)."""
    div = [c for c in range(lo, hi + 1) if n >= c and n % c == 0]
    if div: return min(div, key=lambda c: (abs(c - ideal), c))
    return min(range(lo, 7), key=lambda c: ((-n) % c if n >= c else 99, abs(c - ideal), c))
def rimg(url, sizes, widths=(480, 800)):
    """srcset/sizes/width/height: crea copias reducidas en media/<dir>/w<N>/ a partir de la imagen ya optimizada."""
    src = ROOT / (url[len(MB):] if MB and url.startswith(MB) else url).lstrip("/")
    try:
        with Image.open(src) as im0: W, H = im0.size
    except OSError: return ""
    parts = []
    for w in widths:
        if w >= W: continue
        dest = src.parent / f"w{w}" / src.name
        if not newer(dest, src):
            with Image.open(src) as im:
                im.convert("RGB").resize((w, round(H * w / W)), Image.LANCZOS).save(ensure(dest), "JPEG", quality=80, optimize=True, progressive=True)
        parts.append(f"{url[:url.rindex('/')]}/w{w}/{src.name} {w}w")
    parts.append(f"{url} {W}w")
    return f' srcset="{", ".join(parts)}" sizes="{sizes}" width="{W}" height="{H}"'

def process_photos(ev):
    d = ev["secret"] if ev.get("exclusive") else ev["slug"]
    folder = SRC / ev["slug"]
    files = sorted(p for p in folder.glob("*") if p.suffix.lower() in EXTS) if folder.exists() else []
    out = []
    for n, p in enumerate(files, 1):
        full, thumb = ROOT / "media" / d / "full" / f"{n:03d}.jpg", ROOT / "media" / d / "thumb" / f"{n:03d}.jpg"
        if not (newer(full, p) and newer(thumb, p)):
            im = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
            f = im.copy(); f.thumbnail((2500, 2500), Image.LANCZOS); f.save(ensure(full), "JPEG", quality=86, optimize=True, progressive=True)
            t = im.copy(); t.thumbnail((720, 1440), Image.LANCZOS); t.save(ensure(thumb), "JPEG", quality=78, optimize=True, progressive=True)
        with Image.open(thumb) as t: w, h = t.size
        out.append(dict(n=n, w=w, h=h, full=f"{MB}/media/{d}/full/{n:03d}.jpg", thumb=f"{MB}/media/{d}/thumb/{n:03d}.jpg",
                        name=f"estocastic_{ev['slug']}_{n:03d}.jpg"))
    return out
def acc(ev): return f"var(--{ev.get('accent', 'yin')})"
def code(ev): return ev["slug"].upper().replace("-", "·")

# ---------- imagen para compartir (og.jpg) ----------
def make_og():
    """1200x630: símbolo + logo sobre el fondo de la web. Se regenera solo si cambian symbol.png/logo.png."""
    dest = ROOT / "og.jpg"
    if newer(dest, ROOT / "symbol.png") and newer(dest, ROOT / "logo.png"): return
    im = Image.new("RGB", (1200, 630), (10, 10, 13))
    sym = Image.open(ROOT / "symbol.png").convert("RGBA"); sym.thumbnail((520, 340), Image.LANCZOS)
    logo = Image.open(ROOT / "logo.png").convert("RGBA"); logo.thumbnail((760, 200), Image.LANCZOS)
    im.paste(sym, ((1200 - sym.width) // 2, 70), sym)
    im.paste(logo, ((1200 - logo.width) // 2, 70 + sym.height + 50), logo)
    im.save(dest, "JPEG", quality=88, optimize=True, progressive=True)

def make_symbol_small():
    """symbol-s.png (480 px de ancho) para pantallas donde el símbolo se muestra a ~150-210 px."""
    dest = ROOT / "symbol-s.png"
    if newer(dest, ROOT / "symbol.png"): return
    with Image.open(ROOT / "symbol.png") as im:
        im.convert("RGBA").resize((480, round(im.height * 480 / im.width)), Image.LANCZOS).save(dest, "PNG", optimize=True)

# ---------- datos estructurados (JSON-LD) ----------
def jsonld(data, noindex=False):
    if not data or noindex: return ""
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + "</script>"
def same_as(links): return [u for u in links if u]
def org_ld():
    return {"@context": "https://schema.org", "@type": "MusicGroup", "name": "esτocasτic", "url": SITE["domain"] + "/",
            "logo": SITE["domain"] + "/logo.png", "image": SITE["domain"] + "/og.jpg",
            "location": {"@type": "Place", "address": {"@type": "PostalAddress", "addressLocality": "Barcelona", "addressCountry": "ES"}},
            "genre": "Electronic", "sameAs": ["https://soundcloud.com/estocastic", "https://www.instagram.com/estocastic_/"]}
def artist_ld(L, a, photo):
    d = {"@context": "https://schema.org", "@type": "MusicGroup", "name": a["name"], "url": f"{SITE['domain']}{pre(L)}/agency/{a['slug']}/",
         "description": str(loc(a, "bio", L)).split("\n\n")[0], "memberOf": {"@type": "MusicGroup", "name": "esτocasτic", "url": SITE["domain"] + "/"},
         "sameAs": same_as(a.get("links", {}).values())}
    if photo and not MB: d["image"] = SITE["domain"] + photo
    return d
def event_ld(L, ev, photos):
    """Event de schema.org para un evento ya celebrado (no cancelado, no exclusivo)."""
    start = ev["date"] + ("T" + ev["time"].split("–")[0] + ":00" if ev.get("time") else "")
    end = (ev["date"] + "T" + ev["time"].split("–")[1] + ":00") if ev.get("time") and "–" in ev["time"] else None
    d = {"@context": "https://schema.org", "@type": "MusicEvent", "name": loc(ev, "title", L), "startDate": start,
         "eventStatus": "https://schema.org/EventScheduled", "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
         "location": {"@type": "Place", "name": loc(ev, "venue", L), "address": {"@type": "PostalAddress", "addressLocality": "Barcelona", "addressCountry": "ES"}},
         "organizer": {"@type": "Organization", "name": "esτocasτic", "url": SITE["domain"] + "/"},
         "url": f"{SITE['domain']}{pre(L)}/community/{ev['slug']}/"}
    if end: d["endDate"] = end
    if ev.get("lineup"): d["performer"] = [{"@type": "MusicGroup", "name": x.strip()} for x in ev["lineup"].split("·") if x.strip()]
    if photos and not MB: d["image"] = SITE["domain"] + photos[0]["thumb"]
    return d

# ---------- layout ----------
def page(L, title, desc, body, rel, noindex=False, og_image="/og.jpg", ld=None):
    t = T[L]; url = SITE["domain"] + pre(L) + rel
    alts = "" if noindex else "".join(f'<link rel="alternate" hreflang="{l}" href="{SITE["domain"]}{pre(l)}{rel}">' for l in LANGS) \
        + f'<link rel="alternate" hreflang="x-default" href="{SITE["domain"]}{rel}">'
    robots = '<meta name="robots" content="noindex,nofollow">' if noindex else ""
    og = "" if noindex else f'''<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE['domain']}{og_image}"><meta name="twitter:card" content="{"summary_large_image" if og_image == "/og.jpg" else "summary"}">'''
    cfg = json.dumps({"endpoint": SITE.get("endpoint", ""), "m": {k[2:]: t[k] for k in t if k.startswith("m_")}})
    return f'''<!doctype html>
<html lang="{t['html']}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><meta name="theme-color" content="#0a0a0d">
{robots}{alts}{og}{jsonld(ld, noindex)}<link rel="icon" type="image/png" href="/favicon.png">
<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/syne-latin.woff2" crossorigin><link rel="preload" as="font" type="font/woff2" href="/assets/fonts/jetbrains-mono-latin.woff2" crossorigin>
<link rel="stylesheet" href="/assets/fonts.css?v={av("fonts.css")}"><link rel="stylesheet" href="/assets/style.css?v={av("style.css")}">
</head><body>
{body}
<script>window.EST={cfg};</script><script src="/assets/app.js?v={av("app.js")}" defer></script><script src="/assets/bg.js?v={av("bg.js")}" defer></script>
</body></html>'''

def topbar(L, rel, section=None):
    t = T[L]
    items = "".join(f'<a href="{pre(L)}/{s}/"{ARIA_PAGE if s == section else ""}>{s.upper()}</a>' for s in SECTIONS)
    sw = "".join(f'<a href="{pre(l)}{rel}" hreflang="{l}" lang="{l}"{ARIA_TRUE if l == L else ""}>{l.upper()}</a>' for l in LANGS)
    return f'''<a class="skip" href="#main">{t['skip']}</a><header class="wrap top"><div class="bar">
<a class="brand" href="{pre(L)}/" aria-label="esτocasτic"><img src="/logo.png" alt="esτocasτic"></a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">{t['menu']}</button>
<nav id="menu" aria-label="{t['nav_main']}"><span class="items">{items}<a class="contact-link" href="mailto:{SITE['contact']}">{t['contact_h'].upper()}</a></span><span class="lang">{sw}</span></nav></div></header>'''

def footer(note=""):
    n = f'<span class="micro">{esc(note)}</span>' if note else ""
    return f'''<div class="wrap"><footer class="foot">
{n}<img class="foot-mark" src="/symbol-white.png" alt="" width="28" height="21" loading="lazy"><span class="slogan">Let waveforms collapse</span>
<span class="micro">@estocastic_ · <a href="mailto:{SITE['contact']}">{SITE['contact']}</a></span>
<span class="micro">BCN · 41.39 N / 2.17 E · REF EST—2026</span></footer></div>'''

SEC_ACC = {"label": "yin", "about": "text", "shop": "yang", "agency": "yin", "events": "yang", "community": "yang"}
def strip(sec):
    i = SECTIONS.index(sec) + 1
    return (f'<div class="strip" aria-hidden="true"><span>EST—2026</span><span>{sec.upper()}/{i:02d}</span>'
            f'<span class="hide-s">{sec[:2].upper()}{100 + i * 7} · 0.{16 + i * 3}</span><span>41.39 N · 2.17 E</span></div>')

def head(kicker, title, intro="", extra="", sec=""):
    p = f"<p>{intro}</p>" if intro else ""
    st = strip(sec) if sec else ""
    acc = f' style="--acc:var(--{SEC_ACC[sec]})"' if sec else ""
    return f'<header class="page-head"{acc}>{st}<span class="micro">{kicker}</span><h1>{title}</h1>{p}{extra}</header>'


def gate(L, ex):
    t = T[L]
    s = base64.b64encode(f"{pre(L)}/s/{SITE['secret']}/".encode()).decode()
    return f'''<section class="gate brk" id="gate" data-s="{s}" aria-labelledby="gate-t">
<div><span class="micro">{t['gate_kicker']}</span>
<h2 id="gate-t">{esc(loc(ex, 'title', L))}</h2>
<p>{t['gate_text']}</p>
<div style="margin-top:18px"><a class="btn solid open-link" style="--acc:var(--yang)" href="#">{t['gate_open']}</a></div></div>
<div><form novalidate>
<input type="email" name="email" placeholder="{t['email_ph']}" autocomplete="email" aria-label="{t['email_aria']}" required>
<input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
<label class="check"><input type="checkbox" name="consent" required> <span>{t['consent']}</span></label>
<button class="btn" type="submit">{t['submit']}</button><p class="msg" role="status"></p></form>
<p class="fine">{esc(t['fine'].format(ctl=SITE['controller'], c=SITE['contact']))}</p></div>
</section>'''

def lightbox(L):
    t = T[L]
    return f'''<div class="lb" id="lb" role="dialog" aria-modal="true" aria-label="{t['viewer']}">
<div class="lb-top"><span class="micro cnt"></span><button class="x" type="button">{t['close']}</button></div>
<div class="lb-stage"><button class="nav prev" type="button" aria-label="{t['prev']}">←</button><img alt=""><button class="nav next" type="button" aria-label="{t['next']}">→</button></div>
<div class="lb-bot"><span class="micro">esτocasτic · Let waveforms collapse</span><a class="btn dl" href="#" download>{t['dl']}</a></div></div>'''

# ---------- COMMUNITY ----------
def event_card(L, ev, count):
    t = T[L]; title = esc(loc(ev, "title", L)); cancelled = bool(ev.get("cancelled")); soon = count == 0 or cancelled
    badge = f'<span class="badge">{t["cancelled"] if cancelled else t["soon_ph"]}</span>' if soon else ""
    art = f'<div class="fallback"><span class="chip"></span><div><span class="micro">{esc(ev["date"])}</span><br><b>{title}</b></div></div>'
    if ev.get("_poster"): art = f'<img src="{ev["_poster"]}"{rimg(ev["_poster"], SZ_CARD)} alt="{t["poster"]} {title}" loading="lazy">'
    cap = f'<span>{title}</span><span>{"—" if soon else f"{count:02d} ph"}</span>'
    tag, h = ("div", "") if soon else ("a", f' href="{pre(L)}/community/{ev["slug"]}/"')
    return f'<{tag} class="card{" soon" if soon else ""}{" cancelled" if cancelled else ""}" style="--acc:{acc(ev)}"{h}><div class="art brk">{badge}{art}</div><div class="cap">{cap}</div></{tag}>'

def photo_grid(L, ev, photos):
    t = T[L]; title = loc(ev, "title", L)
    return f'<div class="grid">' + "".join(
        f'<a class="ph" href="{p["full"]}" data-full="{p["full"]}" data-name="{p["name"]}">'
        f'<img src="{p["thumb"]}" width="{p["w"]}" height="{p["h"]}" loading="lazy" alt="{esc(title)} — {t["photo_alt"]} {p["n"]:03d}">'
        f'<span class="no">{p["n"]:03d}</span></a>' for p in photos) + "</div>"

def video_block(L, ev):
    v = ev.get("video")
    if not v: return ""
    t = T[L]
    pdir = v["src"].rsplit("/", 1)[0]
    poster = f' poster="{MB}{pdir}/video-poster.jpg"' if (ROOT / pdir.lstrip("/") / "video-poster.jpg").exists() else ""
    return (f'<figure class="vidbox brk"><video controls preload="metadata" playsinline{poster} aria-label="{esc(loc(ev, "title", L))} — {t["video"]}" src="{MB}{v["src"]}"></video>'
            f'<figcaption class="micro">{esc(v["credit_en"] if L == "en" else v["credit"])}</figcaption></figure>')

def event_page(L, ev, photos, ex=None):
    t = T[L]; exclusive = ev.get("exclusive")
    rel = f"/s/{SITE['secret']}/" if exclusive else f"/community/{ev['slug']}/"
    title = loc(ev, "title", L)
    meta = [(t["date"], loc(ev, "date_label", L)), (t["place"], loc(ev, "venue", L)), (t["fmt"] if exclusive else t["time"], loc(ev, "time", L))]
    if ev.get("lineup"): meta.append(("Line-up", ev["lineup"]))
    meta.append((t["photos"], f"{len(photos):02d}"))
    if ev.get("photographer"): meta.append((t["photo"], ev["photographer"]))
    dl = "".join(f"<div><dt>{k.upper()}</dt><dd>{esc(v)}</dd></div>" for k, v in meta)
    if photos:
        grid = f'<section class="grid" aria-label="{t["photos_h"]}">' + "".join(
            f'<a class="ph" href="{p["full"]}" data-full="{p["full"]}" data-name="{p["name"]}">'
            f'<img src="{p["thumb"]}" width="{p["w"]}" height="{p["h"]}" loading="lazy" alt="{esc(title)} — {t["photo_alt"]} {p["n"]:03d}">'
            f'<span class="no">{p["n"]:03d}</span></a>' for p in photos) + "</section>"
    else:
        grid = f'<div class="empty">{t["empty"]}</div>'
    crumb = (f'<a href="{pre(L)}/">esτocasτic</a> / <a href="{pre(L)}/community/">community</a> / {esc(ev["slug"])}' if not exclusive
             else f'<a href="{pre(L)}/">esτocasτic</a> / {t["crumb_ex"]}')
    body = f'''{topbar(L, rel, "community")}<main id="main" class="wrap">
<nav class="crumb micro" aria-label="{t['route']}">{crumb}</nav>
<header class="ev-head" style="--acc:{acc(ev)}"><span class="micro">REF {code(ev)} · {esc(ev["date"])}</span>
<h1>{esc(title)}</h1><dl class="meta brk">{dl}</dl></header>
{video_block(L, ev)}{grid}
{gate(L, ex) if (ex and not exclusive and SHOW_GATE) else ""}
</main>{footer(t['takedown'].format(c=SITE['contact']) if photos and not exclusive else '')}{lightbox(L) if photos else ""}'''
    return page(L, f"{title} · esτocasτic", t["ev_desc"].format(t=title, v=loc(ev, "venue", L)), body, rel, noindex=bool(exclusive), ld=event_ld(L, ev, photos))

def community_page(L, public, counts, ex, photos):
    t = T[L]
    cards = ""
    for e in public:
        if counts[e["slug"]]:
            cards += (f'<section class="sec evsec" style="--acc:{acc(e)}"><h2 class="sec-h"><span class="chip"></span>&nbsp; {esc(loc(e, "title", L))} · {esc(loc(e, "date_label", L))} · {esc(loc(e, "venue", L))}</h2>'
                      f'{video_block(L, e)}{photo_grid(L, e, photos[e["slug"]])}</section>')
    wall = ""
    if not any(counts.values()): cards = ""
    body = f'''{topbar(L, "/community/", "community")}<main id="main" class="wrap">
{head(t['community_kicker'], "Community", '', sec="community")}
{cards}
{gate(L, ex) if (ex and SHOW_GATE) else ""}</main>{footer(t['takedown'].format(c=SITE['contact']) if cards else '')}{lightbox(L) if cards else ""}'''
    return page(L, "Community · esτocasτic", t["community_desc"], body, "/community/")

# ---------- EVENTS ----------
def events_page(L, public, counts, fiestas):
    t = T[L]
    linked = [(e["_poster"], f'{pre(L)}/community/{e["slug"]}/', loc(e, "title", L)) for e in public if e.get("_poster") and counts[e["slug"]]]
    plain = [e["_poster"] for e in public if e.get("_poster") and not counts[e["slug"]]] + list(reversed(fiestas))
    cols = wall_cols(len(linked) + len(plain))
    sz = SZ_WALL.format(cols=cols)
    items = "".join(f'<a class="pw" href="{h}" title="{esc(n)}"><img src="{u}"{rimg(u, sz)} alt="{t["poster"]} {esc(n)}" loading="lazy"></a>' for u, h, n in linked)
    items += "".join(f'<a class="ph pw" href="{u}" data-full="{u}" data-name="estocastic-cartel-{n:02d}.jpg"><img src="{u}"{rimg(u, sz)} alt="{t["fiestas_alt"]} {n:02d}" loading="lazy"></a>' for n, u in enumerate(plain, 1))
    wall = f'<section class="sec"><div class="wall" style="--cols:{cols}">{items}</div></section>' if items else ""
    fiestas = plain
    body = f'''{topbar(L, "/events/", "events")}<main id="main" class="wrap">
{head(t['events_kicker'], "Events", esc(t['events_intro']), sec="events")}
{wall}</main>{footer()}{lightbox(L) if plain else ""}'''
    return page(L, "Events · esτocasτic", t["events_desc"], body, "/events/")

# ---------- LABEL ----------
def label_page(L, covers, radio):
    t = T[L]
    items = ""
    for r in sorted(RELEASES, key=lambda r: r.get("date") or "", reverse=True):
        c = covers.get(r["id"])
        img = f'<img src="{c}"{rimg(c, SZ_CARD)} alt="{esc(r["title"])}" loading="lazy">' if c else f'<div class="fallback"><b>{esc(r["title"])}</b></div>'
        items += (f'<a class="rel" href="{esc(r["url"])}" target="_blank" rel="noopener"><div class="art brk">{img}</div>'
                  f'<div class="cap"><span>{esc(r["title"])}</span></div></a>')
    rad = "".join(
        f'<a class="vid" href="{esc(x["url"])}" target="_blank" rel="noopener"><div class="art">'
        + (f'<img src="{radio[x["thumb"]]}"{rimg(radio[x["thumb"]], SZ_CARD)} alt="{esc(x["title"])}" loading="lazy">' if radio.get(x["thumb"]) else "")
        + f'<span class="play">▶</span></div><div class="cap"><span>{esc(x["title"])}</span><span>pnc radio ↗</span></div></a>'
        for x in CONTENT.get("radio", []))
    body = f'''{topbar(L, "/label/", "label")}<main id="main" class="wrap">
{head(t['label_kicker'], "Label", t['label_intro'], sec="label")}
<section class="sec"><h2 class="sec-h">{t['mixes_h']}</h2><div class="rels">{items}</div></section>
{f'<section class="sec"><h2 class="sec-h">{t["radio_h"]}</h2><div class="vids">{rad}</div></section>' if rad else ""}
</main>{footer()}'''
    return page(L, "Label · esτocasτic", t["label_desc"], body, "/label/")

# ---------- ABOUT ----------
def about_page(L, group):
    t = T[L]; a = CONTENT.get("about", {})
    man = "".join(f"<p>{esc(x)}</p>" for x in (a.get("manifesto_en") if L == "en" else a.get("manifesto", [])))
    img = f'<figure class="group brk"><img src="{group}"{dims(group)} alt="esτocasτic &amp; friends" loading="lazy"></figure>' if group else ""
    body = f'''{topbar(L, "/about/", "about")}<main id="main" class="wrap">
{head(t['about_kicker'], "About", sec="about")}
<section class="defn brk"><b>{esc(loc(a, "term", L))}</b><i>{esc(loc(a, "etym", L))}</i><span>{esc(loc(a, "def", L))}</span></section>
<section class="sec prose"><h2 class="sec-h">{t['manifesto_h']}</h2>{man}</section>
</main>{footer()}'''
    return page(L, "About · esτocasτic", t["about_desc"], body, "/about/", og_image="/symbol.png")

# ---------- SHOP ----------
def shop_page(L):
    t = T[L]
    cta = (f'<a class="btn solid" style="--acc:var(--yang)" href="{pre(L)}/community/#gate">{t["shop_cta"]}</a>' if SHOW_GATE
           else '<a class="btn solid" style="--acc:var(--yang)" href="https://www.instagram.com/estocastic_/" target="_blank" rel="noopener">@estocastic_ ↗</a>')
    body = f'''{topbar(L, "/shop/", "shop")}<main id="main" class="wrap">
{head(t['shop_kicker'], "Shop", sec="shop")}
<section class="soon-box brk"><span class="chip"></span><h2>{t['shop_h']}</h2><p>{t['shop_text']}</p>
{cta}</section>
</main>{footer()}'''
    return page(L, "Shop · esτocasτic", t["shop_desc"], body, "/shop/")

# ---------- AGENCY ----------
LINK_LABELS = [("soundcloud", "SoundCloud"), ("instagram", "Instagram"), ("ra", "Resident Advisor"), ("bandcamp", "Bandcamp"),
               ("spotify", "Spotify"), ("youtube", "YouTube"), ("facebook", "Facebook"), ("presskit", "Press kit"), ("web", "Web")]
def artist_extras(a):
    """Fotos extra del artista: miniatura recortada a 4:5 (rejilla) + foto completa (visor)."""
    out = []
    folder = SRC / "artists"
    files = sorted(q for q in folder.glob(f"{a['slug']}_*") if q.suffix.lower() in EXTS) if folder.exists() else []
    for n, p in enumerate(files, 1):
        thumb = ROOT / "media" / "artists" / "thumb" / f"{p.stem}.jpg"
        full = out_img("artists", p.stem, 2000, dest_sub="artists/full")
        if not full: continue
        if not newer(thumb, p):
            im = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
            ImageOps.fit(im, (800, 1000), Image.LANCZOS, centering=(0.5, 0.35)).save(ensure(thumb), "JPEG", quality=82, optimize=True, progressive=True)
        out.append(dict(n=n, thumb=f"{MB}/media/artists/thumb/{p.stem}.jpg", full=full, name=f"estocastic-{a['slug']}-{n:02d}.jpg"))
    return out

def artist_card(L, a, photo):
    t = T[L]; name = esc(a["name"])
    img = (f'<img src="{photo}"{rimg(photo, SZ_CARD)} alt="{t["artist_ph"]} {name}" loading="lazy">' if photo else f'<div class="fallback"><span class="chip"></span><b>{name}</b></div>')
    return (f'<a class="acard" href="{pre(L)}/agency/{a["slug"]}/"><div class="art brk">{img}</div>'
            f'<div class="cap"><span>{name}</span></div></a>')

def artist_page(L, a, photo):
    t = T[L]; rel = f"/agency/{a['slug']}/"
    name = esc(a["name"]) + (f' ({esc(a["country"])})' if a.get("country") else "")
    ex = artist_extras(a)
    extras = "".join(f'<a class="ph" href="{x["full"]}" data-full="{x["full"]}" data-name="{x["name"]}"><img src="{x["thumb"]}" width="800" height="1000" alt="{t["artist_ph"]} {name} {x["n"]:02d}" loading="lazy"></a>' for x in ex)
    extras = f'<section class="agal">{extras}</section>' if extras else ""
    book = f'<a class="btn solid" style="--acc:var(--yin)" href="mailto:{SITE["contact"]}?subject=Booking%20-%20{esc(a["name"]).replace(" ", "%20")}">{t["book"]} →</a>'
    links = "".join(f'<a class="btn" href="{esc(a["links"][k])}" target="_blank" rel="noopener">{lab} ↗</a>' for k, lab in LINK_LABELS if a.get("links", {}).get(k))
    links += "".join(f'<a class="btn" href="{esc(x["url"])}" target="_blank" rel="noopener">{esc(x["label"])} ↗</a>' for x in a.get("links_extra", []))
    bio = "".join(f"<p>{esc(x)}</p>" for x in str(loc(a, "bio", L)).split("\n\n") if x.strip())
    img = f'<div class="aphoto brk"><img src="{photo}"{dims(photo)} alt="{t["artist_ph"]} {name}"></div>' if photo else ""
    body = f'''{topbar(L, rel, "agency")}<main id="main" class="wrap">
<nav class="crumb micro" aria-label="{t['route']}"><a href="{pre(L)}/agency/">{t["back_roster"]}</a></nav>
<article class="aview">{img}<div class="atext"><span class="micro">{esc(loc(a, "role", L))}</span>
<h1>{name}</h1>{bio}<div class="alinks">{book}{links}</div></div></article>{extras}</main>{footer()}{lightbox(L) if ex else ""}'''
    d = str(loc(a, "bio", L)).split("\n")[0][:150]
    return page(L, f"{a['name']} · esτocasτic", d or t["agency_desc"], body, rel, og_image=(photo if photo and not MB else "/og.jpg"), ld=artist_ld(L, a, photo))

def agency_page(L, photos):
    t = T[L]
    roster = "".join(artist_card(L, a, photos[a["slug"]]) for a in ARTISTS)
    body = f'''{topbar(L, "/agency/", "agency")}<main id="main" class="wrap">
{head(t['agency_kicker'], "Agency", esc(t['agency_intro'].format(c=SITE['contact'])), sec="agency")}
<section class="roster" aria-label="Agency">{roster}</section></main>{footer()}'''
    return page(L, "Agency · esτocasτic", t["agency_desc"], body, "/agency/")

# ---------- HOME ----------
def home_page(L, counts):
    t = T[L]
    chans = "".join(
        f'<a class="ch" href="{pre(L)}/{sec}/"><span class="ch-n">{sec.upper()}</span>'
        f'<span class="ch-rail" aria-hidden="true"><i class="ch-led"></i><b class="ch-cap"></b></span>'
        f'<span class="ch-s">{esc(t["subs"][sec])}</span></a>'
        for sec in SECTIONS)
    ext = (f'<a href="https://soundcloud.com/estocastic"{BLANK}>SoundCloud ↗</a>'
           f'<a href="https://www.instagram.com/estocastic_/"{BLANK}>Instagram ↗</a>')
    body = f'''{topbar(L, "/")}<main id="main" class="wrap home">
<header class="hero"><img class="mark" src="/symbol.png" srcset="/symbol-s.png 480w, /symbol.png 800w" sizes="(max-width:480px) 52vw, 300px" width="800" height="595" alt="{t['symbol']}"><h1><img class="logo" src="/logo.png" alt="esτocasτic"></h1></header>
<nav class="desk brk" aria-label="{t['links']}">{chans}</nav>
<p class="ext micro">{ext}</p></main>{footer()}'''
    return page(L, t["home_title"], t["home_desc"], body, "/", ld=org_ld())

# ---------- LINKS (enlace de bio, estilo linktree) ----------
def links_page(L):
    t = T[L]; rows = ""
    for x in LINKS:
        url = x["url"].replace("{contact}", SITE["contact"])
        local = url.startswith("/")
        href = (pre(L) + url) if local else url
        ext = "" if (local or url.startswith("mailto:")) else ' target="_blank" rel="noopener"'
        label = x.get("label_en", x["label"]) if L == "en" else x["label"]
        sub = x.get("sub_en", x.get("sub", "")) if L == "en" else x.get("sub", "")
        arrow = "→" if local else "↗"
        cls = "lk primary" if x.get("primary") else "lk"
        tag = f'<span class="tag">{esc(x["tag"])}</span>' if x.get("tag") else ""
        rows += f'<a class="{cls}" href="{esc(href)}"{ext}><span class="l">{esc(label)}{tag}</span><span class="s">{esc(sub.replace("{contact}", SITE["contact"]))} {arrow}</span></a>'
    sw = "".join(f'<a href="{pre(l)}/linktree/" hreflang="{l}" lang="{l}"{ARIA_TRUE if l == L else ""}>{l.upper()}</a>' for l in LANGS)
    body = f'''<main class="wrap narrow lkpage">
<div class="lklang"><span class="lang">{sw}</span></div>
<header class="hero"><img class="mark" src="/symbol.png" srcset="/symbol-s.png 480w, /symbol.png 800w" sizes="(max-width:480px) 44vw, 210px" width="800" height="595" alt="{t['symbol']}"><h1><img class="logo" src="/logo.png" alt="esτocasτic"></h1></header>
<nav class="lklist" aria-label="{t['links']}">{rows}</nav>
<footer class="foot"><span class="slogan">Let waveforms collapse</span><span class="micro">@estocastic_</span></footer></main>'''
    return page(L, "esτocasτic · Links", t["home_desc"], body, "/linktree/")

# ---------- main ----------
def main():
    if SITE.get("secret") in (None, "", "CHANGE_ME"): sys.exit("site.json: falta 'secret'")
    events = sorted(EVENTS, key=lambda e: e["date"], reverse=True)
    for e in events:
        e["secret"] = SITE["secret"]; e["_poster"] = out_img("posters", e["slug"], 1400, 84)
    public = [e for e in events if not e.get("exclusive") and not e.get("cancelled")]
    ex = next((e for e in events if e.get("exclusive")), None)
    photos = {e["slug"]: process_photos(e) for e in events}
    counts = {k: len(v) for k, v in photos.items()}
    covers = {r["id"]: out_img("releases", r["cover"], 1200, 86) for r in RELEASES}
    radio = {x["thumb"]: out_img("radio", x["thumb"], 800, 82) for x in CONTENT.get("radio", [])}
    fiestas = [u for u in (out_img("fiestas", s, 1400, 84) for s in CONTENT.get("fiestas", [])) if u]
    group = out_img("about", "group", 1800, 84)
    aph = {a["slug"]: out_img("artists", a["slug"], 1100, 86) for a in ARTISTS}

    def write(L, rel, content):
        ensure(ROOT / (pre(L).strip("/") or ".") / rel.strip("/") / "index.html").write_text(content, encoding="utf-8")
    make_og(); make_symbol_small()
    for L in LANGS:
        write(L, "", home_page(L, counts))
        write(L, "linktree", links_page(L))
        write(L, "label", label_page(L, covers, radio))
        write(L, "about", about_page(L, group))
        write(L, "shop", shop_page(L))
        write(L, "agency", agency_page(L, aph))
        for a in ARTISTS: write(L, f"agency/{a['slug']}", artist_page(L, a, aph[a["slug"]]))
        write(L, "events", events_page(L, public, counts, fiestas))
        write(L, "community", community_page(L, public, counts, ex, photos))
        for e in public:
            if not e.get("cancelled"): write(L, f"community/{e['slug']}", event_page(L, e, photos[e["slug"]], ex))
        if ex and SHOW_GATE: write(L, f"s/{SITE['secret']}", event_page(L, ex, photos[ex["slug"]]))
    (ROOT / "robots.txt").write_text(f"User-agent: *\nDisallow: /s/\nDisallow: /en/s/\nSitemap: {SITE['domain']}/sitemap.xml\n", encoding="utf-8")
    rels = ["/"] + [f"/{s}/" for s in SECTIONS] + [f"/agency/{a['slug']}/" for a in ARTISTS] + [f"/community/{e['slug']}/" for e in public if counts[e["slug"]]]
    def smap(L, r):
        alt = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{SITE["domain"]}{pre(l)}{r}"/>' for l in LANGS)
        return f"<url><loc>{SITE['domain']}{pre(L)}{r}</loc>{alt}</url>\n"
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' +
        "".join(smap(L, r) for L in LANGS for r in rels) + "</urlset>\n", encoding="utf-8")
    if not SITE.get("endpoint"): print("AVISO: site.json 'endpoint' vacío -> el formulario solo funciona en localhost.")
    print(f"OK: {sum(counts[e['slug']] for e in public)} fotos públicas, {len(public)} eventos, {len(ARTISTS)} artistas, {len(RELEASES)} releases.")

if __name__ == "__main__":
    main()
