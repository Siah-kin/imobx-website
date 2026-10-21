"""Public roadmap and model explanation. Content only; no governance execution."""
import json
import re

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


def build_guide(root, page, tr, esc, language_controls):
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
        'cvm': ('CVM · Parecer de Orientação 40', 'CVM · Guidance Opinion 40'),
        'nonprofit': ('Lei 13.019 · art. 2º, I, a', 'Law 13.019 · article 2, I, a'),
        'ica': ('ICA · Identidade cooperativa', 'ICA · Cooperative identity'),
        'ostrom': ('Elinor Ostrom · Palestra do Nobel', 'Elinor Ostrom · Nobel lecture'),
        'arc': ('Arc · Litepaper', 'Arc · Litepaper'),
        'arctide': ('Arctide · exchange na Arc', 'Arctide · exchange on Arc'),
        'argus': ('Argus · exchange na Arc', 'Argus · exchange on Arc'),
        'cash': ('Whitepaper, seção 4: a política de caixa (em inglês)', 'Whitepaper, section 4: the cash policy'),
        'rights': ('Whitepaper, seção 8: o que um token poderia representar (em inglês)', 'Whitepaper, section 8: what a token could represent'),
        'digital': ('Whitepaper, seção 9: o que passa a ser digital (em inglês)', 'Whitepaper, section 9: what becomes digital'),
        'technical': ('Guia do piloto, seção 6: escopo e aceitação (em inglês)', 'Pilot guide, section 6: scope and acceptance'),
        'roadmap': ('Etapas do projeto', 'Project stages'),
        'charter': ('Etapas do projeto: quem decide o quê', 'Project stages: who decides what'),
        'cost': ('Whitepaper, seção 3: os custos (em inglês)', 'Whitepaper, section 3: the costs'),
        'sinapi': ('CAIXA · SINAPI', 'CAIXA · SINAPI'),
        'cub': ('Sinduscon · escopo do CUB', 'Sinduscon · CUB scope'),
        'cnpj': ('Receita Federal · entidades estrangeiras e CNPJ', 'Receita Federal · foreign entities and CNPJ'),
        'title': ('Código Civil · art. 1.245', 'Civil Code · article 1,245'),
        'mb': ('Mercado Bitcoin · elegibilidade de contas', 'Mercado Bitcoin · account eligibility'),
        'bcb': ('Banco Central · Resolução 521', 'Central Bank · Resolution 521'),
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
                out += ''.join(source_line(key) for key in by_sentence.get(index, []))
                pending = []
        return out

    def source_line(key):
        source = guide['sources'][key]
        return ('<p class="source-note">' + text(('Fonte: ', 'Source: '), 'span')
                + f'<a href="{esc(source["url"])}">{label_text(key)}</a>. ' + text(source_effect[key], 'span') + '</p>')

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

    def faq(home=True):
        """The homepage subset. Its anchors are home-faq-<id>: each faq-<id> anchor exists once, on the page that holds the full item."""
        body = '<div class="faq" id="faq">' + text(
            ('Perguntas sobre o projeto', 'Questions about the project'), 'h2')
        body += text(('Como o projeto funcionaria e o que ainda falta decidir.', 'How the project would work and what remains undecided.'))
        body += ''.join(faq_item(x, 'home-faq-') for x in guide['questions'] if x['home'])
        body += text(('Mais perguntas das famílias', 'More questions families ask'),
                     'a', 'class="guide-more" href="rent-to-own.html#questions"')
        return body + '</div>'

    family_questions = [x for x in guide['questions'] if x['id'] in HOUSEHOLD_FAQ]
    funding_questions = [x for x in guide['questions'] if x['id'] not in HOUSEHOLD_FAQ]

    def family_faq_section():
        body = '<section class="faq" id="questions">' + text(('Perguntas das famílias', 'Questions families ask'), 'h2')
        body += ''.join(faq_item(x, 'faq-', 'rent-to-own.html', short=True) for x in family_questions)
        body += text(('Mais perguntas, sobre financiamento e governança', 'More questions, about funding and governance'),
                     'a', 'class="guide-more" href="transparency.html#funding-questions"')
        return body + '</section>'

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
    resident = '<main class="paper guide-paper resident-page" id="main">'
    resident += text(journey['title'], 'h1') + text(journey['intro'], 'p', 'class="guide-lead"')
    resident += '<aside class="guide-status">' + text(journey['status']) + '</aside>'
    resident += '<nav class="guide-jump" aria-label="Sections">'
    for ident, label in [('payments', ('Pagamentos e compra', 'Payments and purchase')),
                         ('repairs', ('Reparos', 'Repairs')), ('decisions', ('Decisões', 'Decisions')),
                         ('hardship', ('Dificuldade de pagamento e saída', 'Hardship and leaving')),
                         ('funding', ('Financiamento', 'Funding')), ('property', ('Imóveis e parceiros', 'Property and partners')),
                         ('questions', ('Perguntas', 'Questions'))]:
        resident += text(label, 'a', f'href="#{ident}"')
    resident += '</nav><section id="payments">' + text(journey['steps_title'], 'h2') + '<ol>'
    for step in journey['steps']:
        resident += '<li>' + text(step['title'], 'h3') + text(step['body']) + '</li>'
    resident += '</ol>' + text(journey['payments_title'], 'h3')
    resident += ''.join(text(pair) for pair in journey['payments'])
    resident += text(('Veja os dois orçamentos de construção', 'Read the two construction budgets'),
                     'a', 'href="index.html#custos"') + '</section>'
    for ident in ('repairs', 'decisions', 'hardship', 'funding', 'property', 'next'):
        resident += f'<section id="{ident}">' + text(journey[ident + '_title'], 'h2')
        resident += ''.join(text(pair) for pair in journey[ident])
        target, label = {
            'repairs': ('roadmap.html#governance', ('Quem cuida do trabalho e como questionar uma decisão', 'Who handles the work and how to question a decision')),
            'decisions': ('roadmap.html#participation', ('Como os papéis se relacionam', 'How participant roles fit together')),
            'hardship': ('reference.html#status', ('Situação atual e documentos disponíveis', 'Current status and available documents')),
            'funding': ('transparency.html#faq-funding', ('De onde viria o dinheiro para as casas', 'Where the money for the homes would come from')),
            'property': ('contact.html?role=property', ('Preparar uma apresentação do imóvel', 'Prepare a property introduction')),
            'next': ('contact.html?role=resident', ('Preparar uma conversa sobre moradia', 'Prepare a housing conversation')),
        }[ident]
        resident += text(label, 'a', f'href="{target}"') + '</section>'
    resident += family_faq_section() + '</main>'
    (root / 'rent-to-own.html').write_text(page('IMOBX | Renting and buying a home', resident,
        version=guide['version'], lang='pt-BR', title_pt='IMOBX | Aluguel e compra da casa'))

    summary = '<section class="content wrap scale-section" id="etapas"><span id="dinheiro"></span>'
    summary += text(('Etapas do projeto', 'Project stages'), 'h2')
    summary += text(('O caminho da IMOBX reúne moradia com opção de compra, participação dos moradores e contas transparentes. A estrutura jurídica, as regras de participação e as ferramentas digitais estão em desenvolvimento.', 'IMOBX’s roadmap brings together rent-to-own housing, resident participation and transparent accounts. The legal structure, participation rules and digital tools are under development.'))
    for label, ordered, members in grouped_stages():
        summary += text(label, 'p', 'class="stage-group"')
        summary += '<ol class="roadmap-overview">' if ordered else '<ul class="roadmap-overview">'
        for number, stage in members:
            summary += '<li><div>'
            summary += text(numbered(number, stage['title']) if number else stage['title'], 'h3') + text(stage['summary'], 'p')
            summary += '</div></li>'
        summary += '</ol>' if ordered else '</ul>'
    summary += text(('Conheça as etapas do projeto',
                              'Explore the project roadmap'),
                             'a', 'class="button" href="roadmap.html"') + '</section>'

    roadmap = '<main class="paper guide-paper" id="main">' + language_controls
    roadmap += text(('Roteiro IMOBX', 'IMOBX roadmap'), 'h1')
    roadmap += text(('As etapas do projeto, quem participa de cada uma e o que precisa estar pronto.', 'The project stages, who takes part in each and what needs to be ready.'), 'p', 'class="guide-lead"')
    roadmap += text(('O plano reúne as primeiras moradias no Rio, as decisões dos moradores e o financiamento. A preparação jurídica, as conversas sobre como os moradores decidem os assuntos comuns e os testes digitais podem acontecer ao mesmo tempo. As datas de obra dependem do projeto escolhido, dos recursos e das permissões.', 'The plan brings together the first homes in Rio, resident decisions and funding. Legal work, discussions about how residents decide shared matters, and digital tests can happen at the same time. Construction dates depend on the chosen project, funding and permissions.'))
    roadmap += '<div class="guide-status">' + text(('Onde estamos', 'Where we stand'), 'h2')
    roadmap += text(('O projeto está em preparação. O site, os documentos, os desenhos e o orçamento de Rafael estão publicados. A forma jurídica está em definição; ainda falta demonstrar o funcionamento das moradias e o uso de blockchain para guardar e pagar recursos do projeto. O modelo do token permanece em pesquisa.', 'The project is in preparation. The website, documents, drawings and Rafael’s budget are published. The legal form is being defined. Running the homes and using blockchain to hold and pay project funds still need to be demonstrated. The token model remains under research.')) + '</div>'
    roadmap += '<nav class="guide-jump" aria-label="Sections">' + text(('Etapas', 'Stages'), 'a', 'href="#stages"')
    roadmap += text(('Quem participa', 'Who takes part'), 'a', 'href="#participation"')
    roadmap += text(('Decisões compartilhadas', 'Shared decisions'), 'a', 'href="#governance"')
    roadmap += text(('Financiamento e gastos', 'Funding and spending'), 'a', 'href="transparency.html"')
    roadmap += text(('Referência e fontes', 'Reference and sources'), 'a', 'href="reference.html"')
    roadmap += text(('Relatórios do projeto', 'Project reports'), 'a', 'href="#ico-comparison"')
    roadmap += text(('Perguntas', 'Questions'), 'a', 'href="transparency.html#funding-questions"') + '</nav>'
    roadmap += '<section id="stages">' + text(('Etapas de desenvolvimento', 'Development stages'), 'h2')
    roadmap += text(('Abra uma etapa para ver os prazos, o trabalho previsto, o que precisa estar pronto e o que impede o avanço.', 'Open a stage to see its timing, planned work, what needs to be ready and what stops it.'))
    for label, ordered, members in grouped_stages():
      roadmap += text(label, 'p', 'class="stage-group"')
      for number, stage in members:
        roadmap += f'<details class="roadmap-stage" id="{esc(stage["id"])}"><summary>'
        roadmap += text(numbered(number, stage['title']) if number else stage['title'], 'h3') + text(stage['window'], 'span', 'class="guide-window"')
        roadmap += '<span class="stage-owner">' + text(('Quem: ', 'Who: '), 'strong') + text(stage['overview_owner'], 'span') + '</span>'
        roadmap += '<span class="stage-needs">' + text(('Precisa de: ', 'Needs: '), 'strong') + text(stage['overview_needs'], 'span') + '</span></summary><dl>'
        for label, key in [(('Quem faria o trabalho', 'Who would do the work'), 'responsible'),
                           (('Quando poderia acontecer', 'When it could happen'), 'schedule'),
                           (('O trabalho previsto', 'The planned work'), 'work'),
                           (('O que precisa estar pronto', 'What needs to be ready'), 'gate'),
                           (('O que impediria esta etapa', 'What would stop this stage'), 'pause'),
                           (('O que as pessoas poderiam acompanhar', 'What people could follow'), 'web')]:
            roadmap += text(label, 'dt') + text(stage[key], 'dd')
        roadmap += '</dl></details>'
    roadmap += '</section>'

    participation = guide['participation']
    roadmap += '<section id="participation">' + text(participation['title'], 'h2')
    roadmap += text(participation['intro'])
    roadmap += ''.join(text(p) for p in participation['scenario'])
    roadmap += text(participation['roles_title'], 'h3')
    for role in participation['roles']:
        roadmap += '<details class="participant-role">' + text(role['who'], 'summary')
        for label, key in zip(participation['headings'][1:], ['need', 'decision']):
            roadmap += text(label, 'h4') + text(role[key])
        roadmap += '</details>'
    for title, key in [('rights_title', 'rights'), ('token_title', 'token'), ('decision_title', 'decisions')]:
        roadmap += text(participation[title], 'h3')
        roadmap += '<ul>' + ''.join(text(p, 'li') for p in participation[key]) + '</ul>'
    roadmap += text(('Veja como isso funcionaria para uma família: pagamentos, reparos e decisões',
                     'See how this would work for a household: payments, repairs and decisions'),
                    'a', 'href="rent-to-own.html"')
    roadmap += source_notes(['ica', 'token-study', 'cvm'])
    roadmap += text(('Essas fontes orientam a proposta. Nenhuma delas revisou ou endossou a IMOBX.',
                     'These sources inform the proposal. None of them has reviewed or endorsed IMOBX.'), 'p', 'class="source-note"') + '</section>'

    # Keep old shared anchors usable while linking the single detailed reading page.
    roadmap += '<section id="settlement"><span id="ramp-options"></span>' + text(
        ('Financiamento e gastos', 'Funding and spending'), 'h2')
    roadmap += text(('Veja o fluxo de caixa proposto, as despesas previstas e o que conferir antes de usar pagamentos na blockchain.', 'See the proposed cash flow, planned spending and checks needed before using blockchain payments.'))
    roadmap += text(('Ver fluxos, fontes e decisões', 'View flows, sources and decisions'),
                    'a', 'class="button" href="transparency.html"') + '</section>'

    # These diagrams describe proposed money/contract paths, not a payment API.
    settlement = guide['settlement']
    settlement_html = ''
    settlement_html += '<section id="settlement">' + text(settlement['title'], 'h2')
    settlement_html += text(settlement['intro'])
    settlement_html += '<div class="settlement-history">' + text(settlement['historical_title'], 'h3')
    settlement_html += text(settlement['historical_route'], 'p', 'class="settlement-chain"')
    settlement_html += text(settlement['historical_note']) + '</div>'
    for route in settlement['routes']:
        settlement_html += f'<article class="settlement-route" id="{esc(route["id"])}">' + text(route['title'], 'h3')
        settlement_html += text(route['intro']) + '<ol class="settlement-steps">'
        for step in route['steps']:
            settlement_html += '<li><div>' + text(step['title'], 'strong') + text(step['body']) + '</div></li>'
        settlement_html += '</ol>' + text(route['note'], 'p', 'class="fine"') + '</article>'
    settlement_html += text(settlement['relationships_title'], 'h3')
    settlement_html += '<div class="settlement-relationships">'
    for relationship in settlement['relationships']:
        settlement_html += '<article>' + text(relationship['title'], 'h3') + text(relationship['body']) + '</article>'
    settlement_html += '</div>' + cited_paragraph(settlement['registration'], {0: ['cnpj'], 2: ['title']})
    settlement_html += cited_paragraph(settlement['network_note'], {0: ['bcb']})
    research = settlement['provider_research']
    settlement_html += '<section id="ramp-options">' + text(research['title'], 'h3')
    settlement_html += text(research['conclusion'])
    settlement_html += '<ul>' + ''.join(text(p, 'li') for p in research['acceptance']) + '</ul>'
    settlement_html += text(research['status'], 'p', 'class="fine"') + '</section>'
    settlement_html += text(settlement['evidence_title'], 'h3')
    settlement_html += '<ul>' + ''.join(text(x, 'li') for x in settlement['evidence']) + '</ul>'
    settlement_html += cited_paragraph(settlement['limits'], {0: ['cash'], 1: ['nonprofit']}) + '</section>'

    public = guide['transparency']
    transparency = '<main class="paper guide-paper transparency-page" id="main">' + language_controls
    transparency += text(public['title'], 'h1') + text(public['lead'], 'p', 'class="guide-lead"')
    transparency += text(public['intro'])
    transparency += '<section id="status">' + text(public['status_title'], 'h2')
    transparency += '<div class="transparency-status">'
    for item in public['statuses']:
        transparency += '<article>' + text(item['title'], 'h3') + text(item['body']) + '</article>'
    transparency += '</div></section><nav class="guide-jump" aria-label="Sections">'
    for label, target in [(('Participação', 'Participation'), 'community-economy'),
                          (('Fluxos', 'Flows'), 'settlement'),
                          (('Serviço de pagamento', 'Payment service'), 'ramp-options'),
                          (('Próximos passos', 'Next steps'), 'next-steps'),
                          (('Relatórios', 'Reports'), 'reporting'),
                          (('Fontes', 'Sources'), 'sources'),
                          (('Atualizações', 'Updates'), 'updates'),
                          (('Perguntas', 'Questions'), 'funding-questions')]:
        transparency += text(label, 'a', f'href="#{target}"')
    transparency += '</nav>'
    transparency += '<section id="household-payments">' + text(
        ('O pagamento da família e a compra da casa', 'The household payment and home purchase'), 'h2')
    transparency += text(journey['steps'][1]['body']) + text(journey['payments'][0])
    transparency += text(('Como seriam os pagamentos e a transferência do imóvel',
                         'How payments and the property transfer would work'),
                        'a', 'href="rent-to-own.html#payments"') + '</section>'
    economy = guide['community_economy']
    transparency += '<section id="community-economy">' + text(economy['title'], 'h2')
    transparency += text(economy['intro']) + text(economy['status'], 'p', 'class="guide-status"')
    for topic in economy['topics']:
        transparency += f'<details class="community-topic" id="{esc(topic["id"])}">' + text(topic['title'], 'summary')
        transparency += with_sources(topic['id'], topic['body']) + '</details>'
    transparency += '<span id="thanks-zeal-lets"></span></section>'
    transparency += settlement_html
    transparency += '<section id="next-steps">' + text(public['followup_title'], 'h2')
    transparency += text(public['followup_intro']) + '<dl class="transparency-followups">'
    for item in public['followups']:
        transparency += text(item['title'], 'dt') + text(item['body'], 'dd')
    transparency += '</dl></section>'
    transparency += '<section id="reporting">' + text(public['reporting_title'], 'h2')
    transparency += text(public['reporting_intro']) + '<ul>'
    transparency += ''.join(text(item, 'li') for item in public['reporting']) + '</ul></section>'
    transparency += '<section id="sources">' + text(public['evidence_title'], 'h2')
    for item in public['evidence']:
        transparency += '<article>' + text(item['title'], 'h3') + text(item['body']) + '</article>'
    transparency += text(public['sources_title'], 'h3') + text(public['sources_intro'])
    for group in public['source_groups']:
        transparency += '<details class="transparency-source-group"><summary>' + text(group['title'])
        transparency += '</summary><ul>'
        for key in group['keys']:
            source = guide['sources'][key]
            transparency += f'<li><a href="{esc(source["url"])}">{label_text(key)}</a></li>'
        transparency += '</ul></details>'
    transparency += '</section><section id="updates">' + text(public['changes_title'], 'h2')
    transparency += '<ol class="transparency-updates">'
    for change in public['changes']:
        transparency += '<li><time datetime="' + esc(change['date']) + '">' + esc(change['date']) + '</time>'
        transparency += text(change['title'], 'h3') + text(change['body']) + '</li>'
    transparency += '</ol>' + text(public['maintenance']) + '</section>' + funding_faq_section() + '<div class="guide-jump">'
    transparency += text(('Para desenvolvedores: conteúdo da página (JSON)', 'For developers: page content (JSON)'),
                         'a', 'href="model-guide.json" download')
    transparency += text(('Roteiro do projeto', 'Project roadmap'), 'a', 'href="roadmap.html"')
    transparency += text(('Todos os documentos', 'All documents'), 'a', 'href="resources.html"') + '</div></main>'
    (root / 'transparency.html').write_text(page('IMOBX | Funding and spending', transparency,
        '<script src="assets/site.js" defer></script>', version=guide['version'], lang='pt-BR', title_pt='IMOBX | Financiamento e gastos'))

    roadmap += '<section id="governance">' + text(('Quem decide o quê?', 'Who decides what?'), 'h2')
    roadmap += text(('Uma pessoa pode morar numa casa, trabalhar para a IMOBX e investir no projeto. Cada relação tem seus próprios direitos e responsabilidades.', 'One person can live in a home, work for IMOBX and invest in the project. Each relationship has its own rights and responsibilities.'))
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
        [('Investimento e possíveis pagamentos', 'Investment and possible payments'),
         ('Quem investe recebe somente os direitos escritos no seu acordo.', 'Investors receive only the rights written in their agreement.'),
         ('Comprar tokens não dá controle automático sobre moradores. Os contratos e o uso combinado das doações continuam valendo.', 'Buying tokens does not give automatic control over residents. Agreements and the stated purpose of donations still apply.')],
        [('Expansão e regras da rede', 'Expansion and network rules'),
         ('Grupos definidos nas regras da organização, com representantes locais e contas abertas à conferência.', 'Groups defined in the organization’s rules, with local representatives and accounts people can check.'),
         ('Regras de votação, competências, resolução de conflitos e substituição dos responsáveis previstas nos acordos da organização.', 'Voting requirements, decision powers, dispute resolution and replacement of responsible people set out in the organisation’s agreements.')]
    ]
    roadmap += '<div class="guide-table"><table><thead><tr>' + ''.join(text(h, 'th', 'scope="col"') for h in headings)
    roadmap += '</tr></thead><tbody>'
    for row in rows:
        roadmap += '<tr>' + ''.join(text(cell, 'td') for cell in row) + '</tr>'
    roadmap += '</tbody></table></div>'
    roadmap += text(('A experiência e o trabalho realizado podem orientar a escolha de responsáveis. A proposta combina funções com prazo definido, revisão das decisões e participação de novos moradores, sem vincular a voz dos moradores ao saldo de tokens.', 'Experience and completed work can inform appointments. People would hold roles for an agreed period. Residents could question decisions, replace representatives and let newcomers take on responsibilities. A resident’s voice would not depend on how many tokens they hold.'))
    roadmap += source_notes(['ostrom'])
    roadmap += text(('Aplicando Ostrom ao piloto', 'Applying Ostrom to the pilot'), 'h3')
    principles = [
        ('Membros, imóveis, recursos compartilhados e direitos de cada família claramente identificados.', 'Clearly identified members, properties, shared resources and household rights.'),
        ('Custos e responsabilidades adequados às condições locais e à capacidade das famílias.', 'Costs and responsibilities suited to local conditions and household circumstances.'),
        ('Participação das pessoas afetadas nas decisões sobre suas regras comuns.', 'Participation by affected people in decisions about their shared rules.'),
        ('Conferência de dinheiro e trabalho por pessoas que prestam contas aos participantes e declaram seus interesses.', 'Checks on money and work by people accountable to participants who disclose their interests.'),
        ('Respostas proporcionais ao descumprimento de regras, com oportunidade de defesa.', 'Proportionate responses to rule violations, with an opportunity to be heard.'),
        ('Mediação e revisão acessíveis, com proteção aos direitos de moradia.', 'Accessible mediation and review, with protection for housing rights.'),
        ('Base jurídica para as responsabilidades e decisões da organização.', 'A legal basis for the organisation’s responsibilities and decisions.'),
        ('Decisões locais próximas dos moradores e serviços compartilhados entre projetos.', 'Local decisions close to residents, with services shared across projects.')
    ]
    roadmap += '<ol class="ostrom-application">' + ''.join(text(p, 'li') for p in principles) + '</ol>'
    roadmap += text(('Estes princípios adaptam o trabalho de Ostrom sobre recursos comuns à governança proposta para a IMOBX. Sua aplicação abrange manutenção, urgências, cobranças contestadas e novas obras, com responsabilidades identificáveis em cada decisão.', 'These principles adapt Ostrom’s work on shared resources to IMOBX’s proposed governance. Their application covers maintenance, emergencies, disputed invoices and new construction, with identifiable responsibility for each decision.'))
    roadmap += text(('Como o trabalho segue no dia a dia', 'How everyday work moves forward'), 'h3')
    for key in ['work', 'example', 'continuity', 'status']:
        roadmap += text(guide['dao_operations'][key])
    roadmap += source_notes(['digital']) + '</section>'

    roadmap += '<section id="ico-comparison">' + text(('Relatórios do projeto', 'Project reports'), 'h2')
    roadmap += text(('Quando a obra começar, a proposta é publicar um relatório para cada projeto. Cada relatório lista:', 'Once building starts, the plan is to publish a report for each project. Each report lists:'))
    report_items = [
        (('Imóvel e contratos', 'Property and agreements'),
         ('os documentos que mostram que a IMOBX pode usar o imóvel e as condições de moradia.', 'the documents showing IMOBX may use the property, and the housing terms.')),
        (('Dinheiro que entra e sai', 'Money in and out'),
         ('de onde veio cada pagamento, para que serviu, o comprovante e quem conferiu.', 'where each payment came from, what it paid for, its receipt and who checked it.')),
        (('Decisões', 'Decisions'),
         ('quem decidiu, dentro de qual limite de gasto, e como pedir revisão.', 'who decided, within what spending limit, and how to ask for a review.')),
        (('As casas', 'The homes'),
         ('custos reais, reparos ainda abertos e quanto cada família já avançou na compra.', 'actual costs, repairs still open and how far each family is towards owning its home.')),
    ]
    roadmap += '<ul class="report-list">' + ''.join(
        '<li>' + text(head, 'strong') + ': ' + text(body, 'span') + '</li>' for head, body in report_items) + '</ul>'
    roadmap += text(('Valores previstos, recebidos e gastos aparecem separados.', 'Planned, received and spent amounts are shown separately.'))
    roadmap += source_notes(['cash', 'cost']) + '</section></main>'
    (root / 'roadmap.html').write_text(page('IMOBX | Roadmap', roadmap,
        '<script src="assets/site.js" defer></script>', version=guide['version'], lang='pt-BR', title_pt='IMOBX | Roteiro'))

    stub_targets = {item['id']: ('rent-to-own.html' if item['id'] in HOUSEHOLD_FAQ else 'transparency.html')
                    for item in guide['questions']}
    stub_targets.update({'thanks-zeal-lets': 'transparency.html', 'euler': 'transparency.html'})
    (root / 'faq.html').write_text(redirect_stub(
        'IMOBX | Perguntas sobre o modelo', 'Perguntas sobre o modelo', 'rent-to-own.html#questions',
        'Open the current version', per_question=stub_targets))

    home = root / 'index.html'
    overview = guide['home_overview']
    housing = '<section class="content wrap solution-section" id="modelo" aria-labelledby="home-purchase-title">'
    housing += '<header class="home-model-heading">'
    housing += text(overview['title'], 'h2', 'id="home-purchase-title"') + text(overview['intro']) + '</header>'
    housing += '<div class="home-model-layout"><div class="home-purchase"><ol class="home-purchase-steps">'
    for step in overview['steps']:
        housing += '<li>' + text(step['title'], 'h3') + text(step['body']) + '</li>'
    housing += '</ol><aside class="home-purchase-terms" id="participation-summary">'
    housing += text(overview['terms_title'], 'h3') + text(overview['terms_status'])
    housing += '</aside>'
    housing += text(overview['link'], 'a', 'class="button" href="rent-to-own.html"') + '</div>'
    housing += '<aside class="home-village-vision" id="visao-rafael">' + text(overview['vision_title'], 'h3') + text(overview['vision_intro'])
    housing += '<figure class="village-illustration"><img src="assets/homepage.jpg" width="1024" height="765" loading="lazy" '
    housing += 'alt="Ilustração conceitual da vila imaginada por Rafael, com casas e espaços compartilhados." '
    housing += 'data-alt-pt="Ilustração conceitual da vila imaginada por Rafael, com casas e espaços compartilhados." '
    housing += 'data-alt-en="Concept illustration of Rafael’s village vision, with homes and shared spaces.">'
    housing += '<figcaption>' + text(overview['vision_caption']) + '</figcaption></figure>'
    housing += text(overview['vision_decisions']) + text(overview['vision_link'], 'a', 'href="rent-to-own.html#decisions"')
    housing += '</aside></div></section>'
    home_source, count = re.subn(r'<section class="content wrap solution-section" id="modelo"[^>]*>.*?</section>',
                                lambda _: housing, home.read_text(), count=1, flags=re.S)
    if count != 1:
        raise ValueError('Expected one homepage housing explanation.')
    source, count = re.subn(r'<section class="content wrap scale-section" id="etapas">.*?</section>(?=<section class="content tint" id="gastos">)',
                            lambda _: summary, home_source, count=1, flags=re.S)
    if count != 1:
        raise ValueError('Expected one homepage roadmap before the spending section.')
    source, count = re.subn(r'<div class="faq"(?: id="faq")?>.*?</div>\s*</section>',
                            lambda _: faq(home=True) + '\n </section>', source, count=1, flags=re.S)
    if count != 1:
        raise ValueError('Expected one homepage FAQ at the end of resources.')
    home.write_text(source)
