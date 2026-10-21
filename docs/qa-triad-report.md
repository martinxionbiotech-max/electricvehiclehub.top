# EVHub Top — QA Triad Report（完整性 / 原创度 / 数据准确度）

- **站点**：electricvehiclehub.top（Astro · 517 深度档案）
- **基底**：CNEVhub（.net 仓，electricvehiclehub.net 源站）
- **日期**：2026-10-21
- **审计范围**：`src/content/vehicles/*.md` 全量 517 篇 + 渲染模板 `src/pages/vehicles/[slug].astro` + 基底 `CNEVhub/src/content/vehicles`（逐 slug 比对）
- **结论**：数据注入**零错误**（映射/残留/断链 0 项），但**站内模板化重蹈 .net 覆辙**（Overview 模板化率 89.2%），且深度档案 8 个 schema 字段 0% 填充。

---

## 评分总览

| 维度 | 评分 | 一句话判定 |
|---|---|---|
| ① 完整性 | **70 / 100** | 核心字段 100%、五段结构渲染完整；但 8 个 deep 字段 0% 填充 + 基底 spec 继承缺口 + 212 描述截断（已修 176） |
| ② 原创度 | **42 / 100** | 外部查重 0 违规（加分），但站内 89.2% 模板化 + certification_notes 511/517 逐字相同 |
| ③ 数据准确度 | **94 / 100** | 注入零错误、HS Code×动力 0 异常、landed_cost 0 偏差、source URL 30/30 有效；仅基底继承的检索值存疑 |

---

## 一、完整性检查

### 1.1 五段字段存在率矩阵（517 全量）

> 五段 = ① Entity Snapshot / ② Powertrain & Architecture（三电）/ ③ Dimensions & Logistics / ④ Market Compliance & Export Profile（合规接口）/ ⑤ Benchmarking Matrix（竞品矩阵，**模板动态计算，无逐文件字段**）。

| 段 | 字段 | 存在 | 缺失 | 填充率 | 说明 |
|---|---|---|---|---|---|
| ① | title / description / slug / brand / type / powertrain / price_usd / currency | 517 | 0 | 100% | 核心全齐 |
| ① | fast_charge / landed_cost / publishedDate / author / tags / family / image / image_credit / image_source / data_tier / data_reviewed | 517 | 0 | 100% | — |
| ① | range_cltc_km | 486 | 31 | 94.0% | 16 篇 null（12 HEV + 3 ICE + 1 PHEV `changan-cs75`） |
| ① | **trim** | 0 | 517 | **0%** | schema 定义未填充，渲染回退 `Standard (base)` |
| ① | **fob_price_usd_min / fob_price_usd_max** | 0 | 517 | **0%** | 渲染回退 `≈ price_usd (ex-factory)` |
| ① | range_wltp_km | 9 | 508 | 1.7% | — |
| ② | battery_kwh | 468 | 49 | 90.5% | 1 null（ICE） |
| ② | motor_power_kw | 484 | 33 | 93.6% | 1 null（ICE） |
| ② | torque_nm | 421 | 96 | 81.4% | — |
| ② | accel_0_100_s | 316 | 201 | 61.1% | 基底继承缺口 |
| ② | top_speed_kmh | 378 | 139 | 73.1% | — |
| ② | efficiency_kwh_100km | 284 | 233 | 54.9% | — |
| ② | battery_type | 503 | 14 | 97.3% | — |
| ② | drive_type | 517 | 0 | 100% | — |
| ② | motor_type | 514 | 3 | 99.4% | — |
| ② | **motor_model** | 1 | 516 | **0.2%** | 检索填充几乎未做 |
| ② | total_power_kw | 14 | 503 | 2.7% | — |
| ② | battery_thermal | 510 | 7 | 98.6% | 1 N/A |
| ② | heat_pump | 190 | 327 | 36.8% | 51 N/A |
| ② | suspension_front / suspension_rear | 505 | 12 | 97.7% | — |
| ② | **brakes** | 0 | 517 | **0%** | schema 定义未填充 |
| ② | drag_coefficient | 28 | 489 | 5.4% | — |
| ③ | length_mm / width_mm / height_mm / wheelbase_mm | 505/503/504/500 | 12–17 | 96.7–97.7% | — |
| ③ | weight_kg | 353 | 164 | 68.3% | — |
| ③ | **gross_weight_kg / ground_clearance_mm** | 0 | 517 | **0%** | schema 定义未填充 |
| ③ | trunk_l | 2 | 515 | 0.4% | — |
| ④ | hs_code / charging_interface / certification_notes / landed_cost / landed_cost_markets | 517 | 0 | 100% | — |
| ④ | charging_adapter | 516 | 1 | 99.8% | 18 N/A |
| ④ | **infotainment_language / network_bands** | 0 | 517 | **0%** | schema 定义未填充 |
| ⑤ | Benchmarking Matrix | — | — | 渲染 100% | 模板从 517 池动态选 2 竞品，无逐文件字段 |

**零填充 schema 字段（8 个，渲染为 N/A 或默认值）**：`trim`、`fob_price_usd_min`、`fob_price_usd_max`、`brakes`、`gross_weight_kg`、`ground_clearance_mm`、`infotainment_language`、`network_bands`。
**近零字段**：`motor_model`（1）、`trunk_l`（2）、`total_power_kw`（14）、`drag_coefficient`（28）、`range_wltp_km`（9）。

### 1.2 五段结构章节完整性

- 渲染层（`[slug].astro`）**五段全在**：Entity Snapshot / Powertrain & Architecture / Dimensions & Logistics / Market Compliance & Export Profile / Benchmarking Matrix，517/517 无例外。
- Markdown 正文仅 3 个 H2：`Overview` / `Landed Cost by Market` / `Detailed Breakdown — Germany`（517/517 全在）。五段内容由模板从 frontmatter 计算渲染，非逐文件手写。

### 1.3 占位残留

- 正文与 frontmatter 残留（`{…}` / `undefined` / `null` / `NaN` / `[object Object]` / `TODO` / `TBD`）：**0**。
- `data_source` / `data_updated` 重复：**0**（各 ×1，无注入残留）。
- 重复 slug：**0**；frontmatter 解析失败：**0**。

### 1.4 N/A 分布（合法留白 vs 应为可填而漏填）

| 字段 | N/A/空 计数 | 占比 | 性质 |
|---|---|---|---|
| fast_charge | 158（null） | 30.6% | **合法**（仅慢充车型） |
| heat_pump | 51 | 9.9% | 合法（多数车型无热泵） |
| charging_interface | 19 | 3.7% | **合法**（HEV 非插混 + ICE，`N/A (…)` 标注） |
| charging_adapter | 18 | 3.5% | 合法（同上） |
| range_cltc_km | 16（null） | 3.1% | 12 HEV + 3 ICE **合法**；**1 PHEV `changan-cs75` 应为可填而漏填（P2）** |
| battery_kwh / motor_power_kw | 1 各（null） | 0.2% | 合法（`changan-nevo-lamore` ICE） |

> 上述 null 均**继承自 .net 基底**（全量逐值比对 0 漂移），非 .top 注入引入。

---

## 二、内容原创度检查

### 2.1 站内模板化检测（核心 —— 重蹈 .net 覆辙）

**判定：.top 深度档案 Overview 散文**重蹈 .net 覆辙**，模板化未解除。**

- **Overview 模板化率：89.2%**（掩码数字/车型/品牌后，句式骨架在 ≥2 篇复用的句子占全部 Overview 句子的比例）。
- Overview 词数：min 29 / max 110 / **mean 84.1** / median 86（.net 审计为 93.9，基本同构）。
- 逐字复用句对（精确相同句子，跨 ≥2 篇）：**192 条**；掩码后复用骨架：**96 种**。

**最重复句式骨架（masked，跨 N 篇复用）**：

| N 篇 | 句式骨架 |
|---|---|
| **404** | `For importers, the cheapest entry point is United Arab Emirates at roughly +{N}% over base (about {PRICE} landed), while …` |
| **347** | `It is positioned as a value-focused import, priced from {PRICE} ex-factory.` |
| **188** | `In practice, the {N} kWh/100km efficiency is strong for its {N} kg curb weight.` |
| **183** | `It suits importers and fleet buyers evaluating Chinese EV landed cost.` |
| **92** | `… while Germany applies the standard tariff …` |
| **91** | `It suits family and executive buyers prioritizing space.` |
| **91** | `only slow AC charging is listed, which affects fleet turnaround.` |
| **74** | `It lands in the mid-market segment where spec-to-price ratio matters most …` |
| **73** | `It suits families and fleet buyers who need practicality.` |
| 41 / 39 / 33 / 31 / 25 … | 其余「efficiency / premium import / affordable end / midsize SUV」变体 |

**逐字复用的非散文字段（模板化枚举，非 prose）**：

- `certification_notes`：**511/517（98.8%）逐字相同** `EU: WVTA type approval; GB/T port needs CCS2/Type 2 adapter. GCC: GSO conformity certificate.`
- `charging_adapter`：3 个值覆盖 510/517：`CCS2 (DC) / Type 2 (AC) adapter required for EU; or OEM EU-spec port`（284）+ `PHEV/EREV: Type 2 (AC) adapter for EU AC charging`（208）+ `N/A`（18）。

### 2.2 外部查重（20 句高信息密度句）

- 抽 20 句含具体数字/专名的句子（含「For importers…UAE…」「luxury-tier flagship…」「midsize SUV battery-electric…」等），`exact-phrase` 检索（DuckDuckGo / Bing）。
- 结果：**0 外部逐字匹配**（模板自产句，未从 Wikipedia/官方源复制）。→ 无外部抄袭违规，但内部同构是「scaled content」信号。

---

## 三、数据准确度检查

### 3.1 深度字段 vs 原始基底交叉核验（**全量 517，非仅抽 40**）

- 比对字段：`price_usd` / `battery_kwh` / `motor_power_kw` / `torque_nm` / `range_cltc_km` / `length_mm` / `width_mm` / `height_mm` / `wheelbase_mm` / `weight_kg` / `accel_0_100_s` / `top_speed_kmh` / `efficiency_kwh_100km` / `powertrain` / `type`。
- 与 `CNEVhub/src/content/vehicles` 同 slug 逐值比对：**0 映射错误**。深度档案注入**未污染任何基底值**。

### 3.2 HS Code × 动力形式（全量 517 复跑）

| Powertrain | 数量 | HS Code | 异常 |
|---|---|---|---|
| BEV | 286 | 87038000 | 0 |
| PHEV | 154 | 870340 | 0 |
| EREV | 58 | 870340 | 0 |
| HEV | 16 | 870340 | 0 |
| ICE | 3 | 87032200 | 0 |

缺失 0，不匹配 0。

### 3.3 Source URL 有效性（30 个 HEAD）

- `image_source` 域名：Wikimedia Commons **475** / 本站 image-credits（原创插图，合法）**42**。
- 抽 30 个 Wikimedia URL `HEAD`：**30/30 200 OK**。
- 图片文件缺失：**0**；`/image-credits/` 页存在。

### 3.4 landed_cost 复算（5 篇，Germany 主市场）

| 车型 | 存储 total | 复算 total | 偏差 |
|---|---|---|---|
| mg-4 | 23,761.74 | 23,761.74 | 0 |
| aion-rt | 28,814.28 | 28,814.28 | 0 |
| maxus-mifa-7 | 53,976.32 | 53,976.32 | 0 |
| onvo-l60 | 52,640.12 | 52,640.12 | 0 |
| jetour-dashing-i-dm | 34,232.99 | 34,232.99 | 0 |

公式 `base + duty + countervailing + VAT + freight + clearance + cert + registration + inland` 内部一致，`landed_cost` 全量 JSON 可解析（0 错误）。

### 3.5 检索填充值抽检（accel_0_100_s / motor_model）

- accel 范围 2.0–14.2s（316 值），数值区间合理。
- 抽检发现 **1 处存疑（P2，继承自基底）**：`byd-dolphin` `motor_power_kw=70` 但 `accel_0_100_s=4.3`（70 kW 版应为 ~12s 级；4.3s 疑似错配更高功率版本）。基底逐值比对 0 漂移，故属 .net 基底数据质量问题，非 .top 注入错误。

---

## 四、修复清单

| # | 级别 | 异常 | 处置 |
|---|---|---|---|
| 1 | P0（映射/残留/断链） | 无 | **0 项** —— 深度档案注入干净，无需当场修 |
| 2 | **P1（已修）** | 176 篇 description 模板截断（`Full landed-cost breakdown across…` 半句截断） | **本批已修**：补全为 `…across 7 export markets for B2B import planning.`（176 插入/176 删除，仅 description 行） |
| 3 | P1（待批） | 36 篇 description 非确定性截断 | 记录：11 篇「to the EU/DAC」变体 + 10 篇手写截断（byd-atto-3/blade bat、byd-seal/at just under、byd-dolphin、byd-han、byd-qin-plus、byd-song-plus、aion-y、denza-d9、xiaomi-su7、zeekr-001）+ 边角截断，需内容判断续写 |
| 4 | P2（建议） | 8 个 schema 字段 0% 填充（trim / fob_price / brakes / gross_weight / ground_clearance / infotainment_language / network_bands） | 按品牌回填（非阻断） |
| 5 | P2（建议） | Overview 散文模板化 89.2%（重蹈 .net） | **去模板化需批准**：为高出口价值车型补 1–2 句车型级独特见解（竞品定位/电池化学/出口强项），目标 mean >150 词、骨架去重率提升 |
| 6 | P2（建议） | certification_notes 511/517 逐字相同、charging_adapter 3 值覆盖 510 | 合规枚举类字段，按 powertrain/地区差异化 |
| 7 | P2（建议） | 基底 spec 缺口（accel 61%、weight 68%、efficiency 55%）+ byd-dolphin accel 存疑 | 属 .net 基底继承缺口，建议另窗回填 |

---

## 五、方法学备注

- 完整性/原创度/准确度三项均由 `scripts/qa-triad/*.py` 程序化产出（可复现）。
- 交叉核验采用**全量 517**（任务要求抽 40，已增强为全量）。
- 外部查重因 `web_search`/`tavily` 不可用，改用 `web_fetch` + DuckDuckGo/Bing `exact-phrase` 检索完成。
- 描述截断修复仅触及 `description:` 单行，未改动任何数据字段/JSON/渲染逻辑。
