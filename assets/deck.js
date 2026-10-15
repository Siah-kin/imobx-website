'use strict';
const deck = document.querySelector('.deck');
const slides = Array.from(document.querySelectorAll('.slide'));
const previous = document.querySelector('[data-previous]');
const next = document.querySelector('[data-next]');
const counter = document.querySelector('[data-counter]');
const notes = document.querySelector('[data-notes]');
let current = 0;
function show(index) {
  current = Math.max(0, Math.min(slides.length - 1, index));
  slides.forEach((slide, number) => { slide.hidden = number !== current; });
  counter.textContent = `${current + 1} / ${slides.length}`;
  previous.disabled = current === 0;
  next.disabled = current === slides.length - 1;
}
if (deck && slides.length && previous && next && counter && notes) {
  deck.classList.add('enhanced');
  document.querySelector('.deck-controls').hidden = false;
  document.querySelectorAll('.notes').forEach(note => { note.hidden = true; });
  previous.addEventListener('click', () => show(current - 1));
  next.addEventListener('click', () => show(current + 1));
  notes.addEventListener('click', () => {
    const enabled = notes.getAttribute('aria-pressed') !== 'true';
    notes.setAttribute('aria-pressed', String(enabled));
    document.querySelectorAll('.notes').forEach(note => { note.hidden = !enabled; });
  });
  document.addEventListener('keydown', event => {
    if (document.activeElement.isContentEditable || ['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)) return;
    if (event.key === 'ArrowRight') { event.preventDefault(); show(current + 1); }
    if (event.key === 'ArrowLeft') { event.preventDefault(); show(current - 1); }
    if (event.key === 'Home') { event.preventDefault(); show(0); }
    if (event.key === 'End') { event.preventDefault(); show(slides.length - 1); }
  });
  show(0);
}
