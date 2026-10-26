# IMOBX website: Dutch translation guide (26 Oct 2026)

**What this is.** IMOBX is a proposed rent-to-own housing cooperative in Rio de Janeiro. The site is in preparation, and nothing is for sale. It speaks to families and to like-minded partners and investors.

**Source.** Translate from the English. The Portuguese is the original, so use it to settle any doubt about meaning.

**Readers.** Dutch speakers: partners, investors and interested people. Write plain Dutch at about B1 level. Keep sentences short.

## Voice
- **Address readers as "je" and "jouw"**, not "u". This is the owner's default and can be switched later. Use "we" and "ons" when IMOBX speaks.
- **Keep every caution exactly as strong as the source.** "would", "could", "is being prepared", "not yet", "under study", "a proposal" carry meaning: translate them with "zou", "kan", "wordt voorbereid", "nog niet", "wordt onderzocht", "voorstel". Never make a proposal sound like a fact or a promise.
- **Keep protections word for word in meaning.** For example: "No vote, including a token vote, can on its own change a family's housing agreement" becomes "Geen stemming, ook geen stemming van tokenhouders, kan op zichzelf de woonovereenkomst van een gezin veranderen."
- **No marketing words or exclamation marks.** No dashes (— or –) as connectors: use a comma, colon or full stop.
- **Sentence case for headings.** Questions stay questions.

## Fixed words (use these every time)
| English | Dutch |
|---|---|
| rent-to-own (the model) | huurkoop |
| rent-to-own home / with IMOBX | huurkoopwoning / huurkoop bij IMOBX |
| cooperative / neighbourhood cooperative | coöperatie / buurtcoöperatie |
| household / family | huishouden / gezin (follow the source) |
| down payment | aanbetaling |
| agreement / contract (family's) | overeenkomst / contract (follow the source; "housing agreement" = woonovereenkomst) |
| funder / investor / donor | financier / investeerder / donateur |
| budget line | begrotingspost |
| reserve | reserve |
| repairs | reparaties |
| the founders | de oprichters |
| founding circle | oprichterskring |
| pilot | pilot |
| token, blockchain, USDC, Arc, DAO, multisig | keep as is (token, blockchain, USDC, Arc, DAO). "several signers" = meerdere ondertekenaars |
| trading fee | handelsvergoeding |
| help desk | helpdesk |
| Take part (menu) | Meedoen |
| How it works (menu) | Zo werkt het |
| Project stages (menu) | Projectfasen |
| Funding and spending (menu) | Financiering en uitgaven |
| Shared records (menu) | Gedeelde registers |
| Drawings and photos (menu) | Tekeningen en foto's |
| Documents (menu) | Documenten |
| The project (menu) | Het project |
| On this page | Op deze pagina |
| Introduce yourself / Introduce myself on Telegram | Stel je voor / Mezelf voorstellen via Telegram |
| Source: | Bron: |
| More information / Less information | Meer informatie / Minder informatie |
| In preparation | In voorbereiding |
| favela | favela |

## Do not translate
- **Names:** people, organisations, places, laws and programmes. Examples: Rafael Britto, Caixa, CVM, Banco Central, Lei 13.709, Minha Casa Minha Vida, Fundação João Pinheiro, IBGE, Agência Brasil, Aneel, FipeZap, Ostrom, ICA, The Flock, Arctide, Argus, Tolly, Ethervista, Circle, OECD.
- **The titles of linked sources:** keep the title as written. Translate only the surrounding words, such as "Source:", months and "via".
- **Portuguese text inside an English string:** a quoted source title or a legal name stays as it is.

## Numbers and dates
- **Dutch number format:** US$ 13.888,50 · US$ 27.777 · 9,13% · 11,4 miljoen · 45 m².
- **Months in lowercase:** 24 oktober 2026 · 20 januari 2026.
- **Currency:** "R$" and "reais" stay. "US dollars" becomes "Amerikaanse dollars".

## Format
- **Keep each string a single string.** Do not split or merge strings.
- **Keep any leading or trailing space or punctuation pieces exactly**: some strings are fragments joined to others, such as "Source: " or ". ".
- **Short labels** (buttons, menu, headings) stay short.

## Output
- One JSON object: {"<the English string exactly as given>": "<Dutch>"}.
- Every input string must appear once.
