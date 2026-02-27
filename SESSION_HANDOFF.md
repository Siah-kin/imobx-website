# IMOBX Website Session Handoff

**Date:** 2026-02-27
**Last commit:** a93de62 (pushed to main)

---

## What Was Done

1. **Exhaustive Narrative Rapport** — `IMOBX_NARRATIVE_RAPPORT.md` (636 lines, 14 sections)
   - Covers: Pix/Drex/tokenization thesis, Ethervista Euler, dual yield, rent-to-own, floor price dynamics, competitive landscape, BlackRock/RWA validation, Bonzi infrastructure, grant strategy, co-founder narratives
   - Sources: IMOBX Exec chat (4,154 msgs), Ethervista exec chat (529 msgs), Devsheet (8 layers), web research
   - All data points source-attributed in Appendix

2. **Page-by-page design critique** — Analyzed all 7 HTML pages + research stubs (in plan file, not committed)

3. **Gemini Design Prompt** — Was written but got reverted (commit f711933). Needs to be recreated.

---

## What's Next (Priority Order)

### 1. Recreate Gemini Design Prompt
The prompt for Gemini to produce a Bootstrap Buy→Stake→Dual Yield page was written but reverted. Plan exists at:
- Bonzi_v5: `.claude/plans/humming-honking-honey.md`

Key requirements for the prompt:
- Merge `buy.html` + `dao-demo.html` into one unified page
- Tabler/Bootstrap 5.3 framework
- 3-step wizard: Connect Wallet → Buy IMOBX → Stake for Dual Yield
- Both yields visible in one view (trade fee APY + rental income APY)
- Dark mode (#0A0A0A), sharp corners, IMOBX brand colors
- Responsive (mobile-first)

### 2. Bootstrap Migration
- Consolidate all pages from custom CSS to Tabler/Bootstrap 5.3
- Reference: `index-bootstrap.html` (partial Tabler implementation)
- Framework files: `tabler-main/` directory (untracked, local only)

### 3. Fix Dead Links
- `whitepaper.html` — referenced but doesn't exist
- `bonzi-journey.html` — referenced but doesn't exist
- All research/ sub-pages are stubs
- `research/sinapi-tracker.html` — stub
- `research/grants.html` — stub

### 4. Brand Alignment
- dao-demo.html uses purple gradients (should be turquoise/orange on dark)
- index-bootstrap.html uses border-radius: 8px (should be sharp corners)
- Design skill colors: turquoise #4A90A4, orange #FF8C00, dark #0A0A0A

---

## Key Files

| File | Repo | Purpose |
|------|------|---------|
| `IMOBX_NARRATIVE_RAPPORT.md` | imobx-website | Exhaustive narrative (this session) |
| `IMOBX_Devsheet.pdf` | Bonzi_v5 `.claude/skills/imobx-design.skill/materials/` | Canonical economics (8 layers) |
| `SKILL.md` | Bonzi_v5 `.claude/skills/imobx-design.skill/` | Design system (348 lines) |
| `imobx_exec.json` | Bonzi_v5 root | Co-founder exec chat (4,154 msgs) |
| `CLippy_v2.json` | Bonzi_v5 root | Ethervista exec chat (529 msgs) |
| `humming-honking-honey.md` | Bonzi_v5 `.claude/plans/` | Bootstrap migration plan |

---

## Token Constants (Quick Reference)

- Supply: 1,000,000 $IMOBX
- LP locked: 75% (750,000)
- Team: 0%
- Fees: $10 buy / $15 sell (FLAT, not %)
- Split: 45% ops / 35% LP / 20% hardstake
- Hardstake: 14-day lock
- Construction: $27,777/unit (SINAPI)
- Rent: $250/month ($208.25 after tax)
- Floor: (units × $45,000) / 1,000,000
