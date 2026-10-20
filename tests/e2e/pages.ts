// Páginas públicas del sitio (mantener en sync con tools/site/build.py y sitemap.xml).
export const PAGES = [
  { path: "/", h1: /Pide una vez/ },
  { path: "/nosotros/", h1: /Somos Nazart/ },
  { path: "/contacto/", h1: /Hablemos/ },
  { path: "/novedades/", h1: /Novedades/ },
  { path: "/privacidad/", h1: /Política de privacidad/ },
  { path: "/terminos/", h1: /Términos y condiciones/ },
  { path: "/libro-de-reclamaciones/", h1: /Libro de Reclamaciones/ },
  { path: "/eliminar-cuenta/", h1: /Eliminar tu cuenta/ },
];

// Textos que no deben volver a aparecer (decisiones de contenido del lanzamiento).
export const FORBIDDEN = [/todo el per[uú]/i, /lanzamiento nacional/i, /gamarra/i, /51987654321/, /hola@pati\.com/i, /conversas antes/i, /interactúas con/i];

export const WHATSAPP = "51924519233";
