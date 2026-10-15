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
        if home:
            body += text(('Mais perguntas sobre moradia, dinheiro e decisões ↗', 'More questions about homes, money and decisions ↗'),
                         'a', 'class="guide-more" href="faq.html"')
        return body + '</div>'

    summary = '<section class="content wrap scale-section" id="etapas"><span id="dinheiro"></span>'
    summary += text(('04 / Roteiro do projeto', '04 / Project roadmap'), 'span', 'class="eyebrow"')
    summary += text(('Começar com um projeto. Aprender a construir mais.', 'Start with one project. Learn how to build more.'), 'h2')
    summary += text(('Preparar o primeiro projeto, acompanhar os resultados e testar onde a blockchain ajuda. Os prazos contam a partir de uma data combinada. A obra depende do imóvel, do dinheiro e das autorizações.', 'Prepare the first project, follow the results and test where blockchain helps. The timetable starts from an agreed date. Building depends on the property, funding and permissions.'))
    summary += '<ol class="roadmap-overview">'
    for i, stage in enumerate(guide['stages'], 1):
        summary += f'<li><span class="roadmap-number">{i:02}</span><div>'
        summary += text(stage['title'], 'h3') + text(stage['window'], 'p', 'class="fine"')
        summary += '</div></li>'
    summary += '</ol>' + text(('Ver responsáveis, entregas e critérios para avançar ↗',
                              'See owners, deliverables and criteria for advancing ↗'),
                             'a', 'class="button" href="roadmap.html"') + '</section>'

    roadmap = '<main class="paper guide-paper" id="main">' + language_controls
    roadmap += text(('Roteiro IMOBX', 'IMOBX roadmap'), 'h1')
    roadmap += text(('Um primeiro projeto que as pessoas possam acompanhar e ajudar a decidir.', 'A first project people can follow and help shape.'), 'p', 'class="guide-lead"')
    roadmap += text(('Plano para discussão · 15 de outubro de 2026. São metas de preparação; não são datas prometidas de obra ou venda. Rafael cuida da construção e das informações locais; John, da comunicação e das ferramentas digitais. Cada responsável precisa aceitar seu papel.', 'Plan for discussion · 15 October 2026. These are preparation targets, not promised building or sale dates. Rafael handles construction and local information; John handles communication and digital tools. Each person needs to agree to their role.'))
    roadmap += '<div class="guide-status">' + text(('Onde estamos', 'Where we stand'), 'h2')
    roadmap += text(('O site, os documentos, os desenhos e o orçamento de Rafael já estão disponíveis. Ainda precisamos confirmar a estrutura jurídica e mostrar o piloto, o caixa na blockchain e o token da IMOBX em funcionamento.', 'The site, documents, drawings and Rafael’s budget are available. We still need to confirm the legal structure and demonstrate the pilot, blockchain-held funds and IMOBX token in use.')) + '</div>'
    roadmap += '<nav class="guide-jump" aria-label="Sections">' + text(('Etapas', 'Stages'), 'a', 'href="#stages"')
    roadmap += text(('Decisões compartilhadas', 'Shared decisions'), 'a', 'href="#governance"')
    roadmap += text(('Transparência', 'Transparency'), 'a', 'href="transparency.html"')
    roadmap += text(('Diferença da ICO', 'ICO comparison'), 'a', 'href="#ico-comparison"')
    roadmap += text(('Perguntas', 'Questions'), 'a', 'href="faq.html"') + '</nav>'
    roadmap += '<section id="stages">' + text(('Etapas e o que precisa estar pronto', 'Steps and what needs to be ready'), 'h2')
    for i, stage in enumerate(guide['stages'], 1):
        roadmap += f'<article class="roadmap-stage" id="{esc(stage["id"])}"><span class="eyebrow">{i:02}</span>'
        roadmap += text(stage['title'], 'h3') + text(stage['window'], 'p', 'class="guide-window"')
        roadmap += '<dl>'
        for label, key in [(('Quem faria', 'Who would do it'), 'lead'),
                           (('Trabalho', 'Work'), 'work'),
                           (('Antes da próxima etapa', 'Before the next step'), 'gate'),
                           (('O que mostrar no site', 'What to show on the site'), 'web')]:
            roadmap += text(label, 'dt') + text(stage[key], 'dd')
        roadmap += '</dl></article>'
    roadmap += '</section>'

    # Keep old shared anchors usable while linking the single detailed reading page.
    roadmap += '<section id="settlement"><span id="ramp-options"></span>' + text(
        ('Dinheiro e transparência', 'Money and transparency'), 'h2')
    roadmap += text(('Veja como o dinheiro passaria de reais para USDC e voltaria, quais empresas pesquisamos e o que falta confirmar.', 'See how money would move from reais to USDC and back, which companies we researched and what needs confirming.'))
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
    settlement_html += '<div class="settlement-review">' + text(settlement['provider_title'], 'h3')
    settlement_html += text(settlement['provider_note']) + links(['mb']) + '</div>'
    settlement_html += text(settlement['network_note']) + links(['bcb'])
    research = settlement['provider_research']
    settlement_html += '<section id="ramp-options">' + text(research['title'], 'h3')
    settlement_html += text(research['conclusion']) + text(research['lean_pilot'])
    for option in research['routes']:
        settlement_html += '<article class="settlement-option">' + text(option['title'], 'h3')
        settlement_html += text(option['flow'], 'p', 'class="settlement-chain"') + text(option['fit'])
        settlement_html += links(option['sources']) + '</article>'
    settlement_html += '<div class="guide-table"><table><thead><tr>' + ''.join(text(h, 'th', 'scope="col"') for h in
        [('Opção', 'Option'), ('O que as empresas descrevem', 'What the companies describe'),
         ('Adequação à IMOBX', 'Fit for IMOBX')]) + '</tr></thead><tbody>'
    for provider in research['providers']:
        settlement_html += '<tr><th scope="row">' + esc(provider['name']) + '</th><td>' + text(provider['supported'])
        settlement_html += links(provider['sources']) + '</td><td>' + text(provider['fit']) + '</td></tr>'
    settlement_html += '</tbody></table></div>'
    settlement_html += text(research['cost']) + links(['blind-price']) + text(research['acceptance_title'], 'h3')
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
    for label, target in [(('Economia comunitária', 'Community economy'), 'community-economy'),
                          (('Fluxos', 'Flows'), 'settlement'),
                          (('Prestadores', 'Providers'), 'ramp-options'),
                          (('Próximos passos', 'Next steps'), 'next-steps'),
                          (('Relatórios', 'Reports'), 'reporting'),
                          (('Fontes', 'Sources'), 'sources'),
                          (('Atualizações', 'Updates'), 'updates')]:
        transparency += text(label, 'a', f'href="#{target}"')
    transparency += '</nav>'
    economy = guide['community_economy']
    transparency += '<section id="community-economy">' + text(economy['title'], 'h2')
    transparency += text(economy['intro']) + text(economy['status'], 'p', 'class="guide-status"')
    for topic in economy['topics']:
        transparency += f'<details class="community-topic" id="{esc(topic["id"])}">' + text(topic['title'], 'summary')
        transparency += ''.join(text(pair) for pair in topic['body']) + links(topic['sources']) + '</details>'
    transparency += '</section>'
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
    (root / 'transparency.html').write_text(page('IMOBX | Money and transparency', transparency,
        '<script src="assets/site.js" defer></script>', lang='pt-BR', title_pt='IMOBX | Dinheiro e transparência'))

    roadmap += '<section id="governance">' + text(('Quem decide o quê?', 'Who decides what?'), 'h2')
    roadmap += text(('Proposta para discutir com a comunidade. Uma pessoa pode morar, trabalhar e investir no mesmo projeto. Precisamos deixar claro o que cada papel permite decidir.', 'A proposal to discuss with the community. One person may live, work and invest in the same project. We need to make clear what each role may decide.'))
    headings = [('Decisão', 'Decision'), ('Quem decidiria', 'Who would decide'), ('Limites e conferências', 'Limits and checks')]
    rows = [
        [('Moradia e compra', 'Occupancy and purchase'),
         ('Morador e entidade, pelo contrato e pela lei.', 'Resident and entity, through agreement and law.'),
         ('Uma votação de tokens não muda sozinha o contrato da família. É preciso poder questionar e pedir revisão.', 'A token vote cannot change a family’s agreement on its own. People need a way to question a decision and ask for review.')],
        [('Uso de espaços e manutenção local', 'Shared spaces and local maintenance'),
         ('Uma opção para discutir: voz igual para cada membro do grupo de moradores.', 'One option to discuss: equal voice for each member of the resident group.'),
         ('Respeitar o orçamento e a segurança, oferecer ajuda para participar e permitir trocar os representantes.', 'Follow the budget and safety rules, help people take part and allow representatives to be replaced.')],
        [('Execução e compras', 'Delivery and purchasing'),
         ('Pessoas escolhidas pela experiência, com função e prazo claros.', 'People chosen for their experience, with a clear job and time limit.'),
         ('A construtora não aprova a própria cobrança. Aprovar o gasto, conferir a entrega e pagar são tarefas com conferências separadas.', 'The builder does not approve its own invoice. Approving spending, checking delivery and paying need separate checks.')],
        [('Investimento e possíveis pagamentos', 'Investment and possible payments'),
         ('Quem investe recebe somente os direitos escritos no seu acordo.', 'Investors receive only the rights written in their agreement.'),
         ('Comprar tokens não dá controle automático sobre moradores. Os contratos e o uso combinado das doações continuam valendo.', 'Buying tokens does not give automatic control over residents. Agreements and the stated purpose of donations still apply.')],
        [('Expansão e regras da rede', 'Expansion and network rules'),
         ('Grupos definidos nas regras da organização, com representantes locais e contas abertas à conferência.', 'Groups defined in the organization’s rules, with local representatives and accounts people can check.'),
         ('Combinar quantas pessoas precisam votar, quem decide cada assunto e como resolver conflitos e trocar responsáveis.', 'Agree how many people must vote, who decides each issue, and how to resolve disputes and replace responsible people.')]
    ]
    roadmap += '<div class="guide-table"><table><thead><tr>' + ''.join(text(h, 'th', 'scope="col"') for h in headings)
    roadmap += '</tr></thead><tbody>'
    for row in rows:
        roadmap += '<tr>' + ''.join(text(cell, 'td') for cell in row) + '</tr>'
    roadmap += '</tbody></table></div>'
    roadmap += text(('O trabalho já feito pode ajudar a escolher alguém para uma função. Isso não precisa virar votos por atividade online. A comunidade precisa decidir os prazos, as formas de revisão e como novos moradores podem participar.', 'Past work can help the community choose someone for a role. It does not need to become votes for online activity. The community needs to agree time limits, review and how newcomers can participate.'))
    roadmap += links(['ica', 'ostrom'])
    roadmap += text(('Aplicando Ostrom ao piloto', 'Applying Ostrom to the pilot'), 'h3')
    principles = [
        ('Quem participa? Definir os membros, os imóveis, o que é compartilhado e o que pertence a cada família.', 'Who takes part? Agree the members, properties, shared resources and what belongs to each family.'),
        ('O que cabe na vida local? Ajustar custos e responsabilidades ao que as famílias podem fazer e pagar.', 'What fits local life? Match costs and responsibilities to what families can do and afford.'),
        ('Quem muda as regras? As pessoas afetadas participam das decisões que lhes cabem.', 'Who changes the rules? People affected take part in the decisions within their role.'),
        ('Quem confere? Quem verifica dinheiro e trabalho presta contas aos participantes e declara interesses próprios.', 'Who checks? People checking money and work report to participants and disclose their own interests.'),
        ('E se uma regra for descumprida? Ouvir a pessoa, considerar a gravidade e dar uma resposta proporcional.', 'What if a rule is broken? Hear the person, consider how serious it is and respond fairly.'),
        ('Como resolver uma discussão? Oferecer mediação e revisão acessíveis, preservando os direitos de moradia.', 'How are disputes resolved? Offer accessible mediation and review while protecting housing rights.'),
        ('As regras têm validade? Dar base jurídica às responsabilidades e decisões combinadas.', 'Do the rules carry legal weight? Give agreed responsibilities and decisions a legal basis.'),
        ('O que fica perto dos moradores? Resolver assuntos locais no próprio projeto e compartilhar os serviços que ajudam vários projetos.', 'What stays close to residents? Handle local matters in each project and share services that help several projects.')
    ]
    roadmap += '<ol class="ostrom-application">' + ''.join(text(p, 'li') for p in principles) + '</ol>'
    roadmap += text(('Estas perguntas adaptam as ideias de Ostrom à IMOBX. Ostrom estudou como pessoas cuidam de recursos comuns; não criou um modelo de token. Vamos ensaiar um reparo, uma urgência, uma cobrança contestada e uma nova obra. Em cada caso: quem pede, aprova, faz, confere e pode questionar?', 'These questions apply Ostrom’s ideas to IMOBX. Ostrom studied how people manage shared resources; she did not create a token model. We will walk through a repair, an emergency, a disputed invoice and a new build. In each case: who asks, approves, acts, checks and may challenge?'))
    roadmap += text(('Como o trabalho segue no dia a dia', 'How everyday work moves forward'), 'h3')
    for key in ['work', 'example', 'continuity', 'status']:
        roadmap += text(guide['dao_operations'][key])
    roadmap += links(['digital']) + '</section>'

    roadmap += '<section id="ico-comparison">' + text(('O que muda em relação à venda de tokens?', 'What changes compared with a token sale?'), 'h2')
    roadmap += text(('Uma ICO é uma venda inicial de tokens para arrecadar dinheiro. A tabela compara uma venda para financiar um produto futuro com o caminho que propomos. Projetos de ICO variam; a IMOBX também precisa seguir as regras de uma eventual oferta.', 'An ICO is an initial token sale to raise money. This table compares selling to fund a future product with our proposed path. ICO projects vary; IMOBX also needs to follow the rules for any future offer.'))
    comparison = [
        [('Ponto de partida', 'Starting point'), ('Venda financia a construção do produto futuro.', 'A sale finances the future product.'),
         ('Definir imóvel, contratos, orçamento e responsáveis. Depois decidir se haverá token.', 'Agree the property, contracts, budget and responsible people. Then decide whether to use a token.')],
        [('De onde vem o dinheiro que sobra', 'Where money left over comes from'), ('Depende do projeto; o preço do token não demonstra receita.', 'Project-dependent; token price does not demonstrate income.'),
         ('Mostrar entradas, contas e dinheiro guardado. Qualquer pagamento exige dinheiro disponível e direito escrito.', 'Show income, bills and money set aside. Any payout needs available money and written rights.')],
        [('As regras da oferta definem os direitos; alguns projetos dão mais votos a quem tem mais tokens.', 'The offer defines rights; some projects give more votes to people with more tokens.'), ('As regras da oferta definem os direitos; alguns projetos dão mais votos a quem tem mais tokens.', 'The offer defines rights; some projects give more votes to people with more tokens.'),
         ('Combinar o que moradores, equipes e investidores podem decidir e como pedir revisão.', 'Agree what residents, teams and investors may decide and how to ask for review.')],
        [('Progresso', 'Progress'), ('Marcos de produto e de mercado escolhidos pelo emissor.', 'Product and market milestones selected by the issuer.'),
         ('Mostrar casas entregues, custos reais, contas conferidas e avanço das famílias na compra.', 'Show homes delivered, actual costs, checked accounts and families’ progress toward purchase.')]
    ]
    roadmap += '<div class="guide-table"><table><thead><tr>' + ''.join(text(h, 'th', 'scope="col"') for h in
        [('Aspecto', 'Aspect'), ('Percurso comum de ICO', 'A common ICO journey'), ('Direção IMOBX', 'IMOBX direction')]) + '</tr></thead><tbody>'
    roadmap += ''.join('<tr>' + ''.join(text(cell, 'td') for cell in row) + '</tr>' for row in comparison)
    roadmap += '</tbody></table></div>' + links(['ico', 'cvm'])
    roadmap += text(('Queremos que o dinheiro e as ferramentas ajudem a cumprir o compromisso de moradia. O primeiro projeto precisa mostrar se isso funciona e se outra equipe consegue repetir.', 'We want money and tools to help fulfill the housing commitment. The first project needs to show whether this works and whether another team can repeat it.'))
    roadmap += '</section><div class="guide-jump">' + text(('Perguntas sobre token, rede e governança ↗',
        'Questions about the token, network and governance ↗'), 'a', 'href="faq.html"')
    roadmap += text(('Whitepaper e premissas ↗', 'Whitepaper and assumptions ↗'), 'a', 'href="whitepaper.html"') + '</div></main>'
    (root / 'roadmap.html').write_text(page('IMOBX | Roadmap', roadmap,
        '<script src="assets/site.js" defer></script>', lang='pt-BR', title_pt='IMOBX | Roteiro'))

    faq_body = '<main class="paper guide-paper" id="main">' + language_controls
    faq_body += text(('Como funciona a proposta IMOBX?', 'How does the IMOBX proposal work?'), 'h1')
    faq_body += text(('Moradia, dinheiro, participação e ferramentas: o que planejamos e o que ainda falta decidir.', 'Homes, money, participation and tools: what we plan and what remains undecided.'), 'p', 'class="guide-lead"')
    faq_body += '<nav class="guide-jump" aria-label="Sections">' + text(('Roteiro', 'Roadmap'), 'a', 'href="roadmap.html"')
    faq_body += text(('Quem decide o quê?', 'Who decides what?'), 'a', 'href="roadmap.html#governance"')
    faq_body += text(('Dinheiro e transparência', 'Money and transparency'), 'a', 'href="transparency.html"')
    faq_body += text(('Comparar plataformas', 'Compare platforms'), 'a', 'href="#faq-exchanges"') + '</nav>' + faq() + '</main>'
    (root / 'faq.html').write_text(page('IMOBX | Model questions', faq_body,
        '<script src="assets/site.js" defer></script>', lang='pt-BR', title_pt='IMOBX | Perguntas sobre o modelo'))

    home = root / 'index.html'
    source, count = re.subn(r'<section class="content wrap scale-section" id="etapas">.*?</section>(?=<section class="content tint" id="digital">)',
                            lambda _: summary, home.read_text(), count=1, flags=re.S)
    if count != 1:
        raise ValueError('Expected one homepage roadmap before the digital section.')
    source, count = re.subn(r'<div class="faq"(?: id="faq")?>.*?</div>\s*</section>',
                            lambda _: faq(home=True) + '\n </section>', source, count=1, flags=re.S)
    if count != 1:
        raise ValueError('Expected one homepage FAQ at the end of resources.')
    home.write_text(source)
