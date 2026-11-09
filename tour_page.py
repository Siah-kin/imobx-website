"""The IMOBX tour: ten chapters that walk through the whole site (owner, 9 Nov: "compelling ... it should reference all the pages
... explain the technical background in a very illustrative way, that's fun to read").

Each chapter has one picture or small drawing, two or three plain sentences and a link to the page it is about. Chapter 1 asks
who the visitor is; the answer decides where the last button leads (contact.html?role=...). The page works on its own,
without JavaScript: the role choices are links and every chapter is readable in order.
"""
from html import escape

NL = {}  # English -> Dutch, merged into i18n/nl.json by the build step below


def T(pt, en, nl):
    NL[en] = nl
    return (pt, en, nl)


def _text(tag, pair, attrs=''):
    pt, en, nl = pair
    a = f'data-pt="{escape(pt, quote=True)}" data-en="{escape(en, quote=True)}" data-nl="{escape(nl, quote=True)}"'
    return f'<{tag} {a}{(" " + attrs) if attrs else ""}>{escape(pt)}</{tag}>'


def _svg_text(x, y, pair, size=18, anchor='middle', weight='700', fill='#193d4e'):
    pt, en, nl = pair
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'data-pt="{escape(pt, quote=True)}" data-en="{escape(en, quote=True)}" data-nl="{escape(nl, quote=True)}">{escape(pt)}</text>')


TEAL, PALE, ORANGE, INK = '#276578', '#edf5f7', '#b35400', '#193d4e'


def svg_bricks():
    """Rent day: part of each payment fills in the house. Example only, no figures."""
    cells = ''
    for i in range(12):
        x, y = 190 + (i % 6) * 38, 105 + (i // 6) * 38
        cells += f'<rect x="{x}" y="{y}" width="30" height="30" rx="3" fill="{TEAL if i < 5 else "#fff"}" stroke="{TEAL}" stroke-width="2"/>'
    return (f'<svg viewBox="0 0 600 240" role="img" aria-hidden="true"><rect width="600" height="240" fill="{PALE}"/>'
            f'<polygon points="170,100 300,28 430,100" fill="{ORANGE}"/><rect x="170" y="100" width="260" height="100" fill="#fff" stroke="{INK}" stroke-width="3"/>'
            + cells
            + _svg_text(300, 226, T('Cada mês, mais um pedaço da casa é seu', 'Each month, a bit more of the house is yours', 'Elke maand is een stukje meer van het huis van jou'), 20)
            + '</svg>')


def svg_repair():
    """A repair from request to open book."""
    boxes = [(30, T('Pedido', 'Request', 'Verzoek')), (225, T('Conferido', 'Checked', 'Gecontroleerd')), (420, T('Livro aberto', 'Open book', 'Open boek'))]
    out = f'<svg viewBox="0 0 600 200" role="img" aria-hidden="true"><rect width="600" height="200" fill="{PALE}"/>'
    for i, (x, label) in enumerate(boxes):
        fill = '#fff' if i < 2 else TEAL
        col = INK if i < 2 else '#fff'
        out += f'<rect x="{x}" y="60" width="150" height="80" rx="8" fill="{fill}" stroke="{TEAL}" stroke-width="3"/>'
        out += _svg_text(x + 75, 108, label, 22, fill=col)
        if i < 2:
            out += f'<path d="M{x + 156} 100 H{x + 189}" stroke="{ORANGE}" stroke-width="4"/><polygon points="{x + 189},92 {x + 199},100 {x + 189},108" fill="{ORANGE}"/>'
    out += _svg_text(300, 176, T('Contratos e dados pessoais ficam privados', 'Contracts and personal data stay private', 'Contracten en persoonsgegevens blijven privé'), 20, weight='400')
    return out + '</svg>'


def svg_courtyard():
    """One member, one vote; the family's housing agreement stays locked."""
    out = f'<svg viewBox="0 0 600 220" role="img" aria-hidden="true"><rect width="600" height="220" fill="{PALE}"/>'
    out += f'<rect x="30" y="40" width="270" height="130" rx="65" fill="#fff" stroke="{TEAL}" stroke-width="3" stroke-dasharray="6 6"/>'
    for i, (x, y) in enumerate([(90, 70), (165, 58), (240, 70), (240, 140), (165, 152), (90, 140)]):
        out += f'<circle cx="{x}" cy="{y}" r="16" fill="{TEAL}"/><path d="M{x - 7} {y} l5 5 l9 -10" stroke="#fff" stroke-width="3" fill="none"/>'
    out += _svg_text(165, 111, T('Um membro, um voto', 'One member, one vote', 'Eén lid, één stem'), 20)
    out += f'<polygon points="380,95 450,45 520,95" fill="{ORANGE}"/><rect x="380" y="95" width="140" height="75" fill="#fff" stroke="{INK}" stroke-width="3"/>'
    out += f'<rect x="438" y="122" width="24" height="22" rx="3" fill="{INK}"/><path d="M443 122 v-6 a7 7 0 0 1 14 0 v6" stroke="{INK}" stroke-width="3" fill="none"/>'
    out += _svg_text(450, 196, T('Só muda se a família concordar', 'Only if the family agrees', 'Alleen als het gezin akkoord is'), 19, weight='400')
    return out + '</svg>'


def svg_token():
    """Trade -> fee -> community work. No percentages: those wait for the lawyer."""
    items = [(100, T('Negociação', 'Trade', 'Transactie')), (300, T('Taxa', 'Fee', 'Vergoeding')), (500, T('Comunidade', 'Community', 'Gemeenschap'))]
    out = f'<svg viewBox="0 0 600 200" role="img" aria-hidden="true"><rect width="600" height="200" fill="{PALE}"/>'
    for i, (x, label) in enumerate(items):
        out += f'<circle cx="{x}" cy="90" r="48" fill="{"#fff" if i < 2 else TEAL}" stroke="{TEAL}" stroke-width="3"/>'
        out += _svg_text(x, 97, label, 17, fill=INK if i < 2 else '#fff')
        if i < 2:
            out += f'<path d="M{x + 54} 90 H{x + 140}" stroke="{ORANGE}" stroke-width="4"/><polygon points="{x + 140},82 {x + 150},90 {x + 140},98" fill="{ORANGE}"/>'
    out += _svg_text(300, 176, T('A cada negociação, a taxa financia o trabalho da comunidade', 'Every trade pays a fee that funds the community', 'Elke transactie betaalt een vergoeding die de gemeenschap financiert'), 19, weight='400')
    return out + '</svg>'


SVGS = {'bricks': svg_bricks, 'repair': svg_repair, 'courtyard': svg_courtyard, 'token': svg_token}

ROLES = [('resident', T('Uma família procurando moradia', 'A family looking for a home', 'Een gezin op zoek naar een woning')),
         ('property', T('Alguém com terreno ou casa', 'Someone with land or a house', 'Iemand met grond of een huis')),
         ('professional', T('Construtor ou profissional', 'A builder or professional', 'Bouwer of professional')),
         ('funding', T('Parceiro ou financiador', 'A partner or funder', 'Partner of financier'))]

# (id, heading, visual, paragraphs, links)  visual: ('img', src, w, h, alt, caption) | ('svg', key) | None
STEPS = [
    ('tour-who', T('Quem é você?', 'Who are you?', 'Wie ben je?'), None,
     [T('Escolha o que mais combina. No fim, levamos você ao lugar certo.', 'Pick the closest one. At the end, we take you to the right place.', 'Kies wat het best past. Aan het eind brengen we je op de juiste plek.')], 'roles'),
    ('tour-home', T('Um lugar para chamar de lar', 'A place to call home', 'Een plek om je thuis te voelen'),
     ('img', 'assets/homepage.jpg', 1024, 765, T('Ilustração conceitual da primeira vila', 'Concept illustration of the first village', 'Conceptillustratie van het eerste dorp'),
      T('Nosso desenho da primeira vila, feito com um gerador de imagens.', 'Our design for the first village, drawn with an image generator.', 'Ons ontwerp voor het eerste dorp, gemaakt met een beeldgenerator.')),
     [T('Construir um lar é uma busca existencial. A IMOBX está preparando um projeto de aluguel com compra no Rio, que será organizado como cooperativa de bairro.',
        'Creating a home is an existential quest. IMOBX is preparing a rent-to-own project in Rio, to be organised as a neighbourhood cooperative.',
        'Een thuis creëren is een existentiële zoektocht. IMOBX bereidt een huurkoopproject in Rio voor, op te zetten als buurtcoöperatie.')],
     [('roadmap.html#village', T('Veja a primeira vila', 'See the first village', 'Bekijk het eerste dorp'))]),
    ('tour-why', T('Por que é tão difícil ter a casa própria?', 'Why is it so hard to own a house?', 'Waarom is een eigen huis zo moeilijk?'),
     ('img', 'assets/community-bay-circles.jpg', 1448, 1086, T('Favelas nos morros ao redor da baía, marcadas com círculos', 'Favelas on the hillsides around the bay, marked with circles', 'Favela’s op de hellingen rond de baai, gemarkeerd met cirkels'),
      T('Os círculos marcam favelas nos morros.', 'The circles mark favelas on the hillsides.', 'De cirkels geven favela’s op de hellingen aan.')),
     [T('Faltam cerca de 6 milhões de moradias no Brasil, e os aluguéis subiram 9,13% nos 12 meses até setembro de 2026, o dobro da inflação oficial. Muitas famílias pagam aluguel por anos sem chegar mais perto da casa própria.',
        'Brazil is short of about 6 million dwellings, and rents rose 9.13% in the 12 months to September 2026, twice the official inflation. Many families pay rent for years without getting closer to owning a house.',
        'In Brazilië ontbreken ongeveer 6 miljoen woningen, en de huren stegen met 9,13% in de 12 maanden tot september 2026, het dubbele van de officiële inflatie. Veel gezinnen betalen jarenlang huur zonder dichter bij een eigen huis te komen.')],
     [('why.html', T('Leia os números', 'Read the numbers', 'Lees de cijfers'))]),
    ('tour-rent', T('Dia de aluguel, com um tijolo seu', 'Rent day, with a brick of your own', 'Huurdag, met een eigen steen'),
     ('svg', 'bricks', T('Exemplo, sem valores reais.', 'An example, with no real figures.', 'Een voorbeeld, zonder echte bedragen.')),
     [T('No aluguel com compra, você paga todo mês como no aluguel, e parte de cada pagamento conta para comprar a casa. O preço, o pagamento e quanto conta ficam combinados por escrito antes de você se mudar.',
        'In rent-to-own, you pay each month like rent, and part of every payment counts towards buying the house. The price, the payment and how much counts are agreed in writing before you move in.',
        'Bij huurkoop betaal je elke maand zoals huur, en een deel van elke betaling telt mee voor de aankoop van het huis. De prijs, de betaling en hoeveel meetelt worden schriftelijk afgesproken voordat je erin trekt.')],
     [('rent-to-own.html', T('Como funciona o aluguel com compra', 'How rent-to-own works', 'Zo werkt huurkoop'))]),
    ('tour-builder', T('Quem constrói, e quanto custa', 'Who builds it, and what it costs', 'Wie bouwt het, en wat kost het'),
     ('img', 'assets/property-1.jpg', 823, 581, T('Modelo 3D dos dois lofts', '3D model of the two lofts', '3D-model van de twee lofts'),
      T('Nosso modelo 3D dos dois lofts, janeiro de 2026.', 'Our 3D model of the two lofts, January 2026.', 'Ons 3D-model van de twee lofts, januari 2026.')),
     [T('Rafael, um dos fundadores, é engenheiro civil e tem a sua própria construtora. O preço dela é ligado ao índice público de custo da construção do Rio (CUB). Planejamos começar com uma família, muito provavelmente no apartamento do Rafael em Guadalupe, e depois construir alguns apartamentos de cada vez.',
        'Rafael, one of the founders, is a civil engineer with his own construction company. Its price is tied to Rio’s public building-cost index (CUB). We plan to start with one family, most likely in Rafael’s flat in Guadalupe, and then build a few flats at a time.',
        'Rafael, een van de oprichters, is civiel ingenieur met een eigen bouwbedrijf. De prijs is gekoppeld aan de openbare bouwkostenindex van Rio (CUB). We willen beginnen met één gezin, hoogstwaarschijnlijk in Rafaels appartement in Guadalupe, en daarna telkens een paar appartementen bouwen.')],
     [('transparency.html', T('O que custa uma casa', 'What a house costs', 'Wat een huis kost')), ('roadmap.html', T('Onde estamos agora', 'Where we are now', 'Waar we nu staan'))]),
    ('tour-books', T('Um reparo, do pedido ao livro aberto', 'A repair, from request to open book', 'Een reparatie, van verzoek tot open boek'),
     ('svg', 'repair', None),
     [T('Um vizinho pede um reparo. Uma pessoa fica responsável e outra confere o resultado. No nosso plano, cada pagamento que a IMOBX faz, com o nome de quem aprovou, vai para um livro de contas aberto que qualquer pessoa pode ler. Quem confere o reparo confirma que ele foi feito.',
        'A neighbour asks for a repair. One person is responsible and another checks the result. In our plan, each payment IMOBX makes, with the name of who approved it, goes into an open book that anyone can read. The person who checks the repair confirms it was done.',
        'Een buur vraagt om een reparatie. Eén persoon is verantwoordelijk en een ander controleert het resultaat. In ons plan komt elke betaling die IMOBX doet, met de naam van wie die goedkeurde, in een open boek dat iedereen kan lezen. Wie de reparatie controleert, bevestigt dat die is uitgevoerd.')],
     [('blockchain.html', T('Como funcionam as contas abertas', 'How the open books work', 'Hoe de open boeken werken'))]),
    ('tour-courtyard', T('A reunião no pátio', 'The courtyard meeting', 'De vergadering op de binnenplaats'),
     ('svg', 'courtyard', None),
     [T('Os moradores cuidam juntos dos espaços comuns. Numa cooperativa, cada membro tem o mesmo peso nas decisões. Nenhuma votação pode mudar o contrato de moradia de uma família: ele só muda quando a família e a IMOBX concordam, dentro da lei brasileira.',
        'Residents look after the shared places together. In a cooperative, each member has an equal say in decisions. No vote can change a family’s housing agreement: it changes only when the family and IMOBX both agree, under Brazilian law.',
        'Bewoners zorgen samen voor de gedeelde plekken. In een coöperatie heeft elk lid evenveel inspraak. Geen stemming kan de woonovereenkomst van een gezin veranderen: die verandert alleen als het gezin en IMOBX het allebei eens zijn, binnen de Braziliaanse wet.')],
     [('governance.html', T('Quem decide, e quando', 'Who decides, and when', 'Wie beslist, en wanneer')), ('governance.html#cooperative', T('Por que uma cooperativa', 'Why a cooperative', 'Waarom een coöperatie'))]),
    ('tour-token', T('Para os curiosos: o token', 'For the curious: the token', 'Voor de nieuwsgierigen: de token'),
     ('svg', 'token', None),
     [T('Mais adiante, a IMOBX também planeja um token. Ter o token é opcional, e as famílias nunca precisam dele. A primeira casa é financiada à parte, nunca pelo token.',
        'Later on, IMOBX also plans a token. Holding it is optional, and families never need it. The first house is funded separately, never by the token.',
        'Later wil IMOBX ook een token uitgeven. Een token hebben is vrijwillig, en gezinnen hebben het nooit nodig. Het eerste huis wordt apart gefinancierd, nooit met de token.')],
     [('token.html', T('Como o token funciona', 'How the token works', 'Hoe de token werkt'))]),
    ('tour-people', T('Quem começou isto, e onde ler mais', 'Who started this, and where to read more', 'Wie begon dit, en waar kun je meer lezen'), None,
     [T('Rafael constrói. John passou anos procurando formas de as comunidades compartilharem o que pertence a todos. Leia as histórias deles, a proposta completa e a pesquisa que estudamos.',
        'Rafael builds. John has spent years looking for ways for communities to share what belongs to everyone. Read their stories, the full proposal and the research we studied.',
        'Rafael bouwt. John zoekt al jaren naar manieren waarop gemeenschappen delen wat van iedereen is. Lees hun verhalen, het volledige voorstel en het onderzoek dat we bestudeerden.')],
     [('about.html', T('Sobre a IMOBX', 'About IMOBX', 'Over IMOBX')), ('resources.html', T('Documentos e fontes', 'Documents and sources', 'Documenten en bronnen')), ('commons-research.html', T('A pesquisa sobre propriedade compartilhada', 'The research on shared ownership', 'Het onderzoek naar gedeeld eigendom'))]),
    ('tour-join', T('Sua vez', 'Your turn', 'Jouw beurt'), None,
     [T('A IMOBX está em preparação, e a sua cooperativa ainda vai ser fundada. Conte quem você é e o que gostaria de fazer com a gente. Se procura trabalho, veja também a vaga aberta.',
        'IMOBX is in preparation, and its cooperative is still to be founded. Tell us who you are and what you would like to do with us. If you are looking for work, see the open role too.',
        'IMOBX is in voorbereiding, en de coöperatie moet nog worden opgericht. Vertel ons wie je bent en wat je met ons wilt doen. Zoek je werk, bekijk dan ook de open vacature.')],
     [('contact.html#apresentacao', T('Apresente-se', 'Introduce yourself', 'Stel je voor'), 'tour-cta'), ('jobs.html', T('Ver a vaga', 'See the open role', 'Bekijk de vacature'))]),
]


def _visual(v):
    if not v:
        return ''
    if v[0] == 'img':
        _, src, w, h, alt, cap = v
        a = f'alt="{escape(alt[0], quote=True)}" data-alt-pt="{escape(alt[0], quote=True)}" data-alt-en="{escape(alt[1], quote=True)}" data-alt-nl="{escape(alt[2], quote=True)}"'
        return f'<figure class="tour-figure"><img src="{src}" width="{w}" height="{h}" {a}>' + _text('figcaption', cap) + '</figure>'
    out = '<figure class="tour-figure tour-drawing">' + SVGS[v[1]]()
    if v[2]:
        out += _text('figcaption', v[2])
    return out + '</figure>'


def build_tour(root, page, version):
    body = '<main class="paper guide-paper tour-page" id="main">' + _text('h1', T('Conheça a IMOBX', 'Take a tour of IMOBX', 'Ontdek IMOBX'))
    for ident, heading, visual, paragraphs, links in STEPS:
        body += f'<section data-tour-step id="{ident}">' + _text('h2', heading) + _visual(visual)
        body += ''.join(_text('p', p) for p in paragraphs)
        if links == 'roles':
            body += '<ul class="tour-roles">' + ''.join(
                '<li>' + _text('a', label, f'href="contact.html?role={rid}#apresentacao" data-tour-role="{rid}" class="tour-role"') + '</li>' for rid, label in ROLES) + '</ul>'
        else:
            body += '<p class="tour-links">' + ' '.join(
                _text('a', l[1], f'href="{escape(l[0], quote=True)}"' + (f' class="{l[2]}"' if len(l) > 2 else '')) for l in links) + '</p>'
        body += '</section>'
    body += '</main>'
    (root / 'tour.html').write_text(page('IMOBX | Take a tour', body, '<link rel="stylesheet" href="assets/tour.css">', version=version,
                                         lang='pt-BR', title_pt='IMOBX | Conheça a IMOBX'), encoding='utf-8')
