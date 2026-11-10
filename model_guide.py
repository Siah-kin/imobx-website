"""Public roadmap and model explanation. Content only; no governance execution."""
import json
import math
import re
import hashlib as _hashlib
from money_flow import money_flow_html, cascade_html, route_html, ledger_flow_html, gov_flow_html, FUNDING_SCRIPT, SCRIPT as MF_SCRIPT

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


PARTNER_LINKS = [('transparency.html', ('de onde viriam os recursos', 'where the funding would come from')),
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


# Terms (decision 21): the status and conditions the copy sweep of 28 Oct moved out of the pages, said once at the end
# of Project stages. Text from TERMS_PAGE_DRAFT_2026-10-28.md, sections 1 to 6, with the coordinator's defaults for its
# three flagged lines ('service income' and the foreign-organisation CNPJ line left out; no Central Bank claim).
TERMS_TITLE = ('O que está decidido, e o que ainda não', 'What is decided, and what is not yet')
TERMS = [
    (('Onde a IMOBX está hoje', 'Where IMOBX stands today'), [
        ('A IMOBX ainda está em preparação, então ainda não há casas para alugar ou comprar.',
         'IMOBX is still in preparation, so there are no houses to rent or buy yet.'),
        ('Planejamos fundar a IMOBX como uma cooperativa habitacional, que ainda não está registrada.', 'We plan to found IMOBX as a housing cooperative, which is not registered yet.'),
        ('A própria IMOBX ainda não assinou nenhum contrato.',
         'IMOBX itself has not signed any contracts yet.'),
        ('Nenhuma autoridade pública aprovou ainda os planos da IMOBX.', 'No public authority has approved IMOBX’s plans yet.'),
    ]),
    (('Casas e famílias', 'Houses and families'), [
        ('O preço, o valor mensal, o prazo e quem pode participar são definidos para cada projeto, num contrato escrito, antes de qualquer mudança.',
         'The price, the monthly amount, the term and who can join are set for each project, in a written agreement, before anyone moves in.'),
        ('Tudo o que uma família recebe como promessa, como uma devolução, mais prazo para pagar ou um desconto, vale quando estiver escrito no contrato assinado.',
         'Anything a family is promised, such as a refund, extra time to pay or a discount, counts once it is written into their signed agreement.'),
    ]),
    (('Recursos', 'Funding'), [
        ('Os recursos vêm primeiro de uma campanha de financiamento coletivo em reais, e depois de financiamento ligado ao ODS 11.',
         'Funding comes first from a crowdfunding campaign in reais, then from funding linked to UN Goal 11.'),
        (('Veja como os recursos são gastos em ', 'See how the funding is spent on '), ('Custos e recursos', 'Costs and funding'), 'transparency.html'),
        ('Só começamos a construir quando os recursos para isso estiverem no banco.', 'We start building only once the funding for it is in the bank.'),
    ]),
    (('Leis', 'Law'), [
        ('Três conjuntos de regras brasileiras definem como a IMOBX é montada: o cadastro na Receita Federal; o Código Civil, que decide o momento em que uma casa passa legalmente a ser da família; e a Lei 13.019, que vale se a IMOBX trabalhar com um órgão público, como a prefeitura.',
         'Three sets of Brazilian rules shape how IMOBX is set up: registering with the tax office (Receita Federal); the Civil Code, which decides the moment a house legally becomes the family’s; and Law 13.019, which applies if IMOBX works with a public body such as the city.'),
    ]),
]


def build_guide(root, page, tr, esc, language_controls):
    def asset_v(name):
        """assets/<name>?v=<hash>: a changed stylesheet is fetched again instead of served from the browser's cache."""
        return f'assets/{name}?v=' + _hashlib.sha256((root / 'assets' / name).read_bytes()).hexdigest()[:10]
    guide = json.loads((root / 'model-guide.json').read_text())
    NL_LOOKUP = json.loads((root / 'i18n' / 'nl.json').read_text())  # Dutch for SVG labels and image alts built here

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
        'cash': ('Nosso whitepaper sobre como os recursos seriam administrados (em inglês)', 'Our whitepaper on how funding would be handled (in English)'),
        'rights': ('Whitepaper, seção 8: para que serve o token (em inglês)', 'Whitepaper, section 8: what the token is for'),
        'digital': ('Nosso whitepaper sobre o que passaria a ser digital (em inglês)', 'Our whitepaper on what would become digital (in English)'),
        'technical': ('Guia do piloto, seção 6: escopo e aceitação (em inglês)', 'Pilot guide, section 6: scope and acceptance'),
        'roadmap': ('Etapas do projeto', 'Project stages'),
        'charter': ('Etapas do projeto: quem decide o quê', 'Project stages: who decides what'),
        'cost': ('Nosso whitepaper sobre os custos (em inglês)', 'Our whitepaper on the costs (in English)'),
        'sinapi': ('SINAPI-RJ: o custo de cada item da obra (Caixa e IBGE)', 'SINAPI-RJ: the cost of each building item (Caixa and IBGE)'),
        'cub': ('CUB-RJ: o custo por m², setembro de 2026 (Sinduscon-Rio)', 'CUB-RJ: the cost per m², September 2026 (Sinduscon-Rio)'),
        'cnpj': ('Registro de organizações estrangeiras na Receita Federal (CNPJ)', 'Tax registration for foreign organisations (Receita Federal)'),
        'title': ('Quando a propriedade de um imóvel passa a outra pessoa (Código Civil)', 'When ownership of a property passes (Civil Code)'),
        'mb': ('Mercado Bitcoin · elegibilidade de contas', 'Mercado Bitcoin · account eligibility'),
        'bcb': ('As regras do Banco Central para serviços com criptoativos', 'Brazil’s Central Bank rules for crypto services'),
        'settlement': ('Fluxo reais ↔ moeda digital', 'Reais ↔ digital currency flow'),
        'ramp-options': ('Opções de conversão e elegibilidade', 'Conversion options and eligibility'),
        'community-economy': ('Economia comunitária proposta', 'Proposed community economy'),
        'token-study': ('OCDE · Estudo sobre registros de ativos digitais', 'OECD · Study of digital asset records'),
        'reference-token': ('Como o token funciona', 'How the token works'),
    }

    # What each source does and does not establish. One line per source, shown under the paragraph it supports.
    source_effect = {
        'cost': ('Mostra os custos como Rafael os enviou. Não mostra um preço nem um pagamento mensal para uma família.',
                 'Shows the costs as Rafael supplied them. It does not show a price or monthly payment for a family.'),
        'digital': ('Descreve o trabalho digital proposto. Não mostra que algo disso já funciona.',
                    'Describes the proposed digital work. It does not show that any of it works yet.'),
        'cash': ('Descreve a política de caixa proposta. É uma proposta, não uma regra aprovada.',
                 'Describes the proposed cash policy. It is a proposal, not an approved rule.'),
        'rights': ('Descreve o token self-compounding e os quatro V. O token ainda não foi emitido.',
                   'Describes the self-compounding token and its four V’s. The token has not been issued yet.'),
        'charter': ('Mostra quem decidiria o quê. As regras ainda não estão decididas.',
                    'Shows who would decide what. The rules are not decided yet.'),
        'roadmap': ('Mostra as etapas e o que precisa estar pronto em cada uma. Não define datas.',
                    'Shows the stages and what must be ready in each. It sets no dates.'),
        'sinapi': ('Dá o custo de cada item e serviço de uma obra. Serve para conferir o orçamento item a item que o Rafael vai entregar.',
                   'Prices each item and service in a build. It is used to check the item-by-item budget Rafael is preparing.'),
        'cub': ('Dá o custo por m² em que o Rafael baseia o preço: R$ 2.476 no padrão R8-N, em setembro de 2026.',
                'Gives the cost per m² Rafael bases the price on: R$2,476 for the R8-N standard in September 2026.'),
        'reference-token': ('Explica a taxa do token, para onde ela vai e os quatro V. O token ainda não foi emitido.',
                            'Explains the token’s fee, where it goes and the four V’s. The token has not been issued yet.'),
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
                'Is the Central Bank rule the plan cites on digital currency. Legal advisers still need to confirm what it requires of IMOBX.'),
        'settlement': ('Mostra o caminho proposto dos recursos. Nenhum provedor está confirmado.',
                       'Shows the proposed route of the funding. No provider is confirmed.'),
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
        (('Agora: em preparação', 'Now: preparing'), False),
        (('Depois disso', 'After that'), True)]

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
    # Copy sweep, 28 Oct (review A, owner 'proceed'): the card says how rent-to-own works once, the lead gives the
    # price rule, and one pointer line sends status to 'Where we are now' (decision 21).
    resident += text(journey['title'], 'h1')
    resident += '<div class="key-card">' + text(rp['key']) + '</div>'
    resident += text(rp['lead'], 'p', 'class="guide-lead"')
    resident += ('<p>' + text(rp['status_line'], 'span') + ' '
                 + text(rp['status_link'], 'a', 'href="index.html#onde-estamos"') + '</p>')
    resident += on_this_page([(('Pagamentos mensais', 'Monthly payments'), 'payments'), (('Reparos', 'Repairs'), 'repairs'),
                              (('Decisões dos moradores', 'Residents’ decisions'), 'decisions'),
                              (('Saída ou atraso no pagamento', 'Leaving or missed payments'), 'hardship')])

    resident += '<section id="payments">' + span_ids(anchors['payments'] + ['questions'])
    rec = [x.split('. ', 1) for x in rp['record']]
    resident += text(journey['steps_title'], 'h2', 'id="money"') + text((rec[0][0] + '.', rec[1][0] + '.'), 'p', 'class="answer"')
    resident += money_flow_html(text) + text((rec[0][1], rec[1][1]))
    resident += text(('Quanto custa construir as primeiras casas', 'What the first houses cost to build'),
                     'a', 'href="transparency.html#budgets"') + '</section>'

    resident += '<section id="repairs">' + span_ids(anchors['repairs']) + text(journey['repairs_title'], 'h2')
    resident += '<ol class="step-strip">' + ''.join(text(st, 'li') for st in rp['repair_steps']) + '</ol>'
    resident += text(rp['repair_note']) + text(('Como contestar uma decisão', 'How to question a decision'),
                                                'a', 'href="governance.html"') + '</section>'

    resident += '<section id="decisions">' + span_ids(anchors['decisions']) + text(rp['decisions_heading'], 'h2')
    resident += '<div class="two-sides"><div><ul>'
    resident += ''.join(text(x, 'li') for x in rp['decide']) + '</ul></div>'
    resident += '<div class="side-protect">' + text(rp['protect_title'], 'strong', 'class="side-title"') + '<ul>'
    resident += ''.join(text(x, 'li') for x in rp['protect']) + '</ul></div></div>'
    resident += text(rp['invest'], 'p', 'class="invest-line"') + '</section>'

    resident += '<section id="hardship" class="soft-panel">' + span_ids(anchors['hardship']) + text(journey['hardship_title'], 'h2', 'id="leaving"')
    resident += ''.join(text(pair) for pair in journey['hardship'])
    resident += text(('O que ainda não foi decidido', 'What is still undecided'), 'a', 'href="roadmap.html#open-terms"') + '</section>'

    resident += '<section id="next" class="closing-band">' + span_ids(anchors['next']) + text(rp['interest'])
    resident += text(('Conte do que a sua família precisa', 'Tell us what your family needs'), 'a', 'class="button act" href="contact.html?role=resident"') + '</section>'
    resident += '<span id="funding"></span><span id="property"></span>' + partner_line('rent-to-own.html') + '</main>'
    (root / 'rent-to-own.html').write_text(page('IMOBX | Renting and buying a home', resident,
        f'<link rel="stylesheet" href="{asset_v("flow.css")}"><link rel="stylesheet" href="{asset_v("bands.css")}">' + MF_SCRIPT,
        version=guide['version'], lang='pt-BR', title_pt='IMOBX | Aluguel e compra da casa'))

    # Roadmap in the attention pattern (owner, 25 Oct): the question as title, one orange key card (where we stand),
    # an "on this page" list, an answer line under each question, background in quiet folds, commitments visible,
    # one orange action at the end. See ATTENTION_ANALYSIS_2026-10-25.md.
    roadmap = '<main class="paper guide-paper band-page roadmap-page" id="main">' + language_controls
    # Copy sweep, 28 Oct (review B, owner 'proceed'): status said once in the card; each stage is two or three
    # plain sentences instead of a labelled form; 'Who takes part' moves to Take part (its anchors stay here).
    roadmap += text(('Onde a IMOBX está agora e o que vem depois', 'Where IMOBX is now, and what comes next'), 'h1')
    # Owner, 31 Oct: his chat words pasted as copy, and a byline, read as AI slop; the reason comes first, then the status.
    roadmap += '<div class="key-card">' + text(('Ter a própria casa é uma das necessidades mais profundas que existem, e para muitas famílias do Rio ela continua fora de alcance.',
                     'A home of your own is one of the deepest needs people have, and for many families in Rio it stays out of reach.'))
    # Owner, 8 Nov: the two favela photos come back here, under the need they show (removed on 28 Oct by mistake).
    roadmap += text(('Com a crise da moradia no Rio, as favelas nos morros crescem rápido.',
                     'With Rio’s housing crisis, the favelas on its hillsides are growing fast.')) + '</div>'
    roadmap += '<figure class="favela-pair"><div class="lead-figures">'
    for f, alt in [('community-bay-circles.jpg', ('Favelas nos morros ao redor da baía, marcadas com círculos', 'Favelas on the hillsides around the bay, marked with circles')),
                   ('community-dusk-circles.jpg', ('Favelas nos morros ao entardecer, marcadas com círculos', 'Favelas on the hillsides at dusk, marked with circles'))]:
        roadmap += f'<img src="assets/{f}" width="1448" height="1086" loading="lazy" alt="{esc(alt[0])}" data-alt-pt="{esc(alt[0])}" data-alt-en="{esc(alt[1])}" data-alt-nl="{esc(NL_LOOKUP.get(alt[1], alt[1]))}">'
    roadmap += '</div><figcaption>' + text(('Os círculos marcam favelas nos morros, ao redor da baía e ao entardecer.', 'The circles mark favelas on the hillsides, around the bay and at dusk.'), 'span') + '</figcaption></figure>'
    roadmap += text(('Ter a própria casa é uma das necessidades mais profundas que existem, e para muitas famílias do Rio ela continua fora de alcance. Estamos preparando o primeiro projeto no Rio de Janeiro. Vamos marcar as datas quando a cooperativa estiver registrada e o terreno dos cinco apartamentos novos escolhido.',
                     'A home of your own is one of the deepest needs people have, and for many families in Rio it stays out of reach. We are preparing the first project in Rio de Janeiro. We’ll set dates once the cooperative is registered and the plot for the five new flats is chosen.'), 'p', 'class="guide-lead" id="where-we-stand"')
    roadmap += on_this_page([(('O caminho até os primeiros apartamentos', 'The path to the first flats'), 'stages'),
                             (('Como os cinco primeiros apartamentos serão financiados', 'How the first five flats will be funded'), 'funding'),
                             (('No que o Rafael está trabalhando agora', 'What Rafael is working on now'), 'rafael-now'),
                             (('Onde a primeira família vai morar', 'Where the first family will live'), 'cases'),
                             (('A vila que imaginamos', 'The village Rafael imagines'), 'village'),
                             (('O que a construtora do Rafael está construindo', 'What Rafael’s company is building'), 'building'), (TERMS_TITLE, 'terms')])


    # The path (owner, 28-29 Oct): one line that draws itself as you scroll, from preparation to the three stages.
    ICONS = {
        'foundation': '<path d="M5 13 14 6l9 7"/><path d="M7 12v10h8"/><rect x="15" y="15" width="9" height="10" rx="1"/><path d="M17.5 19h4M17.5 22h4"/>',
        'cash-and-charter': '<circle cx="10" cy="9" r="3.2"/><circle cx="19" cy="9" r="3.2"/><path d="M4 23c.7-4 3.2-6 6-6s5.3 2 6 6"/><path d="M15.5 17.4c1-.3 2.2-.4 3.5-.4 2.8 0 5.3 2 6 6"/>',
        'digital-trial': '<rect x="5" y="4" width="18" height="21" rx="1.5"/><path d="M9 9h10M9 13h10M9 17h4"/><path d="m15.5 19 2.2 2.2 4.3-4.6"/>',
        'token-decision': '<path d="M14 3.5 23 7v6.5c0 5.5-4 9.2-9 11-5-1.8-9-5.5-9-11V7z"/><ellipse cx="14" cy="11.5" rx="4.5" ry="1.8"/><path d="M9.5 11.5v4c0 1 2 1.8 4.5 1.8s4.5-.8 4.5-1.8v-4"/>',
        'funded-pilot': '<path d="M4 14 14 5l10 9"/><path d="M7 12v12h14V12"/><path d="M12 24v-6h4v6"/>',
        'replication': '<path d="M2 15 7.5 10l5.5 5"/><path d="M4 14v8h7v-8"/><path d="M15 15l5.5-5 5.5 5"/><path d="M17 14v8h7v-8"/><path d="M8.5 8 14 3l5.5 5"/><path d="M10.5 7v3M17.5 7v3"/>',
        'owner-platform': '<circle cx="9" cy="14" r="4.5"/><path d="M13.5 14H25M21 14v4M24 14v3"/><path d="M8 13h2"/>',
    }
    def icon(key):
        return f'<svg class="path-icon" viewBox="0 0 28 28" aria-hidden="true">{ICONS[key]}</svg>'
    TRACK_LINES = {  # owner, 31 Oct: one line each, taken from the track's own detail
        'foundation': ('Estamos preparando o registro da IMOBX como cooperativa habitacional. Também estamos organizando os papéis do imóvel, transformando a estimativa do Rafael num orçamento de obra em reais e escrevendo os termos que uma família assina para alugar uma casa e depois comprá-la.',
                       'We’re preparing to register IMOBX as a housing cooperative. We’re also getting the property papers in order, turning Rafael’s estimate into a building budget in reais, and writing the terms a family signs to rent a house and then buy it.'),
        'cash-and-charter': ('Os futuros moradores vão ajudar a escrever as regras da casa, e uma regra só começa depois que eles opinarem.',
                             'Future residents will help write the house rules, and a rule starts only once they’ve had their say.'),
        'digital-trial': ('Antes de gastar os recursos de alguém, planejamos fazer um pequeno pagamento de teste e conferir duas coisas: quem o aprovou e se o nosso registro bate com o extrato do banco, para sabermos que a conferência funciona antes de passar valores de verdade.',
                          'Before we spend anyone’s funding, we plan to send one small test payment and check two things: who approved it, and whether our record of it matches the bank statement, so we know the checks work before real amounts go through.'),
        'token-decision': ('Planejamos guardar uma reserva para as contas e para o que prometemos às famílias, para que um mês fraco não pare a obra. Se a reserva ficar baixa, gastos novos esperam até ela se recompor.',
                           'We plan to keep a reserve for the bills and for what we’ve promised families, so one slow month doesn’t stop the building work. If the reserve runs low, new spending waits until it’s back up.'),
    }
    # Owner, 9 Nov ("roadmap remains underutilised"): one board, every step with where it stands: done, now, next, then.
    roadmap += '<section id="stages">' + text(('O caminho até os primeiros apartamentos', 'The path to the first flats'), 'h2')
    roadmap += text(('Seis passos, em ordem. Estamos no passo 2.', 'Six steps, in order. We are at step 2.'), 'p', 'class="route-lead"')
    BOARD = [('Pronto', 'Done', 'Klaar', [('O custo de um apartamento e de cinco, calculado pelo índice público de custo da construção do Rio (CUB), em setembro de 2026.', 'The cost of one flat and of five, worked out from Rio’s public building-cost index (CUB), September 2026.', 'De kosten van één appartement en van vijf, berekend met de openbare bouwkostenindex van Rio (CUB), september 2026.'), ('O contrato de obra de dois lofts da construtora do Rafael, assinado em janeiro de 2026.', 'The building contract for two lofts by Rafael’s company, signed January 2026.', 'Het bouwcontract voor twee lofts van het bedrijf van Rafael, getekend in januari 2026.'), ('As respostas do Rafael sobre custo, terreno, atraso no pagamento e recursos, de 4 a 6 de novembro de 2026.', 'Rafael’s answers on cost, site, late payment and funding, 4 to 6 November 2026.', 'Rafaels antwoorden over kosten, kavel, betalingsachterstand en financiering, 4 tot 6 november 2026.')]), ('Agora', 'Now', 'Nu', [('O apartamento de Guadalupe: estamos avaliando um contrato de aluguel com compra, com aluguel menor, para a família que mora lá, e perguntando se quer participar.', 'The Guadalupe flat: we are considering a rent-to-own agreement with a lower rent for the family that rents there, and asking whether they want to take part.', 'Het appartement in Guadalupe: we overwegen een huurkoopovereenkomst met een lagere huur voor het gezin dat er huurt en vragen of het wil meedoen.'), ('O John está nomeando um advogado independente, um contador e um engenheiro independente, nenhum ligado à construtora do Rafael, para conferir os contratos, organizar como os pagamentos são registrados e conferir a obra.', 'John is appointing an independent lawyer, an accountant and an independent engineer, none of them linked to Rafael’s company, to check the agreements, set up how payments are recorded and check the building work.', 'John benoemt een onafhankelijke advocaat, een boekhouder en een onafhankelijke ingenieur, geen van hen verbonden aan het bouwbedrijf van Rafael, om de overeenkomsten te controleren, de registratie van betalingen te regelen en het bouwwerk te controleren.'), ('O custo de um apartamento confirmado para um prédio de cinco.', 'The cost of one flat confirmed for a building of five.', 'De kosten van één appartement bevestigd voor een gebouw van vijf.'), ('Um terreno de 200 a 300 m² em Anchieta, Pavuna, Bangu ou Santa Cruz.', 'A plot of 200 to 300 m² in Anchieta, Pavuna, Bangu or Santa Cruz.', 'Een kavel van 200 tot 300 m² in Anchieta, Pavuna, Bangu of Santa Cruz.'), ('A vaga de apoio à captação, aberta agora: começa organizando os materiais que já temos e depois pesquisa os caminhos de financiamento.', 'The fundraising role, open now: it starts by sorting the materials we already have, then researches the funding routes.', 'De functie voor fondsenwerving, nu open: die begint met het ordenen van het bestaande materiaal en onderzoekt daarna de financieringsroutes.')]), ('Em seguida', 'Next', 'Hierna', [('Registrar a cooperativa.', 'Register the cooperative.', 'De coöperatie inschrijven.'), ('Um pagamento de teste, pequeno: quem aprovou, e se as nossas contas batem com o extrato do banco.', 'A small test payment: who approved it, and whether our books match the bank statement.', 'Een kleine testbetaling: wie die goedkeurde, en of onze boeken kloppen met het bankafschrift.'), ('Uma reserva para as contas e para o que prometemos às famílias. Se ela baixar, os gastos novos esperam.', 'A reserve for the bills and for what we have promised families. If it runs low, new spending waits.', 'Een reserve voor de rekeningen en voor wat we gezinnen hebben beloofd. Loopt ze laag, dan wacht nieuwe uitgave.'), ('A campanha de financiamento coletivo: escolher a plataforma, escrever as recompensas, definir a meta e abrir.', 'The crowdfunding campaign: choose the platform, write the rewards, set the goal and open it.', 'De crowdfundingcampagne: het platform kiezen, de beloningen schrijven, het doel bepalen en openen.'), ('Pedidos de financiamento ligado ao ODS 11 da ONU e a outros caminhos que a vaga de captação encontrar.', 'Applications for funding linked to UN Goal 11 and to other routes the fundraising role finds.', 'Aanvragen voor financiering via VN-doel 11 en andere routes die de functie voor fondsenwerving vindt.')]), ('Depois', 'Then', 'Daarna', [('Se uma família topar, ela assina o contrato do prédio de Guadalupe.', 'If a family agrees, it signs the agreement for the Guadalupe building.', 'Als een gezin meedoet, tekent het de overeenkomst voor het gebouw in Guadalupe.'), ('Construir cinco apartamentos de cada vez, quando o financiamento e as licenças estiverem garantidos.', 'Build five flats at a time, once funding and permits are in place.', 'Telkens vijf appartementen bouwen, zodra financiering en vergunningen rond zijn.'), ('Os moradores ajudam a escrever as regras da casa, e uma regra só começa depois que eles opinarem.', 'Residents help write the house rules, and a rule starts only once they have had their say.', 'Bewoners helpen de huisregels schrijven, en een regel gaat pas in als zij hun zegje hebben gedaan.'), ('Avaliar as primeiras casas, depois abrir mais bairros e, mais tarde, receber imóveis de outros proprietários.', 'Review the first houses, then open more neighbourhoods and, later, take in other owners’ properties.', 'De eerste huizen evalueren, daarna meer buurten openen en later woningen van andere eigenaren opnemen.')])]
    # Owner, 10 Nov: the roadmap must be visual and quick to take in, not a notebook page. A path of six steps (the map),
    # then one readable card per step (the detail). Every board item keeps its place.
    STOPS = [
        ('done', 0, ('Custos calculados', 'Costs worked out'), ('O custo de um apartamento e de cinco, pelo índice público de custo da construção do Rio.', 'The cost of one flat and of five, from Rio’s public building-cost index.'), None, [0, 1]),
        ('now', 1, ('Preparando', 'Preparing'), ('Avaliando uma oferta de aluguel com compra no prédio de Guadalupe, conferentes independentes, busca do terreno.', 'Considering a rent-to-own offer for the Guadalupe building, independent checkers, plot search.'), None, [1, 4]),
        ('next', 2, ('Registrar a cooperativa', 'Register the cooperative'), ('Um pagamento de teste e uma reserva para as contas.', 'A test payment and a reserve for the bills.'), None, [1, 2]),
        ('next', 2, ('Campanha de financiamento coletivo', 'Crowdfunding campaign'), ('Em reais, depois ODS 11 (cidades sustentáveis) e outros financiadores.', 'In reais, then UN Goal 11 (sustainable cities) and other funders.'), ('Aqui entra o financiamento', 'Funding comes in here'), [3, 4]),
        ('then', 3, ('Uma família assina', 'A family signs'), ('Se uma família topar, no prédio de Guadalupe. Depois, os moradores escrevem as regras da casa.', 'If a family agrees, in the Guadalupe building. Residents then write the house rules.'), None, [0, 2, 3]),
        ('then', 3, ('Construir cinco apartamentos', 'Build five flats'), ('Começa quando o custo total estiver na conta.', 'Starts once the full cost is in the bank.'), ('Cerca de R$892.000', 'About R$892,000'), [1]),
    ]
    roadmap += '<ol class="route-map">'
    for n, (key, col, title, summary, tag, idxs) in enumerate(STOPS, 1):
        roadmap += (f'<li class="route-stop route-{key}"><span class="route-dot">' + ('✓' if key == 'done' else str(n)) + '</span>'
                    + text((BOARD[col][0], BOARD[col][1]), 'span', 'class="route-chip"') + '<strong class="route-title">' + text(title, 'a', f'href="#step-{n}"') + '</strong>'
                    + text(summary, 'span', 'class="route-sum"') + (text(tag, 'span', 'class="route-tag"') if tag else '') + '</li>')
    roadmap += '</ol>'
    roadmap += '<h3 class="route-detail-head">' + text(('O que acontece em cada passo', 'What happens at each step'), 'span') + '</h3><div class="route-detail">'
    for n, (key, col, title, summary, tag, idxs) in enumerate(STOPS, 1):
        roadmap += (f'<article id="step-{n}" class="route-card route-card-{key}"><h4><span class="route-dot">' + ('✓' if key == 'done' else str(n)) + '</span>' + text(title, 'span') + '</h4><ul>'
                    + ''.join(text((BOARD[col][3][i][0], BOARD[col][3][i][1]), 'li') for i in idxs)
                    + ('<li>' + text(('No que o Rafael está trabalhando agora', 'What Rafael is working on now'), 'a', 'href="#rafael-now"') + '</li>' if key == 'now' else '') + '</ul></article>')
    roadmap += '</div>'
    housing_membership = ('Na proposta, as famílias se associam a uma cooperativa habitacional e assinam seus próprios contratos de moradia. Elas não precisam comprar nem ter tokens.', 'Under the proposal, families join a housing cooperative and sign their own housing agreements. They do not need to buy or hold tokens.')
    roadmap += ('<div class="route-later">' + text(('Mais adiante: o token da IMOBX', 'Later: the IMOBX token'), 'h3')
                + text(('A IMOBX planeja um token opcional que ajuda a financiar o trabalho da comunidade. As famílias nunca precisam dele, e nenhuma votação sobre o token pode mudar o contrato de moradia de uma família.',
                        'IMOBX plans an optional token that helps fund community work. Families never need it, and no token vote can change a family’s housing agreement.'), 'p')
                + '<p>' + text(('Como o token funciona', 'How the token works'), 'a', 'href="token.html"') + '</p></div></section>')


    # Owner, 9 Nov: the roadmap shows the funding strategy (crowdfunding first, then UN SDG 11, then other routes the
    # fundraising role researches) and Rafael's progress as a sequence. Draft: ROADMAP_FUNDING_PROGRESS_DRAFT_2026-11-09.md.
    roadmap += '<section id="funding">' + text(('Como os cinco primeiros apartamentos serão financiados?', 'How will the first five flats be funded?'), 'h2')
    roadmap += text(('A obra só começa quando o custo total dos cinco apartamentos estiver na conta bancária da cooperativa. Levantamos esse valor nesta ordem. Os custos e as fontes de financiamento estão em Custos e recursos.', 'Building starts once the full cost of the five flats is in the cooperative’s bank account. We raise it in this order. The costs and the sources of funding are on Costs and funding.'), 'p')
    roadmap += '<ol class="funding-cards">'
    for head, body in [
        (('Financiamento coletivo em reais', 'Crowdfunding in reais'),
         ('Assim que a cooperativa estiver registrada, ela abre uma campanha numa plataforma brasileira, como a Benfeitoria. Os apoiadores recebem as recompensas que a campanha oferece. O token da IMOBX é uma etapa separada, mais adiante.',
          'Once the cooperative is registered, it opens a campaign on a Brazilian platform such as Benfeitoria. Backers receive the rewards the campaign offers. The IMOBX token is a separate, later step.')),
        (('Financiamento ligado ao ODS 11', 'Funding for UN Goal 11'),
         ('Pedimos financiamento ligado ao ODS 11, o objetivo da ONU para cidades e comunidades sustentáveis, e é isso que um bairro cooperativo no Rio quer ser.',
          'We apply for funding linked to UN Goal 11, the UN’s goal for sustainable cities and communities, which is what a cooperative neighbourhood in Rio sets out to be.')),
        (('Outros financiadores', 'Other funders'),
         ('Também pedimos apoio a fundações que financiam o desenvolvimento sustentável, aos programas de desenvolvimento da cidade e a financiadores cripto.',
          'We also apply to foundations that fund sustainable development, to the city’s development programmes and to crypto funders.')),
    ]:
        roadmap += '<li>' + text(head, 'strong') + text(body, 'span') + '</li>'
    roadmap += '</ol>'
    roadmap += '<p>' + text(('Custos e recursos', 'Costs and funding'), 'a', 'href="transparency.html"') + '</p>'
    roadmap += '</section>'
    roadmap += '<section id="rafael-now">' + text(('No que o Rafael está trabalhando agora?', 'What is Rafael working on now?'), 'h2')
    roadmap += text(('O Rafael é engenheiro civil e tem a sua própria construtora no Rio. Estes são os passos em que ele está, na ordem em que um leva ao outro.',
                     'Rafael is a civil engineer with his own construction company in Rio. These are the steps he is on, in the order they lead into each other.'), 'p', 'class="answer"')
    roadmap += '<ol class="rafael-steps">'
    for head, body, leads in [
        (('O apartamento de Guadalupe.', 'The Guadalupe flat.'),
         ('A construtora do Rafael, a Olympus, construiu um prédio em Guadalupe, onde uma família aluga um apartamento e tem dificuldade para pagar. Estamos avaliando um contrato de aluguel com compra, com aluguel menor, e estamos avaliando se podemos oferecê-lo à família.', 'Rafael’s company, Olympus, built a building in Guadalupe where a family rents a flat and struggles to pay. We are considering a rent-to-own agreement with a lower rent, and whether to offer it to the family.'),
         ('um primeiro teste dos termos, antes de construir qualquer coisa nova.', 'a first test of the terms, before anything new is built.')),
        (('O custo atualizado de um apartamento.', 'The updated cost of one flat.'),
         ('O Rafael está confirmando qual padrão do índice público de custo da construção (CUB) vale para um prédio pequeno de cinco apartamentos.', 'Rafael is confirming which standard of the public building-cost index (CUB) fits a small building of five flats.'),
         ('a meta da campanha.', 'the campaign goal.')),
        (('Um terreno para cinco apartamentos.', 'A plot for five flats.'),
         ('Ele procura 200 a 300 m² em Anchieta, Pavuna, Bangu ou Santa Cruz, para construir cinco apartamentos de cada vez.', 'He is looking for 200 to 300 m² in Anchieta, Pavuna, Bangu or Santa Cruz, to build five flats at a time.'),
         ('o primeiro prédio novo, quando o financiamento estiver garantido.', 'the first new building, once the funding is in place.')),
        (('Os dois lofts que a construtora dele está construindo.', 'The two lofts his company is building.'),
         ('A obra segue enquanto o resto é preparado.', 'The work on site goes on while the rest is prepared.'),
         ('um exemplo real do tipo de construção que a IMOBX planeja.', 'a working example of the kind of building IMOBX plans.')),
    ]:
        roadmap += ('<li>' + text(head, 'strong') + ' ' + text(body, 'span') + ' <em>' + text(('Resultado:', 'Result:'), 'span') + ' ' + text(leads, 'span') + '</em></li>')
    roadmap += '</ol></section>'
    cases = guide['cases']
    # The answer first (no pilot is confirmed), then what a proposed and a confirmed pilot mean.
    intro_lines = tuple(t.rsplit('. ', 1) for t in cases['intro'])
    roadmap += '<section id="cases">' + text(('Onde a primeira família vai morar?', 'Where will the first family live?'), 'h2')
    roadmap += text(tuple(cases['answer']), 'p', 'class="answer"') + text(tuple(cases['intro'])) + text(tuple(cases['join']))  # owner audit 31 Oct: answer and detail written separately
    # Owner, 10 Nov: the property table reads as a notebook grid; the same four rows are now status cards.
    roadmap += '<ul class="property-cards">' + ''.join('<li class="property-card"><strong class="pc-name">' + text(r[0], 'span') + '</strong>'
                                              + '<span class="pc-row">' + text(cases['headings'][1], 'span', 'class="pc-label"') + text(r[1], 'span', 'class="pc-value"') + '</span>'
                                              + '<span class="pc-row">' + text(cases['headings'][2], 'span', 'class="pc-label"') + text(r[2], 'span', 'class="pc-value pc-status"') + '</span></li>'
                                              for r in cases['rows']) + '</ul>'
    # 'Who takes part' (the eight groups) moves to Take part (review B 80-108); its old anchors stay so links still land here.
    roadmap += '<span id="participation"></span>' + ''.join(f'<span id="role-{role["id"]}"></span>' for role in guide['participation']['roles'])
    roadmap += text(('Como funciona o aluguel com compra para uma família', 'How rent-to-own works for a family'), 'a', 'href="rent-to-own.html"') + '</section>'

    # Where it leads, and the builder's work (owner, 28-29 Oct): the biggest section sits at the bottom, clearly the builder's.
    roadmap += '<section id="village">' + text(('Como poderia ser a vila que imaginamos, mais adiante?', 'What could the village we imagine look like, later on?'), 'h2')
    roadmap += text(('Imaginamos uma vila com casas de 45 m² em volta de um pátio comum, com energia solar, um pomar e lugares para brincar e estudar. É uma etapa posterior: os primeiros passos são fases de cinco apartamentos.',
                     'We imagine a village of 45 m² houses around a shared courtyard, with solar power, an orchard and places to play and study. It is a later stage. The first steps are phases of five flats.'))
    roadmap += '<div class="lead-figures"><figure class="lead-figure"><img src="assets/homepage.jpg" width="1024" height="765" loading="lazy" alt="Ilustração conceitual da vila que imaginamos" data-alt-pt="Ilustração conceitual da vila que imaginamos" data-alt-en="Concept illustration of the village we imagine" data-alt-nl="Conceptillustratie van het dorp dat we ons voorstellen">'
    roadmap += '<figcaption>' + text(('Ilustração conceitual da vila que imaginamos, feita com um gerador de imagens.', 'Concept illustration of the village we imagine, made with an image generator.'), 'span') + '</figcaption></figure>'
    roadmap += '</div></section>'
    roadmap += '<section id="building">' + text(('O que a construtora do Rafael está construindo?', 'What is Rafael’s company building?'), 'h2')
    roadmap += text(('Em janeiro de 2026, a construtora do Rafael assinou um contrato para construir dois lofts. É uma obra própria da construtora, com projetos e agenda dela. Os lofts são o tipo de casa que a IMOBX quer construir, e as fotos abaixo mostram como a equipe do Rafael trabalha.',
                     'In January 2026, Rafael’s company signed a contract to build two lofts. It’s the company’s own job, and the company sets the plans and schedule. The lofts are the kind of house IMOBX plans to build, and the photos below show how Rafael’s team works.'), 'p', 'class="answer"')
    roadmap += '<div class="lead-figures"><figure class="lead-figure"><img src="assets/property-1.jpg" width="823" height="581" loading="lazy" alt="Os dois lofts, vista externa" data-alt-pt="Os dois lofts, vista externa" data-alt-en="The two lofts, exterior view" data-alt-nl="De twee lofts, buitenaanzicht">'
    roadmap += '<figcaption>' + text(('Modelo 3D dos dois lofts, da construtora do Rafael, janeiro de 2026.', 'A 3D model of the two lofts by Rafael’s company, January 2026.'), 'span') + '</figcaption></figure></div>'
    # Owner, 29 Oct: the photos that look like the loft model and show it being built; the frame first and largest.
    photos = [('construction-timber-supplied.jpg', ('Escoras de madeira seguram a laje entre os pilares de concreto.', 'Timber props hold up the slab between the concrete columns.')),
              ('construction-concrete-supplied.jpg', ('Brita e areia prontas ao lado de uma laje nova de concreto.', 'Gravel and sand ready next to a new concrete slab.')),
              ('construction-formwork-supplied.jpg', ('Malha de aço montada na laje antes da concretagem.', 'Steel mesh laid on the slab before the concrete is poured.')),
              ('construction-roof-supplied.jpg', ('Armação de ferro da fundação na vala, ao lado da laje pronta.', 'Foundation rebar in the trench, next to the finished slab.')),
              ('construction-solar-roof-supplied.jpg', ('A nova laje de cobertura ao lado de um telhado com painéis solares.', 'The new roof slab next to a tiled roof with solar panels.'))]
    from PIL import Image as _Img
    dims = {f: _Img.open(root / 'assets' / f).size for f, _ in photos}  # width and height stop the page jumping as photos load
    roadmap += '<ul class="photo-strip">' + ''.join(
        f'<li><figure><img src="assets/{f}" width="{dims[f][0]}" height="{dims[f][1]}" loading="lazy" alt="{esc(cap[0])}" data-alt-pt="{esc(cap[0])}" data-alt-en="{esc(cap[1])}" data-alt-nl="{esc(NL_LOOKUP.get(cap[1], cap[1]))}"><figcaption>' + text(cap, 'span') + '</figcaption></figure></li>'
        for f, cap in photos) + '</ul>'
    roadmap += '<p>' + text(('Fotos da obra, do arquivo da construtora do Rafael. ', 'Building-site photos from Rafael’s company. '), 'span')
    roadmap += text(('Todas as fotos e desenhos dos lofts', 'All photos and drawings of the lofts'), 'a', 'href="properties.html"') + '</p></section>'

    public = guide['transparency']
    Q = {item['id']: item for item in guide['questions']}
    ans = lambda ident, i, keep=None: Q[ident]['a'][i] if keep is None else pick(Q[ident]['a'][i], keep)
    spans = lambda *ids: ''.join(f'<span id="{i}"></span>' for i in ids)

    # The funding page is the home of funding: budgets, sources of funding and their order, who checks a payment and
    # what will be published. Copy sweep, 28 Oct (review B, owner 'proceed'): the status chips, the conversion steps,
    # the token paragraph and the legal-form essay moved to the roadmap, the Distributed ledger page and Terms
    # (decisions 13, 21); their old anchors stay so links still land here.
    def plain_source(key):
        """'Source: <label>.' when the page itself no longer needs to say what the source does not show."""
        return ('<p class="source-note">' + text(('Fonte: ', 'Source: '), 'span')
                + f'<a href="{esc(guide["sources"][key]["url"])}">{label_text(key)}</a>.</p>')

    fp = guide['funding_page']
    transparency = '<main class="paper guide-paper transparency-page band-page" id="main">' + language_controls
    transparency += text(public['title'], 'h1') + '<div class="key-card">' + text(fp['key']) + '</div>'
    transparency += text(fp['lead'], 'p', 'class="guide-lead"')
    transparency += on_this_page([(('Custos', 'Costs'), 'budgets'), (('De onde vêm os recursos', 'Where the funding comes from'), 'money-order'),
                                  (('Quem confere cada pagamento', 'Who checks each payment'), 'settlement'), (('O que vamos publicar', 'What we will publish'), 'reporting')])
    transparency += spans('status')

    # Menu anchors (first-homes, money-sources, payment-route, reports; funding and leaving on rent-to-own) sit on the
    # headings, since the sweep changed the English heading text that build_publication.add_menu_anchors matches.
    transparency += '<section id="budgets">' + spans('faq-cost-basis', 'custos') + guide['budgets_html']
    transparency += source_links('sinapi', 'cub', 'cost') + '</section>'

    order = guide['money_order']
    transparency += ('<section id="money-order">' + spans('funding', 'funding-sources', 'faq-funding', 'community-economy', 'household-payments', 'thanks-zeal-lets')
                     + text(fp['order_title'], 'h2', 'id="money-sources"') + text(fp['order_intro']) + cascade_html(text) + text(order['transfer']))
    # The kinds of funding are shown openly (owner, 26 Oct): their sources and permitted uses are the model.
    transparency += text(fp['kinds_summary'], 'h3') + '<div class="guide-table"><table><thead><tr>'
    transparency += ''.join(text(h, 'th', 'scope="col"') for h in order['headings']) + '</tr></thead><tbody>'
    transparency += ''.join('<tr>' + text(row[0], 'th', 'scope="row"') + text(row[1], 'td') + text(row[2], 'td') + '</tr>'
                            for row in order['kinds']) + '</tbody></table></div>' + plain_source('cash') + '</section>'

    # Funding economics moved here from why.html (review C, why 45-47).
    why_moved = guide['why']
    transparency += ('<section id="rent-to-own-or-rent">' + text(why_moved['fleet_title'], 'h2') + text(why_moved['fleet'])
                     + text(('As três fases de crescimento', 'The three phases of growth'), 'a', 'href="roadmap.html#stages"') + '</section>')

    transparency += ('<section id="settlement">' + spans('faq-on-off-ramp', 'rent-onramp', 'construction-offramp', 'digital-records', 'faq-arc-arctide',
                                                         'treasury-demonstration', 'ramp-options')
                     + text(fp['route_title'], 'h2', 'id="payment-route"') + route_html(text) + '</section>')

    transparency += ('<section id="reporting">' + spans('legal', 'faq-nonprofit', 'faq-ico', 'ico-comparison') + text(public['reporting_title'], 'h2', 'id="reports"')
                     + '<ul>' + ''.join(text(public['reporting'][i], 'li') for i in (0, 1, 2, 3)) + '</ul>' + text(public['reporting_note']) + '</section>')
    transparency += '<section class="closing-band" id="elsewhere">' + spans('sources', 'updates', 'next-steps')
    transparency += spans('token-options', 'faq-yield', 'funding-questions', 'faq-thanks-zeal-lets', 'faq-euler', 'faq-exchanges',
                          'faq-property', 'faq-rwa', 'outreach', 'campaign-work')

    # Old anchors whose answers now live elsewhere, one link to where decisions are described, then the one orange action.
    transparency += '<p>' + spans('faq-governance', 'faq-merit', 'faq-dao', 'faq-flock-siah', 'faq-scale', 'community-rights', 'community-tools')
    transparency += text(('Quem decide o quê', 'Who decides what'), 'a', 'href="governance.html"') + '</p>'
    transparency += text(('Conversar sobre financiamento', 'Talk to us about funding'), 'a', 'class="button act" href="contact.html?role=funding"') + '</section>'
    transparency += partner_line('transparency.html') + '</main>'
    (root / 'transparency.html').write_text(page('IMOBX | Funding and spending', transparency,
        f'<link rel="stylesheet" href="{asset_v("flow.css")}"><link rel="stylesheet" href="{asset_v("bands.css")}">' + FUNDING_SCRIPT, version=guide['version'], lang='pt-BR', title_pt='IMOBX | Financiamento e gastos'))

    # Who decides, and what we are deciding now, moved to their own page (owner, 28 Oct: Local governance).
    # The old addresses stay here, so earlier links still land on the pointer.
    roadmap += ('<section id="governance"><span id="open-terms"></span><span id="who-decides"></span><span id="deciding"></span><p>'
                + text(('Quem decide em cada etapa, e o que estamos decidindo agora: ', 'Who decides at each stage, and what we are deciding now: '), 'span')
                + text(('Governança local', 'Local governance'), 'a', 'href="governance.html"') + '.</p></section>')
    # Terms (decision 21; owner 'proceed', 28 Oct): status and conditions said once, here, from TERMS_PAGE_DRAFT_2026-10-28.md.
    # It sits before the closing band, so the page still ends on the one invitation.
    roadmap += '<section id="terms">' + text(TERMS_TITLE, 'h2')
    roadmap += text(('Se você pensa em participar, apoiar com recursos ou trazer um imóvel, é com isto que você pode contar hoje.',
                     'If you’re thinking of joining, funding or bringing a property, this is what you can count on today.'))
    for _i, (heading, items) in enumerate(TERMS):  # owner, 28 Oct: the long list sits in folds so the page ends lighter; 10 Nov: the first fold opens
        roadmap += '<details class="disclosure"' + (' open' if _i == 0 else '') + '><summary>' + text(heading, 'span') + '</summary><div class="disclosure-body"><ul>'
        for item in items:
            if len(item) == 3:  # (lead-in, link label, anchor)
                roadmap += '<li>' + text(item[0], 'span') + text(item[1], 'a', f'href="{item[2]}"') + '.</li>'
            else:
                roadmap += text(item, 'li')
        roadmap += '</ul></div></details>'
    roadmap += '</section>'
    roadmap += '<section class="closing-band" id="help">' + text(('Vamos resolver as perguntas em aberto, como o terreno dos apartamentos novos e o preço para as famílias, com as pessoas que participarem. Se você pode ajudar com uma delas, apresente-se.',
                                                                   'We’ll settle the open questions, such as the plot for the new flats and the price for families, with the people who join us. If you can help with one of them, introduce yourself.'))
    roadmap += text(('Apresente-se', 'Introduce yourself'), 'a', 'class="button act" href="contact.html"') + '</section>'
    # Owner, 10 Nov: the page must read as one story. Path first, then what we build, who builds, how it is funded, what is decided.
    _ns = roadmap.index('<div class="key-card">')
    _m = re.search(r'<p [^>]*id="where-we-stand"', roadmap)
    roadmap = roadmap[:_ns] + roadmap[_m.start():]  # the need paragraph and the favela photos are dropped; the lead carries one line of why
    _n1 = roadmap.index('<nav class="on-this-page"'); _n2 = roadmap.index('</nav>', _n1) + len('</nav>')
    roadmap = roadmap[:_n1] + roadmap[_n2:]
    _ORDER = ['stages', 'cases', 'village', 'building', 'rafael-now', 'funding', 'governance', 'terms']
    _spans = {}
    for _id in _ORDER:
        _mm = re.search(r'<section id="%s">.*?</section>' % _id, roadmap, re.S)
        _spans[_id] = _mm
    _first = min(m.start() for m in _spans.values())
    _html = {i: m.group(0) for i, m in _spans.items()}
    for _id in sorted(_spans, key=lambda i: -_spans[i].start()):
        roadmap = roadmap[:_spans[_id].start()] + roadmap[_spans[_id].end():]
    roadmap = roadmap[:_first] + ''.join(_html[i] for i in _ORDER) + roadmap[_first:]
    roadmap += partner_line('roadmap.html') + '</main>'
    (root / 'roadmap.html').write_text(page('IMOBX | Project stages', roadmap,
        f'<link rel="stylesheet" href="{asset_v("bands.css")}"><link rel="stylesheet" href="{asset_v("roadmap.css")}"><script src="{asset_v("roadmap.js")}" defer></script>',
        version=guide['version'], lang='pt-BR', title_pt='IMOBX | Etapas do projeto'))

    # Local governance (owner, 28 Oct): one page for who decides, ordered from now to later. Today the team decides;
    # the token's holders decide its rules once it launches; the cooperative's members and residents decide later.
    # Research: CODEX_GOVERNANCE_IA_2026-10-28.md and research/GOVERNANCE_VERTICAL_SCOUT_2026-10-28.md.
    headings = [('Decisão', 'Decision'), ('Quem decide', 'Who decides'), ('Limites e conferências', 'Limits and checks')]
    def gtable(rows):
        out = '<div class="guide-table"><table><thead><tr>' + ''.join(text(h, 'th', 'scope="col"') for h in headings) + '</tr></thead><tbody>'
        return out + ''.join('<tr>' + ''.join(text(cell, 'td') for cell in row) + '</tr>' for row in rows) + '</tbody></table></div>'
    team_rows = [
        [('Projeto, orçamento e obra', 'Design, budgets and building work'),
         ('Rafael Britto, um dos nossos cofundadores. A construtora dele é a construtora proposta.', 'Rafael Britto, one of our co-founders. His construction company is the proposed builder.'),
         ('No plano, as cobranças da empresa dele são aprovadas por outra pessoa, uma segunda pessoa confere o serviço, e só então a cobrança é paga.', 'In the plan, someone other than Rafael approves his company’s invoices, a second person checks the work, and only then is the invoice paid.')],
        [('Comunicação, ferramentas digitais e o grupo', 'Communication, digital tools and the group'),
         ('John, um dos nossos cofundadores.', 'John, one of our co-founders.'),
         ('Ele publica cada mudança no plano aqui e no grupo.', 'He publishes every change to the plan here and in the group.')],
        [('Divulgação, embaixadores e corretores', 'Promotion, ambassadors and brokers'),
         ('Os cofundadores.', 'The co-founders.'),
         ('O trabalho de divulgação é conferido, e o plano é publicar os pagamentos. As condições de pagamento são combinadas antes.', 'Promotional work is checked, and the plan is to publish payments. Payment terms are agreed in advance.')],
        [('Captação de recursos', 'Fundraising'),
         ('A pessoa de captação organiza o próprio trabalho dentro das tarefas e metas combinadas com John. Os cofundadores decidem juntos sobre compromissos de financiamento.', 'The fundraiser organises their own work around the tasks and targets agreed with John. The co-founders decide together on funding commitments.'),
         ('Prepara planos e pedidos de financiamento. Não pode assinar, gastar nem prometer recursos pela IMOBX.', 'Prepares funding plans and applications. Cannot sign, spend or promise funding for IMOBX.')],
        [('O que a campanha promete aos apoiadores', 'What the campaign promises backers'),
         ('Os cofundadores.', 'The co-founders.'),
         ('Recompensas comuns de campanha, nunca tokens.', 'Ordinary campaign rewards, never tokens.')],
        [('Guarda e liberação dos recursos', 'Holding and releasing the funding'),
         ('Os cofundadores, a partir da conta bancária da própria cooperativa.', 'The co-founders, from the cooperative’s own bank account.'),
         ('Nunca uma conta pessoal. Cada pagamento tem duas pessoas: uma aprova, outra confere.', 'Never a personal account. Every payment has two people: one approves, another checks.')],
        [('Quem confere os contratos, os pagamentos e a obra', 'Who checks the agreements, payments and building work'),
         ('O John nomeia um advogado independente, um contador e um engenheiro independente, com o acordo dos dois cofundadores.', 'John appoints an independent lawyer, an accountant and an independent engineer, with both co-founders agreeing.'),
         ('Nenhum deles trabalha para a construtora do Rafael, e o Rafael não escolhe o engenheiro que confere a obra da própria construtora.', 'None of them works for Rafael’s company, and Rafael does not choose the engineer who checks his own company’s building work.')],
        [('Registro da cooperativa, contratos e o plano geral', 'Registering the cooperative, contracts and the overall plan'),
         ('Os cofundadores.', 'The co-founders.'),
         ('Cada passo do registro é publicado aqui e no grupo.', 'Each step of the registration is published here and in the group.')],
    ]
    resident_rows = [
        [('Morar na casa e comprá-la', 'Living in the house and buying it'),
         ('A família e a IMOBX juntas.', 'The family and IMOBX together.'),
         ('Só dentro dos termos que a família assinou e da lei brasileira.', 'Only within the terms the family signed and Brazilian law.')],
        [('Uso de espaços e manutenção local', 'Shared spaces and local maintenance'),
         ('Os moradores juntos, um voto por membro.', 'The residents together, one vote per member.'),
         ('Dentro do orçamento e das regras de segurança. Os moradores podem trocar as pessoas que escolheram para representá-los.', 'Within the budget and the safety rules. Residents can replace the people they chose to represent them.')],
        [('Obras e compras', 'Building work and purchases'),
         ('Pessoas escolhidas pela experiência, para uma função e um prazo definidos.', 'People chosen for their experience, for a set job and a set time.'),
         ('Duas pessoas por pagamento: uma aprova, outra confere o serviço.', 'Two people per payment: one approves, another checks the work.')],
    ]
    open_terms = [  # owner, 31 Oct: plain questions, not a form of empty boxes
        ('Em que terreno serão construídos os cinco apartamentos novos?', 'Which plot will the five new flats be built on?'),
        ('Qual será o preço e o pagamento mensal, e quanto de cada pagamento conta para a compra?', 'What will the price and the monthly payment be, and how much of each payment goes towards buying the house?'),
        ('Quem paga os reparos, em quanto tempo são feitos e como contestar uma cobrança?', 'Who pays for repairs, how fast are they done, and how can a charge be questioned?'),
        ('Como os moradores vão votar, quanto se pode gastar sem consultar e como resolver uma discordância?', 'How will residents vote, how much can be spent without asking, and how are disagreements settled?'),
        ('Como a cooperativa vai ser registrada, e com quais estatutos?', 'How will the cooperative be registered, and under which statute?'),
        ('Quais recompensas a campanha vai oferecer?', 'Which rewards will the campaign offer?'),
        ('Qual empresa vai cuidar dos pagamentos?', 'Which company will handle payments?'),
        ('Quanto passa pela blockchain: nada, alguns pagamentos ou cada pagamento e aprovação?', 'How much runs on the blockchain: none of it, some payments, or every payment and approval?'),
    ]
    groups = [(('A casa, o preço e as regras', 'The house, the price and the rules'), open_terms[0:4]), (('Recursos e registro da cooperativa', 'Funding and registering the cooperative'), open_terms[4:8])]
    gov = '<main class="paper guide-paper band-page governance-page" id="main">' + language_controls
    gov += text(('Quem decide, e quando você tem voz?', 'Who decides, and when do you get a say?'), 'h1')
    gov += text(('A IMOBX está em preparação, então hoje os nossos dois cofundadores tomam as decisões. À medida que o projeto cresce, o plano tem quatro etapas, e cada uma traz mais pessoas:',
                 'IMOBX is in preparation, so today our two co-founders make the decisions. As the project grows, the plan has four stages, and each one brings in more people:'), 'p', 'class="guide-lead"')
    gov += gov_flow_html(text)  # owner, 29 Oct ('go'): the stages as one drawing; owner: every heading gets a line or two
    gov += on_this_page([(('Quem decide agora', 'Who decides now'), 'now'), (('Por que uma cooperativa', 'Why a cooperative'), 'cooperative'), (('O que estamos decidindo agora', 'What we’re deciding now'), 'deciding'),
                         (('Quem decide sobre o token', 'Who decides about the token'), 'token-rules'),
                         (('Quem decide quando as famílias morarem nas casas', 'Who decides once families live in the houses'), 'residents'), (('Como as decisões ficam registradas', 'How decisions are recorded'), 'recorded')])
    gov += '<section id="now">' + text(('Quem decide agora?', 'Who decides now?'), 'h2')
    gov += text(('Por enquanto, o Rafael decide sobre a obra, o John sobre a comunicação, e os dois decidem juntos o resto. Quando um trabalho precisa de outra pessoa, eles a chamam para esse trabalho, com prazo e orçamento.',
                 'For now, Rafael decides on the building, John on communication, and the two decide the rest together. When a job needs someone else, they bring that person in for that job, with a deadline and a budget.'), 'p', 'class="answer"')
    gov += gtable(team_rows) + '</section>'
    # Owner, 8 Nov ("publish" on the why-placement advice): the cooperative's why gets its one home here, after who decides now.
    gov += '<section id="cooperative">' + text(('Por que uma cooperativa?', 'Why a cooperative?'), 'h2')
    gov += text(('Famílias, proprietários e financiadores precisam confiar numa organização maior que os seus dois cofundadores. Numa cooperativa, cada membro tem voz.',
                 'Families, property owners and funders need to trust an organisation that is bigger than its two co-founders. In a cooperative, each member has a say.'), 'p', 'class="answer"')
    gov += text(('Por isso, planejamos fundar a IMOBX como uma cooperativa habitacional: uma organização que os seus membros possuem e administram juntos, um membro, um voto, em benefício dos membros e sem objetivo de lucro.',
                 'So we plan to found IMOBX as a housing cooperative: an organisation its members own and run together, one member, one vote, for the members’ benefit and not for profit.'))
    gov += '</section>'
    # Owner, 31 Oct: 'Who decides now?' and 'What are we deciding now?' belong together; they were apart by accident.
    gov += '<section id="deciding">' + text(('O que estamos decidindo agora?', 'What are we deciding now?'), 'h2')
    gov += '<div class="settle-groups">' + ''.join('<div>' + text(label, 'h3') + '<ul class="settle-list">' + ''.join(text(item, 'li') for item in items) + '</ul></div>'
                                                  for label, items in groups) + '</div>' + text(('As famílias e os financiadores assinam os seus contratos depois que a cooperativa estiver registrada.', 'Families and funders sign their agreements once the cooperative is registered.')) + '</section>'
    gov += '<section id="token-rules"><span id="safeguards"></span>' + text(('Quem decide sobre o token?', 'Who decides about the token?'), 'h2')
    gov += text(('Quando o token for lançado, quem o tem vota as regras dele. Quem ajudou o projeto também vota, depois que outras pessoas confirmam essa ajuda.',
                 'Once the token launches, its holders vote on its rules. People who have helped the project vote too, once others confirm their help.'), 'p', 'class="answer"')
    gov += text(('Uma votação do token pode mudar o contrato de uma família? Nenhuma votação pode mudar o contrato de moradia de uma família: ele só muda quando a família e a IMOBX concordam, dentro da lei brasileira.',
                 'Could a token vote change a family’s agreement? No vote can change a family’s housing agreement: it changes only when the family and IMOBX both agree, under Brazilian law.'))
    gov += '<p>' + text(('Como o token funciona', 'How the token works'), 'a', 'href="blockchain.html#token"') + '</p></section>'
    gov += '<section id="residents">' + text(('Quem decide quando as famílias morarem nas casas?', 'Who decides once families live in the houses?'), 'h2')
    gov += text(('Quando as primeiras casas existirem e a cooperativa estiver registrada, o plano é que os membros tomem as grandes decisões juntos e que os moradores cuidem dos espaços comuns. Os primeiros moradores vão ajudar a escrever essas regras.',
                 'Once the first houses exist and the cooperative is registered, the plan is for members to make the big decisions together and for residents to run their shared spaces. The first residents will help write those rules.'), 'p', 'class="answer"')
    gov += gtable(resident_rows)  # owner, 31 Oct: the section's answer stays open, not folded
    why_org = guide['why']
    gov += text(why_org['org_title'], 'h3')  # owner, 31 Oct audit: the 'this is how' intro was meta
    gov += '<ol class="layer-list org-list">' + ''.join('<li>' + pic + '<h3>' + text(t_, 'span') + '</h3>' + text(b_) + '</li>'
                                                      for pic, (t_, b_) in zip(ORG_PICS, why_org['org_cols'])) + '</ol>'
    gov += '</section>'
    gov += '<section id="recorded">' + text(('Como as decisões ficam registradas?', 'How are decisions recorded?'), 'h2')
    gov += text(('No plano, cada decisão fica registrada na ata da reunião em que foi tomada. Quando a cooperativa estiver registrada, o estatuto vai dizer como se decide. Cada pagamento, e os nomes de quem o aprovou, podem ir para uma blockchain pública, onde qualquer pessoa pode conferir. Quanto vai para lá ainda está sendo decidido: de nada até todos os pagamentos.',
                 'In the plan, every decision is written down in the minutes of the meeting where it was made. Once the cooperative is registered, its statute, the founding rulebook, will set out how decisions are made. Each payment, and the names of the people who approved it, can go on a public blockchain where anyone can check them. How much goes there is still being decided, from none of it to every payment.'))
    gov += '<p>' + text(('Veja as opções para registrar os pagamentos', 'See the options for recording payments'), 'a', 'href="blockchain.html"') + '</p></section>'
    gov += '<section class="closing-band" id="help">' + text(('Quer ajudar a desenhar como se decide? Apresente-se no grupo.', 'Want to help shape how decisions are made? Introduce yourself in the group.'))
    gov += text(('Apresente-se', 'Introduce yourself'), 'a', 'class="button act" href="contact.html"') + '</section>'
    gov += partner_line('governance.html') + '</main>'
    (root / 'governance.html').write_text(page('IMOBX | Local governance', gov,
        f'<link rel="stylesheet" href="{asset_v("flow.css")}"><link rel="stylesheet" href="{asset_v("bands.css")}">' + MF_SCRIPT, version=guide['version'], lang='pt-BR', title_pt='IMOBX | Governança local'))

    # The ideas behind IMOBX (decisions 15-16). Owner, 29 Oct: no quotation blocks or dates ("unorthodox, they do not
    # build familiarity"); his arguments in plain prose, in the "we" voice. Sources: SOURCE_WORDS WHY-04/09/10/11/12/15,
    # WHA-08, chat #228 and #988 (kept private). The section now lives on the Resources page (owner, 29 Oct: one page).
    def idea(title, body, source=None):
        out = '<article class="idea">' + text(title, 'h3') + ''.join(text(p) for p in body)
        if source:
            out += '<p class="idea-source">' + text(source[0], 'a', f'href="{esc(source[1])}" rel="noopener"') + '</p>'
        return out + '</article>'

    def linked(*parts):
        # Names in the story link to their source in the sentence itself: each part is (pt, en) or (pt, en, url).
        out = '<p>'
        for part in parts:
            out += text(part[:2], 'a', f'href="{esc(part[2])}" rel="noopener"') if len(part) == 3 else text(part, 'span')
        return out + '</p>'

    checkable = [(('O contrato que a construtora do Rafael assinou em janeiro de 2026 para construir dois lofts, com os desenhos', 'The contract Rafael’s company signed in January 2026 to build two lofts, with their drawings'), 'properties.html'),
                 (('Um apartamento candidato para o nosso primeiro morador em aluguel com compra', 'A candidate flat for our first rent-to-own tenant'), 'roadmap.html#cases'),
                 (('Custos de obra comparados às tabelas públicas do Brasil', 'Building costs set against Brazil’s public cost tables'), 'transparency.html#first-homes'),
                 (('Pagamentos e aprovações previstos num registro público', 'Payments and approvals planned on a public ledger'), 'blockchain.html')]
    drives = [('Construímos comunidades, não só unidades: lugares onde as pessoas voltam a se encontrar.', 'We build communities, not only units: places where people connect again.'),
              ('O nosso lucro real é social. A nossa riqueza é um mundo onde as pessoas são livres.', 'Our real profit is social. Our wealth is a world where people are free.'),
              ('Quem aluga se torna dono, e um bairro sem estresse vale mais do que ficar milionário.', 'Renters become owners, and a stress-free neighbourhood is worth more than becoming a millionaire.')]
    ideas = '<section id="ideas">' + text(('Por que a IMOBX', 'Why IMOBX'), 'h2', 'id="why"')
    ideas += text(('Para criar bairros onde as pessoas voltam a se conectar, e onde quem aluga pode se tornar dono.',
                   'To create neighbourhoods where people connect again, and where renters can become owners.'), 'p', 'class="answer"')
    ideas += ('<figure class="iceberg"><div class="iceberg-above">' + text(('O que você pode conferir', 'What you can check'), 'p', 'class="iceberg-label"')
              + '<ul>' + ''.join('<li>' + text(label, 'a', f'href="{href}"') + '</li>' for label, href in checkable) + '</ul></div>'
              + '<svg class="iceberg-water" viewBox="0 0 1000 40" preserveAspectRatio="none" aria-hidden="true"><path pathLength="1" d="M0,20 C80,4 160,36 250,20 S420,4 500,20 S670,36 750,20 S920,4 1000,20"/></svg>'
              + '<div class="iceberg-below">' + text(('O que nos move', 'What drives us'), 'p', 'class="iceberg-label"')
              + '<ul class="iceberg-reasons">' + ''.join(text(d, 'li') for d in drives) + '</ul>'
              + '<p class="iceberg-onward">' + text(('Conheça os fundadores', 'Meet the founders'), 'a', 'href="#our-story"') + '</p></div>'
              + '</figure></section>')  # caption removed (owner, 29 Oct: it only described the drawing)
    ideas += '<section id="our-story">' + '<svg class="iceberg-water story-water" viewBox="0 0 1000 40" preserveAspectRatio="none" aria-hidden="true"><path pathLength="1" d="M0,20 C80,4 160,36 250,20 S420,4 500,20 S670,36 750,20 S920,4 1000,20"/></svg>' + text(('Os fundadores', 'The founders'), 'h2')
    # The iceberg's waterline introduces the founders; their own accounts follow without an editorial preamble.
    ideas += text(('Rafael Britto, cofundador e engenheiro civil', 'Rafael Britto, co-founder and civil engineer'), 'h3')
    # Owner, 8 Nov: Rafael's bio follows his own story (Q1, 6 Nov): master's paused after the first year, no sales career.
    # Left out until he agrees: his worries, Dr. Cavalieri's name and the army unit.
    ideas += text(('Minha infância me ensinou cedo o valor de cada centavo e de um teto seguro. Meu pai foi ausente, e minha mãe sustentava a casa trabalhando de 70 a 80 horas por semana para criar três filhos. Aos 7 anos, eu já ia sozinho ao mercado fazer pequenas compras, e tive que aprender números decimais antes da hora só para conferir o troco. Aos 10, fazia bicos para os vizinhos: ia ao mercado, levava as compras até a porta, ganhava um ou dois reais e guardava. Eu sempre guardei.',
                   'My childhood taught me early the value of every cent and of a safe roof. My father was absent, and my mother supported the household working 70 to 80 hours a week to raise three children. At 7, I was already going to the market on my own to do small shopping, and I had to learn decimals ahead of time just to check the change. At 10, I did odd jobs for the neighbours: I’d go to the market, carry their groceries to their door, earn a real or two, and save it. I always saved.'))
    ideas += text(('Aos 14, entrei no CAMP (Círculo dos Amigos do Menino Patrulheiro), um programa que prepara jovens de famílias pobres para o trabalho, e consegui o meu primeiro emprego, como aprendiz de produção numa fábrica de dobradiças, onde fiquei até os 19. Sem perceber, aquele foi o meu primeiro contato com a construção civil. Nesse período, também servi nas Forças Armadas como soldado. Quando terminei o serviço militar, decidi que não ia continuar como auxiliar de produção: eu queria crescer.',
                   'At 14, I joined CAMP (Círculo dos Amigos do Menino Patrulheiro), a programme that prepares young people from poor families for work, and I got my first job as a production trainee at a hinge factory, where I stayed until I was 19. Without realising it, that was my first contact with civil construction. During that period, I also served in the Armed Forces as a soldier. When I finished military service, I decided I would not stay a production assistant: I wanted to grow.'))
    ideas += text(('Comecei Matemática na Universidade Gama Filho e estudei até o 6º período, mas não me via como professor, e também não podia pagar as mensalidades. Prestei vestibular para uma universidade pública e, vindo de escolas públicas, passei para Engenharia Civil, graças ao meu amor pelos livros, que me deu o que a sala de aula não deu. Tornei-me engenheiro civil. Entrei no mestrado em Estruturas da Faculdade de Engenharia da UERJ e concluí o primeiro ano, mas tive que interrompê-lo por dificuldades financeiras.',
                   'I began Mathematics at Universidade Gama Filho and studied through the 6th semester, but I didn’t see myself as a teacher, and I also couldn’t afford the fees. I applied to a public university and, coming from public schools, I passed the entrance exam for Civil Engineering, thanks to my love of books, which gave me what the classroom did not. I became a civil engineer. I was admitted to the master’s in Structures at UERJ’s Faculty of Engineering and completed the first year, then had to pause it due to financial difficulties.'))
    ideas += text(('Desde o início da graduação, em 2013, estudo o mercado imobiliário. Fundei a Construtora Olympus olhando para um problema que conheço de perto: o Brasil valoriza os muito qualificados e precisa da mão de obra braçal, mas deixa de lado quem está no meio.',
                   'Since the start of my degree, in 2013, I have studied the real-estate market. I founded Construtora Olympus looking at a problem I know firsthand: Brazil values the highly qualified and needs manual labour, but leaves aside those in the middle.'))
    ideas += text(('Nunca desisti de um sonho que carrego desde a faculdade: construir boas moradias, de padrão modesto ou acessível, para que as famílias mais pobres possam de novo realizar o sonho da casa própria. A pergunta que não sai da minha cabeça é simples: por que ter a própria caverna não é um direito de todos? A IMOBX é a minha resposta a essa pergunta.',
                   'I never gave up a dream I have carried since university: to build good homes, of modest or affordable standard, so that the poorest families can once again fulfil the dream of owning their own home. The question that won’t leave my mind is simple: why isn’t having one’s own cave a right for everyone? IMOBX is my answer to that question.'))
    ideas += text(('John, cofundador', 'John, co-founder'), 'h3')
    ideas += text(('Hoje, trabalho com Rafael Britto, que traz experiência em construção no Rio. Compartilhamos uma pergunta: como uma família pode chegar à casa própria enquanto os vizinhos cuidam dos espaços que dividem?',
                   'Today, I work with Rafael Britto, who brings construction experience in Rio. We share a question: how can a family find a path to owning a home while neighbours care for the places they share?'))
    ideas += '<span id="shaped"></span>'
    ideas += text(('Cresci numa cidade que parecia uma corrida, como o mais velho de três filhos. A guerra não estava longe da nossa família, e essas cicatrizes me levaram para outra direção: eu não conseguia mais fazer de outro jeito. Saí do ensino tradicional para viajar e descobrir outras formas de viver. Alguns anos depois de eu sair de casa, o casamento dos meus pais acabou. Foi a primeira vez que senti que tinha perdido o meu lar. Ainda sinto falta dessa sensação de estar em casa. É uma busca que continua.',
                   'I grew up in a city that felt like a race, as the oldest of three. The war was not far away in our family, and those scars pushed me in another direction: I could not do otherwise any longer. I left traditional schooling to travel and discover other ways to live. A few years after I left the house, my parents’ marriage collapsed. That was the first time I felt I had lost my home. I still long for that sense of being home. It is an ongoing quest.'))
    ideas += linked(('Desde 2005, procuro formas para que as comunidades compartilhem o que pertence a todos. Visitei ', 'Since 2005, I have looked for ways for communities to share what they hold in common. I visited '),
                    ('Tamera', 'Tamera', 'https://www.tamera.org/about/'),
                    (', passei seis anos em ecovilas pela Europa e, em 2010, cofundei uma organização de inovação social em Antuérpia. Em 2016, desenvolvi uma cozinha cooperativa, a Cuisine Divers, e recusei um investidor-anjo, porque não queria depender de um único investidor, um ponto único de falha. Em 2020, cofundei a ', ', spent six years in eco-villages across Europe and, in 2010, co-founded a social innovation organisation in Antwerp. In 2016, I developed a cooperative kitchen, Cuisine Divers, and turned down a business angel, because I did not want to depend on one investor, a single point of failure. In 2020, I co-founded '),
                    ('DeFiants', 'DeFiants', 'https://be.linkedin.com/company/defiants'),
                    (', uma agência Web3 que trabalhou em mais de 15 projetos com uma equipe de 20 pessoas. Saí em 2023.', ', a Web3 agency that worked on more than 15 projects with a team of 20 people. I left in 2023.'))
    ideas += text(('Em 2025, esses caminhos se juntaram. Estou construindo o SIAH Protocol para guardar um registro de contribuições que outras pessoas confirmam, e a proposta da IMOBX leva essa ideia de compartilhar à moradia.',
                   'In 2025, these threads came together. I’m building SIAH Protocol to keep a record of contributions confirmed by other people, and the IMOBX proposal brings that idea of sharing to housing.'))
    ideas += '<details class="disclosure story-full"><summary>' + text(('Leia a história completa do John', 'Read John’s full story'), 'span') + '</summary><div class="disclosure-body">'
    ideas += text(('Cresci numa cidade que parecia uma corrida, como o mais velho de três filhos, com um irmão e uma irmã. As pessoas competiam desde cedo, com pouco tempo para perguntar para onde estávamos indo. A guerra não estava longe da nossa família. Meu avô por parte de mãe ficou preso em campos de guerra alemães durante a Segunda Guerra Mundial, e minha mãe ficou traumatizada pelos crimes de guerra cometidos contra ele. Do lado do meu pai, a irmã do meu avô tinha quatro anos quando caiu uma bomba V2. Ela ficou soterrada sob os escombros de um muro de tijolos. Correram com ela para o hospital, mas ela perdeu sangue demais e morreu no caminho.',
                   'I grew up in a city that felt like a race, as the oldest of three, with a brother and a sister. People competed from an early age, with little time to ask where we were going. The war was not far away in our family. My grandfather on my mother’s side was imprisoned in German war camps during the Second World War, and my mother was traumatised by the war crimes committed against him. On my father’s side, my grandfather’s sister was four when a V2 bomb struck. She was crushed under the rubble of a brick wall. They ran with her to the hospital, but she lost too much blood and died on the way.'))
    ideas += text(('Essas cicatrizes me levaram para outra direção, porque eu não conseguia mais fazer de outro jeito. O sistema não comportava as perguntas para as quais eu buscava respostas. O trabalho de caridade me inspirou, porque me parecia a única coisa sensata a fazer. O dinheiro não tinha sentido para mim, porque não compra felicidade, amor nem uma base sólida. Então, ainda jovem, saí do ensino tradicional e deixei para trás aquele navio que afundava, para viajar e descobrir outras formas de viver. Alguns anos depois de eu sair de casa, o casamento dos meus pais acabou. Foi a primeira vez que senti que tinha perdido o meu lar. Ainda sinto falta dessa sensação de estar em casa. É uma busca que continua.',
                   'Those scars pushed me in another direction, because I could not do otherwise any longer. The system could not accommodate the questions I was seeking answers to. Charity work inspired me, because it seemed the only common-sense thing to do. Money was meaningless to me, because it cannot buy happiness, love or a strong foundation. So as a young man, I stepped away from traditional schooling and left that sinking ship behind, to travel and discover other ways to live. A few years after I left the house, my parents’ marriage collapsed. That was the first time I felt I had lost my home. I still long for that sense of being home. It is an ongoing quest.'))
    # Founder story: wake-up, lived experience, practical attempts at cooperation, then the conclusion.
    ideas += text(('Quando comecei a viajar, em 2005, o Facebook ainda não tinha aberto as inscrições ao público em geral. Isso aconteceu um ano depois. Na Serra da Estrela, em Portugal, vivi por um tempo sem precisar de dinheiro. Ofereci o meu trabalho e ajudei num sítio nas montanhas. Durante o dia, podava as videiras. À noite, lia à luz de velas. A vida era simples.',
                   'When I started travelling in 2005, Facebook had not yet opened registration to the general public. That happened a year later. In Serra da Estrela, Portugal, I lived for a while without needing money. I offered my hands and helped on a farm in the mountains. I pruned vines during the day and read by candlelight in the evening. Life was simple.'))
    ideas += text(('Eu descrevia aquele contraste assim: “Sociedade domesticada, nossa realidade antinatural. Nossa sociedade antinatural, realidade domesticada.” Naquela simplicidade, comecei a perceber como a pressão social mantém as pessoas encurraladas, com as costas contra a parede. Para mim, essa pressão também é uma armadilha mental. Senti que muitas famílias, como a minha, ainda carregavam feridas das duas guerras mundiais e que raramente reconhecíamos como elas continuam moldando a vida em sociedade.',
                   'I described that contrast this way: “Domesticated society, our unnatural reality. Our unnatural society, domesticated reality.” In that simplicity, I began to see how social pressure keeps people backed against the wall. To me, that pressure is also a mind trap. I felt that many families, like mine, were still carrying wounds from the two world wars, and rarely recognised how they continue to shape life in society.'))
    ideas += linked(('A ajuda mútua foi o que mais me inspirou, como Piotr Kropotkin a descreve no livro ', 'Mutual aid inspired me most, as Peter Kropotkin describes it in his book '),
                    ('Ajuda Mútua: um fator de evolução', 'Mutual Aid: A Factor of Evolution', 'https://www.gutenberg.org/ebooks/4341'),
                    ('. O livro me mostrou como a cooperação é essencial para a nossa capacidade de resistir e seguir em frente. Em 2005, aos 19 anos, visitei ', '. The book showed me how essential cooperation is to our resilience. In 2005, aged 19, I visited '),
                    ('Tamera', 'Tamera', 'https://www.tamera.org/about/'),
                    (', uma comunidade intencional em Portugal. Depois passei seis anos em ecovilas pela Europa e conheci o cohousing na Bélgica. Vi pessoas tentando construir comunidades e locais de trabalho mais acolhedores, e sistemas econômicos que permitissem mais cooperação.', ', an intentional community in Portugal. I went on to spend six years in eco-villages across Europe and got to know co-housing in Belgium. I saw people trying to build warmer communities and workplaces, and economic systems that made more cooperation possible.'))
    ideas += text(('Em 2010, cofundei uma organização de inovação social em Antuérpia. Trabalhávamos com conscientização e meio ambiente. Em 2012, criamos uma horta no telhado. Com pessoas dos maker labs e fab labs, explorei como produzir alimentos localmente, com pouca manutenção. A ideia esbarrava em problemas práticos: logística e capital inicial. Aprendi que boas intenções precisam de formas de organização que funcionem no dia a dia.',
                   'In 2010, I co-founded a social innovation organisation in Antwerp. We worked on public awareness and the environment. In 2012, we built a rooftop garden. With people from maker and fab labs, I explored ways to grow food locally with little upkeep. The idea ran into practical barriers: logistics and starting capital. I learned that good intentions need ways of organising that work day to day.'))
    ideas += text(('Também aprendi a tomar decisões em conjunto. Em organizações de base, conheci a comunicação não violenta, o design centrado nas pessoas e a tomada de decisão por consenso.',
                   'I also learned to make decisions together. In grassroots organisations, I encountered nonviolent communication, human-centred design and consensus decision-making.'))
    ideas += text(('Em 2016, refugiados chegavam da guerra na Síria, e as opiniões se endureciam. Desenvolvi a Cuisine Divers, uma cozinha cooperativa para chefs de diferentes países, para reunir culturas sob o mesmo teto. Queríamos compartilhar equipamentos e criar um lugar onde os chefs pudessem aperfeiçoar o ofício sem carregar sozinhos o risco de falir. A Cuisine Divers tinha todos os ingredientes para dar certo, e foi ali que encontrei meu primeiro investidor, um investidor-anjo.',
                   'In 2016, refugees were arriving from the war in Syria, and opinions were hardening. I developed Cuisine Divers, a cooperative kitchen for chefs from different countries, to bring cultures together under one roof. We wanted to share equipment and create a place where chefs could develop their craft without carrying the risk of failure alone. Cuisine Divers had all the ingredients to succeed, and it was there that I found my first investor, a business angel.'))
    ideas += text(('No fim, recusei. Um desenvolvedor de negócios experiente me aconselhou a não fazer de um restaurante o meu primeiro negócio. Eu também não queria depender de um único investidor, um ponto único de falha no meu cangote. Não estava preparado para liderar sozinho e ser o único responsável por 150 mil euros em investimento e equipamentos. Isso me fez parar no início de 2017.',
                   'In the end, I declined. An experienced business developer advised me not to make a restaurant my first business. I also did not want to depend on one investor, a single point of failure breathing down my neck. I was not prepared to lead alone and be solely accountable for €150,000 of investment and equipment. That made me stop in early 2017.'))
    ideas += text(('Fiz uma pausa, e foi nesse momento que deixei o empreendedorismo e a inovação social offline. Em julho de 2017, fui convidado para uma apresentação sobre Ethereum. Blockchain ainda era algo bastante novo para mim, e aquilo me inspirou a explorá-la como uma forma peer-to-peer de financiar negócios regenerativos. Trabalhar online tirou o peso da logística, das mudanças constantes e da comunicação constante que uma cozinha exige. As redes online também filtram melhor: quando você passa tempo todos os dias numa comunidade atrás da tela, as pessoas passam a conhecer você, e é assim que se encontram as pessoas certas para trabalhar junto. Isso substituiu os eventos de networking, onde eu raramente encontrava o público certo para as minhas ideias de negócio.',
                   'I took a break, and that was the moment I left offline entrepreneurship and social innovation. In July 2017, I was invited to an Ethereum presentation. Blockchain was still fairly new to me, and it inspired me to explore it as a peer-to-peer way to fund regenerative businesses. Working online removed the weight of logistics, and the constant moving and communication a kitchen needs. Online networks also filter better: when you spend time every day in a community behind the screen, people get to know you, and that is how you find the right people to work with. It replaced the networking events where I rarely met the right audience for my business ideas.'))
    ideas += linked(('Assim mergulhei no mundo dos nativos de cripto. Em 2018, tornei-me embaixador da ', 'This took me down the rabbit hole of crypto natives. In 2018, I became a '),
                    ('Holochain', 'Holochain', 'https://www.holochain.org/what-holochain/'),
                    (' e estudei o crédito mútuo, uma forma de uma comunidade trocar valor localmente. Anos depois, esse caminho me levou a entender a ', ' ambassador and explored mutual credit, a way for a community to exchange value locally. Years later, that path led me to understand '),
                    ('teoria de Wyckoff', 'Wyckoff theory', 'https://en.wikipedia.org/wiki/Richard_Wyckoff'),
                    (', e como os ciclos do mercado sufocam a inovação que vem de baixo para cima: iniciativas de negócio que precisam de financiamento e de um público disposto a comprar os seus produtos.', ', and how market cycles suppress innovation that comes from the bottom up: business initiatives that need funding and a retail crowd that wants to buy their products.'))
    ideas += linked(('Em 2020, cofundei a ', 'In 2020, I co-founded '),
                    ('DeFiants', 'DeFiants', 'https://be.linkedin.com/company/defiants'),
                    (', uma agência Web3 sem fins lucrativos. Ela cresceu de forma orgânica, sem plano, a partir do nosso trabalho no meio das startups, onde eu dava conselhos de marketing e ajudava startups chinesas a se comunicar com o Ocidente, cujas estratégias de venda lhes eram completamente estranhas. Ali conheci um desenvolvedor de projetos canadense da IBM, que me ajudou a montar uma estrutura de negócio capaz de crescer. Mantivemos uma rotina de serviços de baixo custo e alto valor e conquistamos contratos suficientes para ter lucro e investi-lo em projetos de impacto social, sem dívidas e sem um único investidor nas nossas costas. Como serviço de intermediação, éramos os técnicos de som: cuidávamos do palco para os projetos que ficavam sob os holofotes.', ', a not-for-profit Web3 agency. It grew organically, without a plan, out of our work in the start-up world, where I gave marketing advice and helped Chinese start-ups communicate with the West, whose sales strategies were completely foreign to them. There I met a Canadian project developer from IBM, who helped me build a business framework that could scale. We kept a routine of low-cost, high-value services and won enough contracts to make a profit and invest it in social-impact projects, without debt and without a single investor on our backs. As a middleware service, we were the sound technicians: we managed the stage for the projects that took the spotlight.'))
    ideas += linked(('No início do mercado de alta de 2020, começamos a trabalhar com lançamentos de tokens. Um contato nos trouxe alguns dos projetos mais promissores da Outlier Ventures, como World Mobile, Lamina1 e ', 'At the beginning of the 2020 bull market, we started working on token launches. A contact brought us some of the most promising projects from Outlier Ventures, such as World Mobile, Lamina1 and '),
                    ('Bittensor', 'Bittensor', 'https://www.linkedin.com/pulse/beginners-guide-bittensor-defiants-dunne'),
                    (', e chegamos a trabalhar um mês com a comunidade da BNB Chain para ajudar a criar o seu programa de embaixadores. Os projetos mais ambiciosos nos respeitavam como construtores de comunidade competentes.', ', and we even worked for a month with the BNB Chain community to help set up its ambassador programme. The most ambitious projects respected us as capable community builders.'))
    ideas += text(('Ao longo de mais de 15 projetos, com uma equipe de 20 pessoas, vimos todas as armadilhas e todos os sucessos: o que funcionou e o que não funcionou. Estávamos nos ombros de gigantes. Ver esse espectro completo nos permitiu dar conselhos que pouparam os projetos de gastos desperdiçados. Os anos na DeFiants me deram uma base sólida em crescimento, operação, gestão de contas, formação de equipes e foco, e me ensinaram o valor do trabalho das pessoas e das finanças.',
                   'Across more than 15 projects, with a team of 20 people, we saw every pitfall and every success: what worked and what didn’t. We were standing on the shoulders of giants. Seeing the full spectrum let us give advice that saved projects from wasteful spending. My years at DeFiants gave me a strong foundation in scaling, operations, account management, team building and focus, and taught me the value of people’s work and of finance.'))
    ideas += linked(('Em 2021, a DeFiants começou a trabalhar com a ', 'In 2021, DeFiants began working with '),
                    ('Unidos', 'Unidos', 'https://unidosprojects.com/'),
                    (', uma organização dirigida por refugiados em Nakivale, Uganda. Juntos, construímos um centro de educação com empregos para professores e formação em Web3. Também ajudei a desenvolver uma proposta para transformar resíduos de mercados e cozinhas em vermicomposto e apoiar a produção local de alimentos. Em 2024, Paulinho Muzaliwa, que dirige a Unidos, recebeu o ', ', a refugee-led organisation in Nakivale, Uganda. Together, we built an education centre with teaching jobs and Web3 training. I also helped develop a proposal to turn market and kitchen waste into vermicompost and support local food production. In 2024, Paulinho Muzaliwa, who leads Unidos, received the '),
                    ('Prêmio Gene Dewey para Refugiados', 'Gene Dewey Refugee Award', 'https://www.prnewswire.com/news-releases/usa-for-unhcr-announces-gene-dewey-refugee-award-winners-302067549.html'),
                    (', e o projeto de agricultura regenerativa da Unidos, o REGESOIL, recebeu o ', ', and Unidos’s regenerative farming project, REGESOIL, received the '),
                    ('Prêmio Internacional Ockenden', 'Ockenden International Prize', 'https://www.ockendenprizes.org/2024-prizes/unidos-social-innovation-center/'),
                    ('. Levar o plano de vermicomposto à escala custaria cerca de US$ 60 mil por ano. Isso me deixou uma pergunta que ainda carrego: como uma organização comunitária consegue financiamento estável para sistemas alimentares que possam crescer?', '. Running the vermicompost plan at scale would cost about US$60,000 a year. It left me with a question I still carry: how can a community organisation get steady funding for food systems that can grow?'))
    ideas += text(('Em 2023, saí da DeFiants, que fechou os escritórios dois anos depois, após um longo mercado de baixa com muito menos grandes lançamentos de tokens. No meu trabalho com comunidades digitais, eu tinha visto campanhas contar publicações e ignorar relações. Pessoas criavam memes e promoviam tokens sem remuneração, enquanto os maiores detentores lucravam com a atenção. Muitas se esgotavam. Em 2024, passei a entender melhor como o X escolhe quais publicações as pessoas veem. Hoje, vejo redes sociais e sistemas de IA repetirem a mesma retórica e reforçarem ciclos em que as pessoas ficam presas, sem perceber o quanto o seu modo de vida se afastou da regeneração.',
                   'In 2023, I left DeFiants, which closed its offices two years later, after a long bear market with far fewer large token launches. In my work with digital communities, I had seen campaigns count posts and ignore relationships. People made memes and promoted tokens without pay, while larger holders gained from the attention. Many burned out. In 2024, I learned more about how X selects which posts people see. Today, I see social media and AI systems repeat the same rhetoric and reinforce loops people get stuck in, without noticing how far their way of life has moved from regeneration.'))
    ideas += text(('Em 2025, esses caminhos se juntaram. Estou construindo o SIAH Protocol para guardar um registro de contribuições que outras pessoas confirmam, para que uma comunidade lembre quem ajudou quando uma campanha termina. A proposta da IMOBX leva essa ideia de compartilhar à moradia: famílias poderiam caminhar para ser donas da própria casa, num bairro que administram juntas. Hoje, agentes de IA que escrevem código fazem boa parte do que antes exigia um diretor de tecnologia e uma equipe de desenvolvimento. Ter estado nos ombros de gigantes, sabendo por dentro o que fez lançamentos darem certo ou errado, é o que eu trago para um projeto de tokenização como a IMOBX.',
                   'In 2025, these threads came together. I’m building SIAH Protocol to keep a record of contributions confirmed by other people, so a community remembers who helped after a campaign ends. The IMOBX proposal brings that idea of sharing to housing: families could move towards owning their house in a neighbourhood they run together. Today, AI coding agents can do much of what once took a CTO and a development team. Having stood on the shoulders of giants, knowing from the inside what made launches succeed or fail, is what I bring to a tokenization project like IMOBX.'))
    ideas += '</div></details>'
    ideas += text(('Como nos conhecemos', 'How we met'), 'h3')
    ideas += text(('Conheci Rafael pela Ether Vista, hoje chamada Arctide, onde nós dois tínhamos o token VISTA. Rafael chegou por uma campanha brasileira, com a grande comunidade brasileira que hoje, junto com uma internacional, é a principal comunidade por trás da Ether Vista. Eu cheguei pelo primeiro token lançado na Ether Vista, que me contratou como gerente de campanha de embaixadores. Esse trabalho me ensinou as bases do projeto, e decidi liderar uma retomada pela comunidade e ajudar a desenhar um modelo de negócio adequado. Foi por isso que Rafael me perguntou se eu o ajudaria a criar um token para a IMOBX e lançá-lo na Arctide. Hoje estou ajudando Rafael a fundar a IMOBX, porque precisamos de ferramentas melhores para nos organizar e levar recursos para onde fazem diferença.',
                   'Rafael and I met through Ether Vista, now called Arctide, where we both held its VISTA token. Rafael came in through a Brazilian campaign, with the large Brazilian community that is now, together with an international one, the main community behind Ether Vista. I came in through the first token launched on Ether Vista, which hired me as its ambassador campaign manager. That work taught me the foundations of the project, and I decided to lead a community takeover and help design a proper business model. That is why Rafael asked me whether I would help him build a token for IMOBX and launch it on Arctide. Now I’m helping him found IMOBX, because we need better tools to organise ourselves and direct resources where they make a difference.'))
    ideas += text(('Como John trabalha com comunidades', 'John’s approach to community work'), 'h3')
    ideas += text(('A questão que vi por trás de muitos problemas, da moradia às organizações comunitárias, é a distribuição: quem controla os recursos e quem consegue acessá-los. O controle fica concentrado nas mãos de quem tem riqueza, enquanto temos poucas formas de compartilhar bens comuns, como moradia e alimentos saudáveis, sazonais e produzidos em harmonia com a natureza. A industrialização mudou a produção, mas não garantiu acesso ao que as pessoas precisam. E distribuir recursos também exige compartilhar a liderança de forma justa.',
                   'The question I kept finding behind many problems, from housing to community organisations, was distribution: who controls resources and who can access them. Control rests heavily with people who hold wealth, while we have too few ways to share what we hold in common, such as housing and healthy, seasonal food grown in balance with nature. Industrialisation changed production, but did not ensure access to what people need. Sharing resources also means sharing leadership fairly.'))
    ideas += text(('Acredito que nossa tarefa é dar às próximas gerações meios para distribuir recursos e influência de forma mais justa. O caminho começa perto de casa. Autossuficiência e cooperação local podem nos ajudar a gastar menos energia em disputas sobre forças que não controlamos e mais em nos adaptar e construir alternativas práticas.',
                   'I believe our task is to give future generations the means to distribute resources and influence more fairly. The way forward starts close to home. Self-sufficiency and local cooperation can help us spend less energy fighting over forces we cannot control, and more on adapting and building practical alternatives.'))
    ideas += text(('Acredito que muita gente já percebe isso, mas falta estrutura para agir: ferramentas, formas de nos organizar e meios para sustentar a vida de outra maneira. Para mim, construir essas alternativas é uma forma de desobediência civil. Podemos pisar no freio e criar meios locais de sustentar a vida, com menos dependência de infraestruturas controladas por outros e de sistemas de tributação que muitas pessoas sentem como agressivos e fora do seu controle. Assim, podemos assumir o papel de guardiões e ajudar a atravessar as crises. Uma crise também pode abrir espaço para mudar de rumo.',
                   'I believe many people already sense this, but lack a structure for action: tools, ways to organise ourselves and means to sustain life differently. To me, building these alternatives is a form of civil disobedience. We can step on the brake and create local ways to sustain life, with less dependence on infrastructure controlled by others and tax systems many people experience as aggressive and beyond their control. That can help us act as stewards and navigate crises. A crisis can also open the way to change course.'))
    ideas += text(('O meu método começa com a generosidade. Quando você oferece o seu trabalho e o seu conhecimento livremente, as pessoas começam a prestar atenção. Quando continuam vendo você entregar, essa atenção vira confiança, e a confiança traz mais atenção. Foi assim que construímos a DeFiants: pela ação, fazendo o trabalho e mostrando como trabalhávamos, em vez de growth hacking, grandes orçamentos e marketing rápido. O desenvolvimento de produtos me ensinou a criar impulso e uma história: envolver as pessoas certas no momento certo, para que a qualidade se mantenha em cada apresentação, sempre. A IMOBX está no começo, e quero construí-la da mesma forma.',
                   'My method starts with generosity. When you give your work and knowledge freely, people start to pay attention. When they keep seeing you deliver, that attention turns into trust, and trust brings more attention. That is how we built DeFiants: through action, by doing the work and showing how we worked, instead of growth hacking, big budgets and fast marketing. Product development taught me how to build momentum and a story: to involve the right stakeholders at the right time, so that the quality holds at every pitch, consistently. IMOBX is at its start, and I want to build it the same way.'))
    ideas += '</section>'
    ideas += '<section id="check">' + text(('Os princípios por trás da IMOBX', 'The principles behind IMOBX'), 'h2')
    ideas += '<div class="idea-grid">'
    ideas += idea(('Os princípios de Elinor Ostrom', 'Elinor Ostrom’s principles'),
                  [('Elinor Ostrom estudou como comunidades administram recursos compartilhados. Recebeu o Nobel de economia em 2009 por seu trabalho sobre governança econômica. Sua pesquisa orienta as regras propostas pela IMOBX para os espaços comuns.',
                    'Elinor Ostrom studied how communities manage shared resources. She received the 2009 Nobel Prize in economics for her work on economic governance. Her research informs IMOBX’s proposed rules for shared spaces.')],
                  (('Elinor Ostrom no site do Prêmio Nobel', 'Elinor Ostrom on the Nobel Prize site'), 'https://www.nobelprize.org/prizes/economic-sciences/2009/ostrom/facts/'))
    ideas += idea(('Os princípios das cooperativas', 'The cooperative principles'),
                  [('Os sete princípios da Aliança Cooperativa Internacional incluem a gestão democrática pelos membros. No Brasil, a lei das cooperativas define um membro, um voto (Lei 5.764, art. 42).',
                    'The International Cooperative Alliance’s seven principles include democratic control by members. In Brazil, the cooperative law sets one member, one vote (Lei 5.764, article 42).')],
                  (('A identidade cooperativa (ICA)', 'The cooperative identity (ICA)'), 'https://ica.coop/en/cooperatives/cooperative-identity'))
    ideas += '</div></section>'
    ideas += '<section id="studied">' + text(('Modelos de moradia comunitária', 'Community housing models'), 'h2')
    ideas += '<div class="idea-grid">'
    ideas += idea(('Mietshäuser Syndikat (Alemanha)', 'Mietshäuser Syndikat (Germany)'),
                  [('Uma rede alemã de imóveis de aluguel administrados pelos moradores. A venda de um imóvel exige o acordo da associação de moradores e do Syndikat. Os moradores decidem os aluguéis e quem entra. No plano da IMOBX, pátios e salas de estudo continuam compartilhados, com o custo inicial dividido entre todas as casas.',
                    'A German network of rental housing run by residents. Selling a property needs agreement from the residents’ association and the Syndikat. Residents decide rents and who moves in. IMOBX’s plan keeps courtyards and study rooms shared, with their initial cost covered by all the houses.')],
                  (('Mietshäuser Syndikat', 'Mietshäuser Syndikat'), 'https://www.syndikat.org/syndikat/'))
    ideas += idea(('FUCVAM (Uruguai)', 'FUCVAM (Uruguay)'),
                  [('A federação uruguaia de cooperativas de moradia por ajuda mútua, fundada em 1970. As famílias ajudam a construir as casas, que pertencem à cooperativa. A proposta da IMOBX prevê que cada família se torne dona de sua casa.',
                    'Uruguay’s federation of mutual-aid housing cooperatives, founded in 1970. Families help build the houses, which the cooperative owns. IMOBX proposes that each family gradually becomes the owner of its house.')],
                  (('FUCVAM', 'FUCVAM'), 'https://www.fucvam.org.uy'))
    ideas += idea(('Fundos comunitários de terra', 'Community land trusts'),
                  [('O fundo é dono do terreno. As famílias podem comprar uma casa e arrendar o terreno onde ela fica por um contrato de longa duração. Na proposta da IMOBX, nenhuma votação pode, por si só, mudar o contrato de moradia de uma família. O contrato planejado exigiria que a família e a IMOBX concordassem com mudanças, sujeito à lei brasileira.',
                    'The trust owns the land. Families can buy a house and lease the land underneath it through a long-term agreement. In IMOBX’s proposal, no vote can on its own change a family’s housing agreement. The planned agreement would require the family and IMOBX to agree to changes, subject to Brazilian law.')],
                  (('Community land trusts (Grounded Solutions Network)', 'Community land trusts (Grounded Solutions Network)'), 'https://groundedsolutions.org/strengthening-neighborhoods/community-land-trusts'))
    ideas += '</div></section>'
    # The closing makes the founders' case (owner, 29 Oct: "use my arguments … instead of 'if you have ideas let me know'").
    ideas_close = ('<section class="closing-band" id="help">'
                   + text(('Quem aluga pode se tornar dono, e um bairro pode viver sem estresse. Estamos formando o círculo fundador do primeiro bairro: venha construir com a gente.',
                           'Renters can become owners, and a neighbourhood can live without stress. We are forming the founding circle for the first one: come and build it with us.'))
                   + text(('Apresente-se', 'Introduce yourself'), 'a', 'class="button act" href="contact.html"') + '</section>')
    build_guide.ideas_html = ideas
    build_guide.ideas_close = ideas_close
    build_guide.ideas_head = (f'<link rel="stylesheet" href="{asset_v("bands.css")}"><link rel="stylesheet" href="{asset_v("ideas.css")}">'
                              f'<script src="{asset_v("ideas.js")}" defer></script>')

    def flow(items, cls='flow'):
        """A short sequence drawn as connected steps (numbers from the list, no arrow glyphs)."""
        return f'<ol class="{cls}">' + ''.join('<li>' + (text(i[0], 'strong') + text(i[1], 'span') if isinstance(i[0], list) else text(i, 'span')) + '</li>'
                                              for i in items) + '</ol>'

    # Why housing: the wider problem in figures, each with its source, and what IMOBX works on.
    why = guide['why']
    # Copy sweep, 28 Oct (review C, owner 'proceed'): the problem stays; the rent-or-sell economics moved to
    # Costs and funding, how decisions are shared moved to Project stages, and the sources wait for the Ideas page.
    wl = [x.split('. ', 1) for x in why['lead']]
    page_why = '<main class="paper guide-paper why-page band-page" id="main">' + text(why['title'], 'h1')
    page_why += '<div class="key-card">' + text((wl[0][0] + '.', wl[1][0] + '.')) + '</div>'
    page_why += text((wl[0][1], wl[1][1]), 'p', 'class="guide-lead"')
    page_why += on_this_page([(('Os números', 'The figures'), 'figures'), (('Favelas', 'Favelas'), 'context'),
                              (('Por que o aluguel sobe', 'Why rents rise'), 'causes'), (('O que a IMOBX faria', 'What IMOBX would do'), 'answer')])
    page_why += '<section id="figures">' + text(why['facts_title'], 'h2') + '<ol class="figure-row">'
    for big, fact in zip(why['figures_big'], why['facts']):
        page_why += '<li>' + text(big, 'strong', 'class="figure-big"') + text(fact['text']) + '<p class="source-note">' + text(('Fonte: ', 'Source: '), 'span')
        page_why += text(fact['source'], 'a', f'href="{esc(fact["url"])}"') + ('. ' + text(fact['limit'], 'span') if fact.get('limit') else '.') + '</p></li>'
    page_why += '</ol></section><section id="context">' + text(why['context_title'], 'h2') + why['context_html']
    page_why += '</section><section id="causes">' + text(why['causes_title'], 'h2') + text(why['causes'])
    page_why += '<ul id="answer">' + ''.join(text(a, 'li') for a in why['answer']) + '</ul></section>'
    page_why += '<span id="rent-to-own-or-rent"></span><span id="organisation"></span>'  # sections moved to transparency.html and roadmap.html#governance
    page_why += '<section class="closing-band" id="next">'
    page_why += text(('Como funcionaria o aluguel com compra', 'How rent-to-own would work'), 'a', 'class="button act" href="rent-to-own.html"') + '</section>'
    page_why += partner_line('why.html') + '</main>'
    (root / 'why.html').write_text(page('IMOBX | Why housing', page_why, f'<link rel="stylesheet" href="{asset_v("bands.css")}"><script src="assets/site.js" defer></script>',
        version=guide['version'], lang='pt-BR', title_pt='IMOBX | Por que moradia'))

    # Copy for 'The self-compounding token' (owner, 1 Nov). PT and EN here; NL in i18n/nl.json.
    TK = {'title': ('Self-compounding', 'Self-compounding'), 'lead': ('O token da IMOBX é um token self-compounding de financiamento da comunidade: suas taxas voltam para a comunidade que cresce em torno das casas da IMOBX.', 'The IMOBX token is a self-compounding community-funding token: its fees go back into the community that grows around the IMOBX houses.'), 'toc': [(('Para que serve', 'What it is for'), 'use'), (('O que significa', 'What it means'), 'meaning'), (('Para onde vai a taxa', 'Where the fee goes'), 'fee'), (('Em que é diferente', 'How it differs'), 'sale'), (('As quatro regras', 'The four rules'), 'laws'), (('Aviso importante', 'Important notice'), 'notice')], 'use_h': ('Para que serve?', 'What is it for?'), 'use': ('Cada negociação do token paga uma taxa que financia a comunidade que cresce em torno das casas. Ter o token é opcional.', 'Every trade of the token pays a fee that funds the community growing around the houses. Holding the token is optional.'), 'use_more': ('Qualquer benefício para quem trava seus tokens será nomeado, com suas condições, antes de valer. O que o token faz pela comunidade é definido por quatro regras, os quatro V, mais abaixo nesta página.', 'Any benefit for people who lock their tokens will be named, with its terms, before it applies. What the token does for the community is set by four rules, the four V’s, further down this page.'), 'use2': ('Na proposta, as famílias se associam a uma cooperativa habitacional e não precisam comprar nem ter tokens. A IMOBX muito provavelmente começa com uma família em Guadalupe e depois constrói cinco apartamentos novos de cada vez, cada família com o seu próprio contrato de moradia. O token vem numa etapa posterior e fica separado desses contratos.', 'Under the proposal, families join a housing cooperative and do not need to buy or hold tokens. IMOBX most likely starts with one family in Guadalupe, then builds five new flats at a time, each family with its own housing agreement. The token comes at a later stage and stays separate from those agreements.'), 'supply': ('A IMOBX cria 1.000.000 de tokens, uma única vez. Três quartos ficam para o mercado quando o token abrir. O quarto restante fica reservado: 5% para parceiros, 5% para a operação, 5% para recompensas da comunidade, 5% para a governança e 3% para corretores, todos travados para sempre, além de 2% para custos jurídicos. A equipe não recebe tokens.', 'IMOBX creates 1,000,000 tokens, once. Three quarters are for the market when the token opens. The remaining quarter is set aside: 5% for partners, 5% for operations, 5% for community rewards, 5% for governance and 3% for brokers, all locked for good, plus 2% for legal costs. The team receives no tokens.'), 'notice_h': ('Aviso importante', 'Important notice'), 'notice': [('O token da IMOBX está planejado e ainda não foi emitido. Esta página descreve o desenho pretendido, que pode mudar antes do lançamento, à medida que as regras brasileiras para criptoativos forem definidas.', 'The IMOBX token is planned and has not been issued. This page describes its intended design, which may change before launch as Brazil’s rules for crypto-assets take shape.'), ('Esta página não é uma oferta nem um convite para comprar, nem uma recomendação financeira, jurídica ou fiscal. Nenhuma autoridade analisou ou aprovou este conteúdo.', 'This page is not an offer or an invitation to buy, and it is not financial, legal or tax advice. No authority has reviewed or approved it.'), ('O token não dá participação na IMOBX nem direito a qualquer casa, terreno ou pagamento das famílias. Os valores das taxas descrevem o desenho e não são pagamentos prometidos.', 'The token gives no share in IMOBX and no claim on any house, plot or family payment. The fee figures describe the design and are not promised payments.'), ('Depois de emitido, um criptoativo pode perder seu valor em parte ou totalmente, e pode ser difícil vendê-lo quando você quiser. Ele não tem a proteção do FGC nem de outro fundo de garantia, e uma falha no software ou a perda da chave da carteira pode fazer você perder os tokens para sempre.', 'Once issued, a crypto-asset may lose its value in part or in full and may be hard to sell when you want to. It is not covered by Brazil’s deposit guarantee fund (FGC) or any compensation scheme, and a software fault or a lost wallet key can mean losing tokens for good.'), ('Procure orientação independente antes de tomar qualquer decisão sobre o token.', 'Get independent advice before making any decision about the token.')], 'meaning_h': ('O que significa self-compounding?', 'What does self-compounding mean?'), 'meaning': ('A maioria dos projetos de token levanta recursos vendendo tokens a investidores antes do lançamento, ou criando tokens novos. A IMOBX não faz rodada antecipada e não cria tokens depois. O que os primeiros compradores pagam vai para o pool do token, e a renda do projeto com o token é a taxa paga cada vez que ele muda de mãos. A maior parte dessa taxa volta para o projeto, para salários, novas casas e o pool, e assim o projeto cresce com o que ele mesmo gera.', 'Most token projects raise funds by selling tokens to early investors before launch, or by creating new ones. IMOBX holds no early round and creates no tokens later. What the first buyers pay goes into the token’s pool, and the project’s income from the token is the fee paid each time it changes hands. Most of that fee goes back into the project, to wages, new houses and the pool, so the project grows from what it earns.'), 'meaning2': ('80% de cada taxa vão para quem é contratado para fazer o trabalho da comunidade, para novas casas e para o pool do token. Os outros 20% vão para quem trava seus tokens para sempre.', 'Four fifths of every fee go to the people hired to do the community’s work, to new houses and to the token’s pool. The other fifth goes to people who lock their tokens for good.'), 'reach_h': ('Como se consegue o token?', 'How do you get the token?'), 'reach': ('Você compra o token num pool de negociação na Arctide, uma corretora na rede Arc, a partir do lançamento. O pool começa com três quartos de todos os 1.000.000 de tokens, travados nele para sempre: ninguém pode retirá-los. A partir do lançamento, qualquer pessoa pode comprar tokens do pool ou vendê-los de volta, pelo preço que o pool der naquele momento. Ninguém vende o token antes do lançamento.', 'You buy it from a trading pool on Arctide, an exchange on the Arc network, once the token launches. The pool starts with three quarters of all 1,000,000 tokens, locked in it for good, so nobody can take them out. From launch on, anyone can buy tokens from the pool or sell them back, at the price the pool gives at that moment. Nobody sells the token before launch.'), 'reach3': ('O quarto restante também fica travado para sempre: 5% para parceiros, 5% para a operação, 5% para recompensas da comunidade e 5% para a governança, além de 3% para corretores e 2% para custos jurídicos. A equipe não recebe tokens.', 'The remaining quarter is locked for good as well: 5% for partners, 5% for operations, 5% for community rewards and 5% for governance, plus 3% for brokers and 2% for legal costs. The team receives no tokens.'), 'reach2': ('Nossos fundadores têm TIDE, o token da própria Arctide.', 'Our founders hold TIDE, Arctide’s own token.'), 'fee_h': ('Para onde vai a taxa?', 'Where does the fee go?'), 'fee': ('Cada vez que o token muda de mãos, 14% do valor é a taxa. Quando US$ 100 em tokens mudam de mãos, a taxa de US$ 14 se divide assim:', 'Each time the token changes hands, 14% of the amount is the fee. When US$100 of tokens changes hands, the US$14 fee divides like this:'), 'row_wages': ('Salários de quem é contratado para fazer o trabalho da comunidade', 'Wages for the people hired to do the community’s work'), 'row_houses': ('Construção de novas casas', 'Building new houses'), 'row_pool': ('Pessoas que colocam seus próprios recursos no pool', 'People who add their own funds to the pool'), 'row_lock': ('Quem trava seus tokens para sempre', 'People who lock their tokens for good'), 'row_venue': ('Taxa da própria Arctide', 'Arctide’s own fee'), 'row_total': ('Total da taxa', 'Total fee'), 'fee2': ('O pool é a reserva comum onde o token muda de mãos, e recebe US$ 4,90 de cada taxa de US$ 14. Quando a IMOBX coloca os recursos iniciais do pool, ela fica com três quartos dele, e essa parte da taxa vai para novas casas (US$ 3,67). O resto (US$ 1,23) vai para quem coloca seus próprios recursos no pool. Se o token abrir pela curva de venda da Arctide, os recursos dos primeiros compradores iniciam o pool, e essa parte da taxa vai para a Arctide; as novas casas recebem então a parte gerada pelos recursos que a própria IMOBX colocar.', 'The pool is the shared reserve through which the token changes hands, and it gets US$4.90 of every US$14 fee. When IMOBX puts in the pool’s starting funds, it holds three quarters of the pool, and that part of the fee goes to new houses (US$3.67). The rest (US$1.23) goes to people who add their own funds to the pool. If the token opens on Arctide’s sale curve instead, the first buyers’ funds start the pool, and that part of the fee goes to Arctide; new houses then get the share earned by funds IMOBX adds itself.'), 'fee3': ('O token também vai ser negociado na Argus, uma segunda corretora. Lá a taxa é de 11%: de cada US$ 100 negociados, a Argus fica com US$ 3,30 e US$ 7,70 vão para o projeto.', 'The token will also trade on Argus, a second exchange. The fee there is 11%: of each US$100 traded, Argus keeps US$3.30 and US$7.70 goes to the project.'), 'price_h': ('O preço pode cair?', 'Can the price fall?'), 'price': ('Sim. O preço muda a cada negociação: sobe quando mais gente compra e cai quando mais gente vende. Por exemplo, se muita gente vender na semana seguinte à sua compra, tokens pelos quais você pagou US$ 100 podem passar a valer US$ 60. Ninguém na IMOBX define o preço. A venda também paga a taxa, então, se você compra e vende logo em seguida pelo mesmo preço, voltam cerca de US$ 73,50 dos seus US$ 100.', 'Yes. The price moves with every trade: it rises when more people buy and falls when more people sell. For example, if many people sell the week after you buy, tokens you paid US$100 for could be worth US$60. Nobody at IMOBX sets the price. Selling also pays the fee, so if you buy and sell straight back at the same price, about US$73.50 of your US$100 comes back.'), 'sale_h': ('Em que ele é diferente da maioria dos tokens?', 'How is it different from most tokens?'), 'sale': ('Tokenomics são as regras de um token: quantos tokens existem, quem recebe uma parte e de onde vem a renda do projeto. Na maioria dos projetos, a equipe e os primeiros investidores ficam com uma grande parte dos tokens, e novos tokens são criados como recompensa. O token da IMOBX segue outras regras:', 'Tokenomics are a token’s rules: how many tokens exist, who gets a share and where the project’s income comes from. In most token projects the team and early investors hold a large share of the tokens, and new tokens are created as rewards. The IMOBX token follows different rules:'), 'cmp_head': [('', ''), ('Tokenomics tradicional', 'Traditional tokenomics'), ('O token da IMOBX', 'The IMOBX token')], 'cmp': [[('De onde vem a renda do projeto', 'Where the project’s income comes from'), ('Dos próprios tokens: as partes da equipe e dos primeiros investidores', 'The tokens themselves: the team’s and early investors’ shares'), ('De uma taxa cada vez que o token muda de mãos', 'A fee each time the token changes hands')], [('Quantos tokens existem', 'How many tokens exist'), ('Muitas vezes novos tokens são criados como recompensa, e cada token passa a representar uma parte menor', 'New tokens are often created as rewards, so each token stands for a smaller share over time'), ('1.000.000 de tokens, fixos. Nenhum é criado depois', '1,000,000 tokens, fixed. None are created later')], [('O que a equipe recebe', 'What the team gets'), ('Uma grande parte dos tokens', 'A large share of the tokens'), ('Nenhum token para a equipe', 'No tokens for the team')], [('O que mantém o projeto de pé', 'What keeps it going'), ('A entrada constante de recursos de novos participantes', 'A steady flow of funding from newcomers'), ('A renda que a comunidade já ganhou, usada dentro de um orçamento que os membros aprovam', 'Income the community has already earned, spent under a budget the members agree')], [('Para onde vai a renda', 'Where the income goes'), ('Principalmente para a equipe e os primeiros investidores', 'Mostly to the team and early investors'), ('De cada taxa de 14%: 45% para salários, 35% para o pool (a maior parte para novas casas), 20% para quem trava seus tokens', 'Of every 14% fee: 45% to wages, 35% to the pool (most of it to new houses), 20% to people who lock their tokens')]], 'laws_h': ('Volume, verificação e voto', 'Volume, verify, vote'), 'laws': ('Quando olhamos para a utilidade do token, três leis são inegociáveis: a taxa, os registros e os votos.', 'When we look at the token’s utility, three laws are non-negotiable: the fee, the records and the votes.'), 'laws_list': [(('Volume', 'Volume'), ('A negociação paga o trabalho, então a taxa precisa ficar como foi publicada. Antes do lançamento, publicamos a taxa, quem pode mudá-la e quem tem as chaves de administração, para que ninguém possa aumentá-la às escondidas.', 'Trading pays for the work, so the fee must stay as published. Before launch we publish the fee, who can change it and who holds the admin keys, so nobody can raise it in secret.')), (('Verificação', 'Verify'), ('Qualquer pessoa, com ou sem token, pode ver para onde foi cada taxa: cada pagamento, para que foi e quem aprovou.', 'Anyone, with or without a token, can see where each fee went: every payment, what it was for and who approved it.')), (('Voto', 'Vote'), ('O peso de um voto vem principalmente do trabalho que outras pessoas confirmaram, como construir ou trazer gente que usa os serviços, e não de quantos tokens alguém tem. Publicamos o equilíbrio exato antes do lançamento.', 'A vote’s weight comes mainly from work that others have confirmed, such as building or bringing in people who use the services, rather than from how many tokens someone holds. We publish the exact balance before launch.'))], 'vote_rule': ('Nas regras propostas, votos sobre o token não alterariam o contrato de moradia de uma família. O contrato planejado exigiria o consentimento da família e da IMOBX para mudanças, sujeito à lei brasileira.', 'Under the proposed rules, token votes cannot change a family’s housing agreement. The planned agreement would require consent from the family and IMOBX for changes, subject to Brazilian law.'), 'risk_h': ('O que pode dar errado?', 'What could go wrong?'), 'risks': [('O preço pode cair muito, e um pool pequeno pode dificultar a venda do token.', 'The price can fall a long way, and a small pool can make the token hard to sell.'), ('A negociação costuma cair bastante depois do lançamento: na Arctide, as taxas semanais caíram de US$ 9.845 na primeira semana para menos de US$ 200 no fim de outubro de 2026.', 'Trading usually drops sharply after a launch: on Arctide, weekly fees fell from US$9,845 in its first week to under US$200 by late October 2026.'), ('A Arc e o USDC são operados por empresas, e o USDC pode ser bloqueado pela empresa que o emite.', 'Arc and USDC are run by companies, and USDC can be frozen by the company that issues it.'), ('As regras para criptoativos estão mudando no Brasil, na Europa e nos Estados Unidos, e uma regra nova pode obrigar a mudar o modelo do token.', 'The rules for crypto-assets are changing in Brazil, Europe and the US, and a new rule can force changes to the token.')], 'closing_link': ('Como a IMOBX registra os pagamentos', 'How IMOBX records payments'), 'closing': ('Perguntas sobre o token?', 'Questions about the token?'), 'closing_btn': ('Pergunte no grupo da IMOBX no Telegram', 'Ask in the IMOBX Telegram group'), 'ledger_answer': ('A IMOBX planeja um token self-compounding de financiamento comunitário para uma etapa posterior. As pessoas poderão escolher comprá-lo ou vendê-lo. As taxas de negociação deverão apoiar o trabalho da comunidade e futuras moradias, mas essa receita é incerta.', 'IMOBX is planning a self-compounding community-funding token for a later stage. People could choose to buy or sell it. Trading fees are intended to support community work and future housing, but that income is uncertain.'), 'ledger_link': ('Como o token funciona', 'How the token works')}

    # token.html is built after the ledger page (it reuses the loop drawing): 'The self-compounding token' (owner, 1 Nov).

    # The blockchain page (owner, 25 Oct): how IMOBX would use Arc for its records and funding, how a token would
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
    # Rebuilt 28 Oct (owner decisions 25 and 27, review-C §1): the reader's picture first, then privacy, requests and
    # complaints, the records, and what is not decided; the token and the blockchain's limits sit in folds.
    def fold(summary, body):
        return '<details class="disclosure"><summary>' + text(summary, 'span') + '</summary><div class="disclosure-body">' + body + '</div></details>'
    chain = '<main class="paper guide-paper band-page chain-page" id="main">' + language_controls
    chain += text(ch['title'], 'h1') + '<div class="key-card">' + text(ch['key']) + '</div>'
    chain += text(ch['lead'], 'p', 'class="guide-lead"')
    chain += on_this_page([(label, anchor) for label, anchor in ch['toc']])
    chain += '<section id="layers">' + text(ch['layers_title'], 'h2') + text(ch['layers_answer'], 'p', 'class="answer"')
    chain += '<ol class="layer-list">' + ''.join('<li>' + '<h3>' + g + text(name, 'span') + '</h3>' + text(what) + '<p class="layer-who">' + text(ch['layers_who'], 'strong') + ' ' + text(who, 'span') + '</p></li>'
                                                for g, (name, what, who) in zip(glyphs, ch['layers'])) + '</ol>'
    chain += text(ch['layers_why'])
    chain += fold(ch['glossary_title'], '<dl class="glossary">' + ''.join(text(term, 'dt') + text(meaning, 'dd') for term, meaning in ch['glossary']) + '</dl>')
    chain += fold(ch['sources_title'],
                  chain_source(('As notas técnicas da Arc (em inglês)', 'Arc’s technical notes (in English)'), 'https://docs.arc.io/arc/concepts/system-overview.md',
                               ('Diz que os recursos de privacidade ainda vão chegar.', 'Says privacy features are still to come.'))
                  + chain_source(('Seus direitos pela lei brasileira de proteção de dados (LGPD)', 'Your rights under Brazil’s data protection law (LGPD)'), 'https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm',
                                 ('Seus direitos sobre seus dados pessoais, inclusive o de pedir que sejam apagados.', 'Your rights over your personal data, including deletion.'))) + '</section>'
    chain += '<section id="request">' + text(ch['request_title'], 'h2') + text(ch['request_answer'], 'p', 'class="answer"')
    chain += ledger_flow_html(text, ch['request_steps'])  # the drawing replaces the step strip (owner, 28 Oct)
    chain += fold(ch['request_fold'], text(ch['request_fold_body'])
                  + '<p>' + text(ch['request_more'], 'a', 'href="governance.html"') + '</p>'
                  + '<p>' + text(ch['whitepaper_link'], 'a', f'href="{esc(guide["sources"]["digital"]["url"])}"') + '</p>') + '</section>'
    chain += '<section id="records">' + text(ch['records_title'], 'h2')
    chain += '<div class="guide-table"><table><thead><tr>' + ''.join(text(h, 'th', 'scope="col"') for h in ch['records_head']) + '</tr></thead><tbody>'
    chain += ''.join('<tr>' + text(r[0], 'th', 'scope="row"') + ''.join(text(c, 'td') for c in r[1:]) + '</tr>' for r in ch['records']) + '</tbody></table></div></section>'
    # the token as its own section (owner, 28 Oct). Owner, 29 Oct: "keep overview low in information and high in read
    # quality … turn the four V's into a matrix, which is an animation". One answer line, a 2x2 matrix (a drawing,
    # the word, one line, "More info" holding the approved paragraph), then one fold for the launch and commitments.
    v_glyphs = [
        # Volume: a trade drops a coin into the next house
        '<svg class="v-glyph" viewBox="0 0 64 64" aria-hidden="true"><path class="vg-arrow" d="M8 18h22m-6-6 6 6-6 6M40 30H18m6-6-6 6 6 6"/>'
        '<path class="vg-house" d="M34 58V42l12-9 12 9v16Z"/><circle class="vg-coin" cx="46" cy="48" r="5"/></svg>',
        # Voting: a ballot slides into the box
        '<svg class="v-glyph" viewBox="0 0 64 64" aria-hidden="true"><path class="vg-box" d="M12 34h40v22H12Z M24 34v-2h16v2"/>'
        '<path class="vg-ballot" d="M25 14h14v24H25Z M28.5 24l3 3 5-6"/></svg>',
        # Verify: the ledger's blocks, and a lens passes over them
        '<svg class="v-glyph" viewBox="0 0 64 64" aria-hidden="true"><path class="vg-box" d="M6 40h14v12H6Z M25 40h14v12H25Z M44 40h14v12H44Z"/>'
        '<g class="vg-lens"><circle cx="20" cy="22" r="9"/><path d="M26.5 28.5 34 36"/></g></svg>',
        # Vow: a lock with a clock arc that fills over the set period
        '<svg class="v-glyph" viewBox="0 0 64 64" aria-hidden="true"><circle class="vg-ring" cx="32" cy="32" r="22"/>'
        '<circle class="vg-arc" cx="32" cy="32" r="22" pathLength="100"/><path class="vg-lockbody" d="M25 32h14v12H25Z"/>'
        '<path class="vg-shackle" d="M28 32v-4a4 4 0 0 1 8 0v4"/></svg>']
    ax = ch['matrix_axes']
    def v_cell(i):
        # Owner, 29 Oct: the whole card opens; a visible 'More info' link drops the detail down (no separate icon, no corner +).
        g, o, short = v_glyphs[i], ch['bridge'][i], ch['bridge_short'][i]
        return ('<details class="v-cell"><summary>' + g
                + text((o[0][0].rstrip('.'), o[0][1].rstrip('.')), 'span', 'class="v-title"')
                + text(short, 'span', 'class="v-line"') + text(ch['more_info'], 'span', 'class="v-link"') + '</summary>'
                + '<div class="v-body">' + text(o[1]) + text(ch['bridge_more'][i]) + '</div></details>')
    # Decision 33 (owner, 29 Oct, after Codex and DeepSeek): the loop is the one drawing; Volume, Voting and Verify are
    # plain lines with More info; Vow waits in the fold until a lock has a purpose.
    def v_line(i):
        o, short = ch['bridge'][i], ch['bridge_short'][i]
        # Owner, 31 Oct: the surface stays simple; the detail behind each function is in the whitepaper, section 8.
        return ('<div class="v-line-item">' + text((o[0][0].rstrip('.'), o[0][1].rstrip('.')), 'span', 'class="v-title"')
                + text(short, 'span', 'class="v-line"') + '</div>')
    cells = v_line(0) + v_line(1) + v_line(2)
    # The token's loop (owner, 29 Oct: "you can make such animation"). It starts with backing (owner, 1 Nov: the token
    # works like crowdfunding; see TOKEN_POSITION.md). The drawing is for sighted readers; the list carries the meaning.
    def loop_figure():
        cx, cy, r = 320, 190, 140
        steps = ch['loop_steps']
        angles = [-90, -18, 54, 126, 198]
        pt = lambda deg: (cx + r * math.cos(math.radians(deg)), cy + r * math.sin(math.radians(deg)))
        arcs, nodes, labels = '', '', ''
        anchors = [('middle', 0, -44), ('start', 40, 6), ('start', 34, 40), ('end', -34, 40), ('end', -40, 6)]
        for i, deg in enumerate(angles):
            nxt = angles[(i + 1) % 5] + (360 if i == 4 else 0)
            x1, y1 = pt(deg + 14); x2, y2 = pt(nxt - 14)
            arcs += f'<path class="loop-arc" style="--i:{i}" pathLength="1" marker-end="url(#loop-head)" d="M{x1:.1f},{y1:.1f} A{r},{r} 0 0 1 {x2:.1f},{y2:.1f}"/>'
            x, y = pt(deg)
            nodes += f'<circle class="loop-node{" loop-start" if i == 0 else ""}" style="--i:{i}" cx="{x:.1f}" cy="{y:.1f}" r="22"/>'
            anc, dx, dy = anchors[i]
            pair = steps[i][0]
            nl_ = NL_LOOKUP.get(pair[1], pair[1])
            labels += (f'<text class="loop-label" style="--i:{i}" x="{x + dx:.1f}" y="{y + dy:.1f}" text-anchor="{anc}" data-pt="{esc(pair[0])}" data-en="{esc(pair[1])}" data-nl="{esc(nl_)}">{esc(pair[0])}</text>')
        svg = ('<svg class="loop-svg" viewBox="0 -30 640 420" aria-hidden="true"><defs><marker id="loop-head" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
               '<path d="M0,0 L10,5 L0,10 Z" class="loop-headpath"/></marker></defs>'
               + f'<circle class="loop-track" cx="{cx}" cy="{cy}" r="{r}"/>' + arcs + nodes + labels
               + f'<circle class="loop-dot" r="7"><animateMotion dur="5s" repeatCount="2" fill="freeze" begin="indefinite" rotate="auto" path="M{cx},{cy - r} A{r},{r} 0 0 1 {cx},{cy + r} A{r},{r} 0 0 1 {cx},{cy - r}"/></circle></svg>')
        steps_list = '<ol class="loop-steps">' + ''.join('<li>' + text(st[0], 'strong') + ' ' + text(st[1], 'span') + '</li>' for st in steps) + '</ol>'
        return '<figure class="token-loop">' + svg + steps_list + '</figure>'

    # Owner, 1 Nov: the token has its own page, 'The self-compounding token'; the ledger keeps a short summary and the loop.
    LOOP_JS = ('<script>document.addEventListener("DOMContentLoaded",function(){var l=document.querySelector(".token-loop");'
                'if(!l||!("IntersectionObserver" in window)||matchMedia("(prefers-reduced-motion: reduce)").matches)return;l.classList.add("js-loop");'
                'new IntersectionObserver(function(e,o){e.forEach(function(x){if(x.isIntersecting){l.classList.add("is-looping");'
                'var a=l.querySelector("animateMotion");setTimeout(function(){try{a.beginElement()}catch(_){}} ,2200);o.disconnect();}});},{threshold:.35}).observe(l);});</script>')
    chain += ('<section id="token">' + text(ch['token_fold'], 'h2')
              + text(TK['ledger_answer'], 'p', 'class="answer"') + text(housing_membership) + loop_figure() + text(TK['vote_rule'])
              + '<p>' + text(TK['ledger_link'], 'a', 'class="button act" href="token.html"') + '</p>' + LOOP_JS + '</section>')
    chain += '<section id="open">' + text(ch['open_title'], 'h2')
    chain += text(ch['open_runs_title'], 'h3') + '<ol class="path-list">' + ''.join(text(o, 'li') for o in ch['open_runs']) + '</ol>'
    chain += '<div class="window">' + text(ch['same_title'], 'h3') + '<ul>' + ''.join(text(o, 'li') for o in ch['same']) + '</ul></div>'
    # Owner, 31 Oct: what a blockchain can't do stays as one line; the Arc and USDC risks and their sources are in the whitepaper, section 12.
    chain += ('<span id="limits"></span>' + text(('A Arc é nova, e o USDC pode ser bloqueado pela empresa que o emite.',
                                                  'Arc is new, and USDC can be frozen by the company that issues it.'))
              + '<p>' + text(('Esses riscos em detalhe (whitepaper, seção 12, em inglês)', 'These risks in full (whitepaper, section 12)'), 'a', 'href="whitepaper.html#12-risks-and-what-still-needs-checking"') + '</p></section>')
    chain += '<section class="closing-band" id="help">' + text(ch['closing']) + text(ch['button'], 'a', 'class="button act" href="contact.html"') + '</section>'
    chain += partner_line('blockchain.html') + '</main>'
    # Jargon popups (owner, 28 Oct): the meanings travel inside the page; terms.js runs after site.js.
    terms_data = json.dumps(json.loads((root / 'terms.json').read_text()), ensure_ascii=False).replace('</', '<\\/')
    terms_script = ('<script type="application/json" id="imobx-terms">' + terms_data + '</script>'
                    '<script src="assets/site.js" defer></script>' + f'<script src="{asset_v("terms.js")}" defer></script>')
    (root / 'blockchain.html').write_text(page('IMOBX | Distributed ledger', chain, f'<link rel="stylesheet" href="{asset_v("flow.css")}"><link rel="stylesheet" href="{asset_v("bands.css")}">' + MF_SCRIPT + terms_script,
        version=guide['version'], lang='pt-BR', title_pt='IMOBX | Registro distribuído'))

    # 'The self-compounding token' (owner, 1 Nov): what self-compounding means (fees work like a not-for-profit's income,
    # highest priorities first), how the token reaches people, what a US$100 trade pays for (animated bar), the price,
    # a token sale, the three laws, use, the families and the risks. Venue facts: Arctide 14% + its own 0.25%.
    segs = [('seg-wages', 6.30, TK['row_wages']), ('seg-houses', 3.675, TK['row_houses']), ('seg-pool', 1.225, TK['row_pool']),
            ('seg-lock', 2.80, TK['row_lock'])]
    total = sum(v for _, v, _ in segs)
    bar = ('<figure class="fee-bar"><div class="fee-track" aria-hidden="true">'
           + ''.join(f'<span class="fee-seg {c}" style="--w:{v / total * 100:.1f}%;--d:{i * 0.25:.2f}s"></span>' for i, (c, v, _) in enumerate(segs))
           + '</div><table class="fee-table"><tbody>'
           + ''.join('<tr><th scope="row"><span class="fee-key ' + c + '"></span>' + text(lab, 'span') + '</th>' + text(('US$ ' + f'{v:.2f}'.replace('.', ','), 'US$' + f'{v:.2f}'), 'td') + '</tr>' for c, v, lab in segs)
           + '<tr class="fee-total">' + text(TK['row_total'], 'th', 'scope="row"') + text(('US$ ' + f'{total:.2f}'.replace('.', ','), 'US$' + f'{total:.2f}'), 'td') + '</tr></tbody></table></figure>')
    FEE_JS = ('<script>document.addEventListener("DOMContentLoaded",function(){var f=document.querySelector(".fee-bar");'
              'if(!f||!("IntersectionObserver" in window)||matchMedia("(prefers-reduced-motion: reduce)").matches)return;f.classList.add("js-fee");'
              'new IntersectionObserver(function(e,o){e.forEach(function(x){if(x.isIntersecting){f.classList.add("is-flowing");o.disconnect();}});},{threshold:.4}).observe(f);});</script>')
    tk = '<main class="paper guide-paper token-page band-page" id="main">' + text(TK['title'], 'h1')
    tk += text(TK['lead'], 'p', 'class="guide-lead"')
    tk += on_this_page([(l, a) for l, a in TK['toc']])
    tk += ('<section id="use">' + text(TK['use_h'], 'h2') + text(TK['use'], 'p', 'class="answer"') + text(TK['use_more']) + text(TK['use2']) + '</section>')
    tk += '<section id="meaning">' + text(TK['meaning_h'], 'h2') + text(TK['meaning'], 'p', 'class="answer"') + loop_figure() + '</section>'
    tk += '<section id="fee">' + text(TK['fee_h'], 'h2') + text(TK['fee'], 'p', 'class="answer"') + bar + text(TK['fee2']) + '</section>'
    cmp = ('<div class="guide-table"><table class="cmp-table"><thead><tr>' + ''.join(text(h_, 'th', 'scope="col"') for h_ in TK['cmp_head']) + '</tr></thead><tbody>'
           + ''.join('<tr>' + text(r_[0], 'th', 'scope="row"') + text(r_[1], 'td') + text(r_[2], 'td') + '</tr>' for r_ in TK['cmp']) + '</tbody></table></div>')
    tk += '<section id="sale">' + text(TK['sale_h'], 'h2') + text(TK['sale'], 'p', 'class="answer"') + cmp + text(TK['supply']) + '</section>'
    VX = {'h': ('Quais quatro regras orientam os recursos da comunidade?', 'Which four rules govern the community’s funding?'), 'intro': ('Sempre que pessoas juntam recursos, surgem as mesmas quatro perguntas, uma para cada regra abaixo. A IMOBX responde com quatro regras, os quatro V: Volume, Voto, Verificação e Vínculo. Elas são a razão de ser do token e valem para todos os recursos da comunidade.', 'Whenever people pool funding, the same four questions come up, one for each rule below. IMOBX answers them with four rules, the four V’s: Volume, Vote, Verify and Vow. They are what the token is for, and they apply to all of the community’s funding.'), 'cols': [('Recursos e informação', 'Resources and information'), ('Pessoas e autoridade', 'People and authority')], 'rows': [('Operação', 'Operation'), ('Prestação de contas e proteção', 'Accountability and protection')], 'more': ('Mais informações', 'More info'), 'cells': {'volume': (('Volume', 'Volume'), ('Como a comunidade gera e distribui recursos?', 'How does the community generate and allocate resources?'), ('A renda sustenta as casas, o trabalho, a manutenção e as reservas, dentro de um orçamento que os membros aprovam.', 'Income supports the houses, the work, maintenance and reserves, under a budget the members agree.'), ('O pagamento de cada família cobre primeiro o que já está comprometido: a obra, a manutenção e um possível pagamento de saída. Salários, novas casas e reservas saem do que sobra, dentro do orçamento dos membros, e a taxa do token se soma a isso.', 'Each family’s payment first covers what it is already committed to: building, maintenance and a possible exit payment. Wages, new houses and reserves come from what is left, under the members’ budget, and the token’s fee adds to that.'), ('Para onde vai a taxa', 'Where the fee goes'), '#fee'), 'vote': (('Voto', 'Vote'), ('Como as pessoas decidem e agem juntas?', 'How do people make decisions and act together?'), ('Os membros decidem sobre moradia e assuntos comuns, um membro, um voto, dentro de poderes definidos.', 'Members decide housing and shared matters, one member, one vote, within defined powers.'), ('Tokens, registros de contribuição e tempo online não aumentam o voto de ninguém sobre moradia. Os moradores decidem juntos como os espaços comuns são usados, e cada decisão vai para a ata da reunião em que foi tomada.', 'Token holdings, contribution records and time spent online add nothing to anyone’s vote on housing. Residents decide together how the shared spaces are used, and every decision goes into the minutes of the meeting where it was made.'), ('Governança local', 'Local governance'), 'governance.html'), 'verify': (('Verificação', 'Verify'), ('Como registros, decisões e resultados podem ser conferidos?', 'How can records, decisions and results be checked?'), ('Registros e conferências independentes permitem prestar contas das finanças e das decisões, protegendo os dados pessoais.', 'Records and independent checks keep finances and decisions accountable, while personal information stays protected.'), ('As contas da comunidade podem ser conferidas de forma independente, e os dados pessoais ficam protegidos. Um registro mostra que um pagamento foi feito; conferências independentes e os documentos de apoio mostram se o trabalho foi feito, e no plano os membros podem contestar um pagamento.', 'The community’s accounts can be checked independently, and personal information stays protected. A record shows that a payment was made; independent checks and the supporting documents show whether the work was done, and in the plan members can challenge a payment.'), ('Registro distribuído', 'Distributed ledger'), 'blockchain.html'), 'vow': (('Vínculo', 'Vow'), ('Que direitos, compromissos e limites ao poder precisam ser protegidos?', 'What rights, commitments and limits on authority must be protected?'), ('Compromissos protegem os direitos dos moradores, os bens comuns, uma entrada e uma saída justas, e as regras de como um compromisso pode mudar.', 'Commitments protect residents’ rights, shared assets, a fair way in and out, and the rules for how a commitment can change.'), ('O contrato de cada família vem primeiro. Uma votação não pode mudar o contrato de moradia de uma família: só a família e a IMOBX juntas podem, dentro da lei brasileira. No plano, o contrato também diz o que acontece se a família sair antes do prazo, e como um compromisso pode mudar quando algo precisa ser consertado ou substituído. As partes comuns da vila, como o pátio, a caixa d’água e as salas de estudo, são pagas uma vez por todas as casas e continuam sendo de todos.', 'Each family’s agreement comes first. A vote can’t change a family’s housing agreement: only the family and IMOBX together can, under Brazilian law. In the plan, the agreement also says what happens if the family leaves early, and how a commitment can change when something must be repaired or replaced. The shared parts of the village, such as the courtyard, the water tank and the study rooms, are paid for once by all the houses and stay shared.'), ('Saída e atrasos', 'Leaving or falling behind'), 'rent-to-own.html#leaving')}}
    def vx_cell(key, i):
        t_, q_, line_, more_, lab_, href_ = VX['cells'][key]
        return ('<details class="vx-cell vx-' + key + '" style="--i:' + str(i) + '"><summary>' + text(t_, 'span', 'class="vx-title"')
                + text(q_, 'span', 'class="vx-q"') + text(line_, 'span', 'class="vx-line"') + text(VX['more'], 'span', 'class="vx-more"') + '</summary>'
                + '<div class="vx-body">' + text(more_) + '<p>' + text(lab_, 'a', 'href="' + href_ + '"') + '</p></div></details>')
    vx = ('<figure class="vx-matrix"><div class="vx-grid">'
          + '<span class="vx-corner" aria-hidden="true"></span>' + text(VX['cols'][0], 'span', 'class="vx-col"') + text(VX['cols'][1], 'span', 'class="vx-col"')
          + text(VX['rows'][0], 'span', 'class="vx-row"') + vx_cell('volume', 0) + vx_cell('vote', 1)
          + text(VX['rows'][1], 'span', 'class="vx-row"') + vx_cell('verify', 2) + vx_cell('vow', 3)
          + '</div></figure>')
    VX_JS = ('<script>document.addEventListener("DOMContentLoaded",function(){var m=document.querySelector(".vx-matrix");'
             'if(!m||!("IntersectionObserver" in window)||matchMedia("(prefers-reduced-motion: reduce)").matches)return;m.classList.add("js-vx");'
             'new IntersectionObserver(function(e,o){e.forEach(function(x){if(x.isIntersecting){m.classList.add("is-flowing");o.disconnect();}});},{threshold:.3}).observe(m);});</script>')
    tk += '<section id="laws">' + text(VX['h'], 'h2') + text(VX['intro']) + vx + '</section>'
    tk += '<section id="notice" class="token-notice">' + text(TK['notice_h'], 'h2') + '<ul>' + ''.join(text(n_, 'li') for n_ in TK['notice']) + '</ul></section>'
    tk += ('<section class="closing-band" id="help">' + '<p>' + text(TK['closing_link'], 'a', 'href="blockchain.html"') + '</p>' + text(TK['closing'])
           + text(TK['closing_btn'], 'a', 'class="button act" href="https://t.me/+n-42pfkXna5mNzRk"') + '</section>')
    tk += LOOP_JS + FEE_JS + VX_JS + partner_line('token.html') + '</main>'
    (root / 'token.html').write_text(page('IMOBX | Self-compounding', tk, '<script>if("IntersectionObserver" in window&&!matchMedia("(prefers-reduced-motion: reduce)").matches)document.documentElement.classList.add("fee-ready")</script>' + f'<link rel="stylesheet" href="{asset_v("flow.css")}"><link rel="stylesheet" href="{asset_v("bands.css")}">' + terms_script,
        version=guide['version'], lang='pt-BR', title_pt='IMOBX | Self-compounding'))

    stub_targets = {item['id']: ('rent-to-own.html' if item['id'] in HOUSEHOLD_FAQ else 'transparency.html')
                    for item in guide['questions']}
    stub_targets.update({'thanks-zeal-lets': 'transparency.html', 'euler': 'transparency.html'})
    (root / 'faq.html').write_text(redirect_stub(
        'IMOBX | Perguntas sobre o modelo', 'Perguntas sobre o modelo', 'rent-to-own.html#questions',
        'Open the current version', per_question=stub_targets))

    # The homepage is built whole by home_page.py (owner-approved mock, 26 Oct 2026); its three phases live on the roadmap.
