"""The About page: why IMOBX exists, who started it, what it wants to build, how it would work, where it stands.

Owner, 8 Nov 2026: the site lacked the why; the draft (ABOUT_PAGE_DRAFT_2026-11-08.md, reviewed) approved with
"publish", and Rafael's OK to use his story here. Each why has one home; this page is the home of "why IMOBX".
"""


from page_frame import term_scripts


def build_about(root, page, tr, esc):
    def t(pair, tag='p', attrs=''):
        return tr(*pair, tag, attrs)

    def linked(*parts, attrs=''):
        out = f'<p{attrs}>'
        for i, part in enumerate(parts):
            out += (' ' if i and not part[1][:1] in '.,;:' else '') + (t(part[:2], 'a', f'href="{esc(part[2])}"') if len(part) == 3 else t(part, 'span'))
        return out + '</p>'

    b = '<main class="paper about-page" id="main">'
    b += t(('Sobre a IMOBX', 'About IMOBX'), 'h1')

    b += '<section id="why">' + t(('Por que a IMOBX existe?', 'Why does IMOBX exist?'), 'h2')
    b += t(('Construir um lar é uma busca existencial de todo ser humano, onde quer que esteja.',
            'Creating a home is an existential quest for every human, wherever you are.'), 'p', 'class="about-lead"')
    b += linked(('Em 2024,', 'In 2024,'),
                ('o déficit habitacional do Brasil', 'Brazil’s housing deficit', 'why.html'),
                ('era de cerca de 5,77 milhões de domicílios, segundo a', 'was about 5.77 million households, according to the'),
                ('Fundação João Pinheiro', 'Fundação João Pinheiro', 'https://fjp.mg.gov.br/deficit-habitacional-recua-34-no-brasil-e-soma-5-773-983-domicilios/'),
                ('. Desses, cerca de 3,59 milhões (62%) eram domicílios urbanos com renda de até três salários mínimos que gastam mais de 30% da renda com aluguel.',
                 '. Of those, about 3.59 million (62%) were urban households earning up to three minimum wages that spend more than 30% of their income on rent.'))
    b += linked(('Nos 12 meses até setembro de 2026, os preços pedidos para novos aluguéis subiram 9,13%, o dobro da inflação oficial de 4,58%, segundo o', 'In the 12 months to September 2026, asking rents for new rentals rose 9.13%, twice the official inflation of 4.58%, according to the'),
                ('índice FipeZAP', 'FipeZAP index', 'https://diariodocomercio.com.br/economia/aluguel-sobe-dobro-inflacao-2026/'),
                ('. O índice acompanha os preços pedidos nos anúncios de 36 cidades.', '. The index follows asking prices in listings across 36 cities.'))
    b += linked(('O Censo 2022', 'The 2022 Census', 'https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/41797-censo-2022-brasil-tinha-16-4-milhoes-de-pessoas-morando-em-favelas-e-comunidades-urbanas'),
                ('contou cerca de 16,4 milhões de pessoas morando em favelas e comunidades urbanas: um em cada doze brasileiros.',
                 'counted about 16.4 million people living in favelas and urban communities: one in every twelve Brazilians.'))
    b += '</section>'

    b += '<section id="founders">' + t(('Quem começou a IMOBX, e por quê?', 'Who started IMOBX, and why?'), 'h2') + '<div class="about-founders">'
    b += ('<figure class="about-founder"><blockquote>'
          + t(('Minha infância me ensinou cedo o valor de cada centavo e de um teto seguro. Meu pai foi ausente, e minha mãe sustentava a casa trabalhando de 70 a 80 horas por semana para criar três filhos. Nunca desisti de um sonho que carrego desde a faculdade: construir boas moradias, de padrão modesto ou acessível, para que as famílias mais pobres possam de novo realizar o sonho da casa própria. Porque todo brasileiro sonha com isso.',
                 'My childhood taught me early the value of every cent and of a safe roof. My father was absent, and my mother supported the household working 70 to 80 hours a week to raise three children. I never gave up a dream I have carried since university: to build good homes, of modest or affordable standard, so that the poorest families can once again fulfil the dream of owning their own home. Because every Brazilian dreams of that.'))
          + t(('Ninguém gosta de pagar aluguel, de criar raízes num lugar e um dia ter que sair porque a casa não é sua. Quando a vida aperta, a primeira coisa que queremos é entrar na nossa caverna e nos proteger. A pergunta que não sai da minha cabeça é simples: por que ter a própria caverna não é um direito de todos? A IMOBX é a minha resposta a essa pergunta.',
                 'Nobody likes to rent, to put down roots in a place and one day have to leave because the home isn’t theirs. When life gets hard, the first thing we want is to go into our cave and protect ourselves. The question that won’t leave my mind is simple: why isn’t having one’s own cave a right for everyone? IMOBX is my answer to that question.'))
          + '</blockquote><figcaption>' + t(('Rafael, cofundador e engenheiro civil, Rio de Janeiro', 'Rafael, co-founder and civil engineer, Rio de Janeiro'), 'span') + '</figcaption>'
          + '<p class="about-founder-link">' + t(('As obras do Rafael', 'Rafael’s building work'), 'a', 'href="properties.html"') + '</p></figure>')
    b += ('<figure class="about-founder"><blockquote>'
          + t(('Cresci como o mais velho de três filhos. Alguns anos depois de eu sair de casa, o casamento dos meus pais acabou. Foi a primeira vez que senti que tinha perdido o meu lar. Ainda sinto falta dessa sensação de estar em casa. É uma busca que continua.',
                 'I grew up the oldest of three. A few years after I left the house, my parents’ marriage collapsed. That was the first time I felt I had lost my home. I still long for that sense of being home. It is an ongoing quest.'))
          + t(('Desde 2005, procuro formas para que as comunidades compartilhem o que pertence a todos. A proposta da IMOBX leva essa ideia de compartilhar à moradia.',
                 'Since 2005, I have looked for ways for communities to share what they hold in common. The IMOBX proposal brings that idea of sharing to housing.'))
          + '</blockquote><figcaption>' + t(('John, cofundador, engenheiro de tokens e designer ecológico', 'John, co-founder, token engineer and ecological designer'), 'span') + '</figcaption>'
          + t(('John passou seis anos em ecovilas pela Europa. Hoje ele constrói o SIAH Protocol, um registro de contribuições que outras pessoas confirmam.', 'John spent six years in eco-villages across Europe. Today he is building SIAH Protocol, a record of contributions that other people confirm.'), 'p', 'class="about-founder-role"') + '</figure>')
    b += '</div><p>' + t(('As histórias completas de Rafael e John', 'Rafael’s and John’s full stories'), 'a', 'href="resources.html#our-story"') + '</p></section>'

    b += '<section id="build">' + t(('O que queremos construir?', 'What do we want to build?'), 'h2')
    b += t(('Queremos bairros de transição social rumo a um futuro resiliente, onde os vizinhos voltam a se conhecer e as crianças brincam onde os pais podem vê-las. Quem mora ali decide junto como o lugar funciona.',
            'We want neighbourhoods of social transition towards a resilient future, where neighbours know each other again and children play where their parents can see them. The people who live there decide together how the place is run.'))
    b += ('<figure class="about-picture"><img src="assets/village-street.jpg" width="1600" height="1067" loading="lazy" alt="Desenho de um caminho entre dois blocos brancos de apartamentos de dois andares, com varandas e painéis solares, que leva a um espaço verde com árvores frutíferas, um parquinho e hortas." data-alt-pt="Desenho de um caminho entre dois blocos brancos de apartamentos de dois andares, com varandas e painéis solares, que leva a um espaço verde com árvores frutíferas, um parquinho e hortas." data-alt-en="Drawing of a footpath between two white two-storey blocks of flats with balconies and solar panels, leading to a green space with fruit trees, a playground and vegetable beds." data-alt-nl="Tekening van een pad tussen twee witte appartementengebouwen van twee verdiepingen, met balkons en zonnepanelen, dat leidt naar een groene ruimte met fruitbomen, een speeltuin en moestuinen.">'
          '</figure>')
    b += '</section>'

    b += '<section id="how">' + t(('Como funcionaria?', 'How would it work?'), 'h2')
    # 15 Nov 2026 (owner, decision 97): the section says the point and sends the reader to the pages that hold the detail.
    b += linked(('Nosso plano é o', 'Our plan is'),
                ('aluguel com compra', 'rent-to-own', 'rent-to-own.html'),
                (': uma família se mudaria sem dar entrada, e parte de cada pagamento mensal iria para a compra do apartamento.',
                 ': a family would move in without a down payment, and part of every monthly payment would go towards buying the flat.'),
                ('A Olympus, a construtora do Rafael', 'Olympus, Rafael’s construction company', 'properties.html'),
                (', construiria a um preço ligado ao índice público de custo da construção do Rio, conferido de forma independente, e',
                 ', would build at a price tied to Rio’s public building-cost index, checked independently, and'),
                ('Custos e recursos', 'Costs and funding', 'costs-and-funding.html'),
                ('mostra as contas.', 'shows the sums.'))
    b += '</section>'

    b += '<section id="now" class="about-now">' + t(('Onde estamos agora?', 'Where are we now?'), 'h2')
    b += linked(('A IMOBX está em preparação, e a sua cooperativa ainda vai ser fundada. O caminho até os primeiros apartamentos tem',
                 'IMOBX is in preparation, and its cooperative is still to be founded. The path to the first flats has'),
                ('seis passos', 'six steps', 'project-development.html#stages'),
                (', e o terreno dos cinco apartamentos novos ainda está por escolher. Se você é uma família procurando moradia, tem um terreno ou uma casa, constrói, financia ou é um vizinho que quer que isso exista, queremos conhecer você.',
                 ', and the plot for the five new flats is still to be chosen. If you are a family looking for a home, someone with land or a house, a builder, a funder or a neighbour who wants this to exist, we would like to meet you.'))
    b += '<p>' + t(('Apresente-se', 'Introduce yourself'), 'a', 'class="button act" href="contact.html#apresentacao"') + '</p></section>'
    b += '</main>'
    (root / 'about.html').write_text(page('IMOBX | About', b, '<link rel="stylesheet" href="assets/about.css">' + term_scripts(root, ('token-engineer',)), lang='pt-BR', title_pt='IMOBX | Sobre',
                                          description='Por que a IMOBX existe, quem a começou e como funcionaria.'))
