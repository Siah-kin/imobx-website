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
  const returnRoleKey = '__imobxTourReturnRole';
  const validRoles = ['resident', 'property', 'professional', 'funding'];

  function updateScrollHint() {
    if (!dialog || !dialog.open) return;
    const content = dialog.querySelector('[data-tour-content]');
    const hint = dialog.querySelector('[data-tour-scroll-hint]');
    hint.hidden = content.scrollHeight - content.clientHeight - content.scrollTop <= 2;
  }

  let role = null;
  let allSteps = [];  // owner, 9 Nov: the answer to 'Who are you?' decides where the last button leads

  function update() {
    const code = language();
    const words = labels[code];
    allSteps.forEach(step => { step.hidden = true; });
    steps[current].hidden = false;
    dialog.querySelectorAll('[data-pt][data-en]').forEach(node => {
      node.textContent = node.dataset[code] || node.dataset.en;
    });
    dialog.querySelectorAll('img[data-alt-pt][data-alt-en]').forEach(image => {
      image.alt = image.dataset['alt' + code.charAt(0).toUpperCase() + code.slice(1)] || image.dataset.altEn;
    });
    const contactPath = dialog.querySelector('.tour-contact select');
    if (contactPath && role && !contactPath.value) contactPath.value = role;
    dialog.querySelector('[data-tour-progress]').textContent = words.step(current + 1, steps.length);
    dialog.querySelector('[data-tour-bar]').style.width = ((current + 1) / steps.length * 100) + '%';
    dialog.querySelector('[data-tour-close]').textContent = words.close;
    dialog.querySelector('[data-tour-back]').textContent = words.back;
    dialog.querySelector('[data-tour-back]').hidden = current === 0;
    dialog.querySelector('[data-tour-next]').classList.toggle('is-last', current === steps.length - 1);
    dialog.querySelector('[data-tour-next]').textContent = current === steps.length - 1 ? words.finish : words.next;
    dialog.querySelector('[data-tour-scroll-hint]').textContent = words.scroll;
    dialog.querySelectorAll('a.tour-cta').forEach(link => {
      link.href = 'contact.html' + (role ? '?role=' + encodeURIComponent(role) : '') + '#apresentacao';
    });
    dialog.querySelectorAll('a.tour-jobs').forEach(link => { link.hidden = role === 'resident'; });  // a family looking for a home does not need the job link
    dialog.querySelectorAll('[data-tour-role]').forEach(link => {
      const chosen = link.dataset.tourRole === role;
      link.classList.toggle('is-chosen', chosen);
      if (chosen) link.setAttribute('aria-current', 'true');
      else link.removeAttribute('aria-current');
    });
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
    box.innerHTML = '<div class="tour-dialog-shell"><div class="tour-dialog-top"><p class="tour-progress" data-tour-progress aria-live="polite"></p><button type="button" class="tour-close" data-tour-close></button></div><div class="tour-bar" aria-hidden="true"><span data-tour-bar></span></div><div class="tour-dialog-content" data-tour-content></div><p class="tour-scroll-hint" data-tour-scroll-hint hidden></p><div class="tour-dialog-actions"><button type="button" class="tour-back" data-tour-back></button><button type="button" class="tour-next" data-tour-next></button></div></div>';
    const content = box.querySelector('[data-tour-content]');
    content.addEventListener('scroll', updateScrollHint, { passive: true });
    sourceSteps.forEach(section => {
      const copy = document.importNode(section, true);
      // Standalone page anchors must not duplicate ids in the current document.
      copy.removeAttribute('id');
      copy.querySelectorAll('[id]').forEach(node => node.removeAttribute('id'));
      content.appendChild(copy);
    });
    allSteps = Array.from(content.children);
    steps = allSteps.slice();
    // The final card keeps the founders' story and offers a private conversation.
    const last = allSteps[allSteps.length - 1];
    const oldContact = last.querySelector('a.tour-cta');
    const contact = last.querySelector('[data-tour-contact-page]') || document.createElement('div');
    if (!contact.parentNode) last.appendChild(contact);
    if (window.IMOBXTourContact && typeof window.IMOBXTourContact.mount === 'function') {
      try {
        window.IMOBXTourContact.mount(contact, { role });
        if (contact.querySelector('form') && oldContact) oldContact.remove();
      } catch (_) { contact.remove(); /* Preserve the original contact link. */ }
    }
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
      const choice = event.target.closest('[data-tour-role]');
      if (choice) {
        if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        role = choice.dataset.tourRole;
        // Owner, 9 Nov: each visitor gets its own journey. A chapter without data-tour-for is for everyone.
        steps = allSteps.filter(step => !step.dataset.tourFor || step.dataset.tourFor.split(' ').includes(role));
        const contactPath = box.querySelector('.tour-contact select');
        if (contactPath) contactPath.value = role;
        moveTo(current + 1);
        return;
      }
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
          history.replaceState({ ...state, [returnKey]: current, [returnRoleKey]: role }, '');
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
    role = validRoles.includes(state[returnRoleKey]) ? state[returnRoleKey] : null;
    const rest = { ...state };
    delete rest[returnKey];
    delete rest[returnRoleKey];
    try { history.replaceState(rest, ''); } catch (_) { /* Ignore if history is unavailable. */ }
    const navigation = performance.getEntriesByType('navigation')[0];
    if (event.persisted || (navigation && navigation.type === 'back_forward')) openTour(index, false);
  });
  document.addEventListener('imobx:languagechange', () => { if (dialog) update(); });
  window.addEventListener('resize', updateScrollHint);

  // The invitation is optional and only shown when browser storage is available.
  // A fragment is a direct destination, so never cover it with a first-visit prompt.
  const invitationKey = 'imobx-tour-invitation-v1';
  let shouldInvite = false;
  try {
    const previous = localStorage.getItem(invitationKey);
    const probe = invitationKey + '-probe';
    localStorage.setItem(probe, '1');
    localStorage.removeItem(probe);
    shouldInvite = !previous && !window.location.hash;
  } catch (_) { /* Manual tour access remains available. */ }
  if (shouldInvite) {
    const words = {
      pt: { title: 'Conheça a IMOBX', intro: 'Quer conhecer o projeto em uma visita guiada?', take: 'Fazer a visita', skip: 'Pular' },
      en: { title: 'Discover IMOBX', intro: 'Would you like a guided tour of the project?', take: 'Take the tour', skip: 'Skip' },
      nl: { title: 'Ontdek IMOBX', intro: 'Wil je het project leren kennen met een rondleiding?', take: 'Start de rondleiding', skip: 'Overslaan' }
    };
    const invite = document.createElement('dialog');
    invite.className = 'tour-invitation';
    invite.setAttribute('aria-labelledby', 'tour-invitation-title');
    invite.setAttribute('aria-describedby', 'tour-invitation-intro');
    invite.innerHTML = '<div class="tour-invitation-inner"><h2 id="tour-invitation-title"></h2><p id="tour-invitation-intro"></p><div class="tour-invitation-actions"><button type="button" data-invite-take></button><button type="button" data-invite-skip></button></div></div>';
    const renderInvite = () => {
      const w = words[language()];
      invite.querySelector('h2').textContent = w.title;
      invite.querySelector('p').textContent = w.intro;
      invite.querySelector('[data-invite-take]').textContent = w.take;
      invite.querySelector('[data-invite-skip]').textContent = w.skip;
    };
    const remember = choice => { try { localStorage.setItem(invitationKey, choice); } catch (_) {} };
    invite.querySelector('[data-invite-skip]').addEventListener('click', () => { remember('skipped'); invite.close(); });
    invite.querySelector('[data-invite-take]').addEventListener('click', () => { remember('started'); invite.close(); openTour(0, true); });
    invite.addEventListener('cancel', () => remember('skipped'));
    invite.addEventListener('close', () => { if (document.activeElement === document.body && opener.isConnected) opener.focus(); });
    document.addEventListener('imobx:languagechange', renderInvite);
    document.body.appendChild(invite);
    renderInvite();
    try { invite.showModal(); } catch (_) { invite.remove(); }
  }
})();
