# ChinaEVMart Phase 8 — Implementation & Acceptance 验收交付批（收官）

> 仓库：`electricvehiclehub.top`（chinaevmart.com 代码库）
> 阶段：Phase 8 · 验收交付总包
> 日期：2026-10-22 · 前序报告 P1–P7 全部就位（P1 基线 / P2 品牌 / P3 数据 / P4a-c 模板 / P5 落地成本 / P6 优先级 / P7 技术 SEO）
> 总纲：`/root/.openclaw/workspace/phase2/55-chinaevmart-prompt.md`（Phase 8 全文 + 验收标准）
> 本文档 = 十项交付物 + 验收标准逐项核对 + 最终一致性 + 回滚手册

---

## 0. 收官状态快照（本批实测，非引述）

| 项 | 结果 |
|---|---|
| `npm run validate:data` | ✅ **0 issues**（72 brands / 517 vehicles / 双向关系 model_count 对账） |
| `npm run build` | ✅ **899 pages, exit 0**（170s 全量静态构建） |
| sitemap | ✅ **700 URL**，全部 `chinaevmart.com`（0 非目标域） |
| 抽 5 页跨模板渲染 | ✅ 首页 / 目录 / 车型 / 品牌 / About 全部单 `<title>`、canonical 正确 |
| git 工作区 | ✅ clean（构建产物 `dist/` 不入库） |
| 前序报告 | ✅ P1–P7 共 8 份 + 规范文档 1 份，全在 `docs/`；P5 在 CNEVhub 仓 `docs/landed-cost-validation.md` |

---

## ① 基线审计与已验证发现汇总（P1）

基线报告：`docs/chinaevmart-p1-baseline.md`。核心结论（均有文件/行号证据）：

- **车辆 517 / 品牌 72 / 技术实体 137 / 法规实体 66 / 博客 86（77 发布 + 9 草稿）/ 文档 14 / 市场 30**。
- **可索引 URL 估算 ~701**（517 车型 + 72 品牌 + 77 博客 + 14 文档 + ~16 静态 + 1 市场 + 4 数据端点；不含 noindex 分页/标签，不含 .md 变体）。
- **7 项假设核验结果**：① 动力分类混乱=真实（ICE 3 + HEV 16 边界）；② 可疑重复价格=真实（22 值跨 ≥4 品牌撞价）；③ ex-factory 冒充 FOB=**不成立**；④ 重复记录/品牌计数不一致=**不成立**（0 偏差）；⑤ Overview 同构句=真实（517 全量）；⑥ 进口税计算残留=真实（landed-cost 字段在 .top 4 渲染面存活）；⑦ 过期规格=部分真实（by-seal 1 处描述↔字段漂移确认）。
- **问题登记表 22 项**（P0 4 / P1 8 / P2 7 / P3 3），全部在 P2–P7 逐项处置或显式顺延。

---

## ② 受影响 URL 与记录 Inventory（全阶段变更总表）

### 2.1 URL 层（零结构性新增/删除）

| 变更 | 说明 | 证据 |
|---|---|---|
| **无新增可索引 URL** | 目录/首页筛选纯客户端 JS，不产 `?param=` URL；无 /compare/ 矩阵 | P4a / P7 ⑧ |
| **无删除 URL** | 517 车型 + 72 品牌 + 77 博客 + 14 文档 + 16 静态 + 1 市场全部保留 | sitemap 700 不变（P4a–P7 一致） |
| sitemap 收录范围 | 700 URL（车型 518 + 品牌 73 + 博客 78 + 文档 15 + 静态 16）；排除分页/tag/.md 变体/data 端点 | P7 ③ 实测 |
| `.md` 机器可读变体 | 594 个（517 车型 + 77 博客）保留，补 `Link: <canonical>` header | P7 F-5 |

### 2.2 记录层（数据源 = 内容集合 frontmatter 单一数据源）

| 集合 | 数量 | 本阶段改动 |
|---|---|---|
| `src/content/vehicles/*.md` | 517 | P2 品牌残留批量（data_source 517 + image_credit 42 + image_source 域 42）；P3 `price_type` 517 显式回填 + 2 处 description 漂移修正；P4b 正文不再渲染 Overview |
| `src/content/brands/*.md` | 72 | P2 品牌残留；P4b 剥离 landed-cost 残留 213 行 + 冗余 3 节 |
| `src/content/blog/*.md` | 86 | P2 品牌残留批量（86 文件，含 17 文件旧域 URL） |
| `src/content/docs/*.md` | 14 | P2 品牌残留；P4c glossary/data-provenance 四层标注 |

> **单一数据源判定**：`vehicle-master.json` / `brand-master.json` / `technical-master.json` / `regulatory-master.json` / `market-master.json` / `entity-graph.json` 均为孤儿文件（无 import），被内容集合取代；`validate-data.mjs` 已重写为 frontmatter 单一源，消除 2 条孤儿 master 误报（hongqi-guoya `Unknown`、xpeng-p7-plus `SUV`）。

---

## ③ 文件 / 组件 / 数据表改动清单 + 理由

> 全阶段 `c4ca006..HEAD`（P1 基线 → 当前 HEAD）共 **725 文件**（含 docs 报告与 scripts）；P3 边界后 615、P2 边界后 709。核心改动按层归类：

### 3.1 配置与共享层

| 文件 | 改动 | 理由 |
|---|---|---|
| `src/config/site.ts` | name→`China EV Mart`、url→`https://chinaevmart.com`、description 去「72 brands」绝对化 | P0-1/P0-4 品牌迁移 |
| `src/config/contact.ts` | FAQ 去「代找车源/landed-cost 情报」越权表述 + 品牌残留 | P4c 4-G |
| `.env.example` | `SITE_NAME`/`SITE_URL` 默认值 → China EV Mart / chinaevmart.com | P0-1 |
| `astro.config.mjs` | sitemap filter（排除分页/tag/feature flag 关闭页） | P7 ③ |
| `public/logo.svg` | `<text>EV</text><text>Hub</text>` → `China EV Mart` 品牌标识 | P0-2 |
| `public/llms.txt` | 标题 `CNEVhub`→`China EV Mart`、计数「315/58」→「517/72」 | P0-3 |
| `public/_redirects` | 计算器跨域 301 + www/sitemap/blog page1 301（详见 ⑧） | P1 §1.4 / P5 |

### 3.2 模板层（`src/pages/`）

| 文件 | 改动 | 理由 |
|---|---|---|
| `index.astro` | 首页重建：定位句 / A-tier 精选（quality_tier=A 433 取 6）/ 品牌墙动态推导 / 入口区 / B2B 如实 CTA / 移除「complete/source-verified/500+」 | P4a 4-A |
| `vehicles/index.astro` | 目录重建：4 维客户端筛选 / 数据集范围说明 4 条 / 实时计数 | P4a 4-B |
| `vehicles/[slug].astro` | 车型详情十要素 + 四分组规格表 + 续航标准表 + C 层紧凑档案 + 移除 6 类冗余区块（Entity Snapshot/40HQ/扁平大表/Technology/Market Compliance/双卡 Data Sources） | P4b 4-C |
| `brands/[slug].astro` | 品牌页重建：集团/品牌/子品牌关系表 + 动力分布 + 车系分组 + 移除 landed-cost 卡片 + 3 级面包屑 JSON-LD | P4b 4-D / P7 F-4 |
| `about.astro` | 信息平台非卖家定位 + does/does-not 区 | P4c 4-G |
| `methodology.astro` | 四层分离 + 数据来源/更新/纠错/价格五类/续航标准/编辑审查 + 成本假设省略（无计算器）+ 对比标准 | P4c 4-G |
| `landed-cost-methodology.astro` | 顶部指针「本平台不运行计算器，计算器在 electricvehiclehub.net」 | P5 C1 |
| `vehicles/[slug].md.ts` / `blog/[...slug].md.ts` | `.md` 变体加 `Link: <canonical>` header | P7 F-5 |
| `authors.astro` / `editorial-independence.astro` / `image-credits.astro` 等 | 移除冗余 `<SEO>`（双 title 根因） | P7 F-1 |

### 3.3 组件与库（`src/lib/`、`src/components/`）

| 文件 | 改动 | 理由 |
|---|---|---|
| `src/lib/powertrain.ts` | **新增**：动力标签单一术语源（POWERTRAIN_ORDER/LABELS/powertrainLabel/powertrainCode） | P4a |
| `src/lib/site-stats.ts` | HEV/ICE 分列（hevCount/iceCount），计数实时推导 | P4a |
| `src/lib/brand-label.ts` | 正则 `/EV Hub original/i` → `/China EV Mart original/i` | P2 P1-2 |
| `SEO.astro` | title 去重（已含站点名不追加）、移除失效 SearchAction、canonical 基于 siteConfig.url | P7 F-2/F-3 |

### 3.4 数据 Schema 与校验（`src/content.config.ts` + `scripts/`）

| 文件 | 改动 | 理由 |
|---|---|---|
| `src/content.config.ts` | `powertrain`/`type`/`price_type` 枚举化 + `range_epa_km`/`range_nedc_km`/`model_year` 新增字段 | P3 |
| `scripts/validate-data.mjs` | **重写**为 frontmatter 单一源，8 类字段级校验 | P3 |
| `scripts/migrate-p3-data.mjs` | 迁移脚本（默认 dry-run，`--apply` 写盘） | P3 |

---

## ④ Before / After 示例（首页 / 车型页 / 品牌页 / 成本方法论）

> 引用 P4/P5 报告实测 + 本批 `dist/` 抽检复验。

### 4.1 首页

| 项 | Before | After | 证据 |
|---|---|---|---|
| H1/定位 | 「The complete product database for Chinese EVs」+「source-verified product record」+「500+」 | 「Independent information platform」定位句 + P2 规范句「…discovering Chinese new-energy vehicles, comparing vehicle specifications, researching automotive technology, and evaluating export-market requirements」 | `dist/index.html` 0 命中 `source-verified`/`complete product database`/`500+` |
| 精选车型 | 四字段齐全筛选 | `quality_tier === 'A'`（433 取 6），空态兜底 | P4a §1 |
| 品牌墙 | 硬编码 72 项 + `// 58 品牌墙` 错注释 | 品牌集合实时推导 + `{brandCount} Chinese EV brands` | P4a §1 |
| 公开计数 | meta「500+ Chinese EVs」 | 「517 vehicles across 72 brands」（实时） | P4a §1 |

### 4.2 车型详情页（以 byd-seal 为例，本批复验）

| 项 | Before | After | 证据（`dist/vehicles/byd-seal/index.html`） |
|---|---|---|---|
| 续航标注 | 相关车型列表引用不存在的 `range_standard` 字段（恒「range TBA」） | 独立 `## Range by test standard` 表（CLTC/WLTP/EPA/NEDC 分列） | `Range by test standard`=1 |
| 价格口径 | `price_type` 依赖默认值（未显式） | `## Price` 表显式 `China ex-factory reference price` | 命中=3 |
| 冗余区块 | Entity Snapshot / 40HQ / Market Compliance / 扁平 63 字段大表 / 正文 Overview | 全部移除，改四分组规格表 + 字段生成 Summary + 竞品对比 + provenance | `Entity Snapshot`=0 / `Dimensions & Logistics`=0 / `Market Compliance`=0 / `40HQ`=0 |
| 竞品/溯源 | — | `Comparable Sedan BEVs` + `Data provenance & verification` | `Comparable`=1 / `Data provenance`=1 |
| schema 诚信 | — | 无 rating/review/availability/seller/priceValidUntil（offers 仅真实 price_usd + 诚实描述） | 上述字段 0 命中（`review` 唯一命中是 `/blog/byd-seal-deep-review` 内链，非 JSON-LD） |

### 4.3 品牌页（以 byd 为例，本批复验）

| 项 | Before | After | 证据（`dist/brands/byd/index.html`） |
|---|---|---|---|
| 集团关系 | 无 | `Manufacturer group` 关系表（「BYD is the brand name of the BYD group」） | 命中=1 |
| 动力分布 | 无 | `Powertrain lineup`（枚举顺序 + 计数） | 命中=1 |
| 车系分组 | 无 | `Model families`（按 family 字段，排除「Ungrouped」） | 命中=1 |
| landed-cost 残留 | 车型卡「Landed DE $X (+N%)」+ 正文「Brand Overview/At a Glance/Explore」 | 全部剥离（213 行 landed-cost + 3 节冗余） | `Landed DE`=0 / `Landed premium`=0 |

### 4.4 成本方法论（跨站一致性，P5 已证 + 本批复验）

| 项 | Before | After | 证据 |
|---|---|---|---|
| 方法论文档口径 | 「标准关税按 CIF 值计」 | 「按出厂基价计」+ CIF 为严格口径的保守简化说明 | P5 F1（.net）/ C2（.top） |
| CVD 税率范围 | 「17%–35.3%」 | 「7.8%–35.3%」（补 Tesla 7.8% + other-cooperating 20.7%） | P5 F2 |
| .top 定位 | 方法论文档把公式表述为 chinaevmart 自身产出 | 顶部指针「本平台不运行计算器，交互计算器与逐市场数据在 electricvehiclehub.net」 | `dist/landed-cost-methodology/index.html` 命中「not run a landed-cost calculator」+ 外链 |
| 公式↔代码 | — | 三处实现代数恒等（base×(1+duty)×(1+cvd)×(1+VAT)+fixed） | P5 §1.1 + 9 用例 PASS |

---

## ⑤ 车辆数据校验报告 + 未解决冲突清单

### 5.1 校验结果（本批实测）

- `npm run validate:data` → **0 issues**：72 brands（必填 + 唯一 slug）、517 vehicles（必填/枚举/单位/family/品牌关系）、品牌↔车辆双向关系 + `model_count` 对账。
- 分类分布：BEV 286 / PHEV 154 / EREV 58 / HEV 16 / ICE 3 = 517；车身 SUV 348 / Sedan 106 / Hatchback 25 / MPV 38 = 517。
- 价格口径：**517/517 显式 `China ex-factory reference price`**（五类枚举分离，`fob_price_usd_min/max` 0/517）。
- 续航标准：CLTC 486 / WLTP 9 / EPA 0 / NEDC 0（EPA/NEDC 无源不编造）；无裸 range 字段。
- 重复记录：slug/title/vehicle_id 三重去重 **0 重复**。
- 品牌计数：72 brand `model_count` 求和 = 517，0 偏差，双向无孤儿。
- description 漂移：2 处已修正（byd-seal 450→550km、byd-han 72→76.9kWh）。

### 5.2 未解决冲突清单（待人工，未武断取舍）

| # | 冲突/疑点 | 处置 |
|---|---|---|
| U-1 | 22–24 个价格值跨 ≥4 品牌撞价（$13,860×11、$21,100×9 等） | 判定为整数人民币起步价换算巧合，保留原值，逐值溯源后无法核验者标 `Reference (unverified)`，不改值 |
| U-2 | ICE 3 + HEV 16 在「新能源车」库中 | 显式标注（HEV=混动非插电、ICE=燃油对照），不擅自删除（规则 #6） |
| U-3 | `variants` 字段 49 文件存在但 schema 未定义（孤儿字段） | 决定是否入 schema 或清理 |
| U-4 | 7 处 description「N kW peak output」与 `motor_power_kw` 不一致 | 人工核对功率口径（peak vs motor vs total） |
| U-5 | `verification_status` 仅 40/517 有值；`data_reviewed` 517/517=false | 建立人工复核流水线 |
| U-6 | landed-cost 字段在 .top 残留（.md 变体/JSON 端点仍渲染） | Phase 5 决策：移除 or 统一存档（车型 HTML 页 + 品牌页已剥离） |
| U-7 | EU CVD 税率 `verification_status: unknown`（EUR-Lex 复核被 WAF 拦截） | 人工权威复核 |

---

## ⑥ 测试清单（引用 P7 + P5 测试结果）

### 6.1 筛选 / 渲染 / 链接 / schema / canonical（P7）

| 测试 | 结果 |
|---|---|
| 目录/首页筛选不产可索引 URL | ✅ 纯客户端 JS，0 `?param=` 链接，sitemap 700 不变 |
| 关键路由渲染 | ✅ 899 页静态构建 exit 0；404/500 页存在 |
| canonical 域名一致性 | ✅ 全站 canonical 均 `chinaevmart.com`（0 非目标域残留） |
| sitemap 排除逻辑 | ✅ 分页/tag/.md 变体/data 端点均正确排除 |
| 内链导航/面包屑 | ✅ 品牌页 3 级面包屑 JSON-LD 已修；孤儿页 `/markets/` 0 入链（待人工 H-3） |
| title/desc/heading | ✅ 5 页双 `<title>` + 103 页站点名重复已修，全量 0 残留 |
| schema 与可见内容一致 | ✅ 移除失效 SearchAction；无 rating/review/availability/seller |
| 重复 URL / 薄筛选页 | ✅ 无自动对比 URL 矩阵；`.md` 变体已加 canonical header |

### 6.2 计算器回归（P5，.net 仓）

- 回归脚本 `scripts/test_landed_cost_regression.py`：**9/9 用例 PASS**（覆盖 EU 高关税/PHEV/EREV/中东/澳新/高非欧关税）；全量 517×30 重算 **0 真实偏差（≥$0.015）**，78 处 ±$0.01 取整伪差（cosmetic）。
- 运行方式：`python3 scripts/test_landed_cost_regression.py [--cases|--full]`。
- chinaevmart 侧无计算器（`/landed-cost-calculator/` 301 到 .net），本仓回归由 `.net` 仓承载；交叉一致性由 C1/C2 文案指针保证。

---

## ⑦ 构建 / 测试结果与失败项

| 项 | 结果 |
|---|---|
| `npm run validate:data` | ✅ 0 issues |
| `npm run build` | ✅ 899 pages, exit 0（本批 170.25s） |
| sitemap | ✅ 700 URL，全 chinaevmart.com |
| 抽 5 页渲染 | ✅ 单 title / canonical 正确（见 §0 表） |
| **失败项** | **0**（无未解决构建/测试失败；`WARNING: SITE_URL not set` 为预期 fallback，生产用 `.env` 注入 `SITE_URL`） |

> 已知非阻断项：全站渲染 `noindex,nofollow`（`PUBLIC_INDEXABLE` 未设，预览过渡期预期行为，非缺陷）。生产放开步骤见 §⑨ H-1。

---

## ⑧ URL / 重定向变更日志（计算器 301 等）

`public/_redirects` 当前完整规则（Cloudflare Pages `_redirects` 格式）：

| 规则 | 目标 | 状态 | 引入 |
|---|---|---|---|
| `/landed-cost-calculator/` | `https://electricvehiclehub.net/landed-cost-calculator/` | 301 跨域 | P5（`b14cc6b` differentiate-calculator） |
| `/landed-cost-calculator` | `https://electricvehiclehub.net/landed-cost-calculator/` | 301 跨域 | 同上 |
| `/sitemap.xml` | `/sitemap-index.xml` | 301 | 既有 |
| `https://www.chinaevmart.com/*` | `https://chinaevmart.com/:splat` | 301 裸域 | 既有（P2 更新域） |
| `/index.php` / `/index.htm` | `/` | 301 | 既有 |
| `/blog/page/1/` | `/blog/` | 301 | 既有（消除重复） |

> **唯一功能性重定向变更 = 计算器跨域 301**（.top 去计算功能，出口情报归属 .net 姐妹站）。无 sitewide redirect、无批量 URL 变更、无生产路由改写。

---

## ⑨ 剩余待人工事项清单

| # | 事项 | 严重度 | 来源 |
|---|---|---|---|
| H-1 | 生产上线放开 `PUBLIC_INDEXABLE=1`（Cloudflare Pages 环境变量）+ 逐页 HTTP 状态码/`.md` Content-Type 实测 | P0（上线阻断） | P7 H-1 |
| H-2 | 公司联系邮箱 `info@electricvehiclehub.top` 迁移（需运营方确认 chinaevmart.com 邮箱已开通） | P1 | P2 §4 / P7 H-4 |
| H-3 | Organization `sameAs` 遗留 `x.com/cnevhub` + github `CNEVhub`（待运营方新账号） | P2 | P7 H-2 |
| H-4 | `/markets/` 孤儿页（0 入链但 sitemap 收录）——加导航链接或随 Phase 5 迁 .net | P2 | P7 H-3 |
| H-5 | landed-cost 数据字段在 .top 残留决策（.md 变体/`data/vehicles.json.ts` 端点）——移除 or 存档 | P1 | P7 H-5 |
| H-6 | EU CVD 税率 + 非欧市场税率权威复核（EUR-Lex 上次被 WAF 拦截） | P1 | P5 H1/H2 / U-7 |
| H-7 | 逐条价格溯源（U-1 撞价 22 值） | P2 | P3 U-1 |
| H-8 | `data_reviewed` 复核流水线 + `verification_status` 补全（当前 517/517=false） | P2 | P3 U-5 |
| H-9 | `model_year` 0 填充补数据；`variants` 孤儿字段决策 | P3 | P3 U-3 |
| H-10 | GSC 接入后校准 P6 批次优先级（当前无流量数据，不虚构） | P3 | P6 §0 |

**待人工事项规模：10 项**（P0 1 / P1 3 / P2 3 / P3 3），全部为「需外部源 / 运营方决策 / 生产环境操作」项，均未武断改动、未当已确认事实呈现。

---

## ⑩ 回滚说明（逐阶段 commit revert 手册）

> 总原则：每个 commit 独立原子，`git revert <hash>` 可单批回滚（非破坏、保留历史）；`git reset --hard` 为破坏性操作，仅作最后手段。60 个 commit 中，ChinaEVMart Phase 1–8 的提交边界如下（从 HEAD 向下）：

| 阶段 | 提交 | 说明 |
|---|---|---|
| **P8（本报告）** | `<p8-commit>` | 纯 docs（本文件），revert 零风险 |
| **P6+P7** | `f4c8f59` | 优先级文档 + SEO 护栏修复（标题/schema/面包屑/.md canonical） |
| **P5** | `35df63b` | 落地成本交叉一致性（.top 方法论指针 + CVD/CIF 文案） |
| **P4c** | `ae0f6b4`（docs）/ `69023a4` / `9d9baaa` | 对比/技术/信任页 |
| **P4b** | `2fe8be7`（docs）/ `176efdd` / `4df7d43` / `6e2e607` | 车型详情 + 品牌页 |
| **P4a** | `5a11297`（docs）/ `c92849f` / `a30676d` / `77dce9a` | 首页 + 目录 |
| **P3** | `c0182aa`（docs）/ `418e306` / `a5f87af` / `11c84d0` | 数据 schema + 价格口径 + 校验重写 |
| **P2** | `a098495` / `36652ee` / `c6098ea` / `55aeaf8` / `ed340e2` | 品牌统一（core/data/blog/docs/styleguide） |
| **P1 基线** | `c4ca006` | 只读审计（零编辑），即回滚终点 |

### 逐阶段回滚命令（按需取用）

```bash
# 回滚 P6+P7（撤销 SEO 护栏修复）
git revert f4c8f59

# 回滚 P5（撤销落地成本交叉一致性）
git revert 35df63b

# 回滚 P4c（技术+信任，docs 可一并 revert）
git revert ae0f6b4 69023a4 9d9baaa

# 回滚 P4b（车型详情+品牌页）
git revert 2fe8be7 176efdd 4df7d43 6e2e607

# 回滚 P4a（首页+目录）
git revert 5a11297 c92849f a30676d 77dce9a

# 回滚 P3（数据 schema/价格/校验）
git revert c0182aa 418e306 a5f87af 11c84d0

# 回滚 P2（品牌统一全批）
git revert a098495 36652ee c6098ea 55aeaf8 ed340e2

# 全量回滚到 P1 基线（保留历史，逐 commit 反向）
git revert c4ca006..HEAD

# 全量硬回滚（破坏性，丢弃后续历史，慎用）
git reset --hard c4ca006 && git push --force
```

**回滚注意**：
1. `git revert` 需工作区 clean（本批已验证 clean）。
2. P2 数据批（`55aeaf8`）为纯文案替换（517 data_source + 42 image_credit + 42 image_source），回滚零回归风险；P3 `a5f87af`（517 price_type 回填）为数据值改动，回滚后 `price_type` 回到默认值依赖，`validate:data` 仍应通过（枚举兼容）。
3. 反向 `git revert c4ca006..HEAD` 会按时间逆序逐个 revert，P3 的 schema 枚举化先撤、P2 的品牌替换后撤，依赖顺序已由 git 保证（后进先出）。
4. 计算器 301 属 `b14cc6b`（P1 之前的 legacy .top 工作，非本 Phase 1–8 提交），如需撤销须单独 `git revert b14cc6b`。

---

## 验收标准逐项核对（Prompt acceptance criteria）

| # | 验收标准 | 结论 | 证据 |
|---|---|---|---|
| 1 | 零编造事实 / 无未支撑验证声明 | ✅ **通过** | P2/P4c：0 虚构员工/资质/合作关系；verification_status 诚实（None 477/partial 36/unverifiable 2/verified 2）；四层标注（Fact/Claim/Interpretation/Estimate）；缺失字段标「not recorded」不估算 |
| 2 | 无静默 ex-factory→FOB | ✅ **通过** | P3：price_type 五类互斥枚举，517/517 显式 `China ex-factory reference price`；`fob_price_usd_min/max` 0/517；无任何字段静默改写口径 |
| 3 | 无默认价冒充验证价 | ✅ **通过** | P3：默认值依赖消除（0 依赖默认）；撞价 22 值判定为巧合并保留待核（U-1），`data_reviewed` 517/517=false 如实呈现，无「verified price」陈述 |
| 4 | 续航值无缺失标准标注 | ✅ **通过** | P3：CLTC/WLTP/EPA/NEDC 四标准分字段，0 裸 range；`## Range by test standard` 独立表（本批复验命中） |
| 5 | 公开计数同源 | ✅ **通过** | 517/72 均从内容集合实时推导（`site-stats.ts`），无硬编码；品牌 model_count 求和=517，0 偏差 |
| 6 | 新内容独立价值（非模板复述） | ✅ **通过** | P4b 移除 517 Overview 同构句 + 6 类冗余区块，改字段生成差异化 Summary + 竞品对比 + provenance；P6 6 批优先策略，不一次性重写 |
| 7 | 既有 URL 保留（除非批准映射） | ✅ **通过** | sitemap 700 全程不变；0 删除、0 sitewide redirect；`.md` 变体保留并补 canonical；唯一功能性变更 = 计算器 301（有据，P5 决策） |
| 8 | 计算器文档与实现一致 | ✅ **通过** | P5：公式三处代数恒等，9/9 回归 PASS，517×30 重算 0 真实偏差；.top 方法论指针与本仓「无计算器」定位一致 |
| 9 | 变更可测可逆 | ✅ **通过** | `validate:data` 0 issues + `build` exit 0 可复现；每 commit 原子 + 逐阶段 revert 手册（§⑩）；迁移脚本 dry-run/--apply |

**验收结论：9/9 全部通过。** 无未解决阻断项；10 项待人工事项均为「外部源/运营方决策/生产环境操作」，已显式分离、未当已确认事实呈现。

---

## 收尾（本批交付）

- **报告路径**：`docs/chinaevmart-p8-acceptance.md`（本文档）。
- **前序报告**：`docs/chinaevmart-p1-baseline.md` 至 `p7-seo-safeguards.md`（8 份）+ `docs/chinaevmart-style-guide.md` + CNEVhub 仓 `docs/landed-cost-validation.md`（P5）。
- **最终一致性**：`validate:data` 0 issues · `build` 899 页 exit 0 · sitemap 700 全 chinaevmart.com · 抽 5 页单 title/canonical 正确 · git 工作区 clean。
- **分离声明**：本文档全部「已验证事实」有 `dist/` 全量 grep + `npm` 命令 + git log 证据；「待人工」10 项显式单列；未覆盖 live HTTP 逐页状态码与 GSC 真实流量（均已标注）。

---

*报告路径：`docs/chinaevmart-p8-acceptance.md` · 收官*
