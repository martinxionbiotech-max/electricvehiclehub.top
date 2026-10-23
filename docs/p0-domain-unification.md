# ChinaEVMart P0 — 新旧域名统一与产品定位报告

> 批次：四阶段计划 01 P0 · 仓库：`electricvehiclehub.top`（生产域 chinaevmart.com）
> 执行日期：2026-10-23 · 三域结构：chinaevmart.com=产品信息站（本仓）· electricvehiclehub.net=出口情报站（计算器/关税，跨域 301）· electricvehiclehub-top.pages.dev=预览（noindex）

---

## 0. 结论摘要

| 项 | 结果 |
|---|---|
| 旧域名/旧品牌引用 | ✅ 全仓扫描 + 分类处置（修正 21 处 · 有意保留 7 类） |
| 联系邮箱域 | ✅ `@electricvehiclehub.top` → `@chinaevmart.com`（10 处） |
| 工具域归属 | ✅ 计算器/关税/市场指南=.net · 产品信息/对比/技术=.com，无残留计算功能块 |
| 方法论矛盾 | ✅ 修复 6 处「本仓计算器」第一人称陈述 + 1 处 Cost assumptions 段落 |
| 重定向/canonical/sitemap | ✅ 复核通过（301 目标有效 · canonical/sitemap 全 chinaevmart.com） |
| Build | ✅ 896 页 · exit 0 |
| 提交 | 3 个 `p0-domain-unify-*` commit |

---

## 1. 旧域名全站扫描与分类处置

### 1.1 口径

扫描面：`src/` 源码 + `public/`（llms.txt/_redirects/_headers/OG/alt）+ 根配置文件 + `docs/` 文档 + 注释 + 脚本。
分类规则：**真过时引用**（指向旧域/旧品牌的当前表述）→ 修正为 chinaevmart.com / China EV Mart；**有意的跨域/真实资产引用** → 保留。

### 1.2 修正清单（21 处）

| # | 位置 | 前 | 后 | 依据 |
|---|---|---|---|---|
| 1–4 | `src/config/site.ts` | 注释 + company.email + privacyEmail + legalEmail = `@electricvehiclehub.top` | `@chinaevmart.com` | 旧域废弃，邮箱随生产域统一 |
| 5–9 | `src/config/contact.ts` | email/supportEmail/salesEmail/value/href = `@electricvehiclehub.top` | `@chinaevmart.com` | 同上 |
| 10 | `public/llms.txt` | `Contact: info@electricvehiclehub.top` | `info@chinaevmart.com` | 同上 |
| 11 | `LICENSE` | 标题 `EV Hub — Copyright and Licensing` | `China EV Mart — Copyright and Licensing` | 品牌统一 |
| 12 | `LICENSE` | `https://electricvehiclehub.top/copyright/` | `https://chinaevmart.com/copyright/` | 旧域 URL |
| 13 | `LICENSE` | `credit to EV Hub` | `credit to China EV Mart` | 品牌统一 |
| 14 | `LICENSE` | `https://electricvehiclehub.top/image-credits/` | `https://chinaevmart.com/image-credits/` | 旧域 URL |
| 15 | `THIRD-PARTY-NOTICES.md` | `published on electricvehiclehub.top` | `published on chinaevmart.com` | 旧域 |
| 16 | `package.json` | description `EV Hub — China EV export intelligence…` | `China EV Mart — Chinese EV product database…` | 品牌 + 定位（产品信息站非出口情报） |
| 17 | `content-backlog.md` | `# EV Hub 内容创作 Backlog` | `# China EV Mart 内容创作 Backlog` | 品牌 |
| 18–20 | `scripts/quality-gate.mjs` / `seo-validation.mjs` / `site-consistency.mjs` | `const SITE = 'https://electricvehiclehub.top'` | `https://chinaevmart.com` | 校验脚本对生产域执行 |
| 21 | `scripts/placeholder-scan.mjs` + 上述 3 脚本头部注释 | `EV Hub` | `China EV Mart` | 注释品牌 |

### 1.3 有意保留（跨域/真实资产，不改写）

| 类别 | 内容 | 依据 |
|---|---|---|
| 社交句柄 | `x.com/cnevhub`、`github.com/martinxionbiotech-max/CNEVhub`（site.ts social + JSON-LD sameAs） | 真实账号，运营方更新前不伪造 |
| 姐妹站外链 | `electricvehiclehub.net`（landed-cost-calculator / 首页出口指南卡 / markets 页 / 车型页 export profile / methodology 页） | 差异化定位的合理跨域引用 |
| `_redirects` 跨域 301 | `/landed-cost-calculator/` → `.net/landed-cost-calculator/` | 计算器已迁 .net |
| docs/ 历史报告 | `docs/chinaevmart-p1-baseline.md` 等 22 份迁移报告内的旧域/旧品牌 | 历史审计记录，保留原样 |
| scripts/*.py 一次性脚本 | `inject_deep_profile*.py` 等内的 `EVHub Top`/`EV Hub` | 已执行的历史数据脚本，不改写 |
| `regulatory-master.json` 等数据键 | `evhub_calculation`/`evhub_estimate` enum 键名 | 历史数据约定标识（P2 已定） |

---

## 2. 核心工具域归属确认

功能-域映射核对（三域结构）：

| 功能 | 归属域 | 本仓状态 |
|---|---|---|
| 落地成本计算器 | `.net` | ✅ 已移除，跨域 301 → `.net/landed-cost-calculator/` |
| 关税 / 市场指南 / CVD 表 | `.net`（markets 页跨域外链） | ✅ 本仓 `/markets/` 已降级为跨域外链 + 静态关税参考 |
| 产品信息 / 车型规格 / 品牌 | `.com`（本仓） | ✅ 核心 |
| 对比 / 技术 / 术语表 | `.com`（本仓） | ✅ 核心 |

**残留成本计算功能块检查**：无。`src/components/`、`src/lib/`、`src/styles/` 无 calculator/landed-cost 计算逻辑；`src/pages/landed-cost-calculator.astro` 已不存在（仅 `_redirects` 301）。车型 `.md` 变体仍保留 `landed_cost` 数据字段渲染（P2 定「数据层不动、模板不渲染」，本批不破坏数据）。

**域一致性**：
- `siteConfig.url` = `https://chinaevmart.com`（site.ts / astro.config.mjs / .env.example 三处一致）
- `public/llms.txt` 全部链接 chinaevmart.com ✅
- `robots.txt.ts` Sitemap = `${siteConfig.url}/sitemap-index.xml` ✅
- `_headers` Link sitemap = `/sitemap-index.xml`（相对，随域） ✅
- build 产物 dist/sitemap-index.xml 全部 `https://chinaevmart.com` ✅

---

## 3. 方法论与产品功能矛盾修复

逐条比对 `/methodology/`、`/data-methodology/`、About、Authors 等陈述 vs 实际功能。

### 3.1 矛盾清单（6 处第一人称「本仓计算器」+ 1 处段落）

| # | 文件 | 矛盾陈述 | 修正 |
|---|---|---|---|
| 1 | `docs/faq.md:57` | 「[landed-cost calculator](/landed-cost-calculator/) lets you pick…」——内链指向已移除的本仓计算器 | 改为跨域 `https://electricvehiclehub.net/landed-cost-calculator/` + 「on our sister site」 |
| 2 | `docs/import-overview.md:58` | 内链 `/landed-cost-calculator/` | 跨域 .net |
| 3 | `docs/introduction.md:43` | 「run the numbers in the [calculator](/landed-cost-calculator/)」 | 跨域 .net + 「on electricvehiclehub.net」 |
| 4 | `blog/byd-seal-deep-review.md` | 「Use our calculator to model…」+ 内链 | 「the calculator on electricvehiclehub.net」+ 跨域 |
| 5 | `blog/chinese-ev-export-landscape-2026.md` | 「We built a calculator for exactly that…[here](/landed-cost-calculator/)」 | 「That calculation runs on our sister site」+ 跨域 .net |
| 6 | `blog/byd-seal-vs-tesla-model-3.md` / `byd-atto-3-vs-tesla-model-y.md` | 内链 `/landed-cost-calculator/` | 跨域 .net |
| 7 | `blog/import-chinese-ev-eu-guide.md` | 「we built a dedicated calculator」「our landed cost calculator」（3 处） | 跨域 .net + 「the calculator exists on electricvehiclehub.net」 |
| 8 | `pages/methodology.astro` Cost assumptions 段 | 「we publish no calculator assumptions here」与实际不符（本仓仍有参考页 + 姐妹站计算器） | 改述「本仓不运行计算器，仅保留共享公式参考页；交互式计算器在 .net」 |

### 3.2 结果

- 本仓无任何「本仓运行计算器 / we built a calculator」第一人称残留（`grep -rni "our calculator\|we built\|dedicated calculator" src/content/` = 0 命中）。
- `data-methodology.astro` 仅描述数据库结构（源/归一化/价格换算/版本匹配），无计算器声称 ✅。
- About/Authors/Contact 页已确认「landed-cost 在 .net，本仓只引用不复制」口径一致 ✅。

---

## 4. 重定向与 Canonical 复核

### 4.1 `_redirects` 全部条目复核

| 条目 | 目标 | 判定 |
|---|---|---|
| `http://chinaevmart.com/index.php` / `.htm` | `/` | ✅ |
| `/sitemap.xml` | `/sitemap-index.xml` | ✅ |
| `https://www.chinaevmart.com/*` | apex `:splat` | ✅ |
| `/index.php` / `/index.htm` | `/` | ✅ |
| `/blog/page/1/` | `/blog/` | ✅ |
| `/landed-cost-calculator/`（含无斜杠） | `https://electricvehiclehub.net/landed-cost-calculator/` | ✅ 跨域 301 合理 |
| `/docs/eu-import-guide/` 等 5 篇薄指南 | `/docs/regional-import-guides/` | ✅ 目标存在 |

### 4.2 Canonical / Sitemap

- 全站 canonical 由 `SEO.astro` 用 `siteConfig.url` 派生 → 全 `chinaevmart.com`（抽检 byd-seal 页 canonical + og:url + JSON-LD url 均正确）。
- `.md` 变体 canonical 同源 `siteConfig.url` ✅。
- sitemap 域：dist 全部 `https://chinaevmart.com` ✅。
- 幽灵/无效路径抽查：`/landed-cost-calculator/` 内链已全部转跨域外链，无残留本仓幽灵路径。

---

## 5. 遗留（需运营方）

1. **邮箱开通**：`info@/privacy@/legal@` 已统一为 `@chinaevmart.com`，但该域当前无 MX 记录（DNS 实测）。需在 chinaevmart.com 的 DNS/邮件服务开通这些邮箱，否则联系邮件无法投递。
2. **社交句柄**：`x.com/cnevhub`、`github.com/martinxionbiotech-max/CNEVhub` 待运营方提供新账号或确认沿用。
3. **线上生效**：源码已全量切 chinaevmart.com；需用 `.env.example`（SITE_URL/SITE_NAME）重新部署后线上生效。`PUBLIC_INDEXABLE` 预览 noindex 开关未改动。

---

## 6. 提交清单

| commit | 内容 |
|---|---|
| `p0-domain-unify-1-brand-emails` | 邮箱域（site.ts/contact.ts/llms.txt）+ LICENSE + THIRD-PARTY-NOTICES + package.json + content-backlog + scripts |
| `p0-domain-unify-2-calculator-contradictions` | 6 处第一人称计算器陈述 + 1 处 methodology Cost assumptions 段 → 跨域 .net |
| `p0-domain-unify-3-report` | 本报告 + style-guide 审计清单微调 |

*本批未改动任何数据值（价格/续航/税率/规格）；未改动 landed_cost 数据层；未改动 PUBLIC_INDEXABLE。*
