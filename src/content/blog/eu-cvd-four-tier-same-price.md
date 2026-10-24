---
title: "Same Car, Four Duty Tiers: What the EU Countervailing Duty Actually Costs"
description: "Independent isolation: hold a single $20,000 ex-factory price constant and vary only the EU countervailing-duty tier — 17%, 18.8%, 20.7%, 35.3% — to quantify what the producer-specific rate costs an importer in Germany. Plus Brazil (35% duty, no CVD) as the control."
image: "/logo.svg"
author: "Wei Wang"
publishedDate: "2026-10-23"
draft: false
tags: [countervailing-duty, eu-tariff, landed-cost, ev-import, germany, brazil]
---

## TL;DR

Most countervailing-duty coverage compares *cars* — a BYD against an MG — which mixes up base price and duty rate and muddies the conclusion. Here we isolate the duty by holding **one variable constant: a $20,000 ex-factory BEV**. Same car, four producer tiers, one market (Germany).

The result: the producer-specific CVD is worth between **$5,538 and $10,329 in absolute landed cost** on that $20,000 car, relative to a no-CVD baseline. The gap between the cheapest tier (BYD 17%) and the dearest (SAIC 35.3%) is **$4,791** — nearly a quarter of the car's base price. And a no-CVD market with a high standard duty (Brazil, 35%) can cost *less* than Germany for three of the four producer tiers.

## Key statistics

- **Isolation method:** $20,000 base held constant; only `countervailing_rate` varies
- **No-CVD Germany baseline:** $32,342 landed (+61.7%)
- **BYD 17%:** $37,231 (+86.2%) — the cheapest producer tier
- **Geely 18.8%:** $37,702 (+88.5%)
- **Other cooperating 20.7%:** $38,199 (+91.0%)
- **SAIC 35.3%:** $42,022 (+110.1%) — the dearest tier, a $4,791 gap over BYD
- **Control — Brazil 35% duty, no CVD:** $38,160 (+90.8%), cheaper than Germany for the SAIC tier

## The four EU producer tiers

The EU countervailing duty (Regulation (EU) 2024/2754) is assessed **per producer**, not per car or per destination. The four tiers in our data:

| Producer group | CVD rate | Example brands |
|----------------|----------|----------------|
| BYD group | 17.0% | BYD, Denza, Yangwang, Fangchengbao |
| Geely group | 18.8% | Geely, Zeekr, Lynk & Co, Galaxy, Livan, Geometry |
| Other cooperating | 20.7% | Xiaomi, XPeng, NIO/Onvo, Leapmotor, most others |
| SAIC group | 35.3% | MG, Maxus, Roewe, Wuling, Baojun, IM |

[Source: EU Implementing Regulation (EU) 2024/2754; `tariffs.json` `brand_cvd`, verification status `consistent_with_definitive_rates`, last verified 2026-10-23]

## The isolation calculation

Germany's structure: 10% standard duty, then CVD on top, then 19% VAT on the duty-inclusive value, plus $6,600 fixed (freight $2,000 + clearance $350 + certification $3,250 + inland $500 + registration $500).

```
duty  = 20000 × 0.10 = 2000
cvd   = (20000 + 2000) × cvd_rate
vat   = (20000 + 2000 + cvd) × 0.19
total = 20000 + duty + cvd + vat + 6600
```

| CVD tier | CVD amount | VAT | Total landed | Premium vs base | Premium vs no-CVD |
|----------|-----------|-----|-------------|-----------------|-------------------|
| No CVD (baseline) | $0 | $4,342 | $32,342 | +61.7% | — |
| BYD 17% | $3,740 | $5,053 | $37,231 | +86.2% | +$4,889 |
| Geely 18.8% | $4,136 | $5,128 | $37,702 | +88.5% | +$5,360 |
| Other 20.7% | $4,554 | $5,207 | $38,199 | +91.0% | +$5,857 |
| SAIC 35.3% | $7,766 | $5,818 | $42,022 | +110.1% | +$9,680 |

[Source: China EV Mart landed-cost formula; all values computed from the $20,000 constant base]

**Reading the table:** the CVD is *not* simply "rate × base". It's charged on the duty-inclusive value, and then VAT is charged on top of the CVD. So a 17% rate actually adds $4,889 to the landed price (24.4% of base), and a 35.3% rate adds $9,680 (48.4% of base) once VAT compounding is included. The headline rate understates the real cost by roughly 40%.

## Brazil as the control: duty structure vs CVD

Brazil has **no countervailing duty** but a **35% standard import duty**. Holding the same $20,000 base:

| Market | Structure | Landed | Premium |
|--------|-----------|--------|---------|
| Germany, BYD tier | 10% duty + 17% CVD + 19% VAT | $37,231 | +86.2% |
| Germany, other tier | 10% duty + 20.7% CVD + 19% VAT | $38,199 | +91.0% |
| **Brazil, no CVD** | 35% duty + 17% VAT | **$38,160** | **+90.8%** |
| Germany, SAIC tier | 10% duty + 35.3% CVD + 19% VAT | $42,022 | +110.1% |

[Source: computed; Brazil duty/VAT from `tariffs.json` markets.brazil, data date 2026-09-15]

The insight: **for the SAIC tier (MG/Wuling), importing into Germany is more expensive than importing into Brazil** — even though Brazil's standard duty is 35% versus Germany's 10%. The 35.3% CVD plus 19% VAT compounding overwhelms the 25-point standard-duty advantage. For BYD and Geely tiers, Germany is slightly cheaper than Brazil, but the margin is thin ($929 and $458 respectively).

## What this means for importers

1. **The producer tier is a pricing input, not a footnote.** A dealer who can source a $20,000 BEV from a BYD-group producer saves $4,791 in Germany versus the same-price SAIC-group car — before any negotiation.
2. **Compounding means the true CVD cost is ~40% higher than the headline rate.** Budget for it; don't under-price a proposal off the raw percentage.
3. **A no-CVD high-duty market can beat a low-duty CVD market.** Brazil beats Germany for three of the four tiers; only the SAIC 35.3% tier flips it.
4. **The cheapest producer tier matters most in the EU.** In Thailand, UAE, or Australia there is no CVD, so the producer tier is irrelevant — only base price and standard duty/VAT matter. See the [market comparison](/markets/).

## Conclusion

Holding base price constant isolates the producer-specific countervailing duty as a **$4,889–$9,680 absolute landed-cost swing** on a $20,000 BEV in Germany, with a $4,791 gap between the cheapest and dearest producer tiers. The CVD compounds with duty and VAT, so the real cost is materially higher than the headline rate, and in the worst tier it can push Germany above a 35%-duty no-CVD market like Brazil.

## Sources

1. EU Implementing Regulation (EU) 2024/2754 — producer-specific countervailing duty rates — https://eur-lex.europa.eu/eli/reg_impl/2024/2754/oj
2. China EV Mart `tariffs.json` — `brand_cvd` and `markets` (Germany, Brazil) — data date 2026-09-15
3. China EV Mart [Landed Cost Methodology](/landed-cost-methodology/) — formula

---

*For reference only — B2B import estimate, not a retail quote. Duty rates are effective 31 October 2024 and may be revised; confirm with a customs broker. See the full brand-rate table in the [CVD master table](/blog/china-ev-brand-cvd-master-table/).*
