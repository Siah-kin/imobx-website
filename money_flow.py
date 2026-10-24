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
            + text(('Como o dinheiro circula numa casa', 'How the money moves through one home'), 'figcaption', 'class="money-flow-title"')
            + '<div class="money-flow-frame">' + SVG + '</div>'
            + '<ol class="money-flow-steps">' + steps + '</ol></figure>')


SCRIPT = ('<script>document.addEventListener("DOMContentLoaded",function(){var f=document.querySelector(".money-flow");if(!f||!("IntersectionObserver" in window))return;'
          'document.documentElement.classList.add("js-flow");new IntersectionObserver(function(e,o){e.forEach(function(x){'
          'if(x.isIntersecting){f.classList.add("is-flowing");o.disconnect();}});},{threshold:.35}).observe(f);});</script>')
