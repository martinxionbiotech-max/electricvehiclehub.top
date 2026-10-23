# P2 全站 SEO 与 Spam 质量审计（p2-seo-spam-audit）

> 仓库：`electricvehiclehub.top`（chinaevmart.com 代码库）
> 阶段：03 P2 · 技术 SEO + 内容质量审计
> 日期：2026-10-23 · 方法：源码审查 + `npm run build`（896 页 exit 0）+ `dist/` 全量 grep + 程序化分组抽样
> 纪律：按**独立价值**决定补充 / 合并 / 保留 / 排除索引；排除索引类**列清单待批、不擅自执行**；无证据不判罚；零编辑除明确修复。

---

## 0. 结论摘要

| 维度 | 结果 |
|---|---|
| 分组抽样 | 60 页（车型 30 = A/B/C 各 10 · 品牌 15 · 指南 8 · 市场 7），程序化逐页核查 |
| 独立价值处置 | **保留 33 · 补充 22 · 合并 4 · 排除索引 1**（排除索引仅列清单待批，未执行 noindex） |
| 模板重复（n-gram） | 车型 Overview 散文高度同构：2585 句 → 1673 独特骨架，顶骨架复用 31× |
| 无效页（渲染空/数据缺） | **0 无效页**；C 层数据缺为诚实标注（非渲染缺陷） |
| 薄内容 | 品牌族中位 55 词（最薄）· 车型族中位 124 词 · 市场族中位 444 词 · 指南族中位 2254 词 |
| 错误内链 | **2 断链 → 本批当场修复（p2-seo-fix）**；81886 内链复扫后 **0 断链** |
| Schema | 15 页抽样：WebSite/Organization/BreadcrumbList 全有 + 车型 Vehicle/品牌 Organization/博客 Article；**0 虚构**（无 rating/review/availability/seller/aggregateRating） |
| Sitemap | **697 URL**（对账见 §3.2），全同域、0 缺 dist、0 断链 |
| Canonical | 全站 `chinaevmart.com` 自指，**0 非目标域残留** |
| Robots | `PUBLIC_INDEXABLE` 未设 → 全站 `noindex,nofollow`（预览过渡态，非缺陷） |
| SSR 渲染 | 抽 10 页：**0** `undefined/null/NaN/{…}` 残留 |

---

## 1. 分组抽样矩阵（60 页）

### 1.1 抽样方法

- **车型 30**：`scripts/p1_quality_tiers.json` 三层（A 433 / B 53 / C 31）各等距抽 10。
- **品牌 15**：72 品牌等距抽 15。
- **指南 8**：博客非 draft 77 篇等距抽 8（`draft:true` 的 9 篇不渲染，不计入）。
- **市场 7**：docs 非 draft 10 篇等距抽 7（5 篇 `draft:true` 不渲染）。

每页核查四项：① 模板重复（n-gram 骨架复用）② 无效页（渲染空/数据缺）③ 薄内容（词数 < 基线 / 纯表格无叙事）④ 错误内链（断链/错锚）。

### 1.2 车型抽样矩阵（30 页）

基线：车型正文中位 124 词（min 102 / max 151）。正文为「简介列表 + Overview 散文」，规格数据在 frontmatter 渲染表格中。

| 层 | slug | 正文词数 | 关键字段缺 | 核验 | 处置 |
|---|---|---|---|---|---|
| A | aeolus-e70 | 124 | 3 | unverified | 保留 |
| A | baojun-yunhai | 117 | 4 | unverified | 保留 |
| A | byd-tang | 131 | 3 | unverified | 保留 |
| A | chery-tiggo-8-pro-new-energy | 136 | 7 | unverified | 保留 |
| A | fangchengbao-ti-3 | 134 | 3 | unverified | 保留 |
| A | geometry-m6 | 122 | 3 | unverified | 保留 |
| A | jac-refine-e4 | 121 | 4 | unverified | 保留 |
| A | lynk-co-01 | 125 | 4 | unverified | 保留 |
| A | ora-lightning-cat | 125 | 4 | unverified | 保留 |
| A | wuling-binguo-pro | 123 | 7 | unverified | 保留 |
| B | aion-n60 | 116 | 7 | unverified | 保留 |
| B | aion-y | 121 | 3 | partial | 保留 |
| B | byd-sealion-05-dm-i | 125 | 3 | unverified | 保留 |
| B | byd-song-plus | 128 | 2 | unverified | 保留 |
| B | chery-tiggo-7-c-dm | 134 | 4 | unverified | 保留 |
| B | geely-galaxy-a7 | 126 | 3 | unverified | 保留 |
| B | hongqi-eh5 | 122 | 3 | unverified | 保留 |
| B | jetour-x70-c-dm | 124 | 4 | unverified | 保留 |
| B | lynk-co-05 | 126 | 4 | unverified | 保留 |
| B | skywell-ev6 | 124 | 4 | unverified | 保留 |
| C | aion-v-plus | 123 | 9 | unverified | 补充 |
| C | chery-explore-06-c-dm | 125 | 7 | unverifiable | **排除索引（待批）** |
| C | chery-fulwin-x3-plus | 125 | 9 | unverified | 补充 |
| C | dongfeng-epi-m8 | 106 | 10 | unverified | 补充 |
| C | gac-motor-xiangwang-s7 | 123 | 8 | unverified | 补充 |
| C | icaur-03t | 102 | 10 | unverified | 补充 |
| C | jetour-shanhai-l9 | 112 | 8 | unverified | 补充 |
| C | jmc-yi-chi-06 | 113 | 10 | unverified | 补充 |
| C | landian-e5 | 116 | 9 | unverified | 补充 |
| C | ora-5 | 103 | 9 | unverified | 补充 |

> 关键字段 = range_cltc_km / battery_kwh / motor_power_kw / torque_nm / accel_0_100_s / top_speed_kmh / weight_kg / model_year / trim / range_wltp_km（按动力形式排除合法留白）。C 层缺失以 `N/A` 诚实渲染，非无效页。

### 1.3 品牌抽样矩阵（15 页）

基线：品牌正文中位 55 词（min 37 / max 84），**整站最薄族** —— 单段品牌简介，无表格、无车型列表正文。

| slug | 词数 | 车型数 | 成立 | 处置 |
|---|---|---|---|---|
| aeolus | 48 | 7 | 2009 | 补充 |
| avatr | 56 | 9 | 2018 | 补充 |
| changan | 42 | 14 | 1957 | 补充 |
| cowin | 44 | 4 | 2014 | 补充 |
| dongfeng-nammi | 49 | 2 | 2020 | 补充 |
| gac-motor | 49 | 11 | 2010 | 补充 |
| haval | 74 | 7 | 2013 | 保留 |
| im | 83 | 7 | 2020 | 保留 |
| jetour | 83 | 11 | 2018 | 保留 |
| li-auto | 58 | 7 | 2015 | 补充 |
| maextro | 82 | 1 | 2024 | 补充 |
| nio | 54 | 10 | 2014 | 补充 |
| saic | 58 | 2 | 2025 | 补充 |
| tank | 59 | 4 | 2021 | 补充 |
| xiaomi | 61 | 6 | 2021 | 补充 |

> 品牌页均**有独立价值**（品牌实体 + 车型目录入链），判「补充」而非「排除」——薄但非无价值。`saic`（2 款）/`dongfeng-nammi`（2 款）/`maextro`（1 款）为冷门新品牌，可随内容批扩写，不构成索引排除。

### 1.4 指南抽样矩阵（8 页，blog）

基线：指南正文中位 2254 词（min 791 / max 5558），内容充实。

| slug | 词数 | 处置 |
|---|---|---|
| asean-import-comparison | 4086 | 保留 |
| byd-seal-vs-tesla-model-3 | 2015 | 保留 |
| denmark-import-guide | 3155 | 保留 |
| ireland-import-guide | 3533 | 保留 |
| netherlands-import-guide | 2976 | 保留 |
| qatar-import-guide | 1652 | 保留 |
| thailand-import-guide | 2811 | 保留 |
| xiaomi-su7-vs-tesla-model-3 | 1859 | 保留 |

### 1.5 市场抽样矩阵（7 页，docs 非 draft）

基线：市场正文中位 444 词（min 331 / max 1085）。

| slug | 词数 | section | 处置 |
|---|---|---|---|
| compliance-requirements | 444 | Certification & Compliance | 保留 |
| cost-breakdown-example | 441 | Landed Cost | 保留 |
| data-provenance | 554 | Data Quality | 保留 |
| faq | 643 | Reference | **合并（待批）** |
| glossary | 1085 | Reference | 保留 |
| introduction | 388 | Getting Started | 保留 |
| landed-cost-methodology | 682 | Landed Cost | **合并（待批）** |

> `docs/faq` 与静态页 `/faq/`、`docs/landed-cost-methodology` 与静态页 `/landed-cost-methodology/` 为**同主题重复**（§4 合并清单）。

---

## 2. 独立价值判定（四类处置）

### 2.1 处置原则

| 类 | 定义 | 证据门槛 |
|---|---|---|
| **保留** | 达标，有独立决策价值 | 数据完整 + 差异化叙事，或内容充实 |
| **补充** | 有价值但薄 | 有独立价值（实体/车型/主题真实存在），但正文词数低于基线或缺关键字段 |
| **合并** | 近重复 / 同主题 | 两个 URL 覆盖同一主题，其一无增量价值 |
| **排除索引** | 无独立价值 + 无流量潜力 | `unverifiable`（无权威源对应车型/代际）+ 核心字段大面积缺失 |

### 2.2 处置统计

| 类 | 数量 | 分布 |
|---|---|---|
| 保留 | 33 | 车型 20（A10+B10）· 品牌 3 · 指南 8 · 市场 2 |
| 补充 | 22 | 车型 9（C 层）· 品牌 12 · 市场 0 |
| 合并 | 4 | 市场 2（faq / landed-cost-methodology）+ 车型 Qin/Xinghai 系近重复 2（见 §4） |
| 排除索引 | 1 | 车型 `chery-explore-06-c-dm`（unverifiable） |

### 2.3 排除索引清单（**待批准后执行，本批未 noindex**）

| # | URL | 证据 | 建议 |
|---|---|---|---|
| E-1 | `/vehicles/chery-explore-06-c-dm/` | `verification_status: unverifiable`（P0 已标：Wikipedia 无对应车型/代际），10 关键字段缺 7，无流量潜力 | noindex 或并入品牌页说明 |

> 其余 C 层 30 款为「数据缺」但**车型真实存在**（有对应车系/代际），判「补充」不判「排除」。`byd-qin-l-dm-i` 同为 unverifiable 但未落入本批抽样，列入后续批同规则复核。

---

## 3. 技术面五查

### 3.1 ① Schema（抽 15 页）

抽样：车型 5（A×2/B×1/C×1 + byd-seal）· 品牌 5 · 博客 3 · 市场 2。

| 页面 | JSON-LD 类型 | 结果 |
|---|---|---|
| vehicles/byd-seal | WebSite + Organization + BreadcrumbList + **Vehicle** | ✅ |
| vehicles/aion-v-plus（C） | WebSite + Organization + BreadcrumbList + Vehicle | ✅ |
| vehicles/wuling-binguo-pro（A） | 同上 | ✅ |
| vehicles/aeolus-e70（A） | 同上 | ✅ |
| vehicles/aion-n60（B） | 同上 | ✅ |
| brands/byd · saic · xiaomi · nio · tank | WebSite + Organization + BreadcrumbList + Organization | ✅ |
| blog/byd-seal-deep-review · qatar-import-guide · xiaomi-su7-vs-tesla-model-3 | WebSite + Organization + BreadcrumbList + **Article** | ✅ |
| docs/glossary · landed-cost-methodology | WebSite + Organization + BreadcrumbList | ✅ |

**零虚构核验**：15 页 JSON-LD 逐键扫描 `rating / review / aggregateRating / reviewCount / availability / seller / priceValidUntil / numberOfReviews` —— **0 命中**。Vehicle `offers` 仅含 `price + priceCurrency + 诚实描述`，无库存/商家/评分。

### 3.2 ② Sitemap（对账）

`npm run build` 后 `dist/sitemap-0.xml` 实测 **697 URL**（P7 基线记为 700，差 3，见下）。

| 类 | 计数 | 状态 |
|---|---|---|
| 车型页 + 目录 | 517 + 1 = 518 | ✅ |
| 品牌页 + 目录 | 72 + 1 = 73 | ✅ |
| 博客正文 + 目录 | 77 + 1 = 78 | ✅ |
| 市场（docs 非 draft）+ 目录 | 10 + 1 = 11 | ✅ |
| 首页 | 1 | ✅ |
| 静态页（about/…/terms） | 16 | ✅ |
| **合计** | **697** | ✅ |

- 全 697 同域（`chinaevmart.com`），`dist/` 中 0 缺文件，0 断链。
- **与 P7「700」差 3**：docs 非 draft 由 14 篇 → 10 篇（5 篇转为 `draft:true`：australia-import / eu-import-guide / germany-import / uae-saudi-import / uk-import）导致 −4，叠加静态页 +1（data-methodology 新增）。**非缺陷**——draft 正确排除。
- 排除项正确：`/blog/page/N/`（13）· `/blog/tag/x/`（184）· 404/500 均不进 sitemap。

### 3.3 ③ Canonical（域一致）

- 全站 `<link rel="canonical">` 0 命中非 `chinaevmart.com`（dist 全量 grep）。
- 抽 7 页（首页/车型/品牌/博客/市场/静态）均自指正确。首页 canonical = `https://chinaevmart.com/`。

### 3.4 ④ Robots（PUBLIC_INDEXABLE 现状）

- `robots.txt.ts`：`Allow: /` + `Disallow: /api/`（无害空规则）+ AI crawler 显式放行 + `Sitemap: https://chinaevmart.com/sitemap-index.xml` ✅。
- `BaseLayout.astro`：`indexable = PUBLIC_INDEXABLE === '1'`；**未设 → 全站 `<meta name="robots" content="noindex, nofollow">`**（首页/车型页实测确认）。
- **现状 = 预览过渡态**（符合方案 C：`.pages.dev` 过渡期不入索引），**非缺陷**。生产上线放开步骤见 P7 §4。

### 3.5 ⑤ 页面渲染（抽 10 页 SSR）

抽 10 页（首页 / 车型 A·C / 品牌 2 / 博客 2 / 市场 1 / 静态 1），正则扫描 `\bundefined|null|NaN\b / {…} / [object Object]` 残留：

| 页面 | HTML 字节 | 残留 |
|---|---|---|
| index | — | 0 |
| vehicles/byd-seal | 39538 | 0 |
| vehicles/aion-v-plus | 35356 | 0 |
| vehicles/aeolus-e70 | 37939 | 0 |
| brands/byd | 93907 | 0 |
| brands/saic | 28437 | 0 |
| blog/byd-seal-deep-review | 64765 | 0 |
| blog/qatar-import-guide | 41489 | 0 |
| docs/glossary | 33723 | 0 |
| markets | 35001 | 0 |

**0 无效渲染**（初扫 `nan` 命中为误报——正文单词 "financial/dominant" 等子串，词边界正则后归零）。

---

## 4. 合并清单（近重复 / 同主题）

| # | 重复对 | 证据 | 建议 |
|---|---|---|---|
| M-1 | `/faq/`（静态）↔ `/docs/faq/` | 同主题（Frequently Asked Questions），两 URL 覆盖重叠 | 保留 `/docs/faq/`（docs 语境），`/faq/` 301 或 canonical 指向前者 |
| M-2 | `/landed-cost-methodology/`（静态）↔ `/docs/landed-cost-methodology/` | 同主题（landed-cost 公式），静态页 1163 词 vs docs 682 词 | 保留静态页（更完整），docs 页 301 或合并 |
| M-3 | 车型 Qin 系近重复（byd-qin / byd-qin-plus-dm-i / byd-qin-max-dm-i / byd-qin-l-dm-i / byd-qin-max-ev） | 同 brand+family "Qin" 5 变体，参数高重叠 | 评估合并为单一 Qin 车型页 + 变体表 |
| M-4 | 车型 Xinghai 系（forthing-xinghai-v6 / v6-plus / t5） | 同 brand+family "Xinghai" 3 变体 | 同 M-3 评估 |

> M-3/M-4 涉及页面结构改动，**列清单待批**，本批不执行。

---

## 5. 当场修复（低风险 · p2-seo-fix · 2 项）

| # | 异常 | 根因 | 修复 |
|---|---|---|---|
| F-1 | `/data-methodology/` → `/docs/verification-system/` 断链 | verification-system 是仓库报告（`docs/verification-system.md`）非内容页 | 指向 `/docs/data-provenance/`（真实内容页，覆盖参数级核验） |
| F-2 | `/docs/regional-import-guides/` → `/blog/australia-import-guide/` 断链 | 目标 `draft:true` 不渲染 | 指向 `/blog/australia-import-zero-duty/`（真实渲染页） |

验证：修复后 `npm run build` exit 0（896 页）+ `seo-validation` 复扫 **81886 内链 0 断链**。

---

## 6. 证据采样

- **模板同构证据**（车型 Overview 句骨架，2585 句 → 1673 独特骨架）：
  - `[31×] MODEL MODEL with DRIVE from MODEL.`
  - `[28×] MODEL MODEL MODEL from MODEL.`
  - `[24×] MODEL MODEL DRIVE from MODEL.`
  - `[21×] MODEL's MODEL MODEL is an DRIVE PT MODEL.`
  - `[16×] MODEL MODEL PT MODEL from MODEL MODEL.`
  - 顶骨架复用 10–31×，佐证 B 层「叙事同构」判定（P1 §5）。
- **品牌薄内容证据**：`changan` 42 词、`cowin` 44 词、`aeolus` 48 词（整站最薄族）。
- **无效页证据**：`npm run build` 896 页 exit 0 + 抽 10 页 0 残留 + 81886 内链 0 断链。
- **Schema 零虚构证据**：15 页 JSON-LD 无 rating/review/availability/seller/aggregateRating/priceValidUntil。

---

## 7. 分离声明

- **已验证**：§3.1 schema 一致性、§3.2 sitemap 697 对账、§3.3 canonical 域一致、§3.4 robots 过渡态、§3.5 SSR 渲染——均有 `dist/` 全量 grep / 程序化扫描证据。
- **已修复**：§5 F-1/F-2 两断链，`npm run build` exit 0 + 复扫 0 断链。
- **待批准（未执行）**：§2.3 排除索引 E-1（1 项）；§4 合并 M-1~M-4（4 项）。
- **推断/后续批**：车型正文散文与 frontmatter 漂移同步（P0/P1 遗留）；B 层 53 款去模板化队列；品牌族 12 页薄内容扩写。
- **未覆盖**：live HTTP 逐页状态码、Search Console 实际索引数据（无 GSC）。

---

*报告路径：`docs/p2-seo-spam-audit.md`*
