# China EV Mart — P2 持续数据质量门槛（收官批）

> 仓库：`electricvehiclehub.top`（chinaevmart.com 代码库）
> 批次：five-06 · 日期：2026-10-24
> 前序：five-01 数据核验系统 / five-05 发布门槛
> 纪律：零编造 · 未知/未核验数值一律 **N/A 或 待核验** · 冲突只标记不自动填补

---

## 0. 结论摘要

| 维度 | 结果 |
|---|---|
| 发布前质量门槛 | `npm run gate`（`scripts/pre-publish-gate.mjs`）——7 项检查 + 高风险字段人工审核，产出 `docs/pre-publish-checklist.md` |
| 数据校验扩展 | `validate:data` 新增 4 项（trim/版本、单位枚举、测试标准、来源/日期） |
| 索引门槛扩展 | `quality:gate` 新增 3 项（conflict 拦截、canonical 域、结构化数据虚构字段） |
| 高风险字段清单 | 价格 / 续航 / 认证 / HS Code（影响采购决策） |
| gate 基线（517 车） | **PASS 500 / BLOCK 17 / warn-only 76 / clean 424** |
| 待人工清单规模 | conflict 16（未解决 10 + 已标注 6）· 高风险字段待核验 **237** |
| 未知值拦截 | 脚本层拦截：`unverified`/缺来源值不得静默填充（0 例缺来源通过） |

> 关键纪律已落地：**参数单位由字段名承载（kg/kWh/mm/kW/Nm），数值必须是裸数字；续航必须归属 CLTC/WLTP/EPA/NEDC 之一；任何 conflict 与 unverified 值只标记、绝不静默填充。**

---

## 1. 发布前质量门槛（`npm run gate`）

### 1.1 入口与产物

- 脚本：`scripts/pre-publish-gate.mjs`
- 入口：`npm run gate`（package.json 新增）
- 产物：`docs/pre-publish-checklist.md`（发布前检查单，自动生成）
- 退出码：`0` = 通过；`1` = 存在阻断项（发布前必须解决或显式标注「已知/待人工」）
- 单一真源：读 `src/content/vehicles/*.md` frontmatter（**不读** 陈旧的 `src/data/*-master.json` 快照）

### 1.2 七项检查

| # | 检查 | 判定（block = 阻断发布，warn = 可发布但待复核） |
|---|---|---|
| ① | 车型版本 / trim 一致性 | trim 有值必须可定位年款（缺 model_year → warn）；trim 不得横跨与 `powertrain` 字段矛盾的动力形式（block） |
| ② | 参数单位规范 | 数值字段必须为裸数字，单位由字段名承载（kg/kWh/mm/kW/Nm 枚举）；未知数值字段告警 |
| ③ | 测试标准标注 | 续航值必须归属 CLTC/WLTP/EPA/NEDC；`range_long_km` 无标准字段 → block |
| ④ | 来源与价格日期 | `data_source` + `data_updated` 必填；`data_updated` 须 YYYY-MM-DD 且非未来 |
| ⑤ | conflict 拦截 | `parameter-verification.json` 的 `conflict` 必须人工处理或带 note 明确标注（无 note → block） |
| ⑥ | canonical 域 | 四处 canonical 来源统一为 `https://chinaevmart.com` |
| ⑦ | 结构化数据 | JSON-LD 无虚构字段（rating/review/award/sku/mpn 等一律禁止） |
| ⑧ | 高风险字段人工审核 | 价格/续航/认证/HS Code：有值必须带来源+日期+核验状态；否则 N/A（缺来源 → block） |

### 1.3 与既有脚本的关系

| 脚本 | 入口 | 职责 | 本批改动 |
|---|---|---|---|
| `validate-data.mjs` | `npm run validate:data` | 数据层校验（frontmatter 真源） | **新增 ①-④** |
| `quality-gate.mjs` | `npm run quality:gate` | 索引化五门槛 + 报告 | **新增 ⑤-⑦** |
| `pre-publish-gate.mjs` | `npm run gate` | 发布前总门槛（7 项 + 高风险审核） | **新增** |

---

## 2. 高风险字段清单与人工审核机制

### 2.1 高风险字段（影响采购决策，发布前必须人工审核）

| 字段 | 类别 | 采购影响 | 未知值处置 |
|---|---|---|---|
| `price_usd` / `price_type` / `currency` | 价格 | 直接影响报价与预算 | 缺来源/日期 → N/A；未核验 → 待核验 |
| `range_cltc_km` / `range_wltp_km` / `range_epa_km` / `range_nedc_km` / `range_long_km` | 续航 | 影响选型与续驶预期 | 未核验 → 待核验；标准不明 → 阻断 |
| `certification_notes` | 认证 | 影响清关与准入 | 缺来源 → N/A |
| `hs_code` | HS Code | 影响关税归类与到岸成本 | 缺来源 → N/A |

### 2.2 审核流程（按站点现有人员体系如实写）

站点为**小规模独立出版**，作者与审核为同一人，且如实披露（不虚构第二审核人）。现有署名体系见 `/authors` 与 `/editorial-independence`：

- **作者 / 审核人**：Wei Wang（EV & Battery Industry Analyst）——撰写并审核数据记录与贸易文章，署名即责任人。
- **数据库维护方**：Chengguang Energy（Jinzhou Chengguang Power Source Co., Ltd.）——负责车型记录规范化、来源元数据、核验状态、更新日期。
- **商业隔离**：无商业伙伴审核、批准或编辑内容。

**审核路径**：

1. **录入**：记录由公开来源（厂商规格页 / 型式核准库 / 行业记录）编制，逐字段带 `data_source` + `data_updated` + `verification_status`。
2. **自审**：发布前跑 `npm run gate`——作者本人核对 check ①-⑧ 的阻断项与告警项。
3. **冲突升级**：`conflict` 状态（字段↔正文/两源矛盾）**只标记不改值**，在 `parameter-verification.json` 加 `note` 说明分歧点，列入待人工清单；无法从公开源定论的，标注 `unverifiable`（待核验），**不猜测、不填补**。
4. **未知值**：无来源依据的字段一律 **N/A 或 待核验**；脚本层拦截 AI 自动填充路径——`unverified` 值不得以任何值静默填充（校验规则在 §1.2 ⑧ 与 `pre-publish-gate.mjs`）。
5. **发布**：gate 退出码 0 才可发布；有阻断项时，要么人工解决，要么在记录中显式标注「已知/待人工」后以 warn 状态发布。

### 2.3 冲突升级明细（基线，16 单元）

- **未解决（10，阻断）**：`denza-z9-gt-dm-i.type`、`denza-n8l.range`、`ora-lightning-cat.range`、`ora-lightning-cat.battery`、`zeekr-007-gt.type`、`geometry-a.battery`、`geometry-a.motor`、`lynk-co-07.motor`、`aion-lx-plus.range`、`avatr-06t.type`——发布前必须补 `note` 或人工对账。
- **已标注（6，待人工）**：`hongqi-guoya.motor`、`yangwang-u8l.range/battery`、`nio-et9.battery/type`、`maextro-s800.battery`——已带 note，仍待人工复核。

---

## 3. gate 基线（517 车，2026-10-24 实测）

```
=== China EV Mart Pre-publish Gate (P2) ===
vehicles: 517
PASS: 500 | BLOCK: 17 | warn-only: 76 | clean: 424
blocking issues: 19 | warnings: 324
待人工: conflict=16 (unresolved=10) high-risk-unverified=237 high-risk-no-source=0
→ docs/pre-publish-checklist.md written
```

| 指标 | 数值 | 说明 |
|---|---|---|
| 车型总数 | 517 | 全量 frontmatter |
| PASS（零阻断） | 500 | 可直接发布 |
| BLOCK（≥1 阻断） | 17 | = 4 trim/powertrain 矛盾 + 5 range 标准不明 + 8 conflict 未解决车 |
| warn-only | 76 | 有告警但无阻断（trim 未定年款等） |
| clean | 424 | 零阻断零告警 |
| 阻断项合计 | 19 | 4 + 5 + 10 |
| 告警项合计 | 324 | 81 trim-unpinned + 6 conflict-documented + 237 high-risk-unverified |

**待人工清单规模**：conflict 16 单元（10 未解决 + 6 已标注）· 高风险字段待核验 237 项 · 缺来源高风险字段 0 项。

---

## 4. 变更清单（commit `five-06-*`）

| 文件 | 变更 |
|---|---|
| `scripts/pre-publish-gate.mjs` | **新增**：发布前总门槛（7 项检查 + 高风险审核 + 检查单生成） |
| `scripts/validate-data.mjs` | **扩展**：① trim/版本 ② 单位枚举 ③ 测试标准 ④ 来源/日期 |
| `scripts/quality-gate.mjs` | **扩展**：⑤ conflict 拦截 ⑥ canonical 域 ⑦ 结构化数据虚构字段 |
| `package.json` | 新增 `gate` 脚本入口 |
| `docs/pre-publish-checklist.md` | **生成**：发布前检查单（gate 自动产出） |
| `docs/p2-quality-gate.md` | **新增**：本文档 |

---

## 5. 分离声明

- **已完成**：发布前质量门槛（`npm run gate` + 检查单）、高风险字段清单与审核流程、未知值脚本拦截、gate 基线（517 车 pass/fail + 待人工规模）。
- **未覆盖**：17 台阻断车与 10 个未解决 conflict 的实际人工对账（需逐条 web 核验，后续批次）；237 项高风险字段待核验的逐条补齐。

---

*报告路径：`docs/p2-quality-gate.md` · five-06*
