# IMOBX design guidelines

Updated 15 October 2026. This is the current website design reference. The owner's white-background direction and current project documents supersede the historical dark-theme and financial examples in SESSION_HANDOFF.md and AUDIT_PROMPT_WEBDESIGN.md.

## Purpose and sequence

Help a resident, local partner or supporter understand a housing DAO in development, starting with its rent-to-own housing journey. Lead with the project, proposed homes, distinct cost scopes, and treasury/governance development. Documentary community context supports the proposal further down the homepage. Let readers choose detail and describe the actual development status plainly.

Use two reading levels:

1. The initial page shows the mission, local context, a short explanation of the proposed housing model, the housing-first funding principle and access to documents.
2. Clearly named expandable sections and the document library provide the cost order, evidence requirements, digital tools, concept studies and file formats.

Essential status, resident protections and the distinction between proposals and completed work stay visible. Expandable content adds detail rather than correcting an exaggerated headline. Every section must answer a different question.

## Visual rules

- White page background (#FFFFFF); pale teal (#EDF5F7) only for occasional grouping.
- Main text #193D4E, secondary text #526571, dividers #D9E3E8. Primary buttons #276578 with white text. Accent #4A90A4. Check contrast for the actual combination.
- Retain the supplied IMOBX logo unchanged. Use its white-background version.
- Use Arial/Helvetica/system sans-serif, with readable body text at 16–18px and line height around 1.6. Keep paragraphs within approximately 65–75 characters per line.
- Use a consistent spacing scale: 8, 16, 24, 32, 48, 64 and 96px. Keep page gutters at least 20px on phones and content within 1120–1200px on desktop.
- Use a few clear heading sizes and weights. Prefer editorial rows and whitespace to repeated bordered cards. Keep corners square, with circles reserved for photographic annotations.
- One prominent next action per section. Secondary links should explain their destination. Avoid competing bright buttons and a wall of download formats on the homepage.

## Documentary editorial approach

Explain the place and the people before presenting IMOBX's proposed response. Use original, factual reporting: an observable detail, its dated source, what remains to be checked locally, then the relevant engineering or operating action. National Geographic's photo essays are an editorial reference for attention to place and caption specificity; no affiliation, borrowed reporting or reproduced prose is implied.

Use “favelas and urban communities” in the Brazilian context. Explain the worldwide challenge of inadequate housing through the relevant UN-Habitat categories, rather than treating “favela,” “slum,” “displacement” and “homelessness” as synonyms. Describe residents' work, relationships and decisions as well as housing and service needs. A photograph or a national statistic cannot establish an individual household's condition. Discuss resident choice and access to work, transport and services when describing the proposed pilot.

State the ambition plainly: IMOBX wants to combine rent-to-own housing with shared decision rules and, where useful, a DAO. Describe the pilot, agreed roles and digital tools at their actual stage. Show engineering expertise through scoped designs, cost evidence, responsible professionals, maintenance planning and checked delivery. Identify professional credentials and company/property documents only when verified; distinguish founder-supplied estimates from current scoped quotes. Present local voices only from consented, attributable reporting. Never invent an interview, beneficiary, site visit or completed result.

Put sources near factual claims, date statistics, distinguish national context from pilot evidence and keep contextual facts separate from project ambitions. Core references checked 15 October 2026:

- [IBGE: Favelas e Comunidades Urbanas](https://www.ibge.gov.br/geociencias/organizacao-do-territorio/tipologias-do-territorio/15788-favelas-ecomunidades-urbanas.html?edicao=38944&t=o-que-e): terminology and community context.
- [IBGE: 2022 Census housing-community results](https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/41797-censo-2022-brasil-tinha-16-4-milhoes-de-pessoas-morando-em-favelas-e-comunidades-urbanas): approximately 16.4 million residents, 8.1% of Brazil's population in 2022; a dated national measure, not a pilot count.
- [UN-Habitat: adequate housing](https://unhabitat.org/11-1-adequate-housing): global housing context and adequacy, including affordability.

## Photographs and annotation

Use the supplied local photographs to explain the mission. Distinguish local context, construction archive material and architectural concepts in captions. Photograph markers indicate visual focus, not surveyed boundaries, confirmed pilot ownership or beneficiary eligibility.

Replace hand-drawn blue arrows with restrained, unfilled teal circular outlines around the same communities. Preserve composition, lighting, houses, landscape and people as closely as the edit permits. Keep original source files and save edited versions separately. Record that annotation removal used generative image editing; do not describe the edited photographs as pixel-identical originals. Avoid retouching that makes the area look richer, poorer or more developed.

Link each displayed context photograph to the unchanged supplied original. State generative annotation editing in the caption and explain provenance in the image archive. Retain the distinction between a labelled presentation image and original field evidence. Confirm photographer, date, exact location and publication permissions before claiming a documented site report; source filenames are not proof of capture date.

## Interaction and gradual disclosure

- Use native HTML details/summary for secondary explanations. Name the content: for example, "How project money would be used" or "View housing concept studies".
- Keep frequently needed information and document access outside accordions. Do not nest accordions. The standalone resource library keeps direct reading and download links.
- Keep essential content readable without JavaScript. Preserve keyboard focus, normal browser navigation and anchor links.
- Let readers control the pace. No scroll locking, forced slideshow, delayed content, autoplay, artificial loading or mandatory animation. Respect reduced-motion preferences.
- Keep the PT/EN control visible. Update language, page title and image descriptions consistently. Open sections must stay open when language changes.
- Aim for 44px interactive targets, visible focus and no horizontal page overflow at 390px. Check at 320px as a narrow-screen case.

## Clickable model gallery

Use a large, manually controlled carousel for the six loft views on the homepage and archive. Keep photographs separate from design slides. Provide previous/next buttons, numbered thumbnails, a current-slide counter, touch scrolling and keyboard navigation. Do not autoplay. Keep the drawings uncropped on white or pale backgrounds. Selecting a drawing opens a labelled on-page image viewer with Close, Escape dismissal, focus return and a link to its source. Without JavaScript, the horizontal gallery and original-image links remain usable. Translate controls, descriptions and captions; retain the selected slide when language changes. Respect reduced-motion preferences.

The two replacement photographs show site access and construction beside a solar-panel roof. Preserve their supplied bytes. Their captions identify observable content; source dates, locations and association with the loft contract remain unconfirmed. The previous wall photograph stays in the asset archive but is no longer displayed.

Keep problem, proposed solution, distinct cost bases and blockchain development status visible on the homepage. The two-loft construction figure is $27,777 combined; the historical village target is $27,777 per 45 m² home at a proposed scale of at least 36. The planned treasury/governance uses of blockchain do not define the complete token model, which remains in research and development.

## Content and maintenance

Write in concrete, ordinary language. Explain what a person can do next. Describe a planned pilot as planned; use delivery and funding claims only when supported. Keep current project documents as the content source. Do not copy historical token returns, price floors or unverified partner claims into the interface.

Keep one resource catalogue in build_publication.py. The homepage presents its three primary resources concisely; resources.html exposes the full catalogue and downloads. Changes must survive rebuilding.

Before publishing, check the homepage and library on phone and desktop, keyboard and no-JavaScript access, language switching, photograph loading, links/downloads, and the actual published release.

## Reference access and chosen use

- [Nielsen Norman Group: Progressive Disclosure](https://www.nngroup.com/articles/progressive-disclosure/): usability basis for primary/secondary content and clear routes to detail.
- [Minimal Gallery](https://minimal.gallery/): visual reference for restrained composition, whitespace and image-led editorial pages; especially its architecture and nonprofit collections.
- [Kage](https://kage.design/): reference for navigation, gallery and disclosure/steps patterns. Use selected patterns in the existing buildless site.
- [Refero Styles](https://styles.refero.design/): reference for recording typography, colours, spacing and components together in a design document.
- [Designmd.ai](https://designmd.ai/): reference for keeping a project-local Markdown design specification. This file expresses IMOBX's decisions rather than importing another brand's system.
- [Mobbin](https://mobbin.com/): optional reference for real product flows; the current work uses publicly accessible material and does not require an account or paid integration.
- [VibePrompt](https://vibeprompts.dev/): optional component-prompt reference. The project keeps its existing HTML/CSS and does not add Tailwind or dependencies to reproduce snippets.

These are inspiration and usability references, not IMOBX partners or endorsements. Reference screenshots and source assets are not copied into the website.

## Image edit prompt record

Built-in image generation/editing was used on the supplied photographs. Original source files remain at assets/community-bay.jpg and assets/community-dusk.jpg. Selected website versions are assets/community-bay-circles.jpg and assets/community-dusk-circles.jpg; they are JPEG encodings of the selected edited outputs. These are edited context photographs, not independent evidence of site condition or measured boundaries.

### Bay view: final prompt

Use case: precise-object-edit. Edit target: this exact supplied real neighbourhood photograph of a bay and hillside communities, 4:3 composition. Replace ONLY its two bright blue hand-drawn arrows with TWO refined, unfilled circular outlines in muted IMOBX teal #4A90A4, thin clean strokes, no fill, no glow, no text. Completely remove both blue arrow shafts and heads and repair the sky/mountain behind them naturally. Put the left circle around the dense hillside homes where the left arrow tip points (rough centre x=220,y=475 in the 1280x960 source, radius about 90 pixels); put the right circle around the hillside homes where the right arrow tip points (rough centre x=1100,y=515, radius about 65 pixels). Circles should sit around communities, not in the sky. Maintain the entire original photo framing and 4:3 aspect ratio, all real houses, streets, terrain, bay, vegetation, clouds, photographic texture, colours and daylight. This is documentary context, not concept art: do not improve, modernize, add, remove or rearrange buildings, roads, people or natural features. The only intended changes are removing blue marks and adding these two restrained matching teal circles. No arrows remain; no extra circles or labels.

### Dusk view: final prompt

Use case: precise-object-edit. Edit target: this exact supplied real neighbourhood photograph at dusk, 4:3 composition. Replace ONLY its three bright blue hand-drawn arrows with THREE refined unfilled circular outlines in muted IMOBX teal #4A90A4, thin clean strokes, no fill, no glow, no text. Completely remove all blue arrow shafts and heads and naturally repair only the sky and hillside behind those marks. Circle the same distant hillside communities at the original arrow tips: left cluster rough centre x=300,y=330 with radius 40 pixels; middle cluster rough centre x=780,y=310 with radius 30 pixels; right cluster rough centre x=1145,y=300 with radius 35 pixels, coordinates relative to the 1280x960 source. Keep circles around homes, not floating above the skyline. Preserve the entire original composition, 4:3 aspect ratio, all real rooftops, houses, streets, people, hills, vegetation, dusk lighting, sunset gradient and photographic texture. This is documentary context: do not add, improve, remove or rearrange buildings, roads, people or natural features. Only remove blue annotations and add these three restrained matching teal circles. No arrows remain; no extra circles or labels.


## Roadmap, governance and model questions

Keep a distinct roadmap linked from navigation and resources. Show stage, proposed owner, work, advancement evidence and the corresponding website version. Preparation windows are relative to an agreed start; construction needs funding and permissions. Website v2 can report operations without a token; any later token access follows accepted rights and the reviewed legal/provider route. Use model-guide.json as the bilingual source for roadmap and FAQ, rendered by model_guide.py through build_publication.py.

Use native details for model questions, with direct section links and primary sources near claims. Separate Arc the settlement network from Arctide the exchange application; acknowledge Argus/Uniswap alternatives. Describe cooperative decision options as consultation proposals, not adopted token-weight rules or a demonstrated Hive DAO implementation. Nonprofit mission protection and any financial distribution require distinct, compatible rights.

Explain Rafael’s $27,777 village budget through his explicit CUB/SINAPI reference basis and cost-engineering breakdown, rather than merely calling it a historical estimate. Date and distinguish this per-home/36-home plan from January’s combined two-loft contract. Preserve the reference period, scope and actual-spending trail; do not imply the index publisher certifies an individual complete-home price.


## On/off-ramp explanation

The dedicated transparency page includes a bilingual settlement section with ordered, readable flow diagrams, the current USDC route clearly distinguished from the original July discussion. Show rent collection and spending back in BRL, preserve costs/reserves/restrictions before allocation, and distinguish CNPJ, title and provider approval. Mercado Bitcoin is a historical candidate, not an integrated or confirmed eligible provider. Keep contractor/client relations separate from banking and any token rights. Flow diagrams describe requirements, not an executable payment service.


## USDC settlement and provider research

USDC is the proposed current settlement asset. Use provider-neutral flow diagrams and keep the July source history separate from the updated proposal. The dedicated transparency page includes a dated comparison of direct Arc delivery, a native-USDC/CCTP route and institutional access. State technical support separately from acceptance of IMOBX’s actual entity and activity. Provider exclusions, unknown prices and unconfirmed onboarding remain visible. A payment kit is not a bank account, and cross-chain transfer is not a fiat off-ramp. Keep local BRL reserves and preserve the distinction between approved website documentation and financial execution.


## Dedicated money and transparency page

transparency.html is the canonical reading page for BRL/USDC routes, provider research, evidence and pending decisions. Generate it from the existing model-guide.json source through model_guide.py. The roadmap retains a short linked summary and old section anchors. Link the dedicated page from homepage, document navigation, FAQ and Resources; keep it in the document ZIP.

Lead with proposal, provider-acceptance and operation-evidence status. Do not invent balances or show missing figures as zero. Distinguish documented provider capabilities from customer approval and actual tests. Show dates, sources, proposed follow-up responsibilities, a future reporting outline and a manual update record. Keep source groups expandable, the main money flow readable and the PT/EN experience usable without JavaScript. No live financial integration, automatic provider monitoring or member information is introduced.


## SIAH Protocol and Hive DAO terminology

SIAH Protocol is the brand. Hive DAO is the founder-defined operating model and rails for decentralized business coordination: shared context, voluntary role-taking, accepted authority and succession let work continue without constant founder instructions. IMOBX is the proposed housing use case. Describe the assembly of Ostrom-informed rules, Python agents, Arc settlement, possible Arctide fee integration and The Flock as the Telegram interface. Preserve the distinction between the intended operating model and verified implementation. Avoid reducing the brand and the operating model to a combined “SIAH/HiveDAO service.” This is an explanation of the owner’s vision, not a claim that all participants inevitably agree or an instruction to implement backend governance here.


## Plain language for every reader

Reviewed across the public site on 15 October 2026. Write for someone who has never used a crypto app or read a housing-finance paper. Lead with the person, action and result: who pays, who checks, who decides, who owns the home. Prefer short sentences and familiar verbs. Explain necessary names such as DAO, USDC, CNPJ and CCTP at first use on a reading page. Keep source names and specialist detail available through the existing links and expandable sections.

Use “money left after bills and agreed savings” for surplus, “money set aside for repairs” for reserves, and “check the bank statement against the payment” for reconciliation. Explain a future token through what its agreement would let someone do or receive. Distinguish a right to live in a home, a membership voice and an investment. Plain wording must preserve conditions, uncertainty, source dates and protected commitments. Never turn a target into a promise or suggest an example calculation is a current price or return. Apply the same standard to Portuguese and English, navigation, photo captions, papers, slides and downloadable files. Keep the SIAH Protocol brand and Hive DAO operating model distinct.


## Main menu and page sections

Use the same main menu on every reading page: The project, Costs, Roadmap, Photos and drawings, Money, Documents. Each label has the same destination throughout the site. Keep all links available on phones by wrapping them into rows. Use the common site_header renderer in build_publication.py, including for the handwritten homepage and image archive. Show the current page where applicable. Keep a single PT/EN control in the header; remember the choice when following a link, without making storage necessary for navigation.

The image archive supports the housing proposal with drawings, supplied photos, captions and original-image links. It is not a property sale catalogue. Its separate local links are labelled On this page and stay within the archive. Main navigation and page-section navigation must be visibly distinct.


## Construction photo gallery

Keep the fuller construction selection on the existing Photos and drawings page, separate from architectural drawings and neighbourhood context. Use a quiet two-column grid on desktop and one column on phones, with lazy-loaded originals and the existing accessible image viewer. The eight-photo selection shows access, exposed rock, excavation, timber/block work, formwork, concrete and roofing. Keep captions about visible features and retain source files unchanged. Do not infer capture dates, construction chronology, ownership, project identity, technical approval or completion from the photos. Keep the source limitations visible before the gallery. Avoid near-duplicate views or identifiable people when a clear alternative exists.
