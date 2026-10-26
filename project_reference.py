"""Build a public project reference from dated, bilingual content.

This module publishes descriptions. It implements no voting, scoring or payments.
"""
import hashlib
import json
import re
from urllib.parse import urljoin

VERSION = '0.8'
REVIEW_DATE = '2026-10-24'
_MONTHS_PT = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
_MONTHS_EN = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
_y, _m, _d = (int(x) for x in REVIEW_DATE.split('-'))
DATE_PT = f'{_d} de {_MONTHS_PT[_m - 1]} de {_y}'
DATE_EN = f'{_d} {_MONTHS_EN[_m - 1]} {_y}'
LABEL_PT = f'Versão {VERSION}, {DATE_PT}'
LABEL_EN = f'Version {VERSION}, {DATE_EN}'


def build_reference(root, page, tr, esc):
    data = json.loads((root / 'project-reference.json').read_text())

    def text(pair, tag='p', attrs=''):
        return tr(*pair, tag, attrs)

    body = '<main class="paper guide-paper reference-page" id="main">'
    body += text(data['title'], 'h1')
    body += '<div class="key-card">' + text(('Ainda faltam pessoas para algumas funções, entre elas assessoria jurídica, contabilidade e a responsabilidade pelo orçamento.',
                                             'Some roles are still open, including legal adviser, accountant and budget lead.')) + '</div>'
    body += text(data['intro']) + '<p class="page-action">' + text(('Oferecer ajuda', 'Offer your help'), 'a', 'class="button act" href="contact.html"') + '</p>'
    body += text((LABEL_PT, LABEL_EN), 'p', 'class="resource-meta"')
    body += '<nav class="guide-jump" aria-label="Sections">'
    body += text(('Onde está cada assunto', 'Where each subject is'), 'a', 'href="#subjects"')
    for section in [x for x in data['sections'] if x.get('keep')]:
        body += text(section['nav'], 'a', f'href="#{esc(section["id"])}"')
    for label, target in [(('Mapa de capítulos', 'Chapter map'), 'chapters'),
                          (('Fontes', 'Sources'), 'sources'), (('Versões e downloads', 'Versions and downloads'), 'versions')]:
        body += text(label, 'a', f'href="#{target}"')
    body += '</nav>'
    exports = [[], []]
    for i in range(2):
        exports[i] = ['# ' + data['title'][i], f'**{(LABEL_PT, LABEL_EN)[i]}**', data['intro'][i]]
    elsewhere = {'status': 'roadmap.html#open-terms', 'costs': 'transparency.html#budgets', 'work': 'roadmap.html#governance',
                 'token': 'transparency.html#token-options', 'governance': 'rent-to-own.html#decisions',
                 'technology': 'transparency.html#digital-records', 'risks': 'roadmap.html#stages'}
    body += '<section id="subjects">' + text(('Onde está cada assunto', 'Where each subject is'), 'h2') + '<ul>'
    for section in data['sections']:
        if not section.get('keep'):
            body += f'<li id="{esc(section["id"])}">' + text(section['nav'], 'a', f'href="{elsewhere[section["id"]]}"') + '</li>'
            for i in range(2):
                exports[i].append(f'- [{section["nav"][i]}]({elsewhere[section["id"]]})')
    body += '</ul></section>'
    for section in [x for x in data['sections'] if x.get('keep')]:
        body += f'<section id="{esc(section["id"])}">' + text(section['title'], 'h2')
        for i in range(2):
            exports[i].append('## ' + section['title'][i])
        for paragraph in section.get('body', []):
            body += text(paragraph)
            for i in range(2):
                exports[i].append(paragraph[i])
        if section.get('columns'):
            body += '<div class="guide-table"><table><thead><tr>'
            body += ''.join(text(col, 'th', 'scope="col"') for col in section['columns'])
            body += '</tr></thead><tbody>'
            for row in section['rows']:
                body += '<tr>' + ''.join(text(cell, 'td') for cell in row) + '</tr>'
            body += '</tbody></table></div>'
            for i in range(2):
                table = ['| ' + ' | '.join(col[i] for col in section['columns']) + ' |',
                         '| ' + ' | '.join('---' for _ in section['columns']) + ' |']
                table += ['| ' + ' | '.join(cell[i] for cell in row) + ' |' for row in section['rows']]
                exports[i].append('\n'.join(table))
        for paragraph in section.get('after', []):
            body += text(paragraph)
            for i in range(2):
                exports[i].append(paragraph[i])
        for item in section.get('links', []):
            body += '<p>' + text(item['label'], 'a', f'href="{esc(item["url"])}"') + '</p>'
            for i in range(2):
                exports[i].append(f'[{item["label"][i]}]({item["url"]})')
        body += '</section>'
    body += '<section id="chapters">' + text(data['chapters_title'], 'h2')
    body += text(data['chapters_intro']) + '<ol class="reference-chapters">'
    for chapter in data['chapters']:
        body += f'<li id="chapter-{chapter["id"]}">' + text(chapter['title'], 'h3')
        body += text(chapter['scope']) + '<p>'
        for link in chapter['links']:
            body += text(link['label'], 'a', f'href="{esc(link["url"])}"') + ' · '
        body += '</p></li>'
    body += '</ol></section><section id="sources">' + text(data['sources_title'], 'h2')
    body += text(data['sources_intro']) + '<ol>'
    for source in data['sources']:
        body += f'<li id="source-{esc(source["id"])}">' + text(source['label'], 'a', f'href="{esc(source["url"])}"')
        body += text(source['scope']) + '</li>'
    body += '</ol></section><section id="versions">' + text(data['versions_title'], 'h2')
    body += ''.join(text(p) for p in data['versions'])
    body += text(data['changes_title'], 'h3') + '<ol class="transparency-updates">'
    for change in data['changes'][:2]:   # the page shows the two latest updates; the downloadable reference keeps all
        body += '<li><time datetime="' + esc(change['date']) + '">' + esc(change['date']) + '</time>'
        body += text(change['title'], 'h4') + text(change['body']) + '</li>'
    body += '</ol>' + text(('Atualizações anteriores estão na referência para baixar.', 'Earlier updates are in the downloadable reference.')) + text(data['maintenance'])
    body += '<p><a href="publication-manifest.json">' + text(('Versões e identificação dos arquivos', 'File versions and identifiers'), 'span') + '</a></p>'
    body += '<p><a href="project-reference-pt.pdf" download>Português · PDF</a> · '
    body += '<a href="project-reference-pt.md" download>Português · Markdown</a> · '
    body += '<a href="project-reference-en.pdf" download>English · PDF</a> · '
    body += '<a href="project-reference-en.md" download>English · Markdown</a> · '
    body += '<a href="project-reference.json" download>PT/EN · JSON</a></p></section></main>'
    (root / 'reference.html').write_text(page('IMOBX | Project reference', body, version=VERSION,
                                            lang='pt-BR', title_pt='IMOBX | Referência do projeto'))
    for i, lang in enumerate(['pt', 'en']):
        exports[i] += ['## ' + data['chapters_title'][i], data['chapters_intro'][i]]
        for chapter in data['chapters']:
            exports[i] += ['### ' + chapter['title'][i], chapter['scope'][i]]
            exports[i] += [f'[{link["label"][i]}]({link["url"]})' for link in chapter['links']]
        exports[i] += ['## ' + data['sources_title'][i], data['sources_intro'][i]]
        for source in data['sources']:
            exports[i].append(f'[{source["label"][i]}]({source["url"]})\n\n{source["scope"][i]}')
        exports[i] += ['## ' + data['versions_title'][i], *[p[i] for p in data['versions']]]
        exports[i] += ['### ' + data['changes_title'][i], *[f"**{c['date']}** {c['title'][i]}. {c['body'][i]}" for c in data['changes']],
                       data['maintenance'][i]]
        # Editable exports retain working links when shared away from the site.
        source = '\n\n'.join(exports[i]) + '\n'
        source = re.sub(r'\]\(([^)]+)\)', lambda m: '](' + urljoin('https://siah-kin.github.io/imobx-website/', m[1]) + ')', source)
        (root / f'project-reference-{lang}.md').write_text(source)


def write_manifest(root):
    names = ['index.html', 'rent-to-own.html', 'properties.html',
             'project-reference.json', 'project-reference-pt.md', 'project-reference-en.md',
             'project-reference-pt.pdf', 'project-reference-en.pdf', 'reference.html',
             'whitepaper.md', 'whitepaper.html', 'whitepaper.pdf', 'devsheet.md', 'devsheet.html', 'devsheet.pdf',
             'pitchdeck.json', 'pitchdeck.md', 'pitchdeck.html', 'pitchdeck.pdf', 'pitchdeck.pptx',
             'roadmap.html', 'transparency.html', 'resources.html', 'model-guide.json',
             'contact.html', 'contact-routes.json', 'assets/contact.js', 'assets/contact.css']
    data = {'version': VERSION, 'reviewed': REVIEW_DATE, 'status': 'Project proposal; no investment offer',
            'reference': 'reference.html',
            'files': [{'path': name, 'sha256': hashlib.sha256((root / name).read_bytes()).hexdigest()}
                      for name in names]}
    (root / 'publication-manifest.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
