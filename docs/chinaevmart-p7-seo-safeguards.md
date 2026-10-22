# ChinaEVMart Phase 7 — Technical SEO Safeguards Verification

> 仓库：`electricvehiclehub.top`（chinaevmart.com 代码库）
> 阶段：Phase 7 · 技术 SEO 护栏验证
> 日期：2026-10-22 · 验证对象：构建产物 `dist/`（899 页）+ 源码配置
> 方法：源码审查 + `npm run build`（exit 0）+ `dist/` 全量 grep 抽检

---

## 0. 结论摘要

| 检查项 | 结果 |
|---|---|
| ① 关键路由 HTTP 状态与渲染 | ✅ 899 页构建成功（静态构建验证；未跑 live server 逐页 HTTP 抓取） |
| ② canonical 与域名一致性 | ✅ 全站 canonical 均 `https://chinaevmart.com/...`（0 非目标域残留） |
| ③ sitemap 收录/排除 | ✅ 700 URL；.md 变体 / blog 分页 / tag 页 / data 端点均正确排除 |
| ④ robots 指令与索引性 | ⚠️ 预览 noindex（预期）；生产放开步骤见 §4 |
| ⑤ 内链导航/面包屑/孤儿页 | ⚠️ 1 孤儿页（/markets/）；面包屑 JSON-LD 已修 |
| ⑥ title/desc/heading 准确性 | ⚠️ 已修 5 页双 `<title>` + 103 页站点名重复 |
| ⑦ schema 与可见内容一致性 | ⚠️ 已移除失效 SearchAction；sameAs 残留待人工 |
| ⑧ 重复 URL/查询参数/薄筛选页 | ✅ 无索引筛选 URL；.md 变体已加 canonical header |

**本批当场修复（低风险）：5 项 · 列清单待人工：5 项 · 验证通过项：4 项**

---

## 1. ① 关键路由 HTTP 状态与渲染

- `npm run build` → **899 pages, exit 0**（.top 全量静态构建，含 517 车型 + 72 品牌 + 77 博客 + 14 文档 + 16 静态页）。
- 关键路由均产出 `dist/*/index.html`：首页、`/vehicles/`、`/vehicles/[slug]/`、`/brands/`、`/brands/[slug]/`、`/blog/`、`/blog/[slug]/`、`/docs/`、`/docs/[slug]/`、`/markets/`、`/about/`、`/methodology/`、`/contact/`。
- 404 / 500 静态页存在（`dist/404.html` / `dist/500.html`）。
- **限制**：本批未启动 dev/preview server 逐页抓取 HTTP 状态码，属静态构建产物验证。live HTTP 逐页确认（含 200/301/404 实际返回、`.md` 变体 Content-Type）列为待人工项（§8 H-1）。

## 2. ② canonical 与域名一致性

- `src/config/site.ts`：`url = import.meta.env.SITE_URL || 'https://chinaevmart.com'` ✅；`.env.example` `SITE_URL=https://chinaevmart.com` ✅。
- `SEO.astro`：`canonicalURL = new URL(Astro.url.pathname, siteConfig.url)` → 全站 canonical 基于 chinaevmart.com。
- **全量抽检**：`dist/` 所有 `index.html` 的 `<link rel="canonical">` **0 命中非 chinaevmart.com** ✅。
- `og:url` / JSON-LD `url` / `@id` 同源自 siteConfig.url ✅。
- `public/_redirects`：`www.* → 裸域 301`、`/sitemap.xml → /sitemap-index.xml 301`、`/index.php|.htm → / 301`、`/blog/page/1/ → /blog/ 301` 均指向 chinaevmart.com ✅。

## 3. ③ sitemap 收录/排除逻辑

`astro.config.mjs` sitemap filter + `dist/sitemap-0.xml` 实测：

| 类 | 应排除 | 实测 |
|---|---|---|
| 车型页 + 目录 | 收录 | 518（517 + `/vehicles/`） |
| 品牌页 + 目录 | 收录 | 73（72 + `/brands/`） |
| 博客正文 + 首页 | 收录 | 78（77 + `/blog/`） |
| 文档 + 首页 | 收录 | 15（14 + `/docs/`） |
| 静态页（about/methodology/…） | 收录 | 16 |
| `/blog/page/N/` 分页 | **排除** | ✅ 0 |
| `/blog/tag/x/` 标签 | **排除** | ✅ 0 |
| `/vehicles/*.md` / `/blog/*.md` 机器可读变体 | **排除** | ✅ 0 |
| `/data/*.json` 端点 | **排除** | ✅ 0 |
| **合计** | — | **700** ✅ |

- sitemap-index.xml 单索引指向 `sitemap-0.xml`，域名 chinaevmart.com ✅。
- `_headers` 输出 `Link: </sitemap-index.xml>; rel="sitemap"` ✅。

## 4. ④ robots 指令与索引性（PUBLIC_INDEXABLE 开关现状）

- `robots.txt.ts`：`User-agent: *` + `Allow: /` + `Disallow: /api/`（无 /api 路由，Disallow 为无害空规则）+ 显式放行 GPTBot/ClaudeBot/PerplexityBot/Google-Extended 等 AI crawler + `Sitemap: https://chinaevmart.com/sitemap-index.xml` ✅。
- `BaseLayout.astro`：`indexable = import.meta.env.PUBLIC_INDEXABLE === '1'`；非 1 时全站 `noindex,nofollow`。
- **现状**：构建未设 `PUBLIC_INDEXABLE` → **全站渲染 `noindex,nofollow`**（预览过渡期，符合方案 C 预期，非缺陷）。
- **生产域名上线放开步骤（待人工执行）**：
  1. Cloudflare Pages → 项目环境变量设 `PUBLIC_INDEXABLE=1`（同时确认 `SITE_URL=https://chinaevmart.com`、`SITE_NAME=China EV Mart`）；
  2. 重新部署构建，抽检 `/`、`/vehicles/byd-seal/` 渲染 `<meta name="robots">` 消失或为页面自有指令；
  3. 博客分页/tag 页自有 `robots="noindex,follow"` 在放开后正确生效（BaseLayout 逻辑：`indexable ? robots : 'noindex, nofollow'`，放开后透传页面自有值）✅ 已核逻辑；
  4. Search Console 提交 chinaevmart.com 验证 + sitemap，观察索引增长。

## 5. ⑤ 内链导航 / 面包屑 / 孤儿页

- 主导航（Header/Footer）覆盖 Home/Vehicles/Brands/Guides/Docs/About/Methodology/Contact/legal 全链路 ✅。
- **孤儿页扫描结果**：

| 页面 | 站内入链数 | 状态 |
|---|---|---|
| /markets/ | **0** | ⚠️ **孤儿页**（仅 sitemap 收录，无导航/页脚/正文链接） |
| /landed-cost-methodology/ | 2 | 弱链（仅 methodology 页 note 提及） |
| 其余静态页 | ≥1 | ✅（footer legal/company 列覆盖） |

- **面包屑修复**：品牌页 `brands/[slug].astro` 可见面包屑为 3 级（Home / Brands / {brand}），但 SEO JSON-LD 此前为默认 2 级 → **本批已传 3 级 breadcrumb prop 修复** ✅。车型页 4 级面包屑本已一致 ✅。

## 6. ⑥ title / description / heading 准确性

**本批修复 2 类标题缺陷**：

| 缺陷 | 根因 | 影响页数 | 修复 |
|---|---|---|---|
| 双 `<title>` 标签 | 页面同时渲染 `<SEO>` + `<MarketingLayout>`（后者内含 BaseLayout→SEO），产生两个 title/canonical/JSON-LD | 5 页（authors / methodology / landed-cost-methodology / editorial-independence / image-credits） | 移除冗余 `<SEO>` 组件，title+description 并入 MarketingLayout ✅ |
| 站点名重复进标题 | 页面 title prop 已含 `{siteConfig.name}`（如 `About - China EV Mart`），SEO.astro 又追加 `| China EV Mart` → `About - China EV Mart | China EV Mart` | **103 页**（全博客 + 文档 + 部分静态页） | `SEO.astro` 加去重：title 已含站点名则不追加 ✅ |

- 修复后全量抽检：`dist/` 0 双 `<title>`、0 站点名重复标题 ✅。代表性 title 现在形如 `About - China EV Mart`、`BYD Seal | China EV Mart`、`China EV Mart — Chinese New-Energy Vehicle Database`。
- heading：车型页单 H1（`rehypeDropLeadingH1` 插件 + 模板 H1 唯一）✅；博客/文档 H1 由 layout 统一渲染，正文首个 H1 被插件去除 ✅。

## 7. ⑦ schema 与可见内容一致性 + 实体关系有效性

| Schema | 检查 | 结果 |
|---|---|---|
| Organization | name=Chengguang Energy / legalName / url=chinaevmart.com / address Jinzhou CN / contactPoint | ✅ 与 about/site.ts 一致，**无虚构资质** |
| Organization `sameAs` | `https://x.com/cnevhub` + `https://github.com/martinxionbiotech-max/CNEVhub` | ⚠️ **遗留 CNEVhub/旧品牌**（P2-6 未清，待人工） |
| WebSite `potentialAction.SearchAction` | target=`/search?q=`，但**站内无 /search 路由**（404） | ⚠️ **本批已移除 SearchAction** ✅（失效实体） |
| BreadcrumbList | 车型 4 级 / 品牌 3 级 / 其他 2 级 | ✅ 与可见面包屑一致（品牌页本批修复） |
| Article（博客） | headline/datePublished/author/publisher/mainEntityOfPage | ✅ 与可见内容一致 |
| Vehicle（车型页） | name/brand/bodyType/fuelType/vehicleEngine + `offers`(price+currency+description) | ✅ 无虚构 rating/reviews/availability/seller；offers 仅含真实 price_usd + 诚实描述「reference starting price — confirm with a supplier quote」 |
| Dataset（首页） | name/creator/license/variableMeasured | ✅ 与可见内容一致 |
| FAQPage（博客正文 FAQ 段） | 从正文 `## Frequently asked questions` 解析 | ✅ 与可见内容一致 |
| Brand 页 Organization | name/foundingDate/parentOrganization | ✅ 数据驱动，无虚构 |

- **不加虚构原则核验**：全站 JSON-LD **无 `rating` / `review` / `availability` / `seller` 字段**，offers 无 `priceValidUntil` 夸大、无库存、无商家 ✅。

## 8. ⑧ 重复 URL / 查询参数变体 / 薄筛选页

- 目录/首页筛选为**纯客户端 JS**，不产生 `?powertrain=` 等查询串 URL（P4a 已核）✅。
- `/blog/page/1/` → `/blog/` 301 消除重复 ✅；`/blog/tag/*` noindex,follow + 不进 sitemap ✅。
- **机器可读 `.md` 变体**（517 车型 + 77 博客 = 594 个）：不进 sitemap（§3 已核），但此前**无 canonical 信号**（HTTP 层），属重复内容风险。**本批已为 `.md` 端点加 `Link: <canonical>; rel="canonical"` header** ✅。
- 无自动对比 URL 矩阵 / 无海量筛选组合页（P4c/P4a 延续）✅。

---

## 9. 异常清单汇总

### 9.1 本批当场修复（低风险，5 项）

| # | 异常 | 严重度 | 修复文件 |
|---|---|---|---|
| F-1 | 5 页双 `<title>`（冗余 `<SEO>` 组件） | P1 | authors / methodology / landed-cost-methodology / editorial-independence / image-credits |
| F-2 | 103 页站点名重复进标题 | P1 | `SEO.astro`（title 去重） |
| F-3 | WebSite SearchAction 指向不存在的 /search | P1 | `SEO.astro`（移除 SearchAction） |
| F-4 | 品牌页 BreadcrumbList JSON-LD 2 级 ≠ 可见 3 级 | P2 | `brands/[slug].astro`（传 3 级 breadcrumb） |
| F-5 | `.md` 变体无 canonical 信号（重复内容风险） | P2 | `vehicles/[slug].md.ts` + `blog/[...slug].md.ts`（加 Link canonical header） |

### 9.2 列清单待人工（5 项）

| # | 异常 | 严重度 | 建议 |
|---|---|---|---|
| H-1 | live HTTP 逐页状态码未验证（仅静态构建验证） | P1 | 部署后 curl 关键路由 + .md 变体 Content-Type 确认 |
| H-2 | Organization `sameAs` 遗留 x.com/cnevhub + github CNEVhub | P2 | 更新为 chinaevmart 对应社交账号，或移除 |
| H-3 | `/markets/` 孤儿页（0 入链但 sitemap 收录） | P2 | 从导航/页脚加链接，或评估是否随 Phase 5 迁移到 .net |
| H-4 | 公司邮箱仍 `info@electricvehiclehub.top`（site.ts/contact.ts/llms.txt） | P2 | 确认 chinaevmart.com 邮箱后统一替换（P1/P2 遗留） |
| H-5 | `landed-cost-methodology.astro` + `markets/index.astro` 整页仍存于 .top | P1 | Phase 5 决策：迁 .net 或明确保留为 .net 公式文档（与 .net 计算器边界） |

---

## 10. 分离声明

- **已验证**：§2 canonical 域名一致性、§3 sitemap 700 排除逻辑、§5 面包屑、§7 schema 一致性、§8 无索引筛选 URL——均有 `dist/` 全量 grep 证据。
- **已修复**：§6 标题 2 类缺陷、§7 SearchAction、§5 品牌面包屑、§8 .md canonical——均 `npm run build` exit 0 + 复抽检通过。
- **推断/待人工**：§9.2 H-1~H-5，均未武断改动（涉及外部账号/邮箱/跨站边界/live 环境）。
- **未覆盖**：live HTTP 逐页状态码、Search Console 实际索引数据（无 GSC）、税率权威复核（Phase 5）。

---

*报告路径：`docs/chinaevmart-p7-seo-safeguards.md`*
