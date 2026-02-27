# IMOBX Website + Design Skill Audit Prompt

**Purpose:** Copy-paste this into Gemini, ChatGPT, or any LLM to get an independent audit of the IMOBX website design against the design skill rules.

---

## Instructions for the Auditor

You are auditing a tokenized real estate website (IMOBX) against its own design system rules. Be harsh. Flag every deviation. Score each page 0-100.

**Your job:**
1. Read the Design Skill rules below (the "spec")
2. Read each HTML page provided (the "implementation")
3. For each page, produce a compliance table showing pass/fail per rule
4. Flag contradictions between the design skill and the CSS
5. Recommend specific fixes with code snippets
6. Score overall design coherence

---

## SECTION A: Design Skill (The Spec)

### Brand Palette (Web — Dark Mode)
```css
:root {
    --imobx-bg: #0A0A0A;          /* Background */
    --imobx-surface: #1F1F23;      /* Cards/elevated */
    --imobx-border: #27272A;       /* Borders */
    --imobx-text: #FFFFFF;         /* Text */
    --imobx-muted: #A1A1AA;       /* Secondary text */
    --imobx-turquoise: #4A90A4;   /* Technical accent */
    --imobx-orange: #FF8C00;      /* Strategic accent (rare) */
    --imobx-green: #10B981;       /* Success/transparency */
    --imobx-red: #DC2626;         /* Errors only */
}
```

### Current CSS (styles.css) — DIFFERENT PALETTE
```css
:root {
    --imobx-technical: #14B8A6;    /* ← NOT #4A90A4 */
    --imobx-framework: #F97316;    /* ← NOT #FF8C00 */
    --imobx-strategic: #D4AF37;    /* ← NOT #FF8C00 */
    --imobx-bg: #FFFFFF;           /* ← NOT #0A0A0A (LIGHT MODE!) */
    --imobx-text: #1A1A1A;        /* ← NOT #FFFFFF */
}
```

**AUDIT QUESTION 1:** The design skill mandates dark mode (#0A0A0A background). The CSS uses white (#FFFFFF). Which pages comply? Which don't? What's the migration path?

### 3-Box System Rules
- **Technical boxes (turquoise):** 2-4 per section (40-50%)
- **Framework boxes (turquoise border, different label):** 2-3 per section (30-40%)
- **Strategic boxes (orange, RARE):** 1-2 MAX per section (10-20%)
- **Every section must start with 2-3 sentences of prose** before boxes (smoothing rule)
- **60-70% prose, 20-25% tech/framework boxes, 5-10% strategic boxes** (rhythm rule)

**AUDIT QUESTION 2:** Count the box types on each page. Do they match the ratio? Are there sections that start with boxes without prose intros?

### Sharp Corners (Mandatory)
```css
* { border-radius: 0; }
.avatar { border-radius: 50% !important; } /* Only exception */
```

**AUDIT QUESTION 3:** Does any page use border-radius? Check all elements including buttons, inputs, cards, nav items.

### Required Pages (per skill)
| Page | Required | Exists? |
|------|----------|---------|
| Home | Yes | index.html + index-bootstrap.html (TWO versions!) |
| Tokenomics | Yes | tokenomics.html |
| Properties | Yes | properties.html |
| Rent-to-Own | Yes | rent-to-own.html |
| Treasury | Yes | NO (stub in research/) |
| Devsheet | Yes | NO |
| Buy | Not in spec | buy.html |
| DAO Demo | Not in spec | dao-demo.html |

**AUDIT QUESTION 4:** Which required pages are missing? Which existing pages aren't in the spec? Should they be?

### Transparency Requirements
Every claim must link to verification:
- Token supply → Etherscan contract
- Construction cost → SINAPI index reference
- LP lock → Lock contract address
- Treasury balance → Multisig address on-chain
- Rental income → Property management reports

**AUDIT QUESTION 5:** For each page, list every claim made and whether it links to a verification source. What percentage of claims are verifiable?

### Voice Rules
**Banned words:** revolutionary, disrupt, paradigm, transform, innovate, cutting-edge, game-changer, leverage, utilize, unlock, synergy, seamlessly, holistic, fundamentally, essentially

**AI fingerprints to kill:** em-dash overuse, "applies the same principle", vague benefits ("higher yields" without numbers), vocabulary tells ("validated", "targets", "leverage")

**AUDIT QUESTION 6:** Scan all page copy for banned words and AI fingerprints. List every occurrence.

### Responsive Breakpoints (per skill)
```css
@media (max-width: 1200px) { /* Collapse nav to hamburger */ }
@media (max-width: 900px)  { /* Stack grid layouts */ }
@media (max-width: 600px)  { /* Full-width, reduce padding */ }
```

**Current CSS uses only one breakpoint:** `@media (max-width: 768px)`

**AUDIT QUESTION 7:** Is the responsive implementation sufficient? Does the nav collapse to hamburger? What breaks between 600-900px?

---

## SECTION B: Pages to Audit

### Page 1: index.html (Custom CSS Homepage)
**Key elements:** Hero with dark photo overlay, 3-box color system, partner cards, jurisdiction table
**Known issues:** No hamburger menu, no buy CTA above fold, light mode background

### Page 2: index-bootstrap.html (Bootstrap/Tabler Homepage)
**Key elements:** "Where Do I Start?" cards, divide-y step lists, honest tone
**Known issues:** Light mode, border-radius: 8px on cards, gradient backgrounds (#4A90A4 → #FF8C00), dead links to whitepaper.html and bonzi-journey.html

### Page 3: buy.html
**Key elements:** Fee comparison table, step-by-step guide, email purchase widget, risk disclosure
**Known issues:** Dead email widget (console.log placeholder), duplicates tokenomics content

### Page 4: tokenomics.html
**Key elements:** Supply table, dual-yield A/B, burn mechanics, hardstaking comparison
**Known issues:** Same dead email widget, too table-heavy (violates 60-70% prose rule)

### Page 5: properties.html
**Key elements:** SINAPI milestone table, 4-pillar growth model, ROI example
**Known issues:** No property images (7 exist in assets/), links to SINAPI tracker stub

### Page 6: rent-to-own.html
**Key elements:** 180-month economics table, virtuous cycle steps, competitor comparison
**Known issues:** 2 strategic boxes (exceeds 1-2 MAX rule), links to grants stub

### Page 7: dao-demo.html (Bootstrap/Tabler)
**Key elements:** Wallet connect, stake widget, treasury overview, voting
**Known issues:** Purple gradients (#667eea), staking ETH not IMOBX, fake APY formula, lock slider goes to 90 days (should be 14 fixed)

---

## SECTION C: Consolidated Audit Questions

For your report, address each:

| # | Question | Scope |
|---|----------|-------|
| 1 | Dark mode compliance | All pages vs skill spec |
| 2 | Box ratio compliance | Count per page |
| 3 | Sharp corners compliance | All border-radius usage |
| 4 | Required pages present? | Skill spec vs actual |
| 5 | Claim verification links | Per page |
| 6 | Banned words + AI fingerprints | All copy |
| 7 | Responsive breakpoints | CSS + mobile behavior |
| 8 | Two frameworks — which wins? | Custom CSS vs Tabler |
| 9 | Dead links | All href targets verified |
| 10 | Data accuracy | All numbers vs Devsheet |

### Token Constants (For Data Accuracy Check)
```
Supply: 1,000,000 $IMOBX (fixed)
LP Locked: 75% (750,000 tokens)
Team Allocation: 0%
Trade Fees: $10 buy / $15 sell (FLAT, not %)
Fee Split: 45% operations / 35% LP / 20% hardstake
Hardstake Lock: 14 days (single lock, no tiers)
Construction: $27,777/unit (SINAPI-verified)
Market Value: $45,000/unit
Rent: R$1,250/month (~$250)
After-tax Rent: $208.25/month (15% tax + 2% platform)
Rent-to-Own: 180 months to ownership
Distribution: 98% to holders / 2% management
Euler Cost: $109/year (vs $140,400 traditional)
```

---

## SECTION D: Scoring Template

Score each page:

| Page | Dark Mode | Box Ratio | Sharp Corners | Transparency | Voice | Responsive | Data Accuracy | Total /100 |
|------|-----------|-----------|---------------|-------------|-------|------------|---------------|------------|
| index.html | /15 | /15 | /10 | /15 | /15 | /15 | /15 | /100 |
| index-bootstrap.html | /15 | /15 | /10 | /15 | /15 | /15 | /15 | /100 |
| buy.html | /15 | /15 | /10 | /15 | /15 | /15 | /15 | /100 |
| tokenomics.html | /15 | /15 | /10 | /15 | /15 | /15 | /15 | /100 |
| properties.html | /15 | /15 | /10 | /15 | /15 | /15 | /15 | /100 |
| rent-to-own.html | /15 | /15 | /10 | /15 | /15 | /15 | /15 | /100 |
| dao-demo.html | /15 | /15 | /10 | /15 | /15 | /15 | /15 | /100 |

**Overall design coherence:** /100 (how well does the site feel as one product?)

---

## How to Run This Audit

1. Clone: `git clone https://github.com/Siah-kin/imobx-website.git`
2. Open each HTML file in browser (or read the source)
3. Compare against Section A rules
4. Fill in Section D scoring template
5. Write specific fix recommendations with CSS/HTML snippets

**For Gemini/ChatGPT:** You can paste the HTML source of each page directly into context. All pages are in the repo root. CSS is at `assets/css/styles.css`.
