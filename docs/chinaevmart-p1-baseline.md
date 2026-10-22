# ChinaEVMart Phase 1 — Baseline Audit

> 严格只读审计 · 零编辑 · 基线记录
> 仓库：`electricvehiclehub.top`（chinaevmart.com 代码库）
> 审计日期：2026-10-22 · 审计对象：源码 + 数据文件 + 内容集合
> 线上实测（任务书提供）：chinaevmart.com 标题仍为「EVHub Top — Chinese EV Product Database」

---

## 0. 关键结论摘要

| 项 | 结果 |
|---|---|
| 车辆记录 | 517（frontmatter 与 vehicle-master.json 计数一致） |
| 品牌 | 72（content 集合与 brand-master.json 一致，模型计数零偏差） |
| 技术实体 | 137（technical-master.json） |
| 法规实体 | 66（regulatory-master.json） |
| 博客 | 86 文件（77 发布 / 9 草稿） |
| 文档 | 14 |
| 市场 | 30（tariffs.json） |
| **旧品牌残留** | **全站系统级残留，P0**（详见 §4） |
| **数据字段口径** | **ex-factory 标注正确，但 landed-cost 字段在 .top 仍 517 处残留（P1）** |

---

## 1. URL / 路由 Inventory

### 1.1 静态页面（`src/pages/*.astro`）
首页、404、500、about、accessibility、authors、contact、cookies、copyright、disclaimer、editorial-independence、faq、image-credits、landed-cost-methodology、methodology、privacy、terms。

### 1.2 动态路由（内容集合驱动）

| 路由 | 模板 | 数量 | 备注 |
|---|---|---|---|
| `/vehicles/[slug]/` | `vehicles/[slug].astro` | 517 | 车型详情 |
| `/vehicles/[slug].md` | `vehicles/[slug].md.ts` | 517 | 机器可读 Markdown 变体 |
| `/vehicles/` | `vehicles/index.astro` | 1 | 目录（按价格升序） |
| `/brands/[slug]/` | `brands/[slug].astro` | 72 | 品牌详情 |
| `/brands/` | `brands/index.astro` | 1 | 品牌目录 |
| `/blog/[slug]/` | `blog/[...slug].astro` | 77 | 已发布文章 |
| `/blog/` | `blog/index.astro` | 1 | 博客首页 |
| `/blog/page/[page]/` | `blog/page/[page].astro` | 13 | 分页（77/6≈13 页，noindex） |
| `/blog/tag/[tag]/` | `blog/tag/[tag].astro` | 15 | 标签聚合（noindex,follow） |
| `/docs/[...slug]/` | `docs/[...slug].astro` | 14 | 文档 |
| `/docs/` | `docs/index.astro` | 1 | 文档首页 |
| `/markets/` | `markets/index.astro` | 1 | 市场对比（30 市场动态） |
| `/data/vehicles.json` | `data/vehicles.json.ts` | 1 | 机器可读导出 |
| `/data/brands.json` | `data/brands.json.ts` | 1 | 机器可读导出 |
| `/data/tariffs.json` | `data/tariffs.json.ts` | 1 | 机器可读导出 |
| `/data/source-master.json` | `data/source-master.json.ts` | 1 | 机器可读导出 |
| `/robots.txt` | `robots.txt.ts` | 1 | |
| `/rss.xml` | `rss.xml.ts` | 1 | |

**索引范围内 URL 估算**：约 517（车型）+ 72（品牌）+ 77（博客）+ 14（文档）+ ~16（静态）+ 1（市场）+ 4（数据端点）= **~701 个可索引页面**（不含 noindex 的分页/标签，不含 .md 变体是否入 sitemap 取决于 sitemap filter）。

### 1.3 Sitemap 生成逻辑（`astro.config.mjs`）
- 用 `@astrojs/sitemap`，输出 `sitemap-index.xml`（`_headers` 中 `Link: </sitemap-index.xml>; rel="sitemap"`）。
- filter 排除：`/blog/page/`、`/blog/tag/`，以及 feature flag 关闭的 `/changelog`、`/testimonials`、`/roadmap`（三者均已关）。
- **注意**：`.md` 变体路由（`/vehicles/[slug].md`、`/blog/[slug].md`）未被 filter 排除，理论上会进 sitemap——需在 Phase 7 确认是否应排除机器可读变体。

### 1.4 重定向（`public/_redirects`）
- `electricvehiclehub.top/index.php`、`/index.htm` → 首页 301
- `/sitemap.xml` → `/sitemap-index.xml` 301
- `www.*` → 裸域 301
- `/blog/page/1/` → `/blog/` 301
- `/landed-cost-calculator/` → `https://electricvehiclehub.net/landed-cost-calculator/` 跨域 301（计算器已迁 .net）

---

## 2. 共享层盘查

| 共享项 | 文件 | 状态 |
|---|---|---|
| 站点名 | `src/config/site.ts` `name` | **`'EVHub Top'`（默认值，P0 残留）** |
| 站点 URL | `site.ts` `url` | **`https://electricvehiclehub.top`（默认值，非 chinaevmart.com）** |
| 站点描述 | `site.ts` `description` | "…across 72 brands" |
| 作者 | `site.ts` `author` | `Wei Wang` |
| Logo | `site.ts` `logo` → `public/logo.svg` | **SVG 内嵌「EV」「Hub」文字（P0 残留）** |
| OG 图 | `ogImage` → `/images/og-image.png` | 存在 |
| 公司 | `site.ts` `company` | Chengguang Energy / 锦州成光电源，邮箱 `info@electricvehiclehub.top` |
| 导航 | `navigation.ts` | Header: Home/Vehicles/Brands/Guides(blog)/Docs；Footer 5 列 + legal 7 项 |
| 页脚 | `Footer.astro` | 品牌列用 `siteConfig.description`（72 brands 描述） |
| 面包屑 | `SEO.astro` BreadcrumbList + 各页可见面包屑 | 车型页 4 级、品牌页 3 级 |
| Schema | `SEO.astro` | WebSite + Organization + BreadcrumbList + Article（博客）+ 车型页自有 Vehicle JSON-LD |
| Canonical | `SEO.astro` | `new URL(pathname, siteConfig.url)` — **基于 electricvehiclehub.top，非 chinaevmart.com** |
| robots | `robots.txt.ts` + `BaseLayout.astro` | Allow all；`PUBLIC_INDEXABLE` 控制预览 noindex |
| 站点统计 | `lib/site-stats.ts` | 单一数据源，构建期从集合推导（良好） |

### 2.1 Robots / Indexability 细节
- `BaseLayout.astro`：`PUBLIC_INDEXABLE === '1'` 才放开索引，否则全站 `noindex,nofollow`（.pages.dev 预览过渡期）。
- 博客标签页 `robots="noindex,follow"`；分页页无 robots 属性（依赖 sitemap filter + 可能无 noindex）。
- `_headers`：CSP、HSTS、X-Frame-Options、Referrer-Policy 已配置。

---

## 3. 数据 Schema 盘查

### 3.1 内容集合 schema（`src/content.config.ts`）
**vehicles** 集合字段（核心）：
- 必填：`title, description, slug, brand, type, powertrain, price_usd, publishedDate, author`
- 默认值：`price_type: 'China ex-factory price (MSRP)'`（zod default）、`currency: 'USD'`、`fast_charge: null`、`landed_cost_markets: []`、`tags: []`
- 可选深档字段（EVHub Top 五段模板）：`trim, range_wltp_km, fob_price_usd_min/max, battery_type, drive_type, motor_type, total_power_kw, battery_thermal, heat_pump, suspension_front/rear, brakes, drag_coefficient, gross_weight_kg, ground_clearance_mm, trunk_l, charging_interface, charging_adapter, infotainment_language, network_bands, certification_notes, hs_code`
- 数据质量字段：`data_tier, data_source, data_updated, data_reviewed, verification_status, quality_tier, confidence, family`

**brands** 集合字段：`title, description, brand_name, established, parent_manufacturer, parent_location, parent_founded, website, model_count, publishedDate, tags`

### 3.2 数据文件（`src/data/*.json`）与引用关系

| 文件 | 记录数 | 被引用？ |
|---|---|---|
| `vehicle-master.json` | 517 | ❌ **孤儿文件**（无任何 import） |
| `brand-master.json` | 72 | ❌ **孤儿文件** |
| `technical-master.json` | 137 | ❌ **孤儿文件** |
| `regulatory-master.json` | 66 | ❌ **孤儿文件** |
| `market-master.json` | 30 | ❌ **孤儿文件** |
| `entity-graph.json` | 8 实体 | ❌ **孤儿文件** |
| `source-master.json` | 8 来源 | ✅ `data/source-master.json.ts` |
| `tariffs.json` | 30 市场 | ✅ `markets/index.astro` + `data/tariffs.json.ts` |

**关键发现**：`vehicle-master.json` / `brand-master.json` 是**旧的单文件数据层，已被内容集合（`src/content/vehicles/*.md`、`brands/*.md`）取代**，但文件仍保留在仓库中。`vehicle-master.json` 与 frontmatter 存在**数据漂移**（见 §5 各假设）：

| 差异点 | vehicle-master.json | frontmatter（实际渲染源） |
|---|---|---|
| powertrain 计数 | BEV 286 / PHEV 154 / EREV 58 / HEV **15** / ICE 3 / **Unknown 1** | BEV 286 / PHEV 154 / EREV 58 / HEV **16** / ICE 3 |
| hongqi-guoya | powertrain=`Unknown` | powertrain=`HEV` |
| 字段命名 | `body_type` | `type` |
| 字段命名 | `range_standard` | `range_cltc_km` / `range_wltp_km` |
| 字段命名 | `source` / `source_url` | `data_source` / `image_source` |

### 3.3 默认值 / 回退值清单
- `price_type` → zod default `'China ex-factory price (MSRP)'`（**517/517 车型 frontmatter 均未显式声明 price_type**，全部靠默认值）→ 见假设③
- `currency` → default `'USD'`（frontmatter 全部 `currency: "USD"`）
- `fast_charge` → default `null`
- `fob_price_usd_min/max` → schema 存在但 **0/517 车型有值**（全部为空）
- `range_wltp_km` → 9/517 有值
- `total_power_kw` → 14/517 有值
- `trim` → 81/517 有值
- `hs_code` → 全部有值，渲染层有 powertrain 回退逻辑（BEV→87038000，PHEV/EREV/HEV→870340）
- `data_reviewed` → 517/517 为 `false`（**无一车型标记已复核**）

---

## 4. 旧品牌残留扫描（逐项证据）

> 假设核验：**真实且全站系统级，P0**。生产域 chinaevmart.com 未在任何源码中被引用；全站品牌仍是「EVHub Top / EV Hub / electricvehiclehub.top」。

### 4.1 站点元数据（源头）
- `src/config/site.ts:14` → `name = import.meta.env.SITE_NAME || 'EVHub Top'` ← **默认品牌名**
- `site.ts:22` → `url = import.meta.env.SITE_URL || 'https://electricvehiclehub.top'` ← **默认 URL**
- `site.ts:48` → `company.email = 'info@electricvehiclehub.top'`
- `site.ts:57-58` → `privacyEmail/legalEmail = *@electricvehiclehub.top`
- `.env.example:7` → `SITE_URL=https://electricvehiclehub.top`；`:10` → `SITE_NAME=EVHub Top` ← **生产环境若按此模板配置，即解释了线上「EVHub Top」标题**

### 4.2 残留分类统计（`grep -rio` 口径，去重前原始命中）

| 目录 | 命中数 | 类型 |
|---|---|---|
| `src/content/vehicles` | 601 | `data_source: "EV Hub catalog…"`（504）+ `image_credit: "EV Hub original illustration"`（42）+ 混合（55） |
| `src/content/blog` | 487 | 正文「EV Hub landed-cost / EV Hub tariff / EV Hub analysis team」等 |
| `public` | 56 | `llms.txt` 标题「# CNEVhub」+ 全篇 electricvehiclehub.top 链接 |
| `src/pages` | 40 | about/authors/methodology/landed-cost-methodology/markets/vehicles 模板正文 |
| `src/config` | 19 | site/navigation/contact |
| `src/content/docs` | 16 | 文档正文「EV Hub is a data platform…」 |
| `src/data` | 8 | entity-graph.json `name: "EV Hub"` 等 |
| `src/lib` | 1 | `brand-label.ts` 正则 `/EV Hub original/i` |

### 4.3 逐项品牌残留证据清单

| 位置 | 具体残留 | 严重度 |
|---|---|---|
| 站点名 `site.ts` | `EVHub Top`（默认值） | P0 |
| 站点 URL `site.ts` / `astro.config.mjs` | `electricvehiclehub.top` | P0 |
| Logo `public/logo.svg` | `<text>EV</text><text>Hub</text>` | P0 |
| `llms.txt` | 标题 `# CNEVhub` + 「315 models across 58 brands」（过时） | P0 |
| 车辆 data_source（504 文件） | `"EV Hub catalog + manufacturer specs…"` | P1 |
| 车辆 image_credit（42 文件） | `"EV Hub original illustration"` | P1 |
| 博客正文（77 篇中多数） | 「EV Hub landed-cost records / EV Hub — tariff / EV Hub analysis team」 | P1 |
| 文档正文 | 「EV Hub is a data platform for anyone importing…」 | P1 |
| `contact.ts` FAQ | 「No. EV Hub is an independent information platform…」 | P1 |
| `about.astro` | 「EV Hub exists to solve…」 | P1 |
| `authors.astro` | 「Who writes EV Hub…」「He writes EV Hub's landed-cost analysis」 | P1 |
| `landed-cost-methodology.astro` | 「EV Hub landed-cost estimates」 | P1 |
| `entity-graph.json` | `id: "ev-hub"` `name: "EV Hub"` `url: electricvehiclehub.top` | P2 |
| `site.ts` 社交链接 | `twitter: https://x.com/cnevhub` `github: …/CNEVhub` | P2 |
| `navigation.ts` / `contact.ts` / `site.ts` 注释 | 「EV Hub」文件头注释 | P3 |

### 4.4 反证（chinaevmart 是否已被引用）
- 全仓 `grep -ri "chinaevmart\|China EV Mart\|ChinaEVMart"` → **0 命中**。
- 结论：**品牌迁移（EVHub Top → China EV Mart）尚未开始**，Phase 2 是全新工作。

---

## 5. 数据质量假设逐项核验

### 假设① EV/PHEV/EREV/HEV/ICE 分类混乱

**判定：真实，但规模有限（P1/P2）。**

- 分类**枚举本身存在**：BEV 286 / PHEV 154 / EREV 58 / HEV 16 / ICE 3（frontmatter 源）。
- **ICE（3 台）出现在「Chinese EV product database」中属分类越界**：`changan-nevo-lamore`（Sedan, $11,110）、`changan-x5-plus`（SUV, $8,400）、`wuling-jiachen`（MPV, $16,310）。
- **HEV（16 台）** 属于「混动但非插电/增程」，与「new-energy vehicle」定位边界模糊：aeolus-huge、aeolus-mage、changan cs55/cs75/eado/uni-v HEV、gac emkoo/empow/gs8、geely xingrui-l、haval jolion-pro/shenshou、hongqi-guoya（$197,180 旗舰）、wuling asta/nebula/victory。
- **`hongqi-guoya` 数据漂移**：vehicle-master.json 标 `Unknown`，frontmatter 标 `HEV`（孤儿文件与源不一致的实证）。
- 首页 `index.astro` 变量注释写「// 58 品牌墙」但数组实为 72 项（注释与数据不符，P3）。
- `site-stats.ts` 将 HEV/ICE 归入 `otherPowertrainCount`，未在 UI 单独呈现分类——**分类存在但首页筛选只显示 BEV/PHEV/EREV/HEV/ICE 原始值，无「新能源 vs 燃油」区分文案**。

**受影响**：19 条记录（16 HEV + 3 ICE），首页 powertrain 筛选 chips、车型详情 powertrain 标签。

**建议修复**：① 明确数据库边界——若定位「中国新能源车」，ICE 3 台应移除或显式标注「燃油对照」；② 统一 powertrain 枚举与术语表（HEV vs 普通混动 vs 增程）；③ 删除/同步 `vehicle-master.json` 消除 Unknown 漂移。

---

### 假设② 可疑重复/默认价格（跨不相关车型同值）

**判定：真实，规模可观（P1）。**

全量聚类扫描：517 条记录，321 个不同价格值。**22 个价格值被 ≥4 个不同品牌共享**，最严重者：

| 价格 | 记录数 | 跨品牌数 |
|---|---|---|
| $13,860 | 11 | 10（aion/bestune/byd/forthing/geely-galaxy/jac/landian/mg/ora/wuling） |
| $21,100 | 9 | 8（byd/forthing/gac-motor/geely-galaxy/jetour/kaicene/leapmotor/ora） |
| $15,460 | 8 | 6 |
| $14,060 | 8 | 6 |
| $20,820 | 7 | 6 |
| $32,370 | 7 | 6 |
| $22,510 | 7 | 6 |

**但需谨慎定性**：这些多为中国车市常见的整数人民币起步价换算（如 ¥99,800 ≈ $13,860、¥151,800 ≈ $21,100），**可能是巧合而非「默认值填充」**。证据不足以证明是「未填值兜底」，但**至少证明价格精度可疑、且多品牌撞价未经交叉核验**。`data_reviewed` 517/517 = false 进一步削弱可信度。

**建议**：对 22 个高频撞价值逐一溯源（官方价目表/媒体报价），无法核验者标注 `verification_status`；不改数据，仅登记待核。

---

### 假设③ ex-factory 价冒充 FOB 价

**判定：口径标注正确，无冒充（假设不成立，P3 仅登记口径一致性）。**

- 517/517 车型 `price_type` 依赖 zod 默认值 `'China ex-factory price (MSRP)'`——**明确标注 ex-factory，未标 FOB**。
- 车型详情页 `[slug].astro` 标题处渲染「starting price (ex-factory China)」；`fobRange` 变量在无 fob 数据时回退显示「≈ $X (ex-factory reference)」——**诚实回退，未伪装 FOB**。
- `.md` 变体输出「Price (ex-factory China)」。
- `fob_price_usd_min/max` 字段 0/517 有值——**没有 FOB 数据可冒充**。
- 唯一需登记：`authors.astro` 有「FOB-to-landed pricing」表述、`landed-cost-methodology.astro` 有「factory or FOB price」表述，均属正确区分口径，**无需修**。

**结论**：假设③ 在源码中**不成立**。ex-factory 标注规范。（注：`llms.txt` 与历史博客用「base price」表述，属旧 .net 口径残留，见假设⑥。）

---

### 假设④ 重复车型记录 / 品牌计数不一致 / 车系关系错误

**判定：不存在（假设不成立）。**

- `vehicle_id` 重复：0。
- `model` 名重复：0。
- 品牌 frontmatter `model_count` vs 实际车型数：**0 偏差**（72/72 一致）。
- 品牌集合 vs 车辆记录品牌：**双向无孤儿**（无缺品牌、无多品牌）。
- `family`（车系）字段：517/517 有值，但**未做车系父子关系校验**（如 BYD Seal 系 vs Seal 05/06/07 DM-i 的归属）——建议 Phase 3 补充 family 关系审计脚本，当前未发现错误但**未验证**。

**结论**：假设④ 中「重复记录、品牌计数不一致」不成立；「车系关系」**证据不足**（字段存在但无校验规则）。

---

### 假设⑤ Overview 同构句残留

**判定：真实，全站规模（P1）。**

- 517/517 车型正文含 `## Overview` 段落。
- 对 Overview 句子做数字归一化聚类，出现**大量模板同构句**（同句式跨不同车型重复 3–5 次）：

> 「As a value-oriented SUV battery-electric, it starts at $N,N ex-factory.」（4 次）
> 「With a $N,N ex-factory price, the SUV fully electric reads as mid-tier.」（4 次）
> 「Priced from $N,N ex-factory, the SUV plug-in hybrid electric falls in the value tier.」（4 次）
> 「As a budget SUV plug-in hybrid electric, it starts at $N,N ex-factory.」（3 次）
> 「For this SUV battery-electric, Germany's estimate carries a N% countervailing duty over the N% base tariff — the lowest landed premium is Qatar at roughly +N%…」（3 次）

- 描述字段（frontmatter `description`）**517 条全部唯一但高度同构**，如「The {Model} is {BRAND}'s {type} {powertrain}, offering a CLTC-rated range of N km, N kWh of battery, N kW of motor power, and LFP chemistry…」——语义模板化。

**受影响**：517 车型详情页 Overview + 描述字段。

**建议**：Phase 4 重写 Overview 为差异化编辑内容；描述字段保留结构化但减少同构冗余。这是「原创性/同质化」风险，非错误。

---

### 假设⑥ 进口税计算不一致（landed-cost 字段 vs 已知税率）

**判定：真实，结构性残留（P1）。核心矛盾：.top 已去计算功能，但 landed-cost 数据字段仍全量存在。**

证据链：
1. **计算器已迁走**：`_redirects` 将 `/landed-cost-calculator/` 301 到 `.net`；git log `differentiate-calculator` 提交「remove /landed-cost-calculator/ from .top」。
2. **但数据字段仍在**：517/517 车型 frontmatter 含 `landed_cost`（德国明细 breakdown）+ `landed_cost_markets`（30 市场完整 landed 表）。
3. **渲染层仍在消费**：
   - `vehicles/[slug].md.ts` → 输出「## Landed Cost by Market」+「## Landed Cost Breakdown」表格（**机器可读变体仍暴露 landed-cost**）。
   - `brands/[slug].astro` → 品牌页车型卡渲染「Landed DE $X (+N%)」。
   - `data/vehicles.json.ts` → 导出 `landed_cost_markets`。
   - `markets/index.astro` → 仍渲染 30 市场关税对比表。
   - `landed-cost-methodology.astro` → 仍存在整页方法论。
4. **车型 HTML 详情页已降权**：`[slug].astro` 的「Market Compliance」区改为「landed-cost lives on electricvehiclehub.net」外链，不再渲染 landed 表——**但 .md 变体、品牌页、JSON 端点仍在渲染**。

**口径核查（税率一致性）**：
- `tariffs.json` `cvd_scope`：CVD 仅 EU + 仅 BEV；非 EU 市场、PHEV/EREV/HEV 无 CVD——**逻辑正确**。
- `brand_cvd`：BYD 17% / Geely 系 18.8% / SAIC 系 35.3% / Tesla 7.8% / 其他 20.7%——与 `cvd_meta.note` 一致。
- **风险**：`cvd_meta.verification_status: "unknown"`，`verification_note` 明确记录「2026-09-17 权威复核失败（EUR-Lex 被 WAF 拦截），税率保持既有值，待人工复核」——**税率未经权威复核**。
- `market-master.json` 有 `notes` 字段记录巴西 35%（Jul 2026）、墨西哥 50%（Jan 2026）、加拿大「100% surtax repealed Mar 2026」等时点性规则——**但这些在孤儿文件中，实际渲染用 tariffs.json**。

**结论**：假设⑥ 成立。矛盾不是「税率算错」而是「**.top 宣称已去计算功能，但 landed-cost 数据/渲染在 4 个面（.md 变体、品牌页、JSON 端点、市场页）仍存活**」，且税率 `verification_status: unknown`。需在 Phase 5 决策：彻底移除 .top 的 landed-cost 字段，还是保留为「数据存档」并统一口径。

---

### 假设⑦ 过期规格/价格/法规/市场可得性

**判定：部分真实，证据不足（P2）。**

- **数据新鲜度字段存在且近期**：`data_updated` 分布为 2026-10-21（477）+ 2026-10-22（40），近 517/517 标注近期更新。
- **但 `data_reviewed: false`（517/517）** + `verification_status`：None 477 / partial 36 / unverifiable 2 / verified 2——**「已复核」仅 2 条，「verified」仅 2 条**，绝大多数标注「未复核」。
- **`price_usd` 全为 2026-09-07 采集批次**（vehicle-master.json `generated: 2026-09-14`、`data_updated: 2026-09-07`），价格距今 ~1.5 月，无逐条刷新证据。
- **`byd-seal.md` 数据矛盾实证**：description 写「CLTC-rated range of 450 km」但 frontmatter `range_cltc_km: 550`——**描述与字段不一致**（1 处确认，同类可能更多）。
- 法规时点规则（巴西/墨西哥/加拿大）存在但未经权威复核（同假设⑥）。

**结论**：假设⑦ 「过期」**证据不足**（更新日期字段近期，但无复核状态支撑）；「规格/价格与描述不一致」**真实**（至少 byd-seal 1 处）；建议 Phase 3 加一致性校验脚本全量扫描。

---

## 6. 优先级问题登记表（Issue Register）

### P0（品牌迁移阻断项 — 生产域标题错误）
| # | 问题 | 证据 | 受影响 | 建议修复 | 回归风险 |
|---|---|---|---|---|---|
| P0-1 | 站点名/URL 仍是 EVHub Top / electricvehiclehub.top | `site.ts` name/url 默认值；`.env.example`；线上标题「EVHub Top — Chinese EV Product Database」 | 全站 title/OG/schema/canonical | Phase 2：设 `SITE_NAME=China EV Mart`、`SITE_URL=https://chinaevmart.com/` 于生产环境变量 + 更新源码默认值 | 低（纯配置+默认值），但需先定品牌名规范 |
| P0-2 | Logo SVG 内嵌「EV」「Hub」文字 | `public/logo.svg` | 全站 header/footer logo | 重做 logo 文字为「China EV Mart」或纯图形 | 低（替换 SVG） |
| P0-3 | llms.txt 标题「CNEVhub」+ 过时计数「315 models / 58 brands」 | `public/llms.txt` | AI/LLM 抓取入口 | 更新标题 + 计数为 517/72 | 低 |
| P0-4 | canonical/schema/og:url 基于 electricvehiclehub.top | `SEO.astro` `canonicalURL = new URL(pathname, siteConfig.url)` | 全站 canonical | 修 `siteConfig.url` 后自动生效 | 低（单点） |

### P1（数据质量 + 品牌残留批量项）
| # | 问题 | 证据 | 受影响 | 建议修复 | 回归风险 |
|---|---|---|---|---|---|
| P1-1 | 504 车型 data_source 含「EV Hub catalog」 | `grep data_source` | 504 记录 | 批量替换为「China EV Mart catalog」 | 低（文案） |
| P1-2 | 42 车型 image_credit 含「EV Hub original illustration」+ `brand-label.ts` 正则 | grep + `brand-label.ts:50` | 42 记录 + 1 代码 | 批量替换 + 同步正则 | 低 |
| P1-3 | 博客/文档正文大量「EV Hub」措辞 | grep blog 487 / docs 16 | ~77 文章 + 14 文档 | Phase 2 术语表批量替换（保留历史准确引用） | 中（正文语义需逐句核对） |
| P1-4 | Overview 同构句（模板化文案） | §5 假设⑤聚类 | 517 车型 | Phase 4 差异化重写 | 中（大量编辑） |
| P1-5 | 22 个价格值跨 ≥4 品牌撞价（含 $13,860×11、$21,100×9） | §5 假设②聚类 | ~110 记录 | 逐值溯源，无法核验标 unverifiable | 低（不改值，加标注） |
| P1-6 | landed-cost 字段在 .top 残留（.md 变体/品牌页/JSON 端点/市场页仍渲染） | §5 假设⑥ | 517 记录 + 4 渲染面 | Phase 5 决策：移除或统一存档 | 高（跨数据+渲染层） |
| P1-7 | 进口税税率 `verification_status: unknown`（EUR-Lex 复核失败） | `tariffs.json cvd_meta` | 30 市场 CVD | Phase 5 人工权威复核 | 中 |
| P1-8 | `data_reviewed: false` 517/517 + verification 几乎全 None | §5 假设⑦ | 517 记录 | Phase 3 建立复核流水线 | 低（加字段值） |

### P2（数据一致性 + 孤儿资产）
| # | 问题 | 证据 | 受影响 | 建议修复 | 回归风险 |
|---|---|---|---|---|---|
| P2-1 | `vehicle-master.json`/`brand-master.json` 等 6 个 JSON 孤儿文件与内容集合数据漂移 | §3.2（hongqi-guoya Unknown vs HEV 等） | 6 文件 | 删除或改造为生成物（构建期从集合导出） | 低（当前无引用） |
| P2-2 | `byd-seal.md` description(450km) ≠ range_cltc_km(550) | §5 假设⑦ | ≥1 记录 | 全量 description↔字段一致性校验脚本 | 低 |
| P2-3 | ICE 3 台 / HEV 16 台分类边界 | §5 假设① | 19 记录 | 明确数据库边界 + 术语表 | 中（涉及目录定位） |
| P2-4 | 首页 `// 58 品牌墙` 注释 vs 72 项数组 | `index.astro` | 1 文件 | 改注释 + 数组改动态（从集合推导） | 低 |
| P2-5 | `family` 车系字段无父子校验规则 | `content.config.ts` | 517 记录 | Phase 3 加 family 关系校验 | 低 |
| P2-6 | 社交链接 x.com/cnevhub、github CNEVhub | `site.ts` | 2 链接 | 更新或移除 | 低 |
| P2-7 | `entity-graph.json` `id:"ev-hub"` 品牌名残留 | `entity-graph.json` | 1 文件 | 更新实体名 | 低 |

### P3（低优先/登记项）
| # | 问题 | 建议 |
|---|---|---|
| P3-1 | ex-factory vs FOB 口径 | 已正确标注，无需改（假设③不成立） |
| P3-2 | 文件头「EV Hub」注释（site/navigation/contact） | 顺手清理 |
| P3-3 | `.md` 变体路由是否应排除 sitemap | Phase 7 确认 |

---

## 7. 问题登记表规模汇总

| 严重度 | 数量 | 性质 |
|---|---|---|
| **P0** | 4 | 品牌迁移阻断（生产域标题错误为核心） |
| **P1** | 8 | 数据质量 + 品牌残留批量 + landed-cost 结构性残留 |
| **P2** | 7 | 数据一致性 + 孤儿资产 |
| **P3** | 3 | 登记项 |
| **合计** | **22** | |

---

## 8. 未覆盖声明（Final Instruction 要求）

- 本次审计**覆盖**：全部 517 车型 + 72 品牌 + 86 博客 + 14 文档 + 16 静态页的前置源码/数据/模板层，以及全仓品牌残留 grep。
- **未覆盖**：实际 HTTP 渲染结果（未跑 build/dev server 抓取每页 HTML）、线上 chinaevmart.com 逐页抓取（仅采信任务书提供的首页标题实测）、逐条税率权威复核（需 EUR-Lex 等外部源）。
- **分离声明**：上述「已验证事实」均有文件/行号证据；「推断风险」为 P1/P2 中标注「建议/需决策」项；「推荐」为 Phase 2–5 的修复方向，未经实施。

---

*报告路径：`docs/chinaevmart-p1-baseline.md`*
*本阶段零编辑：未改动任何源码/数据文件。*
