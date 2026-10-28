'use strict';
// Three languages (owner, 26 Oct 2026): Portuguese first, English, Dutch. A string without Dutch falls back to English.
const LANGS = { pt: 'pt-BR', en: 'en', nl: 'nl' };
const cap = language => language.charAt(0).toUpperCase() + language.slice(1);
function setLanguage(language) {
  if (!LANGS[language]) language = 'pt';
  document.documentElement.lang = LANGS[language];
  document.querySelectorAll('[data-pt][data-en]').forEach(element => {
    element.textContent = element.dataset[language] || element.dataset.en;
  });
  document.querySelectorAll('img[data-alt-pt][data-alt-en]').forEach(element => {
    element.alt = element.dataset['alt' + cap(language)] || element.dataset.altEn;
  });
  document.querySelectorAll('[data-aria-pt][data-aria-en]').forEach(element => {
    element.setAttribute('aria-label', element.dataset['aria' + cap(language)] || element.dataset.ariaEn);
  });
  document.querySelectorAll('[data-language]').forEach(control => {
    control.setAttribute('aria-pressed', String(control.dataset.language === language));
  });
  document.title = document.body.dataset['title' + cap(language)] || document.body.dataset.titleEn
    || { pt: 'IMOBX | Proposta de piloto no Rio', en: 'IMOBX | Proposed Rio housing pilot', nl: 'IMOBX | Voorgestelde woonpilot in Rio' }[language];
  const navigation = document.querySelector('nav');
  if (navigation) navigation.setAttribute('aria-label', { pt: 'Principal', en: 'Main', nl: 'Hoofdmenu' }[language]);
  // Tables: each cell carries its column name so rows can stack on a phone.
  document.querySelectorAll('.guide-table table').forEach(table => {
    const names = Array.from(table.querySelectorAll('thead th')).map(th => th.textContent.trim());
    table.querySelectorAll('tbody tr').forEach(row => {
      Array.from(row.children).forEach((cell, index) => { if (names[index]) cell.setAttribute('data-label', names[index]); });
    });
  });
  try { localStorage.setItem('imobx-language', language); } catch (_) {}
  document.dispatchEvent(new Event('imobx:languagechange'));
}
document.querySelectorAll('[data-language]').forEach(button => {
  button.addEventListener('click', () => setLanguage(button.dataset.language));
});
let preferredLanguage = document.documentElement.lang.startsWith('pt') ? 'pt' : (document.documentElement.lang.startsWith('nl') ? 'nl' : 'en');
try {
  const savedLanguage = localStorage.getItem('imobx-language');
  if (LANGS[savedLanguage]) preferredLanguage = savedLanguage;
} catch (_) {}
setLanguage(preferredLanguage);

function revealAnchor() {
  if (!location.hash) return;
  let target;
  try { target = document.getElementById(decodeURIComponent(location.hash.slice(1))); }
  catch (_) { return; }
  if (!target) return;
  let ancestor = target;
  while (ancestor) {
    if (ancestor.tagName === 'DETAILS') ancestor.open = true;
    ancestor = ancestor.parentElement;
  }
}
window.addEventListener('hashchange', revealAnchor);
revealAnchor();

// Manual galleries keep the source links and native horizontal scrolling usable.
function initCarousels() {
  document.querySelectorAll('[data-carousel]').forEach(gallery => {
    const track = gallery.querySelector('.carousel-track');
    const slides = Array.from(track.querySelectorAll('.carousel-slide'));
    const previous = gallery.querySelector('[data-carousel-prev]');
    const next = gallery.querySelector('[data-carousel-next]');
    const count = gallery.querySelector('[data-carousel-count]');
    const thumbnails = Array.from(gallery.querySelectorAll('[data-carousel-index]'));
    let current = 0;
    let pending = false;
    function update(index) {
      current = Math.max(0, Math.min(slides.length - 1, index));
      count.textContent = `${current + 1} / ${slides.length}`;
      previous.disabled = current === 0;
      next.disabled = current === slides.length - 1;
      thumbnails.forEach((button, i) => {
        button.setAttribute('aria-pressed', String(i === current));
      });
    }
    function go(index) {
      update(index);
      track.scrollTo({left: current * track.clientWidth, behavior: 'auto'});
    }
    previous.addEventListener('click', () => go(current - 1));
    next.addEventListener('click', () => go(current + 1));
    thumbnails.forEach(button => button.addEventListener('click', () => {
      go(Number(button.dataset.carouselIndex));
    }));
    gallery.addEventListener('keydown', event => {
      if (event.altKey || event.ctrlKey || event.metaKey) return;
      if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
        event.preventDefault();
        go(current + (event.key === 'ArrowLeft' ? -1 : 1));
      }
    });
    track.addEventListener('scroll', () => {
      if (pending) return;
      pending = true;
      requestAnimationFrame(() => {
        if (track.clientWidth) update(Math.round(track.scrollLeft / track.clientWidth));
        pending = false;
      });
    }, {passive: true});
    window.addEventListener('resize', () => go(current));
    gallery.querySelectorAll('.carousel-controls, .carousel-thumbs').forEach(control => {
      control.hidden = false;
    });
    update(0);
  });
}

function initImageViewer() {
  const viewer = document.getElementById('image-viewer');
  if (!viewer || typeof viewer.showModal !== 'function') return;
  const image = viewer.querySelector('[data-viewer-image]');
  const caption = viewer.querySelector('figcaption');
  const original = viewer.querySelector('[data-viewer-original]');
  const close = viewer.querySelector('[data-viewer-close]');
  let opener = null;
  function describe() {
    if (!opener) return;
    const source = opener.querySelector('img');
    const figureCaption = opener.closest('figure').querySelector('figcaption');
    image.src = opener.href;
    image.alt = source.alt;
    caption.textContent = figureCaption ? figureCaption.textContent : source.alt;
    original.href = opener.href;
  }
  document.querySelectorAll('a[data-zoom]').forEach(link => {
    link.addEventListener('click', event => {
      if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      opener = link;
      describe();
      viewer.showModal();
      document.documentElement.classList.add('viewer-open');
      close.focus();
    });
  });
  close.addEventListener('click', () => viewer.close());
  viewer.addEventListener('keydown', event => {
    if (event.key !== 'Tab') return;
    const controls = Array.from(viewer.querySelectorAll('a[href], button:not([disabled])'));
    const first = controls[0];
    const last = controls[controls.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });
  viewer.addEventListener('click', event => {
    if (event.target !== viewer) return;
    const bounds = viewer.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right ||
        event.clientY < bounds.top || event.clientY > bounds.bottom) viewer.close();
  });
  viewer.addEventListener('close', () => {
    document.documentElement.classList.remove('viewer-open');
    if (opener && opener.isConnected) opener.focus({preventScroll: true});
  });
  document.addEventListener('imobx:languagechange', () => {
    if (viewer.open) describe();
  });
}
initCarousels();
initImageViewer();

// Phone menu (25 Oct 2026): one button opens the main links as a list; without JavaScript the links stay visible.
(function () {
  var nav = document.querySelector('[data-site-nav]');
  var button = nav && nav.querySelector('.menu-toggle');
  if (!nav || !button) return;
  document.documentElement.classList.add('js-menu');
  button.addEventListener('click', function () {
    var open = nav.classList.toggle('menu-open');
    button.setAttribute('aria-expanded', String(open));
    var lang = (document.documentElement.lang || 'pt').slice(0, 2);
    button.dataset.pt = open ? 'Fechar' : 'Menu'; button.dataset.en = open ? 'Close' : 'Menu'; button.dataset.nl = open ? 'Sluiten' : 'Menu';
    button.textContent = open ? ({ pt: 'Fechar', en: 'Close', nl: 'Sluiten' }[lang] || 'Close') : 'Menu';
  });
  nav.querySelectorAll('.site-links a').forEach(function (link) {
    link.addEventListener('click', function () {
      nav.classList.remove('menu-open'); button.setAttribute('aria-expanded', 'false');
      button.dataset.pt = 'Menu'; button.dataset.en = 'Menu'; button.dataset.nl = 'Menu'; button.textContent = 'Menu';
    });
  });
})();

// Section dropdowns in the main menu (27 Oct 2026): one open at a time; Escape or a click outside closes it.
(function () {
  var toggles = Array.prototype.slice.call(document.querySelectorAll('.site-links .sub-toggle'));
  if (!toggles.length) return;
  function close(except) {
    toggles.forEach(function (t) {
      if (t === except) return;
      t.setAttribute('aria-expanded', 'false');
      var list = document.getElementById(t.getAttribute('aria-controls'));
      if (list) list.hidden = true;
    });
  }
  toggles.forEach(function (toggle) {
    toggle.addEventListener('click', function (event) {
      event.stopPropagation();
      var open = toggle.getAttribute('aria-expanded') !== 'true';
      close(toggle);
      toggle.setAttribute('aria-expanded', String(open));
      var list = document.getElementById(toggle.getAttribute('aria-controls'));
      if (list) list.hidden = !open;
    });
  });
  document.addEventListener('click', function (event) {
    if (!event.target.closest('.site-links .nav-item') || event.target.closest('.site-links .sub a')) close();
  });
  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Escape') return;
    var openToggle = toggles.filter(function (t) { return t.getAttribute('aria-expanded') === 'true'; })[0];
    close();
    if (openToggle && openToggle.offsetParent !== null) openToggle.focus();
  });
})();
