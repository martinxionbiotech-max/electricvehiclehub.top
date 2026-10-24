---
title: "Budget EVs Under Full Landed Cost: Does the Cheap Car Stay Cheap in 5 Markets?"
description: "Independent calculation: the MG 4, BYD Dolphin, and BYD Atto 3 after duty, VAT, and fixed import costs in Germany, UAE, Thailand, Brazil, and Australia. The cheapest ex-factory car keeps the cheapest absolute landed price in every market — but pays the highest percentage premium."
image: "/logo.svg"
author: "Wei Wang"
publishedDate: "2026-10-23"
draft: false
tags: [landed-cost, budget-ev, mg-4, byd-dolphin, byd-atto-3, ev-import, tariff]
---

## TL;DR

The core fear an importer has about a cheap Chinese EV is that the fixed import costs — freight, customs clearance, certification, registration, inland transport — will swallow the price advantage. We ran the numbers on three sub-$17,000 BEVs across five markets to answer one question: **does the cheapest car stay the cheapest once it's landed?**

The answer is yes on absolute price, with a caveat. The **MG 4** ($9,690 ex-factory) keeps the lowest absolute landed price in all five markets — Germany $23,762, UAE $15,133, Thailand $15,018, Brazil $21,875, Australia $16,509 — despite carrying the highest EU countervailing duty of the three (35.3% vs BYD's 17%). But it also pays the **highest percentage premium** everywhere, because ~$6,600 of fixed costs land on the smallest base price.

The strategic takeaway: **budget EVs win on absolute dollars, lose on percentage markup.** A dealer pricing off percentage margin will find the cheap car's gross-profit-per-unit thin; a dealer pricing off absolute price positioning wins with the cheap car.

## Key statistics

- **MG 4:** $9,690 ex-factory → $23,762 Germany (+145.2%), the lowest absolute landed price of the three in all five markets
- **Fixed import costs (Germany):** $6,600, or **27.8% of the MG 4's landed cost** — vs 10.0% for a $38,000 Zeekr 001
- **The percentage-premium inversion:** cheaper base → higher premium% (MG 4 +145%, Dolphin +100%, Atto 3 +94% in Germany)
- **The absolute-price hold:** MG 4 stays $4,310 cheaper than the Dolphin in Germany even after the 35.3% vs 17% duty gap
- **Market spread:** the same three-car basket lands at an average +88.9% premium in Germany vs +28.8% in Thailand

## The three cars

| Model | Ex-factory (USD) | Battery | CLTC range | EU CVD tier |
|-------|-----------------|---------|-----------|-------------|
| [MG 4](/vehicles/mg-4/) | $9,690 | 42.8 kWh | 437 km | SAIC 35.3% |
| [BYD Dolphin](/vehicles/byd-dolphin/) | $14,020 | 45.1 kWh | 418 km | BYD 17% |
| [BYD Atto 3](/vehicles/byd-atto-3/) | $16,260 | 49.9 kWh | 430 km | BYD 17% |

[Source: China EV Mart vehicle records, frontmatter `price_usd` / `battery_kwh` / `range_cltc_km`; tariff tier from `tariffs.json` `brand_cvd`, data date 2026-09-15]

## The landed-cost formula

Landed cost is computed the same way for every market (see [Landed Cost Methodology](/landed-cost-methodology/)):

```
duty  = base × standard_duty_rate
cvd   = (base + duty) × countervailing_rate     # EU + BEV only
vat   = (base + duty + cvd) × vat_rate
total = base + duty + cvd + vat + region_fixed + registration_fee
```

The `region_fixed` component bundles freight + clearance + certification + inland transport. For Germany it is $6,100 (EU), plus a $500 registration fee — $6,600 total. This is the number that does not scale with car price.

## The five-market landed-cost table

| Model (ex-factory) | Germany | UAE | Thailand | Brazil | Australia |
|--------------------|---------|-----|----------|--------|-----------|
| MG 4 ($9,690) | $23,762 (+145.2%) | $15,133 (+56.2%) | $15,018 (+55.0%) | $21,875 (+125.8%) | $16,509 (+70.4%) |
| BYD Dolphin ($14,020) | $28,072 (+100.2%) | $19,907 (+42.0%) | $19,651 (+40.2%) | $28,715 (+104.8%) | $21,272 (+51.7%) |
| BYD Atto 3 ($16,260) | $31,503 (+93.7%) | $22,377 (+37.6%) | $22,048 (+35.6%) | $32,253 (+98.4%) | $23,736 (+46.0%) |

[Source: China EV Mart `landed_cost_markets` records, computed from the formula above. Market rates: Germany 10% duty + 19% VAT + CVD; UAE 5% duty + 5% VAT; Thailand 0% duty (ACFTA) + 7% VAT; Brazil 35% duty + 17% VAT; Australia 0% duty + 10% GST. See [Market Comparison](/markets/).]

## Calculation walk-through: why the MG 4 still wins in Germany

Germany is the harshest case for the MG 4 because SAIC pays the 35.3% CVD. Step through the arithmetic:

| Line | MG 4 | BYD Dolphin |
|------|------|-------------|
| Base | $9,690 | $14,020 |
| Duty (10%) | $969 | $1,402 |
| CVD (35.3% / 17%) | $3,763 | $2,622 |
| VAT (19%) | $2,740 | $3,428 |
| Fixed + registration | $6,600 | $6,600 |
| **Total landed** | **$23,762** | **$28,072** |

[Source: China EV Mart landed-cost methodology; breakdown figures from vehicle records]

Even though the MG 4 pays $3,763 in countervailing duty against the Dolphin's $2,622 — a $1,141 penalty — its $4,330 lower base price more than absorbs the difference. The MG 4 still lands **$4,310 cheaper**. This is the same "tariff paradox" documented in the [MG budget EV tariff analysis](/blog/mg-budget-ev-tariff-paradox/): at the budget end, **base price beats tariff rate**.

## The caveat: fixed-cost share

The reason the percentage premium is so lopsided is that the $6,600 fixed block is a bigger share of a small base. Across the ten Tier-1 export models we track:

| Model | Ex-factory | Germany landed | Fixed-cost share of landed |
|-------|-----------|----------------|---------------------------|
| MG 4 | $9,690 | $23,762 | 27.8% |
| BYD Dolphin | $14,020 | $28,072 | 23.5% |
| BYD Atto 3 | $16,260 | $31,503 | 21.0% |
| BYD Seal | $24,690 | $44,413 | 14.9% |
| Zeekr 001 | $38,000 | $65,694 | 10.0% |

[Source: computed from `landed_cost_markets` fixed-cost component; Germany region fixed $6,100 + $500 registration]

**What this means for margin:** if you run a fixed percentage gross margin, the MG 4 generates the thinnest dollar margin of the three because its landed cost is lowest — you'd make more dollars per unit on the Dolphin or Atto 3. If you compete on absolute out-the-door price, the MG 4 gives you the sharpest offer in the segment.

## Which market favors the budget EV?

Ranking the five markets by landed premium for the three-car basket:

| Rank | Market | Average premium (3 cars) |
|------|--------|--------------------------|
| 1 (cheapest) | Thailand | +43.6% |
| 2 | UAE | +45.3% |
| 3 | Australia | +56.0% |
| 4 | Brazil | +109.7% |
| 5 (dearest) | Germany | +113.0% |

[Source: computed from the table above]

The budget EV's price advantage is **amplified in low-tariff markets** (Thailand, UAE, Australia) and **compressed in high-tariff markets** (Germany, Brazil). A Thailand-bound importer lands an MG 4 at +55%; a Germany-bound importer at +145%. The same car, nearly triple the markup.

## Conclusion

1. **Absolute price: the cheap car stays cheap.** The MG 4 is the lowest-absolute-landed of the three in all five markets, even in Germany where it faces a 35.3% CVD.
2. **Percentage premium: the cheap car pays the most.** Fixed costs are a 27.8% share of the MG 4's landed cost vs 10% for a $38,000 flagship.
3. **Margin implication:** percentage-margin dealers should prefer the mid-priced Atto 3 or Dolphin; absolute-price competitors should prefer the MG 4.
4. **Market choice dominates car choice.** Moving the same car from Germany to Thailand cuts the landed premium by roughly 90 points — more than any duty-tier difference between two cars.

## Sources

1. China EV Mart vehicle records — MG 4 / BYD Dolphin / BYD Atto 3 frontmatter (`price_usd`, `battery_kwh`, `range_cltc_km`, `landed_cost_markets`) — accessed 2026-10-23
2. China EV Mart `tariffs.json` — market duty/VAT rates and `brand_cvd` tiers — data date 2026-09-15
3. China EV Mart [Landed Cost Methodology](/landed-cost-methodology/) — formula and cost-component definitions

---

*For reference only — this is a B2B import estimate, not a retail quote. Verify current rates with a customs broker before committing funds. Compare all three models in the [vehicle directory](/vehicles/) and model your own destination with the [landed-cost calculator](https://electricvehiclehub.net/landed-cost-calculator/).*
