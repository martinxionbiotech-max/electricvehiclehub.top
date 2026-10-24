---
title: "Five-Market Landed-Cost Basket: Where to Import a Chinese EV in 2026"
description: "Independent calculation: rank Germany, UAE, Thailand, Brazil, and Australia by the landed cost of a 10-model Tier-1 export basket. Thailand is cheapest (+28.8% average), Germany dearest (+88.9%). A market-selection guide built on real tariff structure, not anecdote."
image: "/logo.svg"
author: "Wei Wang"
publishedDate: "2026-10-23"
draft: false
tags: [market-selection, landed-cost, ev-import, tariff, germany, uae, thailand, brazil, australia]
---

## TL;DR

If you can only enter one market, which do you pick? We answered it with a **basket test**: take ten Tier-1 export models — MG 4, BYD Dolphin/Atto 3/Seal, XPeng G6, Onvo L60, Xiaomi SU7/YU7, Zeekr 7X/001 — and land all ten in each of five markets. Sum the totals and average the premiums.

The ranking is unambiguous:

| Rank | Market | Basket total (10 cars) | Average premium |
|------|--------|------------------------|-----------------|
| 1 (cheapest) | **Thailand** | $319,371 | **+28.8%** |
| 2 | **UAE** | $325,660 | **+31.1%** |
| 3 | **Australia** | $339,022 | **+37.5%** |
| 4 | **Brazil** | $468,504 | **+88.8%** |
| 5 (dearest) | **Germany** | $466,362 | **+88.9%** |

Thailand and the UAE cluster around +29–31%; Australia sits mid at +37.5%; Brazil and Germany are effectively tied at ~+89%. The gap between the cheapest and dearest market is **~60 percentage points** — larger than any duty-tier difference between two individual cars.

## Key statistics

- **Basket:** 10 Tier-1 export BEVs, $9,690–$38,000 ex-factory, all `quality_tier: "A"` (full selection rationale in the [selection doc](/docs/p3-vehicle-market-selection/))
- **Thailand:** $319,371 total, +28.8% avg — cheapest, driven by 0% ACFTA duty + 7% VAT
- **Germany:** $466,362 total, +88.9% avg — dearest, driven by 10% duty + brand CVD (17–35.3%) + 19% VAT
- **The structural driver:** Germany's extra cost is almost entirely the **countervailing duty + higher VAT**, both absent in Thailand/UAE/Australia
- **Brazil:** +88.8% despite no CVD — a 35% standard duty reproduces most of the EU's penalty

## The ten-model basket

| Model | Ex-factory | Tier |
|-------|-----------|------|
| [MG 4](/vehicles/mg-4/) | $9,690 | SAIC 35.3% |
| [BYD Dolphin](/vehicles/byd-dolphin/) | $14,020 | BYD 17% |
| [BYD Atto 3](/vehicles/byd-atto-3/) | $16,260 | BYD 17% |
| [BYD Seal](/vehicles/byd-seal/) | $24,690 | BYD 17% |
| [XPeng G6](/vehicles/xpeng-g6/) | $24,830 | other 20.7% |
| [Onvo L60](/vehicles/onvo-l60/) | $29,140 | other 20.7% |
| [Xiaomi SU7](/vehicles/xiaomi-su7/) | $30,320 | other 20.7% |
| [Zeekr 7X](/vehicles/zeekr-7x/) | $32,370 | Geely 18.8% |
| [Xiaomi YU7](/vehicles/xiaomi-yu7/) | $35,700 | other 20.7% |
| [Zeekr 001](/vehicles/zeekr-001/) | $38,000 | Geely 18.8% |

[Source: China EV Mart vehicle records; selection methodology in `docs/p3-vehicle-market-selection.md`]

## Full 10 × 5 matrix

| Model (base) | Germany | UAE | Thailand | Brazil | Australia |
|--------------|---------|-----|----------|--------|-----------|
| MG 4 ($9,690) | $23,762 | $15,133 | $15,018 | $21,875 | $16,509 |
| BYD Dolphin ($14,020) | $28,072 | $19,907 | $19,651 | $28,715 | $21,272 |
| BYD Atto 3 ($16,260) | $31,503 | $22,377 | $22,048 | $32,253 | $23,736 |
| BYD Seal ($24,690) | $44,413 | $31,671 | $31,068 | $45,568 | $33,009 |
| XPeng G6 ($24,830) | $45,830 | $31,825 | $31,218 | $45,789 | $33,163 |
| Onvo L60 ($29,140) | $52,640 | $36,577 | $35,830 | $52,597 | $37,904 |
| Xiaomi SU7 ($30,320) | $54,504 | $37,878 | $37,092 | $54,460 | $39,202 |
| Zeekr 7X ($32,370) | $56,938 | $40,138 | $39,286 | $57,698 | $41,457 |
| Xiaomi YU7 ($35,700) | $63,005 | $43,809 | $42,849 | $62,958 | $45,120 |
| Zeekr 001 ($38,000) | $65,694 | $46,345 | $45,310 | $66,591 | $47,650 |

[Source: China EV Mart `landed_cost_markets`; market rates from `tariffs.json`]

## Why the ranking looks this way

The five markets differ in three levers — standard duty, VAT/GST, and countervailing duty — and the ranking is a pure function of which levers each market pulls.

| Market | Standard duty | VAT/GST | Countervailing duty | Net effect |
|--------|--------------|---------|---------------------|------------|
| Thailand | 0% (ACFTA) | 7% | none | cheapest |
| UAE | 5% | 5% | none | second |
| Australia | 0% | 10% | none | third (10% GST is the whole premium) |
| Brazil | 35% | 17% | none | dearest-by-duty, no CVD |
| Germany | 10% | 19% | 17–35.3% | dearest-by-CVD |

[Source: `tariffs.json` markets; Thailand 0% under ASEAN–China FTA, Brazil 35% BEV II from Jul 2026, Germany CVD per Regulation (EU) 2024/2754]

**Two structural lessons:**

1. **VAT/GST is the quiet cost.** Australia's 10% GST — with zero duty and zero CVD — still produces a +37.5% average premium, more than UAE's +31.1% despite UAE's 5% duty. A high consumption tax alone is enough to move a market down the ranking.
2. **A 35% duty ≈ a CVD stack.** Brazil's 35% standard duty, with no CVD, lands a basket at +88.8% — statistically indistinguishable from Germany's +88.9%. The EU's producer-specific CVD is the *incremental* cost on top of its 10% duty + 19% VAT, but a blunt high duty gets you to the same place.

## Market selection guide

**Choose Thailand** if you want the cheapest entry and can handle RHD logistics and a smaller BEV penetration base. 0% ACFTA duty + 7% VAT gives the lowest landed cost of the five.

**Choose UAE** for the second-cheapest entry with LHD convenience and a Gulf distribution hub. 5% duty + 5% VAT, no CVD.

**Choose Australia** for a zero-duty, RHD market with higher consumer spending power — but price in the 10% GST and ADR/RHD compliance.

**Choose Brazil** only with a strong local-assembly or CKD strategy; the 35% duty plus 17% VAT erases most of the China price advantage for CBU imports.

**Choose Germany** for volume and premium-brand positioning, not for margin — it is the most expensive market to land into, driven by the producer-specific CVD on top of duty and VAT.

## Conclusion

A ten-model basket test ranks the five markets **Thailand (+28.8%) < UAE (+31.1%) < Australia (+37.5%) < Brazil (+88.8%) ≈ Germany (+88.9%)**. The ~60-point spread between cheapest and dearest is driven by tariff structure, and it dominates any single-car or single-brand choice. Pick your market first, then your model — the market is the bigger variable.

## Sources

1. China EV Mart `landed_cost_markets` — 10-model × 5-market records — accessed 2026-10-23
2. China EV Mart `tariffs.json` — market duty/VAT/registration and `brand_cvd` — data date 2026-09-15
3. China EV Mart [Market Comparison](/markets/) — full 30-market tariff table
4. China EV Mart [Landed Cost Methodology](/landed-cost-methodology/)

---

*For reference only — B2B import estimate, not a retail quote. Rates change; verify with a customs broker before committing funds. Selection methodology: `docs/p3-vehicle-market-selection.md`.*
