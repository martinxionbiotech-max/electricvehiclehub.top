# China EV Mart — 国家指南去重与价值审查（Guides Dedup Review）

> 仓库：`electricvehiclehub.top`（chinaevmart.com 代码库）
> 批次：five-02 · 日期：2026-10-23
> 纪律：零编造 · 低价值页合并而非换名保留 · 每项可回滚

---

## 0. 结论摘要

| 维度 | 结果 |
|---|---|
| Inventory | 30 市场（`tariffs.json`）+ 30 篇国家 import-guide 博客 + 6 篇区域对比 + 6 篇 docs 薄指南 |
| 五维对比 | n-gram 相似度 / 法规引用 / 费用计算 / 认证信息 / 当地独有内容（见 §2） |
| 合并执行 | **5 篇 docs 薄指南 → 1 篇 `regional-import-guides`**（区域指南 + 国家差异表），原 URL 301 |
| 博客 30 篇国家指南 | **保留**（同区对相似度仅 1.6%–16%，各有当地独有内容，非低价值重复） |

---

## 1. Inventory

### 1.1 市场/国家指南页面族

| 族 | 数量 | 载体 |
|---|---|---|
| 市场关税数据 | 30 | `src/data/tariffs.json`（`/markets/` 单页渲染 + `/data/tariffs.json` 端点） |
| 国家 import-guide 博客 | 30 | `src/content/blog/*-import-guide.md`（1,395–4,158 词，含当地独有内容） |
| 区域对比博客 | 6 | `*-import-comparison.md`（germany-nl-fr / uae-saudi / nordics / asean / latam / turkey-indonesia） |
| docs 薄指南 | 6 | `src/content/docs/*-import*.md`（408–572 词，与博客重复） |

### 1.2 docs 薄指南清单（合并对象）

| 文件 | 词数 | 内容 | 与博客重复对象 |
|---|---|---|---|
| `eu-import-guide.md` | 571 | EU 关税栈总览 | `import-chinese-ev-eu-guide.md`（4,778 词） |
| `germany-import.md` | 470 | 德国 | `germany-import-guide.md`（2,850 词） |
| `uk-import.md` | 426 | 英国 | `uk-import-guide.md`（3,268 词） |
| `australia-import.md` | 411 | 澳洲 | `australia-import-guide.md`（3,435 词） |
| `uae-saudi-import.md` | 408 | 海湾 | `uae-import-guide.md` + `saudi-arabia-import-guide.md`（各 ~2,300 词） |
| `import-overview.md` | 572 | 十步流程总览 | `import-chinese-ev-eu-guide.md`（十步流程章节） |

---

## 2. 五维对比

### 2.1 正文相似度（n-gram，4-gram Jaccard）

| 对比对 | 相似度 | 判定 |
|---|---|---|
| docs/`germany-import` vs blog/`germany-import-guide` | 1.4% | docs 为薄摘要（非逐字重复，但同主题无增量） |
| docs/`eu-import-guide` vs blog/`import-chinese-ev-eu-guide` | 1.1% | 同上 |
| docs/`import-overview` vs blog/`import-chinese-ev-eu-guide` | 2.5% | 十步流程重复 |
| docs/`uk-import` vs blog/`uk-import-guide` | 0.7% | 同上 |
| docs/`australia-import` vs blog/`australia-import-guide` | 0.4% | 同上 |
| docs/`uae-saudi-import` vs blog/`uae-import-guide` | 0.3% | 同上 |
| **blog 同区对照** germany vs france | 3.1% | 各有独有内容，保留 |
| **blog 同区对照** austria vs belgium | 16.0% | 结构同构但当地内容（NoVA/安特卫普港）不同，保留 |
| **blog 同区对照** uae vs saudi | 10.0% | 税率/认证不同，保留 |
| **blog 同区对照** sweden vs norway | 1.6% | 保留 |

> 结论：docs 薄指南与博客**主题重复但无增量价值**（薄摘要 vs 深度指南）；博客 30 篇同区对相似度普遍 <16%，各自有当地独有内容（NoVA、registreringsafgift、安特卫普港、RAV/ADR 等），**不是低价值重复**，不合并。

### 2.2 法规引用 / 费用计算 / 认证信息 / 当地独有内容

| 对象 | 法规引用 | 费用计算 | 认证信息 | 当地独有内容 |
|---|---|---|---|---|
| docs 薄指南 | 无 source 段、无日期 | 有（BYD Seal 示例）但无来源日期 | 概述级 | 无（全为通用） |
| blog 国家指南 | 逐条带 source + accessed 日期（EUR-Lex、EAFO、当地统计） | 完整 worked example + 来源 | WVTA/IVA/RAV/GSO 细分 | 强（NoVA、BIV、registreringsafgift、港口吞吐、补贴政策） |

---

## 3. 合并执行（低价值页合并，非换名保留）

### 3.1 动作

| 步骤 | 内容 |
|---|---|
| 新建 | `src/content/docs/regional-import-guides.md`：区域指南 + 8 区域国家差异表（30 市场 duty/VAT/CVD/注册费，数据来自 `tariffs.json`） |
| 降级 | 5 篇 docs 薄指南 `draft: true`（eu-import-guide / germany-import / uk-import / australia-import / uae-saudi-import） |
| 保留 | `import-overview.md` 保留（十步流程，属 Getting Started 区，非国家指南，仍有独立入口价值） |
| 301 | 5 篇旧 URL → `/docs/regional-import-guides/` |
| 修引用 | 博客 7 处 + docs 4 处（faq/compliance/eu-homologation/landed-cost-methodology/cost-breakdown-example）+ docs/index 快速链接 |

### 3.2 为什么「合并」而非「换名保留」

- 5 篇 docs 薄指南是**低价值重复**：无来源日期、无当地独有内容、主题被博客深度指南完全覆盖。
- 合并为**一篇区域指南 + 国家差异表**：消除 5 个薄页面，保留全部 30 市场数字（以差异表形式），价值不降反升。
- 博客 30 篇国家指南**不合并**：各自有不可替代的当地独有内容与来源，合并会损失价值。

---

## 4. 变更清单（commit `five-02-*`）

| 文件 | 变更 |
|---|---|
| `src/content/docs/regional-import-guides.md` | **新增**：区域指南 + 国家差异表 |
| `src/content/docs/{eu-import-guide,germany-import,uk-import,australia-import,uae-saudi-import}.md` | `draft: true`（5 篇） |
| `public/_redirects` | 5 条旧 URL → 区域指南 301 |
| `src/pages/docs/index.astro` | 快速链接 EU Import Guide → regional-import-guides |
| `src/content/blog/*`（7 处） | 内链指向 regional-import-guides |
| `src/content/docs/*`（5 处） | 内链指向 regional-import-guides |
| `docs/guides-dedup-review.md` | **新增**：本文档 |

---

## 5. 分离声明

- **已完成（已验证）**：inventory 计数、n-gram 相似度实测（§2.1 数据为脚本实测）、5 篇合并 + 301 + 引用修复。
- **保留（有意不合并）**：博客 30 篇国家指南（各有当地独有内容）、`import-overview.md`（流程类非国家类）。
- **未覆盖**：`/markets/` 单页与博客国家指南之间的进一步去重（当前 `/markets/` 是关税对比表、博客是深度指南，定位不同，本批未动）。

---

*报告路径：`docs/guides-dedup-review.md` · five-02*
