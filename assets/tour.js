'use strict';
// The page remains the source of truth and the fallback when dialogs cannot open.
(function () {
  const opener = document.querySelector('[data-tour-open]');
  if (!opener || typeof HTMLDialogElement === 'undefined' ||
      typeof HTMLDialogElement.prototype.showModal !== 'function') return;

  const labels = {
    pt: { close: 'Fechar', back: 'Voltar', next: 'Próximo', finish: 'Concluir', scroll: 'Role para ler mais ↓', step: (n, total) => `Etapa ${n} de ${total}` },
    en: { close: 'Close', back: 'Back', next: 'Next', finish: 'Finish', scroll: 'Scroll to read more ↓', step: (n, total) => `Step ${n} of ${total}` },
    nl: { close: 'Sluiten', back: 'Terug', next: 'Volgende', finish: 'Afronden', scroll: 'Scroll om verder te lezen ↓', step: (n, total) => `Stap ${n} van ${total}` }
  };
  const language = () => {
    const code = document.documentElement.lang.slice(0, 2);
    return labels[code] ? code : 'pt';
  };
  let dialog = null;
  let steps = [];
  let current = 0;
  let loading = false;
  const returnKey = '__imobxTourReturnCard';

  function updateScrollHint() {
    if (!dialog || !dialog.open) return;
    const content = dialog.querySelector('[data-tour-content]');
    const hint = dialog.querySelector('[data-tour-scroll-hint]');
    hint.hidden = content.scrollHeight - content.clientHeight - content.scrollTop <= 2;
  }

  function update() {
    const code = language();
    const words = labels[code];
    steps.forEach((step, index) => { step.hidden = index !== current; });
    dialog.querySelectorAll('[data-pt][data-en]').forEach(node => {
      node.textContent = node.dataset[code] || node.dataset.en;
    });
    dialog.querySelector('[data-tour-progress]').textContent = words.step(current + 1, steps.length);
    dialog.querySelector('[data-tour-close]').textContent = words.close;
    dialog.querySelector('[data-tour-back]').textContent = words.back;
    dialog.querySelector('[data-tour-back]').hidden = current === 0;
    dialog.querySelector('[data-tour-next]').classList.toggle('is-last', current === steps.length - 1);
    dialog.querySelector('[data-tour-next]').textContent = current === steps.length - 1 ? words.finish : words.next;
    dialog.querySelector('[data-tour-scroll-hint]').textContent = words.scroll;
    const heading = steps[current].querySelector('h2, h3');
    if (heading) {
      heading.id = 'tour-dialog-heading-' + (current + 1);
      heading.tabIndex = -1;
      dialog.setAttribute('aria-labelledby', heading.id);
    }
    requestAnimationFrame(updateScrollHint);
  }

  function moveTo(index) {
    current = Math.max(0, Math.min(steps.length - 1, index));
    update();
    const heading = steps[current].querySelector('h2, h3');
    if (heading) heading.focus();
    dialog.querySelector('[data-tour-content]').scrollTop = 0;
  }

  function makeDialog(sourceSteps, related) {
    const box = document.createElement('dialog');
    box.className = 'tour-dialog';
    box.innerHTML = '<div class="tour-dialog-shell"><div class="tour-dialog-top"><p class="tour-progress" data-tour-progress aria-live="polite"></p><button type="button" class="tour-close" data-tour-close></button></div><div class="tour-dialog-content" data-tour-content></div><p class="tour-scroll-hint" data-tour-scroll-hint hidden></p><div class="tour-dialog-actions"><button type="button" class="tour-back" data-tour-back></button><button type="button" class="tour-next" data-tour-next></button></div></div>';
    const content = box.querySelector('[data-tour-content]');
    content.addEventListener('scroll', updateScrollHint, { passive: true });
    sourceSteps.forEach(section => {
      const copy = document.importNode(section, true);
      // Standalone page anchors must not duplicate ids in the current document.
      copy.removeAttribute('id');
      copy.querySelectorAll('[id]').forEach(node => node.removeAttribute('id'));
      content.appendChild(copy);
    });
    steps = Array.from(content.children);
    if (related) {
      const paragraph = document.createElement('p');
      const link = document.createElement('a');
      link.href = 'tour.html#tour-next';
      link.dataset.pt = 'Mais caminhos para conhecer a IMOBX';
      link.dataset.en = 'More ways to explore IMOBX';
      link.dataset.nl = 'Meer manieren om IMOBX te ontdekken';
      link.textContent = link.dataset.pt;
      paragraph.appendChild(link);
      steps[steps.length - 1].appendChild(paragraph);
    }
    box.querySelector('[data-tour-close]').addEventListener('click', () => box.close());
    box.querySelector('[data-tour-back]').addEventListener('click', () => moveTo(current - 1));
    box.querySelector('[data-tour-next]').addEventListener('click', () => {
      if (current === steps.length - 1) box.close();
      else moveTo(current + 1);
    });
    content.addEventListener('click', event => {
      const link = event.target.closest('a[href]');
      if (!link || event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey ||
          event.shiftKey || event.altKey || link.hasAttribute('download') ||
          (link.target && link.target.toLowerCase() !== '_self')) return;
      const destination = new URL(link.href, window.location.href);
      if (!['http:', 'https:'].includes(destination.protocol) ||
          destination.href.split('#')[0] === window.location.href.split('#')[0]) return;
      try {
        const state = history.state;
        if (state === null || (typeof state === 'object' && !Array.isArray(state))) {
          history.replaceState({ ...state, [returnKey]: current }, '');
        }
      } catch (_) { /* Navigation still works when history cannot be updated. */ }
    });
    box.addEventListener('close', () => { if (opener.isConnected) opener.focus(); });
    document.body.appendChild(box);
    return box;
  }

  async function openTour(index, followFallback) {
    if (loading) return;
    loading = true;
    try {
      if (!dialog) {
        const response = await fetch(opener.href, { credentials: 'same-origin' });
        if (!response.ok) throw new Error('Tour page unavailable');
        const page = new DOMParser().parseFromString(await response.text(), 'text/html');
        const sourceSteps = Array.from(page.querySelectorAll('section[data-tour-step]'));
        if (sourceSteps.length === 0 || sourceSteps.some(section => !section.querySelector('h2, h3'))) throw new Error('Tour incomplete');
        dialog = makeDialog(sourceSteps, page.querySelector('main > .tour-next'));
      }
      current = Math.max(0, Math.min(steps.length - 1, index));
      update();
      if (!dialog.open) dialog.showModal();
      const heading = steps[current].querySelector('h2, h3');
      if (heading) heading.focus();
    } catch (_) {
      if (followFallback) window.location.href = opener.href;
    } finally {
      loading = false;
    }
  }
  opener.addEventListener('click', event => {
    if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    openTour(0, true);
  });
  window.addEventListener('pageshow', event => {
    const state = history.state;
    if (!state || !Number.isInteger(state[returnKey])) return;
    const index = state[returnKey];
    const rest = { ...state };
    delete rest[returnKey];
    try { history.replaceState(rest, ''); } catch (_) { /* Ignore if history is unavailable. */ }
    const navigation = performance.getEntriesByType('navigation')[0];
    if (event.persisted || (navigation && navigation.type === 'back_forward')) openTour(index, false);
  });
  document.addEventListener('imobx:languagechange', () => { if (dialog) update(); });
  window.addEventListener('resize', updateScrollHint);
})();
