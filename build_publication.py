"""Build static reading/presentation exports. Not imported by the Telegram bot."""
from pathlib import Path
import html
import json
import re
import xml.etree.ElementTree as ET
import zipfile
from model_guide import build_guide

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
INK = '#1a1a1a'
ACCENT = '#4a90a4'
MUTED = '#596772'
PAPER = '#ffffff'
LINE = '#dae2e6'


def esc(value):
    return html.escape(str(value), quote=True)


def page(title, body, script='', version='0.1', lang='en', title_pt=None):
    def label(pt, en):
        return f'<span data-pt="{esc(pt)}" data-en="{esc(en)}">{esc(pt if lang.startswith("pt") else en)}</span>'
    return f'''<!doctype html>
<html lang="{esc(lang)}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="IMOBX housing pilot: model, roadmap and project resources.">
<title>{esc(title_pt if lang.startswith('pt') and title_pt else title)}</title><link rel="icon" href="assets/imobx-logo-light.png" type="image/png"><link rel="stylesheet" href="assets/style.css"><link rel="stylesheet" href="assets/brand.css">{script}</head>
<body data-title-pt="{esc(title_pt or title)}" data-title-en="{esc(title)}"><div class="review">{label('Projeto em desenvolvimento', 'Project in development')} · v{esc(version)} · 15 October 2026</div>
<nav class="wrap paper-nav" aria-label="Documents"><a class="wordmark" href="index.html"><img class="brand-logo" src="assets/imobx-logo-light.png" width="94" height="94" alt="IMOBX"></a>
<span><a href="resources.html">{label('Recursos', 'Resources')}</a> · <a href="roadmap.html">{label('Roteiro', 'Roadmap')}</a> · <a href="faq.html">FAQ</a> · <a href="whitepaper.html">Whitepaper</a> · <a href="pitchdeck.html">Pitch deck</a> · <a href="index.html">Website</a></span></nav>
{body}</body></html>'''


RESOURCE_CATALOG = [
    {'id': 'media-kit', 'pt': 'Media kit IMOBX', 'en': 'IMOBX media kit', 'version': '0.2',
     'description_pt': 'Logos para fundos claros e escuros, cores e guia de uso da marca.',
     'description_en': 'Logos for light and dark backgrounds, colours and brand usage guide.',
     'meta_pt': 'Guia em inglês · descrições PT/EN', 'meta_en': 'English guide · PT/EN descriptions',
     'links': [('media-kit.html','Ver o kit','View kit'), ('media-kit.zip','Baixar kit (ZIP)','Download kit (ZIP)')]},
    {'id': 'whitepaper', 'pt': 'Whitepaper', 'en': 'Whitepaper', 'version': '0.2',
     'description_pt': 'Modelo de moradia, custos, contratos, dinheiro e decisões em aberto.',
     'description_en': 'Housing model, costs, agreements, money and open decisions.',
     'meta_pt': '8 páginas · inglês · rascunho', 'meta_en': '8 pages · English · draft',
     'links': [('whitepaper.html','Ler','Read'), ('whitepaper.pdf','PDF','PDF'), ('whitepaper.md','Texto editável','Editable text')]},
    {'id': 'pitchdeck', 'pt': 'Pitch deck', 'en': 'Pitch deck', 'version': '0.2',
     'description_pt': 'Apresentação para parceiros, com notas para quem apresenta.',
     'description_en': 'Partner presentation with presenter notes.',
     'meta_pt': '12 slides · inglês · rascunho', 'meta_en': '12 slides · English · draft',
     'links': [('pitchdeck.html','Ver slides','View slides'), ('pitchdeck.pdf','PDF','PDF'),
               ('pitchdeck.pptx','PowerPoint','PowerPoint'), ('pitchdeck.md','Texto e notas','Text and notes'),
               ('pitchdeck.json','Dados dos slides (JSON)','Slide content (JSON)')]},
    {'id': 'devsheet', 'pt': 'Ficha do piloto e desenvolvimento', 'en': 'Developer and pilot specification', 'version': '0.3',
     'description_pt': 'Cálculos, requisitos, responsabilidades e metas propostas para os primeiros 90 dias.',
     'description_en': 'Calculations, requirements, responsibilities and proposed first-90-day targets.',
     'meta_pt': '8 páginas · inglês · rascunho', 'meta_en': '8 pages · English · draft',
     'links': [('devsheet.html','Ler','Read'), ('devsheet.pdf','PDF','PDF'), ('devsheet.md','Texto editável','Editable text')]},
]


def translated(pt, en, tag='span', attributes=''):
    return f'<{tag} data-pt="{esc(pt)}" data-en="{esc(en)}" {attributes}>{esc(pt)}</{tag}>'


def resource_section(standalone=False):
    if not standalone:
        rows = []
        for item in RESOURCE_CATALOG[:3]:
            target, pt, en = item['links'][0]
            rows.append(f'''<article class="resource-row" id="resource-{esc(item['id'])}">
<div>{translated(item['pt'],item['en'],'h3')}{translated(item['description_pt'],item['description_en'],'p')}</div>
{translated(pt + ' ↗',en + ' ↗','a',f'href="{esc(target)}" aria-label="{esc(item["en"])}"')}</article>''')
        return '<section class="content wrap" id="documentos"><span id="resources"></span><span id="recursos"></span>' + \
            translated('Recursos','Resources','span','class="eyebrow"') + \
            translated('Conheça a proposta em detalhe.','Explore the proposal in detail.','h2') + \
            translated('Documentos em inglês, em desenvolvimento. O media kit inclui descrições em português e inglês.',
                       'English project documents, in development. The media kit includes Portuguese and English descriptions.','p') + \
            '<div class="resource-rows">' + ''.join(rows) + '</div><div class="resource-more">' + \
            translated('Todos os documentos e downloads','All documents and downloads','a','href="resources.html"') + \
            translated('Roteiro e governança','Roadmap and governance','a','href="roadmap.html"') + \
            translated('Perguntas sobre o modelo','Model questions','a','href="faq.html"') + \
            translated('Ficha do piloto e metas','Pilot specification and targets','a','id="resource-devsheet" href="devsheet.html"') + '</div>'
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
        translated('05 / Recursos do projeto','05 / Project resources','span','class="eyebrow"') + \
        translated('Documentos e identidade IMOBX.','IMOBX documents and brand assets.','h1' if standalone else 'h2') + \
        translated('Leia no navegador ou baixe os arquivos. Os documentos do projeto são rascunhos em inglês para revisão; o kit inclui descrições em português e inglês.',
                    'Read in your browser or download the files. The project documents are English review drafts; the kit includes Portuguese and English descriptions.','p') + \
        '<div class="resource-grid">' + ''.join(cards) + '</div>' + \
        '<div class="resource-more">' + \
        translated('Ver roteiro e governança','View roadmap and governance','a','href="roadmap.html"') + \
        translated('Perguntas sobre o modelo','Model questions','a','href="faq.html"') + \
        translated('Fonte editável do roteiro e FAQ (JSON)','Editable roadmap and FAQ source (JSON)','a','href="model-guide.json" download') + \
        translated('Ver fontes e premissas','View sources and assumptions','a','href="whitepaper.html#12-risks-decisions-and-evidence-register"') + \
        translated('Baixar documentos e logos (ZIP)','Download documents and logos (ZIP)','a','href="imobx-documents.zip" download') + \
        '</div>'


home = ROOT / 'index.html'
home_source, replaced = re.subn(r' <section class="content wrap" id="documentos">.*?(?= <div class="faq"(?: id="faq")?>)',
                              lambda _: ' ' + resource_section() + '\n', home.read_text(), count=1, flags=re.S)
if replaced != 1:
    raise ValueError('Expected one home resource section before the FAQ.')
home.write_text(home_source)
language_controls = '''<div class="resource-language"><div class="lang" role="group" aria-label="Idioma / Language">
<button type="button" data-language="pt" aria-pressed="true" aria-label="Português brasileiro">PT</button>
<button type="button" data-language="en" aria-pressed="false" aria-label="English">EN</button></div></div>'''
build_guide(ROOT, page, translated, esc, language_controls)
(ROOT / 'resources.html').write_text(page('IMOBX | Resources',
    '<main id="main">' + language_controls + resource_section(standalone=True) + '</section></main>',
    '<script src="assets/site.js" defer></script>', lang='pt-BR', title_pt='IMOBX | Recursos'))
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
(ROOT / 'whitepaper.html').write_text(page('IMOBX | Project paper v0.2',
    '<main class="paper"><p><a href="whitepaper.pdf" download>Download PDF</a> · '
    '<a href="whitepaper.md" download>Editable text</a></p>' + paper_html + '</main>', version='0.2'))
devsheet_html = markdown.markdown((ROOT / 'devsheet.md').read_text(), extensions=['tables', 'toc'])
(ROOT / 'devsheet.html').write_text(page('IMOBX | Developer and pilot specification v0.3',
    '<main class="paper"><p><strong>Developer and pilot specification · revision 0.3</strong><br>'
    '<a href="devsheet.pdf" download>Download revised PDF</a> · '
    '<a href="devsheet.md" download>Editable text</a></p>' + devsheet_html + '</main>', version='0.3'))

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
(ROOT / 'pitchdeck.html').write_text(page('IMOBX | Partner deck v0.2', body, '<script src="assets/deck.js" defer></script>', version='0.2'))
deck_md += ['## Sources', *('- ['+x['label']+']('+x['url']+')' for x in deck['sources'])]
(ROOT / 'pitchdeck.md').write_text('\n\n'.join(deck_md) + '\n')

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
    ('whitepaper', paper_html, 'IMOBX / FOUNDER REVIEW / v0.2 / 15 OCTOBER 2026', 'IMOBX project paper v0.2'),
    ('devsheet', devsheet_html, 'IMOBX / DEVSHEET REVIEW / v0.3 / 15 OCTOBER 2026', 'IMOBX developer and pilot specification v0.3'),
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
    ppt_text(slide,'IMOBX / PARTNER DISCUSSION DRAFT / 15 OCT 2026',.82,7.04,10,.2,9,MUTED)
    ppt_text(slide,f'{number:02d} / {len(deck["slides"]):02d}',11.6,7.04,1,.2,9,MUTED)
    slide.notes_slide.notes_text_frame.text = item['notes'] + '\n\nSources and factual limits: companion whitepaper v0.2.'
    pdf.setFillColor(colors.HexColor(PAPER)); pdf.rect(0,0,13.333*inch,7.5*inch,fill=1,stroke=0)
    pdf.drawImage(str(ROOT / 'assets/imobx-logo-light.png'),11.6*inch,6.47*inch,width=.95*inch,height=.95*inch)
    pdf_text(item['eyebrow'],.82,.62,10,11,ACCENT,True)
    pdf_text(item['title'],.82,1.18,11.7,40,limit=1.7)
    pdf_text(item['lead'],.82,3.03,11.6,21,MUTED,limit=1.0)
    for row, bullet in enumerate(item['bullets']):
        pdf_text('0'+str(row+1),.82,4.25+row*.73,.42,11,ACCENT,True)
        pdf_text(bullet,1.35,4.2+row*.73,11,18,limit=.65)
    pdf_text('IMOBX / PARTNER DISCUSSION DRAFT / 15 OCT 2026',.82,7.04,10,9,MUTED)
    pdf_text(f'{number:02d} / {len(deck["slides"]):02d}',11.6,7.04,1,9,MUTED)
    pdf.showPage()
presentation.save(ROOT / 'pitchdeck.pptx')
pdf.save()


def archive(name, paths, introduction):
    with zipfile.ZipFile(ROOT / name, 'w', compression=zipfile.ZIP_DEFLATED) as bundle:
        bundle.writestr('READ-ME.txt', introduction)
        for path in paths:
            bundle.write(ROOT / path, path)


logo_paths = ['assets/imobx-logo-light.png', 'assets/imobx-logo-dark.jpg', 'assets/imobx-logo-light-source.webp']
archive('media-kit.zip', ['media-kit.md', 'brand-colors.json', 'DESIGN.md'] + logo_paths,
        'IMOBX media kit v0.2 / 15 October 2026\nOriginal logo artwork, colour definitions and a review-draft usage guide.\nRead media-kit.md. Public claims must follow the accepted project status.\n')
archive('imobx-documents.zip', ['whitepaper.pdf', 'whitepaper.md', 'pitchdeck.pdf', 'pitchdeck.pptx',
        'pitchdeck.md', 'pitchdeck.json', 'devsheet.pdf', 'devsheet.md', 'roadmap.html', 'faq.html', 'model-guide.json',
        'assets/style.css', 'assets/brand.css', 'assets/site.js', 'media-kit.md', 'brand-colors.json', 'DESIGN.md'] + logo_paths,
        'IMOBX document collection / 15 October 2026\nWhitepaper, partner deck, developer/pilot specification, roadmap, model FAQ and media kit.\nThese are founder/partner review drafts. No token offer or legal approval is established.\nPDF files are for reading; the PowerPoint and text files are editable. Read the roadmap and FAQ on the website; model-guide.json is their bilingual content source.\n')
print('Built document exports, on-page resources, the resources page, media kit and download archives.')
