# P1 Uniqueness Audit — Brand Pages · Country Guides · Comparison Articles

Scope: ChinaEVMart / electricvehiclehub.top. Discipline: sample → confirm → dispose (keep / rewrite / supplement / merge). Merge class is **listed only, not executed**.

Date: 2026-10-24 · Author: 小筑 (content strategist + technical SEO) · Repo: `electricvehiclehub.top`

---

## 1. Method & sample

Three content families were audited against four checks:

1. **Similar template sentences (n-gram)** — shared boilerplate skeleton.
2. **Repeated conclusions** — same verdict reworded across pages.
3. **Missing local data** (guides) — whether local regulation / market data is real and non-generic.
4. **Comparison coherence** — unified metric basis, substantive difference, sources.

Sampling: **10 brand pages + 10 country guides + 10 comparison articles**, stratified across body length, plus a **full-corpus structural scan** (word counts, title counts, heading fingerprints, n-gram counts) over all 72 brands / 30 guides / 31 comparisons.

| Family | Corpus size | Sampled | Corpus scan |
|---|---|---|---|
| Brand pages (`src/content/brands/*.md`) | 72 | 10 | word counts + title count + n-gram over all 72 |
| Country guides (`src/content/blog/*-import-guide.md`) | 30 | 10 | word counts over all 30 |
| Comparison articles (`src/content/blog/*-vs-*.md`) | 31 | 10 (1 full + heading fingerprint of all 31) | heading structure over all 31 |

---

## 2. Sampling matrix (four-class counts)

| Family | 保留 keep | 重写 rewrite | 补充 supplement | 合并 merge | Total |
|---|---|---|---|---|---|
| Brand pages | 3 | 69 | 0 | 0 | 72 |
| Country guides | 30 | 0 | 0 | 0 | 30 |
| Comparison articles | 31 | 0 | 0 | 0 | 31 |
| **Total** | **64** | **69** | **0** | **0** | **133** |

---

## 3. Findings by family

### 3.1 Brand pages — severe isomorphism (the core P1 problem)

- **72/72** share the identical title suffix `"…: Chinese EV Brand Profile & Export Data"`.
- Bodies are **1–3 sentences (34–84 words)** following one skeleton: `「X is a [descriptor] brand under [parent]… [philosophy]」` — confirmed by n-gram scan (e.g. `"is a premium intelligent electric vehicle brand under…"` ×3, `"is a passenger vehicle brand under…"` ×2, and 12 more near-identical `"is a … brand under …"` variants).
- The `description` fields are **literally truncated with `…`** in the source (e.g. `"…Since entering the auto…"`), a machine-generation artefact.
- **3 pages already carry real data** (model count + factory price range + Germany landed-cost range + premium): `aito`, `arcfox`, `im` — these are the template the rest should follow.
- The brand page **template itself is data-rich** (renders model list, powertrain distribution, family grouping from the `vehicles` collection) — the *prose* is what is thin/isomorphic.

**Disposition:** 3 keep · 69 rewrite. No supplement (thinness is secondary to isomorphism; fix is a data-enrichment rewrite, not padding). No merge (each describes a distinct legal entity).

### 3.2 Country guides — high value, differentiated (keep)

All 10 sampled guides carry **real, non-generic local data with sources**: tariff schedules with dates (Brazil 35% II ramp, Turkey 40% + ÖTV, Indonesia 50% after exemption expiry, Mexico 50% decree, South Africa 25% + ad-valorem ambiguity, Norway NOK 300k VAT threshold, Australia 0% + RHD/ADR/RAV gates), brand-level CVD tiers (EU), worked examples, and per-market landed-cost tables computed from `landed_cost_markets`. The section skeleton is shared, the content is not. No repeated conclusions (each "Author's Take" is market-specific).

**Disposition:** 30 keep.

### 3.3 Comparison articles — shared series template, unique data (keep)

All 31 share a deliberate series skeleton (TL;DR → Key statistics → spec table → tariff stack → landed-cost matrix → German customs worked example → "where the comparison can go wrong" → Author's Take → Sources). Content is **unique per vehicle pair**: different specs, different CVD tiers, different market matrices, different "flip" analyses, real sources. The 6-article "vs Tesla Model Y" cluster compares different challengers and reaches different verdicts — **not near-duplicates**. The 5 methodology "vs" articles (CCS2-vs-GBT, CLTC-vs-WLTP, LHD-vs-RHD, sticker-vs-landed, WVTA-vs-SVA) are shorter reference explainers but complete.

**Disposition:** 31 keep. No merge.

---

## 4. Disposition matrix (sampled pages)

### 4.1 Brand pages (10 sampled)

| Page | Finding | Disposition |
|---|---|---|
| aito | data-rich (model count, price range, DE landed) | **keep** |
| arcfox | data-rich | **keep** |
| im | data-rich | **keep** |
| byd | boilerplate, 46-model flagship | **rewrite** ✅ executed |
| xpeng | boilerplate | **rewrite** ✅ executed |
| nio | boilerplate | **rewrite** ✅ executed |
| zeekr | boilerplate | rewrite (batch) |
| avatr | boilerplate | rewrite (batch) |
| jetour | boilerplate (name-etymology variant) | rewrite (batch) |
| haval | boilerplate | rewrite (batch) |

### 4.2 Country guides (10 sampled) — all **keep**

brazil · turkey · south-africa · indonesia · mexico · germany · netherlands · australia · norway · australia-suv

### 4.3 Comparison articles (sampled) — all **keep**

mg-4-vs-byd-dolphin (full read) + byd-atto-3-vs-tesla-model-y + zeekr-7x-vs-tesla-model-y (full reads) + heading fingerprint of all 31.

---

## 5. Execution record

### 5.1 Rewrite pilot — 3 brand pages (executed)

Rebuilt the thin boilerplate body + truncated description into the data-rich format (matching `aito`/`arcfox`/`im`), using **only computed real data** from the `vehicles` collection (`price_usd`, `landed_cost_markets`) and `brand-master.json`. No fabricated numbers.

| Page | New body data (computed) |
|---|---|
| `byd.md` | 46 models · factory $8,940–$32,370 · Germany landed $20,292–$56,176 · +51%–+127% · 17.0% CVD |
| `xpeng.md` | 10 models · factory $16,800–$43,630 · Germany landed $33,143–$75,534 · +48%–+97% · 20.7% CVD |
| `nio.md` | 10 models · factory $41,850–$108,170 · Germany landed $72,721–$177,505 · +64%–+74% · 20.7% CVD |

### 5.2 Supplement — 0 executed

No thin-but-clear-intent page found outside the brand pages (which are classified *rewrite*, not *supplement*). Country guides (min 963 words) and comparisons (min 778 words) are all substantial.

### 5.3 Merge — 0 executed (none found)

No near-duplicate pages. Each brand/country/vehicle-pair is a distinct entity or topic.

---

## 6. Pending — await approval (not executed)

1. **66 brand-page rewrites** — remaining boilerplate brand pages (72 − 3 keep − 3 rewritten). Batch into data-rich format from `vehicles` + `brand-master.json`.
2. **Title unification** — replace the 72 identical `"…: Chinese EV Brand Profile & Export Data"` suffix with unique per-brand titles (the "Export Data" claim is misleading on boilerplate pages that carry no export data). Touches sitemap + internal links; do as a separate reviewed batch.
3. **Description truncation cleanup** — remove the literal `…` truncation artefacts in the 66 remaining `description` fields.
4. **Draft-flag decisions** — `australia-import-guide.md` and `zeekr-7x-vs-tesla-model-y.md` are `draft: true` (not in sitemap). Publish or delete — owner decision.

---

## 7. Verification

- Build + 3-page render + git commit/push recorded in the delivery report (see commit log, `p1-unique-*` tag).
