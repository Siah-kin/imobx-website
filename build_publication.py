"""Build static reading/presentation exports. Not imported by the Telegram bot."""
from pathlib import Path
import html
import json
import re
import xml.etree.ElementTree as ET
import zipfile
from urllib.parse import urljoin
from model_guide import build_guide, redirect_stub, new_faq_location, partner_line_html
from archive_gateway import build_gateway, pages_from_pdf
from contact_page import build_contact
from project_reference import build_reference, write_manifest, VERSION, REVIEW_DATE, DATE_PT, DATE_EN, LABEL_EN, LABEL_PT
from copy_review import require_review

import markdown
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parent
PREVIEW_ONLY = require_review(ROOT)
INK = '#193d4e'
ACCENT = '#276578'
MUTED = '#596772'
PAPER = '#ffffff'
LINE = '#dae2e6'


def esc(value):
    return html.escape(str(value), quote=True)


def version_label(item, lang):
    """'Version 0.8, 24 October 2026'. Items that were not revised on that date show only their version."""
    word, date = ('Versão', DATE_PT) if lang == 'pt' else ('Version', DATE_EN)
    return f"{word} {item['version']}" + (f', {date}' if item['version'] == VERSION else '')


MONTHS_PT = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto',
             'setembro', 'outubro', 'novembro', 'dezembro']
MONTHS_EN = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
             'September', 'October', 'November', 'December']


# The date the site's pages last changed. The documents keep their own date (REVIEW_DATE).
SITE_UPDATED = '2026-10-27'


def status_bar_text():
    """Visitor-facing status bar: the project status and the date the site last changed, without a version number."""
    year, month, day = (int(part) for part in SITE_UPDATED.split('-'))
    pt = f'Em preparação · atualizado em {day:02d}/{month:02d}/{year}'
    en = f'In preparation · updated {day} {MONTHS_EN[month - 1][:3]} {year}'
    return pt, en


def site_header(lang='pt-BR', current=''):
    """One main menu; local section links belong inside each page."""
    portuguese = lang.startswith('pt')
    items = [
        ('index.html', 'O projeto', 'The project'),
        ('rent-to-own.html', 'Como funciona', 'How it works'),
        ('roadmap.html', 'Etapas do projeto', 'Project stages'),
        ('transparency.html', 'Financiamento e gastos', 'Funding and spending'),
        ('blockchain.html', 'Registros compartilhados', 'Shared records'),
        ('properties.html', 'Desenhos e fotos', 'Drawings and photos'),
        ('resources.html', 'Documentos', 'Documents'),
        ('contact.html', 'Participar', 'Take part'),
    ]
    links = ''
    for target, pt, en in items:
        active = ' aria-current="page"' if target == current else ''
        links += f'<a href="{target}" data-pt="{esc(pt)}" data-en="{esc(en)}"{active}>{esc(pt if portuguese else en)}</a>'
    return ('<header class="top site-header"><nav class="wrap site-nav" data-site-nav '
            'aria-label="Principal" data-aria-pt="Principal" data-aria-en="Main">'
            '<a class="wordmark" href="index.html" aria-label="IMOBX"><img class="brand-logo" '
            'src="assets/imobx-logo-light.png" width="94" height="94" alt="IMOBX"></a>'
            '<button type="button" class="menu-toggle" aria-expanded="false" aria-controls="site-links" '
            'data-pt="Menu" data-en="Menu">Menu</button>'
            '<div class="site-links" id="site-links">' + links + '</div>'
            '<div class="lang" role="group" aria-label="Idioma / Language / Taal">'
            f'<button type="button" data-language="pt" aria-pressed="{str(portuguese).lower()}" aria-label="Português brasileiro">PT</button>'
            f'<button type="button" data-language="en" aria-pressed="{str(not portuguese).lower()}" aria-label="English">EN</button>'
            '<button type="button" data-language="nl" aria-pressed="false" aria-label="Nederlands">NL</button>'
            '</div></nav></header>')


SITE_FOOTER = '<footer class="footer site-footer"><div class="wrap"><p data-pt="IMOBX · Rio de Janeiro. Projeto de moradia em preparação por Rafael Britto, fundador, e John (comunicação e ferramentas digitais). A forma jurídica da organização ainda está sendo definida." data-en="IMOBX · Rio de Janeiro. A housing project being prepared by Rafael Britto, founder, and John (communication and digital tools). The organisation’s legal form is still being defined.">IMOBX · Rio de Janeiro. Projeto de moradia em preparação por Rafael Britto, fundador, e John (comunicação e ferramentas digitais). A forma jurídica da organização ainda está sendo definida.</p><p><a href="transparency.html" data-pt="Financiamento e gastos" data-en="Funding and spending">Financiamento e gastos</a>&nbsp;· <a href="reference.html#people" data-pt="Pessoas e responsabilidades" data-en="People and responsibilities">Pessoas e responsabilidades</a>&nbsp;· <a href="resources.html" data-pt="Documentos para baixar" data-en="Documents to download">Documentos para baixar</a>&nbsp;· <a href="contact.html" data-pt="Participar" data-en="Take part">Participar</a></p></div></footer>'


def page(title, body, script='', version='0.1', lang='en', title_pt=None, head='', description=None):
    if 'id="main"' not in body:
        body = re.sub(r'<main(?![^>]*\bid=)', '<main id="main"', body, count=1)
    if 'assets/site.js' not in script:
        script += '<script src="assets/site.js" defer></script>'
    description = description or 'IMOBX housing pilot: model, roadmap and project resources.'
    current = {'IMOBX | Proposed Rio housing pilot': 'index.html',
               'IMOBX | Resources': 'resources.html', 'IMOBX | Funding and spending': 'transparency.html',
               'IMOBX | Roadmap': 'roadmap.html', 'IMOBX | IMOBX roadmap': 'roadmap.html', 'IMOBX | Project stages': 'roadmap.html', 'IMOBX | Blockchain': 'blockchain.html',
               'IMOBX | Renting and buying a home': 'rent-to-own.html',
               'IMOBX | Take part': 'contact.html', 'IMOBX | The token': 'transparency.html'}.get(title, '')
    document = f'''<!doctype html>
<html lang="{esc(lang)}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{esc(description)}">
<title>{esc(title_pt if lang.startswith('pt') and title_pt else title)}</title><link rel="icon" href="assets/imobx-logo-light.png" type="image/png"><link rel="stylesheet" href="assets/style.css"><link rel="stylesheet" href="assets/brand.css">{script}{head}</head>
<body data-title-pt="{esc(title_pt or title)}" data-title-en="{esc(title)}"><div class="review" data-pt="{esc(status_bar_text()[0])}" data-en="{esc(status_bar_text()[1])}">{esc(status_bar_text()[0] if lang.startswith('pt') else status_bar_text()[1])}</div>
<a href="#main" class="skip" data-pt="Pular para o conteúdo" data-en="Skip to content">{'Pular para o conteúdo' if lang.startswith('pt') else 'Skip to content'}</a>
{site_header(lang, current)}
{body}
{SITE_FOOTER}</body></html>'''
    # Text sources owned by other work (whitepaper, pilot guide, project reference) may still link to the retired faq.html.
    return re.sub(r'href="(faq\.html[^"]*)"', lambda m: 'href="' + new_faq_location(m.group(1)) + '"', document)


RESOURCE_CATALOG = [
    {'id': 'media-kit', 'pt': 'Media kit IMOBX', 'en': 'IMOBX media kit', 'version': '0.2',
     'description_pt': 'Logos para fundos claros e escuros, cores e guia de uso da marca.',
     'description_en': 'Logos for light and dark backgrounds, colours and brand usage guide.',
     'meta_pt': 'Guia em inglês · descrições PT/EN', 'meta_en': 'English guide · PT/EN descriptions',
     'links': [('media-kit.html','Ver o kit','View kit'), ('media-kit.zip','Baixar kit (ZIP)','Download kit (ZIP)')]},
    {'id': 'whitepaper', 'pt': 'Whitepaper', 'en': 'Whitepaper', 'version': VERSION,
     'description_pt': 'Modelo de moradia, custos, contratos, fluxo de caixa e decisões em aberto.',
     'description_en': 'Housing model, costs, agreements, cash flow and open decisions.',
     'meta_pt': 'Inglês · rascunho de referência', 'meta_en': 'English · reference draft',
     'archive': True, 'links': [('whitepaper.pdf','PDF','PDF'), ('whitepaper.md','Texto editável','Editable text')]},
    {'id': 'pitchdeck', 'pt': 'Pitch deck', 'en': 'Pitch deck', 'version': VERSION,
     'description_pt': 'Apresentação para parceiros, com notas para quem apresenta.',
     'description_en': 'Partner presentation with presenter notes.',
     'meta_pt': '12 slides · inglês · rascunho', 'meta_en': '12 slides · English · draft',
     'archive': True, 'links': [('pitchdeck.pdf','PDF','PDF'),
               ('pitchdeck.pptx','PowerPoint','PowerPoint'), ('pitchdeck.md','Texto e notas','Text and notes')]},
    {'id': 'devsheet', 'pt': 'Guia do piloto e da construção', 'en': 'Pilot and building guide', 'version': VERSION,
     'description_pt': 'Planos de moradia, participação dos moradores e etapas de desenvolvimento propostas.',
     'description_en': 'Housing plans, resident participation and proposed development stages.',
     'meta_pt': 'Inglês · processo proposto', 'meta_en': 'English · proposed process',
     'archive': True, 'links': [('devsheet.pdf','PDF','PDF'), ('devsheet.md','Texto editável','Editable text')]},
    {'id': 'transparency', 'pt': 'Financiamento e gastos', 'en': 'Funding and spending', 'version': '0.1',
     'description_pt': 'Fontes de financiamento, despesas previstas e como os participantes poderiam conferir as contas.',
     'description_en': 'Funding sources, planned spending and how participants could check the accounts.',
     'meta_pt': 'Português e inglês · planos e fontes',
     'meta_en': 'Portuguese and English · plans and sources',
     'links': [('transparency.html','Ver a página','View page')]},
]
RESOURCE_CATALOG[-1]['version'] = VERSION
RESOURCE_CATALOG.insert(0, {
    'id': 'housing', 'pt': 'Aluguel e compra da casa', 'en': 'Renting and buying the home', 'version': VERSION,
    'description_pt': 'Como os pagamentos contariam para a compra, quem cuidaria dos reparos e o que os moradores poderiam decidir.',
    'description_en': 'How payments would count towards purchase, who would handle repairs and what residents could decide.',
    'meta_pt': 'Português e inglês · modelo proposto', 'meta_en': 'Portuguese and English · housing plan',
    'links': [('rent-to-own.html', 'Ler a explicação', 'Read the explanation')]
})
RESOURCE_CATALOG.append({
    'id': 'reference', 'pt': 'Referência atual do projeto', 'en': 'Current project reference', 'version': VERSION,
    'description_pt': 'Situação, responsabilidades, fontes e mapa dos capítulos do documento de Rafael.',
    'description_en': 'Status, responsibilities, sources and a chapter map for Rafael’s manuscript.',
    'meta_pt': 'Português e inglês', 'meta_en': 'Portuguese and English',
    'links': [('reference.html', 'Ler a referência', 'Read the reference'),
              ('project-reference-pt.pdf', 'PDF em português', 'Portuguese PDF'),
              ('project-reference-en.pdf', 'PDF em inglês', 'English PDF'),
              ('project-reference-pt.md', 'Texto editável PT', 'Editable text PT'),
              ('project-reference-en.md', 'Texto editável EN', 'Editable text EN')]
})


def translated(pt, en, tag='span', attributes=''):
    return f'<{tag} data-pt="{esc(pt)}" data-en="{esc(en)}" {attributes}>{esc(pt)}</{tag}>'


def resource_section(standalone=False):
    catalog = {item['id']: item for item in RESOURCE_CATALOG}
    document_ids = ('whitepaper', 'pitchdeck', 'devsheet')

    def card(item, level='h3'):
        actions = []
        for target, pt, en in item['links']:
            download = ' download' if '#' not in target and not target.endswith('.html') else ''
            actions.append(translated(pt, en, 'a', f'href="{esc(target)}" aria-label="{esc(item["pt"] + ": " + pt)}" data-aria-pt="{esc(item["pt"] + ": " + pt)}" data-aria-en="{esc(item["en"] + ": " + en)}"{download}'))
        return f'''<article class="resource-card" id="resource-{esc(item['id'])}" aria-labelledby="title-{esc(item['id'])}">
{translated(item['pt'], item['en'], level, f'id="title-{item["id"]}"')}
{translated(item['description_pt'], item['description_en'], 'p')}
<p class="resource-meta">{translated(version_label(item, 'pt') + ' · ' + item['meta_pt'], version_label(item, 'en') + ' · ' + item['meta_en'])}</p>
<div class="resource-actions">{''.join(actions)}</div></article>'''

    intro_pt = 'O whitepaper apresenta a proposta de moradia e seu financiamento. O pitch deck resume o projeto para parceiros. O guia do piloto detalha o trabalho e as responsabilidades. Os três documentos são rascunhos em inglês.'
    intro_en = 'The whitepaper explains the housing proposal and its funding. The pitch deck presents the project to partners. The pilot and building guide covers the work and responsibilities. All three documents are English drafts.'
    body = '<section class="content wrap" id="documentos"><span id="resources"></span><span id="recursos"></span>'
    body += translated('Documentos do projeto', 'Project documents', 'h1' if standalone else 'h2')
    if standalone:
        # attention pass (owner-approved package, 25 Oct): the first sentence as the card, one orange action
        first_pt, rest_pt = intro_pt.split('. ', 1); first_en, rest_en = intro_en.split('. ', 1)
        body += '<div class="key-card">' + translated(first_pt + '.', first_en + '.', 'p') + '</div>' + translated(rest_pt, rest_en, 'p')
        body += '<p class="page-action">' + translated('Ir para o download do whitepaper', 'Go to the whitepaper download', 'a', 'class="button act" href="whitepaper.html"') + '</p>'
    else:
        body += translated(intro_pt, intro_en, 'p')
    if not standalone:
        rows = []
        for key in document_ids:
            item = catalog[key]
            target, pt, en = item['links'][0]
            rows.append(f'''<article class="resource-row" id="resource-{esc(key)}">
<div>{translated(item['pt'], item['en'], 'h3')}{translated(item['description_pt'], item['description_en'], 'p')}</div>
{translated(pt, en, 'a', f'href="{esc(target)}" aria-label="{esc(item["pt"])}" data-aria-pt="{esc(item["pt"])}" data-aria-en="{esc(item["en"])}"')}</article>''')
        body += '<div class="resource-rows">' + ''.join(rows) + '</div><div class="resource-more">'
        body += translated('Todos os documentos e downloads', 'All documents and downloads', 'a', 'href="resources.html"')
        body += translated('Aluguel e compra da casa', 'Renting and buying the home', 'a', 'id="resource-housing" href="rent-to-own.html"')
        body += translated('Financiamento e gastos', 'Funding and spending', 'a', 'href="transparency.html"')
        body += translated('Referência atual do projeto', 'Current project reference', 'a', 'href="reference.html"')
        body += translated('Roteiro e decisões compartilhadas', 'Roadmap and shared decisions', 'a', 'href="roadmap.html"')
        body += translated('Perguntas das famílias', 'Questions families ask', 'a', 'href="rent-to-own.html#questions"')
        return body + '</div>'

    body += '<div class="resource-grid">' + ''.join(card(catalog[key], 'h2') for key in ('reference',) + document_ids) + '</div>'
    body += '<section id="media-resources" aria-labelledby="media-resources-title">'
    body += translated('Materiais para divulgação', 'Media resources', 'h2', 'id="media-resources-title"')
    body += '<div class="resource-grid">' + card(catalog['media-kit']) + '</div></section>'
    body += '<section id="website-pages" aria-labelledby="website-pages-title">'
    body += translated('No site', 'On the website', 'h2', 'id="website-pages-title"')
    body += '<div class="resource-more">'
    for key in ('housing', 'transparency'):
        item = catalog[key]
        target = item['links'][0][0]
        body += f'<span id="title-{key}">' + translated(item['pt'], item['en'], 'a', f'id="resource-{key}" href="{esc(target)}"') + '</span>'
    body += translated('Roteiro e decisões compartilhadas', 'Roadmap and shared decisions', 'a', 'href="roadmap.html"')
    body += translated('Perguntas das famílias', 'Questions families ask', 'a', 'href="rent-to-own.html#questions"')
    body += translated('Participar', 'Take part', 'a', 'href="contact.html"') + '</div>'
    body += '<nav class="archive-nav" aria-label="Contexto do projeto" data-aria-pt="Contexto do projeto" data-aria-en="Project background">'
    body += translated('Por que a IMOBX existe', 'Why IMOBX exists', 'a', 'href="index.html#missao"')
    body += translated('A visão de Rafael para a vila', 'Rafael’s village vision', 'a', 'href="properties.html#visao-rafael"')
    body += translated('Pessoas e responsabilidades', 'People and responsibilities', 'a', 'href="reference.html#people"')
    body += translated('Fontes da proposta', 'Sources behind the proposal', 'a', 'href="reference.html#sources"') + '</nav></section>'
    body += '<div class="resource-more">'
    body += translated('Fontes e mapa de capítulos do documento do projeto', 'Sources and chapter map for the project paper', 'a', 'href="reference.html#chapters"')
    body += translated('Para desenvolvedores: o texto do site como dados (JSON)', 'For developers: the site’s text as data (JSON)', 'a', 'href="model-guide.json" download')
    body += translated('Baixar documentos e logos (ZIP)', 'Download documents and logos (ZIP)', 'a', 'href="imobx-documents.zip" download')
    return body + '</div>'


# The homepage is built whole from its copy table (owner-approved mock, 26 Oct 2026): home_page.py.
import hashlib as _hashlib
from home_page import build_home
build_home(ROOT, page, lambda name: f'assets/{name}?v=' + _hashlib.sha256((ROOT / 'assets' / name).read_bytes()).hexdigest()[:10])

for name in ['index.html', 'properties.html']:
    target = ROOT / name
    source, count = re.subn(r'<header class="top(?: site-header)?">.*?</header>',
                           lambda _: site_header('pt-BR', name),
                           target.read_text(), count=1, flags=re.S)
    if count != 1:
        raise ValueError(f'Expected one main header in {name}.')
    review_pt, review_en = status_bar_text()
    source, count = re.subn(r'<div class="review"[^>]*>.*?</div>',
        lambda _: f'<div class="review" data-pt="{esc(review_pt)}" data-en="{esc(review_en)}">{esc(review_pt)}</div>',
        source, count=1, flags=re.S)
    if count != 1:
        raise ValueError(f'Expected one review date in {name}.')
    source, count = re.subn(r'<footer class="footer(?: site-footer)?">.*?</footer>', lambda _: SITE_FOOTER, source, count=1, flags=re.S)
    if count != 1:
        raise ValueError(f'Expected one footer in {name}.')
    source, count = re.subn(r'<p class="partner-line">.*?</p>',
                           lambda _: partner_line_html(name, lambda pair, tag='p', attrs='': translated(*pair, tag, attrs)),
                           source, count=1, flags=re.S)
    # 25 Oct 2026: the partner links live once, in the footer; pages no longer carry their own partner line.
    target.write_text(source)


language_controls = ''  # The shared header contains the single language control.
build_guide(ROOT, page, translated, esc, language_controls)
build_reference(ROOT, page, translated, esc)
build_contact(ROOT, page, translated, esc, VERSION)
(ROOT / 'resources.html').write_text(page('IMOBX | Resources',
    '<main id="main">' + language_controls + resource_section(standalone=True) + '</section>'
    + partner_line_html('resources.html', lambda pair, tag='p', attrs='': translated(*pair, tag, attrs)) + '</main>',
    '<script src="assets/site.js" defer></script>', version=VERSION, lang='pt-BR', title_pt='IMOBX | Recursos'))
kit_html = markdown.markdown((ROOT / 'media-kit.md').read_text(), extensions=['tables', 'toc'])
logo_previews = '''<div class="media-logo-grid"><figure class="media-logo light">
<img src="assets/imobx-logo-light.png" width="400" height="400" alt="IMOBX logo on a white background">
<figcaption><a href="assets/imobx-logo-light.png" download>Light logo · PNG</a></figcaption></figure>
<figure class="media-logo light"><img src="assets/imobx-logo-light.png" width="400" height="400" alt="Existing IMOBX house symbol and wordmark">
<figcaption>Original IMOBX identity · white website and document backgrounds</figcaption></figure></div>'''
kit_html = kit_html.replace('<h2', logo_previews + '<h2', 1)
# The brand guide (DESIGN.md) is a section of the media kit; design.html is a redirect stub.
brand_html = markdown.markdown((ROOT / 'DESIGN.md').read_text(), extensions=['tables', 'toc'])
brand_html = re.sub(r'<(/?)h2\b', r'<\1h4', brand_html)
brand_html = re.sub(r'<(/?)h1\b', r'<\1h3', brand_html)
brand_section = ('<section id="brand-guide"><h2>Brand guide</h2>'
                 '<p><a href="DESIGN.md" download>Download design guidelines</a></p>' + brand_html + '</section>')
(ROOT / 'media-kit.html').write_text(page('IMOBX | Media kit',
    '<main class="paper"><p><a href="media-kit.zip" download>Download media kit ZIP</a> · '
    '<a href="media-kit.md" download>Editable guide</a> · <a href="brand-colors.json" download>Brand colours (JSON)</a> · '
    '<a href="#brand-guide">Brand guide</a></p>' + kit_html + brand_section + '</main>', version='0.2'))
(ROOT / 'design.html').write_text(redirect_stub(
    'IMOBX | Design guidelines', 'Design guidelines', 'media-kit.html#brand-guide', 'Open the current version'))


# The whitepaper, pilot guide and deck are English downloads. Their web addresses are download pages that keep every
# old section link; a full build rebuilds the documents and points each section at its page in the new PDF.
paper_html = markdown.markdown((ROOT / 'whitepaper.md').read_text(), extensions=['tables', 'toc'])
devsheet_html = markdown.markdown((ROOT / 'devsheet.md').read_text(), extensions=['tables', 'toc'])
deck = json.loads((ROOT / 'pitchdeck.json').read_text())
deck_md = [f"# {deck['title']}", deck['subtitle'], f"**{deck['status']}**", '']
for number, item in enumerate(deck['slides'], 1):
    deck_md += [f"## {number}. {item['title']}", item['lead'], '', *('- '+b for b in item['bullets']), '',
                *(f"Source: [{x['label']}]({x['url']}). {x['effect']}" for x in item.get('sources', [])),
                '**Presenter notes:** '+item['notes'], '']
(ROOT / 'pitchdeck.md').write_text('\n\n'.join(deck_md) + '\n')
catalog = {item['id']: item for item in RESOURCE_CATALOG}
GATEWAYS = [('whitepaper', 'IMOBX | Whitepaper'), ('devsheet', 'IMOBX | Pilot and building guide'), ('pitchdeck', 'IMOBX | Pitch deck')]
for doc, doc_title in GATEWAYS:
    build_gateway(ROOT, page, translated, esc, catalog[doc], doc, doc_title)

if PREVIEW_ONLY:
    from add_dutch import add_dutch  # the preview gets its Dutch too; a full build adds it again after the exports
    add_dutch(ROOT)
    print('Rendered local HTML for editorial and browser review. Existing exports are unchanged.')
    raise SystemExit(0)

# Fonts are local system fonts, not external requests from the website.
font_candidates = [
    ('/System/Library/Fonts/Supplemental/Arial.ttf', '/System/Library/Fonts/Supplemental/Arial Bold.ttf'),
    ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'),
]
FONT, BOLD = 'Helvetica', 'Helvetica-Bold'
for normal, bold in font_candidates:
    if Path(normal).is_file() and Path(bold).is_file():
        pdfmetrics.registerFont(TTFont('ImobxSans', normal))
        pdfmetrics.registerFont(TTFont('ImobxBold', bold))
        pdfmetrics.registerFontFamily('ImobxSans', normal='ImobxSans', bold='ImobxBold',
                                      italic='ImobxSans', boldItalic='ImobxBold')
        FONT, BOLD = 'ImobxSans', 'ImobxBold'
        break

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='PaperBody', fontName=FONT, fontSize=10, leading=15, spaceAfter=10, textColor=colors.HexColor(INK)))
styles.add(ParagraphStyle(name='PaperTitle', fontName=BOLD, fontSize=38, leading=43, spaceAfter=15, textColor=colors.HexColor(INK)))
styles.add(ParagraphStyle(name='PaperHeading', fontName=BOLD, fontSize=16, leading=21, spaceBefore=17, spaceAfter=10, keepWithNext=True, textColor=colors.HexColor(INK)))
styles.add(ParagraphStyle(name='PaperCell', parent=styles['PaperBody'], fontSize=8.5, leading=12, spaceAfter=0))
styles.add(ParagraphStyle(name='SpecBody', parent=styles['PaperBody'], fontSize=9.5, leading=13, spaceAfter=7))
styles.add(ParagraphStyle(name='SpecTitle', parent=styles['PaperTitle'], fontSize=32, leading=36, spaceAfter=10))
styles.add(ParagraphStyle(name='SpecHeading', parent=styles['PaperHeading'], fontSize=14, leading=18, spaceBefore=10, spaceAfter=8))
styles.add(ParagraphStyle(name='SpecCell', parent=styles['PaperCell'], fontSize=8.5, leading=11))


def inline(element):
    value = ET.tostring(element, encoding='unicode', method='html')
    value = re.sub(r'^<[^>]+>|</[^>]+>$', '', value.strip())
    value = re.sub(r'href="([^"]+)"', lambda m: 'href="' + urljoin('https://siah-kin.github.io/imobx-website/', m[1]) + '"', value)
    return value.replace('<strong>', '<b>').replace('</strong>', '</b>').replace('<em>', '<i>').replace('</em>', '</i>')


def article_story(document_html, compact=False):
    story = []
    style_prefix = 'Spec' if compact else 'Paper'
    for element in ET.fromstring('<root>' + document_html + '</root>'):
        if element.tag == 'h1':
            if element.text == 'IMOBX':
                logo_size = 50 if compact else 84
                logo = Image(str(ROOT / 'assets/imobx-logo-light.png'), width=logo_size, height=logo_size)
                logo.hAlign = 'LEFT'
                story.append(logo)
                story.append(Spacer(1, 4 if compact else 8))
            else:
                story.append(Paragraph(inline(element), styles[style_prefix + 'Title']))
        elif element.tag in ('h2', 'h3'):
            story.append(Paragraph(inline(element), styles[style_prefix + 'Heading']))
        elif element.tag == 'p':
            story.append(Paragraph(inline(element), styles[style_prefix + 'Body']))
        elif element.tag == 'div' and element.get('class') == 'pagebreak':
            story.append(PageBreak())
        elif element.tag in ('ul', 'ol'):
            for number, item in enumerate(element, 1):
                list_prefix = f'{number}. ' if element.tag == 'ol' else '• '
                story.append(Paragraph(list_prefix + inline(item), styles[style_prefix + 'Body']))
        elif element.tag == 'table':
            rows = [[Paragraph(inline(cell), styles[style_prefix + 'Cell']) for cell in row] for row in element.iter('tr')]
            width = 468
            columns = len(rows[0])
            widths = [width * .38] + [width * .62 / (columns - 1)] * (columns - 1)
            table = Table(rows, colWidths=widths, repeatRows=1, hAlign='LEFT')
            table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e8f4f8')),
                ('GRID',(0,0),(-1,-1),.4,colors.HexColor(LINE)),('VALIGN',(0,0),(-1,-1),'TOP'),
                ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
                ('TOPPADDING',(0,0),(-1,-1),5 if compact else 7),('BOTTOMPADDING',(0,0),(-1,-1),5 if compact else 7)]))
            story.extend([table, Spacer(1,8 if compact else 12)])
    return story


def paper_footer(c, doc):
    c.setFillColor(colors.white)
    c.rect(0, 0, 594, 842, fill=1, stroke=0)
    c.setStrokeColor(colors.HexColor(LINE))
    c.line(63, 46, 531, 46)
    c.setFont(FONT,8)
    c.setFillColor(colors.HexColor(MUTED))
    c.drawString(63,31,doc.imobx_label)
    c.drawRightString(531,31,str(doc.page))


for name, content, label, title in [
    ('whitepaper', paper_html, f'IMOBX / PROJECT PROPOSAL / {LABEL_EN}', 'IMOBX project paper v' + VERSION),
    ('devsheet', devsheet_html, f'IMOBX / PILOT AND BUILDING GUIDE / {LABEL_EN}', 'IMOBX pilot and building guide v' + VERSION),
    *[(f'project-reference-{lang}', markdown.markdown((ROOT / f'project-reference-{lang}.md').read_text(), extensions=['tables']),
       f'IMOBX / {lang.upper()} / {LABEL_PT if lang == "pt" else LABEL_EN}', f'IMOBX project reference / {lang.upper()} / v{VERSION}')
      for lang in ['pt', 'en']],
]:
    document = SimpleDocTemplate(str(ROOT / (name + '.pdf')), pagesize=(594,842), rightMargin=63, leftMargin=63,
                                 topMargin=55,bottomMargin=62,title=title,author='IMOBX draft')
    document.imobx_label = label
    document.build(article_story(content, compact=(name == 'devsheet')),onFirstPage=paper_footer,onLaterPages=paper_footer)

# Editable 16:9 PowerPoint with speaker notes.
presentation = Presentation()
presentation.slide_width = Inches(13.333)
presentation.slide_height = Inches(7.5)
presentation.core_properties.title = 'IMOBX | Partner discussion draft'
presentation.core_properties.subject = 'Proposed Rio rent-to-own housing pilot'


def ppt_text(slide, text, x, y, width, height, size, color=INK, bold=False, family='Arial'):
    box = slide.shapes.add_textbox(Inches(x),Inches(y),Inches(width),Inches(height))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = 0
    tf.margin_left = tf.margin_right = 0
    paragraph = tf.paragraphs[0]
    paragraph.text = text
    paragraph.font.name = family
    paragraph.font.size = Pt(size)
    paragraph.font.bold = bold
    paragraph.font.color.rgb = RGBColor.from_string(color.lstrip('#'))
    return box


pdf = canvas.Canvas(str(ROOT / 'pitchdeck.pdf'),pagesize=(13.333*inch,7.5*inch))
pdf.setTitle('IMOBX | Partner discussion draft')


def pdf_text(text, x, top, width, size, color=INK, bold=False, limit=None):
    style = ParagraphStyle('Slide',fontName=BOLD if bold else FONT,fontSize=size,leading=size*1.2,
                           textColor=colors.HexColor(color),alignment=TA_LEFT)
    paragraph = Paragraph(esc(text),style)
    _, height = paragraph.wrap(width*inch, 700)
    if limit and height > limit*inch:
        raise ValueError(f'Slide text exceeds its area ({height:.1f} pt): {text}')
    paragraph.drawOn(pdf,x*inch,7.5*inch-top*inch-height)


for number, item in enumerate(deck['slides'],1):
    slide = presentation.slides.add_slide(presentation.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = RGBColor.from_string(PAPER.lstrip('#'))
    accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(.65),Inches(.62),Inches(.07),Inches(.2))
    accent.fill.solid(); accent.fill.fore_color.rgb=RGBColor.from_string(ACCENT.lstrip('#')); accent.line.fill.background()
    slide.shapes.add_picture(str(ROOT / 'assets/imobx-logo-light.png'), Inches(11.6), Inches(.08), width=Inches(.95), height=Inches(.95))
    ppt_text(slide,item['title'],.8,1.17,11.7,1.7,40,INK,False,'Arial')
    ppt_text(slide,item['lead'],.82,3.03,11.6,1.0,21,MUTED)
    for row, bullet in enumerate(item['bullets']):
        ppt_text(slide,'0'+str(row+1),.82,4.25+row*.73,.42,.35,11,ACCENT,True)
        ppt_text(slide,bullet,1.35,4.2+row*.73,11,.65,18)
    for line, src in enumerate(item.get('sources', [])):
        ppt_text(slide,f"Source: {src['label']}. {src['effect']}",.82,6.3+line*.3,11.6,.28,11,MUTED)
    ppt_text(slide,f'IMOBX / PARTNER DISCUSSION DRAFT / {LABEL_EN}',.82,7.04,10,.2,9,MUTED)
    ppt_text(slide,f'{number:02d} / {len(deck["slides"]):02d}',11.6,7.04,1,.2,9,MUTED)
    slide.notes_slide.notes_text_frame.text = item['notes'] + f'\n\nSources and factual limits: companion whitepaper v{VERSION} and reference.html.'
    pdf.setFillColor(colors.HexColor(PAPER)); pdf.rect(0,0,13.333*inch,7.5*inch,fill=1,stroke=0)
    pdf.drawImage(str(ROOT / 'assets/imobx-logo-light.png'),11.6*inch,6.47*inch,width=.95*inch,height=.95*inch)
    pdf_text(item['title'],.82,1.18,11.7,40,limit=1.7)
    pdf_text(item['lead'],.82,3.03,11.6,21,MUTED,limit=1.0)
    for row, bullet in enumerate(item['bullets']):
        pdf_text('0'+str(row+1),.82,4.25+row*.73,.42,11,ACCENT,True)
        pdf_text(bullet,1.35,4.2+row*.73,11,18,limit=.65)
    for line, src in enumerate(item.get('sources', [])):
        pdf_text(f"Source: {src['label']}. {src['effect']}",.82,6.3+line*.3,11.6,11,MUTED,limit=.3)
    pdf_text(f'IMOBX / PARTNER DISCUSSION DRAFT / {LABEL_EN}',.82,7.04,10,9,MUTED)
    pdf_text(f'{number:02d} / {len(deck["slides"]):02d}',11.6,7.04,1,9,MUTED)
    pdf.showPage()
presentation.save(ROOT / 'pitchdeck.pptx')
pdf.save()
# Each old section address now points at its page in the rebuilt PDF.
for doc, doc_title in GATEWAYS:
    build_gateway(ROOT, page, translated, esc, catalog[doc], doc, doc_title, pages_from_pdf(ROOT, doc))
# Dutch beside Portuguese and English (owner, 26 Oct 2026); the gate fails while any string lacks Dutch.
from add_dutch import add_dutch
add_dutch(ROOT)
write_manifest(ROOT)


def archive(name, paths, introduction):
    with zipfile.ZipFile(ROOT / name, 'w', compression=zipfile.ZIP_DEFLATED) as bundle:
        bundle.writestr('READ-ME.txt', introduction)
        for path in dict.fromkeys(paths):
            bundle.write(ROOT / path, path)


logo_paths = ['assets/imobx-logo-light.png', 'assets/imobx-logo-dark.jpg', 'assets/imobx-logo-light-source.webp']
archive('media-kit.zip', ['media-kit.md', 'brand-colors.json', 'DESIGN.md'] + logo_paths,
        'IMOBX media kit v0.2 / 16 October 2026\nLogo artwork, colours, image sources and project descriptions.\nRead media-kit.md for the project status and available assets.\n')
archive('imobx-documents.zip', ['whitepaper.pdf', 'whitepaper.md', 'pitchdeck.pdf', 'pitchdeck.pptx',
        'pitchdeck.md', 'pitchdeck.json', 'devsheet.pdf', 'devsheet.md', 'roadmap.html', 'transparency.html', 'model-guide.json',
        'project-reference.json', 'project-reference-pt.md', 'project-reference-en.md', 'publication-manifest.json', 'contact-routes.json',
        'project-reference-pt.pdf', 'project-reference-en.pdf', 'media-kit.md', 'media-kit.zip', 'brand-colors.json', 'DESIGN.md']
        + sorted(str(p.relative_to(ROOT)) for p in ROOT.glob('*.html'))
        + sorted(str(p.relative_to(ROOT)) for p in (ROOT / 'research').rglob('*.html'))
        + sorted(str(p.relative_to(ROOT)) for p in (ROOT / 'assets').rglob('*') if p.is_file()),
        f'IMOBX document collection / {LABEL_EN}\nStart with reference.html or project-reference-pt.pdf for status, sources and the manuscript chapter map.\nThe project is in preparation. These documents do not offer an investment.\nThe paper, deck and working guide are English drafts. The project reference, roadmap, questions and money page are Portuguese/English.\nThe bundle includes the website HTML and assets. External sources require an internet connection.\n')
print('Built document exports, on-page resources, the resources page, media kit and download archives.')
