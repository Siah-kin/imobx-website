"""Search titles, descriptions and link previews for the reader pages (owner, 28 Oct 2026: SEO step 2).

Runs after the pages are built, before the Dutch step: the <title> and description are Portuguese first (Google shows
the site in Portuguese), the body carries the English title for the language switch, and add_dutch.py adds the Dutch.
Link previews (WhatsApp, Telegram) use the same lines and the village drawing. Lines: SEO_TITLES_DESCRIPTIONS_DRAFT_2026-10-28.md.
"""
import html
import re
from pathlib import Path

LIVE = 'https://siah-kin.github.io/imobx-website/'
IMAGE = LIVE + 'assets/homepage.jpg'

# file: (title PT, title EN, description PT)
PAGES = {
    'index.html': ('IMOBX Rio: aluguel com opção de compra, sem entrada', 'IMOBX Rio: rent-to-own houses, no down payment',
                   'Estamos preparando moradias com aluguel e compra para famílias no Rio de Janeiro, como cooperativa de bairro. Em preparação: ainda não há casas à venda.'),
    'rent-to-own.html': ('Como funciona o aluguel com compra da casa · IMOBX Rio', 'How rent-to-own would work · IMOBX Rio',
                         'Parte de cada pagamento mensal vai para a compra da casa, sem entrada. Veja como seriam o preço, os reparos e a saída.'),
    'transparency.html': ('Quanto custa uma casa e para onde vão os recursos · IMOBX Rio', 'What a home costs and where the funding goes · IMOBX Rio',
                          'Os custos de construção, a ordem em que o recurso é gasto e quem pode financiar a primeira etapa.'),
    'roadmap.html': ('Onde estamos e o que vem depois · IMOBX Rio', 'Where we are and what comes next · IMOBX Rio',
                     'A etapa atual do projeto, as próximas três etapas e o que ainda não está decidido.'),
    'blockchain.html': ('Como funcionaria um bairro na blockchain · IMOBX Rio', 'How would a neighbourhood work on a blockchain? · IMOBX Rio',
                        'Pagamentos e aprovações registrados para os moradores conferirem; dados pessoais e contratos ficam privados. Ainda não está em funcionamento.'),
    'governance.html': ('Quem decide na IMOBX, e quando você tem voz · IMOBX Rio', 'Who decides in IMOBX, and when you get a say · IMOBX Rio',
                        'Hoje os fundadores decidem; depois, quem tem o token decide as regras do token, e os membros da cooperativa decidem um membro, um voto.'),
    'properties.html': ('Lofts e terreno: desenhos e fotos · IMOBX Rio', 'Lofts and site: drawings and photos · IMOBX Rio',
                        'O protótipo de dois lofts e o projeto da primeira vila. Estudos de projeto, não anúncios de casas.'),
    'resources.html': ('Documentos do projeto · IMOBX Rio', 'Project documents · IMOBX Rio',
                       'O documento do projeto, a apresentação e as fontes, para baixar.'),
    'contact.html': ('Participe da IMOBX Rio: apresente-se no Telegram', 'Take part in IMOBX Rio: introduce yourself on Telegram',
                     'Proprietários, construtoras, profissionais, financiadores e famílias: apresente-se no grupo da IMOBX.'),
    'why.html': ('Por que moradia: aluguel, entrada e déficit no Brasil · IMOBX Rio', 'Why housing: rent, down payments and the shortage in Brazil · IMOBX Rio',
                 'Por que tantas famílias pagam aluguel e não conseguem comprar: os números e as fontes.'),
    'reference.html': ('Quem prepara a IMOBX e as fontes · IMOBX Rio', 'Who is preparing IMOBX, and the sources · IMOBX Rio',
                       'As pessoas, as responsabilidades e as fontes de cada afirmação do projeto.'),
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
