"""Build the IMOBX contact page."""
import json


def build_contact(root, page, tr, esc, version):
    data = json.loads((root / 'contact-routes.json').read_text())
    contact = data['contact']
    def t(pair, tag='p', attrs=''):
        return tr(*pair, tag, attrs)
    body = '<main class="paper contact-page" id="main">'
    body += t(('Fale com a IMOBX', 'Contact IMOBX'), 'h1')
    # Owner, 8 Nov: lines that explain what each link does, or warn about the group, are narration. One sentence per
    # route, the link inside it. The group note stays in the window that opens on the Telegram link (owner, 28 Oct).
    mail = '<a href="mailto:' + esc(contact['email']) + '">' + esc(contact['email']) + '</a>'
    body += '<p class="contact-lead">' + t(('Escreva para', 'Write to'), 'span') + ' ' + mail + ' ' + t(('sobre moradia, parcerias ou financiamento.', 'about housing, partnerships or funding.'), 'span') + '</p>'
    body += '<p>' + t(('Acompanhe o projeto no', 'Follow the project in'), 'span') + ' ' + t(('grupo da IMOBX no Telegram', 'the IMOBX group on Telegram'), 'a', f'href="{esc(contact["telegram"])}" target="_blank" rel="noopener noreferrer"') + '.</p>'
    body += '<p>' + t(('Procuramos uma pessoa para a', 'We are looking for a'), 'span') + ' ' + t(('captação de recursos e parcerias', 'fundraising and partnerships coordinator'), 'a', 'href="jobs.html"') + '.</p>'
    body += '<noscript><p class="fine" data-pt="É um grupo aberto: todos nele veem o que você publica. Não inclua telefone, endereço nem documentos." data-en="This is an open group: everyone in it sees what you post. Leave out phone numbers, addresses and documents." data-nl="Dit is een open groep: iedereen erin ziet wat je plaatst. Laat telefoonnummers, adressen en documenten weg.">É um grupo aberto: todos nele veem o que você publica. Não inclua telefone, endereço nem documentos.</p></noscript><dialog id="group-dialog" class="group-dialog" aria-labelledby="group-dialog-title"><h2 id="group-dialog-title" data-pt="Antes de entrar" data-en="Before you join" data-nl="Voordat je meedoet">Antes de entrar</h2><p data-pt="É um grupo aberto: todos nele veem o que você publica. Não inclua telefone, endereço nem documentos." data-en="This is an open group: everyone in it sees what you post. Leave out phone numbers, addresses and documents." data-nl="Dit is een open groep: iedereen erin ziet wat je plaatst. Laat telefoonnummers, adressen en documenten weg.">É um grupo aberto: todos nele veem o que você publica. Não inclua telefone, endereço nem documentos.</p><div class="group-dialog-actions"><a class="button" data-go href="https://t.me/+n-42pfkXna5mNzRk" target="_blank" rel="noopener noreferrer" data-pt="Continuar para o Telegram" data-en="Continue to Telegram" data-nl="Verder naar Telegram">Continuar para o Telegram</a><button type="button" data-back data-pt="Voltar" data-en="Back" data-nl="Terug">Voltar</button></div></dialog>'
    body += '</main>'
    (root / 'contact.html').write_text(page('IMOBX | Take part', body,
        '<link rel="stylesheet" href="assets/contact.css"><script src="assets/group-note.js" defer></script>', version=version, lang='pt-BR', title_pt='IMOBX | Participar'))
