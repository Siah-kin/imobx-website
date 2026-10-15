'use strict';
function setLanguage(language) {
  document.documentElement.lang = language === 'pt' ? 'pt-BR' : 'en';
  document.querySelectorAll('[data-pt][data-en]').forEach(element => {
    element.textContent = element.dataset[language];
  });
  document.querySelectorAll('img[data-alt-pt][data-alt-en]').forEach(element => {
    element.alt = language === 'pt' ? element.dataset.altPt : element.dataset.altEn;
  });
  document.querySelectorAll('[data-language]').forEach(control => {
    control.setAttribute('aria-pressed', String(control.dataset.language === language));
  });
  const titleKey = language === 'pt' ? 'titlePt' : 'titleEn';
  document.title = document.body.dataset[titleKey] || (language === 'pt'
    ? 'IMOBX | Proposta de piloto no Rio' : 'IMOBX | Proposed Rio housing pilot');
  const navigation = document.querySelector('nav');
  if (navigation) navigation.setAttribute('aria-label', language === 'pt' ? 'Principal' : 'Main');
}
document.querySelectorAll('[data-language]').forEach(button => {
  button.addEventListener('click', () => setLanguage(button.dataset.language));
});
setLanguage(document.documentElement.lang.startsWith('pt') ? 'pt' : 'en');

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
