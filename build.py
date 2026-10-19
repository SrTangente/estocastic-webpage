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
SHOW_GATE = bool(SITE.get("endpoint")) or "--with-gate" in sys.argv  # sin endpoint no se muestra el formulario
EXTS = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}
MB = SITE.get("media_base", "").rstrip("/")  # "" = mismo dominio; luego "https://media.estocastic.xyz"
esc = html.escape
LANGS = ("es", "en")
SECTIONS = ["label", "about", "shop", "agency", "community"]

T = {
 "es": dict(html="es", menu="Menú",
   community_kicker="Comunidad · Community — 05", community_intro="Fotos de nuestras fiestas, los carteles y la gente que viene. Puedes ver y descargar las fotos gratis. Si apareces en alguna y prefieres que la quitemos, escríbenos a {c}.",
   community_desc="Fotos y carteles de las fiestas de esτocasτic.", photos_h="Fotos", fiestas_h="Fiestas", fiestas_alt="Cartel de fiesta esτocasτic",
   label_kicker="Label — 01", label_intro="Nuestra serie de mixes y los streams de radio.", label_desc="Mixes y radio de esτocasτic.",
   mixes_h="Mixes", radio_h="Radio", listen="Escuchar", watch="Ver",
   about_kicker="About — 02", about_desc="Manifiesto de esτocasτic.", manifesto_h="Manifiesto", parties_h="Fiestas", contact_h="Contacto",
   shop_kicker="Shop — 03", shop_desc="Tienda de esτocasτic.", shop_h="Pronto", shop_text="Estamos preparando la tienda. Síguenos para enterarte cuando abra.", shop_cta="Avisadme →",
   agency_kicker="Agency — 04", agency_intro="Artistas e integrantes. Para contratar, escríbenos a {c}.", agency_desc="Artistas de esτocasτic.",
   back_roster="← Volver a Agency", book="Contratar artista", artist_ph="Retrato de",
   soon="Pronto", empty="Las fotos llegarán pronto.", date="Fecha", place="Lugar", time="Horario", fmt="Formato", photos="Fotos", photo="Foto",
   ev_desc="Fotos de {t} — esτocasτic. {v}.", crumb_ex="archivo analógico", photo_alt="foto", poster="Cartel",
   gate_kicker="Acceso · Access", gate_text="Una selección de fotos analógicas de los dos días. Deja tu correo y entra: te avisaremos de vez en cuando de novedades y próximas fechas de esτocasτic.",
   gate_open="Entrar al archivo analógico →", email_ph="correo@ejemplo.com", email_aria="Correo electrónico",
   consent="Acepto recibir comunicaciones de esτocasτic (novedades y próximos eventos). Puedo darme de baja cuando quiera.", submit="Entrar →",
   fine="Responsable: {ctl}. Finalidad: enviarte la newsletter y darte acceso a las fotos. Legitimación: tu consentimiento. Derechos de acceso, rectificación y supresión (y baja): {c}.",
   close="Cerrar ✕", prev="Anterior", next="Siguiente", dl="Descargar ↓", viewer="Visor de fotos", route="Ruta", links="Enlaces", events="Eventos",
   m_email="Revisa el correo.", m_consent="Debes aceptar para continuar.", m_na="Formulario no disponible ahora mismo.", m_fail="No se ha podido enviar. Inténtalo de nuevo.",
   symbol="Símbolo de esτocasτic", home_desc="esτocasτic — Let waveforms collapse. Label, About, Shop, Agency y Community.", home_sub_photos="Fotos de las fiestas",
   subs=dict(label="Mixes · Radio", about="Manifiesto", shop="Pronto", agency="Artistas", community="Fotos · Fiestas")),
 "en": dict(html="en", menu="Menu",
   community_kicker="Community · Comunidad — 05", community_intro="Photos from our parties, the posters and the people who come. You can view and download the photos for free. If you appear in one and would rather we take it down, write to {c}.",
   community_desc="Photos and posters from esτocasτic parties.", photos_h="Photos", fiestas_h="Parties", fiestas_alt="esτocasτic party poster",
   label_kicker="Label — 01", label_intro="Our mix series and radio streams.", label_desc="esτocasτic mixes and radio.",
   mixes_h="Mixes", radio_h="Radio", listen="Listen", watch="Watch",
   about_kicker="About — 02", about_desc="esτocasτic manifesto.", manifesto_h="Manifesto", parties_h="Parties", contact_h="Contact",
   shop_kicker="Shop — 03", shop_desc="esτocasτic shop.", shop_h="Soon", shop_text="We're preparing the shop. Follow us to know when it opens.", shop_cta="Notify me →",
   agency_kicker="Agency — 04", agency_intro="Artists and members. To book, write to {c}.", agency_desc="esτocasτic artists.",
   back_roster="← Back to Agency", book="Book artist", artist_ph="Portrait of",
   soon="Soon", empty="Photos coming soon.", date="Date", place="Place", time="Time", fmt="Format", photos="Photos", photo="Photo",
   ev_desc="Photos from {t} — esτocasτic. {v}.", crumb_ex="analog archive", photo_alt="photo", poster="Poster",
   gate_kicker="Access · Acceso", gate_text="A selection of analog photos from both days. Leave your email and step in: we'll let you know now and then about news and upcoming esτocasτic dates.",
   gate_open="Enter the analog archive →", email_ph="you@example.com", email_aria="Email address",
   consent="I agree to receive communications from esτocasτic (news and upcoming events). I can unsubscribe at any time.", submit="Enter →",
   fine="Controller: {ctl}. Purpose: sending you the newsletter and giving you access to the photos. Legal basis: your consent. Rights of access, rectification and erasure (and unsubscribing): {c}.",
   close="Close ✕", prev="Previous", next="Next", dl="Download ↓", viewer="Photo viewer", route="Breadcrumb", links="Links", events="Events",
   m_email="Check your email address.", m_consent="You need to accept to continue.", m_na="The form is not available right now.", m_fail="Could not send. Please try again.",
   symbol="esτocasτic symbol", home_desc="esτocasτic — Let waveforms collapse. Label, About, Shop, Agency and Community.", home_sub_photos="Party photos",
   subs=dict(label="Mixes · Radio", about="Manifesto", shop="Soon", agency="Artists", community="Photos · Parties")),
}
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

# ---------- layout ----------
def page(L, title, desc, body, rel, noindex=False, og_image="/symbol.png"):
    t = T[L]; url = SITE["domain"] + pre(L) + rel
    alts = "" if noindex else "".join(f'<link rel="alternate" hreflang="{l}" href="{SITE["domain"]}{pre(l)}{rel}">' for l in LANGS) \
        + f'<link rel="alternate" hreflang="x-default" href="{SITE["domain"]}{rel}">'
    robots = '<meta name="robots" content="noindex,nofollow">' if noindex else ""
    og = "" if noindex else f'''<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE['domain']}{og_image}"><meta name="twitter:card" content="summary">'''
    cfg = json.dumps({"endpoint": SITE.get("endpoint", ""), "m": {k[2:]: t[k] for k in t if k.startswith("m_")}})
    return f'''<!doctype html>
<html lang="{t['html']}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><meta name="theme-color" content="#0a0a0d">
{robots}{alts}{og}<link rel="icon" type="image/png" href="/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="/assets/style.css">
</head><body>
{body}
<script>window.EST={cfg};</script><script src="/assets/app.js" defer></script>
</body></html>'''

def topbar(L, rel, section=None):
    t = T[L]
    items = "".join(f'<a href="{pre(L)}/{s}/"{" aria-current=\"page\"" if s == section else ""}>{s.upper()}</a>' for s in SECTIONS)
    sw = "".join(f'<a href="{pre(l)}{rel}" hreflang="{l}" lang="{l}"{" aria-current=\"true\"" if l == L else ""}>{l.upper()}</a>' for l in LANGS)
    return f'''<div class="wrap"><div class="bar">
<a class="brand" href="{pre(L)}/" aria-label="esτocasτic"><img src="/logo.png" alt="esτocasτic"></a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">{t['menu']}</button>
<nav id="menu"><span class="items">{items}<a class="contact-link" href="mailto:{SITE['contact']}">{t['contact_h'].upper()}</a></span><span class="lang">{sw}</span></nav></div></div>'''

def footer():
    return f'''<div class="wrap"><footer class="foot">
{barcode()}<span class="slogan">Let waveforms collapse</span>
<span class="micro">@estocastic_ · <a href="mailto:{SITE['contact']}">{SITE['contact']}</a></span>
<span class="micro">BCN · 41.39 N / 2.17 E · REF EST—2026</span></footer></div>'''

SEC_ACC = {"label": "yin", "about": "text", "shop": "yang", "agency": "yin", "community": "yang"}
def strip(sec):
    i = SECTIONS.index(sec) + 1
    return (f'<div class="strip" aria-hidden="true"><span>EST—2026</span><span>{sec.upper()}/{i:02d}</span>'
            f'<span class="hide-s">{sec[:2].upper()}{100 + i * 7} · 0.{16 + i * 3}</span><span>41.39 N · 2.17 E</span></div>')

def head(kicker, title, intro="", extra="", sec=""):
    p = f"<p>{intro}</p>" if intro else ""
    st = strip(sec) if sec else ""
    acc = f' style="--acc:var(--{SEC_ACC[sec]})"' if sec else ""
    return f'<header class="page-head"{acc}>{st}<span class="micro">{kicker}</span><h1>{title}</h1>{p}{extra}</header>'

BARCODE = "".join(f'<rect x="{x}" y="0" width="{w}" height="22"/>' for x, w in
                  [(0,2),(4,1),(7,3),(12,1),(15,2),(19,1),(22,3),(27,1),(30,2),(34,1),(37,1),(40,3),(45,2),(49,1),(52,2),(56,1),(59,3),(64,1),(67,2),(71,1),(74,2),(78,3),(83,1),(86,2),(90,1),(93,1)])
def barcode(): return f'<svg class="barcode" viewBox="0 0 94 22" aria-hidden="true" fill="currentColor">{BARCODE}</svg>'

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
    t = T[L]; title = esc(loc(ev, "title", L)); soon = count == 0
    badge = f'<span class="badge">{t["soon"]}</span>' if soon else ""
    art = f'<div class="fallback"><span class="chip"></span><div><span class="micro">{esc(ev["date"])}</span><br><b>{title}</b></div></div>'
    if ev.get("_poster"): art = f'<img src="{ev["_poster"]}" alt="{t["poster"]} {title}" loading="lazy">'
    cap = f'<span>{title}</span><span>{"—" if soon else f"{count:02d} ph"}</span>'
    tag, h = ("div", "") if soon else ("a", f' href="{pre(L)}/community/{ev["slug"]}/"')
    return f'<{tag} class="card{" soon" if soon else ""}" style="--acc:{acc(ev)}"{h}><div class="art brk">{badge}{art}</div><div class="cap">{cap}</div></{tag}>'

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
    body = f'''{topbar(L, rel, "community")}<main class="wrap">
<nav class="crumb micro" aria-label="{t['route']}">{crumb}</nav>
<header class="ev-head" style="--acc:{acc(ev)}"><span class="micro"><span class="chip"></span>&nbsp; REF {code(ev)} · {esc(ev["date"])}</span>
<h1>{esc(title)}</h1><dl class="meta brk">{dl}</dl></header>
{grid}
{gate(L, ex) if (ex and not exclusive and SHOW_GATE) else ""}
</main>{footer()}{lightbox(L) if photos else ""}'''
    return page(L, f"{title} · esτocasτic", t["ev_desc"].format(t=title, v=loc(ev, "venue", L)), body, rel, noindex=bool(exclusive))

def community_page(L, public, counts, ex, fiestas):
    t = T[L]
    cards = "".join(event_card(L, e, counts[e["slug"]]) for e in public)
    wall = ""
    if fiestas:
        wall = f'<section class="sec"><h2 class="sec-h">{t["fiestas_h"]}</h2><div class="wall">' + "".join(
            f'<img src="{u}" alt="{t["fiestas_alt"]}" loading="lazy">' for u in fiestas) + "</div></section>"
    body = f'''{topbar(L, "/community/", "community")}<main class="wrap">
{head(t['community_kicker'], "Community", esc(t['community_intro'].format(c=SITE['contact'])), sec="community")}
<section class="sec"><h2 class="sec-h">{t['photos_h']}</h2><div class="cards" aria-label="{t['events']}">{cards}</div></section>
{wall}{gate(L, ex) if (ex and SHOW_GATE) else ""}</main>{footer()}'''
    return page(L, "Community · esτocasτic", t["community_desc"], body, "/community/")

# ---------- LABEL ----------
def label_page(L, covers, radio):
    t = T[L]
    items = ""
    for r in RELEASES:
        c = covers.get(r["id"])
        num = f'{r["series"].upper()} {r["num"]}'.strip() if r.get("num") else r["series"].upper()
        sub = f'{num}' + (f' · {r["date"][:4]}' if r.get("date") else "")
        img = f'<img src="{c}" alt="{esc(r["title"])}" loading="lazy">' if c else f'<div class="fallback"><b>{esc(r["title"])}</b></div>'
        items += (f'<a class="rel" href="{esc(r["url"])}" target="_blank" rel="noopener"><div class="art brk">{img}</div>'
                  f'<div class="cap"><span>{esc(r["title"])}</span><span>{esc(sub)}</span></div></a>')
    rad = "".join(
        f'<a class="vid" href="{esc(x["url"])}" target="_blank" rel="noopener"><div class="art">'
        + (f'<img src="{radio[x["thumb"]]}" alt="{esc(x["title"])}" loading="lazy">' if radio.get(x["thumb"]) else "")
        + f'<span class="play">▶</span></div><div class="cap"><span>{esc(x["title"])}</span><span>pnc radio ↗</span></div></a>'
        for x in CONTENT.get("radio", []))
    body = f'''{topbar(L, "/label/", "label")}<main class="wrap">
{head(t['label_kicker'], "Label", t['label_intro'], sec="label")}
<section class="sec"><h2 class="sec-h">{t['mixes_h']}</h2><div class="rels">{items}</div></section>
{f'<section class="sec"><h2 class="sec-h">{t["radio_h"]}</h2><div class="vids">{rad}</div></section>' if rad else ""}
</main>{footer()}'''
    return page(L, "Label · esτocasτic", t["label_desc"], body, "/label/")

# ---------- ABOUT ----------
def about_page(L, group):
    t = T[L]; a = CONTENT.get("about", {})
    man = "".join(f"<p>{esc(x)}</p>" for x in (a.get("manifesto_en") if L == "en" else a.get("manifesto", [])))
    img = f'<figure class="group brk"><img src="{group}" alt="esτocasτic &amp; friends" loading="lazy"></figure>' if group else ""
    body = f'''{topbar(L, "/about/", "about")}<main class="wrap">
{head(t['about_kicker'], "About", sec="about")}
<section class="defn brk"><b>{esc(a.get("term",""))}</b><i>{esc(loc(a, "etym", L))}</i><span>{esc(loc(a, "def", L))}</span></section>
<section class="sec prose"><h2 class="sec-h">{t['manifesto_h']}</h2>{man}</section>
</main>{footer()}'''
    return page(L, "About · esτocasτic", t["about_desc"], body, "/about/", og_image="/symbol.png")

# ---------- SHOP ----------
def shop_page(L):
    t = T[L]
    cta = (f'<a class="btn solid" style="--acc:var(--yang)" href="{pre(L)}/community/#gate">{t["shop_cta"]}</a>' if SHOW_GATE
           else '<a class="btn solid" style="--acc:var(--yang)" href="https://www.instagram.com/estocastic_/" target="_blank" rel="noopener">@estocastic_ ↗</a>')
    body = f'''{topbar(L, "/shop/", "shop")}<main class="wrap">
{head(t['shop_kicker'], "Shop", sec="shop")}
<section class="soon-box brk"><span class="chip"></span><h2>{t['shop_h']}</h2><p>{t['shop_text']}</p>
{cta}</section>
</main>{footer()}'''
    return page(L, "Shop · esτocasτic", t["shop_desc"], body, "/shop/")

# ---------- AGENCY ----------
LINK_LABELS = [("soundcloud", "SoundCloud"), ("instagram", "Instagram"), ("ra", "Resident Advisor"), ("bandcamp", "Bandcamp"),
               ("spotify", "Spotify"), ("youtube", "YouTube"), ("facebook", "Facebook"), ("presskit", "Press kit"), ("web", "Web")]
def artist_extras(a):
    out = []
    files = sorted(q for q in (SRC / "artists").glob(f"{a['slug']}_*") if q.suffix.lower() in EXTS) if (SRC / "artists").exists() else []
    for n, p in enumerate(files, 1):
        out.append(out_img("artists", p.stem, 1400))
    return [u for u in out if u]

def artist_card(L, a, photo):
    t = T[L]; name = esc(a["name"])
    img = (f'<img src="{photo}" alt="{t["artist_ph"]} {name}" loading="lazy">' if photo else f'<div class="fallback"><span class="chip"></span><b>{name}</b></div>')
    return (f'<a class="acard" href="{pre(L)}/agency/{a["slug"]}/"><div class="art brk">{img}</div>'
            f'<div class="cap"><span>{name}</span><span>{esc(loc(a, "role", L))}</span></div></a>')

def artist_page(L, a, photo):
    t = T[L]; rel = f"/agency/{a['slug']}/"
    name = esc(a["name"]) + (f' ({esc(a["country"])})' if a.get("country") else "")
    extras = "".join(f'<img src="{u}" alt="{t["artist_ph"]} {name}" loading="lazy">' for u in artist_extras(a))
    extras = f'<section class="agal">{extras}</section>' if extras else ""
    book = f'<a class="btn solid" style="--acc:var(--yin)" href="mailto:{SITE["contact"]}?subject=Booking%20-%20{esc(a["name"]).replace(" ", "%20")}">{t["book"]} →</a>'
    links = "".join(f'<a class="btn" href="{esc(a["links"][k])}" target="_blank" rel="noopener">{lab} ↗</a>' for k, lab in LINK_LABELS if a.get("links", {}).get(k))
    links += "".join(f'<a class="btn" href="{esc(x["url"])}" target="_blank" rel="noopener">{esc(x["label"])} ↗</a>' for x in a.get("links_extra", []))
    bio = "".join(f"<p>{esc(x)}</p>" for x in str(loc(a, "bio", L)).split("\n\n") if x.strip())
    img = f'<div class="aphoto brk"><img src="{photo}" alt="{t["artist_ph"]} {name}"></div>' if photo else ""
    body = f'''{topbar(L, rel, "agency")}<main class="wrap">
<nav class="crumb micro"><a href="{pre(L)}/agency/">{t["back_roster"]}</a></nav>
<article class="aview">{img}<div class="atext"><span class="micro">{esc(loc(a, "role", L))}</span>
<h1>{name}</h1>{bio}<div class="alinks">{book}{links}</div></div></article>{extras}</main>{footer()}'''
    d = str(loc(a, "bio", L)).split("\n")[0][:150]
    return page(L, f"{a['name']} · esτocasτic", d or t["agency_desc"], body, rel, og_image=(photo if photo and not MB else "/symbol.png"))

def agency_page(L, photos):
    t = T[L]
    roster = "".join(artist_card(L, a, photos[a["slug"]]) for a in ARTISTS)
    body = f'''{topbar(L, "/agency/", "agency")}<main class="wrap">
{head(t['agency_kicker'], "Agency", esc(t['agency_intro'].format(c=SITE['contact'])), sec="agency")}
<section class="roster" aria-label="Agency">{roster}</section></main>{footer()}'''
    return page(L, "Agency · esτocasτic", t["agency_desc"], body, "/agency/")

# ---------- HOME ----------
def home_page(L, counts):
    t = T[L]
    rows = [(f"{pre(L)}/{s}/", s.upper(), t["subs"][s], False) for s in SECTIONS]
    rows += [("https://soundcloud.com/estocastic", "SoundCloud", "estocastic ↗", True), ("https://www.instagram.com/estocastic_/", "Instagram", "@estocastic_ ↗", True)]
    nav = "".join(f'<a href="{h}"{" target=\"_blank\" rel=\"noopener\"" if ext else ""}><span class="n">{i:02d}</span><span class="t">{n}</span><span class="s">{esc(s)}{"" if ext else " →"}</span></a>'
                  for i, (h, n, s, ext) in enumerate(rows, 1))
    body = f'''{topbar(L, "/")}<main class="wrap narrow">
<header class="hero"><img class="mark" src="/symbol.png" alt="{t['symbol']}"><h1><img class="logo" src="/logo.png" alt="esτocasτic"></h1></header>
<nav class="index brk" aria-label="{t['links']}">{nav}</nav></main>{footer()}'''
    return page(L, "esτocasτic", t["home_desc"], body, "/")

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
    sw = "".join(f'<a href="{pre(l)}/linktree/" hreflang="{l}" lang="{l}"{" aria-current=\"true\"" if l == L else ""}>{l.upper()}</a>' for l in LANGS)
    body = f'''<main class="wrap narrow lkpage">
<div class="lklang"><span class="lang">{sw}</span></div>
<header class="hero"><img class="mark" src="/symbol.png" alt="{t['symbol']}"><h1><img class="logo" src="/logo.png" alt="esτocasτic"></h1></header>
<nav class="lklist" aria-label="{t['links']}">{rows}</nav>
<footer class="foot"><span class="slogan">Let waveforms collapse</span><span class="micro">@estocastic_</span></footer></main>'''
    return page(L, "esτocasτic · Links", t["home_desc"], body, "/linktree/")

# ---------- main ----------
def main():
    if SITE.get("secret") in (None, "", "CHANGE_ME"): sys.exit("site.json: falta 'secret'")
    events = sorted(EVENTS, key=lambda e: e["date"], reverse=True)
    for e in events:
        e["secret"] = SITE["secret"]; e["_poster"] = out_img("posters", e["slug"], 1400, 84)
    public = [e for e in events if not e.get("exclusive")]
    ex = next((e for e in events if e.get("exclusive")), None)
    photos = {e["slug"]: process_photos(e) for e in events}
    counts = {k: len(v) for k, v in photos.items()}
    covers = {r["id"]: out_img("releases", r["cover"], 800, 86) for r in RELEASES}
    radio = {x["thumb"]: out_img("radio", x["thumb"], 800, 82) for x in CONTENT.get("radio", [])}
    fiestas = [u for u in (out_img("fiestas", s, 700, 84) for s in CONTENT.get("fiestas", [])) if u]
    group = out_img("about", "group", 1800, 84)
    aph = {a["slug"]: out_img("artists", a["slug"], 1100, 86) for a in ARTISTS}

    def write(L, rel, content):
        ensure(ROOT / (pre(L).strip("/") or ".") / rel.strip("/") / "index.html").write_text(content, encoding="utf-8")
    for L in LANGS:
        write(L, "", home_page(L, counts))
        write(L, "linktree", links_page(L))
        write(L, "label", label_page(L, covers, radio))
        write(L, "about", about_page(L, group))
        write(L, "shop", shop_page(L))
        write(L, "agency", agency_page(L, aph))
        for a in ARTISTS: write(L, f"agency/{a['slug']}", artist_page(L, a, aph[a["slug"]]))
        write(L, "community", community_page(L, public, counts, ex, fiestas))
        for e in public: write(L, f"community/{e['slug']}", event_page(L, e, photos[e["slug"]], ex))
        if ex and SHOW_GATE: write(L, f"s/{SITE['secret']}", event_page(L, ex, photos[ex["slug"]]))
    (ROOT / "robots.txt").write_text(f"User-agent: *\nDisallow: /s/\nDisallow: /en/s/\nSitemap: {SITE['domain']}/sitemap.xml\n", encoding="utf-8")
    rels = ["/"] + [f"/{s}/" for s in SECTIONS] + [f"/agency/{a['slug']}/" for a in ARTISTS] + [f"/community/{e['slug']}/" for e in public if counts[e["slug"]]]
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"<url><loc>{SITE['domain']}{pre(L)}{r}</loc></url>\n" for L in LANGS for r in rels) + "</urlset>\n", encoding="utf-8")
    if not SITE.get("endpoint"): print("AVISO: site.json 'endpoint' vacío -> el formulario solo funciona en localhost.")
    print(f"OK: {sum(counts[e['slug']] for e in public)} fotos públicas, {len(public)} eventos, {len(ARTISTS)} artistas, {len(RELEASES)} releases.")

if __name__ == "__main__":
    main()
