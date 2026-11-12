"""Search titles, descriptions and link previews for the reader pages (owner, 28 Oct 2026: SEO step 2).

Runs after the pages are built, before the Dutch step: the <title> and description are Portuguese first (Google shows
the site in Portuguese), the body carries the English title for the language switch, and add_dutch.py adds the Dutch.
Link previews (WhatsApp, Telegram) use the same lines and the village drawing. Lines: SEO_TITLES_DESCRIPTIONS_DRAFT_2026-10-28.md.
"""
import html
import re
from pathlib import Path

LIVE = 'https://imobx.org/'
IMAGE = LIVE + 'assets/homepage.jpg'

# file: (title PT, title EN, description PT)
PAGES = {
    'index.html': ('IMOBX Rio: aluguel com opção de compra, sem entrada', 'IMOBX Rio: rent-to-own houses, no down payment',
                   'Estamos preparando moradias com aluguel e compra para famílias no Rio de Janeiro, como cooperativa de bairro. Em preparação: ainda não há casas à venda.'),
    'rent-to-own.html': ('Como funciona o aluguel com compra da casa · IMOBX Rio', 'How rent-to-own would work · IMOBX Rio',
                         'Parte de cada pagamento mensal vai para a compra da casa, sem entrada. Veja como seriam o preço, os reparos e a saída.'),
    'costs-and-funding.html': ('Custos e recursos: quanto custa uma casa e para onde vão os recursos · IMOBX Rio', 'Costs and funding: what a house costs and where the funding goes · IMOBX Rio',
                          'Os custos de construção, a ordem em que o recurso é gasto e quem pode financiar a primeira etapa.'),
    'project-development.html': ('Desenvolvimento do projeto: onde a IMOBX está agora e o que vem depois · IMOBX Rio', 'Project development: where IMOBX is now, and what comes next · IMOBX Rio',
                     'A etapa atual do projeto, as três etapas de crescimento e o que ainda não está decidido.'),
    'distributed-ledger.html': ('Registro distribuído: como funcionaria um bairro na blockchain? · IMOBX Rio', 'Distributed ledger: how would a neighbourhood work on a blockchain? · IMOBX Rio',
                        'Pagamentos e aprovações registrados para os moradores conferirem; dados pessoais e contratos ficam privados. Em preparação.'),
    'governance.html': ('Governança local: quem decide, e quando você tem voz? · IMOBX Rio', 'Local governance: who decides, and when do you get a say? · IMOBX Rio',
                        'Hoje os fundadores decidem. No plano, quem tem o token vota as regras do token, e os membros decidem um membro, um voto.'),
    'properties.html': ('Lofts e terreno: desenhos e fotos · IMOBX Rio', 'Lofts and site: drawings and photos · IMOBX Rio',
                        'Os dois lofts da construtora do Rafael e a vila que ele imagina para mais adiante. Estudos de projeto, não anúncios de casas.'),
    'resources.html': ('Recursos: documentos e fontes da IMOBX · IMOBX Rio', 'Resources: IMOBX documents and sources · IMOBX Rio',
                       'Os documentos do projeto para baixar, as ideias que formaram a IMOBX, quem faz o quê e as fontes de cada fato.'),
    'tour.html': ('Conheça a IMOBX · IMOBX Rio', 'Take a tour of IMOBX · IMOBX Rio',
                  'Um passeio pela IMOBX: a necessidade, o aluguel com compra, quem constrói, as contas abertas, a reunião no pátio, o token e como participar.'),
    'about.html': ('Sobre a IMOBX: por que existe e quem a começou · IMOBX Rio', 'About IMOBX: why it exists and who started it · IMOBX Rio',
                   'Por que a IMOBX existe, quem a começou, o que queremos construir e como funcionaria o aluguel com compra no Rio.'),
    'contact.html': ('Participar da IMOBX · IMOBX Rio', 'Take part in IMOBX · IMOBX Rio',
                     'Entre em contato com a IMOBX sobre moradia, parcerias ou financiamento.'),
    'self-compounding.html': ('Self-compounding: o token de financiamento comunitário da IMOBX · IMOBX Rio', 'Self-compounding: the IMOBX community-funding token · IMOBX Rio',
                 'Como o token opcional da IMOBX funciona: cada negociação paga uma taxa que financia a comunidade. As famílias nunca precisam dele.'),
    'jobs.html': ('Vagas: apoio à captação de recursos · IMOBX Rio', 'Jobs: fundraising support · IMOBX Rio',
                 'Uma vaga remota de apoio à captação de recursos da IMOBX.'),
    'why.html': ('Por que moradia: aluguel, entrada e déficit no Brasil · IMOBX Rio', 'Why housing: rent, down payments and the shortage in Brazil · IMOBX Rio',
                 'Por que tantas famílias pagam aluguel e não conseguem comprar: os números e as fontes.'),
}


def add_seo(root):
    root = Path(root)
    esc = lambda s: html.escape(s, quote=True)
    for name, (title_pt, title_en, description) in PAGES.items():
        path = root / name
        if not path.exists():
            continue
        text = path.read_text(encoding='utf-8')
        url = LIVE if name == 'index.html' else LIVE + name
        text = re.sub(r'<title>.*?</title>', f'<title>{esc(title_pt)}</title>', text, count=1, flags=re.S)
        # one description and one set of preview tags, replaced on every build
        text = re.sub(r'\s*<meta name="description"[^>]*>', '', text)
        text = re.sub(r'\s*<meta (?:property="og:[^"]*"|name="twitter:[^"]*")[^>]*>', '', text)
        text = re.sub(r'\s*<link rel="canonical"[^>]*>', '', text)
        tags = (f'<meta name="description" content="{esc(description)}"><link rel="canonical" href="{url}">'
                f'<meta property="og:type" content="website"><meta property="og:site_name" content="IMOBX Rio">'
                f'<meta property="og:locale" content="pt_BR"><meta property="og:url" content="{url}">'
                f'<meta property="og:title" content="{esc(title_pt)}"><meta property="og:description" content="{esc(description)}">'
                f'<meta property="og:image" content="{IMAGE}"><meta name="twitter:card" content="summary_large_image">')
        text = text.replace('</title>', '</title>' + tags, 1)
        # the language switch reads the body's titles; Dutch comes from add_dutch.py
        def body(m):
            attrs = re.sub(r'\s*data-title-(?:pt|en|nl)="[^"]*"', '', m.group(1))
            return f'<body{attrs} data-title-pt="{esc(title_pt)}" data-title-en="{esc(title_en)}">'
        text = re.sub(r'<body([^>]*)>', body, text, count=1)
        path.write_text(text, encoding='utf-8')
