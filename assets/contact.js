'use strict';
(() => {
  const form = document.getElementById('enquiry-form');
  if (!form) return;
  const data = JSON.parse(document.getElementById('contact-route-data').textContent);
  const details = document.getElementById('enquiry-details');
  const review = document.getElementById('enquiry-review');
  const message = document.getElementById('enquiry-message');
  const status = document.getElementById('enquiry-status');
  const common = ['contact-name', 'contact-about', 'contact-reply', 'contact-consent'].map(id => document.getElementById(id));
  // 0 Portuguese, 1 English, 2 Dutch (owner, 26 Oct 2026); route data holds [pt, en, nl].
  const language = () => { const l = document.documentElement.lang; return l.startsWith('pt') ? 0 : (l.startsWith('nl') ? 2 : 1); };
  const NL_SAY = {"Hi everyone at IMOBX! My name is ": "Hallo allemaal bij IMOBX! Ik heet ", "Thank you, and I’m happy to talk.": "Alvast bedankt, en ik praat graag verder.", "Please complete this field.": "Vul dit veld in.", "Message copied.": "Bericht gekopieerd.", "Select and copy the text above.": "Selecteer en kopieer de tekst hierboven."};  /* filled from i18n/nl.json at build time */
  const say = (pt, en) => [pt, en, NL_SAY[en] || en][language()];
  let selected = null;

  function showContext() {
    const context = document.getElementById('route-context');  // owner, 8 Nov: no helper lines under the subject
    if (!context) return;
    context.replaceChildren();
    if (!selected) return;
    const explanation = document.createElement('p');
    explanation.textContent = selected.context[language()];
    context.append(explanation);
    if (selected.reading_url && selected.reading_label) {
      const link = document.createElement('a');
      link.href = selected.reading_url;
      link.textContent = selected.reading_label[language()];
      context.append(link);
    }
  }

  function hideReview() {
    review.hidden = true;
    message.value = '';
    status.textContent = '';
  }

  function choose(id) {
    selected = data.routes.find(route => route.id === id) || null;
    form.querySelectorAll('[name="route"]').forEach(input => {
      input.checked = input.value === id;
      input.closest('label').classList.toggle('is-selected', input.checked);
    });
    form.querySelectorAll('[data-route-fields]').forEach(fields => {
      const active = fields.dataset.routeFields === id;
      fields.hidden = !active;
      fields.disabled = !active;
    });
    details.hidden = !selected;
    document.getElementById('contact-routes').classList.toggle('is-chosen', !!selected);
    common.forEach(field => { field.disabled = !selected; });
    document.getElementById('selected-route-name').textContent = selected ? selected.title[language()] : '';
    showContext();
    hideReview();
  }

  function prepare() {
    if (!selected) return;
    // Owner, 8 Nov: a polite introduction a person would post, built from sentences, not our questions pasted back.
    const value = id => document.getElementById(id).value.trim().replace(/[.\s]+$/, '');
    const lines = [say('Olá, pessoal da IMOBX! Meu nome é ', 'Hi everyone at IMOBX! My name is ') + value('contact-name') + '.',
      value('contact-about') + '.', ''];
    for (const field of selected.fields) {
      lines.push(field.lead[language()] + ' ' + value(`${selected.id}-${field.id}`) + '.');
    }
    lines.push('', say('Agradeço desde já e fico à disposição para conversar.', 'Thank you, and I’m happy to talk.'));
    message.value = lines.join('\n');
    const email = document.getElementById('email-enquiry');
    if (email) {
      email.href = `mailto:${data.contact.email}?subject=${encodeURIComponent('IMOBX · ' + selected.title[language()])}&body=${encodeURIComponent(message.value)}`;
    }
  }

  form.addEventListener('change', event => {
    if (event.target.name === 'route') {
      choose(event.target.value);
      const address = new URL(location.href);
      address.searchParams.set('role', selected.id);
      history.replaceState(null, '', address);
      document.getElementById('enquiry-title').focus();
    }
    else hideReview();
  });
  form.addEventListener('input', event => {
    event.target.setCustomValidity('');
    hideReview();
  });
  form.addEventListener('submit', event => {
    event.preventDefault();
    const required = Array.from(form.querySelectorAll('input[required], textarea[required]'))
      .filter(field => !field.matches(':disabled') && !['radio', 'checkbox'].includes(field.type));
    for (const field of required) {
      field.setCustomValidity(field.value.trim() ? '' : say('Preencha este campo.', 'Please complete this field.'));
    }
    if (!form.reportValidity() || !selected) return;
    prepare();
    review.hidden = false;
    message.style.height = 'auto';
    message.style.height = (message.scrollHeight + 4) + 'px';  // the whole message shows, with no empty half
    status.textContent = '';
    document.getElementById('review-title').focus();
  });
  document.getElementById('copy-enquiry').addEventListener('click', async () => {
    try {
      if (!navigator.clipboard) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(message.value);
      status.textContent = say('Mensagem copiada.', 'Message copied.');
    } catch (_) {
      message.focus();
      message.select();
      status.textContent = say('Selecione e copie o texto acima.', 'Select and copy the text above.');
    }
  });
  document.getElementById('change-route').addEventListener('click', event => {
    event.preventDefault();
    document.getElementById('contact-routes').classList.remove('is-chosen');
    document.getElementById('contact-routes').focus();
  });
  document.getElementById('edit-enquiry').addEventListener('click', () => {
    hideReview();
    document.getElementById('contact-name').focus();
  });
  document.addEventListener('imobx:languagechange', () => {
    if (!selected) return;
    document.getElementById('selected-route-name').textContent = selected.title[language()];
    showContext();
    if (!review.hidden) {
      prepare();
    }
  });
  choose(new URLSearchParams(location.search).get('role'));
})();
