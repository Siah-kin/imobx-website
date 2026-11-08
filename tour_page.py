"""The IMOBX tour: five steps in the order why, how, take part (owner, 8 Nov: "Yes" to a tighter tour).

The page is readable on its own and is the source the homepage dialog (assets/tour.js) loads its steps from.
Built from Codex's tour mechanics (take-a-tour-codex, 8 Nov); the steps were rewritten from 13 to 5.
"""
from html import escape


def _text(tag, pt, en, nl, attrs=''):
    """Keep complete sentences together for the site's language switcher."""
    translations = f'data-pt="{escape(pt, quote=True)}" data-en="{escape(en, quote=True)}" data-nl="{escape(nl, quote=True)}"'
    return f'<{tag} {translations}{(" " + attrs) if attrs else ""}>{escape(pt)}</{tag}>'


def _link(href, pt, en, nl, cls=''):
    return _text('a', pt, en, nl, f'href="{escape(href, quote=True)}"' + (f' class="{cls}"' if cls else ''))


STEPS = [
    ('tour-home', ('Um lugar para chamar de lar', 'A place to call home', 'Een plek om je thuis te voelen'), [
        ('Muitas famílias no Rio pagam aluguel por anos sem chegar mais perto da casa própria. No Brasil, os aluguéis subiram 9,13% nos 12 meses até setembro de 2026, o dobro da inflação oficial.',
         'Many families in Rio pay rent for years without getting any closer to owning a house. Across Brazil, rents rose 9.13% in the 12 months to September 2026, twice the official inflation.',
         'Veel gezinnen in Rio betalen jarenlang huur zonder dichter bij een eigen huis te komen. In heel Brazilië stegen de huren met 9,13% in de 12 maanden tot september 2026, het dubbele van de officiële inflatie.'),
        ('A IMOBX quer ajudar inquilinos a se tornarem donos da casa, em bairros onde as pessoas voltam a se conectar.',
         'IMOBX wants to turn renters into owners, in neighbourhoods where people connect again.',
         'IMOBX wil huurders eigenaar maken, in buurten waar mensen weer met elkaar verbonden zijn.'),
    ], ('about.html', 'Por que a IMOBX existe', 'Why IMOBX exists', 'Waarom IMOBX bestaat')),
    ('tour-rent-to-own', ('Do aluguel à casa própria', 'From rent to ownership', 'Van huur naar eigendom'), [
        ('No aluguel com compra que planejamos, a família se muda sem dar entrada, e parte de cada pagamento mensal vai para comprá-la.',
         'With rent-to-own as we plan it, a family moves in without a down payment, and part of every monthly payment goes towards buying it.',
         'Bij de huurkoop die we plannen, betrekt een gezin een huis zonder aanbetaling, en een deel van elke maandelijkse betaling gaat naar de aankoop ervan.'),
        ('O preço, o pagamento mensal e quanto dele conta para a compra ficam combinados por escrito antes de a família se mudar.',
         'The price, the monthly payment and how much of it counts towards buying are agreed in writing before the family moves in.',
         'De prijs, de maandelijkse betaling en hoeveel daarvan meetelt voor de aankoop worden schriftelijk afgesproken voordat het gezin erin trekt.'),
    ], ('rent-to-own.html', 'Como funciona o aluguel com compra', 'How rent-to-own works', 'Zo werkt huurkoop')),
    ('tour-builder', ('Construído pela equipe do Rafael', 'Built by Rafael’s team', 'Gebouwd door het team van Rafael'), [
        ('Rafael, um dos fundadores, é engenheiro civil e tem a sua própria construtora. O preço dela é ligado ao índice público de custo da construção do Rio (CUB).',
         'Rafael, one of the founders, is a civil engineer with his own construction company. Its price is tied to Rio’s public building-cost index (CUB).',
         'Rafael, een van de oprichters, is civiel ingenieur met een eigen bouwbedrijf. De prijs is gekoppeld aan de openbare bouwkostenindex van Rio (CUB).'),
        ('Planejamos começar com uma família, muito provavelmente no apartamento do Rafael em Guadalupe, e depois construir alguns apartamentos de cada vez.',
         'We plan to start with one family, most likely in Rafael’s flat in Guadalupe, and then build a few flats at a time.',
         'We willen beginnen met één gezin, hoogstwaarschijnlijk in Rafaels appartement in Guadalupe, en daarna telkens een paar appartementen bouwen.'),
    ], ('roadmap.html#homes', 'Onde a primeira família vai morar', 'Where the first family will live', 'Waar het eerste gezin gaat wonen')),
    ('tour-neighbourhood', ('Uma voz no bairro, e contas abertas', 'A say in the neighbourhood, and open books', 'Inspraak in de buurt, en open boeken'), [
        ('Planejamos fundar a IMOBX como uma cooperativa habitacional, em que cada membro tem o mesmo peso nas decisões. Quem mora ali decide junto como o lugar funciona.',
         'We plan to found IMOBX as a housing cooperative, in which each member has an equal say in decisions. The people who live there decide together how the place is run.',
         'We willen IMOBX oprichten als wooncoöperatie, waarin elk lid evenveel inspraak heeft. De bewoners beslissen samen hoe de plek wordt beheerd.'),
        ('Cada pagamento que a IMOBX faz, e quem o aprovou, fica aberto para qualquer pessoa conferir num livro de contas aberto na internet. Os contratos e os dados pessoais das famílias ficam privados.',
         'Each payment IMOBX makes, and who approved it, is open for anyone to check in an open ledger on the internet. Families’ contracts and personal data stay private.',
         'Elke betaling die IMOBX doet, en wie die goedkeurde, is voor iedereen te controleren in een openbaar grootboek op internet. De contracten en persoonsgegevens van gezinnen blijven privé.'),
        ('O contrato de moradia de uma família só muda quando a família e a IMOBX concordam, dentro da lei brasileira.',
         'A family’s housing agreement changes only when the family and IMOBX both agree, under Brazilian law.',
         'De woonovereenkomst van een gezin verandert alleen als het gezin en IMOBX het allebei eens zijn, volgens de Braziliaanse wet.'),
    ], ('governance.html#cooperative', 'Por que uma cooperativa', 'Why a cooperative', 'Waarom een coöperatie')),
    ('tour-take-part', ('Onde estamos, e como participar', 'Where we are, and how to take part', 'Waar we staan, en hoe je meedoet'), [
        ('A IMOBX está em preparação, e a sua cooperativa ainda vai ser fundada. Buscamos a primeira família, a primeira casa e as pessoas que vão fundar a cooperativa com a gente. Se você é uma família procurando moradia, tem um terreno ou uma casa, constrói, financia ou é um vizinho que quer que isso exista, queremos conhecer você.',
         'IMOBX is in preparation, and its cooperative is still to be founded. We are looking for the first family, the first house and the people who will found the cooperative with us. If you are a family looking for a home, someone with land or a house, a builder, a funder or a neighbour who wants this to exist, we would like to meet you.',
         'IMOBX is in voorbereiding, en de coöperatie moet nog worden opgericht. We zoeken het eerste gezin, het eerste huis en de mensen die de coöperatie samen met ons oprichten. Ben je een gezin dat een woning zoekt, heb je grond of een huis, ben je bouwer, financier of een buur die dit wil zien ontstaan, dan maken we graag kennis.'),
    ], ('contact.html#apresentacao', 'Apresente-se', 'Introduce yourself', 'Stel je voor', 'tour-cta')),
]


def build_tour(root, page, version):
    body = '<main class="paper guide-paper tour-page" id="main">'
    body += _text('h1', 'Conheça a IMOBX', 'Take a tour of IMOBX', 'Ontdek IMOBX')
    for ident, heading, paragraphs, link in STEPS:
        body += f'<section data-tour-step id="{ident}">' + _text('h2', *heading)
        body += ''.join(_text('p', *p) for p in paragraphs)
        body += '<p>' + _link(link[0], *link[1:4], cls=link[4] if len(link) > 4 else '') + '</p></section>'
    body += '</main>'
    (root / 'tour.html').write_text(page('IMOBX | Take a tour', body, '<link rel="stylesheet" href="assets/tour.css">', version=version,
                                         lang='pt-BR', title_pt='IMOBX | Conheça a IMOBX'),
                                    encoding='utf-8')
