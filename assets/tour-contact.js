/* Mount the tour's private contact questionnaire in an existing container. */
(function () {
  'use strict';
  const copy = {
    pt: {
      talk: 'Conversar conosco', intro: 'Conte um pouco sobre o que trouxe você até aqui.',
      path: 'Como gostaria de participar?', choose: 'Escolha uma opção',
      paths: ['Buscar uma moradia', 'Oferecer um imóvel', 'Colaborar como profissional', 'Ajudar com recursos', 'Outro'],
      topic: 'Sobre o que gostaria de conversar?', message: 'Sua mensagem',
      note: 'Ao continuar, seu aplicativo de email abrirá com a mensagem. Você poderá revisá-la antes de enviar para contact@imobx.org. Podemos responder ao endereço de email usado no envio.',
      info: 'Suas informações', details: 'Este navegador lembra se você começou ou pulou a visita, quando possível. A opção de participação escolhida preenche este formulário. Fazer a visita não inscreve você em novidades por email.',
      privacy: 'Usaremos sua mensagem para responder e conversar sobre sua participação.',
      send: 'Abrir email', subject: 'Conversa com a IMOBX',
    },
    en: {
      talk: 'Talk to us', intro: 'Tell us a little about what brought you here.',
      path: 'How would you like to take part?', choose: 'Choose an option',
      paths: ['Find a home', 'Offer a property', 'Help as a professional', 'Help with funding', 'Other'],
      topic: 'What would you like to talk about?', message: 'Your message',
      note: 'Continue to open your email app with the message. You can review it before sending it to contact@imobx.org. We can reply to the email address you send it from.',
      info: 'Your information', details: 'This browser remembers whether you started or skipped the tour when possible. The participation option you select is filled into this form. Taking the tour does not sign you up for email updates.',
      privacy: 'We will use your message to reply and discuss how you would like to take part.',
      send: 'Open email', subject: 'A conversation with IMOBX',
    },
    nl: {
      talk: 'Praat met ons', intro: 'Vertel ons wat je hierheen heeft gebracht.',
      path: 'Hoe wil je meedoen?', choose: 'Kies een optie',
      paths: ['Een woning zoeken', 'Een pand aanbieden', 'Als professional helpen', 'Helpen met financiering', 'Anders'],
      topic: 'Waarover wil je praten?', message: 'Je bericht',
      note: 'Je e-mailprogramma opent met het bericht. Je kunt het bekijken voordat je het naar contact@imobx.org verstuurt. We kunnen antwoorden op het e-mailadres waarmee je het verstuurt.',
      info: 'Je gegevens', details: 'Deze browser onthoudt waar mogelijk of je de rondleiding bent gestart of hebt overgeslagen. De gekozen manier om mee te doen wordt ingevuld in dit formulier. De rondleiding volgen meldt je niet aan voor nieuws per e-mail.',
      privacy: 'We gebruiken je bericht om te antwoorden en te bespreken hoe je wilt meedoen.',
      send: 'Open e-mail', subject: 'Een gesprek met IMOBX',
    }
  };
  const lang = () => copy[(document.documentElement.lang || 'pt').slice(0, 2)] ? (document.documentElement.lang || 'pt').slice(0, 2) : 'en';
  let serial = 0;
  function mount(container, options) {
    if (!container || container.dataset.tourContactMounted) return;
    container.dataset.tourContactMounted = 'true';
    const id = 'tour-contact-' + (++serial);
    container.classList.add('tour-contact');
    container.innerHTML = '<section class="tour-contact-conversation"><button type="button" data-copy="talk" aria-expanded="false" aria-controls="' + id + '-form"></button><form id="' + id + '-form" hidden><p data-copy="intro"></p><label for="' + id + '-path" data-copy="path"></label><select id="' + id + '-path" required><option value=""></option><option value="resident"></option><option value="property"></option><option value="professional"></option><option value="funding"></option><option value="other"></option></select><label for="' + id + '-topic" data-copy="topic"></label><input id="' + id + '-topic" maxlength="120" required><label for="' + id + '-message" data-copy="message"></label><textarea id="' + id + '-message" rows="4" required></textarea><p class="tour-contact-note" data-copy="note"></p><p class="tour-contact-note" data-copy="privacy"></p><details class="tour-information"><summary data-copy="info"></summary><p data-copy="details"></p></details><button type="submit" data-copy="send"></button></form></section>';
    const select = container.querySelector('select');
    const roles = ['resident', 'property', 'professional', 'funding', 'other'];
    const talkButton = container.querySelector('[data-copy="talk"]');
    const form = container.querySelector('form');
    talkButton.addEventListener('click', () => {
      const expanded = talkButton.getAttribute('aria-expanded') === 'true';
      talkButton.setAttribute('aria-expanded', String(!expanded));
      form.hidden = expanded;
      if (!expanded) select.focus();
    });
    if (options && roles.includes(options.role)) select.value = options.role;
    const update = () => {
      const text = copy[lang()];
      container.querySelectorAll('[data-copy]').forEach(el => { el.textContent = text[el.dataset.copy]; });
      select.options[0].textContent = text.choose;
      text.paths.forEach((label, index) => { select.options[index + 1].textContent = label; });
    };
    container.querySelector('form').addEventListener('submit', event => {
      event.preventDefault();
      const text = copy[lang()];
      const topic = container.querySelector('input').value.trim();
      const message = container.querySelector('textarea').value.trim();
      if (!topic || !message) return;
      const body = text.path + ' ' + text.paths[roles.indexOf(select.value)] + '\n' + text.topic + ' ' + topic + '\n\n' + message;
      window.location.href = 'mailto:contact@imobx.org?subject=' + encodeURIComponent(text.subject + ': ' + topic) + '&body=' + encodeURIComponent(body);
    });
    document.addEventListener('imobx:languagechange', update);
    update();
  }
  window.IMOBXTourContact = { mount: mount };
  const standalone = document.querySelector('[data-tour-contact-page]');
  if (standalone) {
    // On the long page, start each drawing when it enters the viewport.
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver(entries => entries.forEach(entry => {
        if (entry.isIntersecting) { entry.target.classList.add('tour-motion-active'); observer.unobserve(entry.target); }
      }), { threshold: 0.15 });
      document.querySelectorAll('.tour-page [data-tour-step]').forEach(section => observer.observe(section));
    }
    mount(standalone);
    document.querySelectorAll('.tour-page [data-tour-role]').forEach(choice => {
      choice.addEventListener('click', event => {
        if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        standalone.querySelector('select').value = choice.dataset.tourRole;
        document.querySelectorAll('.tour-page [data-tour-role]').forEach(link => {
          const selected = link === choice;
          link.classList.toggle('is-chosen', selected);
          if (selected) link.setAttribute('aria-current', 'true');
          else link.removeAttribute('aria-current');
        });
        const next = choice.closest('section').nextElementSibling;
        const heading = next && next.querySelector('h2');
        if (heading) { heading.tabIndex = -1; heading.focus(); heading.scrollIntoView({block: 'start'}); }
      });
    });
  }
}());
