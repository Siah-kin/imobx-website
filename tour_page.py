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


def _g(i, inner, extra=''):
    """A drawing part that pops in, one after another (CSS in assets/tour.css; still under reduced motion)."""
    return f'<g class="pop {extra}" style="--i:{i}">{inner}</g>'


def svg_bricks():
    """Rent day: each month, part of the payment counts towards the house. Bricks fill in one by one. No figures."""
    cells = ''
    for i in range(12):
        x, y = 140 + (i % 6) * 40, 112 + (i // 6) * 40
        r = f'<rect x="{x}" y="{y}" width="32" height="32" rx="4" fill="{TEAL if i < 5 else "#fff"}" stroke="{TEAL}" stroke-width="3"/>'
        cells += _g(round(i * 0.7 + 1, 2), r) if i < 5 else r
    return (f'<svg viewBox="0 0 520 220" role="img" aria-hidden="true"><rect width="520" height="220" fill="{PALE}"/>'
            f'<polygon points="118,104 260,30 402,104" fill="{ORANGE}"/><rect x="118" y="104" width="284" height="100" fill="#fff" stroke="{INK}" stroke-width="4"/>'
            + cells + '</svg>')


def svg_repair():
    """1 request, 2 approved and checked, 3 paid and published in the open book. Lights up in order."""
    out = f'<svg viewBox="0 0 520 200" role="img" aria-hidden="true"><rect width="520" height="200" fill="{PALE}"/>'
    c1 = (f'<rect x="20" y="50" width="130" height="110" rx="10" fill="#fff" stroke="{TEAL}" stroke-width="4"/>'
          f'<path d="M60 125 l35 -35 m-10 -12 a14 14 0 1 0 20 20" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/>' + _badge(30, 42, 1))
    c2 = (f'<rect x="195" y="50" width="130" height="110" rx="10" fill="#fff" stroke="{TEAL}" stroke-width="4"/>'
          f'<circle cx="240" cy="92" r="14" fill="{INK}"/><circle cx="282" cy="92" r="14" fill="{TEAL}"/><path d="M236 128 l12 12 l26 -28" stroke="{ORANGE}" stroke-width="7" fill="none" stroke-linecap="round"/>' + _badge(205, 42, 2))
    c3 = (f'<rect x="370" y="50" width="130" height="110" rx="10" fill="{TEAL}"/>'
          f'<path d="M392 80 q43 -14 43 6 q0 -20 43 -6 v60 q-43 -14 -43 6 q0 -20 -43 -6z" fill="#fff"/><path d="M435 86 v60" stroke="{TEAL}" stroke-width="3"/>' + _badge(380, 42, 3))
    return (out + _g(1, c1) + _g(2.2, _arrow(152, 105, 190, 105)) + _g(3, c2) + _g(4.2, _arrow(327, 105, 365, 105)) + _g(5, c3, 'pulse') + '</svg>')


def svg_courtyard():
    """Left: one member, one vote around the shared courtyard. Right: the family's agreement, locked."""
    out = f'<svg viewBox="0 0 520 220" role="img" aria-hidden="true"><rect width="520" height="220" fill="{PALE}"/>'
    out += f'<ellipse cx="150" cy="110" rx="120" ry="78" fill="#fff" stroke="{TEAL}" stroke-width="4" stroke-dasharray="8 8"/>'
    for i, (x, y) in enumerate([(70, 80), (150, 50), (230, 80), (230, 140), (150, 170), (70, 140)]):
        out += _g(round(1 + i * 0.5, 2), f'<circle cx="{x}" cy="{y}" r="20" fill="{TEAL}"/><path d="M{x - 9} {y} l6 6 l12 -13" stroke="#fff" stroke-width="4" fill="none"/>')
    out += f'<rect x="120" y="92" width="60" height="36" rx="4" fill="{PALE}" stroke="{TEAL}" stroke-width="2"/>'
    out += f'<polygon points="330,95 410,40 490,95" fill="{ORANGE}"/><rect x="330" y="95" width="160" height="95" fill="#fff" stroke="{INK}" stroke-width="4"/>'
    out += _g(4.5, f'<rect x="394" y="128" width="32" height="30" rx="4" fill="{INK}"/><path d="M401 128 v-9 a9 9 0 0 1 18 0 v9" stroke="{INK}" stroke-width="5" fill="none"/>', 'lock')
    return out + '</svg>'


def svg_token():
    """Self-compounding as a cycle: 1 a trade, 2 a fee, 3 paid work and new houses, 4 the project grows; back to 1."""
    out = f'<svg viewBox="0 0 520 260" role="img" aria-hidden="true"><rect width="520" height="260" fill="{PALE}"/>'
    nodes = [(260, 55), (430, 130), (260, 205), (90, 130)]
    out += f'<ellipse class="flow" cx="260" cy="130" rx="170" ry="75" fill="none" stroke="{TEAL}" stroke-width="4" stroke-dasharray="2 10" stroke-linecap="round"/>'
    arrows = [_arrow(300, 62, 400, 105), _arrow(400, 158, 300, 200), _arrow(220, 200, 120, 158), _arrow(120, 105, 220, 62)]
    icons = [
        f'<path d="M240 48 h40 M270 40 l10 8 l-10 8 M280 64 h-40 M250 56 l-10 8 l10 8" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round"/>',
        f'<circle cx="430" cy="130" r="20" fill="{ORANGE}"/><text x="430" y="139" text-anchor="middle" font-size="24" font-weight="700" fill="#fff">%</text>',
        f'<polygon points="236,205 260,186 284,205" fill="{ORANGE}"/><rect x="240" y="205" width="40" height="24" fill="#fff" stroke="{INK}" stroke-width="3"/>',
        f'<circle cx="78" cy="128" r="11" fill="{TEAL}"/><circle cx="102" cy="128" r="11" fill="{TEAL}"/><circle cx="90" cy="110" r="11" fill="{INK}"/>',
    ]
    for i, ((x, y), icon) in enumerate(zip(nodes, icons)):
        out += _g(round(1 + i * 1.1, 2), f'<circle cx="{x}" cy="{y}" r="36" fill="#fff" stroke="{TEAL}" stroke-width="4"/>' + icon + _badge(x - 34, y - 30, i + 1))
        out += _g(round(1.6 + i * 1.1, 2), arrows[i])
    return out + '</svg>'


SVGS = {'bricks': svg_bricks, 'repair': svg_repair, 'courtyard': svg_courtyard, 'token': svg_token}

ROLES = [('resident', T('Uma família procurando moradia', 'A family looking for a home', 'Een gezin op zoek naar een woning')),
         ('property', T('Alguém com terreno ou casa', 'Someone with land or a house', 'Iemand met grond of een huis')),
         ('professional', T('Construtor ou profissional', 'A builder or professional', 'Bouwer of professional')),
         ('funding', T('Parceiro ou financiador', 'A partner or funder', 'Partner of financier'))]

JOHN = T('John, cofundador', 'John, co-founder', 'John, medeoprichter')
RAFAEL = T('Rafael Britto, cofundador', 'Rafael Britto, co-founder', 'Rafael Britto, medeoprichter')

# Owner, 9 Nov: "did you just use your own generator to write the text?" Rebuilt with human-copy and Humanizer from
# the founders' own words (SOURCE_WORDS_FOUNDERS_2026-10-27.md; ids in the comments). Each chapter opens differently.
# Chapter: (id, heading, visual, quote, paragraphs, links). quote = (text, who) or None.
STEPS = [
    ('tour-who', T('Quem é você?', 'Who are you?', 'Wie ben je?'), None, None,
     [T('Escolha o que mais combina, e o passeio mostra o que importa para você.', 'Pick the closest one, and the tour shows what matters to you.', 'Kies wat het best past, en de rondleiding laat zien wat voor jou telt.')], 'roles'),
    # WHY-01 (owner's approved landing line)
    ('tour-home', T('Um lugar para chamar de lar', 'A place to call home', 'Een plek om je thuis te voelen'), None,
     (T('Construir um lar é uma busca existencial de todo ser humano, onde quer que esteja.', 'Creating a home is an existential quest for every human, wherever you are.', 'Een thuis creëren is een existentiële zoektocht voor ieder mens, waar je ook bent.'), JOHN),
     [T('A IMOBX está preparando o primeiro projeto no Rio de Janeiro, para famílias que hoje pagam aluguel e querem ter a casa própria.',
        'IMOBX is preparing its first project in Rio de Janeiro, for families who rent today and would like to own.',
        'IMOBX bereidt zijn eerste project in Rio de Janeiro voor, voor gezinnen die nu huren en graag eigenaar willen worden.')],
     [('about.html', T('Por que a IMOBX existe', 'Why IMOBX exists', 'Waarom IMOBX bestaat'))]),
    # SIT-13 as the heading (John); SIT-06 (Rafael)
    ('tour-why', T('Proprietários não conseguem vender. Sonhadores não conseguem comprar.', 'Owners can’t sell. Dreamers can’t buy.', 'Eigenaren kunnen niet verkopen. Dromers kunnen niet kopen.'),
     ('img', 'assets/community-bay-circles.jpg', 1448, 1086, T('Favelas nos morros ao redor da baía, marcadas com círculos', 'Favelas on the hillsides around the bay, marked with circles', 'Favela’s op de hellingen rond de baai, gemarkeerd met cirkels'),
      T('Os círculos marcam favelas nos morros.', 'The circles mark favelas on the hillsides.', 'De cirkels geven favela’s op de hellingen aan.')),
     (T('O absurdo do Brasil não é o preço dos imóveis, é a taxa de juros.', 'The absurdity in Brazil is not the price of real estate, it is the interest rate.', 'Het absurde in Brazilië is niet de prijs van vastgoed, maar de rente.'), RAFAEL),
     [T('Em 2022, faltavam cerca de 6 milhões de moradias no Brasil. Desde então, os aluguéis sobem mais rápido do que a inflação: 9,13% nos 12 meses até setembro de 2026, contra 4,58%. No Rio, a alta foi de 14,80%.',
        'In 2022 Brazil was short of about 6 million dwellings. Rents have since risen faster than inflation: 9.13% in the 12 months to September 2026, against 4.58%. In Rio they rose 14.80%.',
        'In 2022 ontbraken in Brazilië ongeveer 6 miljoen woningen. Sindsdien stijgen de huren sneller dan de inflatie: 9,13% in de 12 maanden tot september 2026, tegen 4,58%. In Rio stegen ze met 14,80%.')],
     [('why.html', T('Leia os números', 'Read the numbers', 'Lees de cijfers'))]),
    ('tour-tenant', T('Um apartamento para começar', 'A flat to start with', 'Een appartement om mee te beginnen'), None, None,
     [T('O Rafael tem um apartamento em Guadalupe, onde uma família mora de aluguel. É muito provável que a IMOBX comece por ele: uma família, antes de qualquer obra nova.',
        'Rafael has a flat in Guadalupe where a family rents today. It is most likely where IMOBX starts: one family, before anything new is built.',
        'Rafael heeft een appartement in Guadalupe waar nu een gezin huurt. Daar begint IMOBX hoogstwaarschijnlijk: één gezin, voordat er iets nieuws wordt gebouwd.')],
     [('roadmap.html#homes', T('Onde a primeira família vai morar', 'Where the first family will live', 'Waar het eerste gezin gaat wonen'))]),
    # WHA-05 (John)
    ('tour-rent', T('Dia de aluguel, com um tijolo seu', 'Rent day, with a brick of your own', 'Huurdag, met een eigen steen'),
     ('svg', 'bricks', T('Um exemplo, sem valores reais: a cada mês, uma parte do pagamento conta para a compra.', 'An example, with no real figures: each month, part of the payment counts towards the house.', 'Een voorbeeld, zonder echte bedragen: elke maand telt een deel van de betaling mee voor het huis.')),
     (T('O impacto social é o fato de ele poder ser dono do imóvel quanto mais pagar o aluguel.', 'The social impact is the fact that he can own the property the more that he pays rent.', 'De sociale impact is dat hij meer eigenaar van het huis wordt naarmate hij meer huur betaalt.'), JOHN),
     [T('Você paga todo mês como paga o aluguel hoje, e propomos que seja sem entrada. Parte de cada pagamento conta para comprar a casa. O preço, o pagamento e quanto conta ficam combinados por escrito antes de você se mudar.',
        'You pay each month as you pay rent today, and we propose no down payment. Part of every payment counts towards buying the house. The price, the payment and how much counts are agreed in writing before you move in.',
        'Je betaalt elke maand zoals je nu huur betaalt, en we stellen voor dat het zonder aanbetaling gaat. Een deel van elke betaling telt mee voor de aankoop van het huis. De prijs, de betaling en hoeveel meetelt worden schriftelijk afgesproken voordat je erin trekt.')],
     [('rent-to-own.html', T('Como funciona o aluguel com compra', 'How rent-to-own works', 'Zo werkt huurkoop'))]),
    # Family only. Register Q24 (Rafael): reminder, negotiation; the agreement sets the steps.
    ('tour-late', T('E se um mês ficar difícil?', 'What if a month gets hard?', 'Wat als een maand krap wordt?'), None, None,
     [T('Muita gente no Rio ganha por bico ou sem carteira assinada, e a renda muda de um mês para o outro. Se você atrasar, primeiro vem um lembrete e uma conversa para encontrar um caminho. O contrato diz cada passo por escrito, e também o que acontece com a parte que você já pagou.',
        'Many people in Rio earn from odd jobs or without a formal contract, and income changes from month to month. If you fall behind, first comes a reminder and a conversation to find a way through. The agreement sets out each step in writing, and what happens to the part you have already paid.',
        'Veel mensen in Rio verdienen met losse klussen of zonder vast contract, en hun inkomen verschilt per maand. Loop je achter, dan krijg je eerst een herinnering en een gesprek om samen een oplossing te vinden. De overeenkomst legt elke stap schriftelijk vast, en ook wat er gebeurt met het deel dat je al hebt betaald.')],
     [('rent-to-own.html#leaving', T('Atraso ou saída', 'Falling behind or leaving', 'Achterstand of vertrek'))]),
    # Owner only. HOW-04 (John); Q14 plot search; Superlogica default index, Rio state, Jul 2026 [read].
    ('tour-owner', T('Você tem um imóvel ou um terreno?', 'Do you have a house or land?', 'Heb je een huis of grond?'), None,
     (T('Depois, vamos olhar imóveis de outras pessoas que possam se juntar à nossa missão e visão.', 'Then we’ll look at secondary properties that can join our mission and vision.', 'Daarna kijken we naar woningen van anderen die zich bij onze missie en visie kunnen aansluiten.'), JOHN),
     [T('Agora, o Rafael procura um terreno de 200 a 300 m² em Anchieta, Pavuna, Bangu ou Santa Cruz. Mais adiante, quem tem uma casa poderá vendê-la a uma família pelo aluguel com compra, quando a IMOBX puder oferecer garantias e seguro.',
        'Right now, Rafael is looking for a plot of 200 to 300 m² in Anchieta, Pavuna, Bangu or Santa Cruz. Later, people who own a house will be able to sell it to a family through rent-to-own, once IMOBX can offer guarantees and insurance.',
        'Op dit moment zoekt Rafael een kavel van 200 tot 300 m² in Anchieta, Pavuna, Bangu of Santa Cruz. Later kunnen eigenaren hun huis via huurkoop aan een gezin verkopen, zodra IMOBX garanties en verzekering kan bieden.'),
      T('O atraso é a preocupação comum de quem aluga. Entre os aluguéis acompanhados pelo índice da Superlógica no estado do Rio, 3,68% estavam com mais de 60 dias de atraso em julho de 2026. No plano da IMOBX, cada atraso segue passos escritos no contrato.',
        'Late payment is an owner’s usual worry. Among rents tracked by the Superlógica index in Rio state, 3.68% were more than 60 days late in July 2026. In IMOBX’s plan, each late payment follows steps written into the agreement.',
        'Achterstand is de gewone zorg van een eigenaar. Van de huren die de Superlógica-index in de staat Rio volgt, was in juli 2026 3,68% meer dan 60 dagen te laat. In het plan van IMOBX volgt elke achterstand stappen die in de overeenkomst staan.')],
     [('contact.html?role=property#apresentacao', T('Escreva para nós', 'Write to us', 'Schrijf ons'))]),
    # HOW-10 (Rafael); Q4 (Olympus may be named); Q10 (index price)
    ('tour-builder', T('Por que construir, em vez de comprar?', 'Why build, instead of buying?', 'Waarom bouwen, in plaats van kopen?'),
     ('img', 'assets/property-1.jpg', 823, 581, T('Modelo 3D dos dois lofts', '3D model of the two lofts', '3D-model van de twee lofts'),
      T('Os lofts que a construtora do Rafael está construindo.', 'The lofts Rafael’s company is building.', 'De lofts die het bouwbedrijf van Rafael bouwt.')),
     (T('Os imóveis nos grandes centros são muito caros, por isso que devemos construir, ao invés de comprar pronto.', 'Properties in large centres are very expensive, which is why we should build, instead of buying ready-made.', 'Woningen in grote steden zijn erg duur, daarom moeten we bouwen in plaats van kant-en-klaar kopen.'), RAFAEL),
     [T('Rafael é engenheiro civil e tem a sua própria construtora, a Olympus. Os preços dela seguem o índice público de custo da construção do Rio (CUB). Depois do primeiro apartamento, o plano é construir cinco apartamentos de cada vez.',
        'Rafael is a civil engineer with his own construction company, Olympus. Its prices are tied to Rio’s public building-cost index (CUB). After the first flat, the plan is to build five flats at a time.',
        'Rafael is civiel ingenieur met een eigen bouwbedrijf, Olympus. Zijn prijzen volgen de openbare bouwkostenindex van Rio (CUB). Na het eerste appartement is het plan telkens vijf appartementen te bouwen.')],
     [('transparency.html', T('O que custa uma casa', 'What a house costs', 'Wat een huis kost'))]),
    # Professional only. ASK-03 (Rafael, his PT original); CUB-RJ R8-N Sep 2026 [read]; register Q5.
    ('tour-work', T('Trabalhar com a IMOBX', 'Working with IMOBX', 'Werken met IMOBX'), None,
     (T('Vou fechar parcerias com colegas de construção e fornecedores também.', 'I will form partnerships with construction colleagues and suppliers as well.', 'Ik ga ook samenwerken met collega’s uit de bouw en met leveranciers.'), RAFAEL),
     [T('Os preços da obra seguem o índice público de custo da construção do Rio, o CUB: R$ 2.476 por m² no padrão R8-N em setembro de 2026. No nosso plano, cada pagamento é aprovado por uma pessoa e conferido por outra antes de ser pago.',
        'Building prices follow Rio’s public building-cost index, the CUB: R$2,476 per m² for the R8-N standard in September 2026. In our plan, each payment is approved by one person and checked by another before it is paid.',
        'Bouwprijzen volgen de openbare bouwkostenindex van Rio, de CUB: R$ 2.476 per m² voor de R8-N-standaard in september 2026. In ons plan wordt elke betaling door één persoon goedgekeurd en door een ander gecontroleerd voordat ze wordt betaald.'),
      T('Buscamos um advogado independente, um contador e construtores para trabalhar com a gente nos primeiros apartamentos.',
        'We are looking for an independent lawyer, an accountant and builders to work with us on the first flats.',
        'We zoeken een onafhankelijke advocaat, een boekhouder en bouwers om met ons aan de eerste appartementen te werken.')],
     [('transparency.html', T('O que custa uma casa', 'What a house costs', 'Wat een huis kost'))]),
    # VIS-03 (John); the village as Rafael planned it (roadmap)
    ('tour-village', T('A vila que queremos', 'The village we want', 'Het dorp dat we willen'),
     ('img', 'assets/homepage.jpg', 1024, 765, T('Ilustração conceitual da primeira vila', 'Concept illustration of the first village', 'Conceptillustratie van het eerste dorp'),
      T('A ideia do Rafael para uma vila mais adiante, desenhada com um gerador de imagens.', 'Rafael’s idea for a later village, drawn with an image generator.', 'Rafaels idee voor een later dorp, gemaakt met een beeldgenerator.')),
     (T('Agora estamos todos fragmentados, mas tenho certeza de que, aos poucos, podemos crescer em comunidades pequenas, mas mais fortes e resilientes.', 'We are now all fragmented, but I am sure that slowly we can grow into small but stronger and resilient communities.', 'We zijn nu allemaal versnipperd, maar ik weet zeker dat we langzaam kunnen uitgroeien tot kleine maar sterkere en veerkrachtige gemeenschappen.'), JOHN),
     [T('No plano do Rafael, casas de 45 m² ficam em volta de um pátio comum, para os pais verem os filhos brincando, com um pomar, energia solar nos telhados e salas para estudar. É uma etapa posterior; primeiro vêm cinco apartamentos de cada vez.',
        'In Rafael’s plan, 45 m² houses stand around a shared courtyard, so parents can see their children play, with an orchard, solar panels on the roofs and rooms to study in. It is a later stage; first come five flats at a time.',
        'In het plan van Rafael staan huizen van 45 m² rond een gedeelde binnenplaats, zodat ouders hun kinderen zien spelen, met een boomgaard, zonnepanelen op de daken en ruimtes om te studeren. Dat is een latere fase; eerst komen telkens vijf appartementen.')],
     [('roadmap.html#village', T('Veja a vila mais adiante', 'See the later village', 'Bekijk het latere dorp'))]),
    # HOW-13 (John); governance page (cooperative, vote protection)
    ('tour-courtyard', T('Quem decide?', 'Who decides?', 'Wie beslist?'),
     ('svg', 'courtyard', T('À esquerda: um membro, um voto. À direita: o contrato da família, que só muda com a família e a IMOBX de acordo.', 'Left: one member, one vote. Right: the family’s agreement, which changes only when the family and IMOBX agree.', 'Links: één lid, één stem. Rechts: de overeenkomst van het gezin, die alleen verandert als gezin en IMOBX akkoord zijn.')),
     (T('Não dá para chegar à autossuficiência ou a comunidades integradas sem uma boa organização por trás.', 'You cannot reach self-sufficiency or integrated communities without proper organisation backing it.', 'Je bereikt geen zelfvoorziening of hechte gemeenschappen zonder een goede organisatie erachter.'), JOHN),
     [T('Planejamos fundar a IMOBX como uma cooperativa habitacional: os membros são donos dela e a administram juntos, com um voto cada. Nenhuma votação pode mudar o contrato de moradia de uma família: ele só muda quando a família e a IMOBX concordam, dentro da lei brasileira.',
        'We plan to found IMOBX as a housing cooperative: its members own it and run it together, with one vote each. No vote can change a family’s housing agreement: it changes only when the family and IMOBX both agree, under Brazilian law.',
        'We willen IMOBX oprichten als wooncoöperatie: de leden bezitten en besturen haar samen, met elk één stem. Geen stemming kan de woonovereenkomst van een gezin veranderen: die verandert alleen als het gezin en IMOBX het allebei eens zijn, binnen de Braziliaanse wet.')],
     [('governance.html#cooperative', T('Por que uma cooperativa', 'Why a cooperative', 'Waarom een coöperatie'))]),
    # Owner-approved ledger lead (28 Oct)
    ('tour-books', T('Para onde vão os recursos dos vizinhos?', 'Where does the neighbours’ funding go?', 'Waar gaat de financiering van de buren heen?'),
     ('svg', 'repair', T('1 O pedido · 2 aprovado e conferido · 3 pago e publicado no livro aberto.', '1 The request · 2 approved and checked · 3 paid and published in the open book.', '1 Het verzoek · 2 goedgekeurd en gecontroleerd · 3 betaald en gepubliceerd in het open boek.')), None,
     [T('Quando vizinhos juntam recursos para construir casas, a primeira pergunta é sempre: para onde vai isso? A IMOBX quer que a resposta fique aberta a todos.',
        'When neighbours pool funding for houses, the first question is always: where does it go? IMOBX wants the answer open to everyone.',
        'Als buren samen financiering inleggen voor huizen, is de eerste vraag altijd: waar gaat het heen? IMOBX wil dat het antwoord voor iedereen open ligt.'),
      T('Veja um reparo. Uma pessoa aprova o serviço e outra confere. Só então ele é pago. No nosso plano, cada pagamento entra num livro de contas aberto com o nome de quem aprovou. Os contratos e os dados pessoais ficam privados.',
        'Take a repair. One person approves the work and another checks it. Only then is it paid. In our plan, each payment goes into an open book with the name of who approved it. Contracts and personal data stay private.',
        'Neem een reparatie. Eén persoon keurt het werk goed en een ander controleert het. Pas dan wordt het betaald. In ons plan komt elke betaling in een open boek met de naam van wie die goedkeurde. Contracten en persoonsgegevens blijven privé.')],
     [('blockchain.html', T('Como funcionam as contas abertas', 'How the open books work', 'Hoe de open boeken werken'))]),
    # TOKEN_POSITION (approved lines, 41c)
    ('tour-token', T('Para os curiosos: o token', 'For the curious: the token', 'Voor de nieuwsgierigen: de token'),
     ('svg', 'token', T('1 Alguém negocia o token · 2 a negociação paga uma taxa · 3 a taxa paga trabalho e novas casas · 4 o projeto cresce com o que ele mesmo gera, e o ciclo recomeça.', '1 Someone trades the token · 2 the trade pays a fee · 3 the fee pays for work and new houses · 4 the project grows from what it earns, and the cycle starts again.', '1 Iemand verhandelt de token · 2 de transactie betaalt een vergoeding · 3 die betaalt werk en nieuwe huizen · 4 het project groeit met wat het zelf verdient, en de cirkel begint opnieuw.')), None,
     [T('Mais adiante, a IMOBX também planeja um token self-compounding de financiamento da comunidade. Ter o token é opcional, e as famílias não precisam dele. A primeira casa é financiada à parte.',
        'Later on, IMOBX also plans a self-compounding community-funding token. Holding it is optional, and families don’t need it. The first house is funded separately.',
        'Later wil IMOBX ook een self-compounding token uitgeven die de gemeenschap financiert. Een token hebben is vrijwillig, en gezinnen hebben het niet nodig. Het eerste huis wordt apart gefinancierd.')],
     [('token.html', T('Como o token funciona', 'How the token works', 'Hoe de token werkt'))]),
    # Funder (and professional). Funding order from the roadmap (owner, 9 Nov); SDG 11.1 measures [read].
    ('tour-funding', T('Como as primeiras casas serão financiadas?', 'How will the first houses be funded?', 'Hoe worden de eerste huizen gefinancierd?'), None, None,
     [T('Primeiro, uma campanha de financiamento coletivo em reais, assim que a cooperativa estiver registrada. Depois, financiamento ligado ao Objetivo de Desenvolvimento Sustentável 11 da ONU, sobre cidades e comunidades sustentáveis. Quem assumir a nossa nova vaga de captação vai pesquisar os outros caminhos.',
        'First, a crowdfunding campaign in reais, once the cooperative is registered. Then, funding linked to UN Sustainable Development Goal 11, on sustainable cities and communities. The person in our new fundraising role will research the other routes.',
        'Eerst een crowdfundingcampagne in reais, zodra de coöperatie is ingeschreven. Daarna financiering via Duurzame Ontwikkelingsdoelstelling 11 van de VN, over duurzame steden en gemeenschappen. Wie onze nieuwe functie voor fondsenwerving invult, onderzoekt de andere routes.'),
      T('Os cinco primeiros apartamentos podem mostrar o que muda: quem passou a morar ali, o aluguel antes e depois, e a segurança de ficar na casa.',
        'The first five flats can show what changes: who moved in, their rent before and after, and how secure their right to stay is.',
        'De eerste vijf appartementen kunnen laten zien wat er verandert: wie er kwam wonen, de huur ervoor en erna, en hoe zeker hun recht op wonen is.')],
     [('roadmap.html#funding', T('O plano de financiamento', 'The funding plan', 'Het financieringsplan')), ('jobs.html', T('A vaga de captação', 'The fundraising role', 'De functie voor fondsenwerving'))]),
    # HOW-02 (John), HOW-12 (John), WHA-15 (Rafael)
    ('tour-grow', T('Como a IMOBX cresce?', 'How does IMOBX grow?', 'Hoe groeit IMOBX?'), None,
     (T('Primeiro trabalhamos com provas. E provas geram confiança. E com confiança, dá para atrair mais recursos e crescer.', 'First we work with proof. And proof builds trust. And with trust, you can draw in more funding and scale.', 'Eerst werken we met bewijs. Bewijs schept vertrouwen. En met vertrouwen trek je meer middelen aan en kun je groeien.'), JOHN),
     [T('Primeiro uma família, depois cinco apartamentos de cada vez, depois proprietários que queiram entrar com as suas casas.',
        'One family first, then five flats at a time, then owners who want to bring in their own houses.',
        'Eerst één gezin, dan telkens vijf appartementen, dan eigenaren die hun eigen huis willen inbrengen.')],
     [('roadmap.html#stages', T('Onde estamos e o que vem depois', 'Where we are and what comes next', 'Waar we staan en wat er komt'))]),
    # Rafael's cave question (his Q1 story, OK'd 8 Nov); John's lines (About page)
    ('tour-people', T('Quem começou a IMOBX, e por quê?', 'Who started IMOBX, and why?', 'Wie begon IMOBX, en waarom?'), None,
     [(T('Quando a vida aperta, a primeira coisa que queremos é entrar na nossa caverna e nos proteger. Por que ter a própria caverna não é um direito de todos? A IMOBX é a minha resposta a essa pergunta.', 'When life gets hard, the first thing we want is to go into our cave and protect ourselves. Why isn’t having one’s own cave a right for everyone? IMOBX is my answer to that question.', 'Als het leven zwaar wordt, willen we eerst onze grot in om ons te beschermen. Waarom is een eigen grot geen recht voor iedereen? IMOBX is mijn antwoord op die vraag.'), RAFAEL),
      (T('Desde 2005, procuro formas para que as comunidades compartilhem o que pertence a todos. A proposta da IMOBX leva essa ideia de compartilhar à moradia.', 'Since 2005, I have looked for ways for communities to share what they hold in common. The IMOBX proposal brings that idea of sharing to housing.', 'Sinds 2005 zoek ik naar manieren waarop gemeenschappen delen wat van hen allemaal is. Het voorstel van IMOBX brengt dat idee van delen naar het wonen.'), JOHN)],
     [],
     [('about.html', T('Sobre a IMOBX', 'About IMOBX', 'Over IMOBX')), ('resources.html', T('Documentos e fontes', 'Documents and sources', 'Documenten en bronnen')), ('commons-research.html', T('A pesquisa sobre propriedade compartilhada', 'The research on shared ownership', 'Het onderzoek naar gedeeld eigendom'))]),
    # ASK-01 (John)
    ('tour-join', T('Sua vez', 'Your turn', 'Jouw beurt'), None,
     (T('Qualquer pessoa que tenha uma visão parecida com a nossa, entenda o problema e tenha os meios ou a dedicação para resolvê-lo. É esse o tipo de pessoa que queremos atrair.', 'Whatever person has a very similar kind of vision to ours, understands the problem, and has the means or dedication to solve it. That’s the type of people we’re trying to attract.', 'Iedereen die een visie heeft die op de onze lijkt, het probleem begrijpt en de middelen of de toewijding heeft om het op te lossen. Dat is het soort mensen dat we willen aantrekken.'), JOHN),
     [T('A IMOBX está em preparação. Buscamos a primeira família, a primeira casa e as pessoas que vão fundar a cooperativa com a gente.',
        'IMOBX is in preparation. We are looking for the first family, the first house and the people who will found the cooperative with us.',
        'IMOBX is in voorbereiding. We zoeken het eerste gezin, het eerste huis en de mensen die de coöperatie met ons oprichten.')],
     [('contact.html#apresentacao', T('Apresente-se', 'Introduce yourself', 'Stel jezelf voor'), 'tour-cta'), ('jobs.html', T('Ver a vaga', 'See the open role', 'Bekijk de vacature'), 'tour-jobs')]),
]


# Owner, 9 Nov: each visitor gets its own journey (evidence: 02-research-housing-and-commons/VISITOR_NEEDS_EVIDENCE_2026-11-09.md).
FOR = {
    'tour-tenant': 'resident property funding',
    'tour-rent': 'resident funding',
    'tour-late': 'resident',
    'tour-owner': 'property',
    'tour-builder': 'professional property funding',
    'tour-work': 'professional',
    'tour-village': 'resident funding',
    'tour-courtyard': 'resident property funding',
    'tour-token': 'funding',
    'tour-funding': 'funding professional',
    'tour-grow': 'funding property professional',
}


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


def _quote(q):
    if not q:
        return ''
    out = ''
    for text, who in (q if isinstance(q, list) else [q]):
        quoted = tuple(f'“{x}”' for x in text)
        out += '<blockquote class="tour-quote">' + _text('p', quoted) + _text('cite', who) + '</blockquote>'
    return out


def build_tour(root, page, version):
    body = '<main class="paper guide-paper tour-page" id="main">' + _text('h1', T('Conheça a IMOBX', 'Take a tour of IMOBX', 'Ontdek IMOBX'))
    for ident, heading, visual, quote, paragraphs, links in STEPS:
        roles = f' data-tour-for="{FOR[ident]}"' if ident in FOR else ''
        body += f'<section data-tour-step id="{ident}"{roles}>' + _text('h2', heading) + _visual(visual) + _quote(quote)
        body += ''.join(_text('p', x) for x in paragraphs)
        if links == 'roles':
            body += '<ul class="tour-roles">' + ''.join(
                '<li>' + _text('a', label, f'href="contact.html?role={rid}#apresentacao" data-tour-role="{rid}" class="tour-role"') + '</li>' for rid, label in ROLES) + '</ul>'
        else:
            body += '<p class="tour-links">' + ' '.join(
                _text('a', l[1], f'href="{escape(l[0], quote=True)}"' + (f' class="{l[2]}"' if len(l) > 2 else '')) for l in links) + '</p>'
        if ident == 'tour-join':
            body += '<div data-tour-contact-page></div>'
        body += '</section>'
    body += '</main>'
    (root / 'tour.html').write_text(page('IMOBX | Take a tour', body, '<link rel="stylesheet" href="assets/tour.css"><link rel="stylesheet" href="assets/tour-contact.css"><script src="assets/tour-contact.js" defer></script>', version=version,
                                         lang='pt-BR', title_pt='IMOBX | Conheça a IMOBX'), encoding='utf-8')
