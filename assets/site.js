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
      // a click right after the hover opened the list keeps it open instead of closing it again
      if (!open && Date.now() - (Number(toggle.dataset.hoverAt) || 0) < 800) return;
      close(toggle);
      toggle.setAttribute('aria-expanded', String(open));
      var list = document.getElementById(toggle.getAttribute('aria-controls'));
      if (list) list.hidden = !open;
    });
  });
  document.addEventListener('click', function (event) {
    if (!event.target.closest('.site-links .nav-item') || event.target.closest('.site-links .sub a')) close();
  });
  // Owner, 28 Oct: on a desktop with a mouse, a list also opens on hover and closes shortly after the pointer leaves.
  var hoverable = window.matchMedia('(hover: hover) and (pointer: fine) and (min-width: 701px)');
  toggles.forEach(function (toggle) {
    var item = toggle.closest('.nav-item'), timer = null;
    var list = document.getElementById(toggle.getAttribute('aria-controls'));
    item.addEventListener('mouseenter', function () {
      if (!hoverable.matches || !list) return;
      clearTimeout(timer); close(toggle);
      if (toggle.getAttribute('aria-expanded') !== 'true') toggle.dataset.hoverAt = String(Date.now());
      toggle.setAttribute('aria-expanded', 'true'); list.hidden = false;
    });
    item.addEventListener('mouseleave', function () {
      if (!hoverable.matches || !list) return;
      timer = setTimeout(function () { toggle.setAttribute('aria-expanded', 'false'); list.hidden = true; }, 200);
    });
  });
  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Escape') return;
    var openToggle = toggles.filter(function (t) { return t.getAttribute('aria-expanded') === 'true'; })[0];
    close();
    if (openToggle && openToggle.offsetParent !== null) openToggle.focus();
  });
})();

// Option B: the arrow opens sections taken from the destination page itself.
(function () {
  var band = document.querySelector('.option-b .pillar-band');
  if (!band) return;
  var toggles = Array.from(band.querySelectorAll('.pillar-toggle'));
  var panels = document.querySelector('.option-b .pillar-panels');
  var hoverOpened = false;
  var closeTimer;
  function close(except) {
    clearTimeout(closeTimer);
    if (!except) hoverOpened = false;
    toggles.forEach(function (button) {
      if (button === except) return;
      button.setAttribute('aria-expanded', 'false');
      document.getElementById(button.getAttribute('aria-controls')).hidden = true;
    });
  }
  function populate(panel) {
    if (panel.dataset.loaded) return Promise.resolve();
    return fetch(panel.dataset.source).then(function (response) {
      if (!response.ok) throw new Error('Cannot load page sections');
      return response.text();
    }).then(function (text) {
      var doc = new DOMParser().parseFromString(text, 'text/html');
      // Short navigation labels point to the same sections as the full page headings.
      var shortLabels = {
        'distributed-ledger.html': {
          layers: ['Privacidade e acesso', 'Privacy and access', 'Privacy en toegang'],
          request: ['Reparos e reclamações', 'Repairs and complaints', 'Reparaties en klachten'],
          records: ['Quem pode ler o quê', 'Who can read what', 'Wie wat kan lezen'],
          token: ['Token da IMOBX', 'IMOBX token', 'IMOBX-token'],
          open: ['Opções para a blockchain', 'Blockchain options', 'Blockchainopties']
        },
        'self-compounding.html': {
          use: ['Para que serve', 'Purpose', 'Waarvoor dient het'],
          meaning: ['Como funciona', 'How it works', 'Hoe het werkt'],
          fee: ['Destino da taxa', 'Where fees go', 'Waar vergoedingen naartoe gaan'],
          sale: ['O que o diferencia', 'How it differs', 'Wat het onderscheidt'],
          laws: ['As quatro regras', 'The four rules', 'De vier regels'],
          notice: ['Aviso importante', 'Important notice', 'Belangrijke mededeling']
        },
        'governance.html': {
          now: ['Quem decide agora', 'Who decides now', 'Wie nu beslist'],
          deciding: ['Decisões em aberto', 'Open decisions', 'Open besluiten'],
          'token-rules': ['Decisões sobre o token', 'Token decisions', 'Besluiten over de token'],
          residents: ['Decisões dos moradores', 'Residents’ decisions', 'Besluiten van bewoners'],
          recorded: ['Registro das decisões', 'Decision records', 'Vastgelegde besluiten']
        }
      };
      var list = document.createElement('ul');
      doc.querySelectorAll('main section[id] > h2').forEach(function (heading) {
        var id = heading.parentElement.id;
        if (!id || !heading.dataset.pt || !heading.dataset.en) return;
        var li = document.createElement('li'), link = document.createElement('a');
        link.href = panel.dataset.source + '#' + id;
        var labels = (shortLabels[panel.dataset.source] || {})[id];
        ['pt', 'en', 'nl'].forEach(function (lang, index) { link.dataset[lang] = labels ? labels[index] : (heading.dataset[lang] || heading.dataset.en); });
        link.textContent = link.dataset[(document.documentElement.lang || 'pt').slice(0, 2)] || link.dataset.en;
        li.appendChild(link); list.appendChild(li);
      });
      panel.replaceChildren(list); panel.dataset.loaded = 'true';
    });
  }
  function open(button, fromHover) {
    close(button);
    hoverOpened = !!fromHover;
    var panel = document.getElementById(button.getAttribute('aria-controls'));
    populate(panel).then(function () {
      if (button.getAttribute('aria-expanded') === 'true') panel.hidden = false;
    }).catch(function () { button.setAttribute('aria-expanded', 'false'); });
    button.setAttribute('aria-expanded', 'true');
  }
  toggles.forEach(function (button) {
    var item = button.closest('.pillar-item');
    button.addEventListener('click', function (event) {
      event.stopPropagation();
      if (event.detail && Date.now() - (Number(button.dataset.hoverAt) || 0) < 500) return;
      if (button.getAttribute('aria-expanded') === 'true') close(); else open(button, false);
    });
    button.addEventListener('mouseenter', function () {
      if (matchMedia('(hover: hover) and (pointer: fine)').matches) { button.dataset.hoverAt = String(Date.now()); open(button, true); }
    });
    item.addEventListener('mouseenter', function () {
      if (button.getAttribute('aria-expanded') === 'true') clearTimeout(closeTimer);
    });
    item.addEventListener('mouseleave', function () {
      if (button.getAttribute('aria-expanded') === 'true') scheduleHoverClose();
    });
  });
  function scheduleHoverClose() {
    if (!hoverOpened) return;
    clearTimeout(closeTimer);
    closeTimer = setTimeout(function () {
      var focused = document.activeElement;
      if (focused && focused.matches(':focus-visible') && (band.contains(focused) || panels.contains(focused))) return;
      if (hoverOpened) close();
    }, 200);
  }
  panels.addEventListener('mouseenter', function () { clearTimeout(closeTimer); });
  panels.addEventListener('mouseleave', scheduleHoverClose);
  document.addEventListener('click', function (event) {
    if (!event.target.closest('.pillar-band') && !event.target.closest('.pillar-panel')) close();
  });
  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Escape') return;
    var active = toggles.find(function (button) { return button.getAttribute('aria-expanded') === 'true'; });
    if (active) { event.stopImmediatePropagation(); close(); active.focus(); }
  }, true);
})();
