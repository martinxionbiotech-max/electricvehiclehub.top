# ChinaEVMart Phase 4b — 车型详情页 + 品牌页模板重建

> 仓库：`electricvehiclehub.top`（chinaevmart.com 代码库）
> 阶段：Phase 4-C 车型详情 / 4-D 品牌页
> 日期：2026-10-22 · 单一数据源 = `src/content/vehicles/*.md` + `src/content/brands/*.md`
> 校验：`npm run validate:data` → **0 issues** · `npm run build` → **899 pages, exit 0** · sitemap **700 URL 不变**

---

## 0. 结论摘要

| 维度 | 结果 |
|---|---|
| 车型详情页 | 十要素全落实，移除纯复述规格的冗余段落（Entity Snapshot / 40HQ / 扁平规格大表 / 正文 Overview） |
| C 层紧凑档案 | 数据贫乏车型用紧凑档案（去竞品对比、去 trim、去冗余分组），与质量分层 C 层标注联动 |
| 品牌页 | 集团/品牌/子品牌关系表 + 动力形式分布 + 车系分组，全数据驱动 |
| 品牌正文 | 72 篇剥离 landed-cost 残留（213 行）+ 冗余「Brand Overview / At a Glance / Explore」段落 |
| 公开计数 | 车型/品牌/动力/车系全部从规范化数据集实时推导 |

---

## 1. 车型详情页十要素落实清单（4-C）

| # | 要素 | 实现 | 证据 |
|---|---|---|---|
| ① | 车型身份（年款/trim/市场/动力形式） | 标题下方徽章（type/powertrain/brand）+ 副文「{powertrain} · {powertrainLabel} · {type} · Trims · Family」；`model_year` 无值标 N/A（P3 新增字段，当前 0 填充） | `[slug].astro` identity 区 |
| ② | 简洁事实摘要（零编造） | `## Summary` 段落：仅从 frontmatter 字段生成，缺失字段明说「not recorded」，不估算 | Summary section |
| ③ | 规格分组（尺寸/性能/电池/充电/续航） | 四组 `Specifications` 子表（Dimensions & weight / Performance / Battery / Charging），仅渲染有值字段 | specs 对象 + 四组 table |
| ④ | 续航测试标准标签 + trim 适用性 | `## Range by test standard` 独立表，CLTC / CLTC(long) / WLTP / EPA / NEDC 分字段分列，注明「CLTC 高于 WLTP/EPA」「trim 差异仅记录单一标准代表值」 | rangeStandards |
| ⑤ | 价格类型/币种/市场/日期/来源 | `## Price` 表：price_type（ex-factory 口径显式）、amount、currency、market（China domestic，由 price_type 推导非臆断）、data as of、source | price 表 |
| ⑥ | trim 间实质差异（有 trim 数据的车型） | 81 款有 trim 数据 → `## Versions / trims` 列表 + 明示「per-trim spec breakdown not available」不编造差异 | trimParts / hasTrimVariants |
| ⑦ | 竞品对比（兼容规格） | `## Comparable {type} {powertrain}s`：同车身类型 + 同动力形式、按 ex-factory 价格差最近的 4 款，列价格/CLTC 续航/电池 | competitors |
| ⑧ | 出口考虑（已核验的才写） | 仅 HS code（含 powertrain 回退）+ certification notes；landed-cost/关税/分市场数据外链 .net 出口指南 | Export considerations |
| ⑨ | 来源/最近核查日/未解决字段 | `## Data provenance & verification`：source / last checked / verification status / tier；`Not yet recorded` 列出缺失字段清单 | provenance + unresolved |
| ⑩ | 内链（品牌/相关车型/对比/技术/指南） | `## Explore further`：品牌页 / 车型目录 / 对比文章（`/blog/tag/comparison/`）/ 技术词表（`/docs/glossary/`）+ 同品牌 + 同车系车型列表 | Explore further |

### 1.1 移除的纯复述规格冗余段落（P1 假设⑤「Overview 同构句残留」处置）

| 移除项 | 位置 | 状态 |
|---|---|---|
| 正文 `## Overview` 同构句段落（517 篇） | 车型页不再渲染 markdown 正文 | 已移除渲染（`<Content />` 移除，改为模板生成 Summary） |
| 「Entity Snapshot」规格复述段+表 | `[slug].astro` | 删除 |
| 「Powertrain」独立表（与 Specifications 重复） | `[slug].astro` | 合并入 Performance 组 |
| 「Dimensions & Logistics」40HQ 装箱估算 | `[slug].astro` | 删除（估算非已核验数据，违反「已核验的才写」） |
| 「Technology」独立表 | `[slug].astro` | 合并入 Battery/Charging 组 |
| 「Market Compliance」区 | `[slug].astro` | 收敛为 Export considerations（仅 HS + 认证） |
| 扁平 63 字段「Specifications」大表 | `[slug].astro` | 删除，改为四分组子表 |
| 「Data Sources」双卡冗余区 | `[slug].astro` | 收敛为 provenance 单表 |

**验证**：`dist/vehicles/*/index.html` 全量扫描 0 命中「Entity Snapshot / Dimensions & Logistics / Market Compliance / 40HQ / Overview」。

### 1.2 C 层紧凑档案表现

- 触发条件：`quality_tier === 'C'`（31 款）。
- 表现：显示琥珀色「Data status: partial — compact record」横幅；**抑制竞品对比区**（数据贫乏不硬凑对比）；有 trim 数据才渲染 Versions；规格组仅渲染有值字段。
- 验证：`forthing-xinghai-v6-plus`（C 层）无「Comparable」区、有 compact 横幅；`byd-seal`（A 层）正常渲染竞品对比 + Versions。
- 与质量分层联动：provenance 表同时显示 tier 与 data_tier。

---

## 2. 品牌页字段驱动情况（4-D）

### 2.1 集团/品牌/子品牌关系区分（P3 数据驱动）

| 字段 | 呈现 | 示例 |
|---|---|---|
| `brand_name` | Brand 行 | BYD / AION / Zeekr |
| `parent_manufacturer` | Manufacturer group 行 | GAC / Geely |
| 关系判定（brand ≠ group，大小写归一） | Relationship 行 | `AION is a brand of the GAC group` |
| 关系判定（brand = group） | Relationship 行 | `BYD is the brand name of the BYD group` |
| `parent_location` / `parent_founded` / `established` | 总部 / 集团成立 / 品牌成立 | — |

- 子品牌判定逻辑：`group.toLowerCase() !== brand_name.toLowerCase()` → 子品牌。
- 验证：aion →「AION is a brand of the GAC group」；zeekr →「Zeekr is a brand of the Geely group」；byd →「BYD is the brand name of the BYD group」。

### 2.2 车型与动力形式按规范化数据集展示

- `## Powertrain lineup`：按 `POWERTRAIN_ORDER` 枚举顺序，仅呈现该品牌存在的动力形式，含 `powertrainLabel` 全称 + 计数（实时推导）。
- `## Model families`：按 vehicle `family` 字段分组（排除「Ungrouped」伪车系），列出每车系车型 + type/powertrain。
- `## {brand} models (N)`：全部车型卡，type · powertrain · CLTC 续航 · **ex-factory 价格**（口径显式）。
- **移除 landed-cost 残留**：品牌页车型卡原「Landed DE $X (+N%)」已删除，不再渲染 `landed_cost` / `landed_cost_markets`。

### 2.3 有源品牌背景（有据才写）

- 72 篇品牌正文剥离「Brand Overview」（复述 frontmatter）、「Brand at a Glance」（含 Landed cost / Landed premium 残留）、「Explore（Calculate landed cost 链接）」。
- 仅保留**首段有源品牌背景**（如 BYD 成立历史、AION 归属 GAC），删去 213 行 landed-cost 残留。
- **不编造**：海外布局/出口就绪/销量/制造关系均不新增——原本残留的「Landed cost (Germany)」「Landed premium」全部清除。

---

## 3. 冗余段落清理数

| 项 | 数量 |
|---|---|
| 车型详情页冗余段落/表（Entity Snapshot、40HQ、扁平大表、Technology、Market Compliance、双卡 Data Sources） | 6 类区块 × 517 页渲染移除 |
| 车型正文 `## Overview` 同构句 | 517 篇（不再渲染，模板生成 Summary 取代） |
| 品牌正文「Brand Overview / At a Glance / Explore」段落 | 72 篇 × 3 节 |
| 品牌正文 landed-cost 残留行 | **213 行** |

---

## 4. 验证结果

| 检查 | 结果 |
|---|---|
| `npm run validate:data` | ✅ 0 issues（72 brands / 517 vehicles / 双向关系） |
| `npm run build` | ✅ 899 pages, exit 0 |
| 车型 5 篇抽检（A 层 3 + C 层 2） | ✅ byd-seal / aeolus-e70 / zeekr-7x（A 层）+ forthing-xinghai-v6-plus / aion-v-plus（C 层紧凑） |
| 品牌 3 页抽检 | ✅ byd（46 models）/ aion（13，子品牌）/ zeekr（9，子品牌），0 landed-cost 残留 |
| 规格复述残留扫描 | ✅ 0 命中（Entity Snapshot / Dimensions & Logistics / Market Compliance / 40HQ / Overview） |
| sitemap | ✅ 700 URL 不变 |

---

## 5. 新增/修改文件

| 文件 | 变更 |
|---|---|
| `src/pages/vehicles/[slug].astro` | **重建**：十要素 + 四分组规格表 + 续航标准表 + C 层紧凑档案 + 移除 6 类冗余区块 |
| `src/pages/brands/[slug].astro` | **重建**：集团/品牌/子品牌关系表 + 动力分布 + 车系分组 + 移除 landed-cost 卡片 |
| `src/content/brands/*.md` | 72 篇剥离 landed-cost 残留 + 冗余段落，仅保留首段有源背景 |

---

## 6. 分离声明

- **已完成（已验证）**：车型详情页十要素、冗余段落清理、C 层紧凑档案、品牌页关系区分/动力分布/车系分组、品牌正文 landed-cost 剥离。均有文件/行号 + 渲染抽检证据。
- **未覆盖**：`model_year` 仍 0 填充（P3 字段，待人工补数据）；`.md` 机器可读变体 / `data/vehicles.json.ts` 端点的 landed-cost 字段残留（属 Phase 5 决策）；线上逐页 HTTP 抓取；价格/税率权威溯源（待人工）。
- **顺延**：`data_reviewed: false` 517/517、`verification_status` 几乎全 None（P1-8，Phase 3 复核流水线）。

---

*报告路径：`docs/chinaevmart-p4b-detail-brand.md`*
