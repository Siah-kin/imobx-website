# Dutch translation: editor's review (26 Oct 2026)

**What this is.** One editor's pass over the merged Dutch (`nl.draft.json`, four translators) to give one consistent voice. The output is `nl.json`: same 987 keys, same order, byte-identical keys. 115 entries were changed and 872 kept as they were.

**Not a native-speaker review.** This pass was made by an AI editor working from the Portuguese original and the English source. It does not replace a review by a native Dutch speaker, which is still needed before publication.

## Settled decisions applied

| # | Decision | Entries changed | State in nl.json |
|---|---|---|---|
| 1 | "de token", never "het token" (and pronouns "die/hij") | 6 (incl. 3 pronoun fixes: "zou die", "om de token te lanceren", "Wat hij zou doen") | 13 entries with "de (…)token", 0 with "het token" |
| 2 | outreach = voorlichting; promotion/promote = promotie/promoten | 3 ("Token en voorlichting", "Hoe voorlichtingswerk wordt betaald", the funding route text) | 8 entries with voorlichting, 5 with promotie; none crossed |
| 3 | "(in het Engels)" exactly where the Portuguese says "(em inglês)" | 2 added (Whitepaper sections 9 and 3; section 4 and the two documentation links already had it) | 5 entries, a 1:1 match with the Portuguese |
| 4 | blockchain refers back with "hij" | 4 ("Hij legt betalingen vast.", "Hij controleert geen werk …", "Hij kan niet beoordelen …", menu item "Wat een blockchain niet kan") | no "ze" left for the blockchain |
| 5 | straight apostrophe plurals (foto's, favela's) | 0 (already correct) | 31 entries, no curly ones |
| 6 | law names stay in Portuguese, the words around them in Dutch | 0 (already correct: "Lei 13.709 (LGPD), artikel 18", "Código Civil · artikel 1.245", "CVM: Resolução 249 van 13 oktober 2026") | 9 entries |
| 7 | records = registers; menu "Gedeelde registers" | 5 (payment records → betalingsregisters (2); "Met registers van kosten en betalingen" now matches its twin on the roadmap page; photo "records" → opnamen, see below) | 17 entries with register(s) |
| 8 | readers are "je"; no u/uw | 0 (already correct) | 0 hits for u/uw |

## Meaning and caution fixes (EN → old NL → new NL)
- **A family stays, pays towards owning it and ends up with the whole home in its name.**
  - old: Een gezin blijft wonen, betaalt af op het eigendom en krijgt uiteindelijk de hele woning op zijn naam.
  - new: Een gezin blijft wonen, betaalt om eigenaar te worden en krijgt uiteindelijk de hele woning op zijn naam.
- **On 30 November 2025, Rafael imagined 45 m² duplex homes facing a shared area, with solar power, an orchard, play space and two small study rooms. The design aims to bring together a path to ownership, lower household expenses and places to meet and learn.**
  - old: Op 30 november 2025 bedacht Rafael duplexwoningen van 45 m² rond een gedeelde ruimte, met zonne-energie, een boomgaard, speelruimte en twee kleine studieruimtes. Het ontwerp wil een weg naar eigendom, lagere uitgaven voor het huishouden en plekken om elkaar te ontmoeten en te leren samenbrengen.
  - new: Op 30 november 2025 bedacht Rafael duplexwoningen van 45 m² rond een gedeelde ruimte, met zonne-energie, een boomgaard, speelruimte en twee kleine studieruimtes. Het ontwerp wil een weg naar eigendom samenbrengen met lagere uitgaven voor het huishouden en plekken om elkaar te ontmoeten en te leren.
- **The agreement is signed before moving in.**
  - old: De overeenkomst wordt ondertekend voordat je er gaat wonen.
  - new: De overeenkomst wordt ondertekend voordat het gezin er gaat wonen.
- **A new local team would need to show it can keep the homes and services running. Having a blockchain, tokens or a thousand homes does not by itself show that the income covers the bills.**
  - old: Een nieuw lokaal team zou moeten laten zien dat het de woningen en diensten draaiende kan houden. Een blockchain, tokens of duizend woningen hebben toont op zichzelf niet aan dat de inkomsten de rekeningen dekken.
  - new: Een nieuw lokaal team zou moeten laten zien dat het de woningen en diensten draaiende kan houden. Dat er een blockchain, tokens of duizend woningen zijn, toont op zichzelf niet aan dat de inkomsten de rekeningen dekken.
- **Expansion would pause if money for promises already made is missing or the first project’s results do not support building more homes.**
  - old: Uitbreiding zou worden gepauzeerd als er geen geld is voor toezeggingen die al zijn gedaan, of als de resultaten van het eerste project niet genoeg steun geven om meer woningen te bouwen.
  - new: Uitbreiding zou worden gepauzeerd als er geen geld is voor toezeggingen die al zijn gedaan, of als de resultaten van het eerste project niet onderbouwen dat er meer woningen gebouwd kunnen worden.
- **The team replies on Telegram. The subject and location help direct the conversation. The team may ask questions, or agree with you on an assessment, a meeting or a review of your proposal. Housing, appointments and funding depend on their own agreements.**
  - old: Het team antwoordt via Telegram. Het onderwerp en de locatie helpen om het gesprek goed te richten. Het team kan vragen stellen, of met je afspreken over een beoordeling, een overleg of een bespreking van je voorstel. Wonen, aanstellingen en financiering hangen elk af van eigen overeenkomsten.
  - new: Het team antwoordt via Telegram. Het onderwerp en de locatie helpen om het gesprek goed te richten. Het team kan vragen stellen, of met je een beoordeling, een overleg of een bespreking van je voorstel afspreken. Wonen, aanstellingen en financiering hangen elk af van eigen overeenkomsten.
- **An owner can introduce a property, describe its condition and say whether they are considering donating, selling or leasing it.**
  - old: Een eigenaar kan een pand voorstellen, de staat ervan beschrijven en laten weten of schenken, verkopen of verhuren wordt overwogen.
  - new: Een eigenaar kan een pand voorstellen, de staat ervan beschrijven en laten weten of hij overweegt het te schenken, te verkopen of te verhuren.
- **Each path needs its own legal review. The first project can go ahead with ordinary agreements.**
  - old: Elke route heeft een eigen juridische toetsing nodig. Het eerste project kan verder met gewone overeenkomsten.
  - new: Elke route heeft een eigen juridische toetsing nodig. Het eerste project kan van start gaan met gewone overeenkomsten.
- **The experimental programme under article 1, paragraph 3 excludes real investors, actually issued securities and real-money movements in its tests. It does not authorise public offerings or other regulated activities.**
  - old: Het experimentele programma onder artikel 1, lid 3 sluit in zijn tests echte investeerders, daadwerkelijk uitgegeven effecten en bewegingen van echt geld uit. Het geeft geen toestemming voor openbare aanbiedingen of andere gereguleerde activiteiten.
  - new: Het experimentele programma onder artikel 1, lid 3 sluit in zijn tests echte investeerders, daadwerkelijk uitgegeven effecten en transacties met echt geld uit. Het geeft geen toestemming voor openbare aanbiedingen of andere gereguleerde activiteiten.
- **Homes and courtyard: entrances and windows facing shared space aim to support neighbourly contact and awareness of the surroundings.**
  - old: Woningen en binnenplaats: ingangen en ramen gericht op de gedeelde ruimte zijn bedoeld om contact tussen buren en aandacht voor de omgeving te steunen.
  - new: Woningen en binnenplaats: ingangen en ramen gericht op de gedeelde ruimte zijn bedoeld om contact tussen buren en aandacht voor de omgeving te bevorderen.
- **Missing resident participation or an accessible review process requires the rules to be revised before use.**
  - old: Zonder deelname van bewoners of een toegankelijke manier om een besluit te laten herzien, moeten de regels worden herzien voordat ze worden gebruikt.
  - new: Zonder deelname van bewoners of een toegankelijke herbeoordeling moeten de regels worden aangepast voordat ze worden gebruikt.
- **Agreed, checked tasks; whoever is paid tells the public**
  - old: Afgesproken, gecontroleerde taken; wie betaald wordt, maakt dat openbaar
  - new: Afgesproken, gecontroleerde taken; wie betaald wordt, meldt dat aan het publiek

None of the protections was weakened in the draft: "Geen stemming, ook geen stemming van tokenhouders, kan op zichzelf …", "investeerders krijgen alleen de rechten die in hun overeenkomst staan", "geen aanbod/lijst van beschikbare woningen" and "De website verstuurt zelf niets" are all still at full strength and were checked in every place they appear.

## Consistency changes (grouped)

- **Links to the roadmap page** now use its Dutch menu name: "Projectfasen, drie gevallen", "Projectfasen, wie beslist wat", "Meer bij Projectfasen", "Projectfasen en gedeelde besluiten". "Routekaart" is kept only for the chapter of Rafael's document (reference page).
- **introduction (the message)** = kennismakingsbericht: "Je kennismakingsbericht", "Eerst mijn bericht voorbereiden", "Dit kennismakingsbericht bevestigt geen …"; "Write a brief introduction" = "Stel je kort voor."
- **decision** = besluit everywhere (7 entries had "beslissing"); **question a decision** = een besluit aanvechten; **question a charge** = een rekening betwisten; **review (of a decision)** = herbeoordeling.
- **spending limit** = uitgavenlimiet (was mixed: bestedingslimiet, uitgavengrens); **deadline** = termijn; **budget lead** = budgetverantwoordelijke; **appointment** = aanstelling.
- **builder** = bouwer, **construction company** = bouwbedrijf (the draft mixed the two).
- **exchange (trading venue)** = handelsplatform (Argus and the decentralised exchange now match Arctide).
- **accounts (books)** = boekhouding; bank accounts stay rekeningen. **personal data** = persoonsgegevens. **resident participation** = deelname van bewoners (resident say stays inspraak). **social purpose** = maatschappelijk doel. **operation(s)** = bedrijfsvoering. **token buyer** = tokenkoper.
- **How (the) money moves** = "Hoe (loopt) het geld …" in all three places; "Hoe besluiten verdeeld zouden worden" now matches its heading.
- **Image labels**: "Vergroten: …" always lowercase after the colon; benedenverdieping/bovenverdieping in both label and plan title; "Speeltuinen" as in the illustration text; favela photo captions say "hellingen", as the headings do.
- **Contact form**: "Bericht controleren" / "Controleer je bericht" / "Ik heb de gegevens gecontroleerd"; "verstuurd" throughout.
- **Shared column labels** on the token page and the records table ("What it holds", "What it decides") were made gender-neutral ("Wat erbij hoort", "Wat er wordt beslist"), because one label serves the cooperative, the token and the registers.
- **Aria labels** "X: Y" use a lowercase second part and the same words as the visible button.

## Other changed entries (C = consistency, S = style; the decision rows are in the table above)

- C · "Roadmap, three cases" → Projectfasen, drie gevallen
- C · "Roadmap, who decides what" → Projectfasen, wie beslist wat
- C · "More in the roadmap" → Meer bij Projectfasen
- C · "Roadmap and shared decisions" → Projectfasen en gedeelde besluiten
- C · "Your introduction" → Je kennismakingsbericht
- C · "Prepare my introduction first" → Eerst mijn bericht voorbereiden
- C · "Prepare your introduction here, copy it and send it to th…" → Bereid hier je kennismakingsbericht voor, kopieer het en stuur het via Telegram naar het team. De website v…
- C · "Want to talk about a home? Prepare your introduction and…" → Wil je praten over een woning? Bereid je kennismakingsbericht voor en stuur het via Telegram naar het team;…
- C · "Write a brief introduction. Leave out identity documents,…" → Stel je kort voor. Laat identiteitsbewijzen, bankgegevens en wachtwoorden weg.
- C · "An association can introduce housing needs, a property or…" → Een vereniging kan woonbehoeften, een pand of een netwerk van deelnemers inbrengen. Een gesprek kan leiden…
- C · "Describe your service, area and experience. Construction,…" → Beschrijf je dienst, je gebied en je ervaring. Voor bouwwerk, juridische controle of boekhoudwerk is een af…
- C · "I have reviewed the information." → Ik heb de gegevens gecontroleerd.
- C · "Review message" → Bericht controleren
- C · "Message copied. It has not been sent." → Bericht gekopieerd. Het is nog niet verstuurd.
- C · "Enlarge: Exterior view" → Vergroten: buitenaanzicht
- C · "Enlarge: Interior and stairs" → Vergroten: interieur en trap
- C · "Enlarge: Lower-level plan" → Vergroten: plattegrond van de benedenverdieping
- C · "Upper-level plan" → Plattegrond van de bovenverdieping
- C · "Playgrounds" → Speeltuinen
- C · "Favelas on the hillsides around the bay. The circles high…" → Favela's op de hellingen rond de baai. De cirkels markeren de favela's.
- C · "Favelas on the hillsides around the bay." → Favela's op de hellingen rond de baai.
- C · "Favelas on the hillsides at dusk. The circles highlight t…" → Favela's op de hellingen in de schemering. De cirkels markeren de favela's.
- C · "Favelas on the hillsides at dusk." → Favela's op de hellingen in de schemering.
- C · "Argus · Arc-based exchange" → Argus · handelsplatform op Arc
- C · "Its trading on a decentralised exchange, not yet chosen,…" → De handel erin op een gedecentraliseerd handelsplatform, dat nog niet is gekozen, en de vergoedingen uit di…
- C · "What it holds" → Wat erbij hoort
- C · "What it decides" → Wat er wordt beslist
- C · "How money moves" → Hoe het geld loopt
- C · "How the money moves: see how it works" → Hoe het geld loopt: bekijk hoe het werkt
- C · "How decisions would be shared" → Hoe besluiten verdeeld zouden worden
- C · "Household explanation: payments, repairs and decisions" → Uitleg voor huishoudens: betalingen, reparaties en besluiten
- C · "Eight groups take part, each with its own needs and decis…" → Acht groepen doen mee, elk met eigen behoeften en eigen besluiten.
- C · "Local decisions close to residents, with services shared…" → Lokale besluiten dicht bij de bewoners, met diensten die de projecten delen.
- C · "Decisions within the budget and safety rules, with suppor…" → Besluiten binnen de begroting en de veiligheidsregels, met steun voor deelname en een manier om vertegenwoo…
- C · "Expansion would share designs, purchasing, administration…" → Bij uitbreiding zouden ontwerpen, inkoop, administratie en verslaglegging gedeeld worden, terwijl lokale be…
- C · "The rules would distinguish the household’s agreement, re…" → De regels zouden onderscheid maken tussen de overeenkomst van het huishouden, de deelname van bewoners en d…
- C · "Who handles the work and how to question a decision" → Wie het werk regelt en hoe je een besluit aanvecht
- C · "Who pays for repairs, how quickly they are handled, who t…" → Wie reparaties betaalt, hoe snel ze worden uitgevoerd, wie je kunt benaderen en hoe je een rekening of repa…
- C · "A token vote cannot change a family’s agreement on its ow…" → Een stemming van tokenhouders kan de overeenkomst van een gezin niet op zichzelf veranderen. Mensen moeten…
- C · "Accessible mediation and review, with protection for hous…" → Toegankelijke bemiddeling en herbeoordeling, met bescherming van woonrechten.
- C · "Rules discussed with residents, spending limits and a way…" → Regels besproken met bewoners, uitgavenlimieten en een manier om besluiten aan te vechten.
- C · "Tasks, approvals, spending limits and who holds each role" → Taken, goedkeuringen, uitgavenlimieten en wie welke rol heeft
- C · "Voting procedures, spending limits and ways to resolve di…" → Stemprocedures, uitgavenlimieten en manieren om meningsverschillen op te lossen.
- C · "Named people with spending limits, checked by someone els…" → Mensen met een naam en een uitgavenlimiet, gecontroleerd door iemand anders, die verantwoording afleggen aa…
- C · "Rights, payment source, costs, losses, voting limits and…" → Rechten, bron van betalingen, kosten, verliezen, grenzen aan het stemrecht en regels voor verkoop. Er is ge…
- C · "Tasks are recorded with a responsible person, deadline an…" → Taken worden vastgelegd met een verantwoordelijke, een termijn en een budget. Binnen afgesproken grenzen ka…
- C · "A builder can describe the work and quote a price." → Een bouwer kan het werk beschrijven en een prijs opgeven.
- C · "The same method applies to construction and suppliers. A…" → Dezelfde werkwijze geldt voor de bouw en voor leveranciers. Een bouwer die verbonden is met een oprichter m…
- C · "The builder does not approve its own invoice. Approving s…" → De bouwer keurt zijn eigen factuur niet goed. Uitgaven goedkeuren, de levering controleren en betalen vrage…
- C · "The builder never approves its own invoice." → De bouwer keurt nooit zijn eigen factuur goed.
- C · "The builder is paid in reais" → De bouwer wordt in reais betaald
- C · "Rafael; legal adviser and budget lead not yet appointed." → Rafael; juridisch adviseur en budgetverantwoordelijke nog niet aangesteld.
- C · "Current involvement and planned roles. Professional refer…" → Huidige betrokkenheid en geplande rollen. Professionele referenties, aanstellingen en afspraken met partner…
- C · "What a token buyer would receive" → Wat een tokenkoper zou krijgen
- C · "The rights of token buyers." → De rechten van tokenkopers.
- C · "Comparison of social-purpose activity and investment with…" → Vergelijking tussen activiteiten met een maatschappelijk doel en investeringen met financiële rechten. De r…
- C · "Buyers of new tokens would pay the organisation that crea…" → Kopers van nieuwe tokens zouden betalen aan de organisatie die ze maakt en verkoopt; bij doorverkoop gaat h…
- C · "What Arc, USDC and the working tools are for, and their l…" → Waar Arc, USDC en de hulpmiddelen voor het werk voor dienen, en wat hun grenzen zijn. De volledige werking…
- C · "Describes per-pool fees charged in USDC. It does not show…" → Beschrijft vergoedingen per pool, gerekend in USDC. Het laat geen gebruik door IMOBX zien.
- C · "Sell before the cooperative exists and its founders agree…" → Verkopen voordat de coöperatie bestaat en haar oprichters de regels hebben vastgelegd.
- C · "IMOBX, if money remains and a written agreement allows it" → IMOBX, als er geld overblijft en een schriftelijke overeenkomst dat toestaat
- C · "Whitepaper, section 4: the cash policy" → Whitepaper, hoofdstuk 4: het kasbeleid (in het Engels)
- C · "Families would pay in reais and would need no crypto or d…" → Gezinnen zouden in reais betalen en zouden geen crypto of digitale wallet nodig hebben. Persoonsgegevens en…
- C · "Personal and household data" → Persoonsgegevens en gegevens van het huishouden
- C · "Housing plans, resident participation and proposed develo…" → Woonplannen, deelname van bewoners en voorgestelde ontwikkelingsfasen.
- C · "People checking documents, buildings and accounts" → Mensen die documenten, gebouwen en de boekhouding controleren
- C · "Home designs, purchasing, accounts and reports." → Woningontwerpen, inkoop, boekhouding en verslagen.
- C · "Project organisation, agreements and account reporting." → Projectorganisatie, overeenkomsten en financiële verslaglegging.
- C · "The proposed pilot: a family pays towards its home, with…" → De voorgestelde pilot: een gezin betaalt voor de eigen woning, met een openbare boekhouding.
- C · "Current project reference: Portuguese PDF" → Huidige projectreferentie: Portugese PDF
- C · "Current project reference: Read the reference" → Huidige projectreferentie: lees de referentie
- C · "IMOBX media kit: View kit" → IMOBX-mediakit: kit bekijken
- C · "Digital trials alongside the housing project" → Digitale tests naast het woonproject
- S · "Settled so far:" → Tot nu toe vastgelegd:
- S · "Everything still open" → Alles wat nog openstaat
- S · "Concept illustration made with an image generator from Ra…" → Conceptillustratie, gemaakt met een beeldgenerator op basis van de visie van Rafael. De illustratie toont e…
- S · "It pays for living there." → De huur betaalt het wonen.
- S · "The rights of people whose personal data is processed. It…" → De rechten van mensen van wie persoonsgegevens worden verwerkt. Het artikel gaat niet over blockchains.
- S · "The work is under way." → Het werk loopt al.
- S · "The pitch deck presents the project to partners. The pilo…" → De pitch deck stelt het project voor aan partners. De gids voor de pilot en de bouw beschrijft het werk en…
- S · "What to agree" → Wat we afspreken
- S · "Order for using money" → Volgorde voor het gebruik van het geld
- S · "Arctide · integration documentation" → Arctide · integratiedocumentatie (in het Engels)

## Checks run (python3)

nl.json parses; 987 keys, the same set and order as nl.draft.json; leading and trailing whitespace of every value matches its key (none); no em or en dashes; no "het token"; no " u " or " uw "; no exclamation marks; "(in het Engels)" appears where, and only where, the Portuguese has "(em inglês)"; no "promotie" where the English says outreach, and no "voorlichting" where it says promotion. The site's own `add_dutch` was also run on a scratch copy of the pages: no strings missing, and split sentences (for example "Hij legt betalingen vast. Hij controleert geen werk en vervangt geen contract." and "Tot nu toe vastgelegd: 0 van 9.") join correctly.

## Not sure about (for the native reviewer)

1. **Properties page title "Studies and records"** is now "Studies en opnamen", with "Andere opnamen en referenties" for the section. On that page the records are the team's photos, so "registers" (decision 7) would mislead. Please confirm.
2. **Decision 2 applied literally.** "How outreach work is paid" is now "Hoe voorlichtingswerk wordt betaald", although the paid work it describes is promotion. If "voorlichting" sounds wrong there, the English source should change, not just the Dutch.
3. **"Whitepaper, section N"** = "hoofdstuk N" in all three places. Elsewhere "sections" of a document stay "paragrafen" or "onderdelen".
4. **Source notes "It does not review IMOBX."** keep the draft's "Het beoordeelt IMOBX niet." even after a de-word title (documentatie, aankondiging). It is consistent and common in Dutch, but "De bron beoordeelt IMOBX niet." would be stricter.
5. **"Een eigenaar … of hij overweegt …"** uses the generic "hij". A native reviewer may prefer a neutral wording.
6. **"De pitch deck"** (de-woord) is kept. "Het pitch deck" is also used in Dutch.

## Codex and DeepSeek round (26 Oct)

**What this is.** A second editor's pass that applies two independent reviews of `nl.json` (Codex: 20 findings; DeepSeek: 39 findings in three parts) using the builder's rulings 1 to 10. 56 entries were changed, 931 kept. Same 987 keys, byte-identical, same order and file format. Like the first pass, this is an AI editor's work and does not replace a review by a native Dutch speaker.

**Count.** 43 findings accepted (19 of Codex's 20, 24 of DeepSeek's 39; two of them only in part, see the notes), 16 rejected. Some findings overlap (Codex 1 and 2 = DeepSeek part 3, items 6 and 7; DeepSeek part 3, item 2 was folded into the ruling 1 fix of the same entry). The 43 findings, plus applying ruling 1's pattern to every entry with the same construction, account for 50 changed entries; 6 more are consistency changes made because of them.

### Accepted (EN → old → new)

Notes on partial or adapted acceptances:
- **"Needs"** (phase cards on the roadmap page): DeepSeek was right that "Heeft nodig" is a fragment without a subject, but "Behoeften" would change the meaning, because the label introduces each phase's preconditions ("Needs: property-use documents, a budget and reviewed agreements"). Used "Nodig".
- **"Its trading on a decentralised exchange …"**: "erin" → "in de token" accepted for clarity; "beurs" rejected, because exchange = handelsplatform is settled.
- **"Responses to broken rules that start small …"**: Codex's diagnosis accepted (the relative clause seemed to say the rules start small), but the entry stays a noun phrase like its neighbours in the list: "Eerst lichte maatregelen bij het overtreden van regels, met het recht om gehoord te worden."
- **"Eight groups take part …"**: DeepSeek's meaning fix ("decisions to make") accepted; "besluit" kept, not "beslissing", per the first pass's settled term.
- **Named people (ruling 2)**: the second entry now says that their spending is checked by someone else ("van wie de uitgaven door iemand anders worden gecontroleerd").
- **"Appointment depends on …"** (builder, reference page) and **"Housing, appointments and funding …"** (contact page): the Portuguese is "contratação", hiring a contractor or service. "Opdracht" now matches the contact page's own "Dit kennismakingsbericht bevestigt geen opdracht". "Aanstelling" stays for people appointed to a role (legal adviser, inspector, budget lead).

**Ruling 1: money or a sale as the grammatical subject** (8)

- "Part of each monthly payment buys the home. No down payment."
  - old: Een deel van elke maandbetaling koopt de woning. Geen aanbetaling.
  - new: Een deel van elke maandbetaling telt mee voor de aankoop van de woning. Geen aanbetaling.
- "A bucket that empties each month: rent pays for living there, and none of it buys the home."
  - old: Een emmer die elke maand leegloopt: de huur betaalt het wonen, en niets daarvan koopt de woning.
  - new: Een emmer die elke maand leegloopt: met de huur betaal je om er te wonen, en niets daarvan telt mee voor de aankoop van de woning.
- "It pays for living there."
  - old: De huur betaalt het wonen.
  - new: Met de huur betaal je om er te wonen.
- "Part buys the home; another part pays for upkeep and repairs."
  - old: Een deel koopt de woning; een ander deel betaalt onderhoud en reparaties.
  - new: Een deel telt mee voor de aankoop van de woning; met een ander deel worden onderhoud en reparaties betaald.
- "Each month there is one payment: part is rent, part buys the home. The record shows how much has been paid and…"
  - old: Elke maand is er één betaling: een deel is huur, een deel koopt de woning. De registratie toont hoeveel er al is betaald en hoeveel van de afgesproken prijs nog openstaat. Prijs, looptijd en eventuele prijswijzigingen moeten passen bij het budget van het gezin en de kosten van het project. Zodra de woning van het gezin is, rekent IMOBX er geen huur meer voor.
  - new: Elke maand is er één betaling: een deel is huur, een deel telt mee voor de aankoop van de woning. Het register toont hoeveel er al is betaald en hoeveel van de afgesproken prijs nog openstaat. Prijs, looptijd en eventuele prijswijzigingen moeten passen bij het budget van het gezin en de kosten van het project. Zodra de woning van het gezin is, rekent IMOBX er geen huur meer voor.
- "An agreed use, such as operations and paying the people who do the work; a sale between holders pays the selle…"
  - old: Een afgesproken gebruik, zoals de bedrijfsvoering en het betalen van de mensen die het werk doen; een verkoop tussen houders betaalt de verkoper
  - new: Een afgesproken gebruik, zoals de bedrijfsvoering en het betalen van de mensen die het werk doen; bij een verkoop tussen houders gaat het geld naar de verkoper
- "Homes kept for rent earn income for as long as they are owned. With rent-to-own, the income from a home ends w…"
  - old: Huurwoningen leveren inkomsten op zolang ze eigendom blijven. Bij huurkoop stopt het inkomen uit een woning als het gezin de aankoop heeft afgerond. Daarom moet het geld dat via aankopen terugkomt, nieuwe woningen betalen. De coöperatie heeft ook een basis nodig die blijvend inkomen oplevert, zoals gedeelde ruimtes en diensten. Dit is nog niet getest.
  - new: Woningen die voor verhuur worden aangehouden, leveren inkomsten op zolang ze eigendom van de verhuurder blijven. Bij huurkoop stopt het inkomen uit een woning als het gezin de aankoop heeft afgerond. Daarom moet het geld dat via aankopen terugkomt, worden gebruikt om nieuwe woningen te financieren. De coöperatie heeft ook een basis nodig die blijvend inkomen oplevert, zoals gedeelde ruimtes en diensten. Dit is nog niet getest.
- "Fees would first pay for running the project and for new homes. Any payment to holders would come later, only…"
  - old: De vergoedingen zouden eerst de lopende kosten van het project en nieuwe woningen betalen. Een eventuele betaling aan houders zou later komen, alleen uit geld dat al is ontvangen, en alleen zodra de inkomsten van de woningen de lopende kosten zouden dekken.
  - new: De vergoedingen zouden eerst worden gebruikt voor de bedrijfsvoering van het project en voor nieuwe woningen. Een eventuele betaling aan houders zou later komen, alleen uit geld dat al is ontvangen, en alleen zodra de inkomsten van de woningen de lopende kosten zouden dekken.

**Ruling 1 applied to the same construction elsewhere** (6)

- "What a buyer would receive has not been decided. A buyback pays sellers; burning tokens does not automatically…"
  - old: Wat een koper zou krijgen, is nog niet besloten. Bij een terugkoop krijgen de verkopers geld; tokens verbranden betaalt de anderen niet automatisch. Een advocaat toetst dit aan de regels van de CVM voordat er iets wordt verkocht. Als er geen wettige manier is, gaat IMOBX verder zonder token.
  - new: Wat een koper zou krijgen, is nog niet besloten. Bij een terugkoop krijgen de verkopers geld; als tokens worden verbrand, krijgen de anderen niet automatisch geld. Een advocaat toetst dit aan de regels van de CVM voordat er iets wordt verkocht. Als er geen wettige manier is, gaat IMOBX verder zonder token.
- "Every amount received would be recorded, and money given for a set purpose would keep that purpose. The rest w…"
  - old: Elk ontvangen bedrag zou worden vastgelegd, en geld dat voor een bepaald doel is gegeven, zou dat doel houden. De rest zou belastingen en rekeningen betalen, daarna reserves en toezeggingen aan gezinnen, daarna nieuwe woningen; investeerders zouden alleen worden betaald als er geld overblijft en een overeenkomst dat toestaat.
  - new: Elk ontvangen bedrag zou worden vastgelegd, en geld dat voor een bepaald doel is gegeven, zou dat doel houden. De rest zou gaan naar belastingen en rekeningen, daarna naar reserves en toezeggingen aan gezinnen, daarna naar nieuwe woningen; investeerders zouden alleen worden betaald als er geld overblijft en een overeenkomst dat toestaat.
- "Donations and grants can pay for preparation and building. An investment depends on a lawful route, and invest…"
  - old: Donaties en subsidies kunnen de voorbereiding en de bouw betalen. Een investering hangt af van een route die de wet toestaat, en investeerders krijgen alleen de rechten die in hun overeenkomst staan.
  - new: Met donaties en subsidies kunnen de voorbereiding en de bouw worden betaald. Een investering hangt af van een route die de wet toestaat, en investeerders krijgen alleen de rechten die in hun overeenkomst staan.
- "Part of the trading fees would go into a fund used only to build homes. A token’s price and money locked in a…"
  - old: Een deel van de handelsvergoedingen zou naar een fonds gaan dat alleen wordt gebruikt om woningen te bouwen. De prijs van een token en geld dat vastzit in een handelsmarkt betalen geen bouwrekeningen.
  - new: Een deel van de handelsvergoedingen zou naar een fonds gaan dat alleen wordt gebruikt om woningen te bouwen. Met de prijs van een token en met geld dat vastzit in een handelsmarkt worden geen bouwrekeningen betaald.
- "What it may pay for"
  - old: Waarvoor het mag betalen
  - new: Waarvoor het mag worden gebruikt
- "If one is created, it would fund the work and pay for promotion, and it would stay apart from the housing coop…"
  - old: Als er een wordt gemaakt, zou die het werk financieren en promotie betalen, en zou die los blijven van de woningcoöperatie.
  - new: Als er een wordt gemaakt, zou die dienen om het werk te financieren en promotie te betalen, en zou die los blijven van de woningcoöperatie.

**Ruling 2: named people** (2)

- "Each neighbourhood would decide its own matters, the projects would share tools, and named people would answer…"
  - old: Elke buurt zou over haar eigen zaken beslissen, de projecten zouden hulpmiddelen delen, en mensen met naam zouden verantwoording afleggen over geld en werk.
  - new: Elke buurt zou over haar eigen zaken beslissen, de projecten zouden hulpmiddelen delen, en bij naam genoemde mensen zouden verantwoording afleggen over geld en werk.
- "Named people with spending limits, checked by someone else and accountable to residents and funders."
  - old: Mensen met een naam en een uitgavenlimiet, gecontroleerd door iemand anders, die verantwoording afleggen aan bewoners en financiers.
  - new: Bij naam genoemde mensen met een uitgavenlimiet, van wie de uitgaven door iemand anders worden gecontroleerd, en die verantwoording afleggen aan bewoners en financiers.

**Ruling 4: records on the photo page** (2)

- "IMOBX | Studies and records"
  - old: IMOBX | Studies en opnamen
  - new: IMOBX | Studies en vastleggingen
- "Other records and references"
  - old: Andere opnamen en referenties
  - new: Andere vastleggingen en verwijzingen

**Ruling 5: one wording for "not a listing of available homes"** (1)

- "The drawings and photos show the proposal. This is not a listing of available homes."
  - old: De tekeningen en foto's tonen het voorstel. Dit is geen lijst van beschikbare woningen.
  - new: De tekeningen en foto's tonen het voorstel. Dit is geen aanbod van beschikbare woningen.

**Ruling 6: "None of this works yet"** (2)

- "Each IMOBX payment, and who approved it, would be recorded on Arc, a public blockchain, so anyone can check it…"
  - old: Elke betaling van IMOBX, en wie die heeft goedgekeurd, zou worden vastgelegd op Arc, een openbare blockchain, zodat iedereen het kan controleren. Niets hiervan werkt al: het eerste project gaat het testen.
  - new: Elke betaling van IMOBX, en wie die heeft goedgekeurd, zou worden vastgelegd op Arc, een openbare blockchain, zodat iedereen het kan controleren. Dit werkt allemaal nog niet: het eerste project gaat het testen.
- "The digital support channel would let people submit requests, follow progress and read decisions. Agreed rules…"
  - old: Via het digitale ondersteuningskanaal zouden mensen verzoeken kunnen indienen, de voortgang volgen en besluiten lezen. Afgesproken regels, niet de bot, zouden bepalen wie mag beslissen en uitgeven. Niets hiervan werkt al.
  - new: Via het digitale ondersteuningskanaal zouden mensen verzoeken kunnen indienen, de voortgang volgen en besluiten lezen. Afgesproken regels, niet de bot, zouden bepalen wie mag beslissen en uitgeven. Dit werkt allemaal nog niet.

**Ruling 8: issuer** (1)

- "The risks as described by the issuer."
  - old: De risico's zoals de uitgever ze beschrijft.
  - new: De risico's zoals de uitgevende instelling ze beschrijft.

**Ruling 9: fees charged** (3)

- "A fee charged when someone buys or sells a token."
  - old: Een vergoeding die wordt gerekend als iemand een token koopt of verkoopt.
  - new: Een vergoeding die in rekening wordt gebracht als iemand een token koopt of verkoopt.
- "Describes per-pool fees charged in USDC. It does not show any IMOBX use."
  - old: Beschrijft vergoedingen per pool, gerekend in USDC. Het laat geen gebruik door IMOBX zien.
  - new: Beschrijft vergoedingen per pool, die in USDC in rekening worden gebracht. Het laat geen gebruik door IMOBX zien.
- "The founders’ first choice for launching it is Arctide, a platform on Arc where tokens are launched and traded…"
  - old: De eerste keuze van de oprichters om de token te lanceren is Arctide, een platform op Arc waar tokens worden gelanceerd en verhandeld. Uit de gepubliceerde documentatie blijkt dat elke handelspool eigen instellingen voor vergoedingen en een eigen ontvanger van de vergoedingen heeft, en dat de vergoedingen in USDC, een digitale dollar, worden gerekend. Zo hoeven de vergoedingen niet betaald te worden in een tweede cryptomunt waarvan de koers sterker schommelt; het wisselkoersrisico tussen dollars en reais, en de risico's van USDC zelf, blijven bestaan.
  - new: De eerste keuze van de oprichters om de token te lanceren is Arctide, een platform op Arc waar tokens worden gelanceerd en verhandeld. Uit de gepubliceerde documentatie blijkt dat elke handelspool eigen instellingen voor vergoedingen en een eigen ontvanger van de vergoedingen heeft, en dat de vergoedingen in USDC, een digitale dollar, in rekening worden gebracht. Zo hoeven de vergoedingen niet betaald te worden in een tweede cryptomunt waarvan de koers sterker schommelt; het wisselkoersrisico tussen dollars en reais, en de risico's van USDC zelf, blijven bestaan.

**Other Codex findings (ruling 10)** (10)

- "Missing resident participation or an accessible review process requires the rules to be revised before use."
  - old: Zonder deelname van bewoners of een toegankelijke herbeoordeling moeten de regels worden aangepast voordat ze worden gebruikt.
  - new: Als deelname van bewoners ontbreekt of er geen toegankelijke procedure voor herbeoordeling is, moeten de regels worden aangepast voordat ze worden gebruikt.
- "This page lists the people and roles in the project, the sources and the version history. Each person’s rights…"
  - old: Deze pagina noemt de mensen en rollen in het project, de bronnen en de versiegeschiedenis. De rechten van elke persoon hangen af van getekende overeenkomsten en officiële registraties.
  - new: Deze pagina noemt de mensen en rollen in het project, de bronnen en de versiegeschiedenis. De rechten van elke persoon hangen af van getekende overeenkomsten en officiële registers.
- "Proof builds trust, and trust draws in funding and scale. Each phase starts only when the one before has shown…"
  - old: Bewijs bouwt vertrouwen op, en vertrouwen trekt financiering en schaal aan. Elke fase begint pas als de vorige resultaten heeft laten zien: woningen gebouwd binnen de begroting en vastgelegde betalingen.
  - new: Bewijs bouwt vertrouwen op, en vertrouwen trekt financiering aan en maakt groei mogelijk. Elke fase begint pas als de vorige resultaten heeft laten zien: woningen gebouwd binnen de begroting en vastgelegde betalingen.
- "The founders’ construction company is the proposed builder: the whole village at once, with every cost checked…"
  - old: Het bouwbedrijf van de oprichters is de voorgestelde bouwer: het hele dorp in één keer, waarbij elke kostenpost wordt gecontroleerd door iemand buiten de oprichters.
  - new: Het bouwbedrijf van de oprichters is de voorgestelde bouwer: het hele dorp in één keer, waarbij elke kostenpost wordt gecontroleerd door iemand die niet tot de oprichters behoort.
- "Rafael’s budget, the different building work covered by each case and the planned use of money. A forecast of…"
  - old: De begroting van Rafael, het verschillende bouwwerk dat elk geval omvat en het geplande gebruik van het geld. Een prognose van het geld dat binnenkomt en uitgaat, met de kosten van het gekozen project en verschillende gevallen voor vertraging en reparaties, wordt uitgewerkt.
  - new: De begroting van Rafael, de bouwwerkzaamheden die elk geval omvat en het geplande gebruik van het geld. Een prognose van het geld dat binnenkomt en uitgaat, met de kosten van het gekozen project en verschillende scenario's voor vertragingen en reparaties, wordt uitgewerkt.
- "Costs fair to what each household receives and can afford."
  - old: Kosten die eerlijk zijn naar wat elk huishouden krijgt en kan betalen.
  - new: Kosten die in een eerlijke verhouding staan tot wat elk huishouden krijgt en kan betalen.
- "Know whether they are donating, leasing or selling, when responsibility changes and which costs remain theirs."
  - old: Weten of ze schenken, verhuren of verkopen, wanneer de verantwoordelijkheid overgaat en welke kosten voor hen blijven.
  - new: Weten of ze schenken, verhuren of verkopen, wanneer de verantwoordelijkheid overgaat en welke kosten voor hun rekening blijven.
- "Responses to broken rules that start small, with a right to be heard."
  - old: Reacties op overtreden regels die klein beginnen, met het recht om gehoord te worden.
  - new: Eerst lichte maatregelen bij het overtreden van regels, met het recht om gehoord te worden.
- "The first project’s foundations cover the legal organisation, property documents, a construction budget in rea…"
  - old: De basis van het eerste project omvat de juridische organisatie, de documenten van het pand, een bouwbegroting in reais en de voorwaarden voor wonen en kopen. Gesprekken met mogelijke huishoudens zijn onderdeel van deze voorbereiding.
  - new: De basis van het eerste project omvat de juridische organisatie, de documenten van het pand, een bouwbegroting in reais en de voorwaarden voor wonen en kopen. Gesprekken met huishoudens die mogelijk willen deelnemen, zijn onderdeel van deze voorbereiding.
- "Legal and design"
  - old: Juridisch en ontwerp
  - new: Juridische zaken en ontwerp

**Other DeepSeek findings (ruling 10)** (15)

- "Appointment depends on the agreed work, price comparison and approval by someone independent of the builder."
  - old: Aanstelling hangt af van het afgesproken werk, een prijsvergelijking en goedkeuring door iemand die onafhankelijk is van de bouwer.
  - new: Of de bouwer de opdracht krijgt, hangt af van het afgesproken werk, een prijsvergelijking en goedkeuring door iemand die onafhankelijk is van de bouwer.
- "The team replies on Telegram. The subject and location help direct the conversation. The team may ask question…"
  - old: Het team antwoordt via Telegram. Het onderwerp en de locatie helpen om het gesprek goed te richten. Het team kan vragen stellen, of met je een beoordeling, een overleg of een bespreking van je voorstel afspreken. Wonen, aanstellingen en financiering hangen elk af van eigen overeenkomsten.
  - new: Het team antwoordt via Telegram. Het onderwerp en de locatie helpen om het gesprek goed te richten. Het team kan vragen stellen, of met je een beoordeling, een overleg of een bespreking van je voorstel afspreken. Wonen, opdrachten en financiering hangen elk af van eigen overeenkomsten.
- "On 30 November 2025, Rafael imagined 45 m² duplex homes facing a shared area, with solar power, an orchard, pl…"
  - old: Op 30 november 2025 bedacht Rafael duplexwoningen van 45 m² rond een gedeelde ruimte, met zonne-energie, een boomgaard, speelruimte en twee kleine studieruimtes. Het ontwerp wil een weg naar eigendom samenbrengen met lagere uitgaven voor het huishouden en plekken om elkaar te ontmoeten en te leren.
  - new: Op 30 november 2025 bedacht Rafael duplexwoningen van 45 m² die uitkijken op een gedeelde ruimte, met zonne-energie, een boomgaard, speelruimte en twee kleine studieruimtes. Het ontwerp wil een weg naar eigendom samenbrengen met lagere uitgaven voor het huishouden en plekken om elkaar te ontmoeten en te leren.
- "This method would be agreed with participants and tested in the pilot, including when an invoice is disputed o…"
  - old: Deze werkwijze zou met de deelnemers worden afgesproken en in de pilot worden getest, ook voor als een factuur wordt betwist of een verantwoordelijke wordt vervangen.
  - new: Deze werkwijze zou met de deelnemers worden afgesproken en in de pilot worden getest, ook wanneer een factuur wordt betwist of een verantwoordelijke wordt vervangen.
- "How much runs on Arc, and what a token would give its buyers."
  - old: Hoeveel via Arc loopt, en wat een token zijn kopers zou geven.
  - new: Hoeveel er via Arc loopt, en wat een token zijn kopers zou geven.
- "Housing terms and participation in shared matters."
  - old: Woonvoorwaarden en inspraak in gezamenlijke zaken.
  - new: Woonvoorwaarden en deelname aan gezamenlijke zaken.
- "The agreement would say how to handle temporary hardship, how amounts already credited are kept and what happe…"
  - old: De overeenkomst zou regelen hoe om te gaan met tijdelijke moeilijkheden, wat er gebeurt met bedragen die al zijn opgebouwd en wat er gebeurt als het gezin vertrekt of IMOBX niet verder kan. Een terugbetaling, uitstel van betaling of korting geldt alleen als die in de overeenkomst is opgenomen.
  - new: De overeenkomst zou regelen hoe om te gaan met tijdelijke moeilijkheden, hoe bedragen die al zijn bijgeschreven, behouden blijven en wat er gebeurt als het gezin vertrekt of IMOBX niet verder kan. Een terugbetaling, uitstel van betaling of korting geldt alleen als die in de overeenkomst is opgenomen.
- "Eight groups take part, each with its own needs and decisions to make."
  - old: Acht groepen doen mee, elk met eigen behoeften en eigen besluiten.
  - new: Acht groepen doen mee, elk met eigen behoeften en besluiten die ze moeten nemen.
- "Needs"
  - old: Heeft nodig
  - new: Nodig
- "More in the roadmap"
  - old: Meer bij Projectfasen
  - new: Meer op de pagina Projectfasen
- "Sell before the cooperative exists and its founders agree its rules."
  - old: Verkopen voordat de coöperatie bestaat en haar oprichters de regels hebben vastgelegd.
  - new: Verkopen voordat de coöperatie bestaat en haar oprichters de regels hebben goedgekeurd.
- "Legal advisers still need to confirm what it requires of IMOBX."
  - old: Juridisch adviseurs moeten nog bevestigen wat dit van IMOBX vraagt.
  - new: Juridische adviseurs moeten nog bevestigen wat dit van IMOBX vraagt.
- "Its trading on a decentralised exchange, not yet chosen, and the fees from that trading"
  - old: De handel erin op een gedecentraliseerd handelsplatform, dat nog niet is gekozen, en de vergoedingen uit die handel
  - new: De handel in de token op een gedecentraliseerd handelsplatform, dat nog niet is gekozen, en de vergoedingen uit die handel
- "What will be reported?"
  - old: Wat wordt er gerapporteerd?
  - new: Wat zal er worden gerapporteerd?
- "Reporting period and who prepared and checked the accounts."
  - old: Verslagperiode en wie de cijfers heeft opgesteld en gecontroleerd.
  - new: Verslagperiode en wie de boekhouding heeft opgesteld en gecontroleerd.

### Rejected (with reason)

- **Codex 4, "Roadmap" → "Projectfasen".** On the reference page this heading is the title of a chapter of Rafael's document (`id="chapter-roadmap"`, beside "Risk and compliance" and "Scenarios and risks"). It is not a link to the Projectfasen page. The first pass kept "Routekaart" for exactly this chapter.
- **DeepSeek 1.1, "What it holds" → "Wat het bevat".** One key serves three places: a column of the records table on the blockchain page, the cooperative card and the token card on the token page. "Het" does not fit the de-words coöperatie and token, and "bevat" reads oddly for homes and reserves. The cells carry the meaning, so "Wat erbij hoort" stays.
- **DeepSeek 1.2 and 3.12, "hoofdstuk" → "sectie".** Ruling 3: "hoofdstuk N" stays in all three whitepaper links.
- **DeepSeek 1.6, "vorm van samenwerking" → "regeling".** The Portuguese original is "a forma de participação". The current wording is closer to it, and "regeling" is vaguer.
- **DeepSeek 1.7, "aanbod" → "lijst".** Ruling 5: "geen aanbod van beschikbare woningen" everywhere. The one entry that still said "geen lijst" was changed the other way.
- **DeepSeek 1.11 and 1.12, "registers" on the photo page.** Ruling 4: "vastleggingen" there, "registers" only for the shared records.
- **DeepSeek 1.14, "Inkomsten en uitgaven" → "Geld in en uit".** The heading is a chapter title of Rafael's document (Portuguese "Entradas e saídas"). "Inkomsten en uitgaven" is the standard Dutch for it, and "Geld in en uit" is not idiomatic. The "geld dat binnenkomt en uitgaat" it was compared with translates a different English string.
- **DeepSeek 1.16, "crypto" / "digitale wallet" → "cryptovaluta" / "digitale portemonnee".** This is a style preference (P3). Both words are common Dutch at B1 and are used the same way elsewhere ("cryptowallet", "crypto en financiële producten"). There is no meaning, grammar or consistency fault.
- **DeepSeek 1.17, 2.8 and 2.9, "slides" → "dia's".** "Slides" is standard Dutch for presentation slides and is used the same way in all three entries. There is no fault to fix.
- **DeepSeek 2.3, "Update record" → "Wijzigingsregister".** This is the changelog of the reference page. Ruling 4 keeps "registers" for the shared-records sense, and "Overzicht van wijzigingen" is the natural Dutch here.
- **DeepSeek 2.5, "Zien" → "Bekijk".** This is not an imperative. The entry is a cell in the roadmap's roles table, under "What they need from the project" for donors and social funders. Its sibling cells are infinitives too ("Precies weten wat ze kopen …"), so an imperative would break the pattern.
- **DeepSeek 3.13, "commitment pooling" → "het bundelen van toezeggingen".** Ruling 7: the titles of linked sources stay as written.

### Further consistency changes made because of these findings

- **"counts towards buying" = "telt mee voor de aankoop"** in all entries, to match the wording that ruling 1 sets for the homepage card. In four entries "koop" became "aankoop". "Huur omzetten in koop" keeps "koop" as the headline phrase, and "Geld dat is bijgeschreven voor de koop van een gezin" is unchanged.
- **"Other references" → "Andere verwijzingen"**, the jump link on the photo page, to match its section "Andere vastleggingen en verwijzingen" (ruling 4).
- **"juridische adviseurs"** (plural) also in the roadmap line "Bestuurders, accountant en juridische adviseurs nog niet aangesteld". The singular job title "juridisch adviseur" stays.

- "Before moving in, the family knows the price, the payment in reais and how much of each payment counts towards…"
  - old: Voordat het gezin er gaat wonen, kent het de prijs, de betaling in reais en hoeveel van elke betaling meetelt voor de koop.
  - new: Voordat het gezin er gaat wonen, kent het de prijs, de betaling in reais en hoeveel van elke betaling meetelt voor de aankoop.
- "Final price, price changes, what counts toward purchase, late payments, leaving and how representatives are ch…"
  - old: Uiteindelijke prijs, prijswijzigingen, wat meetelt voor de koop, te late betalingen, vertrek en hoe vertegenwoordigers worden gekozen.
  - new: Uiteindelijke prijs, prijswijzigingen, wat meetelt voor de aankoop, te late betalingen, vertrek en hoe vertegenwoordigers worden gekozen.
- "The price, the monthly payment and how much of each payment counts towards buying the home."
  - old: De prijs, het maandbedrag en hoeveel van elke betaling meetelt voor de koop van de woning.
  - new: De prijs, het maandbedrag en hoeveel van elke betaling meetelt voor de aankoop van de woning.
- "Turn rent into a purchase: part of each monthly payment counts towards buying the home."
  - old: Huur omzetten in koop: een deel van elk maandbedrag telt mee voor de koop van de woning.
  - new: Huur omzetten in koop: een deel van elk maandbedrag telt mee voor de aankoop van de woning.
- "Other references"
  - old: Andere referenties
  - new: Andere verwijzingen
- "Administrators, accountant and legal advisers not yet appointed."
  - old: Bestuurders, accountant en juridisch adviseurs nog niet aangesteld.
  - new: Bestuurders, accountant en juridische adviseurs nog niet aangesteld.

**Kept on purpose (same pattern checked, no change):**
- "Een token wordt onderzocht om het werk te financieren en promotie te betalen". This is a purpose clause, and nothing in it is a payer. The "zou die …" twin was changed to "zou die dienen om …".
- "financieren" with fees or a token as the subject ("Handelsvergoedingen zouden betaald werk … financieren", "zou die de … begrotingsposten financieren"). Dutch uses this naturally.
- "Zodra de woning van het gezin is, rekent IMOBX er geen huur meer voor". IMOBX is the subject, and "huur rekenen" is idiomatic. Ruling 9 concerns fees charged in USDC. All three of those now say "in rekening gebracht".
- "Lopende kosten" stays for "running costs" in the second sentence of the fees entry. Only "running the project" became "bedrijfsvoering".
- "De foto's zijn opnamen die het team heeft aangeleverd" (body text on the photo page). Ruling 4 covers the page title and the section heading. In body text, "opnamen" for photographs is natural. The native reviewer can confirm.

### Checks run (python3)

`nl.json` parses. It has 987 keys, the same set and order as the file before this round, and the same file format (one-space indent, UTF-8, trailing newline). The leading and trailing whitespace of every value matches its key. The file has no em or en dashes, no "het token", no " u " or " uw ", and no exclamation marks. "Geen aanbod van beschikbare woningen" appears in 2 entries, and "geen lijst van beschikbare woningen" appears in none. None of the old constructions is left ("koopt de woning", "betaalt het wonen", "betaalt de verkoper", "Niets hiervan", "opnamen" in the title or section, "gerekend" for USDC fees). The three whitepaper links say "hoofdstuk". The one "sectie" is the pre-existing "titel van de sectie" in the reference page's citation note, which is not a whitepaper chapter. None of the changed entries is a joined fragment, so no split sentence was affected.

### Items from the first pass's "Not sure about" now settled

- Item 1 (photo-page "records"): settled by ruling 4, "Studies en vastleggingen" / "Andere vastleggingen en verwijzingen".
- Item 3 ("Whitepaper, section N"): settled by ruling 3, "hoofdstuk N".

## Confirmation round (26 Oct): Codex and DeepSeek on the 56 changed entries
Both confirm every earlier P1 fixed; both 'ready after fixes'. Applied: 'officiële documenten' (pt 'documentos oficiais'); photo page title and section 'documentatie'; 'de verschillende bouwwerkzaamheden die bij elk geval horen'; 'de financiële overzichten'; label 'Needs' = 'Wat nodig is'; comma removed in the restrictive clause after 'bijgeschreven'.
