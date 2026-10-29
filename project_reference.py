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

    def spans(ids):
        return ''.join(f'<span id="{esc(i)}"></span>' for i in ids)

    # Sweep of 28 Oct 2026 (review C, owner's go-ahead): who does what, and where the facts come from.
    # The chapter map, the citation rules and the change log left this page; their ids stay as empty spans.
    retired = data['retired_anchors']['ids']
    body = '<main class="paper guide-paper reference-page" id="main">'
    body += text(data['title'], 'h1')
    # Owner, 29 Oct: the 'we still need…' line under the title is removed; the open roles are in the table below.
    body += '<p class="page-action">' + text(('Oferecer ajuda', 'Offer your help'), 'a', 'class="button act" href="contact.html"') + '</p>'
    body += '<nav class="guide-jump" aria-label="Sections">'
    for section in [x for x in data['sections'] if x.get('keep')]:
        body += text(section['nav'], 'a', f'href="#{esc(section["id"])}"')
    for label, target in [(('Fontes', 'Sources'), 'sources'), (('Versões e downloads', 'Versions and downloads'), 'versions')]:
        body += text(label, 'a', f'href="#{target}"')
    body += '</nav>' + spans(i for i in retired if not i.startswith('source-'))
    sections_start = len(body)  # Resources one-pager (owner, 29 Oct) takes everything from here on
    exports = [[], []]
    for i in range(2):
        exports[i] = ['# ' + data['title'][i], f'**{(LABEL_PT, LABEL_EN)[i]}**']
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
    body += '<section id="sources">' + text(data['sources_title'], 'h2')
    body += text(data['sources_intro']) + '<ol>'
    for source in data['sources']:
        body += f'<li id="source-{esc(source["id"])}">' + text(source['label'], 'a', f'href="{esc(source["url"])}"')
        body += text(source['scope']) + '</li>'
    body += '</ol>' + spans(i for i in retired if i.startswith('source-'))
    body += '</section><section id="versions">' + text(data['versions_title'], 'h2')
    body += text((LABEL_PT, LABEL_EN), 'p', 'class="resource-meta"')
    body += '<p><a href="project-reference-pt.pdf" download>Português · PDF</a> · '
    body += '<a href="project-reference-pt.md" download>Português · Markdown</a> · '
    body += '<a href="project-reference-en.pdf" download>English · PDF</a> · '
    body += '<a href="project-reference-en.md" download>English · Markdown</a></p></section></main>'  # citing and file versions are on Documents
    build_reference.fragment = body[sections_start:].removesuffix('</main>')
    (root / 'reference.html').write_text(page('IMOBX | Project reference', body, version=VERSION,
                                            lang='pt-BR', title_pt='IMOBX | Referência do projeto'))
    for i, lang in enumerate(['pt', 'en']):
        exports[i] += ['## ' + data['sources_title'][i], data['sources_intro'][i]]
        for source in data['sources']:
            exports[i].append(f'[{source["label"][i]}]({source["url"]})\n\n{source["scope"][i]}')
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
