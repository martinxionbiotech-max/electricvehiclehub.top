---
title: "Australia SUV Import Guide: Atto 3 vs XPeng G6 vs Onvo L60 vs Zeekr 7X"
description: "A market-specific selection guide for Australia, built on real spec comparison (range, battery, charging, dimensions) plus zero-duty landed cost. The Atto 3 wins on price, the Zeekr 7X wins on spec-per-dollar. Full comparison and landed-cost math."
image: "/logo.svg"
author: "Wei Wang"
publishedDate: "2026-10-23"
draft: false
tags: [australia, market-selection, suv, byd-atto-3, xpeng-g6, onvo-l60, zeekr-7x, landed-cost, ev-import]
---

## TL;DR

Australia is the standout zero-duty RHD market for Chinese EVs: 0% import duty, 10% GST, no countervailing duty. That makes it the cheapest rich-country destination to land a Chinese SUV into. We compare four Tier-1 mid-size SUVs — **BYD Atto 3, XPeng G6, Onvo L60, Zeekr 7X** — on real specifications and landed cost.

The verdict: the **Atto 3 is the price leader** (lands at $23,736, +46% over base), while the **Zeekr 7X delivers the best spec-per-dollar** at the higher end (longer range and a bigger battery for a moderate premium). The XPeng G6 and Onvo L60 sit in between, each with a distinct edge — the G6 on charging speed, the L60 on range-per-price in its band.

## Key statistics

- **Australia structure:** 0% duty + 10% GST + no CVD — the cheapest rich-country entry (see the [basket ranking](/blog/five-market-landed-cost-basket/))
- **Atto 3:** $16,260 → $23,736 landed (+46.0%), the segment price floor
- **XPeng G6:** $24,830 → $33,163 (+33.6%), 800V-class fast charging
- **Onvo L60:** $29,140 → $37,904 (+30.1%), 560 km CLTC
- **Zeekr 7X:** $32,370 → $41,457 (+28.1%), 620 km CLTC, 75 kWh — best spec-per-dollar at the top
- **RHD note:** all four must be sourced in RHD or converted; ADR compliance required

## The four SUVs on specification

| Spec | [BYD Atto 3](/vehicles/byd-atto-3/) | [XPeng G6](/vehicles/xpeng-g6/) | [Onvo L60](/vehicles/onvo-l60/) | [Zeekr 7X](/vehicles/zeekr-7x/) |
|------|-------------|----------|----------|----------|
| Ex-factory | $16,260 | $24,830 | $29,140 | $32,370 |
| Battery | 49.9 kWh | 68.5 kWh | 60.0 kWh | 75.0 kWh |
| CLTC range | 430 km | 625 km | 560 km | 620 km |
| Charging interface | GB/T + adapter | CCS2-capable | GB/T + adapter | CCS2-capable |
| Australia landed | $23,736 | $33,163 | $37,904 | $41,457 |
| Landed premium | +46.0% | +33.6% | +30.1% | +28.1% |

[Source: China EV Mart vehicle records; charging interface from `charging_interface` / `charging_adapter` fields. Australia landed from `landed_cost_markets`, computed 0% duty + 10% GST + Oceania fixed costs]

## Australia's tariff structure, applied

Australia applies **zero import duty** on these BEVs, a **10% GST**, and no countervailing duty (the EU's producer-specific CVD does not apply outside the EU). The landed-cost formula for Australia is therefore the simplest of the five markets:

```
duty  = base × 0.00 = 0
cvd   = 0            (non-EU market)
vat   = base × 0.10  (GST)
total = base + vat + region_fixed(Oceania) + registration
```

The Oceania region fixed block (freight + clearance + certification + inland) plus Australia's $500 registration fee means the fixed cost is still ~$5,850 — so even a zero-duty market carries a meaningful fixed-cost floor. The Atto 3's +46% premium is almost entirely GST + fixed costs; the Zeekr 7X's +28.1% is lower because the fixed block is a smaller share of a larger base.

## Spec-per-dollar comparison

The decision hinges on what you're buying: the cheapest entry, or the most capability per dollar. Two derived metrics make it concrete.

**Price per kWh of battery (landed):**

| Model | Landed | Battery | $ per kWh |
|-------|--------|---------|-----------|
| Atto 3 | $23,736 | 49.9 kWh | $476/kWh |
| Zeekr 7X | $41,457 | 75.0 kWh | $553/kWh |
| Onvo L60 | $37,904 | 60.0 kWh | $632/kWh |
| XPeng G6 | $33,163 | 68.5 kWh | $484/kWh |

[Source: computed from landed cost ÷ battery_kwh, both from vehicle records]

**Price per km of CLTC range (landed):**

| Model | Landed | CLTC range | $ per km |
|-------|--------|-----------|----------|
| XPeng G6 | $33,163 | 625 km | $53/km |
| Zeekr 7X | $41,457 | 620 km | $67/km |
| Onvo L60 | $37,904 | 560 km | $68/km |
| Atto 3 | $23,736 | 430 km | $55/km |

[Source: computed from landed cost ÷ range_cltc_km]

The Atto 3 and XPeng G6 are the efficiency leaders on these crude metrics — the Atto 3 on battery-economics, the G6 on range-economics. The Zeekr 7X and Onvo L60 pay a premium per unit of capability, justified only if the buyer values their larger absolute range and (for the 7X) faster CCS2 charging.

## Selection recommendation

**Pick the Atto 3** for the price-sensitive fleet or first-time importer: it is the cheapest to land and the most efficient per kWh. Its limitation is 430 km CLTC and GB/T charging that needs an adapter.

**Pick the XPeng G6** for the range-and-charging sweet spot: 625 km CLTC and 800V-class fast charging at the lowest price-per-km of the four.

**Pick the Onvo L60** for a modern platform at a mid price, if your buyers want a fresh NIO-sub-brand SUV with 560 km range.

**Pick the Zeekr 7X** for the premium end: the most capability (75 kWh, 620 km, CCS2) at the lowest *percentage* premium (+28.1%), though the highest absolute price.

## Conclusion

In Australia's zero-duty, no-CVD structure, all four SUVs land at a +28% to +46% premium — a fraction of their Germany or Brazil landed cost. The Atto 3 is the price floor, the XPeng G6 the range-efficiency leader, and the Zeekr 7X the best spec-per-dollar at the premium end. Match the model to the buyer: price, range, or capability.

## Sources

1. China EV Mart vehicle records — Atto 3 / G6 / L60 / 7X frontmatter (`price_usd`, `battery_kwh`, `range_cltc_km`, `charging_interface`, `landed_cost_markets`) — accessed 2026-10-23
2. China EV Mart `tariffs.json` — Australia 0% duty, 10% GST — data date 2026-09-15
3. China EV Mart [Australia import guide](/docs/regional-import-guides/) and [Australia zero-duty analysis](/blog/australia-import-zero-duty/)

---

*For reference only — B2B import estimate, not a retail quote. RHD availability and ADR compliance must be confirmed per model. Verify with a customs broker. See the full [vehicle directory](/vehicles/) to compare more models.*
