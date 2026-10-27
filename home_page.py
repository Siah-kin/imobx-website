"""The homepage, built whole from one copy table (owner-approved mock of 26 October 2026,
mock-homepage-2026-10-26/build.py, with the owner's four final wording changes of that day). Since 27 October
2026 every string is the owner-approved copy deck COPY_DECK_OWNER_VOICE_2026-10-27.md (main text, not variants),
except the Telegram action, its card note and the join line's first clause: the owner moved the action to the IMOBX
Telegram group the same day (TG below).

Portuguese first; English and Dutch beside it. The page carries data-pt and data-en; add_dutch.py adds data-nl
from i18n/nl.json, keyed by the English. The Dutch of the approved mock is kept here as well, and the build
stops if nl.json ever disagrees with it, so the three languages cannot drift apart.

One warm thread on a teal page: the card and its button on the first screen, the money that leaks away in the
comparison, the same button at the end (brief, section 7b: at most one orange zone per screen height)."""
import html
import json
from pathlib import Path

TG = 'https://t.me/+n-42pfkXna5mNzRk'   # the IMOBX Telegram group, where people can write (owner, 27 Oct)
_dutch = {}      # English -> Dutch, every string on the page


def esc(s):
    return html.escape(s, quote=True)


def t(tag, pt, en, nl, attrs=''):
    en = en.replace("'", '’')
    _dutch[en.strip()] = nl.strip()
    a = f' {attrs}' if attrs else ''
    return f'<{tag}{a} data-pt="{esc(pt)}" data-en="{esc(en)}">{html.escape(pt, quote=False)}</{tag}>'


def img(src, w, h, pt, en, nl, attrs=''):
    en = en.replace("'", '’')
    _dutch[en.strip()] = nl.strip()
    a = f' {attrs}' if attrs else ''
    return (f'<img src="{src}" width="{w}" height="{h}"{a} alt="{esc(pt)}" '
            f'data-alt-pt="{esc(pt)}" data-alt-en="{esc(en)}">')


def anchors(*ids):
    """Old section addresses other pages and older links still use; each lands in the nearest new section."""
    return ''.join(f'<span id="{i}"></span>' for i in ids)


# ---------------------------------------------------------------- drawings
GLYPHS = {   # the four line icons of the earlier homepage (owner, 26 Oct: put the icons back)
    'house': '<path d="M3 11 12 4l9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
    'home': '<path d="M3 11 12 4l9 7"/><path d="M5 10v10h14V10"/><path d="M12 17.6c-2.3-1.5-3.3-2.7-3.3-3.9 0-1 .8-1.8 1.8-1.8.7 0 1.2.4 1.5.9.3-.5.8-.9 1.5-.9 1 0 1.8.8 1.8 1.8 0 1.2-1 2.4-3.3 3.9z"/>',
    'neighbourhood': '<path d="M1.5 20h21"/><path d="M2.5 13 6 10l3.5 3"/><path d="M3.5 12.2V20h5v-7.8"/><path d="M14.5 13 18 10l3.5 3"/><path d="M15.5 12.2V20h5v-7.8"/><path d="M12 20v-4.5"/><circle cx="12" cy="12.2" r="2.6"/>',
    'resilience': '<path d="M4 20.5h16"/><path d="M12 20.5v-8"/><path d="M12 12.5c0-3.4 2.2-5.6 6-5.6 0 3.4-2.2 5.6-6 5.6z"/><path d="M12 15.5c0-2.7-1.8-4.4-4.8-4.4 0 2.7 1.8 4.4 4.8 4.4z"/><path d="M7 4.5a5 5 0 0 1 3-1"/>',
}


def stop(name):
    """A method stop: a line icon in a circle on the teal path."""
    return f'<span class="stop" aria-hidden="true"><svg class="stop-glyph" viewBox="0 0 24 24">{GLYPHS[name]}</svg></span>'


def aria_svg(pt, en, nl, box='0 0 220 180'):
    en = en.replace("'", '’')
    _dutch[en.strip()] = nl.strip()
    return (f'<svg class="way-art" viewBox="{box}" role="img" aria-label="{esc(pt)}" '
            f'data-aria-pt="{esc(pt)}" data-aria-en="{esc(en)}">')


def vessel(cid, body, level, rim):
    return (f'<defs><clipPath id="{cid}"><path d="{body}"/></clipPath></defs>'
            f'<path class="vessel" d="{body}"/>'
            f'<g clip-path="url(#{cid})"><rect class="water" x="0" y="{level}" width="260" height="120"/></g>'
            f'<path class="line" d="{body}"/><path class="line" d="{rim}"/>')


def label(pt, en, nl, style):
    return t('span', pt, en, nl, f'class="fig-label" style="{style}"')


BODY = 'M58 58 L162 58 L150 150 L70 150 Z'
rent_svg = (aria_svg('Um balde que esvazia todo mês: o aluguel paga a moradia e nada dele conta para a compra da casa.',
                     'A bucket that empties each month: rent pays for living there, and none of it counts towards buying the home.',
                     'Een emmer die elke maand leegloopt: met de huur betaal je om er te wonen, en niets daarvan telt mee voor de aankoop van de woning.')
            + '<path class="stream" d="M110 0v118"/>' + vessel('clip-rent', BODY, 122, 'M50 58h120')
            + '<path class="leak" d="M66 104c-14 4-22 20-24 40"/><path class="leak" d="M154 100c14 4 22 22 24 42"/>'
            '<path class="leak" d="M104 150c-2 8-4 14-4 18"/>'
            '<ellipse class="puddle" cx="40" cy="170" rx="26" ry="6"/><ellipse class="puddle" cx="180" cy="170" rx="26" ry="6"/>'
            '<ellipse class="puddle" cx="102" cy="174" rx="18" ry="4"/></svg>')

BANK_BODY = 'M96 58 L200 58 L188 150 L108 150 Z'
bank_svg = (aria_svg('Um balde atrás de um degrau alto: a entrada de 20 a 30% vem antes.',
                     'A bucket behind a high step: the down payment of 20 to 30% comes first.',
                     'Een emmer achter een hoge trede: de aanbetaling van 20 tot 30% komt eerst.')
            + vessel('clip-bank', BANK_BODY, 104, 'M88 58h120')
            + '<rect class="step" x="2" y="46" width="72" height="126"/>'
            '<path class="leak" d="M194 112c12 4 18 18 20 34"/><ellipse class="puddle" cx="206" cy="170" rx="14" ry="5"/>'
            '<path class="line" d="M0 172h220"/></svg>')
bank_fig = ('<div class="way-fig">' + bank_svg
            + label('20 a 30%', '20 to 30%', '20 tot 30%', 'left:0;top:0;font-weight:700')
            + label('entrada', 'down payment', 'aanbetaling', 'left:0;top:17px') + '</div>')

IMOBX_BODY = 'M70 58 L174 58 L162 150 L82 150 Z'
NEXT_BODY = 'M200 122 L246 122 L241 166 L205 166 Z'
imobx_svg = (aria_svg('Um balde que se enche. Um fio fino sai para custos e reservas, e o que sobra transborda para a próxima casa.',
                      'A bucket that fills. A thin stream leaves for costs and reserves, and what remains spills into the next home.',
                      'Een emmer die volloopt. Een dun straaltje gaat naar kosten en reserves, en wat overblijft stroomt over naar de volgende woning.',
                      '0 0 260 180')
             + '<path class="stream" d="M122 0v70"/>'
             f'<defs><clipPath id="clip-imobx"><path d="{IMOBX_BODY}"/></clipPath>'
             f'<clipPath id="clip-next"><path d="{NEXT_BODY}"/></clipPath></defs>'
             f'<path class="vessel" d="{IMOBX_BODY}"/>'
             '<g clip-path="url(#clip-imobx)"><rect class="water water-rise" x="40" y="66" width="160" height="120"/></g>'
             f'<path class="line" d="{IMOBX_BODY}"/><path class="line" d="M62 58h120"/>'
             '<path class="mark" d="M106 120 122 106l16 14"/><path class="mark" d="M110 117v19h24v-19"/>'
             '<path class="outflow" d="M84 134c-16 4-30 14-40 34"/><ellipse class="outpool" cx="38" cy="171" rx="16" ry="4"/>'
             '<path class="stream spill" d="M180 60c16 0 30 20 32 58"/>'
             f'<path class="vessel" d="{NEXT_BODY}"/>'
             '<g clip-path="url(#clip-next)"><rect class="water water-next" x="190" y="146" width="70" height="40"/></g>'
             f'<path class="line" d="{NEXT_BODY}"/><path class="line" d="M196 122h54"/>'
             '<path class="mark" d="M214 148 223 140l9 8"/><path class="mark" d="M216.5 146v10h13v-10"/></svg>')
imobx_fig = ('<div class="way-fig way-fig-wide">' + imobx_svg
             + label('custos e reservas', 'costs and reserves', 'kosten en reserves', 'left:0;top:100%')
             + label('próxima casa', 'next home', 'volgende woning', 'right:0;top:100%') + '</div>')

# ---------------------------------------------------------------- 1. the opening
pins = [(27, 33), (37, 61), (79, 61), (66, 53), (55, 39), (57, 87)]
legend = [
    ('Casas em volta de um gramado, para os pais verem os filhos brincarem', 'Homes around a green, so parents can watch their children play', 'Woningen rond een grasveld, zodat ouders hun kinderen kunnen zien spelen'),
    ('Um pomar', 'An orchard', 'Een boomgaard'),
    ('Uma horta', 'A kitchen garden', 'Een moestuin'),
    ('Parquinhos', 'Playgrounds', 'Speeltuinen'),
    ('Duas salas de estudo', 'Two study rooms', 'Twee studieruimtes'),
    ('Painéis solares nos telhados', 'Solar panels on the roofs', 'Zonnepanelen op de daken'),
]


def button():
    return t('a', 'Entrar no grupo da IMOBX no Telegram', 'Join the IMOBX group on Telegram', 'Doe mee in de IMOBX-groep op Telegram',
             f'class="button act" href="{TG}" target="_blank" rel="noopener noreferrer"')


opening = (
    '<section class="home-opening" id="inicio"><div class="hero-grid"><div class="hero-text">'
    + t('h1', 'Um aluguel que termina com a casa no seu nome', 'Rent that ends with the home in your name', 'Huur die eindigt met de woning op jouw naam')
    + t('p', 'Nas grandes cidades do Brasil, o aluguel de contrato novo subiu quase o dobro da inflação no último ano, e nem um centavo dele vira seu. O banco pede 20 a 30% de entrada, antes de você pegar as chaves. Queremos mudar isso, com um piloto pequeno no Rio, organizado como cooperativa de bairro.',
        "In Brazil's big cities, rent on new contracts rose almost twice as fast as inflation in the past year, and not a cent of it becomes yours. A bank wants 20 to 30% up front, before you get the keys. We want to change that, with a small pilot in Rio, run as a neighbourhood cooperative.",
        'In de grote steden van Brazilië steeg de huur van nieuwe contracten het afgelopen jaar bijna twee keer zo snel als de inflatie, en geen cent daarvan wordt van jou. Een bank wil 20 tot 30% vooraf, voordat je de sleutels krijgt. Dat willen we veranderen, met een kleine pilot in Rio, opgezet als buurtcoöperatie.', 'class="section-lead"')
    + '<div class="key-card">'
    + t('p', 'Aluguel tinha que comprar alguma coisa. No nosso modelo, parte de cada pagamento vai para a compra da casa em que você mora, e o que sobra depois dos custos e das reservas constrói a próxima. A cooperativa ainda não existe. Estamos procurando as pessoas que vão fundá‑la com a gente.',
        "Rent should buy you something. In our model, part of every payment goes towards owning the home you live in, and what's left after costs and reserves builds the next one. The cooperative doesn't exist yet. We're looking for the people to found it with us.",
        'Huur zou je iets moeten opleveren. In ons model gaat een deel van elke betaling naar het kopen van de woning waarin je woont, en wat overblijft na kosten en reserves bouwt de volgende. De coöperatie bestaat nog niet. We zoeken de mensen die haar samen met ons oprichten.')
    + button()
    + t('p', 'Os fundadores respondem lá em português ou inglês. Todos no grupo veem o que você publica, então deixe dados pessoais para uma mensagem privada.',
        'The founders answer there in Portuguese or English. Everyone in the group sees what you post, so keep personal details for a private message.',
        'De oprichters antwoorden daar in het Portugees of Engels. Iedereen in de groep ziet wat je plaatst, dus bewaar persoonlijke gegevens voor een privébericht.', 'class="card-note"')
    + '</div>'
    + '<p class="after-card">'
    + t('span', 'Nada está à venda nem para alugar, e não há preço nem condições. ',
        'Nothing is for sale or rent, and there are no prices or terms. ',
        'Er is niets te koop of te huur, en er zijn geen prijzen of voorwaarden. ')
    + t('a', 'Para famílias: como funciona', 'For families: how it works', 'Voor gezinnen: zo werkt het', 'href="rent-to-own.html"') + '</p>'
    + '</div><figure class="village" id="vila"><span id="visao-rafael"></span><div class="village-frame">'
    + img('assets/homepage.jpg', 1024, 765,
          'Ilustração conceitual da vila projetada por Rafael: casas em torno de um pátio verde com pomar, horta, parquinhos, salas de estudo e painéis solares.',
          'Concept illustration of the village Rafael designed: homes around a green courtyard with an orchard, kitchen garden, playgrounds, study rooms and solar panels.',
          'Conceptillustratie van het dorp dat Rafael ontwierp: woningen rond een groene binnenplaats met een boomgaard, moestuin, speeltuinen, studieruimtes en zonnepanelen.',
          'fetchpriority="high"')
    + ''.join(f'<span class="pin" style="left:{x}%;top:{y}%" aria-hidden="true">{i}</span>' for i, (x, y) in enumerate(pins, 1))
    + '</div><ol class="pin-legend">' + ''.join(t('li', *row) for row in legend) + '</ol>'
    + '<figcaption>' + t('span', 'Rafael Britto desenhou esta vila em novembro de 2025 com um gerador de imagens. Ela mostra a ideia, não casas para alugar. Horta, pomar e energia solar dependem do terreno e do orçamento.',
                         'Rafael Britto drew this village in November 2025 with an image generator. It shows the idea, not homes you can rent. Garden, orchard and solar depend on the land and the budget.',
                         'Rafael Britto tekende dit dorp in november 2025 met een beeldgenerator. Het laat het idee zien, geen woningen die je kunt huren. Moestuin, boomgaard en zonnepanelen hangen af van het terrein en het budget.')
    + '</figcaption></figure></div></section>')

# ---------------------------------------------------------------- 2. the method
steps = [
    ('house', ('Uma casa', 'A house', 'Een huis'),
     ('No nosso plano, a construtora dos fundadores constrói as primeiras casas, e alguém independente de nós confere cada custo.',
      'In our plan, the founders’ construction company builds the first homes, and someone independent of us checks every cost.',
      'In ons plan bouwt het bouwbedrijf van de oprichters de eerste woningen, en controleert iemand onafhankelijk van ons elke kostenpost.')),
    ('home', ('Um lar', 'A home', 'Een thuis'),
     ('Uma família se muda e paga para ser dona da casa. Cumpriu as condições escritas, a escritura fica no nome dela.',
      'A family moves in and pays towards owning it. Meet the written conditions, and the deed is in their name.',
      'Een gezin trekt erin en betaalt om eigenaar te worden. Voldoe aan de schriftelijke voorwaarden, en de akte staat op hun naam.')),
    ('neighbourhood', ('Um bairro', 'A neighbourhood', 'Een buurt'),
     ('Casas próprias em volta de espaços comuns. Moradia compartilhada: uma forma de viver e cooperar que os próprios moradores administram.',
      'Homes of their own around shared spaces. Co-housing: a way of living and cooperating that the residents run.',
      'Eigen woningen rond gedeelde ruimtes. Gedeeld wonen: een manier van wonen en samenwerken die de bewoners zelf runnen.')),
    ('resilience', ('Resiliência', 'Resilience', 'Veerkracht'),
     ('Mais tarde, alimentação, energia e serviços locais, organizados pelos moradores. O piloto começa só com moradia.',
      'Later, food, energy and local services, organised by the residents. The pilot starts with housing only.',
      'Later voedsel, energie en lokale diensten, georganiseerd door de bewoners. De pilot begint alleen met wonen.')),
]
method = (
    '<section id="visao">' + anchors('missao', 'problema', 'ambicao', 'o-que-a-cooperativa-faria', 'contexto')
    + t('h2', 'De uma casa a um bairro resiliente', 'From a house to a resilient neighbourhood', 'Van een huis naar een veerkrachtige buurt')
    + t('p', 'Não queremos construir casas e ir embora. Queremos criar não só casas, mas bairros de transição social rumo a um futuro resiliente. Fazer um lar é uma busca existencial de toda pessoa, esteja onde estiver.',
        "We don't want to build houses and walk away. We want to create not just homes, but neighbourhoods of social transition towards a resilient future. Making a home is an existential quest for every person, wherever they are.",
        'We willen geen huizen bouwen en weglopen. We willen niet alleen woningen maken, maar buurten van sociale transitie op weg naar een veerkrachtige toekomst. Een thuis maken is een existentiële zoektocht van ieder mens, waar je ook bent.', 'class="section-lead"')
    + '<ol class="path">'
    + ''.join('<li>' + stop(k) + '<h3>' + t('span', *title) + '</h3>' + t('p', *body) + '</li>' for k, title, body in steps)
    + '</ol><p class="path-after">'
    + t('span', 'Primeiro provamos que funciona. A prova gera confiança, e a confiança atrai financiamento e escala. ',
        'First we prove it works. Proof builds trust, and trust draws in funding and scale. ',
        'Eerst bewijzen we dat het werkt. Bewijs bouwt vertrouwen op, en vertrouwen trekt financiering en schaal aan. ')
    + t('a', 'Etapas do projeto', 'Project stages', 'Projectfasen', 'href="roadmap.html"')
    + '</p></section>')

# ---------------------------------------------------------------- 3. where each month's money goes
ways = (
    '<section id="pagamento">' + anchors('tres-caminhos', 'dinheiro', 'custos')
    + t('h2', 'Para onde vai o dinheiro de cada mês', "Where each month's money goes", 'Waar het geld van elke maand naartoe gaat')
    + '<ol class="ways">'
    '<li class="way-loss">' + t('h3', 'Alugar', 'Renting', 'Huren') + '<div class="way-fig">' + rent_svg + '</div>'
    + t('p', 'O dinheiro vai embora.', 'The money is gone.', 'Het geld is weg.', 'class="verdict"')
    + '<p>' + t('span', 'O aluguel de contrato novo subiu 9,13% nos 12 meses até setembro de 2026, contra 4,58% de inflação (',
        'Rent on new contracts rose 9.13% in the 12 months to September 2026, against 4.58% inflation (',
        'De huur van nieuwe contracten steeg met 9,13% in de 12 maanden tot september 2026, tegenover 4,58% inflatie (')
    + t('a', 'FipeZap, em Por que moradia', 'FipeZap, in Why housing', 'FipeZap, bij Waarom wonen', 'href="why.html#figures"')
    + t('span', ').', ').', ').') + '</p></li>'
    '<li class="way-loss">' + t('h3', 'Financiar no banco', 'A bank loan', 'Een banklening') + bank_fig
    + t('p', 'Primeiro, uma entrada grande.', 'First, a big down payment.', 'Eerst een grote aanbetaling.', 'class="verdict"')
    + t('p', 'Exemplo da Caixa (9 de dezembro de 2025): 20 a 30% do preço de entrada, e depois até 35 anos com juros.',
        "Caixa's example (9 December 2025): 20 to 30% of the price up front, then up to 35 years with interest.",
        'Voorbeeld van Caixa (9 december 2025): 20 tot 30% van de prijs vooraf, en daarna tot 35 jaar met rente.')
    + '<p class="way-source">' + t('span', 'Fonte: ', 'Source: ', 'Bron: ')
    + t('a', 'Agência Brasil, 9 de dezembro de 2025', 'Agência Brasil, 9 December 2025', 'Agência Brasil, 9 december 2025',
        'href="https://www.opovo.com.br/noticias/economia/2025/12/09/caixa-libera-contratacao-de-mais-de-um-financiamento-imobiliario.html"')
    + t('span', '.', '.', '.') + '</p></li>'
    '<li class="way-imobx">' + t('h3', 'A proposta: aluguel com compra na IMOBX', 'The proposal: rent‑to‑own with IMOBX', 'Het voorstel: huurkoop bij IMOBX') + imobx_fig
    + t('p', 'Parte fica na casa.', 'Part stays in the home.', 'Een deel blijft in de woning.', 'class="verdict"')
    + t('p', 'Propomos que não haja entrada. Preço e condições ficam por escrito antes de alguém se mudar, e os custos e as reservas são pagos primeiro.',
        'We propose no down payment. Price and terms go in writing before anyone moves in, and costs and reserves are paid first.',
        'Wij stellen voor: geen aanbetaling. Prijs en voorwaarden staan op papier voordat iemand erin trekt, en kosten en reserves worden eerst betaald.')
    + '</li></ol></section>')

# ---------------------------------------------------------------- 4. our prototype
views = [('property-1.jpg', 823, 581, 'Vista externa', 'Exterior view', 'Buitenaanzicht'),
         ('property-4-clean.jpg', 957, 591, 'Corte do modelo', 'Model section', 'Doorsnede van het model'),
         ('property-3.jpg', 921, 595, 'Planta do nível superior', 'Upper-level plan', 'Plattegrond van de bovenverdieping')]
prototype = (
    '<section id="prototipo">' + anchors('estudo-lofts-home', 'estudo-lofts', 'modelo')
    + t('h2', 'Nosso protótipo: os dois lofts', 'Our prototype: the two lofts', 'Ons prototype: de twee lofts')
    + '<figure class="proto"><div class="proto-grid">'
    + ''.join(f'<div class="proto-view proto-{i}">' + img('assets/' + f, w, h, pt, en, nl) + '</div>'
              for i, (f, w, h, pt, en, nl) in enumerate(views, 1))
    + '</div><figcaption>'
    + t('span', 'Nossa equipe modelou estes dois lofts em janeiro de 2026. É um estudo de projeto. Nenhuma casa está à venda nem para alugar.',
        "Our team modelled these two lofts in January 2026. It's a design study. No home is for sale or rent.",
        'Ons team maakte in januari 2026 een model van deze twee lofts. Het is een ontwerpstudie. Er is geen woning te koop of te huur.')
    + '</figcaption></figure></section>')

# ---------------------------------------------------------------- 5. who we need, and how to join
roles = [
    ('property', ('Um imóvel', 'A property', 'Grond of een gebouw'),
     ('Terreno ou prédio para doar, vender ou alugar.', 'Land or a building to donate, sell or lease.', 'Grond of een gebouw om te schenken, te verkopen of te verhuren.'),
     ('Primeiro, uma conversa sobre o imóvel e as verificações que ele precisa.',
      'First, a conversation about the property and the checks it needs.',
      'Eerst een gesprek over het pand en de controles die het nodig heeft.')),
    ('construction', ('Obra', 'Construction work', 'Bouwwerkzaamheden'),
     ('Construir a preços combinados, com trabalho e faturas conferidos por alguém independente da construtora e de nós.',
      'Building at agreed prices, with work and invoices checked by someone independent of the builder and of us.',
      'Bouwen tegen afgesproken prijzen, met werk en facturen gecontroleerd door iemand onafhankelijk van de bouwer en van ons.'),
     ('Primeiro conversamos sobre o escopo e o preço.', 'First we talk through the scope and the price.', 'Eerst nemen we de omvang van het werk en de prijs door.')),
    ('skills', ('Trabalho profissional', 'Professional skills', 'Professioneel werk'),
     ('Direito, contabilidade ou trabalho comunitário.',
      'Legal, accounting or community work.',
      'Juridisch werk, boekhouding of buurtwerk.'),
     ('Juntos, escolhemos uma primeira tarefa e marcamos um prazo.',
      'Together we pick a first task and put a time on it.',
      'Samen kiezen we een eerste taak en zetten er een termijn op.')),
    ('funding', ('Financiamento', 'Funding', 'Financiering'),
     ('Doações e editais, por enquanto. Investimento só quando a forma jurídica da cooperativa permitir, e só com termos por escrito.',
      "Donations and grants for now. Investment only once the cooperative's legal form allows it, and only on written terms.",
      'Voorlopig donaties en subsidies. Investeren pas als de rechtsvorm van de coöperatie het toestaat, en alleen op schriftelijke voorwaarden.'),
     ('Conversamos sobre a finalidade do dinheiro e quem pode recebê-lo legalmente.',
      'We talk about what the money is for and who can legally receive it.',
      'We bespreken waar het geld voor is en wie het wettelijk mag ontvangen.')),
]
join = (
    '<section id="participar">' + anchors('parceiros', 'fundadores', 'como-entrar', 'como-chegamos', 'saiba-mais')
    + t('h2', 'De quem precisamos, e como entrar', 'Who we need, and how to join', 'Wie we nodig hebben, en hoe je meedoet')
    + t('p', 'Precisamos de pessoas que compartilhem esta visão, entendam o problema e tenham meios ou dedicação. Traga o que você tem e ajude a fundar a cooperativa com a gente.',
        'We need people who share this vision, understand the problem and have the means or the dedication. Bring what you have, and help us found the cooperative.',
        'We hebben mensen nodig die deze visie delen, het probleem begrijpen en de middelen of de inzet hebben. Breng mee wat je hebt en help ons de coöperatie op te richten.', 'class="section-lead"')
    + '<ul class="roles">'
    + ''.join('<li><h3>' + t('a', *title, f'href="contact.html?role={key}"') + '</h3>' + t('p', *ask) + t('p', *nxt, 'class="next"') + '</li>'
              for key, title, ask, nxt in roles)
    + '</ul>'
    + t('p', 'Entre no grupo da IMOBX no Telegram e um fundador responde. Até a cooperativa ser constituída e suas regras combinadas, não oferecemos filiação, cotas nem investimento.',
        'Join the IMOBX group on Telegram and a founder answers. Until the cooperative is formed and its rules agreed, we offer no membership, no shares and no investment.',
        'Doe mee in de IMOBX-groep op Telegram en een oprichter antwoordt. Tot de coöperatie is opgericht en de regels zijn vastgelegd, bieden we geen lidmaatschap, geen aandelen en geen investering aan.', 'class="join-line"')
    + '<p class="home-actions">' + button() + '</p>'
    + t('p', 'Todos no grupo veem o que você publica, então deixe dados pessoais para uma mensagem privada.',
        'Everyone in the group sees what you post, so keep personal details for a private message.',
        'Iedereen in de groep ziet wat je plaatst, dus bewaar persoonlijke gegevens voor een privébericht.', 'class="button-note"')
    + '</section>')

MAIN = '<main id="main" class="band-page home-page">' + opening + method + ways + prototype + join + '</main>'

TITLE_EN, TITLE_PT, TITLE_NL = 'IMOBX | Proposed Rio housing pilot', 'IMOBX | Proposta de piloto no Rio', 'IMOBX | Voorgestelde woonpilot in Rio'
_dutch[TITLE_EN] = TITLE_NL
HEAD = ('<link rel="canonical" href="https://siah-kin.github.io/imobx-website/">'
        '<meta property="og:image" content="https://siah-kin.github.io/imobx-website/assets/homepage.jpg"><meta property="og:type" content="website">'
        '<meta property="og:title" content="IMOBX | Proposta de piloto no Rio">'
        '<meta property="og:description" content="Um aluguel que termina com a casa no seu nome. Nas grandes cidades do Brasil, o aluguel de contrato novo subiu quase o dobro da inflação no último ano, e nem um centavo dele vira seu. Queremos mudar isso, começando com um piloto pequeno no Rio.">')
DESCRIPTION = 'Proposta de piloto de moradia com opção de compra no Rio, organizado como cooperativa de bairro. Nada está à venda; a cooperativa ainda não está constituída.'


def dutch():
    """English -> Dutch for every string on the page, as approved in the mock."""
    return dict(_dutch)


def check_dutch(root):
    """i18n/nl.json must carry the approved Dutch for every English string here; the build stops on any difference."""
    nl = json.loads((Path(root) / 'i18n' / 'nl.json').read_text())
    bad = [(en, nl.get(en), want) for en, want in _dutch.items() if nl.get(en) != want]
    if bad:
        lines = '\n'.join(f'  {en!r}: nl.json has {have!r}, the approved homepage says {want!r}' for en, have, want in bad)
        raise ValueError('i18n/nl.json disagrees with the approved homepage Dutch:\n' + lines)


def build_home(root, page, asset_v):
    root = Path(root)
    check_dutch(root)
    script = (f'<link rel="stylesheet" href="{asset_v("bands.css")}"><link rel="stylesheet" href="{asset_v("home.css")}">'
              f'<script src="assets/site.js" defer></script><script src="{asset_v("home.js")}" defer></script>')
    (root / 'index.html').write_text(page(TITLE_EN, MAIN, script, lang='pt-BR', title_pt=TITLE_PT, head=HEAD, description=DESCRIPTION))
