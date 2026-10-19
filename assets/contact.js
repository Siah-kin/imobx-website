'use strict';
(() => {
  const form = document.getElementById('enquiry-form');
  if (!form) return;
  const data = JSON.parse(document.getElementById('contact-route-data').textContent);
  const details = document.getElementById('enquiry-details');
  const review = document.getElementById('enquiry-review');
  const message = document.getElementById('enquiry-message');
  const status = document.getElementById('enquiry-status');
  const common = ['contact-name', 'contact-reply', 'contact-consent'].map(id => document.getElementById(id));
  const language = () => document.documentElement.lang.startsWith('pt') ? 0 : 1;
  const say = (pt, en) => language() === 0 ? pt : en;
  let selected = null;

  function showContext() {
    const context = document.getElementById('route-context');
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
    common.forEach(field => { field.disabled = !selected; });
    document.getElementById('selected-route-name').textContent = selected ? selected.title[language()] : '';
    showContext();
    hideReview();
  }

  function prepare() {
    if (!selected) return;
    const lines = [say('Contato IMOBX', 'IMOBX enquiry'), selected.title[language()], '',
      say('Nome: ', 'Name: ') + document.getElementById('contact-name').value.trim(),
      say('Responder por: ', 'Reply to: ') + document.getElementById('contact-reply').value.trim()];
    for (const field of selected.fields) {
      lines.push('', field.label[language()], document.getElementById(`${selected.id}-${field.id}`).value.trim());
    }
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
    status.textContent = say('Mensagem preparada. Ela ainda não foi enviada.', 'Message prepared. It has not been sent.');
    document.getElementById('review-title').focus();
  });
  document.getElementById('copy-enquiry').addEventListener('click', async () => {
    try {
      if (!navigator.clipboard) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(message.value);
      status.textContent = say('Mensagem copiada. Ela ainda não foi enviada.', 'Message copied. It has not been sent.');
    } catch (_) {
      message.focus();
      message.select();
      status.textContent = say('Selecione e copie o texto acima.', 'Select and copy the text above.');
    }
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
      status.textContent = say('Mensagem preparada. Ela ainda não foi enviada.', 'Message prepared. It has not been sent.');
    }
  });
  choose(new URLSearchParams(location.search).get('role'));
})();
