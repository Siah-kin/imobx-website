'use strict';
// The iceberg's waterline draws once and the motives rise into view (owner, 29 Oct 2026). Reduced motion: shown complete.
(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) return;
  const berg = document.querySelector('.iceberg');
  if (!berg) return;
  document.documentElement.classList.add('js-ideas');
  const io = new IntersectionObserver(entries => entries.forEach(e => {
    if (e.isIntersecting) { berg.classList.add('is-in'); io.disconnect(); }
  }), { threshold: 0.3 });
  io.observe(berg);
})();
