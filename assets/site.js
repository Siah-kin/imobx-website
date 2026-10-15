'use strict';
function setLanguage(language) {
  document.documentElement.lang = language === 'pt' ? 'pt-BR' : 'en';
  document.querySelectorAll('[data-pt][data-en]').forEach(element => {
    element.textContent = element.dataset[language];
  });
  document.querySelectorAll('img[data-alt-pt][data-alt-en]').forEach(element => {
    element.alt = language === 'pt' ? element.dataset.altPt : element.dataset.altEn;
  });
  document.querySelectorAll('[data-aria-pt][data-aria-en]').forEach(element => {
    element.setAttribute('aria-label', language === 'pt' ? element.dataset.ariaPt : element.dataset.ariaEn);
  });
  document.querySelectorAll('[data-language]').forEach(control => {
    control.setAttribute('aria-pressed', String(control.dataset.language === language));
  });
  const titleKey = language === 'pt' ? 'titlePt' : 'titleEn';
  document.title = document.body.dataset[titleKey] || (language === 'pt'
    ? 'IMOBX | Proposta de piloto no Rio' : 'IMOBX | Proposed Rio housing pilot');
  const navigation = document.querySelector('nav');
  if (navigation) navigation.setAttribute('aria-label', language === 'pt' ? 'Principal' : 'Main');
  try { localStorage.setItem('imobx-language', language); } catch (_) {}
  document.dispatchEvent(new Event('imobx:languagechange'));
}
document.querySelectorAll('[data-language]').forEach(button => {
  button.addEventListener('click', () => setLanguage(button.dataset.language));
});
let preferredLanguage = document.documentElement.lang.startsWith('pt') ? 'pt' : 'en';
try {
  const savedLanguage = localStorage.getItem('imobx-language');
  if (savedLanguage === 'pt' || savedLanguage === 'en') preferredLanguage = savedLanguage;
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
