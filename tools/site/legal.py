"""Contenido legal de pati.pe: Política de privacidad, Términos y condiciones y
Eliminación de cuenta. Basado en cómo funciona la app (confirmado por el equipo de
la app el 2026-10-20). Si la app cambia (datos, proveedores, créditos), actualizar aquí."""

EFFECTIVE = "31 de octubre de 2026"
EFFECTIVE_ISO = "2026-10-31"
UPDATED = "20 de octubre de 2026"


def sec(id_, title, simple, body):
    return {"id": id_, "title": title, "simple": simple, "body": body}


def render(sections, intro):
    toc = "".join('<li><a href="#%s">%s</a></li>' % (s["id"], s["title"]) for s in sections)
    parts = []
    for i, s in enumerate(sections, 1):
        simple = '<p class="simple"><b>En simple:</b> %s</p>' % s["simple"] if s["simple"] else ""
        parts.append('<section class="legal-sec" id="%s"><h2><span class="n">%d</span>%s</h2>%s%s</section>' % (s["id"], i, s["title"], simple, s["body"]))
    return '''<section class="trust legal">
  <div class="wrap legal-wrap">
    <div class="legal-meta"><span><b>Vigente desde:</b> <time datetime="%s">%s</time></span><span><b>Última actualización:</b> %s</span></div>
    %s
    <nav class="card legal-toc" aria-label="Índice"><b>Índice</b><ol>%s</ol></nav>
    <div class="prose">%s</div>
  </div>
</section>''' % (EFFECTIVE_ISO, EFFECTIVE, UPDATED, intro, toc, "\n".join(parts))


def table(head, rows, label="Tabla"):
    th = "".join("<th>%s</th>" % h for h in head)
    tr = "".join("<tr>%s</tr>" % "".join('<td data-label="%s">%s</td>' % (h, c) for h, c in zip(head, r)) for r in rows)
    return '<div class="table-wrap" role="region" aria-label="%s" tabindex="0"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (label, th, tr)


# ----------------------------------------------------------------- privacidad
def privacy(L, email, wa_link, wa_human):
    contact = '<a href="mailto:%s">%s</a> o por WhatsApp al <a href="%s">%s</a>' % (email, email, wa_link, wa_human)
    S = [
        sec("resumen", "Lo más importante", "",
            '''<ul class="checks">
<li>No vendemos tus datos personales ni mostramos publicidad de terceros.</li>
<li>Usamos tu ubicación solo mientras usas la app, para encontrar vendedores cerca de ti. Nunca en segundo plano.</li>
<li>El vendedor no ve tu número de celular.</li>
<li>Nuestros proveedores están en EE. UU.; por eso tus datos se transfieren a ese país con medidas de protección.</li>
<li>Puedes acceder a tus datos, corregirlos o eliminar tu cuenta cuando quieras.</li>
</ul>'''),
        sec("responsable", "Quién es responsable de tus datos",
            "Pati.pe, la empresa peruana detrás de la app Pati.",
            '''<p>El responsable del tratamiento de tus datos personales es <strong>%s</strong>, con RUC <strong>%s</strong> y domicilio en <strong>%s</strong>, Perú (en adelante, “Pati”).</p>
<p>Esta política aplica a la app <strong>Pati</strong> para Android y iPhone, a nuestro asistente de WhatsApp y al sitio web pati.pe. Puedes escribirnos a %s.</p>
<p>El banco de datos de usuarios de Pati se encuentra en trámite de inscripción en el Registro Nacional de Protección de Datos Personales de la Autoridad Nacional de Protección de Datos Personales (ANPD), conforme a la Ley N.º 29733 y su reglamento.</p>''' % (L["name"], L["ruc"], L["address"], contact)),
        sec("datos", "Qué datos recogemos",
            "Lo necesario para crear tu cuenta, conectar tu pedido con vendedores cercanos y mantener la app segura.",
            table(["Tipo de dato", "Quién", "Para qué"], label="Datos que recogemos", rows=[
                ["Número de celular", "Todos", "Crear tu cuenta y verificarla con un código por SMS."],
                ["Nombre, apellido, distrito, fecha de nacimiento y género", "Todos", "Tu perfil, confirmar que eres mayor de edad y entender a quién sirve Pati."],
                ["Lo que sueles buscar", "Compradores", "Mejorar las sugerencias y el emparejamiento."],
                ["Solicitudes: descripción, categoría y fotos de referencia", "Compradores", "Enviar tu pedido a los vendedores del rubro."],
                ["Ubicación precisa al crear una solicitud", "Compradores", "Encontrar vendedores a unos 3 km y mostrarte la ruta."],
                ["Calificaciones, comentarios y denuncias", "Compradores", "Medir la calidad del servicio y moderar abusos."],
                ["Nombre del negocio, dirección, RUC y descripción", "Vendedores", "Tu perfil de negocio y ubicar tu tienda en el mapa."],
                ["Catálogo: productos, precios y fotos", "Vendedores", "Mostrar lo que vendes y emparejarte con pedidos."],
                ["Ofertas: precio, mensaje y fotos", "Vendedores", "Responder solicitudes de compradores."],
                ["Créditos y código de referido", "Vendedores", "Llevar tu saldo de créditos y premiar invitaciones."],
                ["Token de notificaciones del dispositivo", "Todos", "Avisarte de nuevas solicitudes y ofertas."],
                ["Datos de uso de la app (con un ID interno, sin tu celular)", "Todos", "Saber qué funciona y mejorar la app."],
                ["Reportes técnicos de errores (sin datos personales)", "Todos", "Encontrar y corregir fallas."],
                ["Mensajes con nuestro asistente de WhatsApp", "Compradores", "Registrarte y crear solicitudes sin la app."],
                ["Nombre, correo, celular y mensaje del formulario web", "Quien nos escribe", "Responder tu consulta."],
                ["Nombre, documento, domicilio, teléfono, correo y detalle del reclamo", "Quien presenta un reclamo o queja", "Atender tu reclamo o queja en el Libro de Reclamaciones, como exige la ley."],
            ]) + '''<p><strong>No recogemos</strong> tus contactos, tu micrófono, tu DNI, tu ubicación en segundo plano ni identificadores de publicidad, y no te rastreamos entre otras apps o sitios.</p>'''),
        sec("permisos", "Permisos del celular",
            "Solo pedimos ubicación, fotos y notificaciones, y puedes desactivarlos.",
            '''<ul>
<li><strong>Ubicación (solo mientras usas la app):</strong> para buscar vendedores cercanos y mostrar la ruta.</li>
<li><strong>Fotos:</strong> para adjuntar imágenes a solicitudes, ofertas y productos. Solo subimos las fotos que eliges.</li>
<li><strong>Notificaciones:</strong> para avisarte de solicitudes y ofertas.</li>
</ul>
<p>Puedes retirar estos permisos desde la configuración de tu celular. Sin ubicación, la app no podrá encontrar vendedores cercanos.</p>'''),
        sec("finalidades", "Para qué usamos tus datos",
            "Para que Pati funcione. Las promociones son opcionales y puedes dejarlas cuando quieras.",
            '''<p><strong>Finalidades necesarias</strong> para brindarte el servicio:</p>
<ul>
<li>Crear y administrar tu cuenta, y verificar tu celular.</li>
<li>Enviar tu solicitud a vendedores del rubro cercanos y mostrarte sus ofertas, la dirección de la tienda y la ruta.</li>
<li>Emparejar automáticamente solicitudes con productos y vendedores.</li>
<li>Gestionar créditos y el programa de referidos.</li>
<li>Enviarte notificaciones del servicio.</li>
<li>Gestionar calificaciones y denuncias, moderar contenido, prevenir fraudes y suspender cuentas que incumplan los <a href="/terminos/">Términos</a>.</li>
<li>Atender tus consultas, reclamos y solicitudes de derechos.</li>
<li>Medir el uso de la app y corregir errores.</li>
<li>Cumplir obligaciones legales y requerimientos de autoridades.</li>
</ul>
<p><strong>Finalidad opcional</strong>, solo con tu consentimiento: enviarte novedades y promociones de Pati por notificación, SMS, WhatsApp o correo. Puedes aceptar o no, y retirar tu consentimiento en cualquier momento escribiéndonos; esto no afecta el uso de la app.</p>'''),
        sec("automatizado", "Emparejamiento automático",
            "Un sistema automático decide a qué vendedores llega tu pedido.",
            '''<p>Para decidir qué vendedores reciben una solicitud, analizamos de forma automática su texto, su categoría, la distancia y el catálogo de cada vendedor. Para entender el texto usamos un servicio de inteligencia artificial de Google (Gemini), que recibe el texto de solicitudes y productos, sin tu número de celular. Este proceso no produce decisiones con efectos legales sobre ti; si crees que no funciona bien en tu caso, escríbenos y lo revisará una persona.</p>'''),
        sec("visibilidad", "Qué ve la otra parte",
            "El vendedor ve tu pedido, no tu número. Tú ves la oferta y dónde está la tienda.",
            '''<ul>
<li><strong>El vendedor ve</strong> la descripción, la categoría y las fotos de tu solicitud. <strong>No ve tu número de celular.</strong></li>
<li><strong>El comprador ve</strong> de cada oferta: nombre del negocio, dirección de la tienda, precio, mensaje, fotos, catálogo y la ruta en el mapa.</li>
<li>Si un comprador califica a un vendedor, la calificación queda asociada al perfil del vendedor.</li>
</ul>'''),
        sec("proveedores", "Con quién compartimos datos",
            "Solo con los proveedores que hacen funcionar Pati, y con autoridades cuando la ley lo exige. Nunca los vendemos.",
            '''<p>Trabajamos con estos proveedores, que tratan datos por encargo nuestro y solo para estas finalidades:</p>''' + table(["Proveedor", "País", "Para qué"], label="Proveedores", rows=[
                ["Amazon Web Services", "EE. UU.", "Alojamiento de la app, base de datos y fotos."],
                ["Twilio", "EE. UU.", "SMS de verificación y asistente de WhatsApp."],
                ["Google (Maps)", "EE. UU.", "Mapas, rutas y ubicación de tiendas a partir de su dirección."],
                ["Google (Gemini)", "EE. UU.", "Emparejamiento automático de solicitudes y productos."],
                ["Google (Firebase Cloud Messaging) y Expo", "EE. UU.", "Envío de notificaciones."],
                ["PostHog", "EE. UU.", "Analítica de uso con un ID interno."],
                ["Sentry", "EE. UU.", "Reportes técnicos de errores, sin datos personales."],
                ["Culqi", "Perú", "Procesar pagos, solo cuando se habilite la compra de créditos."],
            ]) + '''<p>También podemos entregar datos a autoridades judiciales o administrativas cuando una norma o una orden nos obligue a hacerlo.</p>'''),
        sec("transferencias", "Transferencia internacional",
            "Tus datos se guardan en servidores de EE. UU.",
            '''<p>Nuestros servidores (Amazon Web Services, región de Virginia) y la mayoría de nuestros proveedores están en Estados Unidos. Al usar Pati, tus datos se transfieren a ese país. Elegimos proveedores que ofrecen garantías de seguridad y confidencialidad adecuadas, conforme a la Ley N.º 29733 y su reglamento.</p>'''),
        sec("conservacion", "Cuánto tiempo guardamos tus datos",
            "Mientras tengas cuenta, y la borramos 30 días después de que la elimines.",
            table(["Dato", "Plazo"], label="Plazos de conservación", rows=[
                ["Datos de tu cuenta y perfil", "Mientras tu cuenta esté activa. Se eliminan dentro de los 30 días siguientes a la eliminación de la cuenta."],
                ["Solicitudes y la ubicación con que se crearon", "12 meses desde su creación."],
                ["Conversación con el asistente de WhatsApp", "24 horas."],
                ["Mensajes del formulario web", "12 meses."],
                ["Hojas del Libro de Reclamaciones", "Al menos 2 años desde su presentación, como exige el reglamento del Libro de Reclamaciones."],
                ["Registros de compras de créditos (cuando se habiliten)", "5 años, por obligaciones tributarias."],
                ["Denuncias y sanciones por fraude", "El tiempo necesario para prevenir nuevos fraudes y atender reclamos o procesos."],
            ]) + "<p>Vencidos estos plazos, eliminamos los datos o los anonimizamos para que ya no te identifiquen.</p>"),
        sec("seguridad", "Cómo protegemos tus datos",
            "Cifrado, acceso restringido y fotos con enlaces temporales.",
            '''<ul>
<li>Toda comunicación con la app y la web viaja cifrada (HTTPS).</li>
<li>La base de datos, los discos y las fotos se almacenan cifrados.</li>
<li>Las fotos solo se muestran con enlaces temporales que vencen en minutos.</li>
<li>Solo el personal autorizado de Pati accede a los datos, y únicamente cuando lo necesita.</li>
</ul>
<p>Ningún sistema es infalible. Si ocurre un incidente que afecte tus datos, te informaremos y comunicaremos a la ANPD conforme a la ley.</p>'''),
        sec("derechos", "Tus derechos",
            "Puedes ver, corregir o borrar tus datos, y oponerte a su uso. Escríbenos.",
            '''<p>Conforme a la Ley N.º 29733 y su reglamento, puedes ejercer en cualquier momento tus derechos de <strong>información, acceso, rectificación, cancelación y oposición</strong>, así como retirar tu consentimiento para finalidades opcionales.</p>
<p>Escríbenos a %s desde el número registrado en tu cuenta, indicando qué derecho quieres ejercer. Para proteger tu cuenta podemos pedirte verificar tu identidad. Responderemos dentro de los plazos que establece la ley.</p>
<p>Si no estás conforme con nuestra respuesta, puedes presentar una reclamación ante la Autoridad Nacional de Protección de Datos Personales del Ministerio de Justicia y Derechos Humanos.</p>''' % contact),
        sec("eliminar", "Eliminar tu cuenta",
            "Puedes eliminarla desde la app o pidiéndonoslo.",
            '''<p>Puedes eliminar tu cuenta desde la app o solicitarlo por correo o WhatsApp. Te explicamos el proceso, qué se borra y en qué plazo en <a href="/eliminar-cuenta/">pati.pe/eliminar-cuenta</a>.</p>'''),
        sec("menores", "Menores de edad",
            "Pati es solo para mayores de 18 años.",
            '''<p>Pati está dirigida a personas mayores de 18 años. No recogemos a sabiendas datos de menores; si detectamos una cuenta de un menor, la eliminaremos.</p>'''),
        sec("web", "Nuestro sitio web",
            "La web no usa cookies de seguimiento.",
            '''<p>En pati.pe no usamos cookies de publicidad ni de seguimiento. Si nos escribes por el formulario de contacto, usamos tus datos solo para responderte y los conservamos según la sección <a href="#conservacion">Cuánto tiempo guardamos tus datos</a>.</p>'''),
        sec("cambios", "Cambios a esta política",
            "Si cambiamos algo importante, te avisamos antes.",
            '''<p>Podemos actualizar esta política cuando cambie la app o la ley. Si el cambio es importante, te avisaremos en la app y en nuestras redes antes de que entre en vigencia. Siempre encontrarás aquí la versión vigente y su fecha.</p>'''),
    ]
    intro = '<p class="legal-intro">En Pati cuidamos tus datos como nos gustaría que cuiden los nuestros. Aquí te contamos, en palabras simples, qué datos usamos, para qué y cuáles son tus derechos.</p>'
    return render(S, intro)


# ----------------------------------------------------------------- términos
def terms(L, email, wa_link, wa_human):
    contact = '<a href="mailto:%s">%s</a> o por WhatsApp al <a href="%s">%s</a>' % (email, email, wa_link, wa_human)
    S = [
        sec("resumen", "Lo más importante", "",
            '''<ul class="checks">
<li>Pati conecta a quien quiere comprar con vendedores cercanos. No vende productos ni cobra las compras.</li>
<li>El precio, el pago, la entrega y la garantía se acuerdan entre comprador y vendedor.</li>
<li>Para el comprador, Pati es gratis. El vendedor usa 1 crédito por oferta y recibe créditos gratis.</li>
<li>Durante el lanzamiento no vendemos créditos: todo es gratis. Si eso cambia, avisamos antes.</li>
<li>Pati es para mayores de 18 años y exige un trato honesto y respetuoso.</li>
</ul>'''),
        sec("aceptacion", "Quiénes somos y aceptación",
            "Al usar Pati aceptas estas reglas.",
            '''<p>Pati es una app y un servicio de <strong>%s</strong> (RUC %s, domicilio en %s, Perú). Estos Términos y condiciones regulan el uso de la app Pati, del asistente de WhatsApp y del sitio pati.pe.</p>
<p>Al crear una cuenta o usar el servicio aceptas estos Términos y nuestra <a href="/privacidad/">Política de privacidad</a>. Si no estás de acuerdo, no uses Pati.</p>''' % (L["name"], L["ruc"], L["address"])),
        sec("requisitos", "Quién puede usar Pati",
            "Mayores de 18 años con datos verdaderos. Los vendedores, con un negocio real.",
            '''<ul>
<li>Debes tener 18 años o más.</li>
<li>Los datos que registras deben ser verdaderos y estar actualizados. Cada persona puede tener una sola cuenta.</li>
<li>Si te registras como vendedor, declaras que tienes un negocio real y que el RUC que registras te pertenece.</li>
<li>Eres responsable de lo que se haga desde tu cuenta y de mantener el acceso a tu celular.</li>
</ul>'''),
        sec("servicio", "Cómo funciona el servicio",
            "Publicas un pedido, te llegan ofertas de vendedores cercanos y tú eliges.",
            '''<ol>
<li>El comprador publica una solicitud desde la app o desde nuestro asistente de WhatsApp.</li>
<li>Pati la envía, de forma automática, a vendedores del rubro cercanos a su ubicación, que tienen un tiempo limitado para responder.</li>
<li>Los vendedores interesados envían su oferta y el comprador ve el precio, la tienda y la ruta.</li>
<li>El comprador decide si acepta alguna oferta y la compra se concreta directamente con el vendedor.</li>
</ol>
<p>Pati no garantiza que toda solicitud reciba ofertas, ni el resultado de una compra.</p>'''),
        sec("intermediario", "Pati es un intermediario",
            "La compra es entre comprador y vendedor. Pati no cobra ni recibe esos pagos.",
            '''<p>Pati es una plataforma que pone en contacto a compradores y vendedores. <strong>No vende los productos, no es parte de la compraventa y no cobra ni recibe pagos por las compras.</strong> Si alguien te pide pagar “a Pati” por una compra, es un fraude: denúncialo.</p>
<p>El vendedor es el único responsable de sus ofertas: precio, disponibilidad, calidad, entrega, comprobantes de pago y garantías, y de cumplir el Código de Protección y Defensa del Consumidor y demás normas aplicables a su negocio.</p>'''),
        sec("creditos", "Créditos para vendedores",
            "1 crédito = 1 oferta. Empiezas con 20 y recibes 15 cada mes, gratis.",
            '''<ul>
<li>Enviar una oferta a una solicitud usa <strong>1 crédito</strong>.</li>
<li>Al registrarte como vendedor recibes <strong>20 créditos de bienvenida</strong>, una sola vez.</li>
<li>Cada mes calendario recibes <strong>15 créditos gratis</strong>. Los créditos gratis mensuales no se acumulan de un mes a otro.</li>
<li><strong>Referidos:</strong> si un vendedor nuevo se registra con tu código, recibe 10 créditos al completar su catálogo, y tú recibes 10 cuando envía su primera oferta.</li>
<li>Los créditos no son dinero: no se pueden canjear por dinero, transferir ni vender.</li>
<li>Podemos anular créditos obtenidos con trampa, por ejemplo con cuentas falsas para aprovechar referidos.</li>
</ul>
<p><strong>Compra de créditos.</strong> Durante el lanzamiento Pati no vende créditos: el servicio es gratuito. Si más adelante habilitamos la compra de paquetes, te informaremos los precios, el medio de pago y sus condiciones antes de que esté disponible y actualizaremos estos Términos. Los créditos que compres no vencerán.</p>'''),
        sec("reglas", "Lo que no está permitido",
            "Nada ilegal, falso ni abusivo.",
            '''<p>En Pati no está permitido:</p>
<ul>
<li>Pedir u ofrecer productos ilegales o cuya venta esté restringida: drogas, armas, municiones, medicamentos que requieren receta, productos falsificados o robados, fauna silvestre, documentos o datos personales de terceros, entre otros.</li>
<li>Publicar ofertas falsas, cambiar el precio ofrecido de forma abusiva o no responder después de comprometerse.</li>
<li>Acosar, amenazar, discriminar o insultar a otras personas.</li>
<li>Publicar contenido sexual, violento o que infrinja derechos de terceros.</li>
<li>Suplantar a otra persona o negocio, o crear cuentas falsas o múltiples.</li>
<li>Usar Pati para enviar spam o publicidad no relacionada con una solicitud.</li>
<li>Copiar datos de la app con programas automáticos o intentar vulnerar su seguridad.</li>
</ul>'''),
        sec("calificaciones", "Calificaciones y denuncias",
            "Las calificaciones y denuncias ayudan a mantener Pati confiable.",
            '''<p>Al cerrar una solicitud, el comprador puede calificar al vendedor de 1 a 5 y dejar un comentario honesto. También puede denunciar una oferta o un vendedor por oferta falsa, cambio de precio, falta de respuesta, sospecha de fraude, robo o pérdida, acoso u otro motivo.</p>
<p>Revisamos las denuncias y podemos retirar contenido, advertir o suspender cuentas. Las calificaciones o denuncias falsas también incumplen estos Términos.</p>'''),
        sec("suspension", "Suspensión y cierre de cuenta",
            "Podemos suspender cuentas que incumplan; tú puedes cerrar la tuya cuando quieras.",
            '''<p>Podemos suspender o cerrar una cuenta que incumpla estos Términos, ponga en riesgo a otros usuarios o lo exija una autoridad. Cuando sea posible te explicaremos el motivo, y puedes escribirnos si crees que es un error.</p>
<p>Puedes dejar de usar Pati y <a href="/eliminar-cuenta/">eliminar tu cuenta</a> en cualquier momento. Al eliminarla pierdes los créditos que tengas.</p>'''),
        sec("contenido", "Tu contenido y nuestra marca",
            "Tus fotos y textos siguen siendo tuyos; nos permites mostrarlos en Pati.",
            '''<p>Conservas los derechos sobre las fotos y textos que publicas. Nos das permiso, gratuito y mientras tengas el contenido publicado, para alojarlo y mostrarlo dentro de Pati con el fin de prestar el servicio. Declaras que tienes derecho a publicar ese contenido.</p>
<p>La marca Pati, su logo, diseño y software pertenecen a %s. No puedes usarlos sin nuestra autorización.</p>''' % L["name"]),
        sec("disponibilidad", "Disponibilidad y cambios del servicio",
            "Pati está en sus primeras versiones: puede tener fallas y va a cambiar.",
            '''<p>Pati es un servicio nuevo que mejoramos constantemente con la comunidad. Puede tener interrupciones o errores, y podemos agregar, cambiar o retirar funciones. Si un cambio afecta de forma importante cómo usas Pati, te avisaremos antes.</p>'''),
        sec("responsabilidad", "Responsabilidad",
            "Respondemos por nuestro servicio, no por las compras entre usuarios.",
            '''<p>Pati responde por la prestación de su propio servicio conforme a la ley. Como no es parte de la compraventa, no responde por los productos, precios, entregas, pagos o garantías acordados entre comprador y vendedor, ni por la conducta de los usuarios, sin perjuicio de que atendamos tus denuncias y colaboremos con las autoridades.</p>
<p>Nada en estos Términos limita los derechos que te reconoce el Código de Protección y Defensa del Consumidor ni otras normas que no pueden ser renunciadas.</p>'''),
        sec("cambios", "Cambios a estos Términos",
            "Si cambiamos algo importante, te avisamos antes.",
            '''<p>Podemos actualizar estos Términos. Si el cambio es importante, te avisaremos en la app y en nuestras redes antes de que entre en vigencia. Si sigues usando Pati después de esa fecha, aceptas la nueva versión.</p>'''),
        sec("ley", "Ley aplicable y reclamos",
            "Aplica la ley peruana. Puedes reclamar en nuestro Libro de Reclamaciones.",
            '''<p>Estos Términos se rigen por las leyes de la República del Perú. Puedes presentar reclamos o quejas en nuestro <a href="/libro-de-reclamaciones/">Libro de Reclamaciones</a> y acudir a Indecopi. Cualquier controversia se someterá a los jueces y tribunales de Lima, sin perjuicio de los derechos que la ley reconoce a los consumidores.</p>'''),
        sec("contacto", "Contacto",
            "",
            '''<p>Escríbenos a %s. Atendemos de lunes a viernes, de 8 a. m. a 8 p. m.</p>''' % contact),
    ]
    intro = '<p class="legal-intro">Estas son las reglas para usar Pati. Las escribimos para que se entiendan: cada sección empieza con un resumen “en simple”.</p>'
    return render(S, intro)


# ----------------------------------------------------------------- eliminar cuenta
def delete_account(email, wa_link, wa_human):
    return '''<section class="trust legal">
  <div class="wrap legal-wrap prose">
    <p class="legal-intro">Puedes eliminar tu cuenta de Pati cuando quieras. Así funciona.</p>
    <div class="steps-legal">
      <article class="card"><h2>Desde la app</h2><ol><li>Abre Pati e inicia sesión.</li><li>Entra a tu <strong>Perfil</strong>.</li><li>Elige <strong>Eliminar cuenta</strong> y confirma.</li></ol></article>
      <article class="card"><h2>Sin la app</h2><p>Escríbenos desde el número de celular registrado en tu cuenta y pide la eliminación:</p>
        <a class="btn wa" href="%s">[[wa]]Pedir por WhatsApp</a>
        <p>o al correo <a href="mailto:%s?subject=Eliminar%%20mi%%20cuenta%%20de%%20Pati">%s</a> indicando tu número de celular. Para proteger tu cuenta, podemos pedirte confirmar que eres el titular.</p></article>
    </div>
    <h2>Qué se elimina</h2>
    <ul><li>Tu cuenta y perfil: nombre, celular, distrito, fecha de nacimiento y género.</li><li>Si eres vendedor: tu perfil de negocio, catálogo, fotos, ofertas y créditos.</li><li>Tus solicitudes, sus fotos y la ubicación con que se crearon.</li><li>El token de notificaciones de tu dispositivo.</li></ul>
    <h2>Plazo</h2>
    <p>Eliminamos tus datos dentro de los <strong>30 días</strong> siguientes a tu solicitud. Podemos conservar por más tiempo solo lo que la ley nos obliga a guardar (por ejemplo, registros tributarios) o lo necesario para atender denuncias de fraude, y únicamente para ese fin.</p>
    <p>Más detalles en nuestra <a href="/privacidad/">Política de privacidad</a>.</p>
  </div>
</section>''' % (wa_link, email, email)


# ----------------------------------------------------------------- libro de reclamaciones
def claims_book(L, email, mode, endpoint, esc):
    """Hoja de Reclamación virtual según el Anexo I del Reglamento del Libro de Reclamaciones
    (DS 011-2011-PCM y modificatorias). mode="live" envía al backend (correlativo + copia por
    correo); mode="email" genera la hoja en pantalla para enviarla por correo o WhatsApp."""
    return '''<section class="trust legal">
  <div class="wrap legal-wrap">
    <div class="card claim-head">
      <div><span class="kicker-dark">Hoja de Reclamación virtual</span><h2>Libro de Reclamaciones</h2></div>
      <div class="legal-data">
        <span><strong>Proveedor:</strong> {name}</span><span><strong>RUC:</strong> {ruc}</span><span><strong>Domicilio:</strong> {addr}</span>
        <span><strong>Fecha:</strong> <span data-today>hoy</span></span>
      </div>
    </div>

    <div class="claim-defs">
      <p><strong>Reclamo:</strong> disconformidad relacionada con los productos o servicios.</p>
      <p><strong>Queja:</strong> disconformidad no relacionada con los productos o servicios, o malestar o descontento respecto a la atención al público.</p>
    </div>

    <form class="card claim-form" data-claim data-mode="{mode}" data-endpoint="{endpoint}" data-mailto="{email}" novalidate>
      <fieldset>
        <legend><span class="n">1</span>Identificación del consumidor reclamante</legend>
        <label>Nombres y apellidos<input name="name" autocomplete="name" required maxlength="120"></label>
        <div class="row2">
          <label>Tipo de documento<select name="docType" required><option>DNI</option><option value="CE">Carné de extranjería</option><option>Pasaporte</option></select></label>
          <label>Número de documento<input name="docNumber" required maxlength="12" autocapitalize="characters" inputmode="text"></label>
        </div>
        <label>Domicilio<input name="address" autocomplete="street-address" required maxlength="200"></label>
        <div class="row2">
          <label>Teléfono<input name="phone" type="tel" inputmode="tel" autocomplete="tel" required maxlength="20"></label>
          <label>Correo electrónico<input name="email" type="email" autocomplete="email" autocapitalize="none" required maxlength="160"></label>
        </div>
        <label class="check"><input name="isMinor" type="checkbox" id="minor"><span>Soy menor de edad</span></label>
        <div class="guardian">
          <p class="hint">Si eres menor de edad, completa los datos de tu padre, madre o apoderado.</p>
          <div class="row2">
            <label>Nombre del padre, madre o apoderado<input name="guardianName" maxlength="120"></label>
            <label>Su documento de identidad<input name="guardianDoc" maxlength="12" autocapitalize="characters"></label>
          </div>
        </div>
      </fieldset>

      <fieldset>
        <legend><span class="n">2</span>Identificación del bien contratado</legend>
        <div class="radios" role="radiogroup" aria-label="Tipo de bien contratado">
          <label class="radio"><input type="radio" name="itemType" value="producto" required><span>Producto</span></label>
          <label class="radio"><input type="radio" name="itemType" value="servicio" checked><span>Servicio</span></label>
        </div>
        <label>Monto reclamado (S/) <small>(opcional)</small><input name="amount" inputmode="decimal" maxlength="12" placeholder="0.00"></label>
        <label>Descripción<textarea name="itemDescription" rows="2" required maxlength="1000" placeholder="Por ejemplo: uso de la app Pati, oferta de un vendedor, atención por WhatsApp"></textarea></label>
      </fieldset>

      <fieldset>
        <legend><span class="n">3</span>Detalle de la reclamación y pedido del consumidor</legend>
        <div class="radios" role="radiogroup" aria-label="Tipo de reclamación">
          <label class="radio"><input type="radio" name="claimType" value="reclamo" required checked><span>Reclamo</span></label>
          <label class="radio"><input type="radio" name="claimType" value="queja"><span>Queja</span></label>
        </div>
        <label>Detalle<textarea name="detail" rows="5" required maxlength="3000"></textarea></label>
        <label>Pedido<textarea name="request" rows="3" required maxlength="1500" placeholder="¿Qué solicitas a Pati?"></textarea></label>
      </fieldset>

      <label class="hp" aria-hidden="true">No llenar<input name="website" tabindex="-1" autocomplete="off"></label>
      <label class="check"><input name="accept" type="checkbox" required><span>Declaro que la información es verdadera y acepto el contenido de esta hoja. Pati tratará mis datos para atender mi reclamo, según su <a href="/privacidad/">política de privacidad</a>.</span></label>
      <button class="btn" type="submit">Enviar hoja de reclamación</button>
      <p class="form-status" role="status" aria-live="polite"></p>
    </form>

    <div class="claim-result card" hidden tabindex="-1">
      <span class="kicker-dark">Hoja de Reclamación</span>
      <h2>N.º <span data-number></span></h2>
      <p class="claim-next"></p>
      <div class="claim-actions"></div>
      <pre class="claim-copy"></pre>
    </div>

    <div class="claim-notes">
      <p>La formulación del reclamo no impide acudir a otras vías de solución de controversias ni es requisito previo para interponer una denuncia ante el Indecopi.</p>
      <p>Pati deberá dar respuesta al reclamo o queja en un plazo no mayor a <strong>quince (15) días hábiles</strong> improrrogables.</p>
    </div>
  </div>
</section>'''.format(name=L["name"], ruc=L["ruc"], addr=L["address"], mode=mode, endpoint=esc(endpoint), email=email)
