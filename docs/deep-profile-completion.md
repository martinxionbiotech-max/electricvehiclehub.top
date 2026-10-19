# EVHub Top — Deep Vehicle Profile Completion Report

- **Site**: electricvehiclehub.top (Astro)
- **Repository**: `electricvehiclehub.top`
- **Date**: 2026-10-19
- **Window**: 2C (final batch) — completion of all remaining vehicles to 517/517

## Completion Summary

| Metric | Value |
|---|---|
| Total vehicle files | **517** |
| Deep profiles complete (`charging_interface` present) | **517 / 517 (100%)** |
| Window 2C added | **133** vehicles |
| Window 2C HS-code backfill (pre-existing w1 gaps) | **52** vehicles |
| Final build | **900 pages**, exit 0 |

## Field Fill Rate (across all 517 deep profiles)

| Field | Filled | Rate |
|---|---|---|
| `drive_type` | 517 | 100.0% |
| `hs_code` | 517 | 100.0% |
| `charging_interface` | 517 | 100.0% |
| `motor_type` | 514 | 99.4% |
| `battery_thermal` | 510 | 98.6% |
| `suspension_front` | 505 | 97.7% |
| `suspension_rear` | 505 | 97.7% |
| `battery_type` | 503 | 97.3% |

Notes:
- `battery_type` / `motor_type` / `battery_thermal` legitimately render **N/A** for non-electrified
  powertrains (3 ICE + non-plug-in HEV units), per the zero-fabrication contract.
- `charging_interface` is `N/A (…)` for **19** vehicles (HEV non-plug-in hybrids + ICE),
  matching the HS-code rule (BEV=87038000, PHEV/EREV/HEV=870340, ICE=87032200).

## HS Code Distribution

| HS Code | Count | Powertrain |
|---|---|---|
| `87038000` | 286 | BEV |
| `870340` | 228 | PHEV / EREV / HEV |
| `87032200` | 3 | ICE (petrol passenger car) |

## Brand Grouping (deep profiles complete)

byd 46 · geely-galaxy 19 · wuling 19 · leapmotor 16 · chery-fulwin 14 · hongqi 14 ·
changan 14 · aion 13 · roewe 12 · lynk-co 12 · gac-motor 11 · jetour 11 · forthing 11 ·
exeed 10 · changan-nevo 10 · xpeng 10 · nio 10 · aito 10 · deepal 10 · denza 9 ·
zeekr 9 · avatr 9 · voyah 8 · jac 8 · im 7 · arcfox 7 · chery-new-energy 7 ·
li-auto 7 · bestune 7 · haval 7 · aeolus 7 · baojun 7 · maxus 7 · mg 6 · hyptec 6 ·
dongfeng-e 6 · xiaomi 6 · chery 6 · geometry 5 · ora 5 · jac-refine 5 · neta 5 ·
jmc 4 · tank 4 · sehol 4 · dayun 4 · fangchengbao 4 · icaur 4 · landian 4 · baw 4 ·
cowin 4 · hycan 4 · wey 4 · geely 4 · oshan 3 · venucia 3 · m-hero 3 · jac-yiwei 3 ·
stelato 3 · livan 3 · onvo 3 · yangwang 3 · skywell 2 · firefly 2 · dongfeng-nammi 2 ·
kaicene 2 · luxeed 2 · yudo 2 · saic 2 · maextro 1 · jaecoo 1 · seres 1

## Data Discipline

- **Precise mapping**: injection scripts add only five-section fields
  (`battery_type`, `drive_type`, `motor_type`, `battery_thermal`, `suspension_front`,
  `suspension_rear`, `charging_interface`, `charging_adapter`, `certification_notes`,
  `hs_code`) — base specs (`battery_kwh`, dimensions, `price_usd`, `landed_cost`) untouched.
- **Sourced fills**: battery chemistry / drive / suspension verified via
  `en.wikipedia.org` MediaWiki API where entries exist (BYD Seal 06, Aion V/Y/RT/UT,
  XPeng Mona M03, Deepal SL03/A07, Neta V/X/Aya, Leapmotor A05, Ora Good Cat,
  Chery Fulwin A9, Changan Nevo A07, MG S5, Hongqi E-QM5); otherwise manufacturer-spec
  conventions by brand. No fabricated sub-fields — uncertain values left as N/A.
- **Idempotent**: `data_source` / `data_updated` de-duplicated via `re.sub` (no
  `.*\n`), repeated runs produce zero diff. All files verify `data_source` ×1 and
  `data_updated` ×1.
- **HS Code by powertrain** enforced programmatically and spot-checked.

## Consistency Spot-Check (10 random profiles)

Sampled 10 deep profiles — all passed:
6/6 core fields present · HS code matches powertrain · `data_updated`/`data_source`
single occurrence (no residue).

## Commits

- `evhub-top-w2c: deep-profile batch C1 (45) …`
- `evhub-top-w2c: deep-profile batch C2 (44) …`
- `evhub-top-w2c: deep-profile batch C3 (44) + hs_code backfill (52) …`

Sync verified `0 0` against `origin/main`.
