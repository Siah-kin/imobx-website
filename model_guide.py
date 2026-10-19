"""Public roadmap and model explanation. Content only; no governance execution."""
import json
import re


def build_guide(root, page, tr, esc, language_controls):
    guide = json.loads((root / 'model-guide.json').read_text())

    def text(pair, tag='p', attrs=''):
        return tr(*pair, tag, attrs)

    def links(keys):
        return '<p class="guide-sources">' + ' · '.join(
            f'<a href="{esc(guide["sources"][key]["url"])}">{esc(guide["sources"][key]["label"])}</a>'
            for key in keys) + '</p>'

    def faq(home=False):
        items = [x for x in guide['questions'] if not home or x['home']]
        body = '<div class="faq" id="faq">' + text(
            ('Perguntas sobre o projeto', 'Questions about the project'), 'h2')
        body += text(('Como o projeto funcionaria e o que ainda falta decidir.', 'How the project would work and what remains undecided.'))
        for item in items:
            body += f'<details id="faq-{esc(item["id"])}">' + text(item['q'], 'summary')
            body += ''.join(text(pair) for pair in item['a']) + links(item['sources']) + '</details>'
            if item.get('detail_url'):
                body = body[:-len('</details>')] + text(
                    ('Veja a explicação completa', 'Read the full explanation'), 'a',
                    f'href="{esc(item["detail_url"])}"') + '</details>'
        if not home:
            body += '<span id="faq-thanks-zeal-lets"></span><span id="faq-euler"></span>'
            body += text(('Quem participa e quais direitos precisa combinar ↗', 'Who takes part and which rights need agreement ↗'),
                         'a', 'class="guide-more" href="roadmap.html#participation"')
        if home:
            body += text(('Mais perguntas sobre moradia, financiamento e decisões ↗', 'More questions about homes, funding and decisions ↗'),
                         'a', 'class="guide-more" href="faq.html"')
        return body + '</div>'

    journey = guide['resident_journey']
    resident = '<main class="paper guide-paper resident-page" id="main">'
    resident += text(journey['title'], 'h1') + text(journey['intro'], 'p', 'class="guide-lead"')
    resident += '<aside class="guide-status">' + text(journey['status']) + '</aside>'
    resident += '<nav class="guide-jump" aria-label="Sections">'
    for ident, label in [('payments', ('Pagamentos e compra', 'Payments and purchase')),
                         ('repairs', ('Reparos', 'Repairs')), ('decisions', ('Decisões', 'Decisions')),
                         ('hardship', ('Dificuldade de pagamento e saída', 'Hardship and leaving')),
                         ('funding', ('Financiamento', 'Funding')), ('property', ('Imóveis e parceiros', 'Property and partners'))]:
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
            'funding': ('transparency.html#community-economy', ('Orçamentos, fontes de recursos e pagamentos', 'Budgets, funding sources and payments')),
            'property': ('contact.html?role=property', ('Preparar uma apresentação do imóvel', 'Prepare a property introduction')),
            'next': ('contact.html?role=resident', ('Preparar uma conversa sobre moradia', 'Prepare a housing conversation')),
        }[ident]
        resident += text(label, 'a', f'href="{target}"') + '</section>'
    resident += '</main>'
    (root / 'rent-to-own.html').write_text(page('IMOBX | Renting and buying a home', resident,
        version=guide['version'], lang='pt-BR', title_pt='IMOBX | Aluguel e compra da casa'))

    summary = '<section class="content wrap scale-section" id="etapas"><span id="dinheiro"></span>'
    summary += text(('04 / Roteiro do projeto', '04 / Project roadmap'), 'span', 'class="eyebrow"')
    summary += text(('Das primeiras casas a uma rede de moradia.', 'From the first homes to a wider housing network.'), 'h2')
    summary += text(('O caminho da IMOBX reúne moradia com opção de compra, participação dos moradores e contas transparentes. O primeiro projeto está em preparação; a estrutura jurídica, as regras de participação e as ferramentas digitais estão em desenvolvimento.', 'IMOBX’s roadmap brings together rent-to-own housing, resident participation and transparent accounts. The first project is in preparation, with the legal structure, participation rules and digital tools under development.'))
    summary += '<ol class="roadmap-overview">'
    for i, stage in enumerate(guide['stages'], 1):
        summary += f'<li><span class="roadmap-number">{i:02}</span><div>'
        summary += text(stage['title'], 'h3') + text(stage['summary'], 'p', 'class="fine"')
        summary += '</div></li>'
    summary += '</ol>' + text(('Conheça as etapas do projeto ↗',
                              'Explore the project roadmap ↗'),
                             'a', 'class="button" href="roadmap.html"') + '</section>'

    roadmap = '<main class="paper guide-paper" id="main">' + language_controls
    roadmap += text(('Roteiro IMOBX', 'IMOBX roadmap'), 'h1')
    roadmap += text(('Das primeiras casas a uma rede de moradia.', 'From the first homes to a wider housing network.'), 'p', 'class="guide-lead"')
    roadmap += text(('O plano reúne as primeiras moradias no Rio, as decisões dos moradores e o financiamento. A preparação jurídica, as conversas sobre como os moradores decidiriam os assuntos comuns e os testes digitais podem acontecer ao mesmo tempo. As datas de obra dependem do projeto escolhido, dos recursos e das permissões.', 'The plan brings together the first homes in Rio, resident decisions and funding. Legal work, discussions about how residents would decide shared matters, and digital tests can happen at the same time. Construction dates depend on the chosen project, funding and permissions.'))
    roadmap += '<div class="guide-status">' + text(('Onde estamos', 'Where we stand'), 'h2')
    roadmap += text(('O projeto está em preparação. O site, os documentos, os desenhos e o orçamento de Rafael estão publicados. A forma jurídica está em definição; ainda falta demonstrar o funcionamento das moradias e o uso de blockchain para guardar e pagar recursos do projeto. O modelo do token permanece em pesquisa.', 'The project is in preparation. The website, documents, drawings and Rafael’s budget are published. The legal form is being defined. Running the homes and using blockchain to hold and pay project funds still need to be demonstrated. The token model remains under research.')) + '</div>'
    roadmap += '<nav class="guide-jump" aria-label="Sections">' + text(('Etapas', 'Stages'), 'a', 'href="#stages"')
    roadmap += text(('Quem participa', 'Who takes part'), 'a', 'href="#participation"')
    roadmap += text(('Decisões compartilhadas', 'Shared decisions'), 'a', 'href="#governance"')
    roadmap += text(('Transparência', 'Transparency'), 'a', 'href="transparency.html"')
    roadmap += text(('Referência e fontes', 'Reference and sources'), 'a', 'href="reference.html"')
    roadmap += text(('Relatórios do projeto', 'Project reports'), 'a', 'href="#ico-comparison"')
    roadmap += text(('Perguntas', 'Questions'), 'a', 'href="faq.html"') + '</nav>'
    roadmap += '<section id="stages">' + text(('Etapas de desenvolvimento', 'Development stages'), 'h2')
    roadmap += text(('Abra uma etapa para ver os prazos, o trabalho previsto, o que precisa estar pronto e o que impediria o avanço.', 'Open a stage to see its timing, planned work, what needs to be ready and what would stop it.'))
    for i, stage in enumerate(guide['stages'], 1):
        roadmap += f'<details class="roadmap-stage" id="{esc(stage["id"])}"><summary><span class="eyebrow">{i:02}</span>'
        roadmap += text(stage['title'], 'h3') + text(stage['window'], 'span', 'class="guide-window"')
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
    roadmap += links(['ica', 'ostrom', 'token-study', 'cvm']) + '</section>'

    # Keep old shared anchors usable while linking the single detailed reading page.
    roadmap += '<section id="settlement"><span id="ramp-options"></span>' + text(
        ('Financiamento e gastos', 'Funding and spending'), 'h2')
    roadmap += text(('Veja o fluxo de caixa proposto, as despesas previstas e o que conferir antes de usar pagamentos na blockchain.', 'See the proposed cash flow, planned spending and checks needed before using blockchain payments.'))
    roadmap += text(('Ver fluxos, fontes e decisões ↗', 'View flows, sources and decisions ↗'),
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
    settlement_html += '</div>' + text(settlement['registration']) + links(['cnpj', 'title'])
    settlement_html += text(settlement['network_note']) + links(['bcb'])
    research = settlement['provider_research']
    settlement_html += '<section id="ramp-options">' + text(research['title'], 'h3')
    settlement_html += text(research['conclusion'])
    settlement_html += '<ul>' + ''.join(text(p, 'li') for p in research['acceptance']) + '</ul>'
    settlement_html += text(research['status'], 'p', 'class="fine"') + '</section>'
    settlement_html += text(settlement['evidence_title'], 'h3')
    settlement_html += '<ul>' + ''.join(text(x, 'li') for x in settlement['evidence']) + '</ul>'
    settlement_html += text(settlement['limits']) + links(['cash', 'nonprofit']) + '</section>'

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
                          (('Atualizações', 'Updates'), 'updates')]:
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
        transparency += ''.join(text(pair) for pair in topic['body']) + links(topic['sources']) + '</details>'
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
            transparency += f'<li><a href="{esc(source["url"])}">{esc(source["label"])}</a></li>'
        transparency += '</ul></details>'
    transparency += '</section><section id="updates">' + text(public['changes_title'], 'h2')
    transparency += '<ol class="transparency-updates">'
    for change in public['changes']:
        transparency += '<li><time datetime="' + esc(change['date']) + '">' + esc(change['date']) + '</time>'
        transparency += text(change['title'], 'h3') + text(change['body']) + '</li>'
    transparency += '</ol>' + text(public['maintenance']) + '</section><div class="guide-jump">'
    transparency += text(('Para desenvolvedores: conteúdo da página (JSON)', 'For developers: page content (JSON)'),
                         'a', 'href="model-guide.json" download')
    transparency += text(('Roteiro do projeto', 'Project roadmap'), 'a', 'href="roadmap.html"')
    transparency += text(('Todos os documentos', 'All documents'), 'a', 'href="resources.html"') + '</div></main>'
    (root / 'transparency.html').write_text(page('IMOBX | Funding and spending', transparency,
        '<script src="assets/site.js" defer></script>', version=guide['version'], lang='pt-BR', title_pt='IMOBX | Financiamento e gastos'))

    roadmap += '<section id="governance">' + text(('Quem decide o quê?', 'Who decides what?'), 'h2')
    roadmap += text(('Uma pessoa poderia morar numa casa, trabalhar para a IMOBX e investir no projeto. Cada relação tem seus próprios direitos e responsabilidades.', 'One person could live in a home, work for IMOBX and invest in the project. Each relationship has its own rights and responsibilities.'))
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
    roadmap += links(['ica', 'ostrom'])
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
    roadmap += links(['digital']) + '</section>'

    roadmap += '<section id="ico-comparison">' + text(('Os relatórios ligariam cada etapa ao trabalho entregue.', 'Reports would connect each stage to delivered work.'), 'h2')
    roadmap += text(('O acompanhamento proposto reúne os contratos, os gastos e os resultados de cada projeto. Valores previstos, recebidos e gastos aparecem separadamente.', 'The proposed reporting brings together each project’s agreements, spending and results. Forecast, received and spent amounts are shown separately.'))
    comparison = [
        [('Imóvel e contratos', 'Property and agreements'),
         ('Direito documentado de uso do imóvel e condições de moradia.', 'Documents showing the legal right to use the property and housing terms.')],
        [('Recebimentos e gastos', 'Receipts and spending'),
         ('Origem, finalidade e comprovante de cada pagamento, com conferência por outra pessoa.', 'Source, purpose and receipt for each payment, reviewed by another person.')],
        [('Decisões', 'Decisions'),
         ('Responsável, limite de gasto e possibilidade de pedir revisão.', 'Responsible person, spending limit and a way to request review.')],
        [('Moradia entregue', 'Delivered housing'),
         ('Custos reais, reparos pendentes e avanço das famílias na compra.', 'Actual costs, unresolved repairs and households’ purchase progress.')]
    ]
    roadmap += '<div class="guide-table"><table><thead><tr>' + ''.join(text(h, 'th', 'scope="col"') for h in
        [('Área', 'Area'), ('O que o relatório mostraria', 'What the report would show')]) + '</tr></thead><tbody>'
    roadmap += ''.join('<tr>' + ''.join(text(cell, 'td') for cell in row) + '</tr>' for row in comparison)
    roadmap += '</tbody></table></div>' + links(['cash', 'cost'])
    roadmap += text(('Queremos que o dinheiro e as ferramentas ajudem a cumprir o compromisso de moradia. O primeiro projeto precisa mostrar se isso funciona e se outra equipe consegue repetir.', 'We want money and tools to help fulfill the housing commitment. The first project needs to show whether this works and whether another team can repeat it.'))
    roadmap += '</section><div class="guide-jump">' + text(('Perguntas sobre token, rede e governança ↗',
        'Questions about the token, network and governance ↗'), 'a', 'href="faq.html"')
    roadmap += text(('Whitepaper e premissas ↗', 'Whitepaper and assumptions ↗'), 'a', 'href="whitepaper.html"') + '</div></main>'
    (root / 'roadmap.html').write_text(page('IMOBX | Roadmap', roadmap,
        '<script src="assets/site.js" defer></script>', version=guide['version'], lang='pt-BR', title_pt='IMOBX | Roteiro'))

    faq_body = '<main class="paper guide-paper" id="main">' + language_controls
    faq_body += text(('Como funciona a proposta IMOBX?', 'How does the IMOBX proposal work?'), 'h1')
    faq_body += text(('Moradia, dinheiro, participação e ferramentas: o que planejamos e o que ainda falta decidir.', 'Homes, money, participation and tools: what we plan and what remains undecided.'), 'p', 'class="guide-lead"')
    faq_body += '<nav class="guide-jump" aria-label="Sections">' + text(('Roteiro', 'Roadmap'), 'a', 'href="roadmap.html"')
    faq_body += text(('Quem decide o quê?', 'Who decides what?'), 'a', 'href="roadmap.html#governance"')
    faq_body += text(('Financiamento e gastos', 'Funding and spending'), 'a', 'href="transparency.html"')
    faq_body += text(('Quem participa', 'Who takes part'), 'a', 'href="roadmap.html#participation"') + '</nav>' + faq() + '</main>'
    (root / 'faq.html').write_text(page('IMOBX | Model questions', faq_body,
        '<script src="assets/site.js" defer></script>', version=guide['version'], lang='pt-BR', title_pt='IMOBX | Perguntas sobre o modelo'))

    home = root / 'index.html'
    overview = guide['home_overview']
    housing = '<section class="content wrap solution-section" id="modelo" aria-labelledby="home-purchase-title">'
    housing += '<header class="home-model-heading">' + text(('01 / A solução em estudo', '01 / The proposed solution'), 'span', 'class="eyebrow"')
    housing += text(overview['title'], 'h2', 'id="home-purchase-title"') + text(overview['intro']) + '</header>'
    housing += '<div class="home-model-layout"><div class="home-purchase"><ol class="home-purchase-steps">'
    for step in overview['steps']:
        housing += '<li>' + text(step['title'], 'h3') + text(step['body']) + '</li>'
    housing += '</ol><aside class="home-purchase-terms" id="participation-summary">'
    housing += text(overview['terms_title'], 'h3') + text(overview['terms_status'])
    housing += '<details>' + text(overview['terms_more_title'], 'summary') + text(overview['terms_more_body']) + '</details></aside>'
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
    source, count = re.subn(r'<section class="content wrap scale-section" id="etapas">.*?</section>(?=<section class="content tint" id="digital">)',
                            lambda _: summary, home_source, count=1, flags=re.S)
    if count != 1:
        raise ValueError('Expected one homepage roadmap before the digital section.')
    source, count = re.subn(r'<div class="faq"(?: id="faq")?>.*?</div>\s*</section>',
                            lambda _: faq(home=True) + '\n </section>', source, count=1, flags=re.S)
    if count != 1:
        raise ValueError('Expected one homepage FAQ at the end of resources.')
    home.write_text(source)
