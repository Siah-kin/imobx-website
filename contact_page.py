"""Build the IMOBX contact page."""
import json


def build_contact(root, page, tr, esc, version):
    data = json.loads((root / 'contact-routes.json').read_text())
    contact = data['contact']
    def t(pair, tag='p', attrs=''):
        return tr(*pair, tag, attrs)
    body = '<main class="paper contact-page" id="main">'
    body += t(('Fale com a IMOBX', 'Contact IMOBX'), 'h1')
    body += t(('Tem alguma pergunta sobre a IMOBX? Escreva para a gente.', 'Have a question about IMOBX? Write to us.'))
    body += '<section class="contact-method">'
    body += t(('Por e-mail', 'By email'), 'h2')
    body += t(('Para conversar sobre moradia, parcerias ou financiamento, envie um e-mail.', 'For housing, partnerships or funding, send us an email.'))
    body += '<p><a href="mailto:' + esc(contact['email']) + '">' + esc(contact['email']) + '</a></p></section>'
    body += '<section class="contact-method">'
    body += t(('Trabalhe com a IMOBX', 'Work with IMOBX'), 'h2')
    body += t(('Conheça a vaga atual e saiba como se candidatar.', 'See the current opportunity and how to apply.'))
    body += '<p>' + t(('Ver a vaga', 'See the opportunity'), 'a', 'href="jobs.html"') + '</p></section>'
    body += '<section class="contact-method">'
    body += t(('Comunidade no Telegram', 'Community on Telegram'), 'h2')
    body += t(('O grupo é aberto: as outras pessoas nele podem ver o que você publicar.', 'The group is open: other members can see what you post.'))
    body += '<p>' + t(('Entrar no grupo da IMOBX no Telegram', 'Join the IMOBX group on Telegram'), 'a', f'href="{esc(contact["telegram"])}" target="_blank" rel="noopener noreferrer"') + '</p></section>'
    body += '<noscript><p class="fine" data-pt="É um grupo aberto: todos nele veem o que você publica. Não inclua telefone, endereço nem documentos." data-en="This is an open group: everyone in it sees what you post. Leave out phone numbers, addresses and documents." data-nl="Dit is een open groep: iedereen erin ziet wat je plaatst. Laat telefoonnummers, adressen en documenten weg.">É um grupo aberto: todos nele veem o que você publica. Não inclua telefone, endereço nem documentos.</p></noscript><dialog id="group-dialog" class="group-dialog" aria-labelledby="group-dialog-title"><h2 id="group-dialog-title" data-pt="Antes de entrar" data-en="Before you join" data-nl="Voordat je meedoet">Antes de entrar</h2><p data-pt="É um grupo aberto: todos nele veem o que você publica. Não inclua telefone, endereço nem documentos." data-en="This is an open group: everyone in it sees what you post. Leave out phone numbers, addresses and documents." data-nl="Dit is een open groep: iedereen erin ziet wat je plaatst. Laat telefoonnummers, adressen en documenten weg.">É um grupo aberto: todos nele veem o que você publica. Não inclua telefone, endereço nem documentos.</p><div class="group-dialog-actions"><a class="button" data-go href="https://t.me/+n-42pfkXna5mNzRk" target="_blank" rel="noopener noreferrer" data-pt="Continuar para o Telegram" data-en="Continue to Telegram" data-nl="Verder naar Telegram">Continuar para o Telegram</a><button type="button" data-back data-pt="Voltar" data-en="Back" data-nl="Terug">Voltar</button></div></dialog>'
    body += '</main>'
    (root / 'contact.html').write_text(page('IMOBX | Take part', body,
        '<link rel="stylesheet" href="assets/contact.css"><script src="assets/group-note.js" defer></script>', version=version, lang='pt-BR', title_pt='IMOBX | Participar'))
