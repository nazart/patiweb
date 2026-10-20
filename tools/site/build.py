"""Genera el sitio estático de pati.pe (diseño v3, "Color peruano") dentro de web/.
Uso: python3 tools/site/build.py   (o pasando otra carpeta de salida como argumento)
Todo el contenido queda como HTML real en cada archivo; el deploy no ejecuta ningún build:
se corre este script, se revisa el resultado y se hace commit de web/."""
import json, os, re, sys, html, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pati_icons import icon  # íconos propios (reemplazan a los emojis)
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.normpath(os.path.join(HERE, "..", "..", "web"))  # los assets (fotos, fuentes) viven aquí
ROOT = sys.argv[1] if len(sys.argv) > 1 else WEB

# ----------------------------------------------------------------- datos
SITE = "https://pati.pe"
WA = "51924519233"
WA_HUMAN = "+51 924 519 233"
LEGAL = {"name": "Pati.pe", "ruc": "20616635485", "address": "Los Totorales 163, San Miguel"}
PLAY_URL = None      # pendiente: enlace de Google Play
IOS_URL = None       # pendiente: enlace de App Store
LAUNCH = "31 oct"
SOCIALS = [("TikTok", None), ("Instagram", None), ("Facebook", None), ("YouTube", None), ("X", None)]  # pendiente: URLs
TODAY = "2026-10-18"
EMAIL = "hola@pati.pe"
# Formulario de contacto:
#   "simulate" → no envía nada: espera un momento y muestra el mensaje de éxito (modo actual, antes del lanzamiento).
#   "live"     → POST JSON a CONTACT_ENDPOINT (la salida contactEndpoint de `pulumi stack output` en infra/).
CONTACT_MODE = "simulate"
CONTACT_ENDPOINT = ""
# Libro de Reclamaciones:
#   "email" → la hoja se genera en pantalla y el consumidor la envía por correo o WhatsApp (hasta activar el backend).
#   "live"  → POST JSON a CLAIMS_ENDPOINT (salida claimsEndpoint de Pulumi): correlativo oficial + copia por correo.
CLAIMS_MODE = "email"
CLAIMS_ENDPOINT = ""

FOUNDERS = [
    {"name": "Nazart Jara", "initials": "NJ", "role": "CEO", "slug": "nazart-jara",
     "line": "Lidera el producto, el negocio y la comunidad de Pati.",
     "linkedin": "https://www.linkedin.com/in/nazartjara/", "game": None},
    {"name": "Daniel Hervias", "initials": "DH", "role": "CTO", "slug": "daniel-hervias",
     "line": "Lidera la tecnología y el equipo que construye la app.",
     "linkedin": "https://www.linkedin.com/in/felix-daniel-hervias-arancibia-1560b5201/", "game": None},
]

NEWS = [
    {"date": "2026-10-31", "label": "31 de octubre de 2026", "title": "Pati sale en Google Play",
     "text": "La primera versión de Pati para Android llega el 31 de octubre. Es gratis para quien compra y los vendedores empiezan con créditos gratis."},
    {"date": "2026-10-31", "label": "31 de octubre de 2026", "title": "Pati sale en App Store",
     "text": "El mismo día llega la versión para iPhone. Así nadie se queda fuera, uses el celular que uses."},
    {"date": "2026-10-16", "label": "16 de octubre de 2026", "title": "Nace Pati.pe como empresa",
     "text": "Constituimos Pati.pe (RUC 20616635485). Es el primer paso formal para construir Pati junto con su comunidad."},
]

FAQ = [
    ("¿Pati es gratis?", "Sí. Para quien compra, siempre. Para quien vende, cada oferta usa 1 crédito y los créditos son gratis: 20 de bienvenida, 15 cada mes y 10 por cada negocio que invites. En el lanzamiento no vendemos créditos; si eso cambia, lo avisaremos antes."),
    ("¿Qué puedo pedir?", "Lo que quieras comprar a un negocio: ropa, insumos, mercadería, equipos o regalos. Mientras más claro tu pedido (qué y cuántos), mejores ofertas recibes."),
    ("¿A qué vendedores llega mi pedido?", "A vendedores del rubro que están cerca de ti, a unos 3 km. Por eso la app usa tu ubicación mientras la usas."),
    ("¿Cómo pago lo que compro?", "Directamente al vendedor, como acuerden entre ustedes. Pati no cobra ni recibe pagos por las compras: si alguien te pide pagar “a Pati”, es un fraude."),
    ("¿Cómo compro seguro?", "Antes de decidir ves la oferta completa, la tienda y su ubicación. Pide comprobante, prefiere medios de pago con respaldo y desconfía de precios demasiado bajos. Si algo sale mal, denuncia la oferta desde la app."),
    ("¿El vendedor ve mi número?", "No. El vendedor ve la descripción, la categoría y las fotos de tu pedido, pero no tu número de celular."),
    ("¿Cómo me registro como vendedor?", "Descarga la app, regístrate con tu celular, completa los datos de tu negocio y tu catálogo. Desde ese momento te llegan pedidos de tu rubro y empiezas con 20 créditos gratis."),
    ("¿Cuándo puedo descargar Pati?", "Pati sale en Google Play y App Store el 31 de octubre de 2026."),
    ("¿Cómo elimino mi cuenta?", "Desde la app, en tu perfil, o pidiéndonoslo por WhatsApp o correo. Te explicamos todo en pati.pe/eliminar-cuenta."),
]

def esc(s): return html.escape(s, quote=True)
def wa(text, origin):
    return "https://wa.me/%s?text=%s" % (WA, urllib.parse.quote("%s (#%s)" % (text, origin)))

# ----------------------------------------------------------------- piezas
ICON_PLAY = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4 2.8v18.4c0 .5.5.8.9.6l9.7-9.8L4.9 2.2c-.4-.2-.9.1-.9.6zM15.6 13l2.6 2.6-11.6 6.5 9-9.1zm0-2L6.6 1.9l11.6 6.5-2.6 2.6zm3.6.6l2.4 1.4c.6.3.6 1.1 0 1.4l-2.4 1.4-2.8-2.8z"/></svg>'
ICON_APPLE = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.4 12.6c0-2.4 2-3.6 2.1-3.7-1.1-1.7-2.9-1.9-3.5-1.9-1.5-.2-2.9.9-3.7.9-.8 0-1.900-.9-3.2-.8-1.6 0-3.1 1-4 2.4-1.7 3-.4 7.3 1.2 9.7.8 1.2 1.8 2.5 3 2.4 1.2 0 1.7-.8 3.1-.8 1.5 0 1.9.8 3.2.8 1.3 0 2.2-1.2 3-2.4.9-1.4 1.3-2.7 1.3-2.8-.1 0-2.5-1-2.5-3.8zM14 5.5c.7-.8 1.1-1.9 1-3-1 0-2.1.7-2.8 1.5-.6.7-1.2 1.8-1 2.9 1.1.1 2.1-.6 2.8-1.4z"/></svg>'
ICON_WA = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/></svg>'
MARK = '<img class="mark" src="/images/pati-mark.svg" alt="" width="1308" height="1544">'

def store(name, url, icon):
    if url:
        return '<a class="btn" href="%s" rel="noopener">%s%s</a>' % (esc(url), icon, name)
    return '<span class="btn soon" aria-label="%s, disponible desde el %s"><span class="soon-row">%s%s</span><small>Desde el %s</small></span>' % (name, LAUNCH, icon, name, LAUNCH)

def stores():
    return '<div class="stores">%s%s</div>' % (store("Google Play", PLAY_URL, ICON_PLAY), store("App Store", IOS_URL, ICON_APPLE))

ICONS_DIR = os.path.join(HERE, "icons")  # Simple Icons (CC0), simple-icons@13.21.0
def social_icon(n):
    svg = open(os.path.join(ICONS_DIR, {"X": "x", "LinkedIn": "linkedin"}.get(n, n.lower()) + ".svg")).read()
    d = re.search(r'<path d="([^"]+)"', svg).group(1)
    return '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="%s"/></svg>' % d

def socials():
    out = []
    for n, u in SOCIALS:
        ic = social_icon(n)
        out.append('<a href="%s" rel="noopener">%s%s</a>' % (esc(u), ic, n) if u else '<span title="Muy pronto">%s%s</span>' % (ic, n))
    return '<div class="socials" aria-label="Redes de Pati">%s</div>' % "".join(out)

NAV = [("/#como-funciona", "Cómo funciona"), ("/nosotros/", "Nosotros"), ("/novedades/", "Novedades"), ("/contacto/", "Contacto")]

def header(show):
    links = "".join('<a href="%s">%s</a>' % (h, t) for h, t in NAV)
    return '''<header class="top%s">
  <div class="wrap">
    <a class="pill" href="/" aria-label="Pati, ir al inicio">%spati</a>
    <div class="top-actions">
      <a class="get" href="/#descargar">Descargar</a>
      <button class="menu-btn" type="button" popovertarget="menu" aria-label="Abrir menú"><span></span><span></span></button>
    </div>
  </div>
</header>
<div id="menu" class="sheet" popover>
  <div class="wrap">
    <div class="sheet-top"><span class="pill">%spati</span><button class="menu-close" type="button" popovertarget="menu" popovertargetaction="hide" aria-label="Cerrar menú">✕</button></div>
    <nav aria-label="Principal">%s</nav>
    <a class="btn" href="/#descargar">Descargar Pati</a>
  </div>
</div>''' % (" show" if show else "", MARK, MARK, links)

def footer():
    return '''<footer>
  <div class="wrap">
    <a class="pill" href="/" aria-label="Pati, ir al inicio">%s pati</a>
    <span class="made">pati.pe · pa' ti, pe.</span>
    <div class="foot-cols">
      <nav aria-label="Producto"><b>Producto</b><a href="/#como-funciona">Cómo funciona</a><a href="/#gratis">Gratis</a><a href="/#faq">Preguntas</a></nav>
      <nav aria-label="Pati"><b>Pati</b><a href="/nosotros/">Nosotros</a><a href="/novedades/">Novedades</a><a href="/contacto/">Contacto</a></nav>
      <nav aria-label="Legal"><b>Legal</b><a href="/privacidad/">Privacidad</a><a href="/terminos/">Términos</a><a href="/libro-de-reclamaciones/">Libro de Reclamaciones</a><a href="/eliminar-cuenta/">Eliminar cuenta</a></nav>
    </div>
    <span>Hecho en Perú [[ico:peru:flag]] · <a href="mailto:%s">%s</a> · WhatsApp %s</span>
    <span>© 2026 %s · RUC %s · %s</span>
  </div>
</footer>''' % (MARK, EMAIL, EMAIL, WA_HUMAN, LEGAL["name"], LEGAL["ruc"], LEGAL["address"])

ORG = {
    "@type": "Organization", "@id": SITE + "/#organization", "name": "Pati", "legalName": LEGAL["name"],
    "url": SITE + "/", "logo": SITE + "/images/pati-logo.png", "taxID": LEGAL["ruc"],
    "foundingDate": "2026-10-16",
    "address": {"@type": "PostalAddress", "streetAddress": "Los Totorales 163", "addressLocality": "San Miguel", "addressCountry": "PE"},
    "email": EMAIL,
    "contactPoint": {"@type": "ContactPoint", "telephone": "+" + WA, "email": EMAIL, "contactType": "customer support", "availableLanguage": "es",
                     "hoursAvailable": {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "20:00"}},
    "description": "Pati es una app peruana y gratuita: cuentas qué quieres comprar y los vendedores te responden con su precio.",
}
ORG["founder"] = [{"@type": "Person", "name": n, "jobTitle": r, "sameAs": [l]} for n, r, l in [
    ("Nazart Jara", "CEO", "https://www.linkedin.com/in/nazartjara/"),
    ("Daniel Hervias", "CTO", "https://www.linkedin.com/in/felix-daniel-hervias-arancibia-1560b5201/")]]
_same = [u for _, u in SOCIALS if u]
if _same: ORG["sameAs"] = _same

def page(path, title, desc, body, show_header=True, extra_ld=None, robots="index, follow"):
    canon = SITE + path
    graph = [ORG, {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Pati", "inLanguage": "es-PE", "publisher": {"@id": SITE + "/#organization"}}]
    if extra_ld: graph += extra_ld
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    doc = '''<!DOCTYPE html>
<html lang="es-PE">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#FFD23F">
<link rel="canonical" href="{canon}">
<link rel="icon" href="/images/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/images/pati-logo.png" type="image/png">
<link rel="apple-touch-icon" href="/images/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Pati">
<meta property="og:locale" content="es_PE">
<meta property="og:url" content="{canon}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{site}/images/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{site}/images/og-image.png">
<script>document.documentElement.classList.add('js')</script>
<link rel="preload" href="/fonts/bricolage-grotesque-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/fonts.css">
<link rel="stylesheet" href="/css/base.css">
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
{header}

<main>
{body}
</main>

{footer}
<script src="/js/site.js" defer></script>
</body>
</html>
'''.format(title=esc(title), desc=esc(desc), robots=robots, canon=canon, site=SITE, ld=ld,
           header=header(show_header), body=body.strip(), footer=footer())
    doc = re.sub(r"\[\[ico:(\w+)(?::([\w-]+))?\]\]", lambda m: icon(m.group(1), m.group(2) or "ico"), doc)
    out = os.path.join(ROOT, path.strip("/"), "index.html") if path.endswith("/") and path != "/" else os.path.join(ROOT, "index.html" if path == "/" else path.strip("/"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(doc)
    return out

# ----------------------------------------------------------------- home
def news_cards(items, cls="card post"):
    return "\n".join('<article class="%s"><time datetime="%s">%s</time><h3>%s</h3><p>%s</p></article>' % (cls, n["date"], n["label"], n["title"], n["text"]) for n in items)

def avatar(f, size=184):
    photo = "/images/team/%s.webp" % f["slug"]
    if os.path.exists(os.path.join(WEB, photo.lstrip("/"))):
        return '<img class="avatar" src="%s" alt="Foto de %s" width="%d" height="%d" loading="lazy">' % (photo, f["name"], size, size)
    return '<span class="avatar" aria-hidden="true">%s</span>' % f["initials"]

faq_html = "\n".join('      <details><summary>%s</summary><p>%s</p></details>' % (q, a) for q, a in FAQ)
faq_ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}

HOME = '''
<!-- 1 · HERO -->
<section class="hero">
  <span class="blob b1"></span><span class="blob b2"></span><span class="blob b3"></span>
  <div class="wrap">
    <div>
      <a class="lockup" href="/" aria-label="Pati">{mark}<b>pati</b></a>
      <span class="made-chip">Pa' ti, pe [[ico:peru:flag]]</span>
      <h1>Pide una vez. <mark>Te mandan precios.</mark></h1>
      <p class="sub">Cuenta qué quieres comprar y los vendedores te mandan su precio. Tú eliges. Gratis, pe.</p>
      <div class="ctas">
        {stores}
        <a class="seller" href="#para-quien">¿Vendes? Así te llegan clientes →</a>
      </div>
      <span class="beta"><i></i>Recién empezamos. Constrúyela con nosotros.</span>
    </div>

    <div class="phone" role="img" aria-label="Ejemplo ilustrativo: un pedido de 20 polos estampados recibe tres ofertas en Pati">
      <span class="best" aria-hidden="true">¡Gratis pa' ti!</span>
      <div class="screen" data-play aria-hidden="true">
        <div class="msg">Busco <b>20 polos estampados</b> para mi promoción. ¿Quién los tiene?</div>
        <div class="offer"><span>Taller de estampado</span><strong>S/ 18</strong><small>A 350 m de ti</small></div>
        <div class="offer"><span>Confecciones</span><strong>S/ 16.50</strong><small>A 800 m de ti</small><img class="mark drop" src="/images/pati-mark.svg" alt="" width="1308" height="1544"></div>
        <div class="offer"><span>Tienda de polos</span><strong>S/ 17</strong><small>A 1.2 km de ti</small></div>
      </div>
    </div>
  </div>
</section>

<!-- 2 · CÓMO FUNCIONA -->
<section class="how" id="como-funciona">
  <span class="blob"></span>
  <div class="wrap">
    <h2 class="h2">Así de <mark>simple.</mark></h2>
    <p class="lead">Tres pasos y cero llamadas para cotizar.</p>
    <ol class="steps">
      <li><div><h3>Publica lo que buscas</h3><p>Qué producto, cuántos y para cuándo.</p></div></li>
      <li><div><h3>Te llegan precios al toque</h3><p>Tu pedido llega a vendedores de ese rubro cerca de ti, y te mandan su oferta en minutos.</p></div></li>
      <li><div><h3>Comparas y eliges</h3><p>Ves el precio, la tienda y cómo llegar. Eliges la oferta que más te conviene.</p></div></li>
    </ol>
  </div>
</section>

<!-- 3 · PARA QUIÉN -->
<section class="who" id="para-quien">
  <span class="blob b1"></span>
  <div class="wrap">
    <h2 class="h2">Hecha para los dos lados.</h2>
    <div class="duo">
      <article class="card">
        <span class="tag">Pa' ti si compras</span>
        <h3>Deja de preguntar en diez tiendas.</h3>
        <ul>
          <li><div><b>Ahorra horas</b><span>Un pedido reemplaza decenas de llamadas y mensajes.</span></div></li>
          <li><div><b>Compara de verdad</b><span>Sabes si estás pagando de más.</span></div></li>
          <li><div><b>Cerca de ti</b><span>Ves la tienda y la ruta antes de ir.</span></div></li>
        </ul>
        <a class="btn" href="#descargar">Descargar Pati</a>
      </article>
      <article class="card">
        <span class="tag tag-orange">Pa' ti si vendes</span>
        <h3>Que los clientes te encuentren a ti.</h3>
        <ul>
          <li><div><b>Clientes que ya quieren comprar</b><span>Cada pedido es alguien que necesita lo que vendes.</span></div></li>
          <li><div><b>Solo de tu rubro</b><span>Y tú eliges a cuáles responder.</span></div></li>
          <li><div><b>Todo desde tu celular</b><span>Respondes en segundos desde la app.</span></div></li>
        </ul>
        <a class="btn light" href="#gratis">Cómo funcionan los créditos</a>
      </article>
    </div>
  </div>
</section>

<!-- 4 · GRATIS -->
<section class="free" id="gratis">
  <div class="wrap">
    <h2 class="h2">Gratis, y te contamos <mark>cómo funciona.</mark></h2>
    <div class="free-grid">
      <article class="card buyer">
        <span class="tag">Pa' ti si compras</span>
        <p class="big">Gratis. Siempre.</p>
        <p>Pedir y recibir ofertas no te cuesta nada.</p>
      </article>
      <article class="card">
        <span class="tag tag-orange">Pa' ti si vendes</span>
        <p class="big big-sm">Siempre tendrás créditos gratis.</p>
        <p>Cada oferta que envías usa 1 crédito. Y los créditos te llegan gratis:</p>
        <div class="earn">
          <div><em>[[ico:gift]]</em><p><b>20 de bienvenida + 15 cada mes</b><span>Gratis, para que respondas pedidos desde el primer día.</span></p></div>
          <div><em>[[ico:chat]]</em><p><b>Comparte tu código</b><span>Invita a otro negocio: ganan 10 créditos cada uno.</span></p></div>
        </div>
      </article>
    </div>
    <p class="promise">[[ico:megaphone]]<span>En el lanzamiento todo es gratis. Si algún día vendemos créditos, te lo contamos antes.</span></p>
  </div>
</section>

<!-- 5 · COMUNIDAD -->
<section class="community" id="comunidad">
  <span class="blob b1"></span>
  <div class="wrap">
    <h2 class="h2">Pati se construye <mark>contigo.</mark></h2>
    <p class="lead">Recién empezamos. Cada mejora sale de lo que nos cuentan, y lo mostramos todo en redes.</p>
    <div class="road">
      <div class="col"><h3><i></i>Llega en la primera versión</h3><ul><li>Publicar pedidos</li><li>Recibir ofertas</li><li>Ver la tienda y la ruta</li></ul></div>
      <div class="col"><h3><i></i>Estamos haciendo</h3><ul><li>Las apps para Android y iPhone, listas el 31 de octubre</li></ul></div>
      <div class="col"><h3><i></i>Lo pidieron ustedes</h3><ul><li>Esta lista la llenan ustedes.</li></ul></div>
    </div>
    <a class="card post latest" href="/novedades/"><span class="kicker-dark">Lo último · {latest_label}</span><h3>{latest_title}</h3><span class="net">Ver todas las novedades →</span></a>
    <div class="ctas">
      <a class="btn wa" href="{wa_idea}">{icon_wa}Cuéntanos qué mejorar</a>
    </div>
    {socials}
  </div>
</section>

<!-- 6 · NOSOTROS (adelanto) -->
<section class="teaser" id="nosotros">
  <div class="wrap">
    <div class="duo-faces">{faces}</div>
    <h2 class="h2">Somos Nazart y Daniel.</h2>
    <p class="lead">Construimos Pati para las micro y pequeñas empresas, que son el 99% de las empresas del Perú.</p>
    <a class="btn light" href="/nosotros/">Conoce nuestra historia →</a>
  </div>
</section>

<!-- 7 · FAQ -->
<section class="faq" id="faq">
  <div class="wrap">
    <h2 class="h2">Preguntas frecuentes.</h2>
    <div class="faq-list">
{faq}
    </div>
  </div>
</section>

<!-- 8 · CIERRE -->
<section class="end" id="descargar">
  <span class="blob b1"></span><span class="blob b2"></span>
  <div class="wrap">
    <img class="mark big-mark" src="/images/pati-mark.svg" alt="" width="1308" height="1544">
    <h2 class="h2">Tu próximo pedido, <mark>sin perseguir a nadie.</mark></h2>
    <p class="pe">Descárgala, pe.</p>
    <div class="ctas">
      {stores}
      <a class="btn light" href="/contacto/">¿Hablamos? Contáctanos</a>
    </div>
    {socials}
  </div>
</section>
'''.format(mark=MARK, stores=stores(), socials=socials(), icon_wa=ICON_WA,
           wa_idea=esc(wa("Hola Pati, tengo una idea para mejorar la app:", "comunidad")),
           latest_label=NEWS[0]["label"], latest_title=NEWS[0]["title"],
           faces="".join(avatar(f) for f in FOUNDERS), faq=faq_html)

page("/", "Pati: pide una vez y te mandan precios. Gratis, pe.",
     "Cuenta qué quieres comprar y los vendedores te responden con su precio. Compara y elige. App peruana y gratuita para compradores; los vendedores siempre tienen créditos gratis.",
     HOME, show_header=False, extra_ld=[faq_ld])

# ----------------------------------------------------------------- páginas internas
def inner(title, sub):
    return '''<section class="page-hero">
  <span class="blob b1"></span>
  <div class="wrap">
    <h1 class="h2">%s</h1>
    <p>%s</p>
  </div>
</section>''' % (title, sub)

timeline = "\n".join('<article class="card"><time datetime="%s">%s</time><h2>%s</h2><p>%s</p></article>' % (n["date"], n["label"], n["title"], n["text"]) for n in NEWS)
page("/novedades/", "Novedades de Pati: lo que vamos construyendo",
     "La bitácora de Pati: cada lanzamiento, mejora y aprendizaje, contado en público.",
     inner("Novedades.", "Todo lo que vamos construyendo, paso a paso. También lo contamos en nuestras redes.") + '''
<section class="news">
  <div class="wrap">
    <div class="timeline">
%s
    </div>
  </div>
</section>''' % timeline)

CONTACT = 'por WhatsApp al <a href="%s">%s</a>' % (esc(wa("Hola Pati, tengo una consulta sobre mis datos:", "privacidad")), WA_HUMAN)
LEGAL_BLOCK = '<div class="legal-data"><span><strong>Razón social:</strong> %s</span><span><strong>RUC:</strong> %s</span><span><strong>Domicilio:</strong> %s</span></div>' % (LEGAL["name"], LEGAL["ruc"], LEGAL["address"])

import legal
_wa_priv = esc(wa("Hola Pati, tengo una consulta sobre mis datos:", "privacidad"))
_wa_terms = esc(wa("Hola Pati, tengo una consulta sobre los términos:", "terminos"))
_wa_del = esc(wa("Hola Pati, quiero eliminar mi cuenta. Mi número registrado es:", "eliminar-cuenta"))

page("/privacidad/", "Política de privacidad · Pati",
     "Qué datos usa la app Pati, para qué, con quién los compartimos y cómo ejercer tus derechos (Ley N.º 29733).",
     inner("Política de privacidad.", "Cómo cuidamos tus datos, en palabras simples.") + legal.privacy(LEGAL, EMAIL, _wa_priv, WA_HUMAN))

page("/terminos/", "Términos y condiciones · Pati",
     "Reglas de uso de Pati para compradores y vendedores: cómo funciona, créditos, conductas prohibidas y responsabilidades.",
     inner("Términos y condiciones.", "Las reglas del juego, claras para todos.") + legal.terms(LEGAL, EMAIL, _wa_terms, WA_HUMAN))

page("/eliminar-cuenta/", "Eliminar tu cuenta · Pati",
     "Cómo eliminar tu cuenta de Pati desde la app o sin ella, qué datos se borran y en qué plazo.",
     inner("Eliminar tu cuenta.", "Desde la app o pidiéndonoslo, cuando quieras.") + legal.delete_account(EMAIL, _wa_del, WA_HUMAN).replace("[[wa]]", ICON_WA))

page("/libro-de-reclamaciones/", "Libro de Reclamaciones · Pati",
     "Libro de Reclamaciones virtual de Pati.pe: presenta tu reclamo o queja conforme al Código de Protección y Defensa del Consumidor.",
     inner("Libro de Reclamaciones.", "Conforme al Código de Protección y Defensa del Consumidor (Ley N.º 29571).") + legal.claims_book(LEGAL, EMAIL, CLAIMS_MODE, CLAIMS_ENDPOINT, esc))

# 404 (Amplify la sirve si se configura la regla 404 en la consola)
# ----------------------------------------------------------------- nosotros
def founder_cards():
    out = []
    for f in FOUNDERS:
        out.append('''      <article class="person big">%s<div><h3>%s</h3><span class="role">%s</span><p>%s</p><span class="game">[[ico:game:ico-sm]] Su juego: %s</span><a class="in" href="%s" rel="noopener" target="_blank">%sLinkedIn</a></div></article>''' % (
            avatar(f), f["name"], f["role"], f["line"], f["game"], esc(f["linkedin"]), social_icon("LinkedIn"))
            if f.get("game") else
            '''      <article class="person big">%s<div><h3>%s</h3><span class="role">%s</span><p>%s</p><a class="in" href="%s" rel="noopener" target="_blank">%sLinkedIn</a></div></article>''' % (
            avatar(f), f["name"], f["role"], f["line"], esc(f["linkedin"]), social_icon("LinkedIn")))
    return "\n".join(out)

ABOUT = '''
<section class="page-hero about-hero">
  <span class="blob b1"></span>
  <div class="wrap">
    <div class="duo-faces">{faces}</div>
    <h1 class="h2">Somos Nazart <mark>y Daniel.</mark></h1>
    <p>Socios, programadores y gamers. Construimos Pati pa' las mypes del Perú.</p>
  </div>
</section>

<section class="story" id="historia">
  <span class="blob b1"></span>
  <div class="wrap">
    <h2 class="h2">Por qué construimos <mark>Pati.</mark></h2>
    <ol class="chapters">
      <li class="card"><span class="kicker">El origen</span><h3>Muchas empresas, y luego dos años juntos.</h3><p>Los dos venimos de trabajar en muchas empresas. Después de dos años trabajando juntos nos dimos cuenta de que coincidíamos en lo importante: la tecnología tiene que estar al servicio de los negocios.</p></li>
      <li class="card stat"><span class="num">99%</span><p>de las empresas del Perú son micro y pequeñas empresas.</p><small>Fuente: Ministerio de la Producción (PRODUCE).</small></li>
      <li class="card"><span class="kicker">El porqué</span><h3>Aportar al país, empezando por las mypes.</h3><p>Siempre pensamos que había que devolverle algo al Perú. Si casi todas sus empresas son micro y pequeñas, es ahí donde la tecnología puede cambiar más cosas.</p></li>
      <li class="card"><span class="kicker">16 de octubre de 2026</span><h3>Nace Pati.pe.</h3><p>Constituimos la empresa para hacerlo en serio, juntando las dos cosas que más nos apasionan: la tecnología y los negocios.</p></li>
    </ol>
  </div>
</section>

<section class="vision-sec">
  <div class="wrap">
    <blockquote class="vision">
      <p>“No queremos ser una sola solución, sino un <mark>conjunto de soluciones</mark> que nazcan del dolor real del empresario.”</p>
    </blockquote>
    <ol class="path">
      <li class="card"><span class="kicker-dark">Hoy</span><h3>Conectar a quien compra con quien vende.</h3></li>
      <li class="card"><span class="kicker-dark">Después</span><h3>Entrar en la cadena de valor de cada negocio.</h3></li>
      <li class="card"><span class="kicker-dark">La meta</span><h3>Un ecosistema de soluciones pensado desde las necesidades del empresario.</h3></li>
    </ol>
  </div>
</section>

<section class="team" id="equipo">
  <div class="wrap">
    <h2 class="h2">Los fundadores.</h2>
    <div class="people">
{founders}
    </div>
    <div class="facts" aria-label="Datos curiosos">
      <span>[[ico:game:ico-sm]]StarCraft y FIFA, nuestros juegos</span>
      <span>[[ico:code:ico-sm]]Amamos programar</span>
      <span>[[ico:duo:ico-sm]]2 años trabajando juntos antes de Pati</span>
      <span>[[ico:peru:ico-sm]]Hechos en Perú</span>
    </div>
  </div>
</section>

<section class="principles-sec">
  <div class="wrap">
    <h2 class="h2">Cómo trabajamos.</h2>
    <div class="principles">
      <article class="card"><h3>Construimos en público</h3><p>Contamos lo que hacemos, lo que falla y lo que viene.</p></article>
      <article class="card"><h3>Claros con lo que cuesta</h3><p>Comprar es gratis. Para vender siempre hay créditos gratis, y avisamos antes de cualquier cambio.</p></article>
      <article class="card"><h3>Desde el dolor del empresario</h3><p>Primero escuchamos qué le cuesta a un negocio. Después escribimos código.</p></article>
      <article class="card"><h3>Hecho en Perú, pa' ti</h3><p>Pensado para cómo se compra y se vende aquí.</p></article>
    </div>
  </div>
</section>

<section class="trust">
  <div class="wrap">
    <div class="card company">
      <h2>La empresa</h2>
      {legal}
      <span><strong>Constituida:</strong> 16 de octubre de 2026</span>
    </div>
    <div class="cta-row">
      <a class="btn" href="/contacto/">¿Hablamos? Contáctanos</a>
    </div>
    {socials}
  </div>
</section>
'''

about_ld = {"@type": "AboutPage", "url": SITE + "/nosotros/", "name": "Nosotros · Pati", "about": {"@id": SITE + "/#organization"}}

# ----------------------------------------------------------------- contacto
CONTACT_PAGE = '''
<section class="page-hero">
  <span class="blob b1"></span>
  <div class="wrap">
    <h1 class="h2">Hablemos, <mark>pe.</mark></h1>
    <p>Respondemos de lunes a viernes, de 8 a. m. a 8 p. m.</p>
  </div>
</section>

<section class="trust">
  <div class="wrap">
    <h2 class="h2 h2-sm">¿Qué necesitas?</h2>
    <div class="channels">
      <article class="card"><span class="ch-ico">[[ico:phone]]</span><h3>Uso la app o tengo un problema</h3><p>Te ayudamos por WhatsApp.</p><a class="btn wa" href="{wa_help}">{icon_wa}Escribir por WhatsApp</a></article>
      <article class="card"><span class="ch-ico">[[ico:idea]]</span><h3>Tengo una idea para Pati</h3><p>Nos encanta. Las mejores entran a la hoja de ruta.</p><a class="btn wa" href="{wa_idea}">{icon_wa}Contar mi idea</a></article>
      <article class="card"><span class="ch-ico">[[ico:brief]]</span><h3>Prensa, alianzas o inversión</h3><p>Escríbenos al correo o directo a los fundadores.</p><a class="btn" href="mailto:{email}">{email}</a><div class="in-row">{linkedins}</div></article>
      <article class="card"><span class="ch-ico">[[ico:book]]</span><h3>Quiero presentar un reclamo</h3><p>Usa nuestro Libro de Reclamaciones.</p><a class="btn light" href="/libro-de-reclamaciones/">Ir al Libro de Reclamaciones</a></article>
    </div>
  </div>
</section>

<section class="faq" id="mensaje">
  <div class="wrap">
    <h2 class="h2 h2-sm">O déjanos un mensaje.</h2>
    <form class="card contact-form" data-contact data-mode="{mode}" data-endpoint="{endpoint}" data-mailto="{email}" action="{action}" method="post" novalidate>
      <label>Nombre<input name="name" type="text" autocomplete="name" required maxlength="120" enterkeyhint="next"></label>
      <label>Correo<input name="email" type="email" autocomplete="email" required maxlength="160" autocapitalize="none" enterkeyhint="next"></label>
      <label>Celular <small>(opcional)</small><input name="phone" type="tel" autocomplete="tel" inputmode="tel" maxlength="20" enterkeyhint="next"></label>
      <label>Motivo<select name="reason" required>
        <option value="">Elige una opción</option>
        <option>Uso de la app</option><option>Idea o sugerencia</option><option>Quiero vender en Pati</option>
        <option>Prensa</option><option>Alianzas</option><option>Inversión</option><option>Otro</option>
      </select></label>
      <label>Mensaje<textarea name="message" rows="5" required maxlength="2000" enterkeyhint="send"></textarea></label>
      <label class="hp" aria-hidden="true">No llenar<input name="website" type="text" tabindex="-1" autocomplete="off"></label>
      <label class="check"><input name="consent" type="checkbox" required><span>Acepto que Pati use estos datos para responderme, según su <a href="/privacidad/">política de privacidad</a>.</span></label>
      <button class="btn" type="submit">Enviar mensaje</button>
      <p class="form-status" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>

<section class="trust">
  <div class="wrap">
    <div class="card company">
      <h2>Datos de contacto</h2>
      <div class="legal-data">
        <span><strong>Correo:</strong> <a href="mailto:{email}">{email}</a></span>
        <span><strong>WhatsApp:</strong> <a href="{wa_help}">{wa_human}</a></span>
        <span><strong>Horario:</strong> lunes a viernes, de 8 a. m. a 8 p. m.</span>
      </div>
      {legal}
    </div>
    {socials}
  </div>
</section>
'''

contact_ld = {"@type": "ContactPage", "url": SITE + "/contacto/", "name": "Contacto · Pati", "about": {"@id": SITE + "/#organization"}}


LEGAL_BLOCK_ = LEGAL_BLOCK
page("/nosotros/", "Nosotros · Pati: quiénes somos y por qué construimos Pati",
     "Somos Nazart Jara y Daniel Hervias. Construimos Pati para las micro y pequeñas empresas del Perú: nuestra historia, visión y cómo trabajamos.",
     ABOUT.format(faces="".join(avatar(f) for f in FOUNDERS), founders=founder_cards(), legal=LEGAL_BLOCK, socials=socials()),
     extra_ld=[about_ld])

page("/contacto/", "Contacto · Pati",
     "Escríbenos por WhatsApp o al correo hola@pati.pe. Atendemos de lunes a viernes, de 8 a. m. a 8 p. m.",
     CONTACT_PAGE.format(wa_help=esc(wa("Hola Pati, necesito ayuda con la app:", "contacto-soporte")),
                         wa_idea=esc(wa("Hola Pati, tengo una idea:", "contacto-idea")),
                         icon_wa=ICON_WA, email=EMAIL, wa_human=WA_HUMAN, legal=LEGAL_BLOCK, socials=socials(),
                         mode=CONTACT_MODE, endpoint=esc(CONTACT_ENDPOINT), action=esc(CONTACT_ENDPOINT or ("mailto:" + EMAIL)),
                         linkedins="".join('<a class="in" href="%s" rel="noopener" target="_blank">%s%s</a>' % (esc(f["linkedin"]), social_icon("LinkedIn"), f["name"].split()[0]) for f in FOUNDERS)),
     extra_ld=[contact_ld])

p404 = page("/404.html", "Página no encontrada · Pati", "Esta página no existe.",
     inner("Esta página no existe, pe.", "Pero lo que buscas puede estar a un pedido de distancia.") + '''
<section class="trust"><div class="wrap"><a class="btn" href="/">Volver al inicio</a></div></section>''', robots="noindex")

# ----------------------------------------------------------------- css, js, fuentes
css = open(os.path.join(HERE, "base.css")).read()
css = css.replace("--font:'Bricolage Grotesque',system-ui,sans-serif;", "--font:'Bricolage Grotesque',system-ui,sans-serif;")
css = re.sub(r"/\* notas de revisión del prototipo \*/\n\.todo\{[^}]*\}\n", "", css)
css = css.replace(".js .screen.on ~ .drop,.js .phone.on .drop", ".js .phone.on .drop")
css = css.replace("section > .wrap{position:relative;z-index:1}", "section > .wrap{position:relative;z-index:1}\n.tag-orange{background:var(--orange)!important;color:#fff!important}\n.big-sm{font-size:clamp(30px,8vw,44px)!important}")
for a, b in [(".how .h2 mark{background:var(--yellow)}", ".how .h2 mark{--mk:var(--yellow)}"),
             (".community .h2 mark{background:var(--yellow)}", ".community .h2 mark{--mk:var(--yellow)}"),
             (".end .h2 mark{background:#fff}", ".end .h2 mark{--mk:#fff}")]:
    assert a in css, a
    css = css.replace(a, b)
css = css.replace("mark{background:#fff;color:#1E1340;", "mark{color:#1E1340;")
css = css.replace(".mark{display:block;aspect-ratio:1308/1544;height:auto}", ".mark{display:block;height:auto}")
css = css.replace("footer .pill{justify-self:start;font-size:28px;box-shadow:3px 3px 0 #000}", "footer .pill{justify-self:start;font-size:28px;box-shadow:3px 3px 0 #000;color:#1E1340}")
css += open(os.path.join(HERE, "pages.css")).read()
os.makedirs(os.path.join(ROOT, "css"), exist_ok=True)
os.makedirs(os.path.join(ROOT, "js"), exist_ok=True)
open(os.path.join(ROOT, "css", "base.css"), "w").write("/* Pati: estilos del sitio (diseño v3 \"Color peruano\"), mobile-first. */\n" + css.strip() + "\n")

open(os.path.join(ROOT, "css", "fonts.css"), "w").write("""/* Bricolage Grotesque (variable: opsz 12–96, wght 400–800), auto-alojada. */
@font-face{font-family:'Bricolage Grotesque';font-style:normal;font-weight:400 800;font-stretch:100%;font-display:swap;src:url(/fonts/bricolage-grotesque-latin-ext.woff2) format('woff2');unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C4,U+2113,U+2C60-2C7F,U+A720-A7FF}
@font-face{font-family:'Bricolage Grotesque';font-style:normal;font-weight:400 800;font-stretch:100%;font-display:swap;src:url(/fonts/bricolage-grotesque-latin.woff2) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
""")

open(os.path.join(ROOT, "js", "site.js"), "w").write("""// Única JS del sitio. Sin JS todo se ve completo (la clase html.js la pone un script inline en <head>).
// 1) El chat de ejemplo del hero se anima la primera vez que entra en pantalla.
// 2) En la home, el header fijo aparece cuando el logo grande del hero sale de pantalla.
// 3) Entradas suaves de títulos y tarjetas al hacer scroll.\n// 4) Cierra el menú al elegir un enlace. 5) Envía el formulario de contacto (simulado, endpoint o mailto).
(function () {
  var hasIO = 'IntersectionObserver' in window;
  var chat = document.querySelector('[data-play]');
  if (chat) {
    var play = function () { chat.classList.add('on'); chat.parentNode.classList.add('on'); };
    if (!hasIO) play();
    else {
      var io = new IntersectionObserver(function (es) {
        if (es[0].isIntersecting) { play(); io.disconnect(); }
      }, { threshold: 0.35 });
      io.observe(chat);
    }
  }
  var top = document.querySelector('.top');
  var lockup = document.querySelector('.lockup');
  if (top && lockup) {
    if (!hasIO) top.classList.add('show');
    else new IntersectionObserver(function (es) {
      top.classList.toggle('show', !es[0].isIntersecting);
    }).observe(lockup);
  }
  // 4) El menú (popover nativo) se cierra al elegir un enlace.
  var menu = document.getElementById('menu');
  if (menu && menu.hidePopover) {
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) menu.hidePopover(); });
  }
  // 5) Formulario de contacto: envía JSON al endpoint; si aún no hay endpoint, abre el correo.
  var form = document.querySelector('form[data-contact]');
  if (form) {
    var status = form.querySelector('.form-status');
    var say = function (msg, kind) { status.textContent = msg; status.className = 'form-status ' + (kind || ''); };
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var bad = [].filter.call(form.elements, function (el) { return el.willValidate && !el.checkValidity(); });
      [].forEach.call(form.elements, function (el) { if (el.willValidate) el.setAttribute('aria-invalid', bad.indexOf(el) > -1 ? 'true' : 'false'); });
      if (bad.length) { say('Revisa los campos marcados.', 'err'); bad[0].focus(); return; }
      var d = {};
      ['name', 'email', 'phone', 'reason', 'message', 'website'].forEach(function (k) { d[k] = (form.elements[k].value || '').trim(); });
      if (d.website) return; // honeypot: lo llenan los bots
      delete d.website;
      d.page = location.pathname;
      var endpoint = form.getAttribute('data-endpoint');
      var btn = form.querySelector('button[type=submit]');
      var done = function () {
        form.innerHTML = '<div class="form-done"><h3>¡Gracias, ' + d.name.split(' ')[0].replace(/[<>&"]/g, '') + '!</h3><p>Recibimos tu mensaje. Te respondemos de lunes a viernes, de 8 a. m. a 8 p. m. Si es urgente, escríbenos por WhatsApp.</p></div>';
      };
      if (form.getAttribute('data-mode') === 'simulate') {
        btn.disabled = true; say('Enviando…');
        setTimeout(done, 700);
        return;
      }
      if (!endpoint) {
        var body = 'Nombre: ' + d.name + '\\nCorreo: ' + d.email + '\\nCelular: ' + d.phone + '\\n\\n' + d.message;
        location.href = 'mailto:' + form.getAttribute('data-mailto') + '?subject=' + encodeURIComponent('[' + d.reason + '] Mensaje desde pati.pe') + '&body=' + encodeURIComponent(body);
        say('Abrimos tu app de correo con el mensaje listo para enviar.', 'ok');
        return;
      }
      btn.disabled = true; say('Enviando…');
      fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(d) })
        .then(function (r) { if (!r.ok) throw new Error(r.status); })
        .then(done)
        .catch(function () {
          btn.disabled = false;
          say('No pudimos enviarlo. Inténtalo de nuevo o escríbenos a ' + form.getAttribute('data-mailto') + '.', 'err');
        });
    });
  }
  // 3) Entradas suaves al hacer scroll (una sola vez). Los hermanos entran escalonados.
  var sel = 'main section:not(.hero) .h2, main section:not(.hero) .lead, .bridge, .channels .card, .principles .card, .path .card, .company, .duo-faces, .promise, .card, .steps li, .person, .road .col, .faq-list details, .socials, .more, .page-hero p, .vision, .vision-text, .facts';
  var els = [].slice.call(document.querySelectorAll(sel));
  if (!hasIO || !els.length) return;
  els.forEach(function (el) {
    var sibs = [].filter.call(el.parentNode.children, function (c) { return els.indexOf(c) > -1; });
    el.style.transitionDelay = Math.min(sibs.indexOf(el), 4) * 80 + 'ms';
    el.classList.add('rv');
  });
  var ro = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      var el = e.target;
      el.classList.add('in');
      ro.unobserve(el);
      setTimeout(function () { el.style.transitionDelay = ''; el.classList.add('done'); }, 1200);
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
  els.forEach(function (el) { ro.observe(el); });
})();
""")
with open(os.path.join(ROOT, "js", "site.js"), "a") as _f:
    _f.write(open(os.path.join(HERE, "claims.js")).read())


# ----------------------------------------------------------------- llms.txt y sitemap
llms = """# Pati

> Pati es una app peruana y gratuita para comprar y vender: cuentas qué quieres comprar y los vendedores te responden con su precio. Tú comparas y eliges. "pati.pe" se lee "pa' ti, pe".

## Cómo funciona

1. Publica lo que buscas: qué producto, cuántos y para cuándo.
2. Te llegan precios: tu pedido llega a vendedores del rubro cercanos (unos 3 km) y ellos te mandan su oferta en minutos.
3. Comparas y eliges: ves precio, la tienda y la ruta, y eliges la oferta que te conviene.

## Cuánto cuesta

- Para quien compra: gratis, siempre.
- Para quien vende: enviar una oferta usa 1 crédito. Créditos gratis: 20 de bienvenida, 15 cada mes calendario (no acumulables) y 10 por referido (el nuevo vendedor recibe 10 al completar su catálogo; quien invitó, 10 cuando el nuevo envía su primera oferta).
- Durante el lanzamiento Pati no vende créditos. Si se habilita la compra, se avisará antes.
- Pati no cobra ni recibe pagos por las compras: el pago se acuerda directamente con el vendedor.

## Disponibilidad

Pati sale en Google Play y App Store el 31 de octubre de 2026.

## Comunidad

Pati se construye en público con su comunidad: publicamos lo que hacemos en TikTok, Instagram, Facebook, YouTube y X, y recibimos ideas por WhatsApp ({wa}).

## Preguntas frecuentes

{faq}

## Novedades

{news}

## Empresa

- Razón social: {name}
- RUC: {ruc}
- Domicilio: {addr}
- Equipo: Nazart Jara (CEO, https://www.linkedin.com/in/nazartjara/) y Daniel Hervias (CTO, https://www.linkedin.com/in/felix-daniel-hervias-arancibia-1560b5201/).

## Historia

Nazart y Daniel vienen de trabajar en muchas empresas y decidieron fundar Pati después de dos años trabajando juntos. Coinciden en que hay que aportar al país, empezando por las micro y pequeñas empresas, que son el 99% de las empresas del Perú. Les apasionan la tecnología, los negocios, programar y los videojuegos (StarCraft y FIFA). Constituyeron Pati.pe el 16 de octubre de 2026.

Visión: Pati empieza conectando a quien compra con quien vende, pero busca ser un ecosistema empresarial, un conjunto de soluciones que nazcan del dolor real del empresario y se integren en su cadena de valor.

## Contacto

- Correo: {email}
- WhatsApp: {wa}
- Horario: lunes a viernes, de 8 a. m. a 8 p. m.

## Páginas

- [Inicio]({site}/)
- [Nosotros]({site}/nosotros/)
- [Novedades]({site}/novedades/)
- [Contacto]({site}/contacto/)
- [Política de privacidad]({site}/privacidad/)
- [Términos y condiciones]({site}/terminos/)
- [Libro de Reclamaciones]({site}/libro-de-reclamaciones/)
- [Eliminar tu cuenta]({site}/eliminar-cuenta/)
""".format(wa=WA_HUMAN, email=EMAIL, site=SITE, name=LEGAL["name"], ruc=LEGAL["ruc"], addr=LEGAL["address"],
           faq="\n\n".join("**%s**\n%s" % (q, a) for q, a in FAQ),
           news="\n".join("- %s: %s. %s" % (n["label"], n["title"], n["text"]) for n in NEWS))
open(os.path.join(ROOT, "llms.txt"), "w").write(llms)

urls = [("/", "weekly", "1.0"), ("/nosotros/", "monthly", "0.7"), ("/contacto/", "monthly", "0.6"), ("/novedades/", "weekly", "0.8"), ("/privacidad/", "yearly", "0.3"), ("/terminos/", "yearly", "0.3"), ("/libro-de-reclamaciones/", "yearly", "0.3"), ("/eliminar-cuenta/", "yearly", "0.3")]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    "  <url>\n    <loc>%s%s</loc>\n    <lastmod>%s</lastmod>\n    <changefreq>%s</changefreq>\n    <priority>%s</priority>\n  </url>\n" % (SITE, u, TODAY, f, p) for u, f, p in urls) + "</urlset>\n"
open(os.path.join(ROOT, "sitemap.xml"), "w").write(sm)
print("ok")
