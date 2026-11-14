"""The privacy page (owner, 13 Nov 2026, decision 55; owner, 14 Nov, decision 57): short and plain, in three languages, for the
independent lawyer to read once.

The facts come from the site's own code: it sets no cookies, loads nothing from other sites, and keeps only the language and the
tour choice in the visitor's browser (assets/site.js, assets/tour.js). The contact form opens the visitor's email app with a message
to contact@imobx.org (assets/contact.js, assets/tour-contact.js). The host, GitHub Pages, logs visitors' IP addresses for security
(GitHub Docs, "About GitHub Pages", section "Data collection"); the page says so and links that page. The page names no person: the
founders are responsible until the cooperative is registered, and contact@imobx.org is how anyone reaches them.
"""


def build_privacy(root, page, tr, esc):
    def t(pair, tag='p', attrs=''):
        return tr(*pair, tag, attrs)

    def linked(*parts):
        out = '<p>'
        for i, part in enumerate(parts):
            out += (' ' if i and not part[1][:1] in '.,;:' else '') + (t(part[:2], 'a', f'href="{esc(part[2])}"') if len(part) == 3 else t(part, 'span'))
        return out + '</p>'

    MAIL = 'mailto:contact@imobx.org'
    b = '<main class="paper privacy-page" id="main">'
    b += t(('Privacidade', 'Privacy'), 'h1')
    b += t(('Ler este site não nos dá nenhum dado seu.', 'Reading this site shares nothing with us.'), 'p', 'class="privacy-lead"')

    b += '<section id="collect">' + t(('O que este site coleta?', 'What does this site collect?'), 'h2')
    b += linked(('Nós mesmos não coletamos nada. O site não usa cookies, não roda ferramentas de análise e não carrega nada de outros sites enquanto você lê. O GitHub Pages, que hospeda o site, registra sim os endereços IP dos visitantes por segurança, como a',
                 'We collect nothing ourselves. The site sets no cookies, runs no analytics and loads nothing from other websites while you read. Its host, GitHub Pages, does log visitors’ IP addresses for security, as'),
                ('documentação do GitHub Pages', 'GitHub’s Pages documentation', 'https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages'),
                ('descreve.', 'describes.'))
    b += '</section>'

    b += '<section id="remember">' + t(('O que ele guarda?', 'What does it remember?'), 'h2')
    b += t(('Duas escolhas, no seu próprio navegador: o idioma que você escolheu e se você começou ou pulou a visita guiada. Elas ficam no seu aparelho. Limpar os dados do site no navegador apaga as duas.',
            'Two choices, kept in your own browser: the language you picked, and whether you started or skipped the tour. They stay on your device. Clearing your browser’s site data removes them.'))
    b += '</section>'

    b += '<section id="write">' + t(('O que acontece quando você nos escreve?', 'What happens when you write to us?'), 'h2')
    b += linked(('O formulário de contato não envia nada sozinho. Ele escreve a sua mensagem no seu aplicativo de e-mail, endereçada a',
                 'The contact form sends nothing by itself. It writes your message in your email app, addressed to'),
                ('contact@imobx.org', 'contact@imobx.org', MAIL),
                (', e ela só vai quando você aperta enviar lá. Aí nós temos o seu endereço de e-mail e o que você escreveu, e usamos isso para responder.',
                 ', and it goes only when you press send there. We then have your email address and what you wrote, and we use them to reply.'))
    b += t(('O link do nosso grupo no Telegram abre o Telegram. Tudo o que você publica lá pode ser lido pelos membros do grupo, e valem as regras do próprio Telegram.',
            'The link to our Telegram group opens Telegram. Everything you post there can be read by the group’s members, and Telegram’s own rules apply.'))
    b += '</section>'

    b += '<section id="responsible">' + t(('Quem é responsável, e como falar com a gente?', 'Who is responsible, and how do you reach us?'), 'h2')
    b += linked(('Os fundadores da IMOBX são responsáveis por este site até a cooperativa ser registrada. Escreva para',
                 'The IMOBX founders are responsible for this site until the cooperative is registered. Write to'),
                ('contact@imobx.org', 'contact@imobx.org', MAIL),
                ('para perguntar o que guardamos sobre você ou para pedir que apaguemos.',
                 'to ask what we hold about you, or to have it deleted.'))
    b += '</section></main>'
    (root / 'privacy.html').write_text(page('IMOBX | Privacy', b, '', lang='pt-BR', title_pt='IMOBX | Privacidade',
                                            description='O que este site coleta, o que ele guarda no seu navegador e quem é responsável.'), encoding='utf-8')
