// Única JS del sitio. Sin JS todo se ve completo (la clase html.js la pone un script inline en <head>).
// 1) El chat de ejemplo del hero se anima la primera vez que entra en pantalla.
// 2) En la home, el header fijo aparece cuando el logo grande del hero sale de pantalla.
// 3) Entradas suaves de títulos y tarjetas al hacer scroll.
// 4) Cierra el menú al elegir un enlace. 5) Envía el formulario de contacto (simulado, endpoint o mailto).
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
        var body = 'Nombre: ' + d.name + '\nCorreo: ' + d.email + '\nCelular: ' + d.phone + '\n\n' + d.message;
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
// 6) Libro de Reclamaciones: valida la Hoja de Reclamación y la registra.
//    data-mode="live": POST al backend → número correlativo oficial y copia por correo.
//    data-mode="email": arma la hoja en pantalla para enviarla por correo o WhatsApp.
(function () {
  var form = document.querySelector('form[data-claim]');
  if (!form) return;
  var today = new Date();
  var fmtDate = today.toLocaleDateString('es-PE', { day: '2-digit', month: '2-digit', year: 'numeric' });
  [].forEach.call(document.querySelectorAll('[data-today]'), function (el) { el.textContent = fmtDate; });

  var status = form.querySelector('.form-status');
  var result = document.querySelector('.claim-result');
  var say = function (msg, kind) { status.textContent = msg; status.className = 'form-status ' + (kind || ''); };
  var DOC = { DNI: /^\d{8}$/, CE: /^[A-Za-z0-9]{9,12}$/, Pasaporte: /^[A-Za-z0-9]{6,12}$/ };
  var val = function (n) { var el = form.elements[n]; return el ? (el.value || '').trim() : ''; };
  var radio = function (n) { var el = form.querySelector('input[name="' + n + '"]:checked'); return el ? el.value : ''; };

  function data() {
    return {
      name: val('name'), docType: val('docType'), docNumber: val('docNumber').toUpperCase(), address: val('address'),
      phone: val('phone'), email: val('email').toLowerCase(), isMinor: form.elements.isMinor.checked,
      guardianName: val('guardianName'), guardianDoc: val('guardianDoc').toUpperCase(),
      itemType: radio('itemType'), amount: val('amount').replace(',', '.'), itemDescription: val('itemDescription'),
      claimType: radio('claimType'), detail: val('detail'), request: val('request'),
      accept: form.elements.accept.checked, website: val('website')
    };
  }

  function check(d) {
    var bad = [];
    var need = function (name, ok) { if (!ok) bad.push(name); };
    need('name', d.name.length >= 3);
    need('docNumber', (DOC[d.docType] || /x^/).test(d.docNumber));
    need('address', d.address.length >= 5);
    need('phone', /^[+\d\s()-]{6,20}$/.test(d.phone));
    need('email', /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(d.email));
    if (d.isMinor) { need('guardianName', d.guardianName.length >= 3); need('guardianDoc', /^[A-Z0-9]{6,12}$/.test(d.guardianDoc)); }
    need('amount', !d.amount || /^\d{1,9}(\.\d{1,2})?$/.test(d.amount));
    need('itemDescription', d.itemDescription.length >= 3);
    need('detail', d.detail.length >= 10);
    need('request', d.request.length >= 5);
    need('accept', d.accept);
    [].forEach.call(form.querySelectorAll('[name]'), function (el) { el.setAttribute('aria-invalid', bad.indexOf(el.name) > -1 ? 'true' : 'false'); });
    return bad;
  }

  function text(d, number, when) {
    var L = [
      'HOJA DE RECLAMACIÓN N.º ' + number, 'Fecha: ' + when, '',
      'Proveedor: Pati.pe · RUC 20616635485 · Los Totorales 163, San Miguel', '',
      '1. Consumidor reclamante', 'Nombre: ' + d.name, d.docType + ': ' + d.docNumber, 'Domicilio: ' + d.address,
      'Teléfono: ' + d.phone + ' · Correo: ' + d.email
    ];
    if (d.isMinor) L.push('Menor de edad. Padre, madre o apoderado: ' + d.guardianName + ' (doc. ' + d.guardianDoc + ')');
    L.push('', '2. Identificación del bien contratado', 'Tipo: ' + d.itemType + ' · Monto reclamado: ' + (d.amount ? 'S/ ' + d.amount : 'no indicado'),
      'Descripción: ' + d.itemDescription, '', '3. Detalle de la reclamación y pedido del consumidor',
      'Tipo: ' + (d.claimType === 'reclamo' ? 'Reclamo (disconformidad con el producto o servicio)' : 'Queja (disconformidad con la atención)'),
      'Detalle: ' + d.detail, 'Pedido: ' + d.request, '',
      'Pati dará respuesta en un plazo no mayor a 15 días hábiles improrrogables.',
      'La formulación del reclamo no impide acudir a otras vías de solución de controversias ni es requisito previo para interponer una denuncia ante el Indecopi.');
    return L.join('\n');
  }

  function show(number, next, actions, copy) {
    result.querySelector('[data-number]').textContent = number;
    result.querySelector('.claim-next').innerHTML = next;
    result.querySelector('.claim-actions').innerHTML = actions;
    result.querySelector('.claim-copy').textContent = copy;
    form.hidden = true;
    result.hidden = false;
    result.scrollIntoView({ block: 'start' });
    result.focus({ preventScroll: true });
    var print = result.querySelector('[data-print]');
    if (print) print.addEventListener('click', function () { window.print(); });
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var d = data();
    if (d.website) return;
    var bad = check(d);
    if (bad.length) { say('Revisa los campos marcados.', 'err'); var f = form.elements[bad[0]]; if (f && f.focus) f.focus(); return; }
    delete d.website;
    var when = today.toLocaleString('es-PE');
    var btn = form.querySelector('button[type=submit]');

    if (form.getAttribute('data-mode') === 'live' && form.getAttribute('data-endpoint')) {
      btn.disabled = true; say('Registrando tu hoja…');
      fetch(form.getAttribute('data-endpoint'), { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(d) })
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then(function (j) {
          show(j.number,
            'Registramos tu ' + d.claimType + '. ' + (j.emailed ? 'Te enviamos una copia a <b>' + d.email.replace(/[<>&"]/g, '') + '</b>. ' : '') + 'Te responderemos en un plazo no mayor a 15 días hábiles.',
            '<button class="btn light" type="button" data-print>Imprimir o guardar</button>',
            text(d, j.number, new Date(j.createdAt).toLocaleString('es-PE')));
        })
        .catch(function () { btn.disabled = false; say('No pudimos registrar tu hoja. Inténtalo de nuevo o escríbenos a ' + form.getAttribute('data-mailto') + '.', 'err'); });
      return;
    }

    // Modo correo: código provisional; la hoja queda registrada cuando nos llega.
    var p = function (n) { return String(n).padStart(2, '0'); };
    var code = 'LR-' + today.getFullYear() + p(today.getMonth() + 1) + p(today.getDate()) + '-' + p(today.getHours()) + p(today.getMinutes()) + p(today.getSeconds());
    var body = text(d, code, when);
    var subject = 'Hoja de Reclamación ' + code + ' (' + d.claimType + ')';
    var mail = 'mailto:' + form.getAttribute('data-mailto') + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    var wa = 'https://wa.me/51924519233?text=' + encodeURIComponent(body);
    show(code,
      'Tu hoja está lista. <b>Para registrarla, envíala a Pati</b> por correo (recomendado: te queda una copia en tu correo) o por WhatsApp. Te responderemos en un plazo no mayor a 15 días hábiles.',
      '<a class="btn" href="' + mail + '" data-send="email">Enviar por correo</a><a class="btn wa" href="' + wa + '" data-send="whatsapp">Enviar por WhatsApp</a><button class="btn light" type="button" data-print>Imprimir o guardar</button>',
      body);
  });
})();
