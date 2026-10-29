'use strict';
// Project development: the method drawing draws itself once; the path fills as the reader scrolls (owner, 28-29 Oct 2026).
(function () {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce) return;  // everything is already shown complete
  document.documentElement.classList.add('js-roadmap');
  const diamond = document.querySelector('.method-diamond');
  if (diamond && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver(entries => entries.forEach(e => {
      if (e.isIntersecting) { diamond.classList.add('is-drawn'); io.disconnect(); }
    }), { threshold: 0.4 });
    io.observe(diamond);
  } else if (diamond) diamond.classList.add('is-drawn');
  const path = document.querySelector('.path'), fill = document.querySelector('.path-fill');
  if (!path || !fill) return;
  let ticking = false;
  const update = () => {
    ticking = false;
    const r = path.getBoundingClientRect(), mid = window.innerHeight * 0.6;
    const p = Math.min(1, Math.max(0, (mid - r.top) / r.height));
    fill.style.setProperty('--path-fill', p.toFixed(3));
  };
  window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
  window.addEventListener('resize', update);
  update();
})();
