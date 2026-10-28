"""'How the money moves through one home': the rent-to-own diagram (owner, 25 Oct 2026), drawn in the same
vessel-and-pipe language as the homepage's 'Three ways to house a family'. Shapes are SVG; every word is page text,
so it switches language with the rest of the site and the release checks can read it."""

STEPS = [
    (('Fundo para casas', 'Fund for homes'),
     ('Dinheiro para construir. O que sobra de cada pagamento, depois dos custos e das reservas, vai para a próxima casa.', 'Money for building. What is left of each payment, after costs and reserves, goes into the next home.')),
    (('Obra', 'Building'),
     ('Nossa construtora faz a obra, e o custo do terreno e da construção fica registrado.', 'Our construction company builds it, and the cost of land and building is written down.')),
    (('A família entra', 'The family moves in'),
     ('O contrato é assinado antes da mudança.', 'The agreement is signed before moving in.')),
    (('O pagamento de cada mês', 'Each month’s payment'),
     ('Parte compra a casa; outra parte paga manutenção e consertos.', 'Part buys the home; another part pays for upkeep and repairs.')),
    (('A casa é da família', 'The home is the family’s'),
     ('Quando terminar de pagar o combinado, a escritura fica no seu nome.',
      'When you have paid what was agreed, the deed is in your name.')),
]

SVG = '''<svg class="money-flow-art" viewBox="0 0 1000 240" aria-hidden="true">
<defs>
<marker id="mf-head-water" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0 10 5 0 10z" fill="#4A90A4"/></marker>
<clipPath id="mf-tank"><path d="M40 70H160L150 175H50Z"/></clipPath>
<clipPath id="mf-home"><path d="M440 70H560L550 175H450Z"/></clipPath>
<clipPath id="mf-reserve"><path d="M690 100H750L745 165H695Z"/></clipPath>
<clipPath id="mf-owned"><path d="M840 70H960L950 175H850Z"/></clipPath>
</defs>
<path class="mf-ground" d="M10 178H990" fill="none" stroke="#D9E3E8" stroke-width="2"/>
<!-- the fund: a bucket -->
<path d="M40 70H160L150 175H50Z" fill="#fff"/>
<g clip-path="url(#mf-tank)"><rect class="mf-water mf-tank-water" x="30" y="100" width="140" height="90" fill="#4A90A4" fill-opacity=".55"/></g>
<path fill="none" stroke="#193D4E" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" d="M40 70H160L150 175H50Z"/><path fill="none" stroke="#193D4E" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" d="M32 70h136"/>
<!-- money for building runs to the building site -->
<path class="mf-stream mf-pipe-out" fill="none" stroke="#4A90A4" stroke-width="6" stroke-linecap="round" d="M154 140H246"/>
<!-- building: a bucket still being made -->
<path d="M240 70H360L350 175H250Z" fill="#fff"/>
<path fill="none" stroke="#193D4E" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="7 6" d="M240 70H360L350 175H250Z"/>
<path fill="none" stroke="#276578" stroke-width="2.2" stroke-dasharray="4 4" d="M282 150 300 134l18 16M286 147v18h28v-18"/>
<path class="mf-stream" fill="none" stroke="#4A90A4" stroke-width="6" stroke-linecap="round" d="M354 140H446"/>
<!-- the family's home: a bucket that fills with each month's payment -->
<path d="M440 70H560L550 175H450Z" fill="#fff"/>
<g clip-path="url(#mf-home)"><rect class="mf-water mf-home-water" x="430" y="112" width="140" height="80" fill="#4A90A4" fill-opacity=".55"/></g>
<path fill="none" stroke="#193D4E" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" d="M440 70H560L550 175H450Z"/><path fill="none" stroke="#193D4E" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" d="M432 70h136"/>
<path fill="none" stroke="#276578" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" d="M482 156 500 140l18 16M486 153v18h28v-18"/>
<!-- each month's payment splits: part buys the home, part goes to upkeep and repairs -->
<path class="mf-stream mf-pay" fill="none" stroke="#4A90A4" stroke-width="6" stroke-linecap="round" d="M640 0v26"/>
<circle class="mf-valve" cx="640" cy="36" r="9" fill="#fff" stroke="#193D4E" stroke-width="2.5"/>
<path class="mf-stream mf-pay-home" fill="none" stroke="#4A90A4" stroke-width="6" stroke-linecap="round" d="M631 36c-40 0-70 6-80 34"/>
<path class="mf-stream mf-pay-reserve" fill="none" stroke="#4A90A4" stroke-width="6" stroke-linecap="round" d="M649 36c34 0 70 14 72 62"/>
<path d="M690 100H750L745 165H695Z" fill="#fff"/>
<g clip-path="url(#mf-reserve)"><rect class="mf-water mf-reserve-water" x="684" y="135" width="72" height="40" fill="#4A90A4" fill-opacity=".55"/></g>
<path fill="none" stroke="#193D4E" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" d="M690 100H750L745 165H695Z"/><path fill="none" stroke="#193D4E" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" d="M684 100h72"/>
<path fill="none" stroke="#526571" stroke-width="2" stroke-linecap="round" d="M708 122h24M720 110v24"/>
<!-- the home is the family's: the same bucket, full -->
<path d="M840 70H960L950 175H850Z" fill="#fff"/>
<g clip-path="url(#mf-owned)"><rect x="830" y="76" width="140" height="110" fill="#4A90A4" fill-opacity=".55"/></g>
<path fill="none" stroke="#193D4E" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" d="M840 70H960L950 175H850Z"/><path fill="none" stroke="#193D4E" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" d="M832 70h136"/>
<path fill="none" stroke="#276578" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" d="M882 156 900 140l18 16M886 153v18h28v-18"/>
<!-- what the family pays towards the purchase goes back to the fund for the next home -->
<path class="mf-stream mf-return" fill="none" stroke="#4A90A4" stroke-width="5" stroke-linecap="round" stroke-dasharray="14 10" d="M500 178V222H100V184" marker-end="url(#mf-head-water)"/>
</svg>'''


def money_flow_html(text):
    """The figure: drawing, then the five numbered steps as text (PT first, EN in data-en)."""
    steps = ''.join('<li>' + text(title, 'strong') + text(body, 'span') + '</li>' for title, body in STEPS)
    return ('<figure class="money-flow" id="como-o-dinheiro-circula">'
            + '<div class="money-flow-frame">' + SVG + '</div>'
            + '<ol class="money-flow-steps">' + steps + '</ol></figure>')


SCRIPT = ('<script>document.addEventListener("DOMContentLoaded",function(){var f=document.querySelector(".money-flow");if(!f||!("IntersectionObserver" in window))return;'
          'document.documentElement.classList.add("js-flow");new IntersectionObserver(function(e,o){e.forEach(function(x){'
          'if(x.isIntersecting){f.classList.add("is-flowing");o.disconnect();}});},{threshold:.35}).observe(f);});</script>')


# ---------- Funding page (25 Oct 2026): the order money is used, drawn as a cascade ----------
CASCADE_STEPS = [
    (('Impostos e dinheiro com destino', 'Taxes and money with a set purpose'),
     ('Pagos ou separados antes de qualquer outra coisa.', 'Paid or set aside before anything else.')),
    (('Contas', 'Bills'),
     ('Contas do imóvel, manutenção e administração, como combinado.', 'Property bills, upkeep and running costs, as agreed.')),
    (('Reservas', 'Reserves'),
     ('Reparos, casas vazias, promessas feitas às famílias e imprevistos.', 'Repairs, empty homes, promises made to families and the unexpected.')),
    (('Novas casas', 'New homes'),
     ('Só dentro do orçamento combinado.', 'Only within the agreed budget.')),
    (('Investidores, por último', 'Investors, last'),
     ('Só se sobrar dinheiro e um acordo escrito válido permitir.', 'Only if money remains and a valid written agreement allows it.')),
]


def _cascade_svg():
    cx = [100, 300, 500, 700, 900]
    top = [60, 95, 130, 165, 200]
    level = [14, 14, 14, 38, None]
    parts = ['<svg class="money-flow-art" viewBox="0 0 1000 300" aria-hidden="true"><defs>']
    for i, (x, t) in enumerate(zip(cx, top)):
        parts.append(f'<clipPath id="cc{i}"><path d="M{x-65} {t}H{x+65}L{x+53} {t+70}H{x-53}Z"/></clipPath>')
    parts.append('</defs><path class="mf-ground" d="M10 285H990"/>')
    parts.append(f'<path class="mf-stream cc-in" d="M66 0V{top[0]+22}"/>')
    for i, (x, t) in enumerate(zip(cx, top)):
        body = f'M{x-65} {t}H{x+65}L{x+53} {t+70}H{x-53}Z'
        parts.append(f'<path class="mf-vessel" d="{body}"/>')
        if level[i] is not None:
            parts.append(f'<g clip-path="url(#cc{i})"><rect class="mf-water cc-water cc-w{i}" x="{x-75}" y="{t+level[i]}" width="150" height="90"/></g>')
        cls = 'mf-line mf-dashed' if i == 4 else 'mf-line'
        parts.append(f'<path class="{cls}" d="{body}"/><path class="{cls}" d="M{x-73} {t}h146"/>')
        if i < 4:
            spill = 'mf-stream cc-spill cc-s%d' % i + (' mf-trickle' if i == 3 else '')
            parts.append(f'<path class="{spill}" d="M{x+65} {t+2}C{x+110} {t+2} {x+135} {t+15} {x+170} {t+47}"/>')
    parts.append('</svg>')
    return ''.join(parts)


def cascade_html(text):
    steps = ''.join('<li>' + text(title, 'strong') + text(body, 'span') + '</li>' for title, body in CASCADE_STEPS)
    return ('<figure class="money-flow money-cascade">'
            + '<div class="money-flow-frame">' + _cascade_svg() + '</div>'
            + '<ol class="money-flow-steps">' + steps + '</ol></figure>')


# ---------- Funding page: how a payment travels, drawn as one pipe with check points ----------
ROUTE_STEPS = [
    (('A família paga em reais', 'The family pays in reais'),
     ('Por Pix ou transferência. Nenhuma família precisa de criptomoedas.', 'By Pix or bank transfer. No family needs crypto.')),
    (('A conta da IMOBX', 'IMOBX’s bank account'),
     ('Impostos, manutenção e reservas saem primeiro.', 'Taxes, upkeep and reserves come off first.')),
    # 'An accepted provider converts' and 'A shared digital record' moved to the Distributed ledger page (sweep 28 Oct, review B).
    (('Outra pessoa aprova o gasto', 'Someone else approves the spending'),
     ('A construtora nunca aprova a própria cobrança.', 'The builder never approves its own invoice.')),
    (('A construtora recebe em reais', 'The builder is paid in reais'),
     ('Depois que alguém de fora dos fundadores confere aquela etapa da obra.', 'After someone outside the founders checks that stage of the work.')),
]


def _route_svg():
    """The payment as water in one pipe, drawn only with buckets, pipe parts and a valve (25 Oct, second review):
    the family's bucket, IMOBX's bucket, the approval valve and the builder's bucket. The conversion coupling and
    the window for a shared digital record moved with their steps to the Distributed ledger page (sweep, 28 Oct),
    so four stations now sit at the centres of four equal columns."""
    N = 'fill="none" stroke="#193D4E" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"'
    T = 'fill="none" stroke="#276578" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"'
    W = 'fill="#4A90A4" fill-opacity=".55"'
    P = 'fill="none" stroke="#4A90A4" stroke-width="6" stroke-linecap="round"'
    y = 112
    def bucket(cx, level, mark=''):
        b = f'M{cx-40} 64H{cx+40}L{cx+33} 150H{cx-33}Z'
        return (f'<path d="{b}" fill="#fff"/><clipPath id="rb{cx}"><path d="{b}"/></clipPath>'
                f'<g clip-path="url(#rb{cx})"><rect x="{cx-45}" y="{level}" width="90" height="100" {W}/></g>'
                f'<path {N} d="{b}"/><path {N} d="M{cx-46} 64h92"/>{mark}')
    def house(cx, attrs):
        return f'<path {attrs} d="M{cx-13} 134 {cx} 122l13 12M{cx-9} 131v13h18v-13"/>'
    family, imobx, valve, builder = 125, 375, 625, 875
    parts = ['<svg class="money-flow-art money-route-art" viewBox="0 40 1000 120" aria-hidden="true">',
             '<path d="M10 153H990" fill="none" stroke="#D9E3E8" stroke-width="2"/>']
    parts.append(f'<path class="rt-pipe rt-p0" {P} d="M{family+35} {y}H{imobx-37}"/>')
    parts.append(f'<path class="rt-pipe rt-p1" {P} d="M{imobx+37} {y}H{(imobx + valve) // 2 + 20}"/>')
    parts.append(f'<path class="rt-pipe rt-p2" {P} d="M{(imobx + valve) // 2 + 20} {y}H{valve-22}"/>')
    parts.append(f'<path class="rt-pipe rt-p3" {P} d="M{valve+22} {y}H{(valve + builder) // 2 - 20}"/>')
    parts.append(f'<path class="rt-pipe rt-p4" {P} d="M{(valve + builder) // 2 - 20} {y}H{builder-37}"/>')
    # 1 the family pays in reais
    parts.append(bucket(family, 96, house(family, T)))
    # 2 IMOBX's account: the same bucket, taxes, upkeep and reserves settle first
    parts.append(bucket(imobx, 104))
    # 3 the approval valve the builder cannot open alone
    v = f'M{valve-22} {y-16}L{valve} {y}L{valve-22} {y+16}ZM{valve+22} {y-16}L{valve} {y}L{valve+22} {y+16}Z'
    parts.append(f'<path d="{v}" fill="#fff"/><path {N} d="{v}"/><path {N} d="M{valve} {y}V{y-34}M{valve-12} {y-34}h24"/>')
    # 4 the builder is paid in reais: a bucket filling, with the building under way
    parts.append(bucket(builder, 118, house(builder, 'fill="none" stroke="#276578" stroke-width="2.2" stroke-dasharray="4 4"')))
    parts.append('</svg>')
    return ''.join(parts)


def route_html(text):
    steps = ''.join('<li>' + text(title, 'strong') + text(body, 'span') + '</li>' for title, body in ROUTE_STEPS)
    return ('<figure class="money-flow money-route">'
            + '<div class="money-flow-frame">' + _route_svg() + '</div>'
            + '<ol class="money-flow-steps money-route-steps">' + steps + '</ol></figure>')


FUNDING_SCRIPT = ('<script>document.addEventListener("DOMContentLoaded",function(){var fs=document.querySelectorAll(".money-flow");'
                  'if(!fs.length||!("IntersectionObserver" in window))return;document.documentElement.classList.add("js-flow");'
                  'var o=new IntersectionObserver(function(e){e.forEach(function(x){if(x.isIntersecting){x.target.classList.add("is-flowing");'
                  'o.unobserve(x.target);}});},{threshold:.35});fs.forEach(function(f){o.observe(f);});});</script>')


# ---------- Distributed ledger page (owner, 28 Oct 2026): from a repair request to a record anyone can check ----------
# Same vessel-and-pipe language. Above the ground line is public, below it private (the Iceberg's waterline).
LEDGER_TITLES = [
    ('Seu pedido', 'Your request'),
    ('Aprovado dentro do limite', 'Approved within the limit'),
    ('Conferido por outra pessoa', 'Checked by someone else'),
    ('Pago, e no registro público', 'Paid, and on the public ledger'),
    ('Segundo olhar? Revisão', 'Second look? A review'),
]
LEDGER_PRIVATE = ('Abaixo da linha fica o que é privado: seu contrato, seus pagamentos e o que diz a sua reclamação.',
                  'Below the line stays what is private: your contract, your payments and what your complaint says.')


def _ledger_svg():
    def bucket(x, mark, cls=''):
        return (f'<path d="M{x-50} 70H{x+50}L{x+42} 170H{x-42}Z" fill="#fff"/>'
                f'<path class="mf-line{cls}" d="M{x-50} 70H{x+50}L{x+42} 170H{x-42}Z"/><path class="mf-line" d="M{x-57} 70h114"/>' + mark)
    request = bucket(100, '<path class="mf-mark" d="M86 120h28v18H98l-8 8v-8h-4z"/>')                 # a speech bubble: the request
    approved = bucket(300, '<path class="mf-mark" d="M286 130l10 10 18-20"/>')                          # a tick: approved
    checked = bucket(500, '<path class="mf-mark" d="M478 130s9-12 22-12 22 12 22 12-9 12-22 12-22-12-22-12z"/><circle class="mf-mark" cx="500" cy="130" r="5"/>')
    # paid, and on the public ledger: three linked blocks that appear one by one
    blocks = ''.join(f'<rect class="lf-block lf-block-{i}" x="{646 + i * 38}" y="104" width="32" height="32" fill="#4A90A4" fill-opacity=".55" stroke="#193D4E" stroke-width="2.5"/>'
                     + (f'<path class="lf-block lf-block-{i}" d="M{678 + i * 38} 120h6" stroke="#193D4E" stroke-width="2.5"/>' if i < 2 else '')
                     for i in range(3))
    review = bucket(900, '<path class="mf-mark" d="M912 118a14 14 0 1 0 4 12"/><path class="mf-mark" d="M906 112l8 6-7 6"/>')  # a circular arrow
    return ('<svg class="money-flow-art ledger-flow-art" viewBox="0 0 1000 260" aria-hidden="true">'
            '<defs><marker id="lf-head" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
            '<path d="M0 0 10 5 0 10z" fill="#4A90A4"/></marker></defs>'
            '<path class="mf-ground lf-waterline" d="M10 178H990"/>'
            + request
            + '<path class="mf-stream lf-pipe lf-pipe-1" d="M146 120H218"/><circle class="mf-valve" cx="228" cy="120" r="9"/><path class="mf-stream lf-pipe lf-pipe-1b" d="M237 120H254"/>'
            + approved
            + '<path class="mf-stream lf-pipe lf-pipe-2" d="M346 120H454"/>'
            + checked
            + '<path class="mf-stream lf-pipe lf-pipe-3" d="M546 120H640"/>'
            + blocks
            + '<path class="mf-thin" d="M646 150h108M646 156h108" stroke-dasharray="4 4"/>'
            + '<path class="mf-stream mf-return lf-return" d="M760 120H850" stroke-dasharray="6 6"/>'
            + review
            # not happy: the review runs back to the start, below the line
            + '<path class="mf-stream mf-return lf-return" d="M900 172V214H100V178" marker-end="url(#lf-head)"/>'
            # below the line, private: a lock
            + '<rect class="mf-mark" x="488" y="230" width="24" height="18"/><path class="mf-mark" d="M492 230v-6a8 8 0 0 1 16 0v6"/>'
            + '</svg>')


def ledger_flow_html(text, bodies):
    """The ledger figure: the drawing, the five steps (titles here, bodies from the page's request steps), the private line."""
    steps = ''.join('<li>' + text(title, 'strong') + text(body, 'span') + '</li>' for title, body in zip(LEDGER_TITLES, bodies))
    return ('<figure class="money-flow ledger-flow">'
            + '<div class="money-flow-frame">' + _ledger_svg() + '</div>'
            + '<ol class="money-flow-steps">' + steps + '</ol>'
            + text(LEDGER_PRIVATE, 'p', 'class="ledger-private"') + '</figure>')
