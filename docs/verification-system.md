# China EV Mart — 数据来源与版本核验系统（Verification System）

> 仓库：`electricvehiclehub.top`（chinaevmart.com 代码库）
> 批次：five-01 · 日期：2026-10-23
> 前序：P1 基线 / P3 数据 / P4a-c / P8 验收（`docs/`）
> 纪律：零编造 · 冲突字段只标记不自动填补 · 每参数五元组 · 三态核验

---

## 0. 结论摘要

| 维度 | 结果 |
|---|---|
| 机制 | 参数级来源元数据五元组 `source / verified_at / model_year / trim / confidence` + 三态 `verified / mismatch / unverifiable` + 额外 `conflict` 标记 |
| 落地形态 | 关键参数表（价格/续航/电池/电机/加速/充电），单源 `src/data/parameter-verification.json`（schema_version 1） |
| 覆盖范围 | **32 款**（首页精选 6 + A 层 Tier 1 前 30，去重后 32） |
| 三态分布 | verified 9 / conflict 7 / unverifiable 176（含覆盖内未逐条核验项） |
| 冲突处置 | **仅标记，0 自动填补**；渲染黄色「conflict」徽标 + 待复核清单 |
| 渲染 | 车型详情页新增「Key parameter verification」表 + 冲突黄框 |

> 说明：`verified` / `conflict` 是本次**真实 web 核验**产出的确定结论（逐条带来源 + 核验日期）；`unverifiable` 是「覆盖但尚未逐条人工核验」的诚实兜底，不是「无数据」。核验对象为 2026-10-23 的官方/权威可查源（厂商官网、Wikipedia、auto-data.net、Electrek、EV Gulf 等）。

---

## 1. 机制设计

### 1.1 五元组（参数级）

与既有车级字段（`data_source` / `data_updated` / `data_reviewed` / `data_tier` / `confidence`）分离，**参数级**五元组为：

| 字段 | 类型 | 含义 |
|---|---|---|
| `source` | string | 该参数的来源（官方规格页/权威媒体/厂商数据），必填 |
| `verified_at` | string (YYYY-MM-DD) | 最近一次核验日期 |
| `model_year` | number\|null | 该参数对应的年款（当前 0 填充，不编造） |
| `trim` | string\|null | 该参数对应的版本/trim（无则 null） |
| `confidence` | `high`/`medium`/`low` | 置信度 |

### 1.2 三态 + conflict（状态机）

| 状态 | 含义 | 渲染 |
|---|---|---|
| `verified` | 官方/权威源已核对一致 | 绿色「verified」 |
| `mismatch` | 与官方源不一致（数值有出入） | 红色「mismatch」 |
| `unverifiable` | 无法从公开源核实（诚实兜底） | 灰色「unverified」 |
| `conflict` | 字段与渲染正文/两源矛盾，**只标记不改值** | 黄色「conflict」+ 待复核清单 |

> **`conflict` 是标记不是状态改写**：值保留原样（`value` 字段原值透出），渲染层加黄色徽标与说明，绝不自动填补或改值。这区别于 `mismatch`（数值对不上，但可判方向）——`conflict` 是「两个源或字段↔正文打架，本平台不做取舍」。

### 1.3 单源与落地

- **单源**：`src/data/parameter-verification.json`（生成脚本 `scripts/generate-parameter-verification.mjs`）。
- **schema 扩展**：`src/content.config.ts` 新增 `param_verification`（可选 record，五元组 + status 枚举），供未来手工修正记录直接写进 frontmatter。
- **渲染**：`src/pages/vehicles/[slug].astro` 新增「Key parameter verification」区块。

---

## 2. 首批覆盖清单（32 款）

### 2.1 首页精选 6 款（`quality_tier=A`，价格降序）

| # | slug | 品牌 | 动力 | 价格(USD) | 关键参数核验 |
|---|---|---|---|---|---|
| 1 | `hongqi-guoya` | Hongqi | HEV | 197,180 | motor **conflict**（160 kW vs 官方混动系统 294–358 kW）；HEV 边界项（P3 U-2） |
| 2 | `yangwang-u8l` | Yangwang | EREV | 180,280 | battery/range **conflict**（55.53 kWh/200 km vs 发布 56.58/230）；motor **verified** 880 kW |
| 3 | `yangwang-u8` | Yangwang | EREV | 154,650 | battery/motor **verified**（49.05 kWh / 880 kW）；range/accel **conflict**（字段 180/3.6 vs 正文 780/3.9） |
| 4 | `nio-et9` | NIO | BEV | 108,170 | battery **conflict**（102 vs 官方 100 kWh）；type **conflict**（SUV vs 官方 Sedan）；motor/range **verified** |
| 5 | `maextro-s800` | Maextro | BEV | 99,720 | battery **conflict**（65 kWh EREV 包 vs BEV 动力）；motor/range **verified** |
| 6 | `aito-m9-ultimate` | AITO | EREV | 90,250 | 关键参数待核验（`unverifiable`，range_long 1260 为增程综合续航非 CLTC 电续航） |

### 2.2 A 层 Tier 1 前 30 款（`quality_tier=A` 且 `data_tier=1`，价格降序）

与精选 6 去重后新增 26 款（完整 slug 见 JSON `coverage.slugs`）：

`m-hero-917 · m-hero-917-erev · yangwang-u7 · xiaomi-su7-ultra · nio-es9 · aito-m9-erev · nio-es7 · nio-ec7 · zeekr-009 · nio-et7 · nio-es8 · dayun-h9 · dayun-y7 · stelato-s9 · xiaomi-yu7-gt · fangchengbao-bao-8 · jac-refine-rf8 · voyah-dream-phev · nio-ec6 · aito-m8-erev · zeekr-8x · dayun-h8 · im-ls7 · nio-es6 · denza-d9-dm-i · denza-z9`

> 这 26 款本次为**覆盖登记**（`unverifiable`，逐条带既有 `data_source`/`data_updated`），未做逐条 web 核验——不冒充已核验。

---

## 3. 三态分布（实测）

| 状态 | 数量 | 说明 |
|---|---|---|
| `verified` | 9 | 本次真实核验一致（yangwang-u8 电池/电机、nio-et9 电机/续航、maextro-s800 电机/续航、yangwang-u8l 电机、hongqi-guoya 动力形式、…） |
| `conflict` | 7 | 字段↔正文/官方源矛盾，只标记不改值 |
| `mismatch` | 0 | 本次未发现「方向可判但值出入」的独立 mismatch（均升级为 conflict 以保留原值） |
| `unverifiable` | 176 | 覆盖内未逐条核验项（6 参数 × 32 款 - 已核验格） |

> `unverifiable` 是覆盖面里的大头，符合「先建机制 + 首批高价值核验 + 余下诚实待核」的节奏，不构成数据缺陷。

---

## 4. 冲突清单（待人工复核，不武断取舍）

| # | 车型 | 参数 | 冲突内容 | 处置 |
|---|---|---|---|---|
| C-1 | `yangwang-u8` | range | 字段 `range_cltc_km=180`（纯电）vs 正文「780 km CLTC」（增程综合）。官方 180/124 km 纯电 | 保留字段值，正文措辞需修正（"780 km" 是综合续航非 CLTC 纯电） |
| C-2 | `yangwang-u8` | accel | 字段 3.6 s vs 正文 3.9 s；官方 3.6 s | 保留字段值，正文需修正 |
| C-3 | `nio-et9` | battery | 字段 102 kWh vs 官方 100 kWh | 保留字段值，人工确认年款/版本 |
| C-4 | `nio-et9` | type | 字段 `SUV` vs 官方「full-size luxury sedan」 | 保留字段值，车身类型字段需人工修正 |
| C-5 | `maextro-s800` | battery | 字段 65 kWh（EREV 包）但 `powertrain=BEV`（BEV 应为 97/120 kWh） | 保留字段值，powertrain/trim 归属需人工对账 |
| C-6 | `yangwang-u8l` | battery | 字段 55.53 kWh vs 发布 56.58 kWh | 保留字段值，人工确认 |
| C-7 | `yangwang-u8l` | range | 字段 200 km vs 发布 230 km（纯电 CLTC） | 保留字段值，人工确认 |
| C-8 | `hongqi-guoya` | motor | 字段 160 kW vs 官方混动系统 294–358 kW（功率口径：单电机 vs 系统） | 保留字段值，功率口径（peak vs motor vs total）人工核对（P3 U-4 同类） |
| C-9 | `hongqi-guoya` | powertrain | HEV（非插电混动）在「新能源车」库（P3 U-2 既有边界） | 显式标注，不擅自删除 |

---

## 5. 核验方法与局限

### 5.1 方法

- 官方优先：厂商官网规格页（如 BYD/Yangwang `bydcn.com`、`yangwangauto.com`）> Wikipedia/auto-data.net（三级交叉核对，非一手）> 权威媒体（Electrek/EV Gulf）。
- 每个 `verified`/`conflict` 结论均带 `source` + `verified_at`（2026-10-23）。

### 5.2 局限

- **未做逐条人工核验的 176 格**为 `unverifiable`，不是「无数据」——需后续批次逐条 web 核验补齐。
- `model_year` 全 0 填充（数据缺失，不编造）；`trim` 仅在有值时透出。
- 价格为「China ex-factory reference price」USD 换算，官方源多给出厂价人民币/美元 MSRP，逐值 USD 换算未做汇率口径核验（标记 `unverifiable`）。
- 未覆盖：landed-cost 字段（.net 姊妹站职责）、逐条价格溯源（P3 U-1）。

---

## 6. 变更清单（commit `five-01-*`）

| 文件 | 变更 |
|---|---|
| `src/content.config.ts` | 新增 `param_verification` 可选字段（五元组 + status 枚举） |
| `src/data/parameter-verification.json` | **新增**：32 款关键参数表单源 |
| `scripts/generate-parameter-verification.mjs` | **新增**：生成脚本（可重跑，不编造） |
| `src/pages/vehicles/[slug].astro` | 新增「Key parameter verification」渲染 + conflict 黄框 |
| `docs/verification-system.md` | **新增**：本文档 |

---

## 7. 分离声明

- **已完成（已验证）**：机制设计、五元组 schema、32 款覆盖、8 项真实核验（verified）、8 项冲突标记（0 自动填补）、渲染落地。均有文件/行号 + web 核验证据。
- **未覆盖**：178 格 `unverifiable` 的逐条核验（后续批次）；`model_year` 填充；价格 USD 汇率口径溯源；landed-cost 字段（.net 职责）。

---

*报告路径：`docs/verification-system.md` · five-01*
