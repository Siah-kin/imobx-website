"""The homepage, built whole from one copy table (owner-approved mock of 26 October 2026,
mock-homepage-2026-10-26/build.py, with the owner's four final wording changes of that day).

Portuguese first; English and Dutch beside it. The page carries data-pt and data-en; add_dutch.py adds data-nl
from i18n/nl.json, keyed by the English. The Dutch of the approved mock is kept here as well, and the build
stops if nl.json ever disagrees with it, so the three languages cannot drift apart.

One warm thread on a teal page: the card and its button on the first screen, the money that leaks away in the
comparison, the same button at the end (brief, section 7b: at most one orange zone per screen height)."""
import html
import json
from pathlib import Path

TG = 'https://t.me/Arctide_TheFlock_Bot?start=imobx'
_dutch = {}      # English -> Dutch, every string on the page


def esc(s):
    return html.escape(s, quote=True)


def t(tag, pt, en, nl, attrs=''):
    _dutch[en.strip()] = nl.strip()
    a = f' {attrs}' if attrs else ''
    return f'<{tag}{a} data-pt="{esc(pt)}" data-en="{esc(en)}">{html.escape(pt, quote=False)}</{tag}>'


def img(src, w, h, pt, en, nl, attrs=''):
    _dutch[en.strip()] = nl.strip()
    a = f' {attrs}' if attrs else ''
    return (f'<img src="{src}" width="{w}" height="{h}"{a} alt="{esc(pt)}" '
            f'data-alt-pt="{esc(pt)}" data-alt-en="{esc(en)}">')


def anchors(*ids):
    """Old section addresses other pages and older links still use; each lands in the nearest new section."""
    return ''.join(f'<span id="{i}"></span>' for i in ids)


# ---------------------------------------------------------------- drawings
def stop(name):
    """A method stop: a small crop from Rafael's village drawing (assets/method-*.jpg)."""
    return f'<span class="stop" aria-hidden="true"><img src="assets/method-{name}.jpg" width="128" height="128" alt=""></span>'


def aria_svg(pt, en, nl, box='0 0 220 180'):
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
bank_svg = (aria_svg('Um balde atrás de um degrau alto: a entrada de 20 a 30% vem antes',
                     'A bucket behind a high step: the down payment of 20 to 30% comes first',
                     'Een emmer achter een hoge trede: de aanbetaling van 20 tot 30% komt eerst')
            + vessel('clip-bank', BANK_BODY, 104, 'M88 58h120')
            + '<rect class="step" x="2" y="46" width="72" height="126"/>'
            '<path class="leak" d="M194 112c12 4 18 18 20 34"/><ellipse class="puddle" cx="206" cy="170" rx="14" ry="5"/>'
            '<path class="line" d="M0 172h220"/></svg>')
bank_fig = ('<div class="way-fig">' + bank_svg
            + label('20 a 30%', '20 to 30%', '20 tot 30%', 'left:0;top:0;font-weight:700')
            + label('entrada', 'down payment', 'aanbetaling', 'left:0;top:17px') + '</div>')

IMOBX_BODY = 'M70 58 L174 58 L162 150 L82 150 Z'
NEXT_BODY = 'M200 122 L246 122 L241 166 L205 166 Z'
imobx_svg = (aria_svg('Um balde que se enche; um fio fino sai para custos e reservas, e o que sobra transborda para a próxima casa',
                      'A bucket that fills; a thin stream leaves for costs and reserves, and what remains spills into the next home',
                      'Een emmer die volloopt; een dun straaltje gaat naar kosten en reserves, en wat overblijft stroomt over naar de volgende woning',
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
    ('Casas voltadas para o pátio: os pais veem os filhos brincarem', 'Homes face the green: parents see their children play', 'Woningen kijken uit op het groen: ouders zien hun kinderen spelen'),
    ('Um pomar', 'An orchard', 'Een boomgaard'),
    ('Uma horta', 'A kitchen garden', 'Een moestuin'),
    ('Parquinhos', 'Playgrounds', 'Speeltuinen'),
    ('Duas salas de estudo', 'Two study rooms', 'Twee studieruimtes'),
    ('Painéis solares nos telhados', 'Solar panels on the roofs', 'Zonnepanelen op de daken'),
]


def button():
    return t('a', 'Apresentar-me no Telegram', 'Introduce myself on Telegram', 'Mezelf voorstellen via Telegram',
             f'class="button act" href="{TG}" target="_blank" rel="noopener noreferrer"')


opening = (
    '<section class="home-opening" id="inicio"><div class="hero-grid"><div class="hero-text">'
    + t('h1', 'Um aluguel que termina com a casa própria', 'Rent that ends in owning the home', 'Huur die eindigt met een eigen woning')
    + t('p', 'Uma cooperativa de bairro no Rio faria isso; preparamos um pequeno piloto e procuramos quem a funde.',
        'A neighbourhood cooperative in Rio would do this; we are preparing a small pilot and looking for its founders.',
        'Een buurtcoöperatie in Rio zou dit doen; we bereiden een kleine pilot voor en zoeken haar oprichters.', 'class="section-lead"')
    + '<div class="key-card">'
    + t('p', 'Parte de cada pagamento mensal conta para a compra da casa. O que sobra depois dos custos e das reservas ajuda a construir as próximas casas. A cooperativa ainda não está constituída; ajude a fundá-la.',
        'Part of each monthly payment counts towards buying the home. What remains after costs and reserves helps build the next homes. The cooperative is not formed yet; help found it.',
        'Een deel van elke maandbetaling telt mee voor de aankoop van de woning. Wat overblijft na kosten en reserves, helpt om de volgende woningen te bouwen. De coöperatie is nog niet opgericht; help haar op te richten.')
    + button()
    + t('p', 'A equipe fundadora responde em português ou inglês, pelo The Flock, a central de atendimento que um fundador da IMOBX administra.',
        'The founding team answers in Portuguese or English, through The Flock, the help desk an IMOBX founder runs.',
        'Het oprichtersteam antwoordt in het Portugees of Engels, via The Flock, de helpdesk die een oprichter van IMOBX beheert.', 'class="card-note"')
    + '</div>'
    + '<p class="after-card">'
    + t('span', 'Nenhuma casa está à venda nem para alugar; nenhum preço ou condição foi decidido. ',
        'Nothing is for sale or rent yet; no price or terms are decided. ',
        'Er is nog niets te koop of te huur; er is geen prijs of voorwaarde vastgelegd. ')
    + t('a', 'Para famílias: como funciona', 'For families: how it works', 'Voor gezinnen: zo werkt het', 'href="rent-to-own.html"') + '</p>'
    + '</div><figure class="village" id="vila"><span id="visao-rafael"></span><div class="village-frame">'
    + img('assets/homepage.jpg', 1024, 765,
          'Ilustração conceitual da vila projetada por Rafael: casas em torno de um pátio verde com pomar, horta, parquinhos, salas de estudo e painéis solares.',
          'Concept illustration of the village Rafael designed: homes around a green courtyard with an orchard, kitchen garden, playgrounds, study rooms and solar panels.',
          'Conceptillustratie van het dorp dat Rafael ontwierp: woningen rond een groene binnenplaats met een boomgaard, moestuin, speeltuinen, studieruimtes en zonnepanelen.',
          'fetchpriority="high"')
    + ''.join(f'<span class="pin" style="left:{x}%;top:{y}%" aria-hidden="true">{i}</span>' for i, (x, y) in enumerate(pins, 1))
    + '</div><ol class="pin-legend">' + ''.join(t('li', *row) for row in legend) + '</ol>'
    + '<figcaption>' + t('span', 'Projeto da vila de Rafael Britto (novembro de 2025), ilustrado com um gerador de imagens; não é um anúncio de casas disponíveis. Horta, pomar e energia solar dependem do terreno e do orçamento.',
                         'Rafael Britto’s village design (November 2025), drawn with an image generator; not a listing of available homes. Garden, orchard and solar depend on the site and budget.',
                         'Het dorpsontwerp van Rafael Britto (november 2025), getekend met een beeldgenerator; geen aanbod van beschikbare woningen. Tuin, boomgaard en zonne-energie hangen af van het terrein en het budget.')
    + '</figcaption></figure></div></section>')

# ---------------------------------------------------------------- 2. the method
steps = [
    ('house', ('Uma casa', 'A house', 'Een huis'),
     ('A construtora dos fundadores construiria as primeiras casas, com cada custo conferido por alguém independente da construtora e dos fundadores.',
      'The founders’ construction company would build the first homes, each cost checked by someone independent of the builder and the founders.',
      'Het bouwbedrijf van de oprichters zou de eerste woningen bouwen, met elke kostenpost gecontroleerd door iemand die onafhankelijk is van de bouwer en de oprichters.')),
    ('home', ('Um lar', 'A home', 'Een thuis'),
     ('A família fica e paga para ser dona; cumpridas as condições escritas, a casa inteira fica em seu nome.',
      'A family stays and pays towards owning it; once the written conditions are met, the whole home is in its name.',
      'Een gezin blijft wonen en betaalt om eigenaar te worden; zodra aan de schriftelijke voorwaarden is voldaan, staat de hele woning op zijn naam.')),
    ('neighbourhood', ('Um bairro', 'A neighbourhood', 'Een buurt'),
     ('Uma forma de viver e cooperar, com moradia compartilhada: casas separadas com espaços comuns, que os moradores administrariam juntos.',
      'A way of living and cooperating, with co-housing: separate homes with shared spaces, which residents would run together.',
      'Een manier van wonen en samenwerken, met gedeeld wonen: aparte woningen met gedeelde ruimtes, die bewoners samen zouden beheren.')),
    ('resilience', ('Resiliência', 'Resilience', 'Veerkracht'),
     ('Mais tarde, os moradores organizariam juntos alimentação, energia e serviços locais. O piloto cobre só a moradia e a obra.',
      'Later, residents would organise food, energy and local services together. The pilot covers only housing and building.',
      'Later zouden bewoners samen voedsel, energie en lokale diensten regelen. De pilot omvat alleen wonen en bouwen.')),
]
method = (
    '<section id="visao">' + anchors('missao', 'problema', 'ambicao', 'o-que-a-cooperativa-faria', 'contexto')
    + t('h2', 'De uma casa a um bairro resiliente', 'From a house to a resilient neighbourhood', 'Van een huis naar een veerkrachtige buurt')
    + t('p', 'A IMOBX quer criar não só casas, mas bairros de transição social rumo a um futuro resiliente. Ter um lar importa para todos, onde quer que vivam.',
        'IMOBX wants to create not just homes, but neighbourhoods of social transition towards a resilient future. A home matters to everyone, wherever they live.',
        'IMOBX wil niet alleen woningen maken, maar buurten van sociale transitie, op weg naar een veerkrachtige toekomst. Een thuis is voor iedereen belangrijk, waar ze ook wonen.', 'class="section-lead"')
    + '<ol class="path">'
    + ''.join('<li>' + stop(k) + '<h3>' + t('span', *title) + '</h3>' + t('p', *body) + '</li>' for k, title, body in steps)
    + '</ol><p class="path-after">'
    + t('span', 'A prova gera confiança, e a confiança atrai financiamento e escala. ',
        'Proof builds trust, and trust draws in funding and scale. ',
        'Bewijs bouwt vertrouwen op, en vertrouwen trekt financiering aan en maakt groei mogelijk. ')
    + t('a', 'Etapas do projeto', 'Project stages', 'Projectfasen', 'href="roadmap.html"')
    + '</p></section>')

# ---------------------------------------------------------------- 3. where each month's payment ends up
ways = (
    '<section id="pagamento">' + anchors('tres-caminhos', 'dinheiro', 'custos')
    + t('h2', 'Para onde vai o pagamento de cada mês', 'Where each month’s payment ends up', 'Waar de betaling van elke maand terechtkomt')
    + '<ol class="ways">'
    '<li class="way-loss">' + t('h3', 'Alugar', 'Renting', 'Huren') + '<div class="way-fig">' + rent_svg + '</div>'
    + t('p', 'O dinheiro vai embora.', 'The money leaves.', 'Het geld verdwijnt.', 'class="verdict"')
    + '<p>' + t('span', 'O aluguel paga a moradia; nada dele conta para a compra daquela casa. Nos novos contratos, o aluguel subiu 9,13% nos 12 meses até setembro de 2026; a inflação foi de 4,58% (',
        'Rent pays for living there; none of it counts towards owning that home. New rents rose 9.13% in the 12 months to September 2026; inflation was 4.58% (',
        'Met de huur betaal je om er te wonen; niets daarvan telt mee voor de aankoop van die woning. Nieuwe huren stegen 9,13% in de 12 maanden tot september 2026; de inflatie was 4,58% (')
    + t('a', 'FipeZap, em Por que moradia', 'FipeZap, in Why housing', 'FipeZap, bij Waarom wonen', 'href="why.html#figures"')
    + t('span', ').', ').', ').') + '</p></li>'
    '<li class="way-loss">' + t('h3', 'Financiar no banco', 'A bank loan', 'Een banklening') + bank_fig
    + t('p', 'Primeiro, uma entrada grande.', 'First, a large down payment.', 'Eerst een grote aanbetaling.', 'class="verdict"')
    + t('p', 'No exemplo da Caixa de 9 de dezembro de 2025, 20 a 30% do preço vêm primeiro, depois até 35 anos de parcelas com juros.',
        'In Caixa’s example of 9 December 2025, 20 to 30% of the price comes first, then up to 35 years of payments with interest.',
        'In het voorbeeld van Caixa van 9 december 2025 komt 20 tot 30% van de prijs eerst, daarna tot 35 jaar lang betalingen met rente.')
    + '<p class="way-source">' + t('span', 'Fonte: ', 'Source: ', 'Bron: ')
    + t('a', 'Agência Brasil, 9 de dezembro de 2025', 'Agência Brasil, 9 December 2025', 'Agência Brasil, 9 december 2025',
        'href="https://www.opovo.com.br/noticias/economia/2025/12/09/caixa-libera-contratacao-de-mais-de-um-financiamento-imobiliario.html"')
    + t('span', '.', '.', '.') + '</p></li>'
    '<li class="way-imobx">' + t('h3', 'A proposta: aluguel com compra na IMOBX', 'The proposal: rent‑to‑own with IMOBX', 'Het voorstel: huurkoop bij IMOBX') + imobx_fig
    + t('p', 'Parte fica na casa.', 'Part stays in the home.', 'Een deel blijft in de woning.', 'class="verdict"')
    + t('p', 'Propõe-se não haver entrada; o preço e as condições seriam escritos antes de alguém se mudar. Os custos e as reservas vêm primeiro.',
        'No down payment is proposed; the price and terms would be written down before anyone moves in. Costs and reserves come first.',
        'Er wordt geen aanbetaling voorgesteld; de prijs en de voorwaarden zouden worden vastgelegd voordat iemand er gaat wonen. Kosten en reserves komen eerst.')
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
    + t('span', 'Modelo arquitetônico dos dois lofts (janeiro de 2026), fornecido pela equipe: um estudo de projeto. Nenhuma casa está à venda nem para alugar.',
        'Architectural model of the two lofts (January 2026), supplied by the team: a design study. No home is for sale or rent.',
        'Architectuurmodel van de twee lofts (januari 2026), aangeleverd door het team: een ontwerpstudie. Er is geen woning te koop of te huur.')
    + '</figcaption></figure></section>')

# ---------------------------------------------------------------- 5. who we are looking for, and how to join
roles = [
    ('property', ('Um imóvel', 'A property', 'Grond of een gebouw'),
     ('Terreno ou prédio para doar, vender ou alugar.', 'Land or a building to donate, sell or lease.', 'Grond of een gebouw om te schenken, te verkopen of te verhuren.'),
     ('Depois, uma primeira conversa sobre o imóvel e as conferências que ainda faltam.',
      'Then a first conversation about the property and the checks still needed.',
      'Daarna een eerste gesprek over de grond of het gebouw en de controles die nog nodig zijn.')),
    ('construction', ('Obra', 'Construction work', 'Bouwwerkzaamheden'),
     ('Construir a preços combinados; trabalho e faturas seriam conferidos por alguém independente da construtora e dos fundadores.',
      'Building at agreed prices; work and invoices would be checked by someone independent of the builder and the founders.',
      'Bouwen tegen afgesproken prijzen; werk en facturen zouden worden gecontroleerd door iemand die onafhankelijk is van de bouwer en de oprichters.'),
     ('Depois, uma primeira conversa sobre o escopo e o preço.', 'Then a first conversation about scope and price.', 'Daarna een eerste gesprek over de omvang van het werk en de prijs.')),
    ('skills', ('Trabalho profissional', 'Professional skills', 'Professioneel werk'),
     ('Direito, contabilidade e trabalho comunitário.',
      'Legal, accounting and community work.',
      'Juridisch werk, boekhouding en buurtwerk.'),
     ('Depois, uma conversa sobre uma primeira tarefa e o tempo que ela leva.',
      'Then a conversation about a first task and the time it takes.',
      'Daarna een gesprek over een eerste taak en de tijd die dat kost.')),
    ('funding', ('Financiamento', 'Funding', 'Financiering'),
     ('Doações e recursos de editais, agora. Investimento só quando a forma jurídica permitir, e quem investe recebe somente os direitos escritos no seu acordo.',
      'Donations and grants now. Investment only when the legal form allows it, and investors receive only the rights written in their agreement.',
      'Donaties en subsidies, nu. Investeren kan pas als de rechtsvorm het toestaat, en investeerders krijgen alleen de rechten die in hun overeenkomst staan.'),
     ('Depois, uma conversa sobre a finalidade da sua contribuição e quem poderia recebê-la.',
      'Then a conversation about its purpose and who could receive it.',
      'Daarna een gesprek over het doel van je bijdrage en wie die zou kunnen ontvangen.')),
]
join = (
    '<section id="participar">' + anchors('parceiros', 'fundadores', 'como-entrar', 'como-chegamos', 'saiba-mais')
    + t('h2', 'Quem procuramos, e como entrar', 'Who we are looking for, and how to join', 'Wie we zoeken, en hoe je meedoet')
    + t('p', 'Procuramos pessoas e organizações que compartilhem esta visão, entendam o problema e tenham meios ou dedicação para ajudar a fundar a cooperativa.',
        'We are looking for people and organisations who share this vision, understand the problem and have the means or the dedication to help found the cooperative.',
        'We zoeken mensen en organisaties die deze visie delen, het probleem begrijpen en de middelen of de inzet hebben om de coöperatie mee op te richten.', 'class="section-lead"')
    + '<ul class="roles">'
    + ''.join('<li><h3>' + t('a', *title, f'href="contact.html?role={key}"') + '</h3>' + t('p', *ask) + t('p', *nxt, 'class="next"') + '</li>'
              for key, title, ask, nxt in roles)
    + '</ul>'
    + t('p', 'Apresente-se pelo Telegram; a equipe fundadora responde. Até a cooperativa ser constituída e seus fundadores combinarem as regras, não se oferece filiação, cota nem investimento.',
        'Introduce yourself on Telegram; the founding team answers. Until the cooperative is formed and its founders agree its rules, no membership, share or investment is offered.',
        'Stel je voor via Telegram; het oprichtersteam antwoordt. Tot de coöperatie is opgericht en haar oprichters de regels hebben vastgelegd, wordt er geen lidmaatschap, aandeel of investering aangeboden.', 'class="join-line"')
    + '<p class="home-actions">' + button() + '</p>'
    + '</section>')

MAIN = '<main id="main" class="band-page home-page">' + opening + method + ways + prototype + join + '</main>'

TITLE_EN, TITLE_PT, TITLE_NL = 'IMOBX | Proposed Rio housing pilot', 'IMOBX | Proposta de piloto no Rio', 'IMOBX | Voorgestelde woonpilot in Rio'
_dutch[TITLE_EN] = TITLE_NL
HEAD = ('<link rel="canonical" href="https://siah-kin.github.io/imobx-website/">'
        '<meta property="og:image" content="https://siah-kin.github.io/imobx-website/assets/homepage.jpg"><meta property="og:type" content="website">'
        '<meta property="og:title" content="IMOBX | Proposta de piloto no Rio">'
        '<meta property="og:description" content="Um aluguel que termina com a casa própria. Uma cooperativa de bairro no Rio faria isso; preparamos um pequeno piloto e procuramos quem a funde.">')
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
