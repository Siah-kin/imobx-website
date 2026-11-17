"""Inline links on the first mention of a topic (owner, 15 Nov 2026, decision 97: "do some link building whenever you
touch a topic").

Rule: the link sits on the name inside its sentence, once per section and topic, internal only. No rows of links, no link
on every mention. Headings, captions, buttons, quotes and the founders' own words stay without links. A topic whose section
already links to its page keeps that link and gets no second one.

Each row of LINKS names a page, a piece of the English sentence that identifies the element (it must be unique on the page),
the phrase that becomes the link in English, Portuguese and Dutch, and the target. The step splits the sentence into
three pieces (before, link, after), each carrying its own Portuguese, English and Dutch, the way the About page already
builds its linked sentences. The Dutch of the pieces is written to i18n/nl.json when it is missing, so the Dutch step can
look every piece up by its English text. The build stops with an error when a row does not match exactly one element, so
a changed sentence can never silently lose its link.

Runs after the pages are built and before the Dutch step.
"""
import html
import json
import re
from pathlib import Path

# (page, where, English phrase, Portuguese phrase, Dutch phrase, target)
LINKS = [
    # Home: one link per topic and section; no token or ledger words are added to the homepage (the gate bans them there)
    ('index.html', 'IMOBX proposes a third way', 'a third way', 'um terceiro caminho', 'een derde manier voor', 'rent-to-own.html'),
    ('index.html', 'residents decide together', 'residents decide together', 'os moradores decidem juntos', 'bewoners beslissen samen', 'governance.html#residents'),
    ('index.html', 'Olympus, the construction company of our co-founder', 'Olympus, the construction company of our co-founder Rafael',
     'a Olympus, a construtora do nosso cofundador Rafael', 'Olympus, het bouwbedrijf van onze medeoprichter Rafael', 'properties.html'),
    ('index.html', 'signed a contract to build these two lofts', 'these two lofts', 'estes dois lofts', 'deze twee lofts te bouwen', 'properties.html'),
    ('index.html', 'considering a rent-to-own agreement for a family in Guadalupe', 'rent-to-own agreement', 'contrato de aluguel com compra',
     'huurkoopovereenkomst', 'rent-to-own.html'),
    ('index.html', 'Rafael’s estimate of about R$180,000', 'Rafael’s estimate of about R$180,000 for a flat',
     'A estimativa do Rafael, de cerca de R$180.000 por apartamento', 'Rafaels schatting van ongeveer R$180.000 voor een appartement', 'costs-and-funding.html'),
    ('index.html', 'to help found the cooperative', 'help found the cooperative', 'ajudar a fundar a cooperativa', 'de coöperatie mee op te richten', 'contact.html'),
    # Project development
    ('project-development.html', 'Olympus, the construction company of our co-founder', 'Olympus, the construction company of our co-founder Rafael',
     'a Olympus, a construtora do nosso cofundador Rafael', 'Olympus, het bouwbedrijf van onze medeoprichter Rafael', 'properties.html'),
    # Rent-to-own
    ('rent-to-own.html', 'We propose no down payment', 'what the flat costs to build', 'custo da obra', 'wat de bouw van het appartement kost', 'costs-and-funding.html#budgets'),
    ('rent-to-own.html', 'Rafael’s construction company builds it', 'Rafael’s construction company', 'A construtora do Rafael', 'Het bouwbedrijf van Rafael', 'properties.html'),
    # Costs and funding
    ('costs-and-funding.html', 'That is why we chose rent-to-own', 'rent-to-own', 'o aluguel com compra', 'huurkoop', 'rent-to-own.html'),
    ('costs-and-funding.html', 'stay private, on the site and on any ledger', 'any ledger', 'qualquer registro distribuído', 'elke distributed ledger', 'distributed-ledger.html'),
    # Distributed ledger
    ('distributed-ledger.html', 'Token holders vote only on the token’s own rules', 'Token holders vote only on the token’s own rules',
     'Quem tem o token vota só as regras do próprio token', 'Tokenhouders stemmen alleen over de regels van het token zelf', 'governance.html#token-rules'),
    # Self-compounding
    ('self-compounding.html', 'The token comes at a later stage', 'a later stage', 'numa etapa posterior', 'een latere fase', 'project-development.html#later'),
    ('self-compounding.html', 'A rent-to-own flat stops paying', 'rent-to-own flat', 'apartamento em aluguel com compra', 'huurkoopappartement', 'rent-to-own.html'),
    ('self-compounding.html', 'Each family’s agreement comes first', 'Terms and law', 'Termos e leis', 'Voorwaarden en wet', 'project-development.html#terms'),
    # Governance
    ('governance.html', 'How much goes on the ledger: none of it', 'the ledger', 'o registro distribuído', 'de distributed ledger komt', 'distributed-ledger.html#open'),
    ('governance.html', 'Once the first flats exist', 'the first flats', 'os primeiros apartamentos', 'de eerste appartementen', 'project-development.html#stages'),
    # Why
    ('why.html', 'itemised budget in reais', 'an itemised budget in reais', 'um orçamento detalhado em reais', 'een gespecificeerde begroting in reais', 'costs-and-funding.html#budgets'),
    ('why.html', 'with Rafael’s construction company', 'with Rafael’s construction company', 'com a construtora de Rafael', 'met het bouwbedrijf van Rafael', 'properties.html'),
    # Tour
    ('tour.html', 'A family rents a flat in the Guadalupe building', 'Olympus, Rafael’s company', 'a Olympus, a construtora do Rafael', 'Olympus, het bouwbedrijf van Rafael', 'properties.html'),
    ('tour.html', 'We are considering a rent-to-own agreement', 'rent-to-own agreement', 'contrato de aluguel com compra', 'huurkoopovereenkomst', 'rent-to-own.html'),
    ('tour.html', 'Rafael is a civil engineer with his own construction company', 'Olympus', 'a Olympus', 'Olympus', 'properties.html'),
    # Resources
    ('resources.html', 'The documents use Rafael', 'Rafael’s September 2026 estimate', 'estimativa do Rafael de setembro de 2026', 'Rafaels schatting van september 2026', 'costs-and-funding.html'),
    ('resources.html', 'Her research informs', 'IMOBX’s proposed rules for shared spaces', 'as regras propostas pela IMOBX para os espaços comuns',
     'de regels die IMOBX voor gedeelde ruimtes voorstelt', 'governance.html#residents'),
    ('resources.html', 'In IMOBX’s plan, part of each payment counts', 'part of each payment counts towards buying the flat',
     'parte de cada pagamento conta para a compra do apartamento', 'telt een deel van elke betaling mee voor de aankoop van het appartement', 'rent-to-own.html'),
    # Research on shared ownership
    ('commons-research.html', 'IMOBX’s plan is for each family eventually to own its flat', 'each family eventually to own its flat',
     'cada família se torne dona do seu apartamento', 'elk gezin uiteindelijk eigenaar wordt van zijn appartement', 'rent-to-own.html'),
    # Jobs
    ('jobs.html', 'preparing a rent-to-own', 'rent-to-own housing pilot', 'projeto piloto de aluguel com compra', 'huurkooppilot', 'rent-to-own.html'),
]

APPLIED = []

_LEAF = re.compile(r'<(p|li|span|dd|dt)((?:\s[^>]*?)?)\sdata-pt="([^"]*)"\sdata-en="([^"]*)"([^>]*)>([^<]*)</\1>')


def _esc(value):
    return html.escape(value, quote=True)


def _pieces(text, phrase, language, where):
    index = text.find(phrase)
    if index < 0 or text.count(phrase) != 1:
        raise ValueError(f'inline link ({language}): phrase {phrase!r} must occur exactly once in {text[:90]!r} ({where})')
    before, after = text[:index], text[index + len(phrase):]
    # A link covers whole words only: never start or end inside a word ('n' + 'uma etapa')
    if (before and before[-1].isalnum() and phrase[0].isalnum()) or (after and after[0].isalnum() and phrase[-1].isalnum()):
        raise ValueError(f'inline link ({language}): phrase {phrase!r} starts or ends inside a word in {text[:90]!r} ({where})')
    return before, phrase, after


_BLOCK_OPEN = re.compile(r'<(p|li|td|th|dd|dt)[\s>]')


def _already_linked(source, done, where):
    """True when the link is already inside the element that holds the sentence `where` (a page that is its own source keeps its links).
    The check looks inside that one element only: the same link in the navigation or the footer says nothing about this sentence."""
    start = 0
    while True:
        index = source.find(done, start)
        if index < 0:
            return False
        start = index + 1
        opened = None
        for opened in _BLOCK_OPEN.finditer(source, max(0, index - 6000), index):
            pass
        if opened is None:
            continue
        close = source.find(f'</{opened.group(1)}>', index)
        if close < 0 or source.find(f'</{opened.group(1)}>', opened.end(), index) >= 0:
            continue  # the nearest element before the link had already closed: it is not the link's parent
        text = html.unescape(''.join(re.findall(r'data-en="([^"]*)"', source[opened.start():close])))
        if where in text:
            return True


def add_inline_links(root):
    root = Path(root)
    nl_path = root / 'i18n' / 'nl.json'
    nl = json.loads(nl_path.read_text(encoding='utf-8'))
    store = {}  # Dutch of the pieces made in this run; only pieces that end up on a page reach nl.json
    APPLIED.clear()
    for page, where, en_phrase, pt_phrase, nl_phrase, href in LINKS:
        path = root / page
        source = path.read_text(encoding='utf-8')
        done = f'<a href="{_esc(href)}" data-pt="{_esc(pt_phrase)}" data-en="{_esc(en_phrase)}"'
        if _already_linked(source, done, where):  # a page that is its own source (jobs, properties) keeps its links between builds
            APPLIED.append((page, '(already in the page)', en_phrase, href))
            continue
        found = [m for m in _LEAF.finditer(source) if where in html.unescape(m.group(4))]
        if len(found) != 1:
            raise ValueError(f'inline link: {len(found)} elements on {page} contain {where!r} (need exactly 1)')
        m = found[0]
        tag, pre, pt_all, en_all, post = m.group(1), m.group(2), html.unescape(m.group(3)), html.unescape(m.group(4)), m.group(5)
        post = re.sub(r'\sdata-nl="[^"]*"', '', post)
        if 'data-nl-key' in post or 'data-nl-key' in pre:
            raise ValueError(f'inline link: {page} element with data-nl-key cannot be split ({where})')
        nl_all = store.get(en_all.strip()) or nl.get(en_all.strip())
        if nl_all is None:
            raise ValueError(f'inline link: no Dutch for the whole sentence on {page}: {en_all[:80]!r}')
        parts = {'pt': _pieces(pt_all, pt_phrase, 'pt', where), 'en': _pieces(en_all, en_phrase, 'en', where),
                 'nl': _pieces(nl_all, nl_phrase, 'nl', where)}
        for side in (0, 2):  # a piece is empty in all three languages or in none
            empties = {bool(parts[lang][side].strip()) for lang in parts}
            if len(empties) != 1:
                raise ValueError(f'inline link: pieces do not line up across languages on {page} ({where})')
            if parts['en'][side].strip():  # the Dutch step gives the Dutch the English edge spaces, so those two must agree
                edge = (lambda s: s.endswith(' ')) if side == 0 else (lambda s: s.startswith(' '))
                if edge(parts['en'][side]) != edge(parts['nl'][side]):
                    raise ValueError(f'inline link: edge spaces of English and Dutch differ on {page} ({where})')

        def put(key, value):
            if key in store and store[key] != value or key in nl and nl[key] != value:
                raise ValueError(f'inline link: Dutch key {key!r} already holds a different text')
            store[key] = value

        def span(side):
            piece = {lang: parts[lang][side] for lang in parts}
            key = piece['en'].strip()
            if not key:
                return ''
            put(key, piece['nl'].strip())
            return f'<span data-pt="{_esc(piece["pt"])}" data-en="{_esc(piece["en"])}">{_esc(piece["pt"])}</span>'

        put(en_phrase.strip(), nl_phrase.strip())
        anchor = (f'<a href="{_esc(href)}" data-pt="{_esc(pt_phrase)}" data-en="{_esc(en_phrase)}">{_esc(pt_phrase)}</a>')
        inner = span(0) + anchor + span(2)
        if tag == 'span':
            replacement = inner
        else:
            replacement = f'<{tag}{pre}{post}>{inner}</{tag}>'
        path.write_text(source[:m.start()] + replacement + source[m.end():], encoding='utf-8')
        APPLIED.append((page, en_all, en_phrase, href))
    shown = set()  # a piece that a later row split again is on no page any more: it gets no Dutch key
    for page in {row[0] for row in LINKS}:
        for value in re.findall(r'data-en="([^"]*)"', (root / page).read_text(encoding='utf-8')):
            shown.add(html.unescape(value).strip())
    changed = False
    for key, value in store.items():
        if key in shown and nl.get(key) != value:
            nl[key] = value
            changed = True
    if changed:
        nl_path.write_text(json.dumps(nl, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return len(APPLIED)
