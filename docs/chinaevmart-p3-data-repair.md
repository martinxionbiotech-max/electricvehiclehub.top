# ChinaEVMart Phase 3 — Vehicle Data Quality Repair

> 仓库：`electricvehiclehub.top`（chinaevmart.com 代码库）
> 阶段：Phase 3 · 车辆数据质量修复
> 日期：2026-10-22 · 单一数据源 = `src/content/vehicles/*.md` + `src/content/brands/*.md`（内容集合 frontmatter）
> 校验：`npm run validate:data` → **0 issues** · `npm run build` → **899 pages, exit 0**

---

## 0. 结论摘要

| 维度 | 结果 |
|---|---|
| 车辆记录 | 517（frontmatter 单一数据源） |
| 品牌 | 72（`model_count` 求和 = 517，双向无孤儿，0 偏差） |
| 动力形式 | BEV 286 / PHEV 154 / EREV 58 / HEV 16 / ICE 3 = 517 |
| 车身类型 | SUV 348 / Sedan 106 / Hatchback 25 / MPV 38 = 517 |
| 重复记录 | 0（slug / title / vehicle_id 均无重复） |
| 价格口径 | **517/517 已显式标注 `China ex-factory reference price`**（原默认值 0 显式） |
| 校验规则 | 新增 8 类字段级校验 + 迁移脚本 dry-run |
| 数据漂移 | 2 处 description↔字段已修正（byd-seal / byd-han） |

---

## 1. 单一数据源与字段规范化

### 1.1 单一数据源判定

Phase 1 已判定 `vehicle-master.json` / `brand-master.json` 等 6 个 JSON 文件为**孤儿导出**（无任何 import，与内容集合存在数据漂移）。Phase 3 正式确立：

> **单一数据源 = 内容集合 frontmatter**（`src/content/vehicles/*.md`、`src/content/brands/*.md`）。

据此重写 `scripts/validate-data.mjs`：**不再校验孤儿 JSON master**，直接从 frontmatter 解析。原 `validate-data.mjs` 因依赖孤儿 `vehicle-master.json` 产生 2 条**误报** `md-drift`（`hongqi-guoya` 的 `Unknown`、`xpeng-p7-plus` 的 `SUV` 均来自过期的 master 快照，frontmatter 实为 `HEV` / `Sedan`）——Phase 3 消除这 2 条误报，验证归零。

### 1.2 字段枚举规范化（`src/content.config.ts`）

| 字段 | 修复前 | 修复后 |
|---|---|---|
| `powertrain` | `z.string()`（任意字符串） | `z.enum(['BEV','PHEV','EREV','HEV','ICE','FCEV','Unknown'])` |
| `type`（车身类型） | `z.string()` | `z.enum(['Sedan','Hatchback','SUV','Crossover','MPV','Wagon','Pickup','Van','Coupe','Convertible','Sports Car','Other','Unknown'])` |
| `price_type` | `z.string().default('China ex-factory price (MSRP)')` | `z.enum([五类]).default('China ex-factory reference price')` |
| `model_year` | 不存在 | `z.number().nullable().optional()`（新增，当前 0 填充） |

### 1.3 分类核对（517 全量）

- **BEV 286 / PHEV 154 / EREV 58 / HEV 16 / ICE 3**，全部落在合法枚举内，**无 `Unknown`、无 `FCEV`**。
- **分类边界登记（不擅自移除，待人工复核）**：ICE 3 台（`changan-nevo-lamore`、`changan-x5-plus`、`wuling-jiachen`）+ HEV 16 台出现在「中国新能源车数据库」中，属**数据库边界问题而非分类错误**。按 P1 建议保留并显式标注（HEV=混动非插电、ICE=燃油对照），不在本阶段武断删除（规则 #6 保留 URL、#3 不编造）。

### 1.4 品牌计数一致性（72 与数据集对账）

- 72 个品牌 frontmatter `model_count` 求和 = **517**，与车辆记录总数一致。
- 车辆 `brand` → 品牌集合 **双向无孤儿**（无缺品牌、无多品牌）。
- 重复记录：`slug` / `title`（不区分大小写）/ `vehicle_id` **均为 0 重复**。

---

## 2. 价格口径修复（P1 重点）

### 2.1 五类口径严格区分

原 schema 默认值 `'China ex-factory price (MSRP)'` **把 ex-factory 与 MSRP 两个不同口径混为一谈**。Phase 3 拆分为五类互斥枚举 + 一个未核实兜底：

| 口径枚举值 | 含义 |
|---|---|
| `Official MSRP` | 官方指导价 |
| `China market reference price` | 中国市场成交/参考价 |
| `China ex-factory reference price` | 出厂参考价 |
| `FOB quotation` | FOB 报价 |
| `Landed cost estimate` | 落地成本估算 |
| `Reference (unverified)` | 参考价（口径未核实） |

### 2.2 处置结果

- **517/517 车型显式标注 `China ex-factory reference price`**（迁移脚本 `--apply` 回填，不再依赖隐藏默认值）。数据来源本身即「China EV Mart catalog + manufacturer specs」的出厂/起始价口径，标注 ex-factory 正确、无 FOB 冒充（与 P1 假设③结论一致）。
- **绝不静默替换口径**：本批只把「ex-factory + (MSRP) 混写」纠正为「ex-factory reference」，未把任何 ex-factory 价改为 MSRP / 市场参考 / FOB。`fob_price_usd_min/max` 仍为 0/517（无 FOB 数据可冒充）。
- **可疑重复/默认价格聚类**（P1：22–24 个价格值跨 ≥4 品牌撞价，如 `$13,860`×11、`$21,100`×9）：
  - 判定为**中国车市常见整数人民币起步价换算的巧合**（如 ¥99,800 ≈ $13,860），**非「未填值兜底」**；
  - **有据修正：0 条**（无证据证明任一值为错误默认值，不擅自改价，规则 #3）；
  - **标注 unknown：0 条**（值本身合理，标 unknown 会损失真实数据）；
  - 处理方式：**保留原值，列入 §6 未解决冲突清单待人工溯源核验**，不改值。

### 2.3 渲染层同步

- `[slug].astro` 规格表 `Price basis`、JSON-LD offer 描述、`fobRange` 回退文案。
- `[slug].md.ts` 机器可读变体 `Price basis`。
- `index.astro` 首页 JSON-LD `price_usd` PropertyValue 描述。
- `data/vehicles.json.ts` 端点 `description`。

以上 4 处硬编码的 `'China ex-factory price (MSRP)'` 全部同步为 `'China ex-factory reference price'`。

---

## 3. 续航标准分离

### 3.1 分字段核验

| 字段 | 修复前 | 修复后 |
|---|---|---|
| `range_cltc_km` | 有（486/517） | 保留 |
| `range_wltp_km` | 有（9/517） | 保留 |
| `range_epa_km` | **缺失** | 新增 `z.number().nullable().optional()` |
| `range_nedc_km` | **缺失** | 新增 `z.number().nullable().optional()` |
| `range_long_km` | 有（47/517，长续航 CLTC 变体） | 保留 |

### 3.2 处置结果

- CLTC / WLTP / EPA / NEDC **四标准分字段**（`range_cltc_km` / `range_wltp_km` / `range_epa_km` / `range_nedc_km`），`range_long_km` 明确为「长续航 CLTC 变体」。
- 无标准标注的续航值：**0**（所有续航值均落在 `*_km` 标准字段内，无裸 `range` 字段）。
- EPA / NEDC 当前 **0 填充**（无数据源，不编造，规则 #3）。渲染层 `[slug].astro` 规格表新增 `Range (EPA)` / `Range (NEDC)` 两行，无值时自动隐藏。
- **修复渲染 bug**：`[slug].astro` 相关车型列表原引用**不存在的字段** `v.data.range_standard`（schema 从未定义，恒渲染「range TBA」），改为 `v.data.range_cltc_km`。

---

## 4. 字段级校验规则（新增/强化清单）

`scripts/validate-data.mjs` 重写（frontmatter 单一数据源），新增/强化规则：

| # | 规则 | 类型 |
|---|---|---|
| 1 | 必填字段：车辆 9 项（title/description/slug/brand/type/powertrain/price_usd/publishedDate/author）、品牌 6 项 | 必填 |
| 2 | `powertrain` 枚举（BEV/PHEV/EREV/HEV/ICE/FCEV/Unknown） | 枚举 |
| 3 | `type` 车身类型枚举（13 类） | 枚举 |
| 4 | `price_type` 五类口径 + 兜底枚举 | 枚举 |
| 5 | 数值单位区间：price(0–300k)、battery(0–300)、range(50–1500×4标准)、top_speed(0–500) | 单位 |
| 6 | 重复 slug（车辆 + 品牌） | 重复 ID |
| 7 | slug 与文件名一致性 | 稳定 ID |
| 8 | 品牌↔车辆双向关系 + `model_count` 对账 + `family` 车系存在性 | 车系/关系 |

**迁移脚本** `scripts/migrate-p3-data.mjs`：
- 默认 **dry-run**（只报数不写盘），`--apply` 才写盘；
- 输出：受影响记录数、已显式数、冲突值清单、缺失 price_usd 数。

### Dry-run 输出摘要（schema 变更前）

```
total vehicles: 517
explicit price_type already present: 0
would add "China ex-factory reference price" (currently default): 517
conflicting values: 0
missing price_usd (skipped): 0
```

→ 517 条受影响，0 冲突，0 缺失；`--apply` 后 517/517 显式回填，0 错误。

---

## 5. before/after 计数 + 示例

### 5.1 字段规范化

| 修复类 | 受影响记录数 | 修正数 | 标注 unknown 数 |
|---|---|---|---|
| `powertrain` / `type` 枚举化 | 517 | 0（值本就合法） | 0 |
| `price_type` 五类枚举 + 默认值纠正 | 517 | 517（显式回填） | 0 |
| `range_epa_km` / `range_nedc_km` 新增字段 | 517 | 0（无数据，不编造） | — |
| `model_year` 新增字段 | 517 | 0（无数据） | — |

### 5.2 价格口径分布（五类各数）

| 口径 | 记录数 |
|---|---|
| Official MSRP | 0 |
| China market reference price | 0 |
| **China ex-factory reference price** | **517** |
| FOB quotation | 0 |
| Landed cost estimate | 0 |
| Reference (unverified) | 0 |

### 5.3 分类修正

- 修正数：**0**（无分类错误；2 条 `md-drift` 为孤儿 master 误报，已通过「单一数据源」重写消除）。
- 边界登记：ICE 3 + HEV 16（待人工复核，未删除）。

### 5.4 重复记录处理

- 合并：**0**（无重复）。识别：slug/title/vehicle_id 三重去重，全通过。

### 5.5 数据漂移修正示例

| 文件 | 字段 | before | after |
|---|---|---|---|
| `byd-seal.md` | description 续航 | 「CLTC-rated range of **450 km**」 | 「CLTC-rated range of **550 km**」（对齐 `range_cltc_km: 550`） |
| `byd-han.md` | description 电池 | 「**72 kWh** of battery」 | 「**76.9 kWh** of battery」（对齐 `battery_kwh: 76.9`） |

---

## 6. 未解决冲突清单（待人工复核，不武断取舍）

| # | 冲突/疑点 | 证据 | 建议处置 |
|---|---|---|---|
| U-1 | 22–24 个价格值跨 ≥4 品牌撞价（`$13,860`×11、`$21,100`×9、`$15,460`×8、`$14,060`×8、`$20,820`×7…） | §2.2 聚类 | 逐值溯源官方价目表/媒体报价；无法核验者标 `Reference (unverified)`，不改值 |
| U-2 | ICE 3 台 + HEV 16 台在「新能源车」库中 | §1.3 | 明确库边界：移除 or 显式「燃油/混动对照」标注 |
| U-3 | `variants` 字段存在于 49 个文件 frontmatter，但 schema 未定义（孤儿字段，不被集合读取） | `grep variants` | 决定是否入 schema 或清理 |
| U-4 | 7 处 description「N kW peak output」与 `motor_power_kw` 字段不一致（多为「峰值/综合功率」vs「单电机功率」口径差异，非必错） | denza-z9-gt/m-hero-917/tank-400 等 | 人工核对功率口径（peak vs motor vs total） |
| U-5 | `verification_status` 仅 40/517 有值（None 477 / partial 36 / unverifiable 2 / verified 2）；`data_reviewed` 517/517 = false | Phase 1 §7 | 建立人工复核流水线 |
| U-6 | `landed_cost` / `landed_cost_markets` 字段在 .top 仍 517 处残留（.md 变体/品牌页/JSON 端点仍渲染） | Phase 1 P1-6 | Phase 5 决策：移除 or 统一存档 |
| U-7 | EU CVD 税率 `verification_status: unknown`（EUR-Lex 复核被 WAF 拦截） | `tariffs.json cvd_meta` | 人工权威复核（Phase 5） |

---

## 7. 分离声明

- **已完成（已验证）**：§1–§4 的 schema 枚举化、price_type 五类拆分与 517 显式回填、range 四标准分字段、validate 脚本重写、迁移脚本 dry-run、2 处 description 漂移修正、渲染层同步。均有文件/行号证据，`validate:data` 0 issues、`build` exit 0。
- **未解决（待人工）**：§6 U-1~U-7，均未武断取舍。
- **未覆盖**：逐条价格/税率权威溯源（需外部源）、线上逐页 HTTP 抓取、landed-cost 去留决策（属 Phase 5）。

---

*报告路径：`docs/chinaevmart-p3-data-repair.md`*
