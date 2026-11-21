"""The IMOBX tour: ten chapters that walk through the whole site (owner, 9 Nov: "compelling ... it should reference all the pages
... explain the technical background in a very illustrative way, that's fun to read").

Each chapter has one picture or small drawing, two or three plain sentences and a link to the page it is about. Chapter 1 asks
who the visitor is; the answer decides where the last button leads (contact.html?role=...). The page works on its own,
without JavaScript: the role choices are links and every chapter is readable in order.
"""
from html import escape

from page_frame import term_scripts

NL = {}  # English -> Dutch, merged into i18n/nl.json by the build step below


def T(pt, en, nl):
    NL[en] = nl
    return (pt, en, nl)


def S(url, label, note=None):
    """A source note after a figure: 'Source: <link>. <what the figure measures>'. Plain parts, so the dialog on the home page can update each one."""
    return ('source', url, label, note)


def _paragraph(item):
    if len(item) == 4 and item[0] == 'source':
        _, url, label, note = item
        out = '<p class="source-note">' + _text('span', T('Fonte: ', 'Source: ', 'Bron: ')) + _text('a', label, f'href="{escape(url, quote=True)}"') + '&#8288;.'
        if note:
            out += ' ' + _text('span', note)
        return out + '</p>'
    return _text('p', item)


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
        r = f'<rect x="{x}" y="{y}" width="32" height="32" fill="{TEAL if i < 5 else "#fff"}" stroke="{TEAL}" stroke-width="3"/>'
        cells += _g(round(i * 0.7 + 1, 2), r) if i < 5 else r
    return (f'<svg viewBox="0 0 520 220" role="img" aria-hidden="true"><rect width="520" height="220" fill="{PALE}"/>'
            f'<polygon points="118,104 260,30 402,104" fill="{ORANGE}"/><rect x="118" y="104" width="284" height="100" fill="#fff" stroke="{INK}" stroke-width="4"/>'
            + cells + '</svg>')


def svg_repair():
    """1 request, 2 approved and checked, 3 paid and recorded (the open-book drawing is the ledger). Lights up in order."""
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
         ('funding', T('Parceiro ou financiador', 'A partner or funder', 'Partner of financier')),
         ('visitor', T('Só estou conhecendo', 'Just visiting', 'Ik kijk even rond'))]

JOHN = T('John, cofundador', 'John, co-founder', 'John, medeoprichter')
RAFAEL = T('Rafael, cofundador', 'Rafael, co-founder', 'Rafael, medeoprichter')

# Owner, 9 Nov: "did you just use your own generator to write the text?" Rebuilt with human-copy and Humanizer from
# the founders' own words (SOURCE_WORDS_FOUNDERS_2026-10-27.md; ids in the comments). Each chapter opens differently.
# Chapter: (id, heading, visual, quote, paragraphs, links). quote = (text, who) or None.
STEPS = [
    ('tour-who', T('Quem é você?', 'Who are you?', 'Wie ben je?'), None, None,
     [T('Escolha o que mais combina, e o passeio mostra o que importa para você.', 'Pick the closest one, and the tour shows what matters to you.', 'Kies wat het best past, en de rondleiding laat zien wat voor jou telt.')], 'roles'),
    # WHY-01 (owner's approved landing line)
    ('tour-home', T('Um lugar para chamar de lar', 'A place to call home', 'Een plek om je thuis te voelen'), None,
     (T('Construir um lar é uma busca existencial de todo ser humano, onde quer que esteja.', 'Creating a home is an existential quest for every human, wherever you are.', 'Een thuis creëren is een existentiële zoektocht voor ieder mens, waar je ook bent.'), JOHN),
     [T('A IMOBX vai ajudar famílias do Rio de Janeiro a alugar um apartamento e a comprá-lo aos poucos, por meio de uma cooperativa habitacional administrada pelos próprios moradores.',
        'IMOBX will help families in Rio de Janeiro rent a flat and slowly buy it, through a housing cooperative the residents run together.',
        'IMOBX helpt gezinnen in Rio de Janeiro een appartement te huren en het geleidelijk te kopen, via een wooncoöperatie die de bewoners samen besturen.')],
     [('about.html', T('Por que a IMOBX existe', 'Why IMOBX exists', 'Waarom IMOBX bestaat'))]),
    # SIT-13 as the heading (John); SIT-06 (Rafael)
    ('tour-why', T('Proprietários não conseguem vender. Sonhadores não conseguem comprar.', 'Owners can’t sell. Dreamers can’t buy.', 'Eigenaren kunnen niet verkopen. Dromers kunnen niet kopen.'),
     ('img', 'assets/community-bay-circles.jpg', 1448, 1086, T('Favelas nos morros ao redor da baía, marcadas com círculos', 'Favelas on the hillsides around the bay, marked with circles', 'Favela’s op de hellingen rond de baai, gemarkeerd met cirkels'),
      T('Os círculos marcam favelas nos morros.', 'The circles mark favelas on the hillsides.', 'De cirkels geven favela’s op de hellingen aan.')),
     (T('O absurdo do Brasil não é o preço dos imóveis, é a taxa de juros.', 'The absurdity in Brazil is not the price of real estate, it is the interest rate.', 'Het absurde in Brazilië is niet de prijs van vastgoed, maar de rente.'), RAFAEL),
     [T('Os preços pedidos nos aluguéis sobem mais rápido que a inflação, e milhões de famílias pagam aluguel por anos sem chegar mais perto da casa própria.',
        'Asking rents are rising faster than inflation, and millions of families pay rent for years without getting closer to owning a home.',
        'De gevraagde huurprijzen stijgen sneller dan de inflatie, en miljoenen gezinnen betalen jarenlang huur zonder dichter bij een eigen woning te komen.')],
     [('why.html', T('Leia os números', 'Read the numbers', 'Lees de cijfers'))]),
    ('tour-tenant', T('Um apartamento para começar', 'A flat to start with', 'Een appartement om mee te beginnen'), None, None,
     [T('Uma família já aluga um apartamento no prédio de Guadalupe que a Olympus, a construtora do Rafael, construiu.',
        'A family already rents a flat in the Guadalupe building that Olympus, Rafael’s company, built.',
        'Een gezin huurt al een appartement in het gebouw in Guadalupe dat Olympus, het bouwbedrijf van Rafael, heeft gebouwd.')],
     [('project-development.html#homes', T('Onde a primeira família vai morar', 'Where the first family will live', 'Waar het eerste gezin gaat wonen'))]),
    # WHA-05 (John)
    ('tour-rent', T('O que acontece no dia do aluguel?', 'What happens on rent day?', 'Wat gebeurt er op huurdag?'),
     ('svg', 'bricks', T('A cada mês, uma parte do pagamento preenche mais um tijolo do apartamento.', 'Each month, part of the payment fills one more brick of the flat.', 'Elke maand vult een deel van de betaling weer een steen van het appartement.')),
     (T('O impacto social é o fato de ele poder ser dono do imóvel quanto mais pagar o aluguel.', 'The social impact is the fact that he can own the property the more that he pays rent.', 'De sociale impact is dat hij meer eigenaar van het huis wordt naarmate hij meer huur betaalt.'), JOHN),
     [T('O plano é começar sem entrada. Todo mês você paga como paga o aluguel hoje, e parte de cada pagamento vai para o apartamento. Antes de você se mudar, o preço, o pagamento mensal e a parte que vai para o apartamento são combinados e escritos. O apartamento passa para o seu nome quando as condições do seu contrato forem cumpridas.',
        'The plan is to start with no down payment. Each month you pay as you pay rent today, and part of every payment goes towards the flat. Before you move in, the price, the monthly payment and the share that goes towards the flat are agreed and written down. The flat goes into your name when the conditions in your agreement are met.',
        'Het plan is om zonder aanbetaling te beginnen. Elke maand betaal je zoals je nu huur betaalt, en een deel van elke betaling gaat naar het appartement. Voordat je erin trekt, worden de prijs, de maandelijkse betaling en het deel dat naar het appartement gaat afgesproken en opgeschreven. Het appartement komt op jouw naam zodra aan de voorwaarden in jouw overeenkomst is voldaan.')],
     [('rent-to-own.html', T('Como funciona o aluguel com compra', 'How rent-to-own works', 'Zo werkt huurkoop')),
      ('project-development.html#terms', T('Termos e leis', 'Terms and law', 'Voorwaarden en wet'))]),
    # Family only. Register Q24 (Rafael): reminder, negotiation; the agreement sets the steps.
    ('tour-late', T('E se um mês ficar difícil?', 'What if a month gets hard?', 'Wat als een maand krap wordt?'), None, None,
     [T('Muita gente no Rio ganha por bico ou sem carteira assinada, e a renda muda de um mês para o outro. Se você atrasar, pretendemos começar com um lembrete e uma conversa para encontrar um caminho, e escrever cada passo seguinte no contrato.',
        'Many people in Rio earn from odd jobs or without a formal contract, and income changes from month to month. If you fall behind, we aim to begin with a reminder and a conversation to find a way through, and to write every later step into the agreement.',
        'Veel mensen in Rio verdienen met losse klussen of zonder vast contract, en hun inkomen verschilt per maand. Loop je achter, dan willen we beginnen met een herinnering en een gesprek om samen een oplossing te vinden, en elke volgende stap in de overeenkomst vastleggen.')],
     [('rent-to-own.html#leaving', T('Saída ou atraso no pagamento', 'Leaving or missed payments', 'Vertrek of gemiste betaling'))]),
    # Owner only. HOW-04 (John); Q14 plot search; Superlogica default index, Rio state, Jul 2026 [read].
    ('tour-owner', T('Você tem um imóvel ou um terreno?', 'Do you have a house or land?', 'Heb je een huis of grond?'), None,
     None,
     [T('Os cinco primeiros apartamentos novos precisam de um terreno de 200 a 300 m² em Anchieta, Pavuna, Bangu ou Santa Cruz. Mais adiante, se a IMOBX puder oferecer garantias e seguro, quem tem uma casa poderá vendê-la a uma família pelo aluguel com compra.',
        'The first five new flats need a plot of 200 to 300 m² in Anchieta, Pavuna, Bangu or Santa Cruz. Later, if IMOBX can offer guarantees and insurance, people who own a house can sell it to a family through rent-to-own.',
        'De eerste vijf nieuwe appartementen hebben een kavel van 200 tot 300 m² nodig in Anchieta, Pavuna, Bangu of Santa Cruz. Later kunnen eigenaren hun huis via huurkoop aan een gezin verkopen, als IMOBX garanties en verzekering kan bieden.'),
      T('O atraso no pagamento preocupa muitos proprietários que alugam um imóvel: em julho de 2026, 3,68% dos aluguéis acompanhados pelo índice da Superlógica no estado do Rio estavam com mais de 60 dias de atraso. O plano: cada atraso segue passos escritos no contrato.',
        'Late payment worries many owners who rent out a home: in July 2026, 3.68% of the rents tracked by the Superlógica index in Rio state were more than 60 days late. The plan: each late payment follows steps written into the agreement.',
        'Veel verhuurders maken zich zorgen over huurachterstand: in juli 2026 was 3,68% van de huren die de Superlógica-index in de staat Rio volgt meer dan 60 dagen te laat. Het plan: elke achterstand volgt stappen die in de overeenkomst staan.'),
      S('https://diariodorio.com/economia/mercado-imobiliario/2026/08/29/inadimplencia-de-aluguel-no-rio-melhora-em-2026-e-atinge-minima-historica.html',
        T('Índice de inadimplência de aluguel da Superlógica, via Diário do Rio', 'Superlógica rental default index, via Diário do Rio', 'Superlógica-index voor huurachterstand, via Diário do Rio'),
        T('Cobre contratos administrados com o software da Superlógica, não todos os aluguéis do estado.', 'It covers contracts managed with Superlógica’s software, not every rental in the state.', 'De index dekt contracten die met de software van Superlógica worden beheerd, niet elke huur in de staat.'))],
     [('contact.html?role=property#apresentacao', T('Escreva para nós', 'Write to us', 'Schrijf ons'))]),
    # HOW-10 (Rafael); Q4 (Olympus may be named); Q10 (index price)
    ('tour-builder', T('Por que construir, em vez de comprar?', 'Why build, instead of buying?', 'Waarom bouwen, in plaats van kopen?'),
     ('img', 'assets/property-1.jpg', 823, 581, T('Modelo 3D dos dois lofts', '3D model of the two lofts', '3D-model van de twee lofts'),
      T('Um modelo 3D dos dois lofts que a construtora do Rafael tem contrato para construir.', 'A 3D model of the two lofts that Rafael’s company has a contract to build.', 'Een 3D-model van de twee lofts waarvoor het bouwbedrijf van Rafael een bouwcontract heeft.')),
     (T('Os imóveis nos grandes centros são muito caros, por isso que devemos construir, ao invés de comprar pronto.', 'Properties in large centres are very expensive, which is why we should build, instead of buying ready-made.', 'Woningen in grote steden zijn erg duur, daarom moeten we bouwen in plaats van kant-en-klaar kopen.'), RAFAEL),
     [T('O Rafael é engenheiro civil e tem a sua própria construtora, a Olympus. Depois do apartamento de Guadalupe, pretendemos construir cinco apartamentos novos de cada vez.',
        'Rafael is a civil engineer with his own construction company, Olympus. After the Guadalupe flat, we plan to build five new flats at a time.',
        'Rafael is civiel ingenieur met een eigen bouwbedrijf, Olympus. Na het appartement in Guadalupe willen we telkens vijf nieuwe appartementen bouwen.')],
     [('costs-and-funding.html', T('O que custa um apartamento', 'What a flat costs', 'Wat een appartement kost'))]),
    # Professional only. ASK-03 (Rafael, his PT original); CUB-RJ R8-N Sep 2026 [read]; register Q5.
    ('tour-work', T('Quem constrói e quem confere', 'Who builds, and who checks', 'Wie bouwt en wie controleert'), None,
     (T('Vou fechar parcerias com colegas de construção e fornecedores também.', 'I will form partnerships with construction colleagues and suppliers as well.', 'Ik ga ook samenwerken met collega’s uit de bouw en met leveranciers.'), RAFAEL),
     [T('A estimativa do Rafael parte do CUB, o índice público de custo da construção do Rio, e soma 35% para despesas gerais e para a margem da construtora dele.',
        'Rafael’s estimate starts from Rio’s public building-cost index, the CUB, and adds 35% for overheads and his company’s margin.',
        'De schatting van Rafael gaat uit van de CUB, de openbare bouwkostenindex van Rio, en telt er 35% bij voor algemene kosten en de marge van zijn bedrijf.'),
      T('Um advogado, um contador e um engenheiro independentes vão conferir os contratos e a obra dos primeiros apartamentos.',
        'An independent lawyer, accountant and engineer will check the contracts and the building work on the first flats.',
        'Een onafhankelijke advocaat, boekhouder en ingenieur controleren de contracten en de bouw van de eerste appartementen.')],
     [('costs-and-funding.html', T('O que custa um apartamento', 'What a flat costs', 'Wat een appartement kost'))]),
    # VIS-03 (John); the village as Rafael planned it (roadmap)
    ('tour-village', T('A vila que queremos', 'The village we want', 'Het dorp dat we willen'),
     ('img', 'assets/homepage.jpg', 1024, 765, T('Ilustração conceitual da vila que imaginamos', 'Concept illustration of the village we imagine', 'Conceptillustratie van het dorp dat we ons voorstellen'), None),
     (T('Agora estamos todos fragmentados, mas tenho certeza de que, aos poucos, podemos crescer em comunidades pequenas, mas mais fortes e resilientes.', 'We are now all fragmented, but I am sure that slowly we can grow into small but stronger and resilient communities.', 'We zijn nu allemaal versnipperd, maar ik weet zeker dat we langzaam kunnen uitgroeien tot kleine maar sterkere en veerkrachtige gemeenschappen.'), JOHN),
     [T('No desenho do Rafael, pequenos prédios com apartamentos de 45 m² ficam em volta de um pátio comum, para os pais verem os filhos brincando, com um pomar, energia solar nos telhados e salas para estudar. Ele vem depois dos cinco primeiros apartamentos.',
        'Rafael’s design has small blocks of 45 m² flats around a shared courtyard, so parents can see their children play, with an orchard, solar panels on the roofs and rooms to study in. It comes after the first five flats.',
        'In het ontwerp van Rafael staan kleine gebouwen met appartementen van 45 m² rond een gedeelde binnenplaats, zodat ouders hun kinderen zien spelen, met een boomgaard, zonnepanelen op de daken en ruimtes om te studeren. Het komt na de eerste vijf appartementen.')],
     [('project-development.html#village', T('Veja a vila mais adiante', 'See the later village', 'Bekijk het latere dorp'))]),
    # HOW-13 (John); governance page (cooperative, vote protection)
    ('tour-courtyard', T('Quem decide?', 'Who decides?', 'Wie beslist?'),
     ('svg', 'courtyard', T('À esquerda: um membro, um voto. À direita: o contrato da família, que só muda com a família e a IMOBX de acordo.', 'Left: one member, one vote. Right: the family’s agreement, which changes only when the family and IMOBX agree.', 'Links: één lid, één stem. Rechts: de overeenkomst van het gezin, die alleen verandert als gezin en IMOBX akkoord zijn.')),
     (T('Não dá para chegar à autossuficiência ou a comunidades integradas sem uma boa organização por trás.', 'You cannot reach self-sufficiency or integrated communities without proper organisation backing it.', 'Je bereikt geen zelfvoorziening of hechte gemeenschappen zonder een goede organisatie erachter.'), JOHN),
     [T('A IMOBX será uma cooperativa habitacional. Os membros vão ser donos dela e vão administrá-la juntos, com um voto cada. O contrato de cada família tem proteção à parte, como explicam Termos e leis.',
        'IMOBX will be a housing cooperative. Its members will own it and run it together, with one vote each. A family’s own agreement is protected separately, as Terms and law explains.',
        'IMOBX wordt een wooncoöperatie. De leden worden eigenaar en besturen haar samen, met elk één stem. De woonovereenkomst van een gezin verandert alleen als het gezin en IMOBX het allebei eens zijn.')],
     [('governance.html#cooperative', T('Por que uma cooperativa', 'Why a cooperative', 'Waarom een coöperatie'))]),
    # Owner-approved ledger lead (28 Oct)
    ('tour-books', T('Para onde vão os recursos dos vizinhos?', 'Where does the neighbours’ funding go?', 'Waar gaat de financiering van de buren heen?'),
     ('svg', 'repair', T('1 O pedido; 2 aprovado e conferido; 3 pago e anotado.', '1 The request; 2 approved and checked; 3 paid and written down.', '1 Het verzoek; 2 goedgekeurd en gecontroleerd; 3 betaald en genoteerd.')), None,
     [T('Quando vizinhos juntam recursos para construir apartamentos, querem ver para onde eles vão. Queremos um registro distribuído que qualquer pessoa possa ler, com cada pagamento e a função de quem o aprovou. Os contratos e os dados pessoais das famílias ficam privados.',
        'When neighbours pool funding for flats, they want to see where it goes. We want a ledger that anyone can read, showing each payment and the role that approved it. Families’ contracts and personal details stay private.',
        'Als buren samen financiering inleggen voor appartementen, willen ze zien waar die naartoe gaat. We willen een distributed ledger die iedereen kan lezen, met elke betaling en de rol van wie haar goedkeurde. De contracten en persoonsgegevens van gezinnen blijven privé.')],
     [('distributed-ledger.html', T('Como o registro distribuído funcionaria', 'How the ledger would work', 'Hoe de distributed ledger zou werken')),
      ('governance.html#now', T('Quem aprova e quem confere', 'Who approves and who checks', 'Wie goedkeurt en wie controleert'))]),
    # TOKEN_POSITION (approved lines, 41c)
    ('tour-token', T('Para os curiosos: o token', 'For the curious: the token', 'Voor de nieuwsgierigen: het token'),
     ('svg', 'token', T('1 Alguém negocia o token; 2 a negociação paga uma taxa; 3 a taxa paga trabalho e novos apartamentos; 4 o projeto cresce com o que ele mesmo gera, e o ciclo recomeça.', '1 Someone trades the token; 2 the trade pays a fee; 3 the fee pays for work and new flats; 4 the project grows from what it earns, and the cycle starts again.', '1 Iemand verhandelt het token; 2 de transactie betaalt een vergoeding; 3 die betaalt werk en nieuwe appartementen; 4 het project groeit met wat het zelf verdient, en de cirkel begint opnieuw.')), None,
     [T('Mais adiante, a IMOBX também planeja um token de financiamento comunitário, em que o que entra no projeto volta a ser usado. Os apartamentos novos são financiados à parte, a começar por uma campanha de financiamento coletivo.',
        'Later on, IMOBX also plans a self-compounding community-funding token. The new flats are funded separately, starting with a crowdfunding campaign.',
        'Later wil IMOBX ook een self-compounding token uitgeven dat de gemeenschap financiert. De nieuwe appartementen worden apart gefinancierd, te beginnen met een crowdfundingcampagne.')],
     [('self-compounding.html', T('Como o token funciona', 'How the token works', 'Hoe het token werkt'))]),
    # Funder (and professional). Funding order from the roadmap (owner, 9 Nov); SDG 11.1 measures [read].
    ('tour-funding', T('Como os primeiros apartamentos serão financiados?', 'How will the first flats be funded?', 'Hoe worden de eerste appartementen gefinancierd?'), None, None,
     [T('A obra começa a ser financiada por uma campanha de financiamento coletivo em reais, assim que a cooperativa estiver registrada. Depois vem financiamento ligado ao Objetivo de Desenvolvimento Sustentável 11 da ONU, sobre cidades e comunidades sustentáveis.',
        'The building is funded first by a crowdfunding campaign in reais, once the cooperative is registered. Funding linked to UN Sustainable Development Goal 11, on sustainable cities and communities, follows.',
        'De bouw wordt eerst gefinancierd met een crowdfundingcampagne in reais, zodra de coöperatie is ingeschreven. Daarna volgt financiering via Duurzame Ontwikkelingsdoelstelling 11 van de VN, over duurzame steden en gemeenschappen.'),
      T('Quem financia deve poder acompanhar, em relatórios publicados, o que os cinco primeiros apartamentos mudam: quantas famílias se mudaram, o aluguel antes e depois, e a segurança do direito de cada família de continuar morando ali. Nomes e contratos ficam privados.',
        'Funders should be able to follow, in published reports, what the first five flats change: how many families moved in, the rent before and after, and how secure each family’s right to stay is. Names and contracts stay private.',
        'Financiers moeten in gepubliceerde rapporten kunnen volgen wat de eerste vijf appartementen veranderen: hoeveel gezinnen er kwamen wonen, de huur ervoor en erna, en hoe zeker het recht van elk gezin is om te blijven wonen. Namen en contracten blijven privé.')],
     [('project-development.html#funding', T('O plano de financiamento', 'The funding plan', 'Het financieringsplan')), ('costs-and-funding.html', T('Custos e recursos', 'Costs and funding', 'Kosten en financiering'))]),
    # HOW-02 (John), HOW-12 (John), WHA-15 (Rafael)
    ('tour-grow', T('Como a IMOBX cresce?', 'How does IMOBX grow?', 'Hoe groeit IMOBX?'), None,
     (T('Primeiro trabalhamos com provas. E provas geram confiança. E com confiança, dá para atrair mais recursos e crescer.', 'First we work with proof. And proof builds trust. And with trust, you can draw in more funding and scale.', 'Eerst werken we met bewijs. Bewijs schept vertrouwen. En met vertrouwen trek je meer middelen aan en kun je groeien.'), JOHN),
     [T('Primeiro uma família, depois cinco apartamentos de cada vez, depois proprietários que queiram entrar com as suas casas.',
        'One family first, then five flats at a time, then owners who want to bring in their own houses.',
        'Eerst één gezin, dan telkens vijf appartementen, dan eigenaren die hun eigen huis willen inbrengen.')],
     [('project-development.html#stages', T('Onde estamos e o que vem depois', 'Where we are and what comes next', 'Waar we staan en wat er komt'))]),
    # Rafael's cave question (his Q1 story, OK'd 8 Nov); John's lines (About page)
    ('tour-people', T('Quem começou a IMOBX, e por quê?', 'Who started IMOBX, and why?', 'Wie begon IMOBX, en waarom?'), None,
     [(T('Quando a vida aperta, a primeira coisa que queremos é entrar na nossa caverna e nos proteger. Por que ter a própria caverna não é um direito de todos? A IMOBX é a minha resposta a essa pergunta.', 'When life gets hard, the first thing we want is to go into our cave and protect ourselves. Why isn’t having one’s own cave a right for everyone? IMOBX is my answer to that question.', 'Als het leven zwaar wordt, willen we eerst onze grot in om ons te beschermen. Waarom is een eigen grot geen recht voor iedereen? IMOBX is mijn antwoord op die vraag.'), RAFAEL),
      (T('Desde 2005, procuro formas para que as comunidades compartilhem o que pertence a todos. A proposta da IMOBX leva essa ideia de compartilhar à moradia.', 'Since 2005, I have looked for ways for communities to share what they hold in common. The IMOBX proposal brings that idea of sharing to housing.', 'Sinds 2005 zoek ik naar manieren waarop gemeenschappen delen wat van hen allemaal is. Het voorstel van IMOBX brengt dat idee van delen naar het wonen.'), JOHN)],
     [T('John é engenheiro de tokens e designer ecológico. Ele está construindo o SIAH Protocol, um registro de contribuições que outras pessoas confirmam.',
        'John is a token engineer and ecological designer. He is building SIAH Protocol, a record of contributions that other people confirm.',
        'John is token-engineer en ecologisch ontwerper. Hij bouwt aan SIAH Protocol, een register van bijdragen die andere mensen bevestigen.')],
     [('about.html', T('Sobre a IMOBX', 'About IMOBX', 'Over IMOBX')), ('resources.html', T('Documentos e fontes', 'Documents and sources', 'Documenten en bronnen')), ('commons-research.html', T('A pesquisa sobre propriedade compartilhada', 'The research on shared ownership', 'Het onderzoek naar gedeeld eigendom'))]),
    # ASK-01 (John)
    ('tour-join', T('Sua vez', 'Your turn', 'Jouw beurt'), None,
     (T('Qualquer pessoa que tenha uma visão parecida com a nossa, entenda o problema e tenha os meios ou a dedicação para resolvê-lo. É esse o tipo de pessoa que queremos atrair.', 'Whatever person has a very similar kind of vision to ours, understands the problem, and has the means or dedication to solve it. That’s the type of people we’re trying to attract.', 'Iedereen die een visie heeft die op de onze lijkt, het probleem begrijpt en de middelen of de toewijding heeft om het op te lossen. Dat is het soort mensen dat we willen aantrekken.'), JOHN),
     [T('Precisamos das pessoas que vão fundar a cooperativa com a gente.',
        'We need the people who will found the cooperative with us.',
        'We hebben de mensen nodig die de coöperatie met ons gaan oprichten.')],
     [('contact.html#apresentacao', T('Apresente-se', 'Introduce yourself', 'Stel jezelf voor'), 'tour-cta'), ('jobs.html', T('Ver a vaga', 'See the open role', 'Bekijk de vacature'), 'tour-jobs')]),
]


# Owner, 9 Nov: each visitor gets its own journey (evidence: 02-research-housing-and-commons/VISITOR_NEEDS_EVIDENCE_2026-11-09.md).
FOR = {
    'tour-tenant': 'resident property funding visitor',
    'tour-rent': 'resident funding visitor',
    'tour-late': 'resident',
    'tour-owner': 'property',
    'tour-builder': 'professional property funding',
    'tour-work': 'professional',
    'tour-village': 'resident funding',
    'tour-courtyard': 'resident property funding visitor',
    'tour-token': 'funding',
    'tour-funding': 'funding professional visitor',
    'tour-grow': 'funding property professional visitor',
    # Owner, 15 Nov: a fifth role, 'visitor'. This chapter lists the four first roles so the visitor's path stays at nine steps; their paths are as before.
    'tour-people': 'resident property professional funding',
}


def _visual(v):
    if not v:
        return ''
    if v[0] == 'img':
        _, src, w, h, alt, cap = v
        a = f'alt="{escape(alt[0], quote=True)}" data-alt-pt="{escape(alt[0], quote=True)}" data-alt-en="{escape(alt[1], quote=True)}" data-alt-nl="{escape(alt[2], quote=True)}"'
        return f'<figure class="tour-figure"><img src="{src}" width="{w}" height="{h}" {a}>' + (_text('figcaption', cap) if cap else '') + '</figure>'
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
        body += ''.join(_paragraph(x) for x in paragraphs)
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
    (root / 'tour.html').write_text(page('IMOBX | Take a tour', body, '<link rel="stylesheet" href="assets/tour.css"><link rel="stylesheet" href="assets/tour-contact.css"><script src="assets/tour-contact.js" defer></script>' + term_scripts(root, ('token-engineer',)), version=version,
                                         lang='pt-BR', title_pt='IMOBX | Conheça a IMOBX'), encoding='utf-8')
