"""Build a static enquiry page. Messages are reviewed and sent by the visitor."""
import json


def build_contact(root, page, tr, esc, version):
    data = json.loads((root / 'contact-routes.json').read_text())
    def t(pair, tag='p', attrs=''):
        return tr(*pair, tag, attrs)
    contact = data['contact']
    body = '<main class="paper contact-page" id="main">'
    body += t(('Conte como gostaria de participar', 'Tell us how you would like to take part'), 'h1')
    body += t(('Escolha o assunto mais próximo do que procura. As perguntas mudam conforme sua escolha. Depois, você pode conferir e copiar sua mensagem.', 'Choose the subject closest to what you need. The questions change with your choice. You can then check and copy your message.'))
    if not contact['email'] and not contact['telegram']:
        body += '<aside class="guide-status">' + t(('Os contatos para receber mensagens ainda não estão disponíveis. Nesta página você pode preparar e copiar uma mensagem; o site não a envia.', 'Contact details for receiving messages are not available yet. On this page you can prepare and copy a message; the website does not send it.')) + '</aside>'
    body += '<noscript>' + t(('Para preparar uma mensagem nesta página, ative JavaScript no navegador.', 'Enable JavaScript in your browser to prepare a message on this page.')) + '</noscript>'
    body += '<form id="enquiry-form" novalidate><fieldset class="contact-route-picker" id="contact-routes" tabindex="-1"><legend>'
    body += t(('Sobre o que gostaria de conversar?', 'What would you like to discuss?'), 'span') + '</legend><div class="contact-routes">'
    for route in data['routes']:
        body += f'<label class="contact-route" id="route-{route["id"]}"><input type="radio" name="route" value="{route["id"]}" required><span>'
        body += t(route['title'], 'strong') + t(route['description'], 'span', 'class="contact-route-description"') + '</span></label>'
    body += '</div></fieldset><div id="enquiry-details" hidden>'
    body += t(('Sua apresentação', 'Your introduction'), 'h2', 'id="enquiry-title" tabindex="-1"')
    body += '<p id="selected-route-name" class="contact-selected-route"></p>'
    body += t(('Escolher outro assunto', 'Choose another route'), 'a', 'href="#contact-routes"')
    body += '<div id="route-context" class="contact-context"></div>'
    body += '<div class="contact-field"><label for="contact-name">' + t(('Como podemos chamar você?', 'What should we call you?'), 'span') + '</label><input id="contact-name" name="name" autocomplete="name" maxlength="100" required disabled></div>'
    body += '<div class="contact-field"><label for="contact-reply">' + t(('E-mail ou telefone para resposta', 'Email or phone number for a reply'), 'span') + '</label><input id="contact-reply" name="reply" autocomplete="email" maxlength="160" required disabled></div>'
    for route in data['routes']:
        body += f'<fieldset class="route-fields" data-route-fields="{route["id"]}" hidden disabled><legend class="visually-hidden">' + t(route['title'], 'span') + '</legend>'
        for field in route['fields']:
            ident = f'{route["id"]}-{field["id"]}'
            body += '<div class="contact-field"><label for="' + ident + '">' + t(field['label'], 'span') + '</label>'
            required = ' required' if field['required'] else ''
            body += (f'<textarea id="{ident}" name="{ident}" rows="4" maxlength="1500"{required}></textarea>' if field.get('multiline') else f'<input id="{ident}" name="{ident}" maxlength="200"{required}>') + '</div>'
        body += '</fieldset>'
    body += t(('Escreva uma breve apresentação. Não inclua documentos de identidade, dados bancários nem senhas.', 'Write a brief introduction. Leave out identity documents, bank details and passwords.'))
    body += '<div class="contact-field"><label class="contact-consent"><input type="checkbox" id="contact-consent" required disabled>' + t(('Revisei as informações. Se eu enviar esta mensagem à IMOBX, a equipe poderá usá-la para responder.', 'I have reviewed this information. If I send this message to IMOBX, the team may use it to reply.'), 'span') + '</label></div>'
    body += t(('Revisar mensagem', 'Review message'), 'button', 'type="submit" class="button"') + '</div></form>'
    body += '<section id="enquiry-review" hidden aria-labelledby="review-title">' + t(('Confira sua mensagem', 'Review your message'), 'h2', 'id="review-title" tabindex="-1"')
    body += '<label for="enquiry-message">' + t(('Mensagem preparada', 'Prepared message'), 'span') + '</label><textarea id="enquiry-message" rows="15" readonly></textarea><div class="contact-actions">'
    body += t(('Copiar mensagem', 'Copy message'), 'button', 'type="button" class="button" id="copy-enquiry"')
    if contact['email']:
        body += t(('Abrir no e-mail', 'Open in email'), 'a', f'id="email-enquiry" class="button" href="mailto:{esc(contact["email"])}"')
    if contact['telegram']:
        body += t(('Abrir contato no Telegram', 'Open Telegram contact'), 'a', f'class="button" href="{esc(contact["telegram"])}" target="_blank" rel="noopener noreferrer"')
    body += t(('Editar respostas', 'Edit answers'), 'button', 'type="button" id="edit-enquiry"') + '</div>'
    body += '<p id="enquiry-status" role="status" aria-live="polite"></p>'
    body += t(('Preparar ou copiar a mensagem não a envia. Guarde uma cópia até ter um contato da equipe para recebê-la.', 'Preparing or copying the message does not send it. Keep a copy until you have a team contact to receive it.'), 'p', 'class="fine"')
    body += '</section><section class="contact-next">' + t(('Depois da primeira conversa', 'After the first conversation'), 'h2')
    body += t(('O assunto e a região ajudam a encaminhar a conversa. A equipe poderá esclarecer necessidades e combinar uma avaliação, uma reunião ou a análise de uma proposta. Moradia, contratação e financiamento dependem de acordos próprios.', 'The subject and location help direct the conversation. The team can clarify needs and agree an assessment, meeting or proposal review. Housing, appointments and funding depend on their own agreements.'))
    body += '<p><a href="roadmap.html#participation">' + t(('Conheça os papéis de cada participante', 'Read about each participant’s role'), 'span') + '</a> · <a href="reference.html#status">' + t(('Situação atual do projeto', 'Current project status'), 'span') + '</a></p></section></main>'
    embedded = json.dumps(data, ensure_ascii=False).replace('<', '\\u003c')
    body += '<script id="contact-route-data" type="application/json">' + embedded + '</script>'
    (root / 'contact.html').write_text(page('IMOBX | Take part', body,
        '<link rel="stylesheet" href="assets/contact.css"><script src="assets/contact.js" defer></script>', version=version, lang='pt-BR', title_pt='IMOBX | Participar'))
