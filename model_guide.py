"""Public roadmap and model explanation. Content only; no governance execution."""
import json
import re
import hashlib as _hashlib
from money_flow import money_flow_html, cascade_html, route_html, FUNDING_SCRIPT, SCRIPT as MF_SCRIPT

# FAQ items that moved into rent-to-own.html; the other questions moved into transparency.html.
HOUSEHOLD_FAQ = ('home-purchase', 'home-repairs', 'home-exit', 'home-decisions', 'home-participate', 'tenant-access')


def new_faq_location(old_link):
    """Where a link to the retired faq.html now points: faq.html#faq-<id> -> the page that holds the item."""
    match = re.fullmatch(r'faq\.html(?:#faq-([a-z0-9-]+))?', old_link)
    if not match:
        return old_link
    ident = match.group(1)
    if not ident:
        return 'rent-to-own.html#questions'
    page_name = 'rent-to-own.html' if ident in HOUSEHOLD_FAQ else 'transparency.html'
    return f'{page_name}#faq-{ident}'


def redirect_stub(title, heading, target, open_label, per_question=None):
    """A page that has moved: meta refresh, a visible link, one PT/EN line. Same pattern as buy.html.
    per_question maps an old #faq-<id> anchor to the page that now holds it, so old links land on the item."""
    script = ''
    if per_question:
        script = ('<script>(function(){var m=' + json.dumps(per_question) + ';var h=location.hash;var t=' + json.dumps(target) + ';'
                  'if(h.indexOf("#faq-")===0&&m[h.slice(5)])t=m[h.slice(5)]+h;'
                  'var a=document.getElementById("moved-link");if(a)a.href=t;location.replace(t);})();</script>')
    refresh = f'<meta http-equiv="refresh" content="0;url={target}">'
    if per_question:
        refresh = '<noscript>' + refresh + '</noscript>'
    return ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{title}</title>{refresh}<link rel="stylesheet" href="assets/style.css"><link rel="stylesheet" href="assets/brand.css"></head>'
            '<body><main class="paper"><a href="index.html"><img class="brand-logo" src="assets/imobx-logo-light.png" width="94" height="94" alt="IMOBX"></a>'
            f'<h1>{heading}</h1><p>Esta página foi atualizada. / This page has moved.</p>'
            f'<p><a id="moved-link" href="{target}">Abrir a versão atual / {open_label}</a></p></main>{script}</body></html>')


PARTNER_LINKS = [('transparency.html', ('de onde viria o dinheiro', 'where the money would come from')),
                 ('reference.html', ('quem responde pelo projeto', 'who is responsible')),
                 ('resources.html', ('documentos para baixar', 'documents to download'))]


def partner_line_html(here, text):
    """Retired 25 Oct 2026 (owner: one home per idea): the partner links now sit once in the site footer."""
    return ''
    """'For partners and funders: <link>, <link> and <link>.' in both languages, skipping the current page."""
    links = [text(label, 'a', f'href="{target}"') for target, label in PARTNER_LINKS if target != here]
    joined = links[0] if len(links) == 1 else ''.join(
        link + (text((', ', ', '), 'span') if i < len(links) - 2 else text((' e ', ' and '), 'span') if i == len(links) - 2 else '')
        for i, link in enumerate(links))
    return ('<p class="partner-line">' + text(('Para parceiros e financiadores: ', 'For partners and funders: '), 'span')
            + joined + '.</p>')


# Why housing: IMOBX's proposed organisation (owner, 25 Oct; REVIEW-5: one picture per column, under its own label).
def _house(x, y):
    return f'<path class="og-line" d="M{x-9} {y}v-10l9-8 9 8v10Z"/>'
def _person(x, y):
    return f'<circle class="og-person" cx="{x}" cy="{y}" r="7"/><path class="og-line" d="M{x-12} {y+26}c2-10 7-15 12-15s10 5 12 15"/>'
ORG_PICS = [
    # decided in each neighbourhood: one neighbourhood with its homes
    '<svg class="org-pic" viewBox="0 0 200 120" aria-hidden="true"><circle class="og-area" cx="100" cy="60" r="54"/>'
    + _house(76, 62) + _house(100, 50) + _house(124, 62) + _house(88, 86) + _house(112, 86) + '</svg>',
    # shared across projects: three neighbourhoods joined to one shared base
    '<svg class="org-pic" viewBox="0 0 200 120" aria-hidden="true">'
    + ''.join(f'<circle class="og-area" cx="{x}" cy="30" r="24"/>' + _house(x, 34) + f'<path class="og-link" d="M{x} 54V86"/>' for x in (40, 100, 160))
    + '<rect class="og-base" x="12" y="86" width="176" height="26"/><path class="og-line" d="M30 93h22v12H30ZM89 93h22v12H89ZM148 93h22v12h-22Z"/></svg>',
    # who answers for it: one person keeps the accounts, another checks them
    '<svg class="org-pic" viewBox="0 0 200 120" aria-hidden="true">' + _person(62, 40) + '<path class="og-line" d="M84 56h24v30H84ZM89 64h14M89 71h14M89 78h9"/>'
    + _person(146, 40) + '<path class="og-check" d="M132 92l9 9 17-20"/></svg>',
]


def build_guide(root, page, tr, esc, language_controls):
    def asset_v(name):
        """assets/<name>?v=<hash>: a changed stylesheet is fetched again instead of served from the browser's cache."""
        return f'assets/{name}?v=' + _hashlib.sha256((root / 'assets' / name).read_bytes()).hexdigest()[:10]
    guide = json.loads((root / 'model-guide.json').read_text())

    def text(pair, tag='p', attrs=''):
        return tr(*pair, tag, attrs)

    source_notes_text = {
        'ica': ('A declaração de identidade cooperativa da ICA orienta como moradores e membros participam das decisões comuns.',
                'The ICA’s statement of cooperative identity informs how residents and members take part in shared decisions.'),
        'ostrom': ('A pesquisa de Elinor Ostrom sobre a gestão de recursos compartilhados orienta as regras para as decisões dos moradores.',
                   'Elinor Ostrom’s research on managing shared resources informs the rules for resident decisions.'),
        'token-study': ('A afirmação de que um token não cria renda de aluguel, não verifica um prédio e não garante um comprador é do próprio plano. O estudo da OCDE é um panorama geral sobre tokenização e não analisa a IMOBX.',
                        'The statement that a token cannot create rental income, verify a building or guarantee a buyer is the plan’s own. The OECD study is general background on tokenisation and does not review IMOBX.'),
        'cvm': ('O Parecer de Orientação 40 da CVM, órgão que regula o mercado de valores do Brasil, orienta como o plano descreve os direitos de um investimento: conta o que ele realmente dá, não o nome.',
                'Guidance Opinion 40 from the CVM, Brazil’s securities-market regulator, informs how the plan describes investment rights: what counts is what an investment actually gives, not its name.'),
        'digital': ('O trabalho digital proposto está detalhado na seção do whitepaper sobre o que se torna digital.',
                    'The proposed digital work is set out in the whitepaper section on what becomes digital.'),
        'cash': ('A política de caixa proposta está detalhada no whitepaper.',
                 'The proposed cash policy is set out in the whitepaper.'),
        'cost': ('Os custos de construção estão detalhados no whitepaper.',
                 'The construction costs are set out in the whitepaper.'),
    }

    own_source_labels = {
        'cvm': ('Como o regulador do mercado de capitais avalia tokens (CVM)', 'How Brazil’s market regulator looks at tokens (CVM)'),
        'nonprofit': ('Regras para parcerias entre o poder público e organizações da sociedade civil (Lei 13.019)', 'Rules for partnerships between government and civil-society organisations (Law 13.019)'),
        'ica': ('O que faz uma cooperativa (Aliança Cooperativa Internacional)', 'What makes a cooperative (International Cooperative Alliance)'),
        'ostrom': ('A palestra de Elinor Ostrom no Nobel sobre recursos compartilhados', 'Elinor Ostrom’s Nobel lecture on shared resources'),
        'arc': ('Arc · Litepaper', 'Arc · Litepaper'),
        'arctide': ('Arctide · exchange na Arc', 'Arctide · exchange on Arc'),
        'argus': ('Argus · exchange na Arc', 'Argus · exchange on Arc'),
        'cash': ('Nosso whitepaper sobre como o dinheiro seria administrado (em inglês)', 'Our whitepaper on how money would be handled (in English)'),
        'rights': ('Whitepaper, seção 8: o que um token poderia representar (em inglês)', 'Whitepaper, section 8: what a token could represent'),
        'digital': ('Nosso whitepaper sobre o que passaria a ser digital (em inglês)', 'Our whitepaper on what would become digital (in English)'),
        'technical': ('Guia do piloto, seção 6: escopo e aceitação (em inglês)', 'Pilot guide, section 6: scope and acceptance'),
        'roadmap': ('Etapas do projeto', 'Project stages'),
        'charter': ('Etapas do projeto: quem decide o quê', 'Project stages: who decides what'),
        'cost': ('Nosso whitepaper sobre os custos (em inglês)', 'Our whitepaper on the costs (in English)'),
        'sinapi': ('O índice oficial de custos de construção (Caixa, SINAPI)', 'The official building cost index (Caixa, SINAPI)'),
        'cub': ('O que o custo padrão de construção inclui (Sinduscon)', 'What the standard building cost covers (Sinduscon)'),
        'cnpj': ('Registro de organizações estrangeiras na Receita Federal (CNPJ)', 'Tax registration for foreign organisations (Receita Federal)'),
        'title': ('Quando a propriedade de um imóvel passa a outra pessoa (Código Civil)', 'When ownership of a property passes (Civil Code)'),
        'mb': ('Mercado Bitcoin · elegibilidade de contas', 'Mercado Bitcoin · account eligibility'),
        'bcb': ('As regras do Banco Central para serviços com criptoativos', 'Brazil’s Central Bank rules for crypto services'),
        'settlement': ('Fluxo reais ↔ moeda digital', 'Reais ↔ digital money flow'),
        'ramp-options': ('Opções de conversão e elegibilidade', 'Conversion options and eligibility'),
        'community-economy': ('Economia comunitária proposta', 'Proposed community economy'),
        'token-study': ('OCDE · Estudo sobre registros de ativos digitais', 'OECD · Study of digital asset records'),
        'reference-token': ('Token e divulgação', 'Token and outreach'),
    }

    # What each source does and does not establish. One line per source, shown under the paragraph it supports.
    source_effect = {
        'cost': ('Mostra os custos como Rafael os enviou. Não mostra um preço nem um pagamento mensal para uma família.',
                 'Shows the costs as Rafael supplied them. It does not show a price or monthly payment for a family.'),
        'digital': ('Descreve o trabalho digital proposto. Não mostra que algo disso já funciona.',
                    'Describes the proposed digital work. It does not show that any of it works yet.'),
        'cash': ('Descreve a política de caixa proposta. É uma proposta, não uma regra aprovada.',
                 'Describes the proposed cash policy. It is a proposal, not an approved rule.'),
        'rights': ('Descreve o que um token poderia representar. Nenhum token foi emitido.',
                   'Describes what a token could represent. No token has been issued.'),
        'charter': ('Mostra quem decidiria o quê. As regras ainda estão em discussão com os participantes.',
                    'Shows who would decide what. The rules are still being discussed with participants.'),
        'roadmap': ('Mostra as etapas e o que precisa estar pronto em cada uma. Não define datas.',
                    'Shows the stages and what must be ready in each. It sets no dates.'),
        'sinapi': ('É a referência pública de custos que Rafael diz ter usado. Não dá o preço deste projeto.',
                   'Is the public cost reference Rafael says he used. It does not price this project.'),
        'cub': ('Explica o que o índice CUB cobre. Não confirma o orçamento de Rafael.',
                'Explains what the CUB index covers. It does not confirm Rafael’s budget.'),
        'reference-token': ('Lista o que está e o que não está decidido sobre o token. Nenhum caminho foi aprovado.',
                            'Lists what is and is not decided about the token. No path has been approved.'),
        'cvm': ('Diz que o regulador brasileiro olha o que um investimento realmente dá, não o nome. Não diz se o plano da IMOBX cumpre as regras.',
                'Says Brazil’s regulator looks at what an investment actually gives, not its name. It does not say whether the IMOBX plan complies.'),
        'arctide': ('É o site da própria plataforma. Não mostra uso nem parceria com a IMOBX.',
                    'Is the platform’s own site. It does not show any IMOBX use or partnership.'),
        'argus': ('É o site da própria plataforma. Não mostra uso nem parceria com a IMOBX.',
                  'Is the platform’s own site. It does not show any IMOBX use or partnership.'),
        'token-study': ('É um panorama geral sobre tokenização. Não analisa a IMOBX.',
                        'Is general background on tokenisation. It does not review IMOBX.'),
        'nonprofit': ('Define as organizações sem fins lucrativos nas parcerias com o setor público. Não diz que a IMOBX é uma delas.',
                      'Defines nonprofits in partnerships with the public sector. It does not say IMOBX is one.'),
        'ostrom': ('É uma pesquisa sobre como comunidades administram recursos compartilhados. Não testa as regras da IMOBX.',
                   'Is research on how communities manage shared resources. It does not test IMOBX’s rules.'),
        'ica': ('Apresenta os princípios das cooperativas, entre eles a participação dos membros. Não analisa a IMOBX.',
                'States the principles of cooperatives, including member participation. It does not review IMOBX.'),
        'cnpj': ('Explica como uma organização estrangeira se cadastra no CNPJ. Não garante conta em banco ou corretora.',
                 'Explains how a foreign organisation registers for a CNPJ. It does not guarantee a bank or exchange account.'),
        'title': ('Diz que a propriedade de um imóvel passa com o registro do título. Não decide nada sobre o projeto da IMOBX.',
                  'Says ownership of a property passes with registration of the title. It decides nothing about the IMOBX project.'),
        'bcb': ('É a norma do Banco Central que o plano cita sobre moeda digital. A assessoria jurídica ainda precisa confirmar o que ela exige da IMOBX.',
                'Is the Central Bank rule the plan cites on digital money. Legal advisers still need to confirm what it requires of IMOBX.'),
        'settlement': ('Mostra o caminho proposto do dinheiro. Nenhum provedor está confirmado.',
                       'Shows the proposed route of the money. No provider is confirmed.'),
    }
    # (question id, source key) -> index of the answer paragraph the source supports.
    source_at = {
        'home-purchase': {'cost': 1}, 'home-repairs': {'digital': 0}, 'home-exit': {'cash': 0},
        'tenant-access': {'charter': 0}, 'ico': {'cash': 0, 'roadmap': 1},
        'cost-basis': {'sinapi': 0, 'cub': 0, 'cost': 1},
        'yield': {'reference-token': 0, 'cvm': 1, 'cash': 2},
        'arc-arctide': {'digital': 0, 'arctide': 2, 'argus': 2},
        'exchanges': {'token-study': 0, 'cvm': 0}, 'funding': {'cash': 0}, 'property': {'rights': 1},
        'nonprofit': {'nonprofit': 1, 'cvm': 1}, 'scale': {'roadmap': 0, 'ostrom': 0},
        'rwa': {'rights': 0, 'cvm': 0}, 'dao': {'ostrom': 0, 'roadmap': 1},
        'governance': {'ica': 0, 'ostrom': 0}, 'merit': {'charter': 0, 'ica': 0},
        'flock-siah': {'charter': 0, 'ostrom': 1, 'digital': 4}, 'on-off-ramp': {'settlement': 0},
        # fold-outs on the funding page (community economy)
        'community-rights': {'charter': 0, 'ostrom': 1},
        'community-tools': {'charter': 0, 'ostrom': 1, 'digital': 4},
        'treasury-demonstration': {'digital': 1}, 'campaign-work': {'reference-token': 0},
    }

    def with_sources(item_id, answers):
        """Answer paragraphs, each source line directly under the paragraph it supports.
        A shortened answer has fewer paragraphs: its sources follow the last one."""
        placed = source_at.get(item_id, {})
        out = ''
        for index, pair in enumerate(answers):
            out += text(pair) + ''.join(source_line(key) for key, at in placed.items()
                                        if min(at, len(answers) - 1) == index)
        return out

    def sentences(pair):
        """Split a PT/EN pair into matching sentences."""
        parts = [re.split(r'(?<=[.!?])\s+(?=[A-ZÀ-Ú])', side) for side in pair]
        assert len(parts[0]) == len(parts[1]), pair
        return list(zip(*parts))

    def cited_paragraph(pair, by_sentence):
        """One paragraph per cited sentence group, with that sentence's sources under it."""
        out, pending = '', []
        for index, sentence in enumerate(sentences(pair)):
            pending.append(sentence)
            if index in by_sentence or index == len(sentences(pair)) - 1:
                out += text((' '.join(x[0] for x in pending), ' '.join(x[1] for x in pending)))
                out += ''.join(short_source(key) for key in by_sentence.get(index, []))
                pending = []
        return out

    def source_line(key):
        source = guide['sources'][key]
        return ('<p class="source-note">' + text(('Fonte: ', 'Source: '), 'span')
                + f'<a href="{esc(source["url"])}">{label_text(key)}</a>. ' + text(source_effect[key], 'span') + '</p>')

    def source_links(*keys):
        """'Sources: <label> · <label>.' when the paragraph above already states what they do not show."""
        return ('<p class="source-note">' + text(('Fontes: ', 'Sources: '), 'span')
                + ' · '.join(f'<a href="{esc(guide["sources"][k]["url"])}">{label_text(k)}</a>' for k in keys) + '.</p>')

    def grouped_sources(note, *keys):
        """'Sources: <label> · <label>. <one limit for all>' (second review, 25 Oct: one line per section)."""
        return ('<p class="source-note">' + text(('Fontes: ', 'Sources: '), 'span')
                + ' · '.join(f'<a href="{esc(guide["sources"][k]["url"])}">{label_text(k)}</a>' for k in keys) + '. '
                + text(note, 'span') + '</p>')

    def full_source(key):
        """A source line with both what it says and what it does not establish."""
        return ('<p class="source-note">' + text(('Fonte: ', 'Source: '), 'span')
                + f'<a href="{esc(guide["sources"][key]["url"])}">{label_text(key)}</a>. ' + text(source_effect[key], 'span') + '</p>')

    def short_source(*keys):
        """'Source: <label>. <what it does not establish>' for one or more sources, one line each."""
        return ''.join('<p class="source-note">' + text(('Fonte: ', 'Source: '), 'span')
                       + f'<a href="{esc(guide["sources"][k]["url"])}">{label_text(k)}</a>. '
                       + text(pick(source_effect[k], [-1]), 'span') + '</p>' for k in keys)

    def label_text(key):
        if key in own_source_labels:
            return text(own_source_labels[key], 'span')
        return esc(guide['sources'][key]['label'])

    def source_notes(keys):
        """One sentence per source, saying what it informs, with the link beside it."""
        html = ''
        for key in keys:
            source = guide['sources'][key]
            html += '<p class="source-note">' + text(source_notes_text[key], 'span') + ' '
            html += f'<a href="{esc(source["url"])}">{label_text(key)}</a></p>'
        return html

    def numbered(number, pair):
        """Only stages that really follow one another are numbered."""
        return (f'{number}. {pair[0]}', f'{number}. {pair[1]}')

    # Four kinds of work run side by side; the last two stages depend on the ones before them.
    parallel_ids = ('foundation', 'cash-and-charter', 'digital-trial', 'token-decision')
    stage_groups = [
        (('Quatro frentes de trabalho ao mesmo tempo', 'Four kinds of work at the same time'), False),
        (('Depois, uma etapa de cada vez', 'Then, one stage after another'), True)]

    def grouped_stages():
        """Yield (group label, in order?, [(number or None, stage)]) with parallel work first."""
        for label, ordered in stage_groups:
            members = [st for st in guide['stages'] if (st['id'] in parallel_ids) != ordered]
            yield label, ordered, [(n if ordered else None, st) for n, st in enumerate(members, 1)]

    def links(keys):
        return '<p class="guide-sources">' + ' · '.join(
            f'<a href="{esc(guide["sources"][key]["url"])}">{label_text(key)}</a>'
            for key in keys) + '</p>'

    FAQ_DETAIL_LABEL = ('Veja a explicação completa', 'Read the full explanation')

    def faq_item(item, prefix, local_page=None, short=False):
        """One collapsible question. Links to a section of the page it sits on drop the file name."""
        answers = item['short'] if short and item.get('short') else item['a']
        body = f'<details id="{prefix}{esc(item["id"])}">' + text(item['q'], 'summary')
        assert set(source_at.get(item['id'], {})) <= set(item['sources']), item['id']  # unplaced sources are dropped
        body += with_sources(item['id'], answers)
        if item.get('detail_url'):
            target = item['detail_url']
            if local_page and target.startswith(local_page + '#'):
                target = target[len(local_page):]
            # The visible words repeat on every question, so the accessible name carries the question too.
            named = tuple(f'{label}: {question}' for label, question in zip(FAQ_DETAIL_LABEL, item['q']))
            body += text(FAQ_DETAIL_LABEL, 'a', f'href="{esc(target)}" aria-label="{esc(named[0])}" '
                                              f'data-aria-pt="{esc(named[0])}" data-aria-en="{esc(named[1])}"')
        return body + '</details>'

    family_questions = [x for x in guide['questions'] if x['id'] in HOUSEHOLD_FAQ]
    funding_questions = [x for x in guide['questions'] if x['id'] not in HOUSEHOLD_FAQ]

    def risk_row(index):
        reference = json.loads((root / 'project-reference.json').read_text())
        return next(x for x in reference['sections'] if x['id'] == 'risks')['rows'][index]

    def participation_decisions_title():
        return guide['participation']['decision_title']

    def guide_question(ident):
        return next(x for x in guide['questions'] if x['id'] == ident)

    def family_faq_section():
        """An index of the families' questions; each answer lives in its section above."""
        body = '<section id="questions">' + text(('Perguntas das famílias', 'Questions families ask'), 'h2') + '<ul class="question-index">'
        for ident, target in [('home-purchase', 'payments'), ('home-repairs', 'repairs'), ('home-decisions', 'decisions'),
                              ('tenant-access', 'decisions'), ('home-exit', 'hardship'), ('home-participate', 'next')]:
            body += '<li>' + text(guide_question(ident)['q'], 'a', f'href="#{target}"') + '</li>'
        return body + '</ul></section>'

    def funding_faq_section():
        body = '<section class="faq" id="funding-questions">' + text(
            ('Perguntas sobre financiamento, tokens e governança', 'Questions about funding, tokens and governance'), 'h2')
        body += text(('Como o projeto funcionaria e o que ainda falta decidir.', 'How the project would work and what remains undecided.'))
        body += ''.join(faq_item(x, 'faq-', 'transparency.html') for x in funding_questions)
        body += '<span id="faq-thanks-zeal-lets"></span><span id="faq-euler"></span>'
        body += text(('Quem participa e quais direitos precisa combinar', 'Who takes part and which rights need agreement'),
                     'a', 'class="guide-more" href="roadmap.html#participation"')
        body += text(('Perguntas das famílias sobre aluguel e compra da casa', 'Questions families ask about renting and buying the home'),
                     'a', 'class="guide-more" href="rent-to-own.html#questions"')
        return body + '</section>'

    journey = guide['resident_journey']
    def pick(pair, keep):
        """Only the listed sentences of a PT/EN pair, in order."""
        chosen = [sentences(pair)[i] for i in keep]
        return (' '.join(x[0] for x in chosen), ' '.join(x[1] for x in chosen))

    def marked(pre, mid, post, cls='answer'):
        """An answer line with one phrase on the pastel marker (ladder level 2); each piece switches language."""
        return (f'<p class="{cls}">' + text(pre, 'span') + text(mid, 'mark', 'class="hint"')
                + text(post, 'span') + '</p>')

    def on_this_page(items):
        """A short list of the page's sections, under the opening (owner, 25 Oct: show readers what they will see)."""
        return ('<nav class="on-this-page" aria-label="On this page">' + text(('Nesta página', 'On this page'))
                + '<ol>' + ''.join('<li>' + text(label, 'a', f'href="#{anchor}"') + '</li>' for label, anchor in items) + '</ol></nav>')

    def partner_line(here=''):
        """The one line on each page that sends partners and funders to their pages (never to the page itself)."""
        return partner_line_html(here, text)

    # The family page is the home of the household's own questions: payments, repairs, decisions, hardship.
    # Old question anchors (faq-<id>) sit on the section that now answers them.
    anchors = {'payments': ['faq-home-purchase'], 'repairs': ['faq-home-repairs'],
               'decisions': ['faq-home-decisions', 'faq-tenant-access'],
               'hardship': ['faq-home-exit'], 'next': ['faq-home-participate']}
    # Rent-to-own, distilled 25 Oct 2026 (owner: integrated and varied, not a string of headed sections):
    # one lead, the drawing with one paragraph, a repair step strip, two columns for decisions, a panel for
    # hardship and a closing band. The old FAQ index is gone; its anchors stay on the sections that answer them.
    rp = guide['rent_page']
    span_ids = lambda ids: ''.join(f'<span id="{a}"></span>' for a in ids)
    resident = '<main class="paper guide-paper resident-page band-page" id="main">'
    # Attention pass (owner-approved package, 25 Oct): the card holds the lead's first and third sentences unchanged.
    lead_s = [x.split('. ') for x in rp['lead']]
    resident += text(journey['title'], 'h1')
    resident += '<div class="key-card">' + text((lead_s[0][0] + '. ' + lead_s[0][2] + '.', lead_s[1][0] + '. ' + lead_s[1][2] + '.')) + '</div>'
    # the lead keeps 'agreed in writing before the family moves in': a required qualification (facts register Q01)
    resident += text((lead_s[0][1] + '. ' + '. '.join(lead_s[0][3:]), lead_s[1][1] + '. ' + '. '.join(lead_s[1][3:])), 'p', 'class="guide-lead"')
    resident += on_this_page([(('O dinheiro', 'The money'), 'payments'), (('Reparos', 'Repairs'), 'repairs'),
                              (('O que os moradores decidem', 'What residents decide'), 'decisions'), (('Se a família não puder pagar', 'If a family cannot pay'), 'hardship')])
    resident += '<p class="rent-cases">' + text(('Os imóveis em estudo e a situação de cada um: ', 'The homes being considered, and where each one stands: '), 'span')
    resident += text(('Roteiro, três casos', 'Roadmap, three cases'), 'a', 'href="roadmap.html#cases"') + '.</p>'

    resident += '<section id="payments">' + span_ids(anchors['payments'] + ['questions'])
    rec = [x.split('. ', 1) for x in rp['record']]
    resident += text(journey['steps_title'], 'h2') + text((rec[0][0] + '.', rec[1][0] + '.'), 'p', 'class="answer"')
    resident += money_flow_html(text) + text((rec[0][1], rec[1][1]))
    resident += text(('Veja os dois orçamentos de obra', 'Read the two construction budgets'),
                     'a', 'href="transparency.html#budgets"') + '</section>'

    resident += '<section id="repairs">' + span_ids(anchors['repairs']) + text(journey['repairs_title'], 'h2')
    resident += '<ol class="step-strip">' + ''.join(text(st, 'li') for st in rp['repair_steps']) + '</ol>'
    resident += text(rp['repair_note']) + text(('Quem cuida do trabalho e como questionar uma decisão', 'Who handles the work and how to question a decision'),
                                                'a', 'href="roadmap.html#governance"') + '</section>'

    resident += '<section id="decisions">' + span_ids(anchors['decisions']) + text(rp['decisions_heading'], 'h2')
    resident += '<div class="two-sides"><div>' + text(rp['decide_title'], 'strong', 'class="side-title"') + '<ul>'
    resident += ''.join(text(x, 'li') for x in rp['decide']) + '</ul>' + text(rp['decide_note']) + '</div>'
    resident += '<div class="side-protect">' + text(rp['protect_title'], 'strong', 'class="side-title"') + '<ul>'
    resident += ''.join(text(x, 'li') for x in rp['protect']) + '</ul></div></div>'
    resident += text(rp['invest'], 'p', 'class="invest-line"') + text(('Mais no roteiro', 'More in the roadmap'), 'a', 'href="roadmap.html#governance"') + '</section>'

    resident += '<section id="hardship" class="soft-panel">' + span_ids(anchors['hardship']) + text(journey['hardship_title'], 'h2')
    resident += ''.join(text(pair) for pair in journey['hardship'])
    resident += text(('Tudo o que está em aberto', 'Everything still open'), 'a', 'href="roadmap.html#open-terms"') + '</section>'

    resident += '<section id="next" class="closing-band">' + span_ids(anchors['next']) + text(rp['interest'])
    resident += text(('Preparar uma conversa sobre moradia', 'Prepare a housing conversation'), 'a', 'class="button act" href="contact.html?role=resident"') + '</section>'
    resident += '<span id="funding"></span><span id="property"></span>' + partner_line('rent-to-own.html') + '</main>'
    (root / 'rent-to-own.html').write_text(page('IMOBX | Renting and buying a home', resident,
        f'<link rel="stylesheet" href="{asset_v("flow.css")}"><link rel="stylesheet" href="{asset_v("bands.css")}">' + MF_SCRIPT,
        version=guide['version'], lang='pt-BR', title_pt='IMOBX | Aluguel e compra da casa'))

    # Roadmap in the attention pattern (owner, 25 Oct): the question as title, one orange key card (where we stand),
    # an "on this page" list, an answer line under each question, background in quiet folds, commitments visible,
    # one orange action at the end. See ATTENTION_ANALYSIS_2026-10-25.md.
    roadmap = '<main class="paper guide-paper band-page roadmap-page" id="main">' + language_controls
    roadmap += text(('Quais são as etapas do projeto?', 'What are the project stages?'), 'h1')
    roadmap += '<div class="key-card" id="where-we-stand">' + text(('O projeto está em preparação. A forma jurídica está em definição; ainda falta demonstrar o funcionamento das moradias e o uso de blockchain para guardar e pagar recursos do projeto.',
                     'The project is in preparation. The legal form is being defined. Running the homes and using blockchain to hold and pay project funds still need to be demonstrated.')) + '</div>'
    roadmap += text(('Cada etapa mostra quem participa e o que precisa estar pronto antes de começar. Ainda não há datas.',
                     'Each stage lists who takes part and what has to be ready before it starts. No dates are set yet.'), 'p', 'class="guide-lead"')
    roadmap += on_this_page([(('Etapas', 'Stages'), 'stages'), (('Os imóveis', 'The properties'), 'cases'), (('Quem participa', 'Who takes part'), 'participation'),
                             (('Quem decide o quê', 'Who decides what'), 'governance'), (('O que falta definir', 'Still to settle'), 'open-terms')])
    roadmap += '<section id="stages">' + text(('Quais são as etapas?', 'What are the stages?'), 'h2')
    roadmap += text(('São sete etapas: quatro andam lado a lado, e três vêm uma depois da outra.',
                     'There are seven stages: four run side by side, and three follow one after another.'), 'p', 'class="answer"')
    # Only the details a stage's summary does not already say. Who does the work is in the summary;
    # what people could follow is on the funding page's reporting section.
    stage_detail = {
        'foundation': {'schedule': [1], 'work': [0, 1]},
        'cash-and-charter': {'gate': [0, 1], 'pause': [0]},
        'funded-pilot': {'schedule': [1], 'work': [0], 'gate': [1]},
        'digital-trial': {'work': [0], 'gate': [1], 'pause': [0]},
        'token-decision': {'pause': [0]},
        'replication': {'work': [0, 1], 'gate': [1], 'pause': [0]},
        'owner-platform': {'work': [0, 1, 2]},
    }
    detail_labels = [(('Quando', 'When'), 'schedule'), (('Trabalho', 'Work'), 'work'),
                     (('Antes de avançar', 'Before it moves on'), 'gate'), (('O que impediria', 'What would stop it'), 'pause')]
    for label, ordered, members in grouped_stages():
      roadmap += text(label, 'p', 'class="stage-group"')
      for number, stage in members:
        roadmap += f'<details class="roadmap-stage" id="{esc(stage["id"])}"><summary>'
        roadmap += text(numbered(number, stage['title']) if number else stage['title'], 'h3') + text(stage['window'], 'span', 'class="guide-window"')
        # A quiet link-styled cue; the whole summary row is the control and the browser keeps it keyboard-operable.
        roadmap += '<span class="stage-toggle">' + text(('Mais informações', 'More information'), 'span', 'class="more"') + text(('Menos informações', 'Less information'), 'span', 'class="less"') + '</span></summary><dl>'
        roadmap += text(('Quem', 'Who'), 'dt') + text(stage['overview_owner'], 'dd') + text(('Precisa de', 'Needs'), 'dt') + text(stage['overview_needs'], 'dd')
        for label, key in detail_labels:
            if key in stage_detail[stage['id']]:
                body = pick(stage[key], stage_detail[stage['id']][key])
                if stage['id'] == 'replication' and key == 'gate':
                    body = tuple(f'{a} {b}' for a, b in zip(body, pick(guide_question('scale')['a'][1], [2])))
                roadmap += text(label, 'dt') + text(body, 'dd')
        roadmap += '</dl></details>'
    roadmap += '</section>'

    cases = guide['cases']
    # The answer first (no pilot is confirmed), then what the three words mean.
    intro_lines = tuple(t.rsplit('. ', 1) for t in cases['intro'])
    roadmap += '<section id="cases">' + text(('De quais imóveis estamos falando?', 'Which properties are we talking about?'), 'h2')
    roadmap += text(tuple(t[1] for t in intro_lines), 'p', 'class="answer"') + text(tuple(t[0] + '.' for t in intro_lines))
    roadmap += '<div class="guide-table"><table><thead><tr>' + ''.join(text(h, 'th', 'scope="col"') for h in cases['headings'])
    roadmap += '</tr></thead><tbody>' + ''.join('<tr>' + text(r[0], 'th', 'scope="row"') + text(r[1], 'td') + text(r[2], 'td') + '</tr>'
                                              for r in cases['rows']) + '</tbody></table></div></section>'
    participation = guide['participation']
    roadmap += '<section id="participation">' + text(('Quem participa?', 'Who takes part?'), 'h2')
    roadmap += text(('Oito grupos participam, cada um com suas necessidades e decisões.',
                     'Eight groups take part, each with its own needs and decisions to make.'), 'p', 'class="answer"')
    # One table instead of eight fold-outs, inside one quiet fold: background, not a commitment.
    roadmap += '<details class="disclosure"><summary>' + text(('Ver os oito grupos e o que cada um precisa', 'See the eight groups and what each needs'), 'span') + '</summary><div class="disclosure-body">'
    roadmap += '<div class="guide-table"><table><thead><tr>' + ''.join(text(h, 'th', 'scope="col"') for h in participation['headings'])
    roadmap += '</tr></thead><tbody>' + ''.join(f'<tr id="role-{role["id"]}">' + text(role['who'], 'th', 'scope="row"') + text(role['need'], 'td')
                                              + text(role['decision'], 'td') + '</tr>' for role in participation['roles'])
    roadmap += '</tbody></table></div></div></details>'
    roadmap += text(('Veja como isso funcionaria para uma família: pagamentos, reparos e decisões',
                     'See how this would work for a household: payments, repairs and decisions'), 'a', 'href="rent-to-own.html"')
    roadmap += short_source('ica') + '</section>'

    public = guide['transparency']
    Q = {item['id']: item for item in guide['questions']}
    ans = lambda ident, i, keep=None: Q[ident]['a'][i] if keep is None else pick(Q[ident]['a'][i], keep)
    spans = lambda *ids: ''.join(f'<span id="{i}"></span>' for i in ids)

    # The funding page is the home of money: budgets, sources of money, the token, the payment route,
    # the legal limits and reporting. Household, governance and people sections live on their own pages.
    # Funding page, distilled 25 Oct 2026 (owner: keep it simple; drawings instead of lists; no string of headed sections).
    # Five sections: what needs money now, the first homes' cost, where money comes from and its order (cascade),
    # how a payment travels (route), legal form and reports. Token questions live on token.html.
    fp = guide['funding_page']
    transparency = '<main class="paper guide-paper transparency-page band-page" id="main">' + language_controls
    transparency += text(public['title'], 'h1') + '<div class="key-card">' + text(fp['key']) + '</div>'
    transparency += text(fp['lead'], 'p', 'class="guide-lead"')
    transparency += on_this_page([(('Custos', 'Costs'), 'budgets'), (('A ordem do dinheiro', 'The order of money'), 'money-order'),
                                  (('O caminho de um pagamento', 'How a payment travels'), 'settlement'), (('Forma jurídica e relatórios', 'Legal form and reports'), 'legal')])
    transparency += '<div id="status"><ul class="funding-status">'
    transparency += ''.join(text(item, 'li', 'class="is-open"' if n else '') for n, item in enumerate(fp['status'])) + '</ul></div>'

    transparency += '<section id="budgets">' + spans('faq-cost-basis', 'custos') + guide['budgets_html'].replace('<p data-pt="São custos de construção', '<p class="answer" data-pt="São custos de construção', 1)
    transparency += grouped_sources(('Nenhuma delas define o preço para uma família.', 'None of them sets a family’s price.'), 'sinapi', 'cub', 'cost') + '</section>'

    order = guide['money_order']
    transparency += ('<section id="money-order">' + spans('funding', 'funding-sources', 'faq-funding', 'community-economy', 'household-payments', 'thanks-zeal-lets')
                     + text(fp['order_title'], 'h2') + text(fp['order_intro']) + cascade_html(text) + text(order['transfer']))
    # The five kinds of money are shown openly (owner, 26 Oct): their sources and permitted uses are the model.
    transparency += text(fp['kinds_summary'], 'h3') + '<div class="guide-table"><table><thead><tr>'
    transparency += ''.join(text(h, 'th', 'scope="col"') for h in order['headings']) + '</tr></thead><tbody>'
    transparency += ''.join('<tr>' + text(row[0], 'th', 'scope="row"') + text(row[1], 'td') + text(row[2], 'td') + '</tr>'
                            for row in order['kinds']) + '</tbody></table></div>' + short_source('cash') + '</section>'

    transparency += ('<section id="settlement">' + spans('faq-on-off-ramp', 'rent-onramp', 'construction-offramp', 'digital-records', 'faq-arc-arctide',
                                                         'treasury-demonstration', 'ramp-options')
                     + text(fp['route_title'], 'h2') + text(tuple(x.split('. ', 1)[0] + '.' for x in fp['route_after']), 'p', 'class="answer"') + route_html(text) + text(tuple(x.split('. ', 1)[1] for x in fp['route_after']))
                     + short_source('bcb', 'digital') + '</section>')

    transparency += '<div class="duo"><section id="legal">' + spans('faq-nonprofit') + text(fp['legal_title'], 'h2') + text(fp['legal'])
    transparency += grouped_sources(('Nenhuma delas diz qual forma a IMOBX terá.', 'None of them says which form IMOBX will take.'), 'cnpj', 'title', 'nonprofit') + '</section>'

    transparency += '<section id="reporting">' + spans('faq-ico', 'ico-comparison') + text(public['reporting_title'], 'h2')
    transparency += '<ul>' + ''.join(text(public['reporting'][i], 'li') for i in (0, 1, 2, 4)) + '</ul>' + text(ans('ico', 1, [0])) + '</section></div>'
    transparency += '<section class="closing-band" id="elsewhere">' + spans('sources', 'updates', 'next-steps')
    transparency += ('<p id="token-options" class="token-line">' + spans('faq-yield', 'funding-questions', 'faq-thanks-zeal-lets', 'faq-euler', 'faq-exchanges',
                                                      'faq-property', 'faq-rwa', 'outreach', 'campaign-work')
                     + text(fp['token'], 'span') + text(fp['token_link'], 'a', 'href="token.html"') + '.</p>')

    # Old anchors whose answers now live elsewhere: one line each, pointing to the answer; then the one orange action.
    transparency += '<p>' + spans('faq-governance', 'faq-merit', 'faq-dao', 'faq-flock-siah', 'faq-scale', 'community-rights', 'community-tools')
    transparency += text(('Quem decide, como o trabalho segue e como a IMOBX cresceria: ', 'Who decides, how work moves forward and how IMOBX would grow: '), 'span')
    transparency += text(('Roteiro, quem decide o quê', 'Roadmap, who decides what'), 'a', 'href="roadmap.html#governance"') + '.</p>'
    transparency += text(('Ver os documentos', 'See the documents'), 'a', 'class="button act" href="resources.html"') + '</section>'
    transparency += partner_line('transparency.html') + '</main>'
    (root / 'transparency.html').write_text(page('IMOBX | Funding and spending', transparency,
        f'<link rel="stylesheet" href="{asset_v("flow.css")}"><link rel="stylesheet" href="{asset_v("bands.css")}">' + FUNDING_SCRIPT, version=guide['version'], lang='pt-BR', title_pt='IMOBX | Financiamento e gastos'))

    roadmap += '<section id="governance">' + spans('faq-governance', 'faq-merit', 'faq-dao', 'faq-flock-siah', 'faq-scale')
    roadmap += text(('Quem decide o quê?', 'Who decides what?'), 'h2')
    roadmap += text(('O contrato de cada família protege a sua casa. Os moradores decidem o que é comum, e outra pessoa confere cada pagamento.',
                     'Each family’s agreement protects its home. Residents decide shared matters, and a different person checks each payment.'), 'p', 'class="answer"')
    headings = [('Decisão', 'Decision'), ('Quem decidiria', 'Who would decide'), ('Limites e conferências', 'Limits and checks')]
    rows = [
        [('Moradia e compra', 'Occupancy and purchase'),
         ('O morador e a organização, conforme o contrato e a lei.', 'The resident and the organisation, under their agreement and the law.'),
         ('Uma votação de tokens não muda sozinha o contrato da família. É preciso poder questionar e pedir revisão.', 'A token vote cannot change a family’s agreement on its own. People need a way to question a decision and ask for review.')],
        [('Uso de espaços e manutenção local', 'Shared spaces and local maintenance'),
         ('Uma opção para discutir: voz igual para cada membro do grupo de moradores.', 'One option to discuss: equal voice for each member of the resident group.'),
         ('Decisões dentro do orçamento e das regras de segurança, com apoio à participação e possibilidade de substituir representantes.', 'Decisions within the budget and safety rules, with support for participation and a way to replace representatives.')],
        [('Execução e compras', 'Delivery and purchasing'),
         ('Pessoas escolhidas pela experiência, com função e prazo claros.', 'People chosen for their experience, with a clear job and time limit.'),
         ('A construtora não aprova a própria cobrança. Aprovar o gasto, conferir a entrega e pagar são tarefas com conferências separadas.', 'The builder does not approve its own invoice. Approving spending, checking delivery and paying need separate checks.')],
    ]  # investor rights live on the token page (one home per idea)
    roadmap += '<div class="guide-table"><table><thead><tr>' + ''.join(text(h, 'th', 'scope="col"') for h in headings)
    roadmap += '</tr></thead><tbody>'
    for row in rows:
        roadmap += '<tr>' + ''.join(text(cell, 'td') for cell in row) + '</tr>'
    roadmap += '</tbody></table></div>'
    # Ostrom's eight design principles, in plain words; her name stays only in the source credit (owner, 24 Oct: low jargon).
    roadmap += '<details class="disclosure"><summary>' + text(('Regras para o que é comum', 'Rules for what residents share'), 'span') + '</summary><div class="disclosure-body">'
    roadmap += text(('Cada família seria dona da casa; espaços comuns, reservas e o dinheiro para novas casas teriam regras comuns.',
                     'Each family would own its home; shared spaces, reserves and the money for more homes would follow rules agreed together.'))
    principles = [
        ('Quem participa, quais imóveis e o que é comum, bem definidos.', 'Who takes part, which properties and what is shared, clearly defined.'),
        ('Custos justos ao que cada família recebe e pode pagar.', 'Costs fair to what each household receives and can afford.'),
        ('Os afetados ajudam a decidir as regras comuns.', 'The people affected help decide the shared rules.'),
        ('Dinheiro e obra conferidos por pessoas que prestam contas aos participantes e declaram seus interesses.', 'Money and work checked by people who answer to the participants and declare their interests.'),
        ('Respostas graduais a regras descumpridas, com defesa.', 'Responses to broken rules that start small, with a right to be heard.'),
        ('Mediação e revisão acessíveis, protegendo o direito de moradia.', 'Accessible mediation and review, with protection for housing rights.'),
        ('O direito dos moradores de fazer suas regras.', 'Residents’ right to make their own rules.'),
        ('Decisões locais com os moradores; serviços compartilhados entre projetos.', 'Local decisions close to residents, with services shared across projects.')
    ]
    roadmap += '<ol class="ostrom-application">' + ''.join(text(p, 'li') for p in principles) + '</ol>' + short_source('ostrom') + '</div></details>'
    roadmap += '<details class="disclosure"><summary>' + text(('Como o trabalho segue no dia a dia', 'How everyday work moves forward'), 'span') + '</summary><div class="disclosure-body">'
    roadmap += text(pick(guide['dao_operations']['work'], [0, 1])) + text(guide['dao_operations']['continuity'])
    roadmap += text(guide['dao_operations']['status'])  # the help-desk paragraph moves to the blockchain page
    roadmap += short_source('digital') + '</div></details></section>'

    hj, rp = guide['resident_journey'], guide['transparency']
    open_terms = [
        ('Qual imóvel o primeiro projeto vai usar.', 'Which property the first project will use.'),
        ('O preço, o pagamento mensal e quanto de cada pagamento conta para a compra.', 'The price, the monthly payment and how much of each payment counts towards buying the home.'),
        ('A divisão dos custos de reparo, os prazos de atendimento, o contato responsável e a forma de revisar uma cobrança ou um serviço contestado.',
         'Who pays for repairs, how quickly they are handled, who to contact and how to question a charge or repair.'),
        pick(hj['hardship'][0], [1]),
        ('Os procedimentos de votação, os limites de gasto e a maneira de resolver uma discordância.',
         'Voting procedures, spending limits and ways to resolve disagreements.'),
        ('A forma jurídica da organização.', 'The organisation’s legal form.'),
        ('O financiamento e o que receberia quem financiar o projeto.', 'The funding, and what people who fund the project would receive.'),
        ('Os direitos de quem compra um token.', 'The rights of token buyers.'), ('O prestador do serviço de pagamento.', 'The payment provider.'),
    ]
    # Commitments stay visible (research, 25 Oct): a checklist in three groups, with how many are settled.
    groups = [(('A casa e o preço', 'The home and its price'), open_terms[0:4]), (('As regras', 'The rules'), open_terms[4:5]),
              (('Dinheiro e forma jurídica', 'Money and legal form'), open_terms[5:9])]
    roadmap += '<section id="open-terms">' + text(('O que os fundadores vão definir primeiro?', 'What will the founders settle first?'), 'h2')
    roadmap += marked(('Definidos até agora: ', 'Settled so far: '), ('0 de 9', '0 of 9'), ('.', '.'))
    roadmap += '<div class="settle-groups">' + ''.join('<div>' + text(label, 'h3') + '<ul class="settle-list">' + ''.join(text(item, 'li') for item in items) + '</ul></div>'
                                                      for label, items in groups) + '</div>'
    roadmap += '<p>' + spans('settlement', 'ramp-options', 'ico-comparison')
    roadmap += text(('Dinheiro, pagamentos e relatórios: ', 'Money, payments and reports: '), 'span')
    roadmap += text(('Financiamento e gastos', 'Funding and spending'), 'a', 'href="transparency.html"') + '.</p></section>'
    roadmap += '<section class="closing-band" id="help">' + text(('Esses pontos são definidos com quem participa. Se você pode ajudar, apresente-se.',
                                                                   'These are worked out with the people who take part. If you can help, introduce yourself.'))
    roadmap += text(('Apresente-se', 'Introduce yourself'), 'a', 'class="button act" href="contact.html"') + '</section>'
    roadmap += partner_line('roadmap.html') + '</main>'
    (root / 'roadmap.html').write_text(page('IMOBX | Project stages', roadmap,
        f'<link rel="stylesheet" href="{asset_v("bands.css")}">', version=guide['version'], lang='pt-BR', title_pt='IMOBX | Etapas do projeto'))

    def flow(items, cls='flow'):
        """A short sequence drawn as connected steps (numbers from the list, no arrow glyphs)."""
        return f'<ol class="{cls}">' + ''.join('<li>' + (text(i[0], 'strong') + text(i[1], 'span') if isinstance(i[0], list) else text(i, 'span')) + '</li>'
                                              for i in items) + '</ol>'

    # Why housing: the wider problem in figures, each with its source and what it does not show.
    why = guide['why']
    # Why housing in the attention pattern (owner-approved package, 25 Oct): the lead's first sentence as the card,
    # the four figures as a row of numbers with their dates and limits kept visible, one home for the money loop
    # (How it works), and a bounded section on how decisions would be shared, marked as a proposal.
    wl = [x.split('. ', 1) for x in why['lead']]
    page_why = '<main class="paper guide-paper why-page band-page" id="main">' + text(why['title'], 'h1')
    page_why += '<div class="key-card">' + text((wl[0][0] + '.', wl[1][0] + '.')) + '</div>'
    page_why += text((wl[0][1], wl[1][1]), 'p', 'class="guide-lead"')
    page_why += on_this_page([(('Os números', 'The figures'), 'figures'), (('Favelas no Rio', 'Favelas in Rio'), 'context'),
                              (('Por que o custo sobe', 'Why costs rise'), 'causes'), (('O que a IMOBX faria', 'What IMOBX would do'), 'answer'),
                              (('Como as decisões seriam divididas', 'How decisions would be shared'), 'organisation')])
    page_why += '<section id="figures">' + text(why['facts_title'], 'h2') + '<ol class="figure-row">'
    for big, fact in zip(why['figures_big'], why['facts']):
        page_why += '<li>' + text(big, 'strong', 'class="figure-big"') + text(fact['text']) + '<p class="source-note">' + text(('Fonte: ', 'Source: '), 'span')
        page_why += text(fact['source'], 'a', f'href="{esc(fact["url"])}"') + '. ' + text(fact['limit'], 'span') + '</p></li>'
    page_why += '</ol></section><section id="context">' + text(why['context_title'], 'h2') + why['context_html']
    page_why += '</section><section id="causes">' + text(why['causes_title'], 'h2') + text(why['causes'])
    page_why += '<p class="source-note">' + text(('Fonte: ', 'Source: '), 'span') + text(why['causes_source'], 'a', f'href="{esc(why["causes_url"])}"') + '. ' + text(why['causes_limit'], 'span') + '</p></section>'
    page_why += '<section id="answer">' + text(why['answer_title'], 'h2') + '<ul>' + ''.join(text(a, 'li') for a in why['answer']) + '</ul>'
    page_why += '<p>' + text(('Como o dinheiro circula: veja como funciona', 'How the money moves: see how it works'), 'a', 'href="rent-to-own.html#payments"') + '</p></section>'
    page_why += '<section id="rent-to-own-or-rent">' + text(why['fleet_title'], 'h2') + text(why['fleet'])
    page_why += text(('As três fases de crescimento', 'The three phases of growth'), 'a', 'href="index.html#como-chegamos"') + '</section>'
    # Bounded context section (owner, 25 Oct): what each neighbourhood decides, what projects share, who answers for it.
    page_why += '<section id="organisation">' + text(why['org_title'], 'h2') + text(why['org_answer'], 'p', 'class="answer"')
    page_why += '<ol class="layer-list org-list">' + ''.join('<li>' + pic + '<h3>' + text(t_, 'span') + '</h3>' + text(b_) + '</li>' for pic, (t_, b_) in zip(ORG_PICS, why['org_cols'])) + '</ol>'
    page_why += text(why['org_note'], 'p', 'class="aside"')
    page_why += '<details class="disclosure"><summary>' + text(('Fontes', 'Sources'), 'span') + '</summary><div class="disclosure-body">'
    page_why += ('<p class="source-note">' + text(('Fonte: ', 'Source: '), 'span') + '<a href="https://wiki.p2pfoundation.net/Will_Ruddick_on_Commitment_Pooling">'
                 + text(('Will Ruddick, sobre compromissos compartilhados (P2P Foundation)', 'Will Ruddick on commitment pooling (P2P Foundation)'), 'span') + '</a>.</p>')
    page_why += ('<p class="source-note">' + text(('Fonte: ', 'Source: '), 'span') + '<a href="https://ixian.pro/the-300-year-anomaly">'
                 + text(("Ramona Tudorancea, 'The 300-Year Anomaly' (Ixian, 28 de setembro de 2026)", "Ramona Tudorancea, 'The 300-Year Anomaly' (Ixian, 28 September 2026)"), 'span') + '</a>.</p>')
    page_why += '</div></details></section>'  # Ostrom's source line has its home on the roadmap (F44)
    page_why += '<section class="closing-band" id="next">'
    page_why += text(('Ver como funciona', 'See how it works'), 'a', 'class="button act" href="rent-to-own.html"') + '</section>'
    page_why += partner_line('why.html') + '</main>'
    (root / 'why.html').write_text(page('IMOBX | Why housing', page_why, f'<link rel="stylesheet" href="{asset_v("bands.css")}"><script src="assets/site.js" defer></script>',
        version=guide['version'], lang='pt-BR', title_pt='IMOBX | Por que moradia'))

    # The token: what it is for, why it is kept apart from the cooperative, and the conditions before it exists
    # (owner, 24 Oct). No percentages or payouts here: allocations stay proposals until a lawyer has seen them.
    tk = guide['token_page']
    tl = [x.split('. ', 1) for x in tk['lead']]
    page_tk = '<main class="paper guide-paper token-page band-page" id="main">' + text(tk['title'], 'h1')
    page_tk += '<div class="key-card">' + text((tl[0][0] + '. ' + tk['bridge_no'][0], tl[1][0] + '. ' + tk['bridge_no'][1])) + '</div>'
    page_tk += text((tl[0][1], tl[1][1]), 'p', 'class="guide-lead"')
    page_tk += on_this_page([(('Para onde iria o dinheiro', 'Where its money would go'), 'purpose'), (('Por que fica separado', 'Why it is separate'), 'separate'),
                             (('Quando poderia ser lançado', 'When it could launch'), 'when'), (('O que a IMOBX não fará', 'What IMOBX will not do'), 'never')])
    page_tk += '<section id="purpose">' + text(tk['purpose_title'], 'h2') + flow(tk['purpose'], 'purpose-list') + text(tk['not']) + '</section>'
    # Two panels with the one-way rule drawn between them (redesign 24 Oct), instead of a table.
    def panel(cls, title, col):
        rows = ''.join('<div>' + text(row[0], 'dt') + text(row[col], 'dd') + '</div>' for row in tk['table'])
        return f'<div class="ct-panel {cls}">' + text(title, 'h3') + '<dl>' + rows + '</dl></div>'
    arrow = ('<svg class="ct-arrow" viewBox="0 0 120 24" aria-hidden="true"><path d="M116 12H6"/><path d="M16 4 6 12l10 8"/></svg>')
    blocked = ('<svg class="ct-arrow ct-blocked" viewBox="0 0 120 24" aria-hidden="true"><path d="M4 12h104"/><path d="M98 4l10 8-10 8"/>'
               '<path class="x" d="M48 2l20 20M68 2 48 22"/></svg>')
    page_tk += '<section id="separate">' + text(tk['separate_title'], 'h2') + '<div class="coop-token">'
    page_tk += panel('ct-coop', tk['table_head'][1], 1)
    page_tk += '<div class="ct-bridge"><p class="ct-yes">' + arrow + text(tk['bridge_yes'], 'span') + '</p>'
    page_tk += '<p class="ct-no">' + blocked + text(tk['bridge_no'], 'span') + '</p></div>'
    page_tk += panel('ct-token', tk['table_head'][2], 2) + '</div>'
    page_tk += text(tk['reasons_title'], 'h3') + '<ul>' + ''.join(text(r, 'li') for r in tk['reasons']) + '</ul></section>'
    page_tk += '<section id="when">' + text(tk['when_title'], 'h2') + flow(tk['when'], 'launch-steps') + text(tk['buyers']) + text(tk['legal']) + full_source('cvm')
    # Names ladder (owner, 25 Oct): platform names only here, with the why, the limits and the founders' link.
    # 'Where would the token trade?': wording approved by the owner on 25 Oct after two revisions (preview only).
    def tk_source(label, url, effect):
        return ('<p class="source-note">' + text(('Fonte: ', 'Source: '), 'span') + f'<a href="{esc(url)}">' + text(label, 'span') + '</a>. ' + text(effect, 'span') + '</p>')
    page_tk += '<details class="disclosure" id="venues"><summary>' + text(tk['venues_title'], 'span') + '</summary><div class="disclosure-body">'
    page_tk += ''.join(text(v) for v in tk['venues'])
    page_tk += tk_source(('As notas técnicas da Arctide (em inglês)', 'Arctide’s technical notes (in English)'), 'https://github.com/0xRustyDev/arctide-docs/blob/main/README.md',
                         ('Descreve as taxas por fundo, cobradas em USDC. Não mostra uso pela IMOBX.', 'Describes per-pool fees charged in USDC. It does not show any IMOBX use.'))
    page_tk += tk_source(('O anúncio da Ethervista de 16 de setembro de 2026', 'Ethervista’s announcement of 16 September 2026'), 'https://t.me/etherfun_trenches/90445',
                         ('É o anúncio da própria empresa. Não foi verificado de forma independente.', 'The company’s own announcement. It has not been independently verified.'))
    page_tk += tk_source(('A lista de riscos do USDC feita pela própria Circle', 'Circle’s own list of USDC risks'), 'https://www.circle.com/legal/usdc-risk-factors',
                         ('Os riscos descritos pela própria emissora.', 'The risks as described by the issuer.'))
    page_tk += '</div></details></section>'
    page_tk += '<section id="never">' + text(tk['never_title'], 'h2') + '<ul>' + ''.join(text(n, 'li') for n in tk['never']) + '</ul>'
    page_tk += text(tk['accounts']) + '</section>'
    page_tk += '<section class="closing-band" id="ask">' + text(tk['closing']) + text(('Fazer uma pergunta', 'Ask a question'), 'a', 'class="button act" href="contact.html"') + '</section>'
    page_tk += '<span id="more"></span>'  # 'Read more' band removed 25 Oct: the menu and the funding page link already lead there
    page_tk += partner_line('token.html') + '</main>'
    (root / 'token.html').write_text(page('IMOBX | The token', page_tk, f'<link rel="stylesheet" href="{asset_v("token.css")}"><link rel="stylesheet" href="{asset_v("bands.css")}"><script src="assets/site.js" defer></script>',
        version=guide['version'], lang='pt-BR', title_pt='IMOBX | O token'))

    # The blockchain page (owner, 25 Oct): how IMOBX would use Arc for its records and money, how a token would
    # connect, what is not decided and what a blockchain cannot do. Plan: BLOCKCHAIN_PAGE_SHAPE_2026-10-25.md.
    # Arc facts checked on the web on 25 Oct 2026 (mainnet live since 16 Sep 2026; privacy features not yet available).
    ch = guide['chain_page']
    def chain_source(label, url, effect):
        return ('<p class="source-note">' + text(('Fonte: ', 'Source: '), 'span') + f'<a href="{esc(url)}">' + text(label, 'span') + '</a>. '
                + text(effect, 'span') + '</p>')
    glyphs = [  # line pictograms in the homepage's style: a lock, two people, an open eye
        '<svg class="vision-glyph" viewBox="0 0 26 26" aria-hidden="true"><rect x="6" y="11" width="14" height="11"/><path d="M9 11V8a4 4 0 0 1 8 0v3"/></svg>',
        '<svg class="vision-glyph" viewBox="0 0 26 26" aria-hidden="true"><circle cx="9" cy="9" r="3.2"/><circle cx="17.5" cy="9" r="3.2"/><path d="M3 21c.8-4 3.2-6 6-6s5.2 2 6 6M13 16.5c1.2-1 2.7-1.5 4.5-1.5 2.8 0 5.2 2 6 6"/></svg>',
        '<svg class="vision-glyph" viewBox="0 0 26 26" aria-hidden="true"><path d="M2 13s4-7 11-7 11 7 11 7-4 7-11 7S2 13 2 13Z"/><circle cx="13" cy="13" r="3.5"/></svg>']
    chain = '<main class="paper guide-paper band-page chain-page" id="main">' + language_controls
    chain += text(ch['title'], 'h1') + '<div class="key-card">' + text(ch['key']) + '</div>'
    chain += text(ch['lead'], 'p', 'class="guide-lead"')
    chain += on_this_page([(label, anchor) for label, anchor in ch['toc']])
    chain += '<section id="layers">' + text(ch['layers_title'], 'h2') + text(ch['layers_answer'], 'p', 'class="answer"')
    chain += '<ol class="layer-list">' + ''.join('<li>' + '<h3>' + g + text(name, 'span') + '</h3>' + text(what) + '<p class="layer-who">' + text(ch['layers_who'], 'strong') + ' ' + text(who, 'span') + '</p></li>'
                                                for g, (name, what, who) in zip(glyphs, ch['layers'])) + '</ol>'
    chain += text(ch['layers_why'])
    chain += '<details class="disclosure"><summary>' + text(ch['glossary_title'], 'span') + '</summary><div class="disclosure-body"><dl class="glossary">'
    chain += ''.join(text(term, 'dt') + text(meaning, 'dd') for term, meaning in ch['glossary']) + '</dl></div></details>'
    chain += '<details class="disclosure"><summary>' + text(('Fontes', 'Sources'), 'span') + '</summary><div class="disclosure-body">'
    chain += chain_source(('As notas técnicas da Arc (em inglês)', 'Arc’s technical notes (in English)'), 'https://docs.arc.io/arc/concepts/system-overview.md',
                          ('Diz que a privacidade ainda não está disponível. Não analisa a IMOBX.', 'Says privacy is not yet available. It does not review IMOBX.'))
    chain += chain_source(('Seus direitos pela lei brasileira de proteção de dados (LGPD)', 'Your rights under Brazil’s data protection law (LGPD)'), 'https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm',
                          ('Direitos de quem tem dados pessoais tratados. Não trata de blockchain.', 'The rights of people whose personal data is processed. It does not mention blockchains.')) + '</div></details></section>'
    chain += '<section id="request">' + text(ch['request_title'], 'h2') + text(ch['request_answer'], 'p', 'class="answer"')
    chain += '<ol class="step-strip">' + ''.join(text(st, 'li') for st in ch['request_steps']) + '</ol>'
    chain += text(guide['dao_operations']['status'], 'p', 'class="aside"')
    chain += '<details class="disclosure"><summary>' + text(ch['request_fold'], 'span') + '</summary><div class="disclosure-body">'
    # Tasks and handovers have their home on the roadmap (facts F09, F10); the help-desk paragraph lives here.
    chain += text(pick(guide_question('flock-siah')['a'][4], [0, 3, 4]))
    chain += '<p>' + text(ch['request_more'], 'a', 'href="roadmap.html#governance"') + '</p>'
    chain += short_source('digital') + '</div></details></section>'
    chain += '<section id="records">' + text(ch['records_title'], 'h2') + text(ch['records_answer'], 'p', 'class="answer"')
    chain += '<div class="guide-table"><table><thead><tr>' + ''.join(text(h, 'th', 'scope="col"') for h in ch['records_head']) + '</tr></thead><tbody>'
    chain += ''.join('<tr>' + text(r[0], 'th', 'scope="row"') + ''.join(text(c, 'td') for c in r[1:]) + '</tr>' for r in ch['records']) + '</tbody></table></div></section>'
    chain += '<section id="token">' + text(ch['token_title'], 'h2') + marked(*ch['token_answer_marked']) + text(ch['token_body'])
    chain += '<p>' + text(ch['token_link'], 'a', 'href="token.html"') + '</p></section>'
    chain += '<section id="open">' + text(ch['open_title'], 'h2') + text(ch['open_answer'], 'p', 'class="answer"')
    chain += '<div class="open-paths"><div>' + text(ch['open_runs_title'], 'h3') + '<ol class="path-list">' + ''.join(text(o, 'li') for o in ch['open_runs']) + '</ol></div>'
    chain += '<div>' + text(ch['open_token_title'], 'h3') + '<ol class="path-list">' + ''.join(text(o, 'li') for o in ch['open_token']) + '</ol></div></div>'
    chain += text(ch['open_note']) + '<div class="window">' + text(ch['same_title'], 'h3') + '<ul>' + ''.join(text(o, 'li') for o in ch['same']) + '</ul></div></section>'
    chain += '<section id="limits">' + text(ch['limits_title'], 'h2') + marked(*ch['limits_answer_marked'])
    chain += '<ul>' + ''.join(text(o, 'li') for o in ch['limits']) + '</ul>'
    chain += '<details class="disclosure"><summary>' + text(('Fontes', 'Sources'), 'span') + '</summary><div class="disclosure-body">'
    chain += chain_source(('O anúncio da Circle de que a Arc entrou em funcionamento (16 de setembro de 2026)', 'Circle’s announcement that Arc went live (16 September 2026)'),
                          'https://www.circle.com/pressroom/circle-launches-arc-mainnet-an-economic-operating-system-for-the-internet',
                          ('Anuncia a rede e diz que nenhum regulador a aprovou. Não analisa a IMOBX.', 'Announces the network and says no regulator has approved it. It does not review IMOBX.'))
    chain += chain_source(('As empresas que operam a rede Arc', 'The companies that run the Arc network'),
                          'https://www.arc.io/pressroom/circle-announces-founding-validator-cohort-and-major-integrations-for-arc-ahead-of-september-16-mainnet-launch',
                          ('Lista as empresas fundadoras. Não analisa a IMOBX.', 'Lists the founding companies. It does not review IMOBX.'))
    chain += chain_source(('A lista de riscos do USDC feita pela própria Circle', 'Circle’s own list of USDC risks'), 'https://www.circle.com/legal/usdc-risk-factors',
                          ('Diz que a Circle pode bloquear USDC. Não analisa a IMOBX.', 'Says Circle can freeze USDC. It does not review IMOBX.'))
    chain += '</div></details></section>'  # 'does not show that any of it works yet' is already beside the request steps
    chain += '<section class="closing-band" id="help">' + text(ch['closing']) + text(ch['button'], 'a', 'class="button act" href="contact.html"') + '</section>'
    chain += partner_line('blockchain.html') + '</main>'
    (root / 'blockchain.html').write_text(page('IMOBX | Shared records', chain, f'<link rel="stylesheet" href="{asset_v("flow.css")}"><link rel="stylesheet" href="{asset_v("bands.css")}">',
        version=guide['version'], lang='pt-BR', title_pt='IMOBX | Registros compartilhados'))

    stub_targets = {item['id']: ('rent-to-own.html' if item['id'] in HOUSEHOLD_FAQ else 'transparency.html')
                    for item in guide['questions']}
    stub_targets.update({'thanks-zeal-lets': 'transparency.html', 'euler': 'transparency.html'})
    (root / 'faq.html').write_text(redirect_stub(
        'IMOBX | Perguntas sobre o modelo', 'Perguntas sobre o modelo', 'rent-to-own.html#questions',
        'Open the current version', per_question=stub_targets))

    home = root / 'index.html'
    overview = guide['home_overview']
    # Second review, 25 Oct: the homepage's agreement section repeated rent-to-own; only its link targets remain.
    housing = ('<section class="content wrap solution-section" id="modelo" data-anchor-only>'
               '<span id="participation-summary"></span><span id="home-purchase-title"></span><span id="visao-rafael-old"></span></section>')
    home_source, count = re.subn(r'<section class="content wrap solution-section" id="modelo"[^>]*>.*?</section>',
                                lambda _: housing, home.read_text(), count=1, flags=re.S)
    if count != 1:
        raise ValueError('Expected one homepage housing explanation.')
    phases = guide['phases']
    phases_html = ('<section class="content wrap" id="como-chegamos">' + text(phases['title'], 'h2') + text(phases['intro'])
                   + flow(phases['steps'], 'flow flow-phases') + text(phases['note'], 'p', 'class="fine"') + '</section>')
    source, count = re.subn(r'<section class="content wrap" id="como-chegamos">.*?</section>', lambda _: phases_html, home_source, count=1, flags=re.S)
    if count != 1:
        raise ValueError('Expected one homepage section for how we get there.')
    home.write_text(source)
