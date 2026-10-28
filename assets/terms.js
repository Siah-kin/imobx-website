'use strict';
// Jargon popups (owner, 28 Oct 2026): the first use of each word per section, in running sentences only (never in
// headings or table headers: owner, 28 Oct), becomes an orange word that explains itself. Desktop: hovering shows the meaning, no click needed. Phone: a tap opens it. Keyboard: focus shows it,
// Enter or Space keeps it open. Escape, a tap outside or the close button closes it (WCAG 1.4.13).
// The meanings are written into the page by the build (<script type="application/json" id="imobx-terms">).
(function () {
  const dataNode = document.getElementById('imobx-terms');
  const main = document.querySelector('main');
  if (!dataNode || !main || !HTMLElement.prototype.hasOwnProperty('popover')) return;  // the word list stays as fallback
  let terms;
  try { terms = JSON.parse(dataNode.textContent).terms; } catch (_) { return; }

  const CLOSE = { pt: 'Fechar', en: 'Close', nl: 'Sluiten' };
  const HINT = { pt: 'O que significa', en: 'What it means', nl: 'Wat het betekent' };
  const SKIP = 'a, button, summary, label, select, option, textarea, input, svg, nav, .language-controls, .glossary, .term-pop, script, style';
  const canHover = window.matchMedia('(hover: hover) and (pointer: fine)');
  const lang = () => (document.documentElement.lang || 'pt').slice(0, 2);

  // One shared popup.
  const pop = document.createElement('div');
  pop.id = 'term-pop';
  pop.className = 'term-pop';
  pop.setAttribute('popover', 'manual');
  pop.setAttribute('role', 'dialog');
  pop.innerHTML = '<p class="term-pop-word"></p><p class="term-pop-meaning"></p><button type="button" class="term-pop-close"></button>';
  document.body.appendChild(pop);
  const popWord = pop.querySelector('.term-pop-word');
  const popMeaning = pop.querySelector('.term-pop-meaning');
  const popClose = pop.querySelector('.term-pop-close');

  let current = null;      // the word whose meaning is showing
  let pinned = false;      // opened by a tap, Enter or Space: stays until dismissed
  let hideTimer = 0;

  function place(anchor) {
    const r = anchor.getBoundingClientRect();
    const margin = 16;
    pop.style.left = '0px'; pop.style.top = '0px';
    const w = pop.offsetWidth, h = pop.offsetHeight;
    let left = Math.min(Math.max(margin, r.left), window.innerWidth - w - margin);
    let top = r.bottom + 8;
    if (top + h > window.innerHeight - margin && r.top - h - 8 > margin) top = r.top - h - 8;
    top = Math.max(margin, Math.min(top, window.innerHeight - h - margin));
    pop.style.left = Math.max(margin, left) + 'px';
    pop.style.top = top + 'px';
  }
  function show(word, pin) {
    clearTimeout(hideTimer);
    const term = terms.find(t => t.id === word.dataset.term);
    const l = lang();
    const entry = term && (term[l] || term.en);
    if (!entry) return;
    if (current && current !== word) current.setAttribute('aria-expanded', 'false');
    const keep = pinned && current === word;
    current = word;
    pinned = pin || keep;
    popWord.textContent = word.textContent;
    popMeaning.textContent = entry.meaning;
    popClose.textContent = CLOSE[l] || CLOSE.en;
    pop.setAttribute('aria-label', (HINT[l] || HINT.en) + ': ' + word.textContent);
    word.setAttribute('aria-expanded', 'true');
    if (!pop.matches(':popover-open')) pop.showPopover();
    place(word);
  }
  function hide(returnFocus) {
    clearTimeout(hideTimer);
    if (pop.matches(':popover-open')) pop.hidePopover();
    if (current) {
      current.setAttribute('aria-expanded', 'false');
      if (returnFocus) current.focus();
    }
    current = null; pinned = false;
  }
  function hideSoon() {
    clearTimeout(hideTimer);
    if (!pinned) hideTimer = setTimeout(() => hide(false), 350);
  }

  // Popup behaviour: the reader can move the mouse into it; it stays while hovered.
  pop.addEventListener('mouseenter', () => clearTimeout(hideTimer));
  pop.addEventListener('mouseleave', () => { if (canHover.matches) hideSoon(); });
  popClose.addEventListener('click', () => hide(true));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && current) { event.preventDefault(); hide(true); }
  });
  document.addEventListener('pointerdown', event => {
    if (current && !pop.contains(event.target) && !event.target.closest('.term')) hide(false);
  });
  window.addEventListener('resize', () => { if (current) place(current); });
  window.addEventListener('scroll', () => { if (current) place(current); }, { passive: true });

  function makeWord(text, id) {
    const word = document.createElement('button');
    word.type = 'button';
    word.className = 'term';
    word.dataset.term = id;
    word.textContent = text;
    word.setAttribute('aria-expanded', 'false');
    word.setAttribute('aria-controls', 'term-pop');
    word.addEventListener('mouseenter', () => { if (canHover.matches) show(word, false); });
    word.addEventListener('mouseleave', () => { if (canHover.matches) hideSoon(); });
    word.addEventListener('focus', () => { if (!current || current !== word) show(word, false); });
    word.addEventListener('blur', event => { if (!pinned && !pop.contains(event.relatedTarget)) hideSoon(); });
    word.addEventListener('click', () => {
      if (current === word && pinned) { hide(false); return; }
      show(word, true);
    });
    return word;
  }
  // A small "?" beside a link or button whose own words are jargon (a control is never put inside another control).
  function makeNear(id, label) {
    const near = makeWord('?', id);
    near.classList.add('term-near');
    near.setAttribute('aria-label', (HINT[lang()] || HINT.en) + ': ' + label);
    return near;
  }

  const escapeRe = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  function matcher(l) {
    const forms = [];
    terms.forEach(t => { const e = t[l] || t.en; if (e) e.forms.forEach(f => forms.push([f, t.id])); });
    forms.sort((a, b) => b[0].length - a[0].length);  // longest first: "distributed ledger" before "ledger"
    const byForm = new Map(forms.map(([f, id]) => [f.toLocaleLowerCase(), id]));
    const re = new RegExp('(?<![\\p{L}\\p{N}])(' + forms.map(([f]) => escapeRe(f)).join('|') + ')(?![\\p{L}\\p{N}])', 'giu');
    return { re, idOf: s => byForm.get(s.toLocaleLowerCase()) };
  }
  // Once per section (owner's choice, 28 Oct): each section explains its own jargon at its first use in a sentence,
  // so a reader who jumps to a section still gets it. Never in headings; never twice in one section.
  const sectionOf = node => node.closest('section') || main;

  function scan() {
    hide(false);
    main.querySelectorAll('.term-near').forEach(n => n.remove());
    main.querySelectorAll('button.term').forEach(b => b.replaceWith(document.createTextNode(b.textContent)));
    main.normalize();
    const { re, idOf } = matcher(lang());
    const seen = new Map();  // section -> Set of term ids already explained there
    const walker = document.createTreeWalker(main, NodeFilter.SHOW_TEXT, {
      acceptNode: n => n.nodeValue.trim() && !n.parentElement.closest('h1, h2, h3, h4, h5, h6, th, .glossary, .term-pop, script, style, svg, nav, .language-controls, summary')
        ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT });
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    // Plain text first, then links and buttons, so a word is explained in the sentence when it can be.
    const inControl = node => node.parentElement.closest(SKIP);
    nodes.sort((a, b) => (inControl(a) ? 1 : 0) - (inControl(b) ? 1 : 0));
    nodes.forEach(node => {
      const section = sectionOf(node.parentElement);
      if (!seen.has(section)) seen.set(section, new Set());
      const done = seen.get(section);
      const control = inControl(node);
      re.lastIndex = 0;
      const pieces = [];
      let last = 0, m;
      while ((m = re.exec(node.nodeValue))) {
        const id = idOf(m[1]);
        if (!id || done.has(id)) continue;
        done.add(id);
        if (control) {  // jargon inside a link or button: explain it beside the control, once
          if (!control.nextElementSibling || !control.nextElementSibling.classList.contains('term-near')) control.after(makeNear(id, m[1]));
          continue;
        }
        pieces.push(node.nodeValue.slice(last, m.index), makeWord(m[1], id));
        last = m.index + m[1].length;
      }
      if (!pieces.length) return;
      pieces.push(node.nodeValue.slice(last));
      node.replaceWith(...pieces.map(p => typeof p === 'string' ? document.createTextNode(p) : p));
    });
    // The word list at the bottom is now redundant: hide it only after the words work.
    main.querySelectorAll('.glossary').forEach(list => { const fold = list.closest('details') || list; fold.hidden = true; });
  }
  scan();
  document.addEventListener('imobx:languagechange', scan);
})();
