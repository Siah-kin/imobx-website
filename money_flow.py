"""'How the money moves through one home': the rent-to-own diagram (owner, 25 Oct 2026), drawn in the same
vessel-and-pipe language as the homepage's 'Three ways to house a family'. Shapes are SVG; every word is page text,
so it switches language with the rest of the site and the release checks can read it."""

STEPS = [
    (('Fundo para casas', 'Fund for homes'),
     ('O dinheiro para construir, incluindo o que volta das compras.', 'Money for building, including what comes back from purchases.')),
    (('Obra', 'Building'),
     ('Terreno e construção, com custos conferidos por alguém de fora.', 'Land and building, with costs checked by someone outside.')),
    (('A família entra', 'The family moves in'),
     ('O contrato vem antes da mudança. Sem entrada.', 'The agreement comes before moving in. No down payment.')),
    (('O pagamento de cada mês', 'Each month’s payment'),
     ('Parte compra a casa; outra parte paga manutenção e consertos.', 'Part buys the home; another part pays for upkeep and repairs.')),
    (('A casa é da família', 'The home is the family’s'),
     ('Cumpridas as condições combinadas, a casa é registrada em nome da família, e o dinheiro volta ao fundo para a próxima casa.',
      'Once the agreed conditions are met, the home is registered in the family’s name, and the money goes back to the fund for the next home.')),
]

SVG = '''<svg class="money-flow-art" viewBox="0 0 1000 285" aria-hidden="true">
<defs>
<marker id="mf-head" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 10 5 0 10z" fill="#193D4E"/></marker>
<marker id="mf-head-water" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0 10 5 0 10z" fill="#4A90A4"/></marker>
<clipPath id="mf-tank"><path d="M30 110H170V215H30Z"/></clipPath>
<clipPath id="mf-home"><path d="M440 95H560L548 215H452Z"/></clipPath>
<clipPath id="mf-reserve"><path d="M690 130H742L737 200H695Z"/></clipPath>
</defs>
<path class="mf-ground" d="M10 215H990"/>
<path class="mf-vessel" d="M30 110H170V215H30Z"/>
<g clip-path="url(#mf-tank)"><rect class="mf-water mf-tank-water" x="20" y="140" width="160" height="90"/></g>
<path class="mf-line" d="M30 110H170V215H30Z"/>
<path class="mf-stream mf-pipe-out" d="M170 195H245"/>
<path class="mf-line mf-dashed" d="M250 150 305 110l55 40M260 145v70h90v-70"/>
<path class="mf-line" d="M392 192H428" marker-end="url(#mf-head)"/>
<path class="mf-vessel" d="M440 95H560L548 215H452Z"/>
<g clip-path="url(#mf-home)"><rect class="mf-water mf-home-water" x="430" y="122" width="140" height="110"/></g>
<path class="mf-line" d="M440 95H560L548 215H452Z"/><path class="mf-line" d="M432 95h136"/>
<path class="mf-mark" d="M482 186 500 170l18 16M486 183v20h28v-20"/>
<path class="mf-stream mf-pay" d="M640 0v40"/>
<circle class="mf-valve" cx="640" cy="50" r="9"/>
<path class="mf-stream mf-pay-home" d="M631 50c-36 0-70 6-82 40"/>
<path class="mf-stream mf-pay-reserve" d="M649 50c32 0 62 12 67 75"/>
<path class="mf-vessel" d="M690 130H742L737 200H695Z"/>
<g clip-path="url(#mf-reserve)"><rect class="mf-water mf-reserve-water" x="684" y="168" width="64" height="40"/></g>
<path class="mf-line" d="M690 130H742L737 200H695Z"/><path class="mf-line" d="M684 130h64"/>
<path class="mf-thin" d="M704 152h24M716 140v24"/>
<path class="mf-line" d="M550 205C620 238 790 238 852 192" marker-end="url(#mf-head)"/>
<path class="mf-vessel" d="M860 105H925L940 120V205H860Z"/>
<path class="mf-line" d="M860 105H925L940 120V205H860ZM925 105V120H940M875 132H925M875 147H915"/>
<path class="mf-mark" d="M880 177l12 12 22-26"/>
<path class="mf-stream mf-return" d="M900 205V258H100V222" marker-end="url(#mf-head-water)"/>
<g class="mf-badges"><rect x="88" y="16" width="24" height="24"/><text x="100" y="33">1</text>
<rect x="288" y="16" width="24" height="24"/><text x="300" y="33">2</text>
<rect x="488" y="16" width="24" height="24"/><text x="500" y="33">3</text>
<rect x="748" y="16" width="24" height="24"/><text x="760" y="33">4</text>
<rect x="888" y="16" width="24" height="24"/><text x="900" y="33">5</text></g>
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
     ('As contas combinadas do imóvel, da manutenção e da administração.', 'The agreed property, upkeep and administration bills.')),
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
        parts.append(f'<g class="mf-badges"><rect x="{x-12}" y="{t-34}" width="24" height="24"/><text x="{x}" y="{t-17}">{i+1}</text></g>')
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
    (('Um prestador aceito converte', 'An accepted provider converts'),
     ('O prestador precisa aceitar a organização, mostrar todas as taxas e permitir a volta ao banco.', 'It must accept the organisation, show every fee and allow money back to the bank.')),
    (('Um registro digital comum', 'A shared digital record'),
     ('USDC na rede Arc está em estudo; mostra quem aprovou cada pagamento.', 'USDC on the Arc network is under consideration; it shows who approved each payment.')),
    (('O gasto é aprovado', 'Spending is approved'),
     ('A construtora nunca aprova a própria cobrança.', 'The builder never approves its own invoice.')),
    (('A construtora recebe em reais', 'The builder is paid in reais'),
     ('Depois que alguém confere a etapa da obra.', 'After someone checks the building stage.')),
]


def _route_svg():
    cx = [85, 250, 415, 585, 750, 915]
    y = 100
    icon = {
        0: lambda x: f'<path class="rt-icon" fill="none" stroke="#276578" stroke-width="2.2" d="M{x-16} {y}L{x} {y-14}L{x+16} {y}M{x-12} {y-3}v18h24v-18"/><text class="mf-glyph" fill="#276578" text-anchor="middle" font-size="11" font-weight="700" x="{x}" y="{y+12}">R$</text>',
        1: lambda x: f'<path class="rt-icon" fill="none" stroke="#276578" stroke-width="2.2" d="M{x-18} {y-8}L{x} {y-20}L{x+18} {y-8}ZM{x-12} {y-5}v16M{x} {y-5}v16M{x+12} {y-5}v16M{x-18} {y+14}h36"/>',
        2: lambda x: f'<path class="rt-icon" fill="none" stroke="#276578" stroke-width="2.2" d="M{x-16} {y-8}h28M{x+6} {y-14}l6 6-6 6M{x+16} {y+8}h-28M{x-6} {y+2}l-6 6 6 6"/>',
        3: lambda x: f'<path class="rt-icon" fill="none" stroke="#276578" stroke-width="2.2" d="M{x-20} {y-6}h10v10h-10zM{x-5} {y-6}h10v10h-10zM{x+10} {y-6}h10v10h-10zM{x-10} {y-1}h5M{x+5} {y-1}h5M{x-20} {y+13}h40"/>',
        4: lambda x: f'<path class="rt-icon" fill="none" stroke="#276578" stroke-width="2.2" d="M{x-12} {y-18}h24v34h-24zM{x-6} {y+1}l5 5 9-11"/>',
        5: lambda x: f'<path class="rt-icon mf-dashed" fill="none" stroke="#276578" stroke-width="2.2" d="M{x-16} {y}L{x} {y-14}L{x+16} {y}M{x-12} {y-3}v18h24v-18"/><text class="mf-glyph" fill="#276578" text-anchor="middle" font-size="11" font-weight="700" x="{x}" y="{y+12}">R$</text>',
    }
    parts = ['<svg class="money-flow-art money-route-art" viewBox="0 0 1000 175" aria-hidden="true">']
    for i in range(5):
        cls = 'mf-stream rt-pipe rt-p%d' % i + (' rt-digital' if i in (2, 3) else '')
        parts.append(f'<path class="{cls}" fill="none" stroke="#4A90A4" stroke-width="6" d="M{cx[i]+35} {y}H{cx[i+1]-35}"/>')
    for i, x in enumerate(cx):
        parts.append(f'<rect class="rt-box" x="{x-35}" y="{y-35}" width="70" height="70" fill="#fff" stroke="#9DC3CF" stroke-width="2"/>')
        parts.append(icon[i](x))
        parts.append(f'<g class="mf-badges"><rect x="{x-12}" y="22" width="24" height="24" fill="#276578"/><text x="{x}" y="39" fill="#fff" text-anchor="middle">{i+1}</text></g>')
        if i in (1, 4):  # the check points: the hint of orange
            parts.append(f'<path class="rt-check" d="M{x+35} {y-45}l10 10-10 10-10-10z" fill="#FF8C00" stroke="#193D4E" stroke-width="1.5"/>')
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
