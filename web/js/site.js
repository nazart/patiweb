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
