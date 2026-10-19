"""Íconos propios de Pati, con el mismo lenguaje que el logo y las tarjetas sticker:
trazo grueso azul noche (#1E1340), rellenos planos de la paleta y esquinas redondeadas.
Cada ícono es un SVG inline de 48×48; no dependen de los emojis de cada sistema."""

INK, Y, O, V, T, W, RED = "#1E1340", "#FFD23F", "#EF5F1F", "#6647E2", "#19C3A6", "#FFFFFF", "#D91023"
S = 'stroke="%s" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"' % INK

GLYPHS = {
    # regalo: compartir tu código
    "gift": f'''<rect x="8" y="21" width="32" height="20" rx="3" fill="{V}" {S}/>
<rect x="6" y="14" width="36" height="8" rx="2.5" fill="{O}" {S}/>
<rect x="21" y="14" width="6" height="27" fill="{Y}" {S}/>
<path d="M24 14c-2-6-10-8-11-3-.6 3 4 4 11 3zM24 14c2-6 10-8 11-3 .6 3-4 4-11 3z" fill="{Y}" {S}/>''',
    # globo de chat: atender compradores
    "chat": f'''<path d="M7 12a5 5 0 0 1 5-5h24a5 5 0 0 1 5 5v15a5 5 0 0 1-5 5H21l-9 8v-8a5 5 0 0 1-5-5z" fill="{O}" {S}/>
<circle cx="16.5" cy="19.5" r="2.6" fill="{W}"/><circle cx="24" cy="19.5" r="2.6" fill="{W}"/><circle cx="31.5" cy="19.5" r="2.6" fill="{W}"/>''',
    # celular con el pin de Pati: uso la app
    "phone": f'''<rect x="12" y="4" width="24" height="40" rx="6" fill="{T}" {S}/>
<rect x="16.5" y="10" width="15" height="24" rx="2.5" fill="{W}" stroke="{INK}" stroke-width="2.5"/>
<path d="M24 15.5a4.5 4.5 0 0 0-3.2 7.7L24 26.5l3.2-3.3A4.5 4.5 0 0 0 24 15.5z" fill="{O}"/>
<circle cx="24" cy="20" r="1.6" fill="{W}"/><path d="M21 39h6" {S}/>''',
    # foco: tengo una idea
    "idea": f'''<path d="M24 5a13 13 0 0 0-7.5 23.6V33h15v-4.4A13 13 0 0 0 24 5z" fill="{Y}" {S}/>
<path d="M18 38h12M20.5 43h7" {S}/><path d="M19 17a6 6 0 0 1 5-4.5" fill="none" stroke="{W}" stroke-width="3" stroke-linecap="round"/>''',
    # maletín: prensa, alianzas o inversión
    "brief": f'''<path d="M18 15v-4a3 3 0 0 1 3-3h6a3 3 0 0 1 3 3v4" fill="none" {S}/>
<rect x="5" y="15" width="38" height="26" rx="5" fill="{V}" {S}/>
<path d="M5 26h38" {S}/><rect x="20.5" y="22.5" width="7" height="7" rx="2" fill="{Y}" {S}/>''',
    # libro: libro de reclamaciones
    "book": f'''<path d="M11 7h24a4 4 0 0 1 4 4v30H15a4 4 0 0 1-4-4z" fill="{O}" {S}/>
<path d="M11 37a4 4 0 0 1 4-4h24" fill="none" {S}/><path d="M18 15h13M18 21h9" stroke="{W}" stroke-width="3" stroke-linecap="round"/>''',
    # control: videojuegos
    "game": f'''<path d="M15 14h18a10 10 0 0 1 9.7 12.6l-1.8 6.7a5 5 0 0 1-8.7 1.8L29 32H19l-3.2 3.1a5 5 0 0 1-8.7-1.8l-1.8-6.7A10 10 0 0 1 15 14z" fill="{V}" {S}/>
<path d="M15 20v8M11 24h8" stroke="{W}" stroke-width="3" stroke-linecap="round"/>
<circle cx="32" cy="21.5" r="2.4" fill="{Y}"/><circle cx="36" cy="26.5" r="2.4" fill="{Y}"/>''',
    # laptop con </>: programar
    "code": f'''<rect x="6" y="8" width="36" height="25" rx="4" fill="{T}" {S}/>
<path d="M3 38h42l-3 4H6z" fill="{W}" {S}/>
<path d="M19 15l-5 5.5 5 5.5M29 15l5 5.5-5 5.5M26 13.5l-4 14" fill="none" {S}/>''',
    # dos personas: trabajando juntos
    "duo": f'''<circle cx="31" cy="15" r="6.5" fill="{V}" {S}/><path d="M20 41c0-7.5 5-12.5 11-12.5S42 33.5 42 41z" fill="{V}" {S}/>
<circle cx="17" cy="15" r="6.5" fill="{O}" {S}/><path d="M6 41c0-7.5 5-12.5 11-12.5S28 33.5 28 41z" fill="{O}" {S}/>''',
    # megáfono: te lo contamos primero
    "megaphone": f'''<path d="M15 29l3.5 11h5.5l-2.5-11" fill="{W}" {S}/>
<path d="M7 19h8l17-9v28l-17-9H7a3 3 0 0 1-3-3v-4a3 3 0 0 1 3-3z" fill="{Y}" {S}/>
<path d="M38 18a7.5 7.5 0 0 1 0 12" fill="none" {S}/>''',
    # bandera del Perú (no depende del emoji, que en Windows sale como "PE")
    "peru": f'''<rect x="3" y="10" width="42" height="28" rx="5" fill="{RED}"/><rect x="17" y="10" width="14" height="28" fill="{W}"/>
<rect x="3" y="10" width="42" height="28" rx="5" fill="none" {S}/>''',
}

def icon(name, cls="ico"):
    return '<svg class="%s" viewBox="0 0 48 48" aria-hidden="true" focusable="false">%s</svg>' % (cls, GLYPHS[name].replace("\n", ""))
