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
        ('A IMOBX é uma proposta em preparação no Rio de Janeiro. Nada está à venda nem para alugar, e nenhuma casa está sendo oferecida.',
         'IMOBX is a proposal being prepared in Rio de Janeiro. Nothing is for sale or rent, and no house is on offer.'),
        ('A IMOBX ainda não tem forma jurídica. Ela está sendo escolhida com assessores brasileiros.',
         'IMOBX has no legal form yet. It is being chosen with Brazilian advisers.'),
        ('Nenhum contrato foi assinado: nem com famílias, nem com construtoras, proprietários ou financiadores.',
         'No contract has been signed: not with families, builders, owners or funders.'),
        ('Nenhum órgão regulador aprovou nada, e o site não afirma ter nenhuma aprovação.',
         'No regulator has approved anything, and the site claims no approval.'),
        (('O plano completo e as suas etapas: ', 'The full plan and its stages: '), ('Etapas do projeto', 'Project stages'), '#stages'),
    ]),
    (('Casas e famílias', 'Houses and families'), [
        ('Os desenhos e as fotos mostram a proposta. Não são anúncios de casas disponíveis, e o modelo dos lofts é um estudo de projeto.',
         'The drawings and photos show the proposal. They are not listings of available houses, and the lofts model is a design study.'),
        ('O preço, o valor mensal, o prazo e quem pode participar são definidos para cada projeto, num contrato escrito, antes de qualquer mudança.',
         'The price, the monthly amount, the term and who can join are set for each project, in a written agreement, before anyone moves in.'),
        ('Devolução, prazo de tolerância ou desconto só valem quando estiverem escritos nesse contrato.',
         'A refund, grace period or discount applies only once it is written into that agreement.'),
        ('Entrar no grupo do Telegram, ou apresentar um imóvel, um serviço ou a si mesmo, não confirma nenhum acordo, nenhum trabalho e nenhuma casa reservada.',
         'Joining the Telegram group, or introducing a property, a service or yourself, confirms no agreement, no job and no reserved house.'),
    ]),
    (('Recursos', 'Funding'), [
        ('Os recursos viriam de doações, editais e investimento, na medida em que a forma jurídica escolhida permitir.',
         'The funding would come from donations, grants and investment, as far as the chosen legal form allows.'),
        ('Investimento só é oferecido por um caminho legal e com direitos escritos. Nenhum retorno é prometido.',
         'Investment is offered only through a lawful route and with written rights. No return is promised.'),
        ('As contas da obra são pagas com recursos já garantidos.', 'Building bills are paid with funding already secured.'),
    ]),
    (('Leis e conferências', 'Law and checks'), [
        ('O cadastro fiscal (Receita Federal), o momento em que a propriedade passa a outra pessoa (Código Civil) e as regras para parcerias com o poder público (Lei 13.019) fazem parte do trabalho jurídico em andamento.',
         'Tax registration (Receita Federal), when ownership passes (Civil Code), and the rules for partnerships with public bodies (Law 13.019) are part of the legal work under way.'),
        ('Um advogado confere as regras antes de qualquer pagamento passar por uma blockchain.',
         'A lawyer checks the rules before any payment runs on a blockchain.'),
        ('As revisões jurídica e de segurança ainda vão ser feitas.', 'Legal and security reviews are still to come.'),
    ]),
    (('Pessoas', 'People'), [
        ('Os direitos e deveres de cada pessoa dependem de contratos assinados e de registros oficiais. Hoje, os deveres formais dos fundadores ainda não estão escritos.',
         'Each person’s rights and duties depend on signed agreements and official records. Today, the founders’ formal duties are not yet written down.'),
    ]),
    (('O grupo do Telegram', 'The Telegram group'), [
        ('O grupo da IMOBX é aberto: todos nele veem o que você publica. Não inclua telefone, endereço nem documentos. As orientações completas estão na mensagem de boas-vindas do grupo.',
         'The IMOBX group is open: everyone in it sees what you post. Leave out phone numbers, addresses and documents. The detailed guidance is in the group’s welcome message.'),
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
        'settlement': ('Fluxo reais ↔ moeda digital', 'Reais ↔ digital currency flow'),
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
        'charter': ('Mostra quem decidiria o quê. As regras ainda não estão decididas.',
                    'Shows who would decide what. The rules are not decided yet.'),
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
    roadmap += text(('Etapas do projeto: onde estamos e o que vem depois', 'Project stages: where we are and what comes next'), 'h1')
    roadmap += '<div class="key-card" id="where-we-stand">' + text(('Estamos preparando o primeiro projeto no Rio de Janeiro. As datas vêm quando a forma jurídica e o primeiro imóvel estiverem confirmados.',
                     'We are preparing the first project in Rio de Janeiro. Dates follow once the legal form and the first property are confirmed.')) + '</div>'
    # The owner's why (founders' chat, 24 Oct 2026), then who is preparing it (owner, 29 Oct).
    roadmap += text(('Por que construir um lar? Todo mundo entende o que isso significa. É uma necessidade profundamente emocional, psicológica, espiritual e sagrada.',
                     'Why build a home? Everybody understands what that means. It is a need that is deeply emotional, psychological, spiritual and sacred.'), 'p', 'class="guide-lead"')
    roadmap += '<p class="prepared-by">' + text(('Preparado por Rafael Britto, fundador e construtor no Rio de Janeiro, e John, comunicação e ferramentas digitais.',
                                                'Prepared by Rafael Britto, founder and builder in Rio de Janeiro, and John, communication and digital tools.'), 'span') + '</p>'
    roadmap += on_this_page([(('Como planejamos', 'How we plan'), 'method'), (('Etapas', 'Stages'), 'stages'), (('Os imóveis', 'The properties'), 'cases'),
                             (('A vila e os lofts', 'The village and the lofts'), 'village'), (('Fotos da obra', 'Building photos'), 'building'), (TERMS_TITLE, 'terms')])

    # How we plan (owner, 29 Oct): the design-thinking method shown openly, with where we are now. Being open about the
    # method invites the cooperation the project aims for. Double Diamond: understand, define, try, test; tests can send
    # us back. The drawing draws itself once when it comes into view; with reduced motion it is shown complete.
    roadmap += '<section id="method">' + text(('Como planejamos?', 'How do we work out the plan?'), 'h2')
    roadmap += text(('Planejamos às claras, com um método que designers usam: primeiro entender o problema com quem vive nele, depois defini-lo, depois experimentar soluções e testá-las. Cada teste pode nos fazer voltar um passo. Ver em que ponto estamos ajuda você a entrar na hora certa.',
                     'We plan in the open, with a method designers use: first understand the problem with the people who live it, then define it, then try solutions and test them. Each test can send us back a step. Seeing where we are helps you join at the right moment.'), 'p', 'class="answer"')
    def svg_t(x, y, pair, cls=''):
        nl_ = NL_LOOKUP.get(pair[1], pair[1])
        return (f'<text x="{x}" y="{y}" text-anchor="middle" class="{cls}" data-pt="{esc(pair[0])}" data-en="{esc(pair[1])}" data-nl="{esc(nl_)}">'
                f'{esc(pair[0])}</text>')
    roadmap += ('<figure class="method-figure"><svg class="method-diamond" viewBox="0 -14 680 270" role="img" aria-labelledby="method-title">'
                + '<title id="method-title">' + esc('Duplo diamante: entender, definir, experimentar, testar. Estamos em: definir.') + '</title>'
                + '<polygon class="dd-line" points="20,110 170,30 320,110 170,190" pathLength="1"/>'
                + '<polygon class="dd-line dd-second" points="360,110 510,30 660,110 510,190" pathLength="1"/>'
                + '<line class="dd-join" x1="320" y1="110" x2="360" y2="110"/>'
                + '<path class="dd-back" d="M640,168 C560,232 160,232 40,168" pathLength="1"/>'
                + svg_t(95, 116, ('Entender', 'Understand'), 'dd-label') + svg_t(245, 116, ('Definir', 'Define'), 'dd-label dd-now')
                + svg_t(450, 116, ('Experimentar', 'Try'), 'dd-label') + svg_t(585, 116, ('Testar', 'Test'), 'dd-label')
                + '<line class="dd-pointer" x1="245" y1="6" x2="245" y2="86"/><circle class="dd-marker" cx="245" cy="92" r="7"/>'
                + svg_t(245, 0, ('Estamos aqui', 'We are here'), 'dd-here')
                + svg_t(340, 248, ('Cada teste pode nos fazer voltar', 'Each test can send us back'), 'dd-note')
                + '</svg><figcaption>' + text(('Hoje estamos definindo: a forma jurídica, as regras com os moradores, um teste de pagamentos e os recursos para o que prometemos.',
                                               'Today we are defining: the legal form, the rules with residents, a test of payments, and funding for what we have promised.'), 'span')
                + '</figcaption></figure></section>')

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
    roadmap += '<section id="stages">' + text(('O que acontece agora e o que vem depois?', 'What happens now, and what comes next?'), 'h2')
    roadmap += text(('Agora, quatro frentes de preparação ao mesmo tempo. Depois, três etapas, uma de cada vez: primeiras casas, mais bairros e uma plataforma para proprietários.',
                     'Now, four kinds of preparation at once. Then three stages, one after another: first houses, more neighbourhoods, and a platform for owners.'), 'p', 'class="answer"')
    roadmap += '<div class="path"><div class="path-line" aria-hidden="true"><span class="path-fill"></span></div>'
    for label, ordered, members in grouped_stages():
        roadmap += '<div class="path-group' + ('' if ordered else ' path-now') + '">'
        roadmap += '<p class="path-group-label">' + ('' if ordered else '<span class="path-here">' + text(('Estamos aqui', 'We are here'), 'span') + '</span>') + text(label, 'span') + '</p>'
        roadmap += '<ol class="path-steps' + (' path-tracks' if not ordered else '') + '">'
        for number, stage in members:
            roadmap += f'<li class="path-step"><span class="path-dot" aria-hidden="true"></span>{icon(stage["id"])}'
            roadmap += f'<details class="roadmap-stage" id="{esc(stage["id"])}"><summary>'
            roadmap += text(numbered(number, stage['title']) if number else stage['title'], 'h3')
            if stage.get('window'):
                roadmap += text(stage['window'], 'span', 'class="guide-window"')
            roadmap += '<span class="stage-toggle">' + text(('Mostrar detalhes', 'Show details'), 'span', 'class="more"') + text(('Esconder detalhes', 'Hide details'), 'span', 'class="less"') + '</span></summary>'
            roadmap += ''.join(text(pair) for pair in stage['card']) + '</details></li>'
        roadmap += '</ol></div>'
    roadmap += '<p class="path-condition">' + text(('O token vem só depois que a organização jurídica existir e as primeiras casas mostrarem um negócio que funciona.',
                                                   'The token comes only after the legal organisation exists and the first rent-to-own properties show a working business.'), 'span') + ' '
    roadmap += text(('Seja qual for o resultado de uma votação, só a família e a IMOBX juntas, dentro da lei, podem mudar o contrato de moradia de uma família.',
                     'Whatever a vote decides, only the family and IMOBX together, under the law, can change a family’s housing agreement.'), 'span') + '</p>'
    roadmap += '</div></section>'

    cases = guide['cases']
    # The answer first (no pilot is confirmed), then what a proposed and a confirmed pilot mean.
    intro_lines = tuple(t.rsplit('. ', 1) for t in cases['intro'])
    roadmap += '<section id="cases">' + text(('Quais imóveis são candidatos para o nosso primeiro morador em aluguel com compra?', 'Which properties are candidates for our first rent-to-own tenant?'), 'h2')
    roadmap += text(tuple(t[1] for t in intro_lines), 'p', 'class="answer"') + text(tuple(t[0] + '.' for t in intro_lines))
    roadmap += '<div class="guide-table"><table><thead><tr>' + ''.join(text(h, 'th', 'scope="col"') for h in cases['headings'])
    roadmap += '</tr></thead><tbody>' + ''.join('<tr>' + text(r[0], 'th', 'scope="row"') + text(r[1], 'td') + text(r[2], 'td') + '</tr>'
                                              for r in cases['rows']) + '</tbody></table></div>'
    # 'Who takes part' (the eight groups) moves to Take part (review B 80-108); its old anchors stay so links still land here.
    roadmap += '<span id="participation"></span>' + ''.join(f'<span id="role-{role["id"]}"></span>' for role in guide['participation']['roles'])
    roadmap += text(('Como funciona o aluguel com compra para uma família', 'How rent-to-own works for a family'), 'a', 'href="rent-to-own.html"') + '</section>'

    # Where it leads, and the builder's work (owner, 28-29 Oct): the biggest section sits at the bottom, clearly the builder's.
    roadmap += '<section id="village">' + text(('Como poderia ser a primeira vila?', 'What could the first village look like?'), 'h2')
    roadmap += text(('Rafael planejou a primeira vila com casas de 45 m² em volta de um pátio comum, com energia solar, um pomar e lugares para brincar e estudar.',
                     'Rafael planned the first village as 45 m² houses around a shared courtyard, with solar power, an orchard and places to play and study.'))
    roadmap += '<div class="lead-figures"><figure class="lead-figure"><img src="assets/homepage.jpg" width="1024" height="765" loading="lazy" alt="Ilustração conceitual da primeira vila" data-alt-pt="Ilustração conceitual da primeira vila" data-alt-en="Concept illustration of the first village" data-alt-nl="Conceptillustratie van het eerste dorp">'
    roadmap += '<figcaption>' + text(('Ilustração conceitual da primeira vila, feita com um gerador de imagens.', 'Concept illustration of the first village, made with an image generator.'), 'span') + '</figcaption></figure>'
    roadmap += '<figure class="lead-figure"><img src="assets/property-1.jpg" width="823" height="581" loading="lazy" alt="Os dois lofts, vista externa" data-alt-pt="Os dois lofts, vista externa" data-alt-en="The two lofts, exterior view" data-alt-nl="De twee lofts, buitenaanzicht">'
    roadmap += '<figcaption>' + text(('Os dois lofts: nossa equipe modelou estes lofts em janeiro de 2026. É um estudo de projeto.', 'The two lofts: our team modelled them in January 2026. It is a design study.'), 'span') + '</figcaption></figure></div></section>'
    roadmap += '<section id="building">' + text(('O que a construtora está fazendo?', 'What is the builder doing?'), 'h2')
    roadmap += text(('Em janeiro de 2026, a construtora do Rafael assinou um contrato para construir dois lofts, como um primeiro teste da ideia da IMOBX. A construtora prepara esses projetos e define a própria agenda.',
                     'In January 2026, Rafael’s construction company signed a contract to build two lofts, as a first test of the IMOBX idea. The company prepares these designs and sets its own schedule.'), 'p', 'class="answer"')
    # Owner, 29 Oct: the photos that look like the loft model and show it being built; the frame first and largest.
    photos = [('construction-timber-supplied.jpg', ('Pilares e paredes de blocos', 'Columns and block walls')), ('construction-concrete-supplied.jpg', ('Concreto', 'Concrete')),
              ('construction-formwork-supplied.jpg', ('Fôrmas', 'Formwork')), ('construction-roof-supplied.jpg', ('Telhado', 'Roof')),
              ('construction-solar-roof-supplied.jpg', ('Telhado solar', 'Solar roof'))]
    from PIL import Image as _Img
    dims = {f: _Img.open(root / 'assets' / f).size for f, _ in photos}  # width and height stop the page jumping as photos load
    roadmap += '<ul class="photo-strip">' + ''.join(
        f'<li><figure><img src="assets/{f}" width="{dims[f][0]}" height="{dims[f][1]}" loading="lazy" alt="{esc(cap[0])}" data-alt-pt="{esc(cap[0])}" data-alt-en="{esc(cap[1])}" data-alt-nl="{esc(NL_LOOKUP.get(cap[1], cap[1]))}"><figcaption>' + text(cap, 'span') + '</figcaption></figure></li>'
        for f, cap in photos) + '</ul>'
    roadmap += '<p>' + text(('Fotos do arquivo da nossa equipe. Ainda estamos confirmando onde e quando cada uma foi tirada. ', 'Photos from our team’s archive. We are still confirming where and when each one was taken. '), 'span')
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
                     + '<ul>' + ''.join(text(public['reporting'][i], 'li') for i in (0, 1, 2, 4)) + '</ul>' + text(public['reporting_note']) + '</section>')
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
    roadmap += text(('Parceiros e famílias precisam saber exatamente no que estão entrando, por isso listamos o que está decidido e o que ainda está em aberto.',
                     'Partners and families should know exactly what they are joining, so we list what is settled and what is still open.'))
    for heading, items in TERMS:  # owner, 28 Oct: the long list sits in folds so the page ends lighter
        roadmap += '<details class="disclosure"><summary>' + text(heading, 'span') + '</summary><div class="disclosure-body"><ul>'
        for item in items:
            if len(item) == 3:  # (lead-in, link label, anchor)
                roadmap += '<li>' + text(item[0], 'span') + text(item[1], 'a', f'href="{item[2]}"') + '.</li>'
            else:
                roadmap += text(item, 'li')
        roadmap += '</ul></div></details>'
    roadmap += '</section>'
    roadmap += '<section class="closing-band" id="help">' + text(('Definimos esses pontos com quem participa. Se você pode ajudar em algum deles, apresente-se no grupo.',
                                                                   'We settle these with the people who join us. If you can help with one of them, introduce yourself in the group.'))
    roadmap += text(('Apresente-se', 'Introduce yourself'), 'a', 'class="button act" href="contact.html"') + '</section>'
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
         ('Rafael Britto, fundador, com a equipe de construção que ele coordena.', 'Rafael Britto, founder, with the construction team he leads.'),
         ('A construtora nunca aprova a própria cobrança. Uma pessoa aprova, outra confere o serviço, e só então se paga.', 'The builder never approves its own invoice. One person approves, another checks the work, and only then is it paid.')],
        [('Comunicação, ferramentas digitais e o grupo', 'Communication, digital tools and the group'),
         ('John, comunicação e ferramentas digitais.', 'John, communication and digital tools.'),
         ('As mudanças no plano são publicadas neste site e no grupo.', 'Changes to the plan are published on this site and in the group.')],
        [('Divulgação, embaixadores e corretores', 'Promotion, ambassadors and brokers'),
         ('Os fundadores contratam cada tarefa, com uma pessoa responsável e um prazo.', 'The founders commission each task, with a person responsible and a deadline.'),
         ('No plano, cada tarefa é paga depois de conferida, e cada pagamento é publicado.', 'In the plan, each task is paid once it has been checked, and every payment is published.')],
        [('Forma jurídica, contratos e o plano geral', 'Legal form, contracts and the overall plan'),
         ('Os fundadores, com advogados e consultores no Brasil.', 'The founders, with lawyers and advisers in Brazil.'),
         ('Contratos com famílias e financiadores vêm depois que a forma jurídica estiver escolhida.', 'Agreements with families and funders come after the legal form is chosen.')],
    ]
    resident_rows = [
        [('Morar na casa e comprá-la', 'Living in the house and buying it'),
         ('A família e a IMOBX, conforme o contrato e a lei.', 'The family and IMOBX, under their agreement and the law.'),
         ('O contrato de cada família segue os termos que ela assinou, e a família pode pedir que qualquer decisão seja revista.', 'Each family’s agreement follows the terms it signed, and the family can ask for any decision to be reviewed.')],
        [('Uso de espaços e manutenção local', 'Shared spaces and local maintenance'),
         ('Os moradores juntos. Uma opção em discussão: um voto por membro.', 'The residents together. One option under discussion: one vote per member.'),
         ('Dentro do orçamento e das regras de segurança. Os moradores podem trocar seus representantes.', 'Within the budget and the safety rules. Residents can replace their representatives.')],
        [('Obras e compras', 'Building work and purchases'),
         ('Pessoas escolhidas pela experiência, para uma função e um prazo definidos.', 'People chosen for their experience, for a set job and a set time.'),
         ('Uma pessoa aprova, outra confere o serviço, e só então se paga.', 'One person approves, another checks the work, and only then is it paid.')],
    ]
    open_terms = [
        ('Qual imóvel o primeiro projeto vai usar.', 'Which property the first project will use.'),
        ('O preço, o pagamento mensal e quanto de cada pagamento conta para a compra.', 'The price, the monthly payment and how much of each payment counts towards buying the home.'),
        ('Quem paga os reparos, em quanto tempo são feitos e como contestar uma cobrança.', 'Who pays for repairs, how fast they are done and how to question a charge.'),
        ('Como os moradores votam, quanto se pode gastar sem consultar e como resolver uma discordância.',
         'How residents vote, how much can be spent without asking, and how disagreements are settled.'),
        ('A forma jurídica da organização.', 'The organisation’s legal form.'),
        ('O financiamento e o que receberia quem financiar o projeto.', 'The funding, and what people who fund the project would receive.'),
        ('O prestador do serviço de pagamento.', 'The payment provider.'),
        ('Quanto dos recursos passa pela blockchain: de só contas bancárias até cada pagamento e aprovação na Arc.',
         'How much of the funding runs on the blockchain: from bank accounts only to every payment and approval on Arc.'),
    ]
    groups = [(('A casa e o preço', 'The house and its price'), open_terms[0:3]), (('As regras', 'The rules'), open_terms[3:4]),
              (('Recursos e forma jurídica', 'Funding and legal form'), open_terms[4:8])]
    # What stays protected at every stage (owner, 29 Oct: the old placement was confusing): right after 'Who decides now?'.
    SAFEGUARDS_SECTION = ('<section id="safeguards">' + text(('O que fica protegido em todas as etapas?', 'What stays protected at every stage?'), 'h2')
        + text(('A casa de cada família é protegida pelo contrato que ela assinou. Seja qual for o resultado de uma votação, só a família e a IMOBX juntas, dentro da lei, podem mudar o contrato de moradia de uma família.',
                'Each family’s home is protected by the agreement it signed. Whatever a vote decides, only the family and IMOBX together, under the law, can change a family’s housing agreement.'), 'p', 'class="answer"')
        + text(('Cada pagamento precisa da aprovação de mais de uma pessoa identificada, e uma família pode pedir que qualquer decisão seja revista.',
                'Every payment needs more than one named person’s approval, and a family can ask for any decision to be reviewed.')) + '</section>')
    gov = '<main class="paper guide-paper band-page governance-page" id="main">' + language_controls
    gov += text(('Quem decide, e quando você tem voz?', 'Who decides, and when do you get a say?'), 'h1')
    gov += text(('A IMOBX está em preparação, então hoje uma pequena equipe toma as decisões. À medida que o projeto cresce, mais pessoas ganham voz, em três etapas:',
                 'IMOBX is in preparation, so today a small team makes the decisions. As the project grows, more people get a say, in three stages:'), 'p', 'class="guide-lead"')
    gov += gov_flow_html(text)  # owner, 29 Oct ('go'): the stages as one drawing; owner: every heading gets a line or two
    gov += on_this_page([(('Agora', 'Now'), 'now'), (('Proteções', 'Protections'), 'safeguards'), (('O token', 'The token'), 'token-rules'), (('Os moradores', 'Residents'), 'residents'),
                         (('O que estamos decidindo', 'What we are deciding'), 'deciding')])
    gov += '<section id="now">' + text(('Quem decide agora?', 'Who decides now?'), 'h2')
    gov += text(('Hoje, os fundadores decidem, com as pessoas que chamam para uma tarefa definida. Cada tarefa tem uma pessoa responsável, um prazo e um orçamento, então o trabalho segue sem esperar por um fundador.',
                 'Today the founders decide, with the people they bring in for a set task. Each task has a person responsible, a deadline and a budget, so work goes on without waiting for a founder.'), 'p', 'class="answer"')
    gov += gtable(team_rows) + '</section>'
    gov += SAFEGUARDS_SECTION
    gov += '<section id="token-rules">' + text(('Quem decide sobre o token?', 'Who decides about the token?'), 'h2')
    gov += text(('No plano, quando o token for lançado, quem tem o token vota nas regras do token, e membros cuja ajuda foi confirmada por outros (Zeal) também têm voz, junto com o que possuem. As decisões da cooperativa continuam com os seus membros: um membro, um voto.',
                 'In the plan, once the token launches, holders vote on the token’s rules, and members whose help others have confirmed (Zeal) have a say alongside what they hold. The cooperative’s own decisions stay with its members: one member, one vote.'), 'p', 'class="answer"')
    gov += '<p>' + text(('Como o token funcionaria', 'How the token would work'), 'a', 'href="blockchain.html#token"') + '</p></section>'
    gov += '<section id="residents">' + text(('Quem decide quando as famílias morarem nas casas?', 'Who decides once families live in the houses?'), 'h2')
    gov += text(('Mais tarde, quando as primeiras casas existirem e a cooperativa estiver formada, os membros decidem as questões da cooperativa, um membro, um voto, e os moradores decidem sobre os espaços comuns. Estamos desenhando essa estrutura agora, e os primeiros moradores vão dar forma a ela.',
                 'Later, once the first houses exist and the cooperative is formed, its members decide cooperative matters, one member, one vote, and residents decide their shared spaces. We are designing this framework now, and the first residents will shape it.'), 'p', 'class="answer"')
    gov += '<details class="disclosure"><summary>' + text(('Como estamos desenhando', 'How we are designing it'), 'span') + '</summary><div class="disclosure-body">'
    gov += gtable(resident_rows)
    why_org = guide['why']
    gov += text(why_org['org_title'], 'h3') + text(why_org['org_answer'])
    gov += '<ol class="layer-list org-list">' + ''.join('<li>' + pic + '<h3>' + text(t_, 'span') + '</h3>' + text(b_) + '</li>'
                                                      for pic, (t_, b_) in zip(ORG_PICS, why_org['org_cols'])) + '</ol>'
    gov += text(('No plano, cada família é dona da sua casa, e os espaços comuns, as reservas e os recursos para novas casas seguem regras combinadas entre os moradores.',
                 'In the plan, each family owns its home, and the shared spaces, the reserves and the funding for new houses follow rules the residents agree together.'))
    gov += '</div></details></section>'
    gov += '<section id="recorded">' + text(('Como as decisões ficam registradas?', 'How are decisions recorded?'), 'h2')
    gov += text(('Cada decisão fica numa ata. Uma decisão vale porque o estatuto da cooperativa diz como se decide; a blockchain guarda a prova. No plano, cada pagamento e quem o aprovou ficam numa blockchain pública, onde qualquer pessoa pode conferir.',
                 'Each decision is written in minutes. A decision binds because the cooperative’s statute sets how decisions are made; the blockchain keeps the proof. In the plan, every payment and who approved it is written on a public blockchain, where anyone can check it.'))
    gov += '<p>' + text(('Registro distribuído', 'Distributed ledger'), 'a', 'href="blockchain.html"') + '</p></section>'
    gov += '<section id="deciding">' + text(('O que estamos decidindo agora?', 'What are we deciding now?'), 'h2')
    gov += '<div class="settle-groups">' + ''.join('<div>' + text(label, 'h3') + '<ul class="settle-list">' + ''.join(text(item, 'li') for item in items) + '</ul></div>'
                                                  for label, items in groups) + '</div></section>'
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

    checkable = [(('Um contrato com a construtora do Rafael para dois lofts (janeiro de 2026), com os desenhos', 'A contract with Rafael’s construction company for two lofts (January 2026), with their drawings'), 'properties.html'),
                 (('Um apartamento candidato para o nosso primeiro morador em aluguel com compra', 'A candidate flat for our first rent-to-own tenant'), 'roadmap.html#cases'),
                 (('Custos de obra comparados às tabelas públicas do Brasil', 'Building costs set against Brazil’s public cost tables'), 'transparency.html#first-homes'),
                 (('Pagamentos e aprovações previstos num registro público', 'Payments and approvals planned on a public ledger'), 'blockchain.html')]
    drives = [('Construímos comunidades, não só unidades: lugares onde as pessoas voltam a se encontrar.', 'We build communities, not only units: places where people connect again.'),
              ('O nosso lucro real é social. A nossa riqueza é um mundo onde as pessoas são livres.', 'Our real profit is social. Our wealth is a world where people are free.'),
              ('Quem aluga se torna dono, e um bairro sem estresse vale mais do que ficar milionário.', 'Renters become owners, and a stress-free neighbourhood is worth more than becoming a millionaire.')]
    ideas = '<section id="ideas">' + text(('Por que fazemos isso?', 'Why are we doing this?'), 'h2', 'id="why"')
    ideas += text(('Para criar bairros onde as pessoas voltam a se conectar, e onde quem aluga pode se tornar dono.',
                   'To create neighbourhoods where people connect again, and where renters can become owners.'), 'p', 'class="answer"')
    ideas += text(('Um projeto funciona como um iceberg: o que você pode conferir fica acima da água, e as razões que o sustentam ficam abaixo.',
                   'A project works like an iceberg: what you can check sits above the water, and the reasons that carry it sit below.'))
    ideas += ('<figure class="iceberg"><div class="iceberg-above">' + text(('O que você pode conferir', 'What you can check'), 'p', 'class="iceberg-label"')
              + '<ul>' + ''.join('<li>' + text(label, 'a', f'href="{href}"') + '</li>' for label, href in checkable) + '</ul></div>'
              + '<svg class="iceberg-water" viewBox="0 0 1000 40" preserveAspectRatio="none" aria-hidden="true"><path pathLength="1" d="M0,20 C80,4 160,36 250,20 S420,4 500,20 S670,36 750,20 S920,4 1000,20"/></svg>'
              + '<div class="iceberg-below">' + text(('O que nos move', 'What drives us'), 'p', 'class="iceberg-label"')
              + '<ul class="iceberg-reasons">' + ''.join(text(d, 'li') for d in drives) + '</ul></div>'
              + '</figure></section>')  # caption removed (owner, 29 Oct: it only described the drawing)
    ideas += '<section id="shaped">' + text(('Quais ideias formaram o plano?', 'Which ideas shaped the plan?'), 'h2')
    ideas += text(('Duas ideias dos anos de John na Europa deram forma à IMOBX.', 'Two ideas from John’s years in Europe gave IMOBX its shape.')) + '<div class="idea-grid">'
    ideas += idea(('Cohousing', 'Co-housing'),
                  [('Cada família tem a sua casa e divide espaços que todos administram juntos. John traz esses princípios da Bélgica. Junto com o aluguel com compra, cada família caminha para ser dona da sua casa dentro de um bairro compartilhado.',
                    'Each family keeps its own house and shares spaces that everyone runs together. John brings these principles from Belgium. Joined with rent-to-own, each family moves towards owning its house inside a shared neighbourhood.')])
    ideas += idea(('Ecovilas na Europa', 'Eco-villages in Europe'),
                  [('John passou seis anos em ecovilas na Europa e depois transformou esse ativismo em modelos de negócio. A IMOBX junta as duas coisas: viver em comunidade e um negócio que se sustenta.',
                    'John spent six years in eco-villages in Europe, then turned that activism into business models. IMOBX brings the two together: living as a community, and a business that sustains itself.')],
                  (('O que é uma ecovila (Global Ecovillage Network)', 'What an eco-village is (Global Ecovillage Network)'), 'https://ecovillage.org/'))
    ideas += '</div></section>'
    ideas += '<section id="check">' + text(('Com quais ideias conferimos o plano?', 'Which ideas do we check the plan against?'), 'h2')
    ideas += text(('Conferimos cada regra que escrevemos com dois conjuntos de princípios que funcionam na prática há décadas.',
                   'We check each rule we write against two sets of principles that have worked in practice for decades.')) + '<div class="idea-grid">'
    ideas += idea(('Os princípios de Elinor Ostrom', 'Elinor Ostrom’s principles'),
                  [('Elinor Ostrom ganhou o Nobel de economia em 2009 por mostrar como comunidades administram bem recursos comuns, sem entregá-los a uma empresa ou ao Estado. A nossa proposta completa confere a IMOBX com os oito princípios dela.',
                    'Elinor Ostrom won the 2009 Nobel Prize in economics for showing how communities manage shared resources well, without handing them to a company or the state. Our full proposal checks IMOBX against her eight principles.')],
                  (('Elinor Ostrom no site do Prêmio Nobel', 'Elinor Ostrom on the Nobel Prize site'), 'https://www.nobelprize.org/prizes/economic-sciences/2009/ostrom/facts/'))
    ideas += idea(('Os princípios das cooperativas', 'The cooperative principles'),
                  [('A Aliança Cooperativa Internacional reúne os sete princípios que as cooperativas do mundo compartilham, entre eles a gestão democrática pelos membros. No Brasil, a lei das cooperativas define um membro, um voto (Lei 5.764, art. 42).',
                    'The International Cooperative Alliance sets out the seven principles cooperatives share worldwide, among them democratic control by the members. In Brazil, the cooperative law sets one member, one vote (Lei 5.764, article 42).')],
                  (('A identidade cooperativa (ICA)', 'The cooperative identity (ICA)'), 'https://ica.coop/en/cooperatives/cooperative-identity'))
    ideas += '</div></section>'
    ideas += '<section id="studied">' + text(('Quais projetos estudamos?', 'Which projects did we study?'), 'h2')
    ideas += text(('Grupos de moradia na Alemanha, no Uruguai e nos Estados Unidos já administram as suas casas juntos. Aproveitamos o que funciona e adaptamos ao Rio.',
                   'Housing groups in Germany, Uruguay and the United States already run their houses together. We take what works and adapt it to Rio.')) + '<div class="idea-grid">'
    ideas += idea(('Mietshäuser Syndikat (Alemanha)', 'Mietshäuser Syndikat (Germany)'),
                  [('Uma federação alemã de casas de aluguel administradas pelos moradores. Uma casa só pode ser vendida quando os moradores e a federação concordam; sobre aluguéis e novos moradores, os moradores decidem sozinhos. Estamos estudando se a IMOBX deve adotar uma regra assim.',
                    'A German federation of rental houses run by their residents. A house can be sold only when both its residents and the federation agree; on rents and move-ins, the residents decide alone. We are studying whether IMOBX should adopt a rule like it.')],
                  (('Mietshäuser Syndikat', 'Mietshäuser Syndikat'), 'https://www.syndikat.org/syndikat/'))
    ideas += idea(('FUCVAM (Uruguai)', 'FUCVAM (Uruguay)'),
                  [('A federação uruguaia de cooperativas de moradia, fundada em 1970. As famílias constroem juntas, em ajuda mútua, e a cooperativa fica com a propriedade. No plano da IMOBX, cada família é dona da sua casa.',
                    'Uruguay’s federation of housing cooperatives, founded in 1970. Families build together through mutual aid, and the cooperative holds the title. In IMOBX’s plan, each family owns its own house.')],
                  (('FUCVAM', 'FUCVAM'), 'https://www.fucvam.org.uy'))
    ideas += idea(('Fundos comunitários de terra', 'Community land trusts'),
                  [('O fundo fica com o terreno, e os direitos de cada família ficam num contrato longo e assinado. Daí vem a nossa regra: seja qual for o resultado de uma votação, só a família e a IMOBX juntas, dentro da lei, podem mudar o contrato de moradia de uma família.',
                    'The trust keeps the land, and each family’s rights sit in a long, signed lease. Our rule comes from there: whatever a vote decides, only the family and IMOBX together, under the law, can change a family’s housing agreement.')],
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

    # The token: what it is for, why it is kept apart from the cooperative, and the conditions before it exists
    # (owner, 24 Oct). No percentages or payouts here: allocations stay proposals until a lawyer has seen them.
    # The token page is a stub until a token is active (owner decision 13; review-C §2, 28 Oct). Its earlier text stays
    # in model-guide.json under token_page, unpublished; the parts that still apply live in the ledger page's token fold.
    ts = guide['token_stub']
    page_tk = '<main class="paper guide-paper token-page band-page" id="main">' + text(ts['title'], 'h1')
    page_tk += text(ts['text'], 'p', 'class="guide-lead"')
    page_tk += text(ts['protection'])  # the owner's vote protection goes with any mention of a token (gate rule)
    page_tk += '<p>' + text(ts['link'], 'a', 'class="button act" href="blockchain.html#token"') + '</p>'
    page_tk += partner_line('token.html') + '</main>'
    (root / 'token.html').write_text(page('IMOBX | Is there an IMOBX token?', page_tk, f'<link rel="stylesheet" href="{asset_v("bands.css")}"><script src="assets/site.js" defer></script>',
        version=guide['version'], lang='pt-BR', title_pt='IMOBX | Existe um token da IMOBX?'))

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
        return ('<details class="v-line-item"><summary>' + text((o[0][0].rstrip('.'), o[0][1].rstrip('.')), 'span', 'class="v-title"')
                + text(short, 'span', 'class="v-line"') + text(ch['more_info'], 'span', 'class="v-link"') + '</summary>'
                + '<div class="v-body">' + text(o[1]) + text(ch['bridge_more'][i]) + '</div></details>')
    cells = v_line(0) + v_line(1) + v_line(2)
    # The token's loop (owner, 29 Oct: "you can make such animation"). It starts with use, which is why the token
    # launches only once it gives access (decision 32). The drawing is for sighted readers; the list carries the meaning.
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

    chain += ('<section id="token">' + text(ch['token_fold'], 'h2') + text(ch['token_answer'], 'p', 'class="answer"')
              + text(ch['loop_title'], 'h3') + text(ch['loop_intro']) + loop_figure()
              + text(ch['bridge_title'], 'h3') + text(ch['matrix_intro']) + '<div class="v-lines">' + cells + '</div>'
              + fold(ch['token_more'],
                     text(ch['token_intro']) + text(ch['receives_text']) + text(ch['token_purpose']) + text(ch['review_note'])
                     + text(ch['lock_title'], 'h3') + text(ch['bridge'][3][1]) + text(ch['bridge_more'][3])
                     + chain_source(('Como o regulador do mercado de capitais avalia tokens (CVM)', 'How Brazil’s market regulator looks at tokens (CVM)'), guide['sources']['cvm']['url'],
                                    ('Explica como a CVM decide quais regras valem para um token.', 'Explains how the CVM decides which rules apply to a token.'))
                     + text(ch['never_title'], 'h3') + text(ch['never_intro']) + '<ul>' + ''.join(text(o, 'li') for o in ch['never']) + '</ul>')
              + '<script>document.addEventListener("DOMContentLoaded",function(){var l=document.querySelector(".token-loop");'
                'if(!l||!("IntersectionObserver" in window)||matchMedia("(prefers-reduced-motion: reduce)").matches)return;l.classList.add("js-loop");'
                'new IntersectionObserver(function(e,o){e.forEach(function(x){if(x.isIntersecting){l.classList.add("is-looping");'
                'var a=l.querySelector("animateMotion");setTimeout(function(){try{a.beginElement()}catch(_){}} ,2200);o.disconnect();}});},{threshold:.35}).observe(l);});</script>'
              + '<script>document.addEventListener("DOMContentLoaded",function(){var m=document.querySelector(".v-matrix");'
                'if(!m||!("IntersectionObserver" in window))return;document.documentElement.classList.add("js-flow");'
                'new IntersectionObserver(function(e,o){e.forEach(function(x){if(x.isIntersecting){m.classList.add("is-flowing");o.disconnect();}});},{threshold:.3}).observe(m);});</script>'
              + '</section>')
    chain += '<section id="open">' + text(ch['open_title'], 'h2')
    chain += text(ch['open_runs_title'], 'h3') + '<ol class="path-list">' + ''.join(text(o, 'li') for o in ch['open_runs']) + '</ol>'
    chain += '<div class="window">' + text(ch['same_title'], 'h3') + '<ul>' + ''.join(text(o, 'li') for o in ch['same']) + '</ul></div>'
    chain += '<span id="limits"></span>' + fold(ch['limits_title'], '<ul>' + ''.join(text(o, 'li') for o in ch['limits']) + '</ul>'
                  + chain_source(('O anúncio da Circle de que a Arc entrou em funcionamento (16 de setembro de 2026)', 'Circle’s announcement that Arc went live (16 September 2026)'),
                                 'https://www.circle.com/pressroom/circle-launches-arc-mainnet-an-economic-operating-system-for-the-internet',
                                 ('Anuncia a rede e observa que os reguladores ainda vão avaliá-la.', 'Announces the network and notes that regulators have yet to approve it.'))
                  + chain_source(('As empresas que operam a rede Arc', 'The companies that run the Arc network'),
                                 'https://www.arc.io/pressroom/circle-announces-founding-validator-cohort-and-major-integrations-for-arc-ahead-of-september-16-mainnet-launch',
                                 ('Lista as empresas fundadoras.', 'Lists the founding companies.'))
                  + chain_source(('A lista de riscos do USDC feita pela própria Circle', 'Circle’s own list of USDC risks'), 'https://www.circle.com/legal/usdc-risk-factors',
                                 ('Diz que a Circle pode bloquear USDC.', 'Says Circle can freeze USDC.'))) + '</section>'
    chain += '<section class="closing-band" id="help">' + text(ch['closing']) + text(ch['button'], 'a', 'class="button act" href="contact.html"') + '</section>'
    chain += partner_line('blockchain.html') + '</main>'
    # Jargon popups (owner, 28 Oct): the meanings travel inside the page; terms.js runs after site.js.
    terms_data = json.dumps(json.loads((root / 'terms.json').read_text()), ensure_ascii=False).replace('</', '<\\/')
    terms_script = ('<script type="application/json" id="imobx-terms">' + terms_data + '</script>'
                    '<script src="assets/site.js" defer></script>' + f'<script src="{asset_v("terms.js")}" defer></script>')
    (root / 'blockchain.html').write_text(page('IMOBX | Distributed ledger', chain, f'<link rel="stylesheet" href="{asset_v("flow.css")}"><link rel="stylesheet" href="{asset_v("bands.css")}">' + MF_SCRIPT + terms_script,
        version=guide['version'], lang='pt-BR', title_pt='IMOBX | Registro distribuído'))

    stub_targets = {item['id']: ('rent-to-own.html' if item['id'] in HOUSEHOLD_FAQ else 'transparency.html')
                    for item in guide['questions']}
    stub_targets.update({'thanks-zeal-lets': 'transparency.html', 'euler': 'transparency.html'})
    (root / 'faq.html').write_text(redirect_stub(
        'IMOBX | Perguntas sobre o modelo', 'Perguntas sobre o modelo', 'rent-to-own.html#questions',
        'Open the current version', per_question=stub_targets))

    # The homepage is built whole by home_page.py (owner-approved mock, 26 Oct 2026); its three phases live on the roadmap.
