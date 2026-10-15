# IMOBX website

Public project-development website for a proposed rent-to-own housing pilot in Rio de Janeiro.

The homepage and Resources page introduce the model and link the whitepaper, partner pitch deck, pilot specification and brand kit. Project documents are development drafts; the site does not process payments or launch a token. Existing archive photographs and architectural concepts are labelled separately.

Read [DESIGN.md](DESIGN.md) first for the current visual and interaction guidelines.

## Editing

- `index.html`: Portuguese/English homepage.
- `assets/style.css`, `assets/brand.css`, `assets/site.js`: shared white layout and language controls.
- `whitepaper.md`, `devsheet.md`, `pitchdeck.json`, `media-kit.md`, `brand-colors.json`: editable document sources.
- `model-guide.json`: bilingual source for the distinct roadmap, governance consultation and FAQ; `model_guide.py` renders them into `roadmap.html`, `faq.html` and the homepage.
- `build_publication.py`: rebuilds HTML, PDF, PowerPoint and ZIP exports, including the roadmap, FAQ and both Resources views. Run in a separate Python environment with `markdown`, `reportlab` and `python-pptx` installed.
- `properties.html`: existing image archive with concept/photo captions.

Older public page URLs lead to the corresponding current documents. GitHub Pages publishes the root of `main`. Historical working notes already present in the repository are not current financial or token terms.
