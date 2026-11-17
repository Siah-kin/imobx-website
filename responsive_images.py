"""Responsive pictures (15 Nov 2026, critic P2: the village JPEGs were 1600 px wide and 420-740 KB, shown at 440-880 px).

Every picture listed in VARIANTS is served as a <picture>: WebP in two widths first, a JPEG in the same two widths as the
fallback, with `sizes` that match the layout. The page keeps the <img> tag with its width, height, loading and alt texts
(data-alt-pt / -en / -nl), so the language switch and the layout do not change. The full-size originals stay in assets/ as
the masters the variants are made from and as the link-preview image (seo.py uses homepage.jpg).

Runs after the pages are built, like inline_links. The variant files are made once and kept in assets/; delete one to make
it again from its master.
"""
import re
from pathlib import Path

from PIL import Image

# name -> widths (the first is the small one). Targets: the large WebP under 110 KB (the brief said 120), the small one under 50 KB.
VARIANTS = {
    'village-block': (480, 900), 'village-courtyard': (480, 900), 'village-evening': (480, 900), 'village-hillside': (480, 900),
    'village-orchard': (480, 900), 'village-playground': (480, 900), 'village-roofs': (480, 900), 'village-street': (480, 900),
    'construction-concrete-supplied': (480, 900), 'construction-solar-roof-supplied': (480, 900),
    'homepage': (480, 1024),
    # Project development: the loft model and the timber props photo, shown at about 564 px (15 Nov 2026, critic P2).
    'construction-timber-supplied': (480, 900), 'property-1': (480, 823),
    # Home, the four small prototype tiles (about 260 px wide): one 480 px size is enough.
    'property-3': (480,), 'property-4': (480,), 'property-5': (480,), 'property-6': (480,),
    # Lofts page viewer, pictures 7 to 9 (17 Nov 2026, John's third model): shown in the carousel at up to about 900 px, so the 480 px size and the picture's own width (the sources are 816, 846 and 892 px wide).
    'model3-front-view': (480, 816), 'model3-corner-view-stair': (480, 846), 'model3-corner-view-slope': (480, 892),
}
LIMITS = {0: 50_000, 1: 108_000}  # bytes for the small and the large WebP

PHONE = 'min(720px, calc(100vw - 32px))'
# Layout width of the picture, by the class of the figure that holds it (measured at 390, 800, 1024, 1280 and 1440 px).
SIZES = [
    ('steps-picture', f'(max-width:1023px) {PHONE}, 512px'),
    ('pic-sm', '(max-width:480px) calc(100vw - 32px), 440px'),
    ('side-picture', f'(max-width:1000px) {PHONE}, 500px'),
    ('about-picture', f'(max-width:960px) {PHONE}, 880px'),
    ('contact-picture', f'(min-width:1024px) 340px, {PHONE}'),
    ('lead-figure', f'(max-width:800px) {PHONE}, 600px'),
    ('decide-figure', f'(max-width:800px) {PHONE}, 490px'),
    ('village-figure', f'(max-width:800px) {PHONE}, 667px'),
    ('tour-figure', PHONE),
    ('loft-figure', '(max-width:700px) 90vw, (min-width:1340px) 588px, 44vw'),
    ('proto-1', '(max-width:900px) 87vw, (min-width:1340px) 566px, 42vw'),
    ('proto-view', '(max-width:900px) 41vw, (min-width:1340px) 272px, 20.5vw'),
]
# The lofts page shows the Olympus photos as a zoomable gallery of originals, and the Tour is not part of this batch (owner: leave it).
SKIP_PAGES = {'properties.html', 'tour.html'}
IMG = re.compile(r'<img\b(?:[^>"]|"[^"]*")*>')
OPEN_FIGURE = re.compile(r'<(?:figure|aside|a(?=[^>]*\bclass="proto-view))\b[^>]*\bclass="([^"]*)"')


def make_variants(root):
    """Make the WebP and JPEG files that are missing. Returns the names made."""
    made = []
    for name, widths in VARIANTS.items():
        master = Path(root) / 'assets' / f'{name}.jpg'
        if not master.is_file():
            raise FileNotFoundError(master)
        image = None
        for index, width in enumerate(widths):
            webp = Path(root) / 'assets' / f'{name}-{width}.webp'
            jpeg = Path(root) / 'assets' / f'{name}-{width}.jpg'
            if webp.is_file() and jpeg.is_file():
                continue
            if image is None:
                image = Image.open(master).convert('RGB')
            height = round(image.height * width / image.width)
            resized = image.resize((width, height), Image.LANCZOS)
            quality = 78
            while True:
                resized.save(webp, 'WEBP', quality=quality, method=6)
                if webp.stat().st_size <= LIMITS[index] or quality <= 52:
                    break
                quality -= 4
            resized.save(jpeg, 'JPEG', quality=74, optimize=True, progressive=True)
            made.append(webp.name)
    return made


def sizes_for(source, start):
    """The `sizes` value for the picture at `start`: the nearest figure or aside before it names the layout."""
    window = source[max(0, start - 400):start]
    opened = OPEN_FIGURE.findall(window)
    classes = opened[-1].split() if opened else []
    for key, value in SIZES:
        if key in classes:
            return value
    raise ValueError(f'no sizes rule for the picture at {source[start:start + 90]!r} (figure classes {classes})')


def picture(tag, sizes):
    match = re.search(r'\bsrc="assets/([a-z0-9-]+)\.jpg"', tag)
    name = match.group(1)
    widths = VARIANTS[name]
    small, large = widths[0], widths[-1]
    set_webp = f'assets/{name}-{small}.webp {small}w, assets/{name}-{large}.webp {large}w'
    set_jpeg = f'assets/{name}-{small}.jpg {small}w, assets/{name}-{large}.jpg {large}w'
    img = tag.replace(match.group(0), f'src="assets/{name}-{large}.jpg" srcset="{set_jpeg}" sizes="{sizes}"', 1)
    return f'<picture><source type="image/webp" srcset="{set_webp}" sizes="{sizes}">{img}</picture>'


def add_responsive_images(root):
    make_variants(root)
    names = '|'.join(re.escape(n) for n in VARIANTS)
    wanted = re.compile(rf'\bsrc="assets/({names})\.jpg"')
    total = 0
    for path in sorted(Path(root).glob('*.html')):
        if path.name in SKIP_PAGES:
            continue
        source = path.read_text(encoding='utf-8')
        if '<img' not in source:
            continue
        out, last, count = [], 0, 0
        for match in IMG.finditer(source):
            tag = match.group(0)
            if not wanted.search(tag) or 'data-viewer-image' in tag:  # the image viewer sets its own source
                continue
            out.append(source[last:match.start()])
            out.append(picture(tag, sizes_for(source, match.start())))
            last, count = match.end(), count + 1
        if count:
            out.append(source[last:])
            path.write_text(''.join(out), encoding='utf-8')
            total += count
    return total
