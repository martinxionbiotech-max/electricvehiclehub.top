# P1 数据核验批 — 分层抽查扩样 + 欧盟税率/计税公式复核

- 日期：2026-10-23
- 仓：`electricvehiclehub.top`（chinaevmart.com 生产仓）
- 前序：P0 数据核验（40 款）、参数级核验系统 five-01（32 款）、P3 数据规范化（517 价格口径）、P5 落地成本三方对账（.net 仓）
- 纪律：零编造 · 冲突标记不自动填补 · 低置信数据设待核验状态 · 三态判定 + 五元组

---

## 0. 结论摘要

| 维度 | 结果 |
|---|---|
| 抽样规模（本批新增） | **58 款**（A 层 Tier 1 优先，品牌 × 动力形式 × 价格带分层） |
| 累计覆盖（参数级核验） | **90 款**（32 既有 + 58 新增） |
| 三态分布（58 款 × 6 关键参数 = 348 格） | verified 21 · conflict 7 · unverifiable 320（另有车身类型 8 修正 + 3 冲突） |
| 当场修正 | **8 款车身类型**（SUV → Sedan/Wagon/MPV，挂 source） |
| 冲突标记（不填补） | **10 处**（7 数值 + 3 车身类型 shooting-brake） |
| 待核验（unverifiable / low-confidence） | **320 格 + 34 款整篇** |
| EU CVD 分档 | **与 Reg 2024/2754 终裁一致**（BYD 17.0 / Geely 18.8 / SAIC 35.3 / Tesla 7.8 / other-coop 20.7 / non-coop 35.3）；映射缺口：non-coop 35.3 未落表 |
| 计税公式链 | **duty→cvd→vat→固定费 复算一致**（byd-seagull 逐项吻合）；计税基础为 ex-factory（非 CIF），方法页已披露为简化 |

---

## 1. 分层抽查扩样（58 款）

### 1.1 抽样设计

- **人群**：A 层（`quality_tier=A`）且 `data_tier∈{1,2}` 未核验者（355 款候选）。
- **优先**：Tier 1（223 款）先于 Tier 2；品牌组按曝光度加权（BYD/Geely/SAIC/Tesla 权重 4 > Changan/Chery/NIO/XPeng/Xiaomi/Li Auto 3 > GAC/FAW/AITO/Leapmotor 2 > Dongfeng/BAIC 1）。
- **分层**：品牌组 × 动力形式 × 价格带。
- **结果**：58 款，品牌覆盖 31 个（denza/byd 7、geely 系 10、SAIC 系 10、changan 系 7、nio/xpeng/xiaomi/li-auto/leapmotor/hongqi/bestune/arcfox/voyah/aion/hyptec/exeed/chery/ora/dayun/hycan/stelato 等）；动力形式 BEV 30 / EREV 15 / PHEV 13；价格带 $10–20k 3 / $20–40k 44 / $40–80k 11（A 层 Tier 1 天然向中高价集中，<10k 与 80k+ 在 A 层 Tier 1 稀疏）。

### 1.2 完整抽样清单

`denza-z9-dm-i · denza-z9-gt-dm-i · denza-n8l · denza-n7 · byd-tang-l-dm-i · byd-han-l-dm-i · byd-song-l-ev · dayun-y6 · hycan-v09 · hycan-007 · ora-lightning-cat · xpeng-g9 · xpeng-gx · stelato-s9t-erev · im-l7 · im-l6 · im-ls6-erev · maxus-mifa-7-phev · roewe-f7 · roewe-r7 · saic-h5-erev · mg6-phev · baojun-xiangjing-phev · roewe-d7-phev · nio-et5t · nio-et5 · geely-galaxy-l380 · zeekr-mix · geely-galaxy-v900 · lynk-co-z10 · zeekr-7x · zeekr-007 · zeekr-007-gt · geometry-a · lynk-co-07 · lynk-co-07-gt · aion-lx-plus · hyptec-hl-erev · voyah-passion-l · voyah-passion-phev · avatr-12-erev · avatr-07l · avatr-06t · avatr-07-erev · changan-nevo-e07-erev · avatr-06 · avatr-06-erev · xiaomi-skynomad-n90 · arcfox-as · li-auto-i6 · leapmotor-d99 · leapmotor-d19 · hongqi-eh7 · bestune-e01 · exeed-ex7 · exeed-exlantix-et-erev · chery-new-energy-shuxiangjia · chery-new-energy-arrizo-e`

### 1.3 核验方法

- **来源**：`en.wikipedia.org`（MediaWiki API `extracts` + `parse/wikitext` infobox；官方/权威邻接源，与既有 `source-verification` skill 的 Wikipedia 路径一致）。
- **五元组**：`source / verified_at / model_year / trim / confidence`，续航参数额外带 `test_standard`（CLTC/WLTP/EPA/NEDC）。
- **说明**：`model_year` 全库 0 填充（不编造）；Wikipedia 给出的投产/上市年份只作为 `source` 措辞证据引用，不擅自写入 `model_year` 数值字段。价格 USD 汇率口径沿用 P3 `ex-factory reference` 默认，本批不做逐值汇率溯源（标记 unverifiable）。

---

## 2. 三态判定与分布

状态机（沿用 five-01，四态 + 待核验）：

| 状态 | 含义 | 处置 |
|---|---|---|
| `verified` | 官方/权威源一致 | 绿标 |
| `mismatch`（→修正） | 方向可判的值错 → **当场修正 + 挂 source** | 修正 |
| `conflict`（标记） | 两源/字段↔正文打架、方向不可判 → **只标记不改值** | 黄标 |
| `unverifiable` | 无公开源 → **待核验（pending）** | 灰标「待核验」 |

> 任务三态 `verified / mismatch / unverifiable` 映射：`mismatch` 拆分两类——方向可判的「当场修正」（本批 8 款车身类型）；方向不可判的升级为 `conflict`（沿用零编造纪律，不武断取舍）。

### 2.1 三态分布（58 款 × 6 参数 = 348 格）

| 参数 | verified | conflict | unverifiable |
|---|---|---|---|
| price | 0 | 0 | 58 |
| range | 9 | 3 | 46 |
| battery | 5 | 2 | 51 |
| motor | 7 | 2 | 49 |
| accel | 0 | 0 | 58 |
| charge | 0 | 0 | 58 |
| **合计** | **21** | **7** | **320** |

另有车身类型 `type` 附加格：**8 修正（verified）+ 3 conflict**。

### 2.2 verified（真实核验一致，21 数值格）

| 车型 | 参数 | 结论（源：en.wikipedia.org infobox） |
|---|---|---|
| denza-n7 | range / battery / motor | 702 km CLTC · 91.3 kWh · 230 kW（base，230–390） |
| hycan-v09 | range / motor | 620 km CLTC（base，620–762）· 202 kW（=275 PS） |
| im-l7 | range / battery | 708 km CLTC（top，615–708）· 90 kWh |
| saic-h5-erev | range / motor | 235 km（EREV）· 150 kW（≈200 hp） |
| geely-galaxy-l380 | range / battery | 570 km（base，570–825）· 100 kWh（option） |
| zeekr-7x | range / battery / motor | 620 km CLTC（605–802）· 75 kWh（base）· 370 kW（310–585） |
| hongqi-eh7 | range / motor | 600 km CLTC（base，600–820）· 253 kW（base，253–455） |
| bestune-e01 | battery / motor | 61.34 kWh · 140 kW（top，100–140） |
| avatr-06 | motor | 231 kW rear PMSM |
| xpeng-gx | range_long | 1585 km 综合 EREV CLTC |
| xiaomi-skynomad-n90 | range_long | 1705 km 综合 CLTC |

> 注：`range_long`（增程综合续航）与纯电 `range_cltc` 分字段，本批对 `xpeng-gx` / `xiaomi-skynomad-n90` 的 range_long 与 Wikipedia 综合续航精确吻合。

---

## 3. 修正清单（mismatch → 当场修正 + source，8 款车身类型）

`data_updated` 统一更新为 `2026-10-23`，`data_source` 追加 `P1 body-type fix {from}→{to} vs en.wikipedia.org, 2026-10-23`。

| slug | 字段 | 旧值 | 新值 | 官方依据（en.wikipedia.org） |
|---|---|---|---|---|
| im-l7 | type | SUV | **Sedan** | full-size sedan（4-door） |
| im-l6 | type | SUV | **Sedan** | compact executive liftback sedan |
| zeekr-mix | type | SUV | **MPV** | minivan（5-door van） |
| zeekr-007 | type | SUV | **Sedan** | compact executive sedan |
| lynk-co-07 | type | SUV | **Sedan** | mid-size sedan / station wagon |
| nio-et5 | type | SUV | **Sedan** | compact executive sedan（D-segment） |
| nio-et5t | type | SUV | **Wagon** | NIO ET5 Touring — station wagon（estate） |
| hongqi-eh7 | type | SUV | **Sedan** | executive sedan（4-door） |

---

## 4. 冲突清单（conflict，只标记不填补，10 处）

| # | 车型 | 参数 | 冲突内容 | 处置 |
|---|---|---|---|---|
| C-1 | ora-lightning-cat | battery | 字段 64.31 kWh vs Wiki 83.5 kWh（NMC）；多电池包（64.31/83.49） | 保留字段值 |
| C-2 | ora-lightning-cat | range | 字段 555 km CLTC vs Wiki 640 km **NEDC**——测试标准/trim 串口径 | 保留字段值，标准标注需人工核对 |
| C-3 | geometry-a | battery | 字段 46.1 kWh vs Wiki 51.9/61.9（2024 改款 vs 2019 首发） | 保留字段值 |
| C-4 | geometry-a | motor | 字段 100 kW vs Wiki 120 kW（改款 vs 首发） | 保留字段值 |
| C-5 | lynk-co-07 | motor | 字段 180 kW vs Wiki 160 kW 前电机 | 保留字段值 |
| C-6 | denza-n8l | range | 字段 230 km 纯电 vs Wiki「Denza N8」（2023 款）80/100 km；N8L 为 2025 改款 | 保留字段值，年款归属待对账 |
| C-7 | aion-lx-plus | range | 字段 1008 km 记为 CLTC，实为 **NEDC**（Wiki 503–1008 NEDC） | 保留字段值，测试标准标注需修正 |
| C-8 | denza-z9-gt-dm-i | type | 字段 Sedan；Z9 GT 为 shooting brake / station wagon | 保留字段值，枚举归属人工对账 |
| C-9 | zeekr-007-gt | type | 字段 Sedan；007 GT 为 shooting brake | 保留字段值 |
| C-10 | avatr-06t | type | 字段 Sedan；06T 为 station wagon 变体 | 保留字段值 |

---

## 5. 待核验清单（unverifiable → 待核验状态）

### 5.1 待核验规模

- **320 格**（58 款 × 6 参数中未逐条确认者）+ 3 处车身类型冲突。
- **34 款整篇待核验**（6 参数全 unverifiable，无独立 verified/conflict）：

`denza-z9-dm-i · byd-tang-l-dm-i · byd-han-l-dm-i · byd-song-l-ev · dayun-y6 · hycan-007 · xpeng-g9 · stelato-s9t-erev · im-ls6-erev · maxus-mifa-7-phev · roewe-f7 · roewe-r7 · mg6-phev · baojun-xiangjing-phev · roewe-d7-phev · geely-galaxy-v900 · lynk-co-z10 · lynk-co-07-gt · hyptec-hl-erev · voyah-passion-l · voyah-passion-phev · avatr-12-erev · avatr-07l · avatr-07-erev · changan-nevo-e07-erev · avatr-06-erev · arcfox-as · li-auto-i6 · leapmotor-d99 · leapmotor-d19 · exeed-ex7 · exeed-exlantix-et-erev · chery-new-energy-shuxiangjia · chery-new-energy-arrizo-e`

### 5.2 待核验原因分类

- **无英文 Wikipedia 条目 / 无 infobox 数值**：dayun-y6、hycan-007、maxus-mifa-7-phev、roewe-f7/r7、mg6-phev、exeed-ex7、exeed-exlantix-et-erev、chery-new-energy-*、arcfox-as、li-auto-i6、geely-galaxy-v900、lynk-co-z10、changan-nevo-e07-erev 等（改款/小众/新车型，公开源无单一权威数值）。
- **infobox 为多 trim/多标准列表，无法对到单一 base 值**：denza-z9-dm-i、byd-tang-l-dm-i、byd-han-l-dm-i、xpeng-g9、stelato-s9t-erev、im-ls6-erev、avatr-07l/07-erev/12-erev 等。
- **价格 / 加速 / 充电**：58 款全部 unverifiable（ex-factory USD 无权威汇率口径；Wikipedia infobox 多不列 0–100 与 DC 快充分钟数）。

> 这些字段 frontmatter 现有值**未删除**（避免破坏既有渲染），通过参数级 `status=unverifiable` / `confidence=low` 在页面「Key parameter verification」区渲染「待核验（pending）」灰标，并列出待核验参数清单。

---

## 6. 低置信数据管理（confidence 规则落实）

- **confidence 枚举**：`high`（官方源直接确认）/ `medium`（权威邻接源或部分一致）/ `low`（未确认，pending）。
- **pending 状态**：`status=unverifiable` 或 `confidence=low` → 渲染「待核验（pending）」灰标 + 区块底部待核验清单。
- **落地**：`src/data/parameter-verification.json` 逐参数带 `confidence`；`src/pages/vehicles/[slug].astro` 新增 `isPendingCell` 判定（unverifiable 或 low → 待核验），`statusLabel.unverifiable = '待核验 (pending)'`，并新增「待核验 (pending review)」汇总框。
- **schema**：`src/content.config.ts` param_verification 单元新增 `test_standard`（CLTC/WLTP/EPA/NEDC）+ `note`。

---

## 7. 欧盟税率映射与计税公式复核

### 7.1 EU CVD 分档映射（vs Reg 2024/2754 与现行公告）

**结论：分档与终裁税率一致，未改任何数字。**

| 生产商组 | 本仓 `brand_cvd` | Reg 2024/2754 终裁 | 判定 |
|---|---|---|---|
| BYD（含 Denza/Yangwang/Fangchengbao） | 0.170 | 17.0% | ✅ 一致 |
| Geely（含 Zeekr/Lynk & Co/Geometry/Livan/Galaxy） | 0.188 | 18.8% | ✅ 一致 |
| SAIC（含 MG/Maxus/Roewe/Wuling/Baojun/IM） | 0.353 | 35.3% | ✅ 一致 |
| Tesla（Shanghai） | 0.078 | 7.8% | ✅ 一致 |
| 其他配合调查生产商 | `_default` 0.207 | 20.7% | ✅ 一致 |
| 未配合调查生产商 | **未落表** | 35.3% | ⚠️ 映射缺口 |

**映射缺口（本仓侧数据字段复核发现）**：`brand_cvd` 缺少显式 `non-cooperating 35.3%` 桶；所有未列名品牌回落到 `_default=0.207`（other-cooperating）。对本库 72 品牌而言全部为主要车企（均属配合组 20.7%），故业务上正确；但若未来新增「未配合」品牌会错误回落 20.7% 而非 35.3%。**建议**：`brand_cvd` 增加显式注释或 `non_cooperating: 0.353` 键 + 注释「按品牌逐个确认」。

**复核局限**：EUR-Lex 直连仍被 AWS WAF challenge 拦截（HTTP 202），终裁税率经 Wikipedia（《Electric car》条目「definitive countervailing duties … by 30 October 2024」框架确认）+ 既有权威参考值核对；未发现 2026-10-23 前的税率变更（可及源范围内）。`cvd_meta.verification_status` 维持「与终裁一致、权威直连复核 pending」如实披露。

### 7.2 计税基础（CIF/货值）

- 本仓/姊妹站计算器均以 **ex-factory base price** 作为计税基数（`duty = base × 10%`），**非严格 CIF**（车价 + 保险 + 运费）。
- `landed-cost-methodology.astro` 已显式披露：「duty assessed on the ex-factory base price … under strict EU customs rules the dutiable value is the CIF value … a conservative simplification」。
- **结论**：计税基础为 ex-factory（简化），与严格 CIF 规则存在已知偏差，方法页已披露——保留现状，标注为「已披露的保守简化」。

### 7.3 公式链（duty → cvd → vat → 固定费）

复算 byd-seagull（base $8,940，德国）逐项吻合：

| 项 | 公式 | 计算值 | frontmatter |
|---|---|---|---|
| duty | 8940 × 10% | 894.00 | 894.0 ✅ |
| cvd | (8940 + 894) × 17% | 1671.78 | 1671.78 ✅ |
| vat | (8940 + 894 + 1671.78) × 19% | 2186.10 | 2186.1 ✅ |
| 固定费 | 2000 + 350 + 3250 + 500(reg) + 500(inland) | 6600 | ✅ |
| 合计 | | 20291.88 | 20291.88 ✅ |

**结论**：公式链 `duty→cvd→vat→固定费` 在 `.top` frontmatter / `landed-cost-methodology.astro` / `.net` 计算器三处**一致**（P5 已对账，本批复算再次确认）。

### 7.4 非欧市场税率抽核（5 市场）

| 市场 | 本仓 `standard_duty` / `vat` | 官方参考 | 判定 |
|---|---|---|---|
| United Kingdom | 10% / 20% | 10% 汽车关税 / 20% VAT | ✅ |
| UAE | 5% / 5% | 5% 关税 / 5% VAT | ✅ |
| Saudi Arabia | 5% / 15% | 5% 关税 / 15% VAT | ✅ |
| Australia | 0% / 10% | 中澳 FTA 0% / 10% GST | ✅ |
| Norway | 0% / 25% | EV 0% 关税 / 25% VAT | ✅ |

> 与官方公开税率一致（参考值核对；受工具限制未做逐市场官方页 live-fetch）。

---

## 8. 变更清单

| 文件 | 变更 |
|---|---|
| `src/data/parameter-verification.json` | **扩展**：32 → **90 款**；schema_version 1→2；续航格新增 `test_standard`；`coverage.p1_expansion=58` |
| `src/content/vehicles/*.md` | **8 款车身类型修正**（im-l7/im-l6/zeekr-mix/zeekr-007/lynk-co-07/nio-et5/nio-et5t/hongqi-eh7），+ source + data_updated=2026-10-23 |
| `src/content.config.ts` | param_verification 单元新增 `test_standard`（CLTC/WLTP/EPA/NEDC）+ `note` |
| `src/pages/vehicles/[slug].astro` | 新增「待核验 (pending)」判定与灰标 + 待核验汇总框 + range 源格显示测试标准 |
| `docs/p1-data-verification.md` | **新增**：本文档 |

---

## 9. 统计（累计）

- 抽样规模：本批 **58** 款 · 累计参数级核验 **90 / 517**。
- 三态分布（本批 348 格）：**verified 21 · conflict 7 · unverifiable 320**（+ 车身类型 8 修正 / 3 冲突）。
- 修正：**8 字段 / 8 文件**（车身类型，全部 + source + data_updated=2026-10-23）。
- 待核验：**320 格 + 34 款整篇**（未编造，已打「待核验」标）。
- EU CVD：分档与终裁一致，映射缺口 1 处（non-coop 35.3% 未落表）；公式链复算 3 处一致；计税基础 ex-factory 简化已披露。

*报告路径：`docs/p1-data-verification.md` · P1*
