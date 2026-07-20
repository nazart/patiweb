(function () {
  var links = document.querySelectorAll('.main-nav a[data-section]');
  if (!links.length) return;
  var sections = Array.prototype.map.call(links, function (a) {
    return document.getElementById(a.dataset.section);
  });

  function update() {
    var probeY = 140;
    var current = sections[0];
    for (var i = 0; i < sections.length; i++) {
      var el = sections[i];
      if (el && el.getBoundingClientRect().top <= probeY) current = el;
    }
    links.forEach(function (a) {
      a.classList.toggle('active', current && a.dataset.section === current.id);
    });
  }

  window.addEventListener('scroll', update, { passive: true });
  update();
})();
