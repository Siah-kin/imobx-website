"""Build the IMOBX Take part page: three ways in, the introduction builder, the village picture."""
import json


def build_contact(root, page, tr, esc, version):
    data = json.loads((root / 'contact-routes.json').read_text())
    contact = data['contact']
    def t(pair, tag='p', attrs=''):
        return tr(*pair, tag, attrs)
    # Owner, 8 Nov: three cards (his choice, mock B); the introduction format comes back ("I never asked to remove formats
    # or any kind of methods that help us get to know the person that joins"); no warnings about the group, because the
    # welcome bot covers that; no lines that explain a link or say what happens next.
    body = '<main class="paper contact-page" id="main">'
    body += t(('Participe da IMOBX', 'Take part in IMOBX'), 'h1')
    body += t(('Conte quem você é e o que gostaria de fazer com a IMOBX.', 'Tell us who you are and what you would like to do with IMOBX.'), 'p', 'class="contact-intro"')
    body += '<div class="contact-cards">'
    body += ('<section class="contact-card contact-card-main">' + t(('Apresente-se', 'Introduce yourself'), 'h2')
             + t(('Escrever minha apresentação', 'Write your introduction'), 'a', 'class="contact-button" href="#apresentacao"') + '</section>')
    body += ('<section class="contact-card">' + t(('Prefere e-mail?', 'Prefer email?'), 'h2')
             + t(('E-mail para ' + contact['email'], 'Email ' + contact['email']), 'a', 'class="contact-button contact-button-quiet" href="mailto:' + esc(contact['email']) + '"') + '</section>')
    body += ('<section class="contact-card">' + t(('Trabalhe com a gente', 'Work with us'), 'h2')
             + t(('Ver a vaga', 'See the open role'), 'a', 'class="contact-button contact-button-quiet" href="jobs.html"') + '</section>')
    body += '</div>'

    # The introduction: pick a subject, answer two questions, copy the message, post it in the group.
    body += '<section class="contact-builder" id="apresentacao" aria-labelledby="builder-title">'
    body += t(('Sua apresentação', 'Your introduction'), 'h2', 'id="builder-title"')
    body += '<noscript>' + t(('Este formulário precisa de JavaScript. Você também pode entrar no grupo e escrever direto lá.', 'This form needs JavaScript. You can also join the group and write to us there.')) + '</noscript>'
    body += '<form id="enquiry-form" novalidate><fieldset class="contact-route-picker" id="contact-routes" tabindex="-1"><legend>'
    body += t(('Sobre o que você quer conversar?', 'What would you like to talk about?'), 'span') + '</legend><div class="contact-routes">'
    for route in data['routes']:
        body += f'<label class="contact-route" id="route-{route["id"]}"><input type="radio" name="route" value="{route["id"]}" required><span>'
        body += t(route['title'], 'strong') + t(route['description'], 'span', 'class="contact-route-description"') + '</span></label>'
    body += '</div></fieldset><div id="enquiry-details" hidden>'
    body += '<p class="contact-selected"><strong id="selected-route-name"></strong> ' + t(('Escolher outro assunto', 'Choose another subject'), 'a', 'href="#contact-routes" id="change-route"') + '</p>'
    body += '<div class="contact-field"><label for="contact-name">' + t(('Como podemos chamar você?', 'What should we call you?'), 'span') + '</label><input id="contact-name" name="name" autocomplete="name" maxlength="100" required disabled></div>'
    body += ('<div class="contact-field"><label for="contact-about">' + t(('Conte um pouco sobre você: onde mora e o que faz.', 'Tell us a little about yourself: where you live and what you do.'), 'span')
             + '</label><textarea id="contact-about" name="about" rows="3" maxlength="600" required disabled></textarea></div>')
    body += '<input id="contact-reply" name="reply" type="hidden" value="" disabled><input id="contact-consent" type="hidden" value="" disabled>'
    for route in data['routes']:
        body += f'<fieldset class="route-fields" data-route-fields="{route["id"]}" hidden disabled><legend class="visually-hidden">' + t(route['title'], 'span') + '</legend>'
        for field in route['fields']:
            ident = f'{route["id"]}-{field["id"]}'
            body += '<div class="contact-field"><label for="' + ident + '">' + t(field['label'], 'span') + '</label>'
            required = ' required' if field['required'] else ''
            body += (f'<textarea id="{ident}" name="{ident}" rows="4" maxlength="1500"{required}></textarea>' if field.get('multiline') else f'<input id="{ident}" name="{ident}" maxlength="200"{required}>') + '</div>'
        body += '</fieldset>'
    body += t(('Ver minha mensagem', 'Show my message'), 'button', 'type="submit" class="contact-button"') + '</div></form>'
    body += '<section id="enquiry-review" hidden aria-labelledby="review-title">' + t(('Sua mensagem', 'Your message'), 'h3', 'id="review-title" tabindex="-1"')
    body += '<label for="enquiry-message" class="visually-hidden">' + t(('Sua mensagem', 'Your message'), 'span') + '</label><textarea id="enquiry-message" rows="12" readonly></textarea><div class="contact-actions">'
    body += t(('Copiar mensagem', 'Copy message'), 'button', 'type="button" class="contact-button" id="copy-enquiry"')
    body += t(('Enviar por e-mail', 'Send by email'), 'a', f'class="contact-button contact-button-quiet" id="email-enquiry" href="mailto:{esc(contact["email"])}"')
    body += t(('Abrir o grupo do Telegram', 'Open the Telegram group'), 'a', f'class="contact-button contact-button-telegram" href="{esc(contact["telegram"])}" target="_blank" rel="noopener noreferrer"')
    body += t(('Editar respostas', 'Edit answers'), 'button', 'type="button" class="contact-text-button" id="edit-enquiry"') + '</div>'
    body += '<p id="enquiry-status" role="status" aria-live="polite"></p></section></section>'

    body += ('<figure class="contact-picture"><img src="assets/homepage.jpg" width="1024" height="765" loading="lazy" alt="Ilustração conceitual da primeira vila" data-alt-pt="Ilustração conceitual da primeira vila" data-alt-en="Concept illustration of the first village" data-alt-nl="Conceptillustratie van het eerste dorp">'
             '<figcaption>' + t(('Ilustração conceitual da primeira vila, feita com um gerador de imagens.', 'Concept illustration of the first village, made with an image generator.'), 'span') + '</figcaption></figure>')
    body += '</main>'
    embedded = json.dumps(data, ensure_ascii=False).replace('<', '\\u003c')
    body += '<script id="contact-route-data" type="application/json">' + embedded + '</script>'
    (root / 'contact.html').write_text(page('IMOBX | Take part', body,
        '<link rel="stylesheet" href="assets/contact.css"><script src="assets/contact.js" defer></script>', version=version, lang='pt-BR', title_pt='IMOBX | Participar'))
