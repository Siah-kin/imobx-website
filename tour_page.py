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


def _badge(x, y, n, fill=ORANGE):
    return (f'<circle cx="{x}" cy="{y}" r="22" fill="{fill}"/>'
            f'<text x="{x}" y="{y + 10}" text-anchor="middle" font-size="28" font-weight="700" fill="#fff">{n}</text>')


def _arrow(x1, y1, x2, y2):
    """A line with a drawn arrowhead (no <marker>: ids repeat inside the tour dialog and break)."""
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 14 * math.cos(ang), y2 - 14 * math.sin(ang)
    lx, ly = hx + 9 * math.sin(ang), hy - 9 * math.cos(ang)
    rx, ry = hx - 9 * math.sin(ang), hy + 9 * math.cos(ang)
    return (f'<line x1="{x1}" y1="{y1}" x2="{hx:.1f}" y2="{hy:.1f}" stroke="{TEAL}" stroke-width="5"/>'
            f'<polygon points="{x2},{y2} {lx:.1f},{ly:.1f} {rx:.1f},{ry:.1f}" fill="{TEAL}"/>')


ARROW_DEF = ''

# Drawings carry no words: the caption under each one is real text that scales and translates (review, 9 Nov).


def svg_bricks():
    """Rent day: each month, part of the payment counts towards the house. No figures."""
    cells = ''
    for i in range(12):
        x, y = 140 + (i % 6) * 40, 112 + (i // 6) * 40
        cells += f'<rect x="{x}" y="{y}" width="32" height="32" rx="4" fill="{TEAL if i < 5 else "#fff"}" stroke="{TEAL}" stroke-width="3"/>'
    return (f'<svg viewBox="0 0 520 220" role="img" aria-hidden="true"><rect width="520" height="220" fill="{PALE}"/>'
            f'<polygon points="118,104 260,30 402,104" fill="{ORANGE}"/><rect x="118" y="104" width="284" height="100" fill="#fff" stroke="{INK}" stroke-width="4"/>'
            + cells + '</svg>')


def svg_repair():
    """1 request, 2 approved and checked, 3 paid and published in the open book."""
    out = f'<svg viewBox="0 0 520 200" role="img" aria-hidden="true">{ARROW_DEF}<rect width="520" height="200" fill="{PALE}"/>'
    # 1: a wrench on a card
    out += f'<rect x="20" y="50" width="130" height="110" rx="10" fill="#fff" stroke="{TEAL}" stroke-width="4"/>'
    out += f'<path d="M60 125 l35 -35 m-10 -12 a14 14 0 1 0 20 20" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/>'
    # 2: two people, one tick
    out += f'<rect x="195" y="50" width="130" height="110" rx="10" fill="#fff" stroke="{TEAL}" stroke-width="4"/>'
    out += f'<circle cx="240" cy="92" r="14" fill="{INK}"/><circle cx="282" cy="92" r="14" fill="{TEAL}"/><path d="M236 128 l12 12 l26 -28" stroke="{ORANGE}" stroke-width="7" fill="none" stroke-linecap="round"/>'
    # 3: open book
    out += f'<rect x="370" y="50" width="130" height="110" rx="10" fill="{TEAL}"/>'
    out += f'<path d="M392 80 q43 -14 43 6 q0 -20 43 -6 v60 q-43 -14 -43 6 q0 -20 -43 -6z" fill="#fff"/><path d="M435 86 v60" stroke="{TEAL}" stroke-width="3"/>'
    out += _arrow(152, 105, 190, 105) + _arrow(327, 105, 365, 105)
    out += _badge(30, 42, 1) + _badge(205, 42, 2) + _badge(380, 42, 3)
    return out + '</svg>'


def svg_courtyard():
    """Left: one member, one vote around the shared courtyard. Right: the family's agreement, locked."""
    out = f'<svg viewBox="0 0 520 220" role="img" aria-hidden="true"><rect width="520" height="220" fill="{PALE}"/>'
    out += f'<ellipse cx="150" cy="110" rx="120" ry="78" fill="#fff" stroke="{TEAL}" stroke-width="4" stroke-dasharray="8 8"/>'
    for x, y in [(70, 80), (150, 50), (230, 80), (230, 140), (150, 170), (70, 140)]:
        out += f'<circle cx="{x}" cy="{y}" r="20" fill="{TEAL}"/><path d="M{x - 9} {y} l6 6 l12 -13" stroke="#fff" stroke-width="4" fill="none"/>'
    out += f'<rect x="120" y="92" width="60" height="36" rx="4" fill="{PALE}" stroke="{TEAL}" stroke-width="2"/>'
    out += f'<polygon points="330,95 410,40 490,95" fill="{ORANGE}"/><rect x="330" y="95" width="160" height="95" fill="#fff" stroke="{INK}" stroke-width="4"/>'
    out += f'<rect x="394" y="128" width="32" height="30" rx="4" fill="{INK}"/><path d="M401 128 v-9 a9 9 0 0 1 18 0 v9" stroke="{INK}" stroke-width="5" fill="none"/>'
    return out + '</svg>'


def svg_token():
    """Self-compounding as a cycle: 1 a trade, 2 a fee, 3 paid work and new houses, 4 the project grows; back to 1."""
    out = f'<svg viewBox="0 0 520 260" role="img" aria-hidden="true">{ARROW_DEF}<rect width="520" height="260" fill="{PALE}"/>'
    nodes = [(260, 55), (430, 130), (260, 205), (90, 130)]
    out += f'<ellipse cx="260" cy="130" rx="170" ry="75" fill="none" stroke="{TEAL}" stroke-width="4" stroke-dasharray="2 10" stroke-linecap="round"/>'
    out += _arrow(300, 62, 400, 105) + _arrow(400, 158, 300, 200) + _arrow(220, 200, 120, 158) + _arrow(120, 105, 220, 62)
    icons = [
        f'<path d="M240 48 h40 M270 40 l10 8 l-10 8 M280 64 h-40 M250 56 l-10 8 l10 8" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round"/>',
        f'<circle cx="430" cy="130" r="20" fill="{ORANGE}"/><text x="430" y="139" text-anchor="middle" font-size="24" font-weight="700" fill="#fff">%</text>',
        f'<polygon points="236,205 260,186 284,205" fill="{ORANGE}"/><rect x="240" y="205" width="40" height="24" fill="#fff" stroke="{INK}" stroke-width="3"/>',
        f'<circle cx="78" cy="128" r="11" fill="{TEAL}"/><circle cx="102" cy="128" r="11" fill="{TEAL}"/><circle cx="90" cy="110" r="11" fill="{INK}"/>',
    ]
    for (x, y), icon in zip(nodes, icons):
        out += f'<circle cx="{x}" cy="{y}" r="36" fill="#fff" stroke="{TEAL}" stroke-width="4"/>' + icon
    for i, (x, y) in enumerate(nodes, 1):
        out += _badge(x - 34, y - 30, i)
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
     [T('Queremos bairros onde os vizinhos voltam a se conhecer e as crianças brincam onde os pais podem vê-las. A IMOBX está preparando o primeiro projeto no Rio de Janeiro.',
        'We want neighbourhoods where neighbours know each other again and children play where their parents can see them. IMOBX is preparing its first project in Rio de Janeiro.',
        'We willen buurten waar buren elkaar weer kennen en kinderen spelen waar hun ouders ze kunnen zien. IMOBX bereidt zijn eerste project in Rio de Janeiro voor.')],
     [('roadmap.html#village', T('Veja a primeira vila', 'See the first village', 'Bekijk het eerste dorp'))]),
    ('tour-why', T('Por que é tão difícil ter a casa própria?', 'Why is it so hard to own a house?', 'Waarom is een eigen huis zo moeilijk?'),
     ('img', 'assets/community-bay-circles.jpg', 1448, 1086, T('Favelas nos morros ao redor da baía, marcadas com círculos', 'Favelas on the hillsides around the bay, marked with circles', 'Favela’s op de hellingen rond de baai, gemarkeerd met cirkels'),
      T('Os círculos marcam favelas nos morros.', 'The circles mark favelas on the hillsides.', 'De cirkels geven favela’s op de hellingen aan.')),
     [T('Em 2022, faltavam cerca de 6 milhões de moradias no Brasil, e os aluguéis subiram 9,13% nos 12 meses até setembro de 2026, o dobro da inflação oficial. Muitas famílias pagam aluguel por anos sem chegar mais perto da casa própria.',
        'In 2022 Brazil was short of about 6 million dwellings, and rents rose 9.13% in the 12 months to September 2026, twice the official inflation. Many families pay rent for years without getting closer to owning a house.',
        'In 2022 ontbraken in Brazilië ongeveer 6 miljoen woningen, en de huren stegen met 9,13% in de 12 maanden tot september 2026, het dubbele van de officiële inflatie. Veel gezinnen betalen jarenlang huur zonder dichter bij een eigen huis te komen.')],
     [('why.html', T('Leia os números', 'Read the numbers', 'Lees de cijfers'))]),
    ('tour-rent', T('Dia de aluguel, com um tijolo seu', 'Rent day, with a brick of your own', 'Huurdag, met een eigen steen'),
     ('svg', 'bricks', T('Um exemplo, sem valores reais: a cada mês, uma parte do pagamento conta para a compra.', 'An example, with no real figures: each month, part of the payment counts towards the house.', 'Een voorbeeld, zonder echte bedragen: elke maand telt een deel van de betaling mee voor het huis.')),
     [T('No aluguel com compra, você paga todo mês como no aluguel, e parte de cada pagamento conta para comprar a casa. O preço, o pagamento e quanto conta ficam combinados por escrito antes de você se mudar.',
        'In rent-to-own, you pay each month like rent, and part of every payment counts towards buying the house. The price, the payment and how much counts are agreed in writing before you move in.',
        'Bij huurkoop betaal je elke maand zoals huur, en een deel van elke betaling telt mee voor de aankoop van het huis. De prijs, de betaling en hoeveel meetelt worden schriftelijk afgesproken voordat je erin trekt.')],
     [('rent-to-own.html', T('Como funciona o aluguel com compra', 'How rent-to-own works', 'Zo werkt huurkoop'))]),
    ('tour-builder', T('Quem constrói, e onde começamos', 'Who builds, and where we start', 'Wie bouwt er, en waar beginnen we'),
     ('img', 'assets/property-1.jpg', 823, 581, T('Modelo 3D dos dois lofts', '3D model of the two lofts', '3D-model van de twee lofts'),
      T('Dois lofts que a construtora do Rafael está construindo.', 'Two lofts Rafael’s company is building.', 'Twee lofts die het bouwbedrijf van Rafael bouwt.')),
     [T('Rafael, um dos fundadores, é engenheiro civil e tem a sua própria construtora. Ela cobra a obra pelo índice público de custo da construção do Rio (CUB). Planejamos começar com uma família, muito provavelmente no apartamento do Rafael em Guadalupe, e depois construir alguns apartamentos de cada vez.',
        'Rafael, one of the founders, is a civil engineer with his own construction company. It charges for building work by Rio’s public building-cost index (CUB). We plan to start with one family, most likely in Rafael’s flat in Guadalupe, and then build a few flats at a time.',
        'Rafael, een van de oprichters, is civiel ingenieur met een eigen bouwbedrijf. Het rekent de bouw af volgens de openbare bouwkostenindex van Rio (CUB). We willen beginnen met één gezin, hoogstwaarschijnlijk in Rafaels appartement in Guadalupe, en daarna telkens een paar appartementen bouwen.')],
     [('transparency.html', T('O que custa uma casa', 'What a house costs', 'Wat een huis kost')), ('roadmap.html', T('Onde estamos agora', 'Where we are now', 'Waar we nu staan'))]),
    ('tour-books', T('Um reparo, do pedido ao livro aberto', 'A repair, from request to open book', 'Een reparatie, van verzoek tot open boek'),
     ('svg', 'repair', T('1 O pedido · 2 aprovado e conferido · 3 pago e publicado no livro aberto.', '1 The request · 2 approved and checked · 3 paid and published in the open book.', '1 Het verzoek · 2 goedgekeurd en gecontroleerd · 3 betaald en gepubliceerd in het open boek.')),
     [T('Um vizinho pede um reparo. Uma pessoa aprova o serviço, outra confere, e só então ele é pago. No nosso plano, cada pagamento é publicado num livro de contas aberto, com o nome de quem aprovou. Os contratos e os dados pessoais ficam privados.',
        'A neighbour asks for a repair. One person approves the work, another checks it, and only then is it paid. In our plan, each payment is published in an open book, with the name of who approved it. Contracts and personal data stay private.',
        'Een buur vraagt om een reparatie. Eén persoon keurt het werk goed, een ander controleert het, en pas dan wordt het betaald. In ons plan wordt elke betaling gepubliceerd in een open boek, met de naam van wie die goedkeurde. Contracten en persoonsgegevens blijven privé.')],
     [('blockchain.html', T('Como funcionam as contas abertas', 'How the open books work', 'Hoe de open boeken werken'))]),
    ('tour-courtyard', T('A reunião no pátio', 'The courtyard meeting', 'De vergadering op de binnenplaats'),
     ('svg', 'courtyard', T('À esquerda: um membro, um voto. À direita: o contrato da família, que só muda com a família e a IMOBX de acordo.', 'Left: one member, one vote. Right: the family’s agreement, which changes only when the family and IMOBX agree.', 'Links: één lid, één stem. Rechts: de overeenkomst van het gezin, die alleen verandert als gezin en IMOBX akkoord zijn.')),
     [T('Os moradores cuidam juntos dos espaços comuns. Numa cooperativa, cada membro tem o mesmo peso nas decisões. Nenhuma votação pode mudar o contrato de moradia de uma família: ele só muda quando a família e a IMOBX concordam, dentro da lei brasileira.',
        'Residents look after the shared places together. In a cooperative, each member has an equal say in decisions. No vote can change a family’s housing agreement: it changes only when the family and IMOBX both agree, under Brazilian law.',
        'Bewoners zorgen samen voor de gedeelde plekken. In een coöperatie heeft elk lid evenveel inspraak. Geen stemming kan de woonovereenkomst van een gezin veranderen: die verandert alleen als het gezin en IMOBX het allebei eens zijn, binnen de Braziliaanse wet.')],
     [('governance.html', T('Quem decide, e quando', 'Who decides, and when', 'Wie beslist, en wanneer'))]),
    ('tour-token', T('Para os curiosos: o token', 'For the curious: the token', 'Voor de nieuwsgierigen: de token'),
     ('svg', 'token', T('1 Alguém negocia o token · 2 a negociação paga uma taxa · 3 a taxa paga trabalho e novas casas · 4 o projeto cresce com o que ele mesmo gera, e o ciclo recomeça.', '1 Someone trades the token · 2 the trade pays a fee · 3 the fee pays for work and new houses · 4 the project grows from what it earns, and the cycle starts again.', '1 Iemand verhandelt de token · 2 de transactie betaalt een vergoeding · 3 die betaalt werk en nieuwe huizen · 4 het project groeit met wat het zelf verdient, en de cirkel begint opnieuw.')),
     [T('Mais adiante, a IMOBX também planeja um token self-compounding de financiamento da comunidade. Ter o token é opcional, e as famílias não precisam dele. A primeira casa é financiada à parte.',
        'Later on, IMOBX also plans a self-compounding community-funding token. Holding it is optional, and families don’t need it. The first house is funded separately.',
        'Later wil IMOBX ook een self-compounding token uitgeven die de gemeenschap financiert. Een token hebben is vrijwillig, en gezinnen hebben het niet nodig. Het eerste huis wordt apart gefinancierd.')],
     [('token.html', T('Como o token funciona', 'How the token works', 'Hoe de token werkt'))]),
    ('tour-people', T('Quem começou a IMOBX, e por quê?', 'Who started IMOBX, and why?', 'Wie begon IMOBX, en waarom?'), None,
     [T('Rafael pergunta: por que ter a própria caverna não é um direito de todos? John passou anos procurando formas de as comunidades compartilharem o que pertence a todos.',
        'Rafael asks: why isn’t having one’s own cave a right for everyone? John has spent years looking for ways for communities to share what belongs to everyone.',
        'Rafael vraagt: waarom is een eigen grot geen recht voor iedereen? John zoekt al jaren naar manieren waarop gemeenschappen delen wat van iedereen is.')],
     [('about.html', T('Sobre a IMOBX', 'About IMOBX', 'Over IMOBX')), ('resources.html', T('Documentos e fontes', 'Documents and sources', 'Documenten en bronnen')), ('commons-research.html', T('A pesquisa sobre propriedade compartilhada', 'The research on shared ownership', 'Het onderzoek naar gedeeld eigendom'))]),
    ('tour-join', T('Sua vez', 'Your turn', 'Jouw beurt'), None,
     [T('A IMOBX está em preparação, e a sua cooperativa ainda vai ser fundada. Buscamos a primeira família, a primeira casa e as pessoas que vão fundar a cooperativa com a gente.',
        'IMOBX is in preparation, and its cooperative is still to be founded. We are looking for the first family, the first house and the people who will found the cooperative with us.',
        'IMOBX is in voorbereiding, en de coöperatie moet nog worden opgericht. We zoeken het eerste gezin, het eerste huis en de mensen die de coöperatie met ons oprichten.')],
     [('contact.html#apresentacao', T('Apresente-se', 'Introduce yourself', 'Stel jezelf voor'), 'tour-cta'), ('jobs.html', T('Ver a vaga', 'See the open role', 'Bekijk de vacature'))]),
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
