# Gemini Design Brief: IMOBX Buy→Stake→Dual Yield Widget

You are designing a production-ready Bootstrap 5.3 page for the IMOBX website — a real-world asset (RWA) tokenization project. Your job is to merge two existing pages (a purchase guide and a staking demo) into one unified Buy→Stake→Dual Yield experience.

**Use your own design intelligence.** The brand constraints below are hard rules, but layout, component choices, animations, spacing, and visual hierarchy are yours to decide. Make it look like a real DeFi product page, not a template.

---

## 1. WHAT YOU'RE BUILDING

A single `buy-stake.html` page with this user journey:

```
[Connect Wallet] → [Buy IMOBX on Ethervista] → [Stake for 14 Days] → [See Both Yields]
```

### Required Sections (in order):

1. **Hero** — "Buy IMOBX. Stake. Earn Dual Yield." with Connect Wallet CTA
2. **Buy Widget** — Swap ETH → IMOBX via Ethervista (link out or embedded iframe). Show flat fee: $10 per buy
3. **Stake Widget** — After purchase, prompt to hardstake. 14-day lock. Show estimated yield
4. **Dual Yield Dashboard** — The key innovation. Show BOTH yields side-by-side:
   - Yield A: Trade fees (20% of $10/$15 per tx → hardstakers)
   - Yield B: Rental income ($250/month per unit → 98% to holders)
5. **Fee Breakdown** — Where the $10 goes (45% ops, 35% LP, 20% hardstakers)
6. **Risk Disclosure** — Honest risks table (liquidity, regulatory, construction, market)
7. **CTA Footer** — Links to tokenomics, properties, research

### Interactive Elements:
- Wallet connect button (MetaMask via `window.ethereum`)
- Stake amount input with live yield calculator
- Toggle between "Your Yield" (connected wallet) and "Example Yield" (demo numbers)
- All contract calls are **placeholder functions** with clear `// TODO: wire to contract` comments

---

## 2. BRAND CONSTRAINTS (HARD RULES)

### Colors — Dark Mode
```css
:root {
    --imobx-bg: #0A0A0A;           /* Background — THE brand */
    --imobx-surface: #1F1F23;       /* Cards, elevated surfaces */
    --imobx-border: #27272A;        /* Borders */
    --imobx-text: #FFFFFF;          /* Primary text */
    --imobx-muted: #A1A1AA;         /* Secondary text */
    --imobx-turquoise: #4A90A4;     /* Technical/primary actions */
    --imobx-orange: #FF8C00;        /* Framework/strategic — RARE */
    --imobx-green: #10B981;         /* Success, verification */
    --imobx-red: #DC2626;           /* Errors ONLY */
}
```

### Typography
- Font: `Inter` (Google Fonts), fallback: `-apple-system, BlinkMacSystemFont, sans-serif`
- Base size: 16px, line-height: 1.6

### Sharp Corners (MANDATORY)
```css
* { border-radius: 0 !important; }
.avatar { border-radius: 50% !important; } /* Only exception */
```
No rounded corners on cards, buttons, inputs, badges — nothing. This IS the brand.

### Button Styles
```css
/* Primary: turquoise */
.btn-primary { background: #4A90A4; color: white; border: none; font-weight: 600; }
/* Secondary: orange (rare, strategic CTAs only) */
.btn-secondary { background: #FF8C00; color: white; border: none; }
/* Outline: turquoise border */
.btn-outline-primary { border: 2px solid #4A90A4; color: #4A90A4; background: transparent; }
```

### 3-Box Content System
The site uses three types of info boxes, each with a colored left border and label:

| Box Type | Border Color | Label | Usage |
|----------|-------------|-------|-------|
| Technical | #4A90A4 (turquoise) | "HOW IT WORKS" | Mechanics, contract flows, step-by-step (40-50%) |
| Framework | #FF8C00 (orange) | "KEY FRAMEWORK" | Unique features, dual-yield architecture (30-40%) |
| Strategic | #FF8C00 (orange) | "STRATEGIC ADVANTAGE" | External factors, competitive moat (10-20% MAX) |
| Transparency | #10B981 (green) | "VERIFY ON-CHAIN" | Links to Etherscan, contract proofs |

```css
/* Example: Technical box on dark background */
.box-technical {
    background: rgba(74, 144, 164, 0.08);
    border-left: 4px solid #4A90A4;
    padding: 24px 28px;
}
.box-technical .box-label {
    display: inline-block;
    background: #4A90A4;
    color: white;
    padding: 4px 12px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    margin-bottom: 12px;
}
```

### Banned
- No gradients (no `linear-gradient` backgrounds)
- No purple (no #667eea, no #764ba2 — that was a bug)
- No border-radius
- No "leverage", "synergies", "innovative", "revolutionary", "disrupt"
- No percentage fees language — always "flat fee: $X per transaction"

---

## 3. FRAMEWORK

**Tabler (Bootstrap 5.3 fork):**
```html
<link href="https://cdn.jsdelivr.net/npm/@tabler/core@latest/dist/css/tabler.min.css" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/dist/tabler-icons.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/@tabler/core@latest/dist/js/tabler.min.js"></script>
```

Use Tabler's component library (cards, badges, tables, progress bars, form controls) but override ALL colors and border-radius with IMOBX brand CSS above.

**Tabler dark mode:** Tabler supports `data-bs-theme="dark"` on `<html>`. Use this as the base, then override with IMOBX colors.

---

## 4. TOKEN CONSTANTS (USE THESE EXACTLY)

```
Token: $IMOBX
Total Supply: 1,000,000 (fixed forever)
Decimals: 18

TOKEN DISTRIBUTION (from Devsheet — use these exact numbers):
  75% LP (hardlocked forever)
   5% Strategic (5×1%, 6-month hardlock)
   5% Multisig (5×1%, 2-year hardlock)
   5% Operations (hardstake)
   5% Community (hardstake)
   3% Broker Incentives (hardstake)
   2% Legal/Compliance
   0% Team Allocation

Buy Fee: $10 flat per transaction
Sell Fee: $15 flat per transaction
Average Fee: $12.50

Fee Distribution:
  45% → Operations (hired staff) = $5.63 per avg trade
  35% → LP Holder Rewards = $4.38 per avg trade
  20% → Hardstaker Rewards = $2.50 per avg trade

Hardstake Lock: 14 days (single lock, no tiers)
Auto-burn: Protocol buys + burns via Euler distribution (deflationary)

EULER ADVANTAGE (critical selling point):
  Traditional reward distribution: $140,400/year @ 1,000 holders
  Euler algorithm: $109/year @ ANY number of holders
  = 99.9% cost savings. Battle-tested: VISTA distributed $1M+ ETH over 400+ days.

RENTAL INCOME (after-tax math from Devsheet):
  Gross rent: $250/month per unit (R$1,250)
  Brazilian tax (15%): -$37.50
  After-tax: $212.50
  Platform fee (2%): -$4.25
  To holders (98%): $208.25/unit/month
  At 100 units: $20,825/month → $249,900/year → $0.25/token/year

TRADE VOLUME SCENARIOS:
  Deep bear: 10 trades/day → $3,750/mo total fees (still profitable)
  Long-term avg: 25 trades/day → $9,375/mo (sustainable ops)
  Bull launch: 100+ trades/day → $37,500+/mo (rapid scaling)

CONSTRUCTION COST BREAKDOWN (SINAPI-verified):
  Land (emerging neighborhoods): $5,550
  House (45m², SINAPI minus 15% BDI): $18,600
  Solar (wholesale B2B, 20-50 units): $1,500
  Shared amenities (÷20 units): $1,500
  Legal/projects (in-house): $627
  TOTAL: $27,777 per unit
  Market value: ~$45,000 per unit
  Instant equity: $17,223 (62%)

FLOOR PRICE FORMULA:
  floor = (units × $45,000) / 1,000,000 tokens
  At 100 units = $4.50 floor
  At 200 units = $9.00 floor
  At 1,000 units = $45.00 floor

YIELD CONCENTRATION (self-correcting mechanism):
  If holders dump, fewer holders share the same rental income.
  100% holders @ 100 units = 6.8% APY
  50% dump = 13.7% APY for remaining holders
  75% dump = 27.4% APY — creates buy pressure back toward floor

EXIT CAPITAL RECYCLING:
  Profit per tenant exit: $45,000 rent paid − $27,777 build = $17,223 (62%)
  New units funded: $17,223 / $27,777 = 0.62 additional units
  Every completed tenant → 1.62 replacement units. Portfolio grows faster than it shrinks.

FOUNDER COMPENSATION:
  Hardstake yield only. No salaries, no sell pressure.
  "We win when you win."

DEX: Ethervista (https://ethervista.app)
Distribution: Euler bonding curve (fair launch, no presale)
```

---

## 5. EXISTING CODE REFERENCE

### dao-demo.html (What Works — Steal These Patterns)

**Wallet connect flow:**
```javascript
function connectWallet() {
    if (typeof window.ethereum !== 'undefined') {
        window.ethereum.request({ method: 'eth_requestAccounts' })
            .then(accounts => {
                walletAddress = accounts[0];
                walletConnected = true;
                updateWalletStatus();
            })
            .catch(err => alert('Wallet connection rejected'));
    } else {
        alert('MetaMask not detected. Please install MetaMask.');
    }
}
```

**Stake widget pattern (adapt — change ETH to IMOBX, fix lock to 14 days):**
```html
<div class="card">
    <div class="card-header"><h3>Stake IMOBX</h3></div>
    <div class="card-body">
        <div class="mb-3">
            <label class="form-label">Amount to Stake</label>
            <input type="number" class="form-control" placeholder="0.00" min="0">
        </div>
        <div class="mb-3">
            <label class="form-label">Lock Duration: 14 days</label>
            <!-- Fixed 14 days, NOT a slider -->
        </div>
        <!-- Yield preview -->
        <div class="reward-preview">
            <div>Trade Fee Yield: <span id="trade-yield">—</span></div>
            <div>Rental Yield: <span id="rental-yield">—</span></div>
            <div>Combined APY: <span id="combined-apy">—</span></div>
        </div>
        <button class="btn btn-primary w-100" onclick="stakeIMOBX()">
            Stake for 14 Days
        </button>
    </div>
</div>
```

### buy.html (Content to Preserve)

**Fee comparison table:**
| Trade Size | Uniswap (0.3%) | Ethervista (Flat) |
|-----------|----------------|-------------------|
| $1,000    | $3             | $10               |
| $10,000   | $30            | $10               |
| $100,000  | $300           | $10               |

**Dual yield options:**
| Option | Yield Source | Lock | Risk |
|--------|-------------|------|------|
| Hold | Rental income ($250/mo per unit) | None | Low |
| LP Provider | 35% trade fees + rental | None (IL risk) | Medium |
| Hardstaker | 20% trade fees (higher APY) | 14 days | Medium |

**Risk disclosure table:**
| Risk | Mitigation |
|------|-----------|
| Liquidity | 75% LP locked on-chain |
| Regulatory | Jurisdiction-agnostic primitive |
| Construction | SINAPI variance tracking (>10% = red flag) |
| Market | Dual yield (fees + rental) |

**Competitive benchmark (from Devsheet — include on page):**
| Platform | Yield Currency | Circular? | Structure | Network Effect |
|----------|---------------|-----------|-----------|----------------|
| EstateX | ESX (own token) | Yes (doom loop, -87%) | Utility + NFT | Negative |
| RealT | USDC | No | Per-property LLC | Limited |
| Lofty | USDC | No | Per-property | Limited |
| IMOBX | ETH | No | Portfolio (SA) | Compounding |

**EstateX doom loop warning (use as "What We Avoided" box):**
Their model: Collect rent → Buy own token → Distribute → Holders sell → Price drops → Yield worth less → Death spiral.
IMOBX model: Collect rent in BRL → Convert to ETH → Distribute ETH. Selling $IMOBX doesn't affect the yield. Rental income flows regardless of token price.

---

## 6. DESIGN CRITIQUE OF EXISTING PAGES (Context for Your Decisions)

**dao-demo.html problems you must fix:**
- Purple gradients (#667eea → #764ba2) — use turquoise/orange on dark instead
- Staking ETH instead of IMOBX — wrong token
- Lock duration slider 14-90 days — should be fixed 14 days only
- APY formula is fake (12% base + 8% bonus) — use placeholder "—" until connected
- Only shows trade fee yield, not rental income — must show both
- Treasury data hardcoded — use "Connect wallet to view" placeholder

**buy.html problems you must fix:**
- Email widget is a dead end — replace with wallet connect + Ethervista link
- Light background (#FFFFFF) — should be dark (#0A0A0A)
- Custom CSS, not Bootstrap — rebuild with Tabler components
- No interactive elements — needs live yield calculator

---

## 7. RESPONSIVE REQUIREMENTS

```
Desktop (>1200px): 2-column layout — Buy widget left, Stake widget right
Tablet (768-1200px): Stack to single column, full width cards
Mobile (<768px): Full width, hamburger nav, touch-friendly inputs (min 44px tap targets)
```

### Navigation Bar
```html
<header class="navbar navbar-expand-md sticky-top" style="background: #0A0A0A; border-bottom: 1px solid #27272A;">
    <div class="container-xl">
        <a class="navbar-brand" href="/imobx-website/">
            <img src="/imobx-website/assets/logo.png" height="32" alt="IMOBX">
        </a>
        <!-- Hamburger for mobile -->
        <button class="navbar-toggler" data-bs-toggle="collapse" data-bs-target="#navbar-menu">
            <span class="navbar-toggler-icon"></span>
        </button>
        <!-- Nav links -->
        <div class="collapse navbar-collapse" id="navbar-menu">
            <ul class="navbar-nav">
                <li class="nav-item"><a class="nav-link" href="/imobx-website/">Home</a></li>
                <li class="nav-item"><a class="nav-link" href="/imobx-website/tokenomics.html">Tokenomics</a></li>
                <li class="nav-item"><a class="nav-link" href="/imobx-website/properties.html">Properties</a></li>
                <li class="nav-item"><a class="nav-link" href="/imobx-website/rent-to-own.html">Rent-to-Own</a></li>
                <li class="nav-item"><a class="nav-link active" href="/imobx-website/buy.html">Buy & Stake</a></li>
                <li class="nav-item"><a class="nav-link" href="/imobx-website/research/">Research</a></li>
            </ul>
        </div>
        <!-- Wallet connect (always visible) -->
        <div class="navbar-nav flex-row order-md-last">
            <button class="btn btn-primary" onclick="connectWallet()">
                <i class="ti ti-wallet"></i> Connect Wallet
            </button>
        </div>
    </div>
</header>
```

---

## 8. YOUR DELIVERABLE

One complete `buy-stake.html` file that:
1. Is self-contained (inline `<style>` for IMOBX overrides + Tabler CDN links)
2. Works when opened locally in a browser
3. Has working wallet connect (MetaMask)
4. Has a live yield calculator (JavaScript, placeholder formulas clearly marked)
5. Shows dual yield (trade fees + rental income) in one unified view
6. Uses dark mode (#0A0A0A background)
7. Has sharp corners everywhere (no border-radius)
8. Uses the 3-box content system for info sections
9. Is mobile-responsive (test at 375px width)
10. All placeholder contract calls marked with `// TODO: wire to Ethervista contract`

**Apply your own design intelligence for:**
- Visual hierarchy and spacing
- Card layout and component composition
- Micro-interactions (hover states, transitions)
- How to make the dual yield dashboard visually compelling
- Whether to use tabs, stepper, or scroll for the Buy→Stake flow
- Any Tabler components that would elevate the UX

---

## 9. VOICE & COPY GUIDELINES

- Write like a person, not a marketing department
- Use contractions. Vary sentence length. Short ones punch.
- No buzzwords: revolutionary, disrupt, paradigm, leverage, utilize, seamlessly
- Flat fees, not percentages: "You pay $10 per buy, regardless of trade size"
- Be honest about risks: "This is experimental. Only invest what you can afford to lose."
- Show the math: "$27,777 construction cost vs $45,000 market value = 62% ROI"

---

## 10. FINAL CONTEXT

IMOBX is a pre-launch project. The token doesn't exist on-chain yet. The website is the public accountability layer — every claim should link to where verification will live (Etherscan, SINAPI, IPFS) even if those links are placeholder `#` for now. Mark unverifiable claims with "Coming soon" badges.

The co-founders:
- **Rafael** — Civic engineer in Rio de Janeiro, owns construction company
- **Freedom John** — Tech, tokenomics, AI infrastructure

Governance: 2 co-founders + 3 strategic advisors → 2/3 multisig treasury.

**Make this page look like it belongs on a serious DeFi protocol, not a student project.**
