"""Add Dutch to every built page (owner, 26 Oct 2026: the website fully in Dutch, beside Portuguese and English).

Every element that carries Portuguese and English (data-pt / data-en, and the aria-, alt- and title- variants) gets
data-nl (or data-aria-nl, data-alt-nl, data-title-nl) from i18n/nl.json, keyed by the exact English text. The contact
page's route data gets a third language in each [pt, en] pair. Strings with no Dutch are listed in
i18n/nl-missing.json; the site gate fails while that list is not empty, so a page can never ship half-translated.
"""
import html
import json
import re
from pathlib import Path


def add_dutch(root):
    root = Path(root)
    table_path = root / 'i18n' / 'nl.json'
    nl = json.loads(table_path.read_text()) if table_path.exists() else {}
    missing = set()

    def lookup(en_escaped):
        en = html.unescape(en_escaped).strip()
        if not en:
            return en_escaped
        if en not in nl:
            missing.add(en)
            return en_escaped  # falls back to English; the gate reports it
        raw = html.unescape(en_escaped)
        lead, trail = raw[:len(raw) - len(raw.lstrip())], raw[len(raw.rstrip()):]
        return html.escape(lead + nl[en].strip() + trail, quote=True)

    def route_pairs(value):
        if isinstance(value, list) and len(value) == 2 and all(isinstance(v, str) for v in value):
            en = value[1].strip()
            if en and en not in nl:
                missing.add(en)
            return [value[0], value[1], nl.get(en, value[1])]
        if isinstance(value, list):
            return [route_pairs(v) for v in value]
        if isinstance(value, dict):
            return {k: route_pairs(v) for k, v in value.items()}
        return value

    for page in sorted(root.glob('*.html')):
        source = page.read_text()
        if 'data-en=' not in source and 'data-aria-en=' not in source:
            continue
        source = re.sub(r'\sdata-([a-z]+-)?nl="[^"]*"', '', source)  # rebuilds start clean
        source = re.sub(r'data-((?:aria-|alt-|title-)?)en="([^"]*)"',
                        lambda m: f'data-{m.group(1)}en="{m.group(2)}" data-{m.group(1)}nl="{lookup(m.group(2))}"', source)
        block = re.search(r'(<script[^>]*id="contact-route-data"[^>]*>)(.*?)(</script>)', source, re.S)
        if block:
            data = route_pairs(json.loads(block.group(2)))
            source = source[:block.start(2)] + json.dumps(data, ensure_ascii=False).replace('</', '<\\/') + source[block.end(2):]
        page.write_text(source)
    # the contact script's own short messages (say(pt, en)) get their Dutch from the same table
    script = root / 'assets' / 'contact.js'
    if script.exists():
        js = script.read_text()
        says = {en: (nl[en.strip()] + en[len(en.rstrip()):]) if en.strip() in nl else None
                for en in re.findall(r"say\('[^']*', '([^']*)'\)", js)}
        missing.update(en for en, value in says.items() if value is None)
        js = re.sub(r'const NL_SAY = \{.*?\};', 'const NL_SAY = ' + json.dumps({k: v for k, v in says.items() if v}, ensure_ascii=False) + ';', js, count=1, flags=re.S)
        script.write_text(js)
    (root / 'i18n').mkdir(exist_ok=True)
    (root / 'i18n' / 'nl-missing.json').write_text(json.dumps(sorted(missing), indent=1, ensure_ascii=False) + '\n')
    return sorted(missing)
