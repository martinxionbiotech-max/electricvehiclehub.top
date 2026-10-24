# P1 成本审计报告（p1-cost-audit）

> 日期：2026-10-24 ｜ 仓：`electricvehiclehub.top`（chinaevmart.com · China EV Mart）
> 范围：本仓渲染的**成本数字/计算示例**盘点 + 来源声明 + EU 关税/VAT 复核 + 可复算公式留存。
> 背景：本仓已去计算器（301 → .net）；export-profile 区块引用 .net 数据；P5 已在 .net 仓完成三方对账（公式=文档=数据 · Reg 2024/2754 六档 CVD）。

---

## 1. 用户两项声明指令（本批落实）

| # | 指令 | 落地方式 |
|---|---|---|
| ① | 数据来源要备注和声明 | 统一「source + 日期」备注，渲染在数字旁 / 区块头 |
| ② | 计算方法要声明「仅作参考」 | 统一 `CostDisclaimer` 组件 + 文案「For reference only — planning estimate, not a quote / offer / legal-tax advice」；无来源估算数字标 estimate |

## 2. 成本数字位置盘点（本仓渲染面）

### 2.1 模板/组件驱动（一次改，全站生效）

| 位置 | 成本数字 | 来源备注 | 声明落地 |
|---|---|---|---|
| `src/pages/markets/index.astro`（市场页） | 30 市场关税/VAT + 品牌 CVD 表 | ✅ 已有 `tariffs.source` | ✅ 新增 `<CostDisclaimer>`（EU CVD + 各国税局，日期 2026-09-15） |
| `src/pages/landed-cost-methodology.astro`（方法页） | 公式 + CVD 六档表 + VAT 表 + 固定成本 | ✅ 已有 [Source: …] | ✅ 新增顶部 `<CostDisclaimer>` + VAT 范围修正 19–25% |
| `src/pages/vehicles/[slug].astro`（车型页 export-profile 区块） | 指向 .net 的落地成本引用 | ✅ 已有 | ✅ 新增「For reference only — planning estimate」小字 |
| `src/pages/vehicles/[slug].md.ts`（.md 变体） | Landed Cost by Market / Breakdown 表 | ✅ 已有 Sources & Last Updated | ✅ 新增两处 blockquote 声明 |

### 2.2 文档页（`src/content/docs/`）

| 文件 | 成本数字 | 来源备注 | 声明 |
|---|---|---|---|
| `landed-cost-methodology.md` | 公式 + CVD 六档 + 固定成本 | ✅ 已有 Source | ✅ 新增「For reference only」+ 日期 |
| `cost-breakdown-example.md` | BYD Seal 四市场逐项表 | ⚠️ 补充 | ✅ 新增顶部声明 + **修正 UAE/澳洲固定成本**（见 §3.2） |
| `regional-import-guides.md` | 30 市场表 | ✅ 已有「reference, not a quote」+ 日期 | ✅ 已达标 |
| `import-overview.md` | 流程 + CIF 口径 | ✅ 已有 | ✅ 新增「For reference only」 |
| `eu-import-guide.md`（draft） | CVD 表 | ⚠️ | ✅ 修正「~20.8%」→「20.7%」 |
| `introduction.md` / `faq.md` / `glossary.md` | 举例数字 | ✅ 已有「B2B estimate」等 | ✅ 已达标 |

### 2.3 分析文章 4 篇（`src/content/blog/`）

| 文件 | 成本数字 | 声明 |
|---|---|---|
| `budget-ev-landed-cost-advantage.md` | 3 车 × 5 市场落地价 | ✅ 末句改为「For reference only —」 |
| `five-market-landed-cost-basket.md` | 10 车 × 5 市场矩阵 | ✅ 同上 |
| `eu-cvd-four-tier-same-price.md` | CVD 四档隔离计算 | ✅ 同上 |
| `australia-suv-import-guide.md` | 4 SUV 落地价 | ✅ 同上 |

### 2.4 其余博客（import-guide / comparison 长尾，75 篇渲染成本数字）

- 75 篇含 `$` 成本数字；其中 **54 篇**已含「last verified / data date / For reference / B2B estimate / not legal-tax advice」之一。
- 剩余 21 篇属历史 import-guide / comparison 长尾，多数有分散来源注（`Source:` 行）但未统一到「For reference only」句式 → 列 **§5 待人工清单**（非本批阻断项，数字来源仍在文中）。

## 3. EU 关税/VAT 复核结论

### 3.1 税率 vs Reg 2024/2754 现行规则

| 项目 | 本仓字段 | 复核结论 |
|---|---|---|
| 标准关税 | 10% MFN（EU BEV） | ✅ 与 TARIC 一致 |
| CVD 六档 | BYD 17.0 / Geely 18.8 / SAIC 35.3 / Tesla 7.8 / other-coop 20.7 / non-coop 35.3 | ✅ `cvd_meta.verification_status = consistent_with_definitive_rates`（复核 2026-10-23） |
| 品牌映射 | `brand_cvd` 19 键 | ✅ 与 `.net` 逐键一致 |
| VAT 分国 | DE 19 / FR 20 / NL 21 / SE·DK 25 / UK 20 / … | ✅ 与各国税法一致；方法页范围标题 19–23% → 修正 19–25% |
| 计税基础 | base（出厂价，非 CIF） | ✅ 文档已披露「保守简化」 |
| 适用范围 | CVD 仅 EU + BEV | ✅ 文档/数据一致 |

### 3.2 本仓侧字段 vs .net 一致性（抽核 10 款）

- `tariffs.json` `brand_cvd` / `markets`：与 `.net` **完全一致（0 差异）**。
- 10 款车型（byd-seal / byd-dolphin / mg-4 / xiaomi-su7 / zeekr-001 / xpeng-g6 / onvo-l60 / byd-atto-3 / yangwang-u8 / nio-et5）frontmatter `landed_cost` + `landed_cost_markets`：**与 .net 完全一致（10/10 = 0 差异）**。

### 3.3 本批修正（误导措辞 / 数据）

| # | 文件 | 修正 |
|---|---|---|
| F1 | `cost-breakdown-example.md` | UAE 固定成本 `~$6,250` → `$4,150` + 注册 `$300`；澳洲 `~$6,250` → `$5,350` + 注册 `$500`；「hover around $6,000–$6,250」→「$4,450 (UAE) to $6,600 (Germany)」 |
| F2 | `markets/index.astro` | CVD 列「Brand-specific (17–35.3%)」→「(7.8–35.3%)」（含 Tesla 7.8%） |
| F3 | `landed-cost-methodology.astro` | VAT 标题「19% to 23%」→「19% to 25%」 |
| F4 | 4 处博客 + 1 处 draft 文档 | 「~20.8%」→「20.7%」（对齐数据源 `_default=0.207`） |

## 4. 可复算公式留存

- 新增 `docs/cost-model-formulas.md`：核心公式、输入参数（税率/固定成本/区域固定）、抽核市场、BYD Seal 复算示例、口径披露、与 .net 方法论一致性。与 `.net` `landed-cost-methodology` 一致。

## 5. 待人工清单（不可核验项，未当已确认事实）

| # | 项目 | 动作 |
|---|---|---|
| H1 | 21 篇长尾博客未统一「For reference only」句式 | 补统一声明（数字来源仍在文中，非错误） |
| H2 | 非欧关税逐市场溯源（Turkey 40% / Indonesia 50% / Singapore 20% / Brazil 35% / Mexico 50% 等） | 逐市场权威复核 |
| H3 | 30 市场注册费出处（丹麦 3500 / 挪威 1400 / 以色列 700 等） | 补 source-master 逐市场条目 |
| H4 | `REGION_BASE_FIXED` 三处副本未入中心表 | 并入 `tariffs.json` |
| H5 | 本地特有税未建模（SCT / ARF+COE / PPnBM / IPI+ICMS） | 决策是否建模或持续披露排除 |
| H6 | `brand_cvd` 无显式 non-cooperating 35.3% 桶（`_default=20.7` 为 other-cooperating） | 补映射 |
| H7 | D1 口径升级（base → CIF 应税基数） | 保持 base + 披露（建议） |

## 6. 收尾

- build 出口 0、抽 3 页成本声明渲染验证、commit（`p1-cost-audit-*`）、push、同步 `0 0`。
- 回滚：`git revert <commit>`（纯文案 + 新增组件 + 文档，无数据/公式改动）。
