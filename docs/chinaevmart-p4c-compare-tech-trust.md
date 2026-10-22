# ChinaEVMart Phase 4c — 对比页 + 技术页 + 信任页重建

> 仓库：`electricvehiclehub.top`（chinaevmart.com 代码库）
> 阶段：Phase 4-E 对比 / 4-F 技术 / 4-G 信任页（About / Methodology / Trust）
> 日期：2026-10-22 · 单一数据源 = `src/content/vehicles/*.md`（517）+ `src/content/brands/*.md`（72）
> 校验：`npm run validate:data` → **0 issues** · `npm run build` → **899 pages, exit 0** · sitemap **700 URL 不变**

---

## 0. 结论摘要

| 维度 | 结果 |
|---|---|
| 对比页（4-E） | 对比 = 31 篇手工精选 `*-vs-*.md` 博客 + 目录内嵌 Comparable 区，**无 /compare/ URL 矩阵、无自动生成海量对比 URL**；对比标准固化进 Methodology |
| 技术页（4-F） | 确立**四层分离标注机制**（Fact / Manufacturer claim / Editorial interpretation / Estimate），glossary 技术+续航术语逐条标注 + 权威标准引用（GB/T、IEC、UNECE） |
| 信任页（4-G） | About 重写（信息平台非卖家如实声明 + 做什么/不做什么）；Methodology 深化（数据来源/更新频率/纠错流程/价格五类口径/续航标准/编辑审查/成本假设——本仓无计算器故省略计算器假设）；contact FAQ 去除「代找车源/landed-cost 情报」越权表述 |
| 作者/验证陈述 | 沿用既有真实作者体系（Wei Wang + Chengguang Energy），**0 新增虚构人员**；作者页/编辑独立页本就真实可审计，本批不改动 |
| 计数对账 | 517 车型 / 72 品牌 / 动力分列 均实时推导，无硬编码 |

---

## 1. 对比页口径（4-E）

### 1.1 现状判定（不扩 URL 矩阵）

对比内容已存在于**手工精选的博客条目**（31 篇 `*-vs-*.md`）与车型详情页的 `Comparable {type} {powertrain}s` 内嵌区（P4b 已建）。本仓**没有 `/compare/` 工具页、没有对比 URL 矩阵**，因此 4-E 的「不自动生成海量对比 URL」天然满足——本批**未新增任何对比路由**。

### 1.2 对比标准（固化进 Methodology「Comparison standards」节）

| 规则 | 呈现 |
|---|---|
| 仅对比可比口径 | 同价格口径 / 同续航标准，或显式标注不同 trim/年款/市场/测试周期 |
| 差异显式标注 | 两车在 trim/市场/测试标准上不同时，标出差异而非静默等同 |
| 重要数字带来源与日期 | 每篇对比 Sources 段 + accessed 日期 |
| 解释实质差异/权衡/未知 | TL;DR + Reasoning 段落解释价差来源、税率放大、未知项标 UNKNOWN |
| 不自动生成 URL | 对比条目手工精选，无模板化 URL 批量产出 |

- 抽检证据：`byd-seal-vs-tesla-model-3`（Sources 3 / accessed 1 / countervailing 9 / Germany 14）、`cltc-vs-wltp-range`（CLTC 24 / WLTP 25 / Sources 2 / rule-of-thumb 5），均带来源+日期+实质差异解释。

---

## 2. 技术页四层分离机制（4-F）

### 2.1 机制定义（确立于 Methodology + glossary）

在 `methodology.astro` 新增「Four layers of a statement」节，确立全站四层标注约定：

| 层 | 含义 | 呈现 |
|---|---|---|
| **Fact** | 可溯源至一级来源（法规/官方规格/型式核准库）的既定事实 | 携带来源引用 |
| **Manufacturer claim** | 厂商宣称、本平台未独立复测 | 归属厂商，不作本平台发现 |
| **Editorial interpretation** | 本平台分析判断（语境/权衡/解读） | 以判断口吻陈述 |
| **Estimate** | 由文档化公式/行业基准推导的估算值 | 显式标为估算 + 依据 |

### 2.2 落地到 glossary（渲染层技术实体）

`glossary.md` 新增「How to read this glossary」图例，并对**续航标准**与**技术术语**逐条标注：

| 术语 | 标注 | 权威引用 |
|---|---|---|
| CLTC / WLTP / NEDC | Fact（15–30% 差距为 editorial estimate） | GB/T 38146 · UNECE GTR No.15 · UNECE R101 |
| Battery chemistry | Fact（化学事实）+ 逐车从厂商数据记录 | — |
| Motor type（PMSM 主导） | Editorial interpretation（行业规律非测量断言） | — |
| Charging interface | Fact | GB/T 20234（中国）· IEC 62196 / CCS2（欧盟） |
| Battery thermal management | Editorial interpretation | — |
| Heat pump | Fact（机理）+ 逐车 fitment 来自厂商数据 | — |
| Drag coefficient（Seal Cd 0.219） | Fact（厂商公布值）+「among the lowest」为 editorial | — |

### 2.3 数据溯源交叉引用

`data-provenance.md` 新增「Statement-layer convention」节，把四层标注与既有 source-type / confidence / verified_date 溯源体系挂钩，指向 Methodology 与 glossary。

---

## 3. 信任页清单（4-G）

### 3.1 About（重写 `about.astro`）

| 区块 | 前 | 后 |
|---|---|---|
| H1 | 「The complete product database for Chinese EVs」 | 「An independent platform for Chinese EV data」（去「complete」无支撑最高级） |
| description | 「deep, source-verified specifications」 | 「information platform… not a seller, importer, or broker」 |
| 价值观「Verified Data」 | 「Every spec is cross-checked against manufacturer datasheets and authoritative sources」 | 「Provenance over assertion」——来源类型+更新日期，无法核实标 not recorded |
| 价值观「Compliance by Default」 | 「HS code…certification facts folded into every record」 | 「Honest about limits」——如实声明边界 |
| 新增「What this platform does not do」 | 无 | 不卖车/非经销商/非进口商/非报关行/非采购代理；不提供报价/成交价/库存/代找车源；不跑测试；不编造资质/奖项/合作/客户 |
| 统计「1 Structured Record Format」 | 弱统计 | 「4 Range test standards tracked」 |

- 渲染验证：`dist/about/index.html` 0 命中「complete product database / source-verified / cross-checked against authoritative」；「What this platform does not do」+「not a seller」就位。

### 3.2 Methodology（深化 `methodology.astro`）

任务书要求的 7 项全覆盖（本仓无计算器，成本假设按实省略）：

| 项 | 状态 |
|---|---|
| 数据来源 | ✅ Source tiers 1–4（保留）+ 指向 data-provenance |
| 更新频率 | ✅ 「periodic，无固定周期，逐条带 data_updated / last-updated」 |
| 纠错流程 | ✅ 「material corrections recorded on page」+ 联系邮箱 |
| 价格定义（ex-factory reference 五类口径） | ✅ Official MSRP / China market reference / **China ex-factory reference** / FOB / Landed cost estimate 五类严格分离，默认 ex-factory 明示 |
| 续航标准 | ✅ CLTC / WLTP / EPA / NEDC 四标准，跨标准不混比 |
| 编辑审查 | ✅ 四段署名（written/reviewed/data-verified/last-updated）+ 同一人自审如实说明 |
| 成本假设 | ✅ **省略计算器假设**——明确「本平台不发布 landed-cost 计算器/落地价」，外链 .net 姐妹站 |
| 新增「Comparison standards」 | ✅ 承载 4-E 对比口径 |
| 新增「Four layers of a statement」 | ✅ 承载 4-F 四层分离机制 |

### 3.3 contact FAQ（修正越权表述）

| FAQ | 前 | 后 |
|---|---|---|
| Can you help me source…? | 「Yes. Send us…we will provide a transparent landed-cost breakdown」 | 「specification guidance only…不代购、不提供成交价/报价」 |
| Do you sell vehicles? | 「provide landed-cost intelligence and sourcing guidance」 | 「catalog and clarify product data…不卖车、不代找车源」 |

- 与 FAQ 页、style-guide §1.1 平台边界对齐；消除「代找车源/landed-cost 情报」两处越权表述。

### 3.4 作者/验证陈述审计

- **沿用既有真实作者体系**：作者 Wei Wang（EV & Battery Industry Analyst）、运营方 Chengguang Energy（Jinzhou Chengguang Power Source Co., Ltd.）——均为 `entity-graph.json` 既有实体，**本批 0 新增虚构人员/资质**。
- `authors.astro` / `editorial-independence.astro` 本就如实（同一人自审明说、无虚构编辑），本批未改动、无需改动。
- `entity-graph.json` 中「Aaron.W (Contact, Customer Service)」为既有联系人实体，非本批新增。

---

## 4. 验证结果

| 检查 | 结果 |
|---|---|
| `npm run validate:data` | ✅ 0 issues（72 brands / 517 vehicles / 双向关系） |
| `npm run build` | ✅ 899 pages, exit 0 |
| sitemap URL 数 | ✅ **700 不变**（无新增可索引 URL） |
| About 渲染 | ✅ 0 最高级残留；does/does-not 区就位 |
| Methodology 渲染 | ✅ 10 项任务书要求区全部命中 |
| glossary 四层图例 + 5 技术实体 | ✅ 图例 + Fact/Claim/Interpretation/Estimate 标签 + GB/T·IEC·UNECE 引用均渲染 |
| data-provenance 交叉引用 | ✅ Statement-layer convention 命中 2 处 |
| 对比抽检 2 组 | ✅ byd-seal-vs-tesla-model-3 / cltc-vs-wltp-range 均带 Sources+accessed+实质差异 |
| 技术 5 实体抽检 | ✅ Battery chemistry / Motor type / Charging interface / Heat pump / Drag coefficient |

---

## 5. 变更文件与 commit

| 文件 | 变更 |
|---|---|
| `src/pages/about.astro` | 重写：信息平台定位 + 做什么/不做什么 + 去「complete/source-verified」最高级 |
| `src/pages/methodology.astro` | 深化：四层分离 + 数据来源 + 更新频率 + 纠错 + 价格五类 + 续航标准 + 编辑审查 + 成本假设省略 + 对比标准 |
| `src/config/contact.ts` | FAQ 两处去「代找车源/landed-cost 情报」越权表述 |
| `src/content/docs/glossary.md` | 四层图例 + 续航/技术术语逐条标注 + 权威标准引用（GB/T 38146·20234、IEC 62196、UNECE GTR No.15/R101） |
| `src/content/docs/data-provenance.md` | 新增 Statement-layer convention 交叉引用节 |

**Commit（分步标记）**：

1. `9d9baaa` — `p4c-trust`: About + Methodology + contact FAQ 重建
2. `69023a4` — `p4c-tech`: 四层分离机制确立 + glossary 标注 + data-provenance 交叉引用

---

## 6. 分离声明

- **已完成（已验证）**：对比口径固化（无 URL 矩阵）、四层分离机制确立并落地 glossary、About/Methodology 重建、contact FAQ 越权修正。均有文件 + 渲染抽检证据，build exit 0，sitemap 700 不变。
- **未覆盖**：`technical-master.json`（137 实体）/`regulatory-master.json`（66 实体）仍为孤儿文件未渲染（属 Phase 2 实体层/Phase 6 决策）；`landed-cost-methodology.astro` 整页与 `markets/index.astro` 关税表仍存在于本仓（属 Phase 5 landed-cost 去留决策）；线上逐页 HTTP 抓取；价格/税率权威溯源（待人工）。
- **顺延**：`data_reviewed: false` 517/517、`verification_status` 几乎全 None（P1-8，Phase 3 复核流水线）；`model_year` 0 填充。

---

*报告路径：`docs/chinaevmart-p4c-compare-tech-trust.md`*
