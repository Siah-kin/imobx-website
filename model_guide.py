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
            ('Perguntas sobre o modelo', 'Questions about the model'), 'h2')
        body += text(('A proposta e os critérios para decidir. Direitos e regras ainda estão em desenvolvimento.',
                      'The proposal and the criteria for deciding. Rights and rules are still in development.'))
        for item in items:
            body += f'<details id="faq-{esc(item["id"])}">' + text(item['q'], 'summary')
            body += ''.join(text(pair) for pair in item['a']) + links(item['sources']) + '</details>'
        if home:
            body += text(('Todas as perguntas: governança, The Flock, SIAH e comparação de plataformas ↗',
                          'All questions: governance, The Flock, SIAH and platform comparison ↗'),
                         'a', 'class="guide-more" href="faq.html"')
        return body + '</div>'

    summary = '<section class="content wrap scale-section" id="etapas"><span id="dinheiro"></span>'
    summary += text(('04 / Roteiro do projeto', '04 / Project roadmap'), 'span', 'class="eyebrow"')
    summary += text(('Do acordo à moradia. Da experiência à rede.',
                     'From agreements to homes. From experience to a network.'), 'h2')
    summary += text(('Preparar o piloto, acompanhar a operação e testar quais processos devem ir para blockchain. '
                     'As metas começam na data acordada pelos responsáveis; o cronograma de obra depende de financiamento, imóvel e autorizações.',
                     'Prepare the pilot, monitor operations and test which processes should move onto blockchain. '
                     'Targets start from a date agreed by the responsible people; construction timing depends on funding, property and permissions.'))
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
    roadmap += text(('Um piloto verificável. Uma comunidade com poder real de decisão.',
                     'A verifiable pilot. A community with real decision authority.'), 'p', 'class="guide-lead"')
    roadmap += text(('Proposta para consulta · 15 outubro 2026. As janelas abaixo são metas de preparação, não datas prometidas de obra ou venda. '
                     'Rafael lidera a evidência de construção e operação local; John, comunicação e coordenação digital. '
                     'Papéis contratuais e compromissos precisam ser aceitos pelos responsáveis.',
                     'Consultation proposal · 15 October 2026. The windows below are preparation targets, not promised construction or sale dates. '
                     'Rafael leads construction and local operating evidence; John leads communication and digital coordination. '
                     'Contractual roles and commitments need acceptance by the responsible people.'))
    roadmap += '<div class="guide-status">' + text(('Onde estamos', 'Where we stand'), 'h2')
    roadmap += text(('O website e os documentos estão publicados. Há estudos arquitetônicos e o orçamento de Rafael com referências CUB/SINAPI. '
                     'A estrutura jurídica final, a operação do piloto, a tesouraria onchain e o token da IMOBX não são apresentados como implantados ou verificados por esta publicação.',
                     'The website and documents are published. Architectural studies and Rafael’s CUB/SINAPI-based budget are available. '
                     'This publication does not present the final legal structure, pilot operation, onchain treasury or IMOBX token as deployed or verified.')) + '</div>'
    roadmap += '<nav class="guide-jump" aria-label="Sections">' + text(('Etapas', 'Stages'), 'a', 'href="#stages"')
    roadmap += text(('Governança', 'Governance'), 'a', 'href="#governance"')
    roadmap += text(('Reais ↔ cripto', 'BRL ↔ crypto'), 'a', 'href="#settlement"')
    roadmap += text(('Diferença da ICO', 'ICO comparison'), 'a', 'href="#ico-comparison"')
    roadmap += text(('Perguntas', 'Questions'), 'a', 'href="faq.html"') + '</nav>'
    roadmap += '<section id="stages">' + text(('Etapas e condições para avançar', 'Stages and conditions for advancing'), 'h2')
    for i, stage in enumerate(guide['stages'], 1):
        roadmap += f'<article class="roadmap-stage" id="{esc(stage["id"])}"><span class="eyebrow">{i:02}</span>'
        roadmap += text(stage['title'], 'h3') + text(stage['window'], 'p', 'class="guide-window"')
        roadmap += '<dl>'
        for label, key in [(('Responsáveis propostos', 'Proposed owners'), 'lead'),
                           (('Trabalho', 'Work'), 'work'),
                           (('Para avançar', 'To advance'), 'gate'),
                           (('Website e comunicação', 'Website and communication'), 'web')]:
            roadmap += text(label, 'dt') + text(stage[key], 'dd')
        roadmap += '</dl></article>'
    roadmap += '</section>'

    # These diagrams describe proposed money/contract paths, not a payment API.
    settlement = guide['settlement']
    roadmap += '<section id="settlement">' + text(settlement['title'], 'h2')
    roadmap += text(settlement['intro'])
    roadmap += '<div class="settlement-history">' + text(settlement['historical_title'], 'h3')
    roadmap += text(settlement['historical_route'], 'p', 'class="settlement-chain"')
    roadmap += text(settlement['historical_note']) + '</div>'
    for route in settlement['routes']:
        roadmap += f'<article class="settlement-route" id="{esc(route["id"])}">' + text(route['title'], 'h3')
        roadmap += text(route['intro']) + '<ol class="settlement-steps">'
        for step in route['steps']:
            roadmap += '<li><div>' + text(step['title'], 'strong') + text(step['body']) + '</div></li>'
        roadmap += '</ol>' + text(route['note'], 'p', 'class="fine"') + '</article>'
    roadmap += text(settlement['relationships_title'], 'h3')
    roadmap += '<div class="settlement-relationships">'
    for relationship in settlement['relationships']:
        roadmap += '<article>' + text(relationship['title'], 'h3') + text(relationship['body']) + '</article>'
    roadmap += '</div>' + text(settlement['registration']) + links(['cnpj', 'title'])
    roadmap += '<div class="settlement-review">' + text(settlement['provider_title'], 'h3')
    roadmap += text(settlement['provider_note']) + links(['mb']) + '</div>'
    roadmap += text(settlement['network_note']) + links(['bcb'])
    research = settlement['provider_research']
    roadmap += '<section id="ramp-options">' + text(research['title'], 'h3')
    roadmap += text(research['conclusion']) + text(research['lean_pilot'])
    for option in research['routes']:
        roadmap += '<article class="settlement-option">' + text(option['title'], 'h3')
        roadmap += text(option['flow'], 'p', 'class="settlement-chain"') + text(option['fit'])
        roadmap += links(option['sources']) + '</article>'
    roadmap += '<div class="guide-table"><table><thead><tr>' + ''.join(text(h, 'th', 'scope="col"') for h in
        [('Opção', 'Option'), ('O que a documentação confirma', 'What documentation confirms'),
         ('Adequação à IMOBX', 'Fit for IMOBX')]) + '</tr></thead><tbody>'
    for provider in research['providers']:
        roadmap += '<tr><th scope="row">' + esc(provider['name']) + '</th><td>' + text(provider['supported'])
        roadmap += links(provider['sources']) + '</td><td>' + text(provider['fit']) + '</td></tr>'
    roadmap += '</tbody></table></div>'
    roadmap += text(research['cost']) + links(['blind-price']) + text(research['acceptance_title'], 'h3')
    roadmap += '<ul>' + ''.join(text(p, 'li') for p in research['acceptance']) + '</ul>'
    roadmap += text(research['status'], 'p', 'class="fine"') + '</section>'
    roadmap += text(settlement['evidence_title'], 'h3')
    roadmap += '<ul>' + ''.join(text(x, 'li') for x in settlement['evidence']) + '</ul>'
    roadmap += text(settlement['limits']) + links(['cash', 'nonprofit']) + '</section>'

    roadmap += '<section id="governance">' + text(('Quem decide o quê?', 'Who decides what?'), 'h2')
    roadmap += text(('Exemplo para consulta, não um estatuto já adotado. O objetivo é separar a voz de quem usa a moradia, '
                     'a responsabilidade de quem trabalha e os direitos de quem financia. Uma mesma pessoa pode ocupar mais de um papel.',
                     'An example for consultation, not an adopted charter. The aim is to separate the voice of housing users, '
                     'the responsibility of people doing the work and the rights of funders. One person can occupy more than one role.'))
    headings = [('Decisão', 'Decision'), ('Autoridade proposta', 'Proposed authority'), ('Limite e controle', 'Boundary and check')]
    rows = [
        [('Moradia e compra', 'Occupancy and purchase'),
         ('Morador e entidade, pelo contrato e pela lei.', 'Resident and entity, through agreement and law.'),
         ('Votos de token não alteram unilateralmente direitos contratados; há contestação e recurso.',
          'Token votes cannot unilaterally alter contracted rights; challenges and appeals remain available.')],
        [('Uso de espaços e manutenção local', 'Shared spaces and local maintenance'),
         ('Moradores com voz igual por membro verificado, como opção a consultar.',
          'Residents with equal voice per verified member, as an option to consult on.'),
         ('Orçamento aprovado; deveres de segurança; participação assistida; representantes substituíveis.',
          'Accepted budget; safety duties; assisted participation; replaceable representatives.')],
        [('Execução e compras', 'Delivery and purchasing'),
         ('Pessoas eleitas ou nomeadas por experiência relevante, com mandato definido.',
          'People elected or appointed for relevant experience, with a defined mandate.'),
         ('O construtor não aprova a própria cobrança. Autorização, verificação e pagamento têm controles separados.',
          'A builder does not approve their own invoice. Authorization, verification and payment have separate checks.')],
        [('Capital e eventual rendimento', 'Capital and any financial return'),
         ('Titulares têm somente os direitos financeiros e de decisão previstos no instrumento.',
          'Holders have the financial and decision rights specified by the instrument.'),
         ('Comprar tokens não compra automaticamente o controle dos moradores. Restrições de doação e contratos são preservados.',
          'Buying tokens does not automatically buy control over residents. Donation restrictions and agreements remain protected.')],
        [('Expansão e regras da rede', 'Expansion and network rules'),
         ('Órgãos definidos no estatuto, com representação local e prestação de contas.',
          'Bodies defined in the charter, with local representation and reporting.'),
         ('Quórum, poderes reservados, conflitos, troca de operadores e revisão precisam ser aceitos antes da automação.',
          'Quorum, reserved powers, conflicts, operator replacement and review need agreement before automation.')]
    ]
    roadmap += '<div class="guide-table"><table><thead><tr>' + ''.join(text(h, 'th', 'scope="col"') for h in headings)
    roadmap += '</tr></thead><tbody>'
    for row in rows:
        roadmap += '<tr>' + ''.join(text(cell, 'td') for cell in row) + '</tr>'
    roadmap += '</tbody></table></div>'
    roadmap += text(('O mérito pode orientar a seleção para uma função com responsabilidade; não precisa transformar atividade online em poder de voto. '
                     'Para evitar outra elite, testar mandatos, revisão, acesso de novos membros, conflitos e substituição. '
                     'Representação, quórum e proteção da voz dos moradores ainda precisam ser definidos com os participantes.',
                     'Merit can inform selection for a responsible role; it need not turn online activity into voting power. '
                     'To avoid another elite, test mandates, review, newcomer access, conflicts and replacement. '
                     'Representation, quorum and protection of resident voice still need definition with participants.'))
    roadmap += links(['ica', 'ostrom'])
    roadmap += text(('Aplicando Ostrom ao piloto', 'Applying Ostrom to the pilot'), 'h3')
    principles = [
        ('Limites: definir membros, imóveis, recursos compartilhados e direitos individuais.',
         'Boundaries: define members, properties, shared resources and individual rights.'),
        ('Adequação local: ajustar custos, contribuições e benefícios às condições reais das famílias.',
         'Local fit: adapt costs, contributions and benefits to households’ actual circumstances.'),
        ('Escolha coletiva: pessoas afetadas participam da mudança das regras que lhes cabem.',
         'Collective choice: affected people participate in changing the rules within their authority.'),
        ('Fiscalização: quem verifica recursos e trabalho responde aos usuários, com conflitos declarados.',
         'Monitoring: people checking resources and work answer to users, with declared conflicts.'),
        ('Respostas proporcionais: tratar descumprimentos com critérios, contexto e direito de resposta.',
         'Proportionate responses: handle breaches with criteria, context and an opportunity to respond.'),
        ('Conflitos: oferecer mediação acessível e recurso; preservar as proteções legais da moradia.',
         'Conflicts: provide accessible mediation and appeals; preserve legal housing protections.'),
        ('Autoridade reconhecida: dar base jurídica aos poderes e responsabilidades acordados.',
         'Recognized authority: give agreed powers and responsibilities a legal foundation.'),
        ('Camadas: resolver assuntos locais perto dos moradores e coordenar serviços comuns entre projetos.',
         'Layers: resolve local matters close to residents and coordinate shared services across projects.')
    ]
    roadmap += '<ol class="ostrom-application">' + ''.join(text(p, 'li') for p in principles) + '</ol>'
    roadmap += text(('Estas são aplicações propostas à IMOBX. Ostrom não prescreveu tokenomics nem um único sistema de votação. '
                     'O teste inclui uma decisão de rotina, uma urgência, uma cobrança contestada e uma proposta de expansão. '
                     'Cada caso deve identificar quem propõe, autoriza, executa, confere e pode recorrer.',
                     'These are proposed IMOBX applications. Ostrom prescribed neither tokenomics nor a single voting system. '
                     'The trial includes a routine decision, an emergency, a challenged invoice and an expansion proposal. '
                     'Each case must identify who proposes, authorizes, executes, checks and can appeal.'))
    roadmap += text(('O papel das ferramentas', 'The role of the tools'), 'h3')
    roadmap += text(('The Flock deve permitir enviar dúvidas, solicitações e propostas e consultar regras e respostas aprovadas. '
                     'O papel proposto para SIAH/HiveDAO é apoiar evidências, trabalho delegado e coordenação, sujeito a desenvolvimento separado. '
                     'Essas ferramentas não escolhem quem tem direito à casa, não fixam a constituição e não substituem julgamento responsável. '
                     'A comunidade precisa conseguir trocar prestadores e continuar operando durante uma falha.',
                     'The Flock should let people send questions, requests and proposals and read approved rules and responses. '
                     'The proposed SIAH/HiveDAO role supports evidence, delegated work and coordination, subject to separate development. '
                     'These tools neither choose who is entitled to a home, set the constitution nor replace accountable judgment. '
                     'The community needs to be able to replace providers and keep operating during an outage.'))
    roadmap += links(['digital']) + '</section>'

    roadmap += '<section id="ico-comparison">' + text(('O que muda em relação à venda de tokens?', 'What changes compared with a token sale?'), 'h2')
    roadmap += text(('ICO descreve uma forma de levantar capital, não um único modelo de negócio. '
                     'A comparação abaixo mostra um percurso comum de venda para financiar um produto futuro e a sequência que propomos para IMOBX. '
                     'Não afirma que toda ICO seja igual nem que a proposta dispense as regras de oferta.',
                     'ICO describes a capital-raising method, not one business model. '
                     'The comparison below shows a common sale-to-finance-a-future-product journey and IMOBX’s proposed sequence. '
                     'It does not claim all ICOs are alike or that the proposal avoids offering requirements.'))
    comparison = [
        [('Ponto de partida', 'Starting point'), ('Venda financia a construção do produto futuro.', 'A sale finances the future product.'),
         ('Organizar contratos, imóvel, orçamento e poderes; decidir o instrumento com essa base.', 'Organize agreements, property, budget and powers; decide the instrument using that foundation.')],
        [('Fonte de resultado', 'Source of surplus'), ('Depende do projeto; o preço do token não demonstra receita.', 'Project-dependent; token price does not demonstrate income.'),
         ('Recebimentos identificados, custos, reservas e obrigações; eventual rendimento só com direito e caixa disponíveis.', 'Identified receipts, costs, reserves and obligations; any yield requires entitlement and available cash.')],
        [('Poder', 'Authority'), ('Direitos definidos pela oferta e pelo protocolo; algumas usam voto por saldo.', 'Rights defined by the offer and protocol; some use balance-weighted votes.'),
         ('Consultar direitos distintos de moradores, executores e financiadores, com limites e recurso.', 'Consult on distinct resident, delivery and funder rights, with boundaries and appeals.')],
        [('Progresso', 'Progress'), ('Marcos de produto e de mercado escolhidos pelo emissor.', 'Product and market milestones selected by the issuer.'),
         ('Entregas, custo total, conciliação, reservas e avanço contratual dos moradores.', 'Delivery, full cost, reconciliation, reserves and residents’ contractual progress.')]
    ]
    roadmap += '<div class="guide-table"><table><thead><tr>' + ''.join(text(h, 'th', 'scope="col"') for h in
        [('Aspecto', 'Aspect'), ('Percurso comum de ICO', 'A common ICO journey'), ('Direção IMOBX', 'IMOBX direction')]) + '</tr></thead><tbody>'
    roadmap += ''.join('<tr>' + ''.join(text(cell, 'td') for cell in row) + '</tr>' for row in comparison)
    roadmap += '</tbody></table></div>' + links(['ico', 'cvm'])
    roadmap += text(('A diferença pretendida é alinhar capital e tecnologia a uma obrigação de moradia e a uma comunidade que participa. '
                     'Seu valor será demonstrado pelo piloto, pelos direitos executáveis e pela operação repetível.',
                     'The intended difference is to align capital and technology with a housing commitment and a participating community. '
                     'Its value will be demonstrated through the pilot, enforceable rights and repeatable operations.'))
    roadmap += '</section><div class="guide-jump">' + text(('Perguntas sobre token, rede e governança ↗',
        'Questions about the token, network and governance ↗'), 'a', 'href="faq.html"')
    roadmap += text(('Whitepaper e premissas ↗', 'Whitepaper and assumptions ↗'), 'a', 'href="whitepaper.html"') + '</div></main>'
    (root / 'roadmap.html').write_text(page('IMOBX | Roadmap', roadmap,
        '<script src="assets/site.js" defer></script>', lang='pt-BR', title_pt='IMOBX | Roteiro'))

    faq_body = '<main class="paper guide-paper" id="main">' + language_controls
    faq_body += text(('Como funciona a proposta IMOBX?', 'How does the IMOBX proposal work?'), 'h1')
    faq_body += text(('Moradia, dinheiro, participação e tecnologia — com as escolhas em aberto identificadas.',
                      'Housing, money, participation and technology — with open choices identified.'), 'p', 'class="guide-lead"')
    faq_body += '<nav class="guide-jump" aria-label="Sections">' + text(('Roteiro', 'Roadmap'), 'a', 'href="roadmap.html"')
    faq_body += text(('Quem decide o quê?', 'Who decides what?'), 'a', 'href="roadmap.html#governance"')
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
