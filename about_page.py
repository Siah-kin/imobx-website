"""The About page: why IMOBX exists, who started it, what it wants to build, how it would work, where it stands.

Owner, 8 Nov 2026: the site lacked the why; the draft (ABOUT_PAGE_DRAFT_2026-11-08.md, reviewed) approved with
"publish", and Rafael's OK to use his story here. Each why has one home; this page is the home of "why IMOBX".
"""


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
    b += linked(('Em 2022,', 'In 2022,'),
                ('o déficit habitacional do Brasil', 'Brazil’s housing deficit', 'why.html'),
                ('era de cerca de 6 milhões de moradias. Mais da metade (cerca de 3,24 milhões) eram famílias com renda de até três salários mínimos que gastam mais de 30% da renda com aluguel. Os aluguéis subiram 9,13% nos 12 meses até setembro de 2026, o dobro da inflação oficial de 4,58%. O Censo 2022 contou cerca de 16,4 milhões de pessoas morando em favelas e comunidades urbanas: um em cada doze brasileiros.',
                 'was about 6 million dwellings. More than half of it (about 3.24 million) were households earning up to three minimum wages that spend more than 30% of their income on rent. Rents rose 9.13% in the 12 months to September 2026, twice the official inflation of 4.58%. The 2022 Census counted about 16.4 million people living in favelas and urban communities: one in every twelve Brazilians.'))
    b += '</section>'

    b += '<section id="founders">' + t(('Quem começou a IMOBX, e por quê?', 'Who started IMOBX, and why?'), 'h2') + '<div class="about-founders">'
    b += ('<figure class="about-founder"><blockquote>'
          + t(('Minha infância me ensinou cedo o valor de cada centavo e de um teto seguro. Meu pai foi ausente, e minha mãe sustentava a casa trabalhando de 70 a 80 horas por semana para criar três filhos. Nunca desisti de um sonho que carrego desde a faculdade: construir boas moradias, de padrão modesto ou acessível, para que as famílias mais pobres possam de novo realizar o sonho da casa própria. Porque todo brasileiro sonha com isso.',
                 'My childhood taught me early the value of every cent and of a safe roof. My father was absent, and my mother supported the household working 70 to 80 hours a week to raise three children. I never gave up a dream I have carried since university: to build good homes, of modest or affordable standard, so that the poorest families can once again fulfil the dream of owning their own home. Because every Brazilian dreams of that.'))
          + t(('Ninguém gosta de pagar aluguel, de criar raízes num lugar e um dia ter que sair porque a casa não é sua. Quando a vida aperta, a primeira coisa que queremos é entrar na nossa caverna e nos proteger. A pergunta que não sai da minha cabeça é simples: por que ter a própria caverna não é um direito de todos? A IMOBX é a minha resposta a essa pergunta.',
                 'Nobody likes to rent, to put down roots in a place and one day have to leave because the home isn’t theirs. When life gets hard, the first thing we want is to go into our cave and protect ourselves. The question that won’t leave my mind is simple: why isn’t having one’s own cave a right for everyone? IMOBX is my answer to that question.'))
          + '</blockquote><figcaption>' + t(('Rafael Britto, cofundador e engenheiro civil, Rio de Janeiro', 'Rafael Britto, co-founder and civil engineer, Rio de Janeiro'), 'span') + '</figcaption></figure>')
    b += ('<figure class="about-founder"><blockquote>'
          + t(('Cresci como o mais velho de três filhos. Alguns anos depois de eu sair de casa, o casamento dos meus pais acabou. Foi a primeira vez que senti que tinha perdido o meu lar. Ainda sinto falta dessa sensação de estar em casa. É uma busca que continua.',
                 'I grew up the oldest of three. A few years after I left the house, my parents’ marriage collapsed. That was the first time I felt I had lost my home. I still long for that sense of being home. It is an ongoing quest.'))
          + t(('Desde 2005, procuro formas para que as comunidades compartilhem o que pertence a todos. A proposta da IMOBX leva essa ideia de compartilhar à moradia.',
                 'Since 2005, I have looked for ways for communities to share what they hold in common. The IMOBX proposal brings that idea of sharing to housing.'))
          + '</blockquote><figcaption>' + t(('John, cofundador', 'John, co-founder'), 'span') + '</figcaption></figure>')
    b += '</div><p>' + t(('As histórias completas de John e Rafael', 'John’s and Rafael’s full stories'), 'a', 'href="resources.html#our-story"') + '</p></section>'

    b += '<section id="build">' + t(('O que queremos construir?', 'What do we want to build?'), 'h2')
    b += t(('Queremos bairros de transição social rumo a um futuro resiliente, onde os vizinhos voltam a se conhecer e as crianças brincam onde os pais podem vê-las. Quem mora ali decide junto como o lugar funciona. O nosso lucro real é social. A nossa riqueza é um mundo onde as pessoas são livres, e um bairro sem estresse vale mais do que ficar milionário.',
            'We want neighbourhoods of social transition towards a resilient future, where neighbours know each other again and children play where their parents can see them. The people who live there decide together how the place is run. Our real profit is social. Our richness is a world where people are free, and a stress-free neighbourhood is worth more than becoming a millionaire.'))
    b += ('<figure class="about-picture"><img src="assets/homepage.jpg" width="1024" height="765" loading="lazy" alt="Ilustração conceitual da vila de Rafael" data-alt-pt="Ilustração conceitual da vila de Rafael" data-alt-en="Concept illustration of Rafael’s village" data-alt-nl="Conceptillustratie van het dorp van Rafael">'
          '<figcaption>' + t(('Ilustração conceitual da vila de Rafael, feita com um gerador de imagens.', 'Concept illustration of Rafael’s village, made with an image generator.'), 'span') + '</figcaption></figure>')
    b += '</section>'

    b += '<section id="how">' + t(('Como funcionaria?', 'How would it work?'), 'h2')
    b += linked(('Nosso plano é o', 'Our plan is'),
                ('aluguel com compra', 'rent-to-own', 'rent-to-own.html'),
                ('. Uma família se mudaria sem dar entrada, e parte de cada pagamento mensal iria para a compra da casa. A construtora do Rafael construiria a um custo conhecido, conferido de forma independente. O que sobrar iria para a próxima casa, para a próxima família. Planejamos começar com uma família, muito provavelmente no apartamento do Rafael em Guadalupe, e depois construir cinco apartamentos de cada vez.',
                 '. A family would move in without a down payment, and part of every monthly payment would go towards buying the house. Rafael’s construction company would build at a known cost, checked independently. What is left over would go into the next house, for the next family. We plan to start with one family, most likely in Rafael’s flat in Guadalupe, and then build five flats at a time.'))
    b += linked(('Outros grupos de moradia já administram suas casas juntos, e', 'Housing groups elsewhere already run their houses together, and'),
                ('aprendemos com eles', 'we learn from them', 'resources.html#studied'),
                ('. A FUCVAM, federação uruguaia de cooperativas de ajuda mútua fundada em 1970, faz as famílias construírem juntas, enquanto a cooperativa fica com a escritura. O Mietshäuser Syndikat, na Alemanha, une casas de aluguel administradas pelos próprios moradores. Nos Estados Unidos, os fundos comunitários de terra mantêm a terra em comum e dão a cada família os seus direitos num contrato longo e assinado. Pegamos o que funciona e adaptamos ao Rio, onde cada família seria dona da própria casa.',
                 '. FUCVAM, Uruguay’s federation of mutual-aid cooperatives founded in 1970, has families build together while the cooperative holds the title. The Mietshäuser Syndikat in Germany links rental houses that their residents run. In the United States, community land trusts keep the land shared and give each family its rights in a long, signed lease. We take what works and adapt it to Rio, where each family would own its own house.'))
    b += '</section>'

    b += '<section id="now" class="about-now">' + t(('Onde estamos agora?', 'Where are we now?'), 'h2')
    b += t(('A IMOBX está em preparação, e a sua cooperativa ainda vai ser fundada. Buscamos a primeira família, a primeira casa e as pessoas que vão fundar a cooperativa com a gente. Se você é uma família procurando moradia, tem um terreno ou uma casa, constrói, financia ou é um vizinho que quer que isso exista, queremos conhecer você.',
            'IMOBX is in preparation, and its cooperative is still to be founded. We are looking for the first family, the first house and the people who will found the cooperative with us. If you are a family looking for a home, someone with land or a house, a builder, a funder or a neighbour who wants this to exist, we would like to meet you.'))
    b += '<p>' + t(('Apresente-se', 'Introduce yourself'), 'a', 'class="button act" href="contact.html#apresentacao"') + '</p></section>'
    b += '</main>'
    (root / 'about.html').write_text(page('IMOBX | About', b, '<link rel="stylesheet" href="assets/about.css">', lang='pt-BR', title_pt='IMOBX | Sobre',
                                          description='Por que a IMOBX existe, quem a começou e como funcionaria.'))
