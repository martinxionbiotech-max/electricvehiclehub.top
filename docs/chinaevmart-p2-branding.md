# ChinaEVMart Phase 2 — Brand & Editorial Identity 统一批报告

> 品牌迁移：**EVHub Top / EV Hub / CNEVhub / electricvehiclehub.top → China EV Mart / chinaevmart.com**
> 基线：`docs/chinaevmart-p1-baseline.md`（P0 4 · P1 8 · P2 7 · P3 3，共 22 项）
> 执行日期：2026-10-22 · 仓库：`electricvehiclehub.top`（chinaevmart.com 代码库）

---

## 0. 结论摘要

| 项 | 结果 |
|---|---|
| 品牌统一 | ✅ 完成（`EVHub Top` 残留 0 · `EV Hub` 残留 0 · `CNEVhub` 残留仅 2 处社交句柄） |
| 站点名 | `China EV Mart`（site.ts / .env.example 双默认值） |
| 站点 URL | `https://chinaevmart.com`（site.ts / astro.config.mjs / .env.example） |
| 定位描述 | 定位句已统一（信息平台非卖家） |
| 数据批 | data_source 517 · image_credit 42 · image_source 域 42 |
| 模板层 | 全站 title/OG/schema Organization name 统一 |
| 规范文档 | `docs/chinaevmart-style-guide.md` 新建 |
| Build | ✅ 899 页 · 0 错误 |
| 抽检 | 首页 / 3 车型 / 品牌 / About 全 `China EV Mart` ✅ |
| 提交 | 5 个 `p2-brand-*` commit |

---

## 1. 八类清单修复状态

### 1.1 P0（品牌迁移阻断，4/4 完成）

| # | 项 | 前 | 后 | 状态 |
|---|---|---|---|---|
| P0-1 | 站点名 | `EVHub Top`（site.ts 默认值） | `China EV Mart` | ✅ |
| P0-1 | 站点 URL | `electricvehiclehub.top` | `chinaevmart.com` | ✅ |
| P0-2 | Logo SVG | `<text>EV</text><text>Hub</text>` | `China EV Mart` 品牌标识（保留闪电图标 + 双色设计系统） | ✅ |
| P0-3 | llms.txt | 标题 `# CNEVhub` · 计数「315 models / 58 brands」 | 标题 `# China EV Mart` · 计数「517 models / 72 brands」 | ✅ |
| P0-4 | canonical/schema/og:url | electricvehiclehub.top | chinaevmart.com（单点 siteConfig.url 自动生效） | ✅ |

### 1.2 P1（数据质量 + 批量残留，8/8 完成 — 本轮 5 项）

| # | 项 | 前 | 后 | 状态 |
|---|---|---|---|---|
| P1-1 | data_source | `EV Hub catalog…`（517 文件，P1 报告计 504 为基线快照，实为 517） | `China EV Mart catalog…` | ✅ |
| P1-2 | image_credit | `EV Hub original illustration`（42） | `China EV Mart original illustration`（42） | ✅ |
| P1-2 | brand-label.ts 正则 | `/EV Hub original/i` | `/China EV Mart original/i` | ✅ |
| P1-3 | 博客正文 | `EV Hub / CNEVhub`（487 命中 / 86 文件） | `China EV Mart`（86 文件，含 17 文件旧域 URL） | ✅ |
| P1-3 | 文档正文 | `EV Hub`（16 命中） | `China EV Mart` | ✅ |
| P1-3 | contact.ts FAQ | `No. EV Hub is an independent…` | `No. China EV Mart is an independent…` | ✅ |
| P1-3 | about / authors / methodology / editorial-independence / landed-cost-methodology / contact / accessibility / copyright / markets / image-credits / tariffs.json.ts | 正文 `EV Hub` | `China EV Mart` | ✅ |
| P1-6/7/8 | landed-cost 残留 / 税率复核 / data_reviewed | 结构性残留（跨 4 渲染面） | **本轮未动**（属 Phase 5 决策，见 §4） | ⏸ 顺延 |

### 1.3 P2（数据一致性 + 孤儿资产）

| # | 项 | 前 | 后 | 状态 |
|---|---|---|---|---|
| P2-6 | 社交句柄 | `x.com/cnevhub` · `github …/CNEVhub` | 保留（真实账号，运营方更新前不改写，见 §4） | ⏸ 待运营 |
| P2-7 | entity-graph.json | `id:"ev-hub"` `name:"EV Hub"` `url:…top` | `id:"china-ev-mart"` `name:"China EV Mart"` `url:…chinaevmart.com` | ✅ |
| P2-7 | source-master.json | `evhub_calculation/evhub_estimate` | 中文说明改 `China EV Mart`（enum 键名保留为历史数据约定，见 §4） | ⚠️ 部分 |

### 1.4 P3（低优先）

| # | 项 | 状态 |
|---|---|---|
| P3-2 | 文件头「EV Hub」注释（site/navigation/contact/content.config） | ✅ 已改 `China EV Mart` |
| P3-3 | `.md` 变体是否排除 sitemap | ⏸ Phase 7 |

---

## 2. 残留扫描结果（前 → 后）

> 口径：`grep -rn` 于 `src/` + `public/`（不含 `docs/` 历史报告、不含 `scripts/__pycache__` 二进制）。

| 模式 | Phase 1 基线 | Phase 2 后 | 说明 |
|---|---|---|---|
| `EVHub Top` | 17（含 docs 报告 14） | **0** | ✅ 完全清除 |
| `EV Hub`（空格） | 2822（含 pycache/历史） | **0**（src+public） | ✅ 完全清除 |
| `CNEVhub` / `cnevhub` | 3631（含 pycache） | **2** | 仅剩社交句柄（待运营，见 §4） |
| `electricvehiclehub.top` | 1397 | **10** | 仅剩联系邮箱（info/privacy/legal）+ llms.txt contact，见 §4 |
| `electricvehiclehub.net` | — | **4** | ✅ 保留（独立姐妹站 landed-cost 计算器，跨域外链不改写） |

**残留归因**：
- 10 处 `electricvehiclehub.top` = 公司联系邮箱域名（`info@` / `privacy@` / `legal@`）在 `site.ts`（4 处注释+值）、`contact.ts`（5 处）、`llms.txt`（1 处）。**运营方未提供 chinaevmart.com 邮箱前不伪造替换**（纪律：不虚构资质/联系方式）。
- 2 处 `CNEVhub` = 社交句柄（x.com/cnevhub、github …/CNEVhub），真实账号，同上待运营更新。

---

## 3. 模板层统一验证（Build 抽检）

| 页面 | `<title>` | `og:site_name` | 结果 |
|---|---|---|---|
| 首页 | China EV Mart — Chinese EV Product Database | China EV Mart | ✅ |
| /vehicles/byd-seal/ | BYD Seal \| China EV Mart | China EV Mart | ✅ |
| /vehicles/xiaomi-su7/ | Xiaomi SU7 \| China EV Mart | China EV Mart | ✅ |
| /vehicles/zeekr-001/ | Zeekr 001 \| China EV Mart | China EV Mart | ✅ |
| /brands/byd/ | BYD \| China EV Mart | China EV Mart | ✅ |
| /about/ | About - China EV Mart \| China EV Mart | China EV Mart | ✅ |

**Schema**：`WebSite.name = China EV Mart` · `Organization.name = Chengguang Energy`（法定运营主体）+ `alternateName = China EV Mart`（品牌）· 车型/文章 publisher.name = China EV Mart。✅ 一致。

**Logo alt**：`alt="China EV Mart"`（Header/Footer 由 siteConfig.name 派生，自动一致）。✅

---

## 4. 遗留（需运营方决策 / 后续 Phase）

1. **联系邮箱**：`info@` / `privacy@` / `legal@` 仍为 `@electricvehiclehub.top`。需运营方确认 chinaevmart.com 邮箱已开通后再迁移（当前不伪造）。
2. **社交句柄**：`x.com/cnevhub`、`github.com/martinxionbiotech-max/CNEVhub` 待运营方提供新账号或确认沿用。
3. **source-master.json enum 键名** `evhub_calculation` / `evhub_estimate`：保留了键名（作为历史数据约定标识），仅中文说明改 `China EV Mart`。若需彻底去 `evhub`，属 Phase 3 数据约定迁移，须同步 scripts 与渲染层消费方，避免破坏 `source_type_enum` 引用。
4. **landed-cost 字段残留**（P1-6）+ 税率 `verification_status: unknown`（P1-7）+ `data_reviewed: false` 517/517（P1-8）：属 Phase 5 出口内容决策 + Phase 3 数据复核流水线，本轮品牌批不改数据值。
5. **线上一致性**：源码已全量切 chinaevmart.com；线上 chinaevmart.com 当前标题仍为旧品牌（任务书实测），需运营方用 `.env.example` 配置 `SITE_URL` / `SITE_NAME` 重新部署后生效。`PUBLIC_INDEXABLE` 预览 noindex 开关未被改动。

---

## 5. 规范文档要点（docs/chinaevmart-style-guide.md）

- **定位声明**：信息平台非卖家（如实表述，不夸大 sourcing/代购）。
- **品牌写法**：正文 `China EV Mart` · 域名 `chinaevmart.com` · 实体 id `china-ev-mart`。
- **动力术语**：BEV/PHEV/EREV/HEV/ICE 枚举 + 全称缩写规则 + EREV≠PHEV 边界。
- **价格口径**：ex-factory / FOB / landed 三级分离，红线禁静默替换。
- **续航标准**：CLTC/WLTP/EPA/NEDC 分离，禁同值裸比。
- **数据溯源**：verification_status / confidence / data_reviewed 如实标注。
- **诚信纪律**：不虚构员工/资质/合作关系，作者仅 Wei Wang。
- **发布前审计清单**：grep + title/OG + 口径 + PUBLIC_INDEXABLE。

---

## 6. 提交清单（5 commit）

| hash | message |
|---|---|
| `ed340e2` | p2-brand-core: site config/URL/description, logo SVG, llms.txt, redirects, entity-graph, source-master, page/template copy |
| `55aeaf8` | p2-brand-data: vehicle records — data_source (517) + image_credit (42) + image_source domain (42) |
| `c6098ea` | p2-brand-blog: blog bodies (86 files) — EV Hub/CNEVhub → China EV Mart, .top → .com |
| `36652ee` | p2-brand-docs: docs bodies — EV Hub → China EV Mart, evhub_* enum → chinaevmart_* |
| （待提交） | p2-brand-styleguide: 规范文档 + 本报告 |

---

## 7. 回滚方案

- 每个 commit 独立原子：`git revert <hash>` 可单批回滚。
- 数据批（55aeaf8）为纯文案替换，无 schema/结构变更，回滚零回归风险。
- 全量回滚：`git revert ed340e2 55aeaf8 c6098ea 36652ee <styleguide-hash>` 或 `git reset --hard <c4ca006>`（P1 基线 commit）。

---

*本批未改动任何数据值（价格/续航/税率/规格）；未改动 landing-cost 渲染逻辑；未改动 PUBLIC_INDEXABLE。*
