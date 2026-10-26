'use strict';
// Homepage: the one authored moment. The IMOBX bucket fills and spills into the next home when it comes into view.
(function () {
  var w = document.querySelector('.way-imobx');
  if (!w || !('IntersectionObserver' in window)) return;
  document.documentElement.classList.add('js-fill');
  new IntersectionObserver(function (entries, o) {
    entries.forEach(function (x) { if (x.isIntersecting) { w.classList.add('is-filled'); o.disconnect(); } });
  }, { threshold: 0.4 }).observe(w);
})();
