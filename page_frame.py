"""The ground line under the opening (owner, 16 Nov 2026, merged board).

Runs after the pages are built, like inline_links: on the pages whose opening answers a question, a decorative line (an orange
rule over a hatched strip, CSS in assets/frame.css) is set between the opening and the first section. It is an empty <div>, so it
does not change the white and pale-teal rhythm of the sections. No words change.
"""
import hashlib
import json
import re
from pathlib import Path

GROUND_PAGES = ('index', 'about', 'why', 'rent-to-own', 'governance', 'project-development', 'self-compounding',
                'distributed-ledger', 'properties', 'tour', 'privacy', 'jobs', 'commons-research', 'contact', 'resources')
# Pages that were plain white from header to footer (critic, 16 Nov): their sections alternate white and pale like the others.
BAND_DOCS = ('about', 'properties', 'tour', 'privacy', 'jobs', 'commons-research')
SPLIT_AT_H2 = ('jobs', 'commons-research')  # one document with no sections: each h2 and what follows it becomes a section
LINE = '<div class="ground-line" aria-hidden="true"></div>'
FIRST_SECTION = re.compile(r'<section\b(?![^>]*data-anchor-only)')


NAV_RIGHT_PAGES = ('why', 'rent-to-own', 'governance', 'self-compounding', 'distributed-ledger', 'resources')


def add_nav_right(root):
    """The "On this page" list moves to the opening's right column from 1100 px (CSS in assets/frame.css; it stays under the text on a
    phone): the page's main gets class nav-right. Costs keeps its drawing in that column."""
    for name in NAV_RIGHT_PAGES:
        path = Path(root) / f'{name}.html'
        source = path.read_text(encoding='utf-8')
        start, end = _main_bounds(source)
        main = source[start:end]
        if 'nav-right' in main[:300] or '<nav class="on-this-page"' not in main:
            continue
        tag_end = main.index('>') + 1
        tag = main[:tag_end].replace('class="', 'class="nav-right ', 1)
        path.write_text(source[:start] + tag + main[tag_end:] + source[end:], encoding='utf-8')


def add_ground_line(root):
    add_nav_right(root)
    add_bands(root)
    done = []
    for name in GROUND_PAGES:
        path = Path(root) / f'{name}.html'
        source = path.read_text(encoding='utf-8')
        if LINE in source:
            continue
        main = source.find('<main')
        match = FIRST_SECTION.search(source, main)
        if name == 'properties':
            match = re.compile(r'<h2 id="lofts"').search(source, main)
        if main < 0 or not match:
            raise ValueError(f'no section to put the ground line before on {name}.html')
        path.write_text(source[:match.start()] + LINE + source[match.start():], encoding='utf-8')
        done.append(name)
    return done


def _main_bounds(source):
    start = source.index('<main')
    return start, source.index('</main>', start)


def add_bands(root):
    """White and pale-teal sections on the pages that had none. A section after the opening that is odd in order gets class "pale"
    (CSS in assets/frame.css); jobs and commons-research, which are one run of paragraphs, are first cut into sections at each h2."""
    for name in BAND_DOCS:
        path = Path(root) / f'{name}.html'
        source = path.read_text(encoding='utf-8')
        start, end = _main_bounds(source)
        main = source[start:end]
        if 'band-doc' in main[:200]:
            continue
        head_end = main.index('>') + 1
        tag, body = main[:head_end], main[head_end:]
        if name in SPLIT_AT_H2:
            parts = re.split(r'(?=<h2[ >])', body)
            body = parts[0] + ''.join('<section class="doc-section">' + part + '</section>' for part in parts[1:])
        # Which sections get the pale ground: the top-level sections, every second one, the first after the opening included.
        # The lofts page (properties.html) keeps its opening section (h1, lead and the two lofts) white and paints the photo section after it.
        depth, count, out, pos = 0, 0, [], 0
        for tok in re.finditer(r'<section\b[^>]*>|</section>', body):
            text = tok.group(0)
            if text == '</section>':
                depth -= 1
                continue
            if depth == 0 and 'data-anchor-only' not in text:
                count += 1
                pale = (text.find('id="fotos-obra"') >= 0) if name == 'properties' else count % 2 == 1
                if pale:
                    out.append((tok.start(), text.replace('<section', '<section data-pale="1"', 1)))
                    out[-1] = (tok.start(), tok.end(), out[-1][1])
            depth += 1
        for st, en, new_tag in reversed([o for o in out if len(o) == 3]):
            body = body[:st] + new_tag + body[en:]
        tag = tag.replace('class="', 'class="band-doc ', 1) if 'class="' in tag else tag.replace('<main', '<main class="band-doc"', 1)
        path.write_text(source[:start] + tag + body + source[end:], encoding='utf-8')


def term_scripts(root, ids):
    """The jargon popup (assets/terms.js) for a page that explains only the terms in `ids` (owner, 17 Nov 2026, decision 121:
    'token engineer' is a tap-to-open word on About and the Tour). The meanings travel inside the page, like on the ledger pages."""
    data = json.loads((Path(root) / 'terms.json').read_text(encoding='utf-8'))
    data['terms'] = [t for t in data['terms'] if t['id'] in ids]
    payload = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    version = hashlib.sha256((Path(root) / 'assets' / 'terms.js').read_bytes()).hexdigest()[:10]
    return ('<script type="application/json" id="imobx-terms">' + payload + '</script>'
            '<script src="assets/site.js" defer></script><script src="assets/terms.js?v=' + version + '" defer></script>')
