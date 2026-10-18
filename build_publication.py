"""Build static reading/presentation exports. Not imported by the Telegram bot."""
from pathlib import Path
import html
import json
import re
import xml.etree.ElementTree as ET
import zipfile
from urllib.parse import urljoin
from model_guide import build_guide
from contact_page import build_contact
from project_reference import build_reference, write_manifest, VERSION, REVIEW_DATE
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
ACCENT = '#4a90a4'
MUTED = '#596772'
PAPER = '#ffffff'
LINE = '#dae2e6'


def esc(value):
    return html.escape(str(value), quote=True)


def site_header(lang='pt-BR', current=''):
    """One main menu; local section links belong inside each page."""
    portuguese = lang.startswith('pt')
    items = [
        ('index.html#modelo', 'O projeto', 'The project'),
        ('index.html#custos', 'Custos da construção', 'Construction costs'),
        ('roadmap.html', 'Roteiro', 'Roadmap'),
        ('properties.html', 'Moradias e projetos', 'Homes & designs'),
        ('transparency.html', 'Financiamento e gastos', 'Funding & spending'),
        ('resources.html', 'Documentos', 'Documents'),
        ('contact.html', 'Participar', 'Get involved'),
    ]
    links = ''
    for target, pt, en in items:
        active = ' aria-current="page"' if target == current else ''
        links += f'<a href="{target}" data-pt="{esc(pt)}" data-en="{esc(en)}"{active}>{esc(pt if portuguese else en)}</a>'
    return ('<header class="top site-header"><nav class="wrap site-nav" data-site-nav '
            'aria-label="Principal" data-aria-pt="Principal" data-aria-en="Main">'
            '<a class="wordmark" href="index.html" aria-label="IMOBX"><img class="brand-logo" '
            'src="assets/imobx-logo-light.png" width="94" height="94" alt="IMOBX"></a>'
            '<div class="site-links">' + links + '</div>'
            '<div class="lang" role="group" aria-label="Idioma / Language">'
            f'<button type="button" data-language="pt" aria-pressed="{str(portuguese).lower()}" aria-label="Português brasileiro">PT</button>'
            f'<button type="button" data-language="en" aria-pressed="{str(not portuguese).lower()}" aria-label="English">EN</button>'
            '</div></nav></header>')


def page(title, body, script='', version='0.1', lang='en', title_pt=None):
    def label(pt, en):
        return f'<span data-pt="{esc(pt)}" data-en="{esc(en)}">{esc(pt if lang.startswith("pt") else en)}</span>'
    if 'assets/site.js' not in script:
        script += '<script src="assets/site.js" defer></script>'
    current = {'IMOBX | Resources': 'resources.html', 'IMOBX | Money and transparency': 'transparency.html',
               'IMOBX | Roadmap': 'roadmap.html', 'IMOBX | IMOBX roadmap': 'roadmap.html',
               'IMOBX | Get involved': 'contact.html'}.get(title, '')
    return f'''<!doctype html>
<html lang="{esc(lang)}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="IMOBX housing pilot: model, roadmap and project resources.">
<title>{esc(title_pt if lang.startswith('pt') and title_pt else title)}</title><link rel="icon" href="assets/imobx-logo-light.png" type="image/png"><link rel="stylesheet" href="assets/style.css"><link rel="stylesheet" href="assets/brand.css">{script}</head>
<body data-title-pt="{esc(title_pt or title)}" data-title-en="{esc(title)}"><div class="review">{label('Projeto em desenvolvimento', 'Project in development')} · v{esc(version)} · {label('Revisão do conteúdo', 'Content review')}: {REVIEW_DATE}</div>
{site_header(lang, current)}
{body}</body></html>'''


RESOURCE_CATALOG = [
    {'id': 'media-kit', 'pt': 'Media kit IMOBX', 'en': 'IMOBX media kit', 'version': '0.2',
     'description_pt': 'Logos para fundos claros e escuros, cores e guia de uso da marca.',
     'description_en': 'Logos for light and dark backgrounds, colours and brand usage guide.',
     'meta_pt': 'Guia em inglês · descrições PT/EN', 'meta_en': 'English guide · PT/EN descriptions',
     'links': [('media-kit.html','Ver o kit','View kit'), ('media-kit.zip','Baixar kit (ZIP)','Download kit (ZIP)')]},
    {'id': 'whitepaper', 'pt': 'Whitepaper', 'en': 'Whitepaper', 'version': VERSION,
     'description_pt': 'Modelo de moradia, custos, contratos, dinheiro e decisões em aberto.',
     'description_en': 'Housing model, costs, agreements, money and open decisions.',
     'meta_pt': 'Inglês · rascunho de referência', 'meta_en': 'English · reference draft',
     'links': [('whitepaper.html','Ler','Read'), ('whitepaper.pdf','PDF','PDF'), ('whitepaper.md','Texto editável','Editable text')]},
    {'id': 'pitchdeck', 'pt': 'Pitch deck', 'en': 'Pitch deck', 'version': VERSION,
     'description_pt': 'Apresentação para parceiros, com notas para quem apresenta.',
     'description_en': 'Partner presentation with presenter notes.',
     'meta_pt': '12 slides · inglês · rascunho', 'meta_en': '12 slides · English · draft',
     'links': [('pitchdeck.html','Ver slides','View slides'), ('pitchdeck.pdf','PDF','PDF'),
               ('pitchdeck.pptx','PowerPoint','PowerPoint'), ('pitchdeck.md','Texto e notas','Text and notes'),
               ('pitchdeck.json','Dados dos slides (JSON)','Slide content (JSON)')]},
    {'id': 'devsheet', 'pt': 'Guia do piloto e da construção', 'en': 'Pilot and building guide', 'version': VERSION,
     'description_pt': 'Planos de moradia, participação dos moradores e etapas de desenvolvimento propostas.',
     'description_en': 'Housing plans, resident participation and proposed development stages.',
     'meta_pt': 'Inglês · processo proposto', 'meta_en': 'English · proposed process',
     'links': [('devsheet.html','Ler','Read'), ('devsheet.pdf','PDF','PDF'), ('devsheet.md','Texto editável','Editable text')]},
    {'id': 'transparency', 'pt': 'Dinheiro e transparência', 'en': 'Money and transparency', 'version': '0.1',
     'description_pt': 'Como o dinheiro entraria, o que pagaria e como os participantes poderiam conferir as contas.',
     'description_en': 'How money would come in, what it would pay for and how participants could check the accounts.',
     'meta_pt': 'Português e inglês · planos e fontes',
     'meta_en': 'Portuguese and English · plans and sources',
     'links': [('transparency.html','Ver a página','View page')]},
]
RESOURCE_CATALOG[-1]['version'] = VERSION
RESOURCE_CATALOG.insert(0, {
    'id': 'housing', 'pt': 'Aluguel e compra da casa', 'en': 'Renting and buying the home', 'version': VERSION,
    'description_pt': 'Como os pagamentos contariam para a compra, quem cuidaria dos reparos e o que os moradores poderiam decidir.',
    'description_en': 'How payments would count towards purchase, who would handle repairs and what residents could decide.',
    'meta_pt': 'Português e inglês · modelo proposto', 'meta_en': 'Portuguese and English · proposed arrangement',
    'links': [('rent-to-own.html', 'Ler a explicação', 'Read the explanation')]
})
RESOURCE_CATALOG.append({
    'id': 'reference', 'pt': 'Referência atual do projeto', 'en': 'Current project reference', 'version': VERSION,
    'description_pt': 'Situação, responsabilidades, fontes e mapa dos capítulos do documento de Rafael.',
    'description_en': 'Status, responsibilities, sources and a chapter map for Rafael’s manuscript.',
    'meta_pt': 'Português e inglês · revisão datada', 'meta_en': 'Portuguese and English · dated review',
    'links': [('reference.html', 'Ler a referência', 'Read the reference'),
              ('project-reference-pt.pdf', 'PDF em português', 'Portuguese PDF'),
              ('project-reference-en.pdf', 'PDF em inglês', 'English PDF'),
              ('project-reference-pt.md', 'Texto editável PT', 'Editable text PT'),
              ('project-reference-en.md', 'Texto editável EN', 'Editable text EN')]
})


def translated(pt, en, tag='span', attributes=''):
    return f'<{tag} data-pt="{esc(pt)}" data-en="{esc(en)}" {attributes}>{esc(pt)}</{tag}>'


def resource_section(standalone=False):
    if not standalone:
        rows = []
        for item in [item for item in RESOURCE_CATALOG if item['id'] in ('housing', 'whitepaper', 'pitchdeck')]:
            target, pt, en = item['links'][0]
            rows.append(f'''<article class="resource-row" id="resource-{esc(item['id'])}">
<div>{translated(item['pt'],item['en'],'h3')}{translated(item['description_pt'],item['description_en'],'p')}</div>
{translated(pt + ' ↗',en + ' ↗','a',f'href="{esc(target)}" aria-label="{esc(item["en"])}"')}</article>''')
        return '<section class="content wrap" id="documentos"><span id="resources"></span><span id="recursos"></span>' + \
            translated('Recursos','Resources','span','class="eyebrow"') + \
            translated('Conheça a proposta em detalhe.','Explore the proposal in detail.','h2') + \
            translated('A explicação para famílias trata de pagamentos, reparos e compra da casa em português e inglês. O whitepaper detalha o projeto e o financiamento; os slides servem para conversas com parceiros. Esses dois documentos são rascunhos em inglês.',
                       'The household explanation covers payments, repairs and buying the home in Portuguese and English. The paper details the project and funding; the slides support partner discussions. Those two documents are English drafts.','p') + \
            '<div class="resource-rows">' + ''.join(rows) + '</div><div class="resource-more">' + \
            translated('Todos os documentos e downloads','All documents and downloads','a','href="resources.html"') + \
            translated('Referência atual do projeto','Current project reference','a','href="reference.html"') + \
            translated('Roteiro e decisões compartilhadas','Roadmap and shared decisions','a','href="roadmap.html"') + \
            translated('Dinheiro e transparência','Money and transparency','a','href="transparency.html"') + \
            translated('Perguntas sobre o modelo','Model questions','a','href="faq.html"') + \
            translated('Guia do piloto e metas','Pilot guide and targets','a','id="resource-devsheet" href="devsheet.html"') + '</div>'
    cards = []
    for item in RESOURCE_CATALOG:
        links = []
        for target, pt, en in item['links']:
            download = ' download' if '#' not in target and not target.endswith('.html') else ''
            links.append(translated(pt, en, 'a', f'href="{esc(target)}" aria-label="{esc(item["en"] + ": " + en)}"{download}'))
        cards.append(f'''<article class="resource-card" id="resource-{esc(item['id'])}" aria-labelledby="title-{esc(item['id'])}">
{translated(item['pt'],item['en'],'h3',f'id="title-{item["id"]}"')}
{translated(item['description_pt'],item['description_en'],'p')}
<p class="resource-meta">v{esc(item['version'])} · {translated(item['meta_pt'],item['meta_en'])}</p>
<div class="resource-actions">{''.join(links)}</div></article>''')
    return '''<section class="content wrap" id="documentos"><span id="resources"></span><span id="recursos"></span>''' + \
        translated('05 / Documentos do projeto','05 / Project documents','span','class="eyebrow"') + \
        translated('Documentos e identidade IMOBX.','IMOBX documents and brand assets.','h1' if standalone else 'h2') + \
        translated('Para entender pagamentos, reparos e compra da casa, comece pela explicação para famílias, em português e inglês. O whitepaper aprofunda os custos e o financiamento; o guia da construção trata de quem executaria e conferiria o trabalho; os slides resumem a proposta para parceiros. Esses três documentos são rascunhos em inglês. A referência em português e inglês reúne fontes e o mapa de capítulos do documento de Rafael.',
                    'For payments, repairs and buying the home, start with the household explanation in Portuguese and English. The paper develops the costs and funding; the building guide covers who would carry out and inspect the work; the slides summarize the proposal for partners. Those three documents are English drafts. The bilingual project reference provides sources and a chapter map for Rafael’s manuscript.','p') + \
        '<p>' + translated('Consultar a referência do projeto e o mapa de capítulos','Read the project reference and chapter map','a','class="button" href="reference.html"') + '</p>' + \
        '<div class="resource-grid">' + ''.join(cards) + '</div>' + \
        '<div class="resource-more">' + \
        translated('Ver roteiro e decisões compartilhadas','View roadmap and shared decisions','a','href="roadmap.html"') + \
        translated('Perguntas sobre o modelo','Model questions','a','href="faq.html"') + \
        translated('Para desenvolvedores: conteúdo das páginas (JSON)','For developers: page content (JSON)','a','href="model-guide.json" download') + \
        translated('Fontes, versões e situação da evidência','Sources, versions and evidence status','a','href="reference.html#sources"') + \
        translated('Baixar documentos e logos (ZIP)','Download documents and logos (ZIP)','a','href="imobx-documents.zip" download') + \
        '</div>'


for name in ['index.html', 'properties.html']:
    target = ROOT / name
    source, count = re.subn(r'<header class="top(?: site-header)?">.*?</header>',
                           lambda _: site_header('pt-BR', 'properties.html' if name == 'properties.html' else ''),
                           target.read_text(), count=1, flags=re.S)
    if count != 1:
        raise ValueError(f'Expected one main header in {name}.')
    review_pt = f'Projeto em desenvolvimento · v{VERSION} · Revisão: {REVIEW_DATE}'
    review_en = f'Project in development · v{VERSION} · Reviewed: {REVIEW_DATE}'
    source, count = re.subn(r'<div class="review"[^>]*>.*?</div>',
        lambda _: f'<div class="review" data-pt="{esc(review_pt)}" data-en="{esc(review_en)}">{esc(review_pt)}</div>',
        source, count=1, flags=re.S)
    if count != 1:
        raise ValueError(f'Expected one review date in {name}.')
    target.write_text(source)


home = ROOT / 'index.html'
home_source, replaced = re.subn(r' <section class="content wrap" id="documentos">.*?(?= <div class="faq"(?: id="faq")?>)',
                              lambda _: ' ' + resource_section() + '\n', home.read_text(), count=1, flags=re.S)
if replaced != 1:
    raise ValueError('Expected one home resource section before the FAQ.')
home.write_text(home_source)
language_controls = ''  # The shared header contains the single language control.
build_guide(ROOT, page, translated, esc, language_controls)
build_reference(ROOT, page, translated, esc)
build_contact(ROOT, page, translated, esc, VERSION)
(ROOT / 'resources.html').write_text(page('IMOBX | Resources',
    '<main id="main">' + language_controls + resource_section(standalone=True) + '</section></main>',
    '<script src="assets/site.js" defer></script>', version=VERSION, lang='pt-BR', title_pt='IMOBX | Recursos'))
if (ROOT / 'DESIGN.md').is_file():
    design_html = markdown.markdown((ROOT / 'DESIGN.md').read_text(), extensions=['tables', 'toc'])
    (ROOT / 'design.html').write_text(page('IMOBX | Design guidelines',
        '<main class="paper"><p><a href="media-kit.html">IMOBX media kit</a> · '
        '<a href="DESIGN.md" download>Download design guidelines</a></p>' + design_html + '</main>'))
kit_html = markdown.markdown((ROOT / 'media-kit.md').read_text(), extensions=['tables', 'toc'])
logo_previews = '''<div class="media-logo-grid"><figure class="media-logo light">
<img src="assets/imobx-logo-light.png" width="400" height="400" alt="IMOBX logo on a white background">
<figcaption><a href="assets/imobx-logo-light.png" download>Light logo · PNG</a></figcaption></figure>
<figure class="media-logo light"><img src="assets/imobx-logo-light.png" width="400" height="400" alt="Existing IMOBX house symbol and wordmark">
<figcaption>Original IMOBX identity · white website and document backgrounds</figcaption></figure></div>'''
kit_html = kit_html.replace('<h2', logo_previews + '<h2', 1)
(ROOT / 'media-kit.html').write_text(page('IMOBX | Media kit',
    '<main class="paper"><p><a href="media-kit.zip" download>Download media kit ZIP</a> · '
    '<a href="media-kit.md" download>Editable guide</a> · <a href="brand-colors.json" download>Brand colours (JSON)</a></p>' + kit_html + '</main>', version='0.2'))


paper_source = (ROOT / 'whitepaper.md').read_text()
paper_html = markdown.markdown(paper_source, extensions=['tables', 'toc'])
(ROOT / 'whitepaper.html').write_text(page('IMOBX | Project paper v' + VERSION,
    '<main class="paper"><p><a href="whitepaper.pdf" download>Download PDF</a> · '
    '<a href="whitepaper.md" download>Editable text</a> · <a href="reference.html">Project reference · PT/EN</a></p>' + paper_html + '</main>', version=VERSION))
devsheet_html = markdown.markdown((ROOT / 'devsheet.md').read_text(), extensions=['tables', 'toc'])
(ROOT / 'devsheet.html').write_text(page('IMOBX | Pilot and building guide v' + VERSION,
    f'<main class="paper"><p><strong>Pilot and building guide · v{VERSION}</strong><br>'
    '<a href="devsheet.pdf" download>Download PDF</a> · '
    '<a href="devsheet.md" download>Editable text</a> · <a href="reference.html">Project reference · PT/EN</a></p>' + devsheet_html + '</main>', version=VERSION))

deck = json.loads((ROOT / 'pitchdeck.json').read_text())
slides_html = []
deck_md = [f"# {deck['title']}", deck['subtitle'], f"**{deck['status']}**", '']
for number, item in enumerate(deck['slides'], 1):
    slides_html.append(f'''<section class="slide" aria-labelledby="slide-{number}">
<div class="eyebrow">{esc(item['eyebrow'])}</div><h1 id="slide-{number}">{esc(item['title'])}</h1>
<p class="lead">{esc(item['lead'])}</p><ul>{''.join('<li>'+esc(x)+'</li>' for x in item['bullets'])}</ul>
<div class="slide-foot"><span>IMOBX / PARTNER DISCUSSION DRAFT</span><span>{number:02d} / {len(deck['slides']):02d}</span></div>
<aside class="notes"><strong>Presenter notes</strong><p>{esc(item['notes'])}</p></aside></section>''')
    deck_md += [f"## {number}. {item['title']}", item['lead'], '', *('- '+b for b in item['bullets']), '',
                '**Presenter notes:** '+item['notes'], '']
source_list = ''.join(f'<li><a href="{esc(x["url"])}">{esc(x["label"])}</a></li>' for x in deck['sources'])
body = '''<main class="deck"><div class="deck-controls" hidden>
<button type="button" data-previous aria-label="Previous slide">← Previous</button><output data-counter aria-live="polite"></output>
<button type="button" data-next aria-label="Next slide">Next →</button><button type="button" data-notes aria-pressed="false">Presenter notes</button>
<a href="pitchdeck.pptx" download>PowerPoint</a><a href="pitchdeck.pdf" download>PDF</a></div>'''
body += ''.join(slides_html) + f'<aside class="sources"><h2>Sources and context</h2><ul>{source_list}</ul></aside></main>'
(ROOT / 'pitchdeck.html').write_text(page('IMOBX | Partner deck v' + VERSION, body, '<script src="assets/deck.js" defer></script>', version=VERSION))
deck_md += ['## Sources', *('- ['+x['label']+']('+x['url']+')' for x in deck['sources'])]
(ROOT / 'pitchdeck.md').write_text('\n\n'.join(deck_md) + '\n')

if PREVIEW_ONLY:
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
    ('whitepaper', paper_html, f'IMOBX / PROJECT PROPOSAL / v{VERSION} / {REVIEW_DATE}', 'IMOBX project paper v' + VERSION),
    ('devsheet', devsheet_html, f'IMOBX / PILOT AND BUILDING GUIDE / v{VERSION} / {REVIEW_DATE}', 'IMOBX pilot and building guide v' + VERSION),
    *[(f'project-reference-{lang}', markdown.markdown((ROOT / f'project-reference-{lang}.md').read_text(), extensions=['tables']),
       f'IMOBX / {lang.upper()} / v{VERSION} / {REVIEW_DATE}', f'IMOBX project reference / {lang.upper()} / v{VERSION}')
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
    ppt_text(slide,item['eyebrow'],.9,.6,10,.35,11,ACCENT,True)
    ppt_text(slide,item['title'],.8,1.17,11.7,1.7,40,INK,False,'Arial')
    ppt_text(slide,item['lead'],.82,3.03,11.6,1.0,21,MUTED)
    for row, bullet in enumerate(item['bullets']):
        ppt_text(slide,'0'+str(row+1),.82,4.25+row*.73,.42,.35,11,ACCENT,True)
        ppt_text(slide,bullet,1.35,4.2+row*.73,11,.65,18)
    ppt_text(slide,f'IMOBX / PARTNER DISCUSSION DRAFT / v{VERSION} / {REVIEW_DATE}',.82,7.04,10,.2,9,MUTED)
    ppt_text(slide,f'{number:02d} / {len(deck["slides"]):02d}',11.6,7.04,1,.2,9,MUTED)
    slide.notes_slide.notes_text_frame.text = item['notes'] + f'\n\nSources and factual limits: companion whitepaper v{VERSION} and reference.html.'
    pdf.setFillColor(colors.HexColor(PAPER)); pdf.rect(0,0,13.333*inch,7.5*inch,fill=1,stroke=0)
    pdf.drawImage(str(ROOT / 'assets/imobx-logo-light.png'),11.6*inch,6.47*inch,width=.95*inch,height=.95*inch)
    pdf_text(item['eyebrow'],.82,.62,10,11,ACCENT,True)
    pdf_text(item['title'],.82,1.18,11.7,40,limit=1.7)
    pdf_text(item['lead'],.82,3.03,11.6,21,MUTED,limit=1.0)
    for row, bullet in enumerate(item['bullets']):
        pdf_text('0'+str(row+1),.82,4.25+row*.73,.42,11,ACCENT,True)
        pdf_text(bullet,1.35,4.2+row*.73,11,18,limit=.65)
    pdf_text(f'IMOBX / PARTNER DISCUSSION DRAFT / v{VERSION} / {REVIEW_DATE}',.82,7.04,10,9,MUTED)
    pdf_text(f'{number:02d} / {len(deck["slides"]):02d}',11.6,7.04,1,9,MUTED)
    pdf.showPage()
presentation.save(ROOT / 'pitchdeck.pptx')
pdf.save()
write_manifest(ROOT)


def archive(name, paths, introduction):
    with zipfile.ZipFile(ROOT / name, 'w', compression=zipfile.ZIP_DEFLATED) as bundle:
        bundle.writestr('READ-ME.txt', introduction)
        for path in dict.fromkeys(paths):
            bundle.write(ROOT / path, path)


logo_paths = ['assets/imobx-logo-light.png', 'assets/imobx-logo-dark.jpg', 'assets/imobx-logo-light-source.webp']
archive('media-kit.zip', ['media-kit.md', 'brand-colors.json', 'DESIGN.md'] + logo_paths,
        'IMOBX media kit v0.2 / 16 October 2026\nLogo artwork, colour definitions, image provenance and project descriptions.\nRead media-kit.md for the project status and available assets.\n')
archive('imobx-documents.zip', ['whitepaper.pdf', 'whitepaper.md', 'pitchdeck.pdf', 'pitchdeck.pptx',
        'pitchdeck.md', 'pitchdeck.json', 'devsheet.pdf', 'devsheet.md', 'roadmap.html', 'faq.html', 'transparency.html', 'model-guide.json',
        'project-reference.json', 'project-reference-pt.md', 'project-reference-en.md', 'publication-manifest.json', 'contact-routes.json',
        'project-reference-pt.pdf', 'project-reference-en.pdf', 'media-kit.md', 'media-kit.zip', 'brand-colors.json', 'DESIGN.md']
        + sorted(str(p.relative_to(ROOT)) for p in ROOT.glob('*.html'))
        + sorted(str(p.relative_to(ROOT)) for p in (ROOT / 'research').rglob('*.html'))
        + sorted(str(p.relative_to(ROOT)) for p in (ROOT / 'assets').rglob('*') if p.is_file()),
        f'IMOBX document collection / v{VERSION} / {REVIEW_DATE}\nStart with reference.html or project-reference-pt.pdf for status, sources and the manuscript chapter map.\nThe project is in preparation. These documents do not offer an investment.\nThe paper, deck and working guide are English drafts. The project reference, roadmap, questions and money page are Portuguese/English.\nThe bundle includes the website HTML and assets. External sources require an internet connection.\n')
print('Built document exports, on-page resources, the resources page, media kit and download archives.')
