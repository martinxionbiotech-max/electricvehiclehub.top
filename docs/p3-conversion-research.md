# P3 · 商业转化与原创研究（收官批）报告

> 仓库：`electricvehiclehub.top`（chinaevmart.com 代码库）
> 阶段：Phase 3 · 强化商业转化与原创研究（04 P3 收官批）
> 日期：2026-10-23
> 执行角色：B2B 内容策略师 + 数据研究员

---

## 0. 诚实边界声明

本批所有结论基于**真实数据与明确计算过程**：

- 车型规格：`src/content/vehicles/*.md`（517 款，`quality_tier` A/B/C 分层）
- 关税结构：`src/data/tariffs.json`（30 市场 + `brand_cvd` 四档）
- 落地成本：各车型 `landed_cost_markets` 记录（与 `landed-cost-methodology` 公式一致）
- **无 GSC 数据**：Search Console 未接入，本批不虚构任何 impressions/clicks/CTR。GSC 评估仅产出框架（`docs/gsc-measurement-plan.md`），待接入后执行。

---

## 1. 交付项清单

| # | 交付项 | 路径 | 状态 |
|---|---|---|---|
| 1 | 选型清单（10 车型 × 5 市场） | `docs/p3-vehicle-market-selection.md` | ✅ |
| 2 | 原创分析 × 4 | `src/content/blog/`（见下） | ✅ |
| 3 | 询价入口强化 | `/quote/` + 车型页按钮 + 导航/FAQ | ✅ |
| 4 | GSC 评估框架 | `docs/gsc-measurement-plan.md` | ✅ |
| 5 | 收尾报告 | `docs/p3-conversion-research.md`（本文件） | ✅ |

---

## 2. 选型清单（10 车型 × 5 市场）

**车型（按出厂价升序）**：MG 4 ($9,690) · BYD Dolphin ($14,020) · BYD Atto 3 ($16,260) · BYD Seal ($24,690) · XPeng G6 ($24,830) · Onvo L60 ($29,140) · Xiaomi SU7 ($30,320) · Zeekr 7X ($32,370) · Xiaomi YU7 ($35,700) · Zeekr 001 ($38,000)。

**市场（一区一代表）**：Germany（欧盟）· UAE（中东）· Thailand（东南亚）· Brazil（拉美）· Australia（澳新）。

**选型依据**：全部 `quality_tier: "A"` 完整数据 + P6 §2.1 Tier 1 出口旗舰 + `brand_cvd` 四档（17/18.8/20.7/35.3）全覆盖 + 价格带 $9.7k–$38k 全覆盖。

**五市场平均落地溢价**（10 车型均值）：Thailand +28.8% < UAE +31.1% < Australia +37.5% < Brazil +88.8% ≈ Germany +88.9%。

---

## 3. 原创分析（4 篇，均有独立计算+结论+来源日期+互链）

| 篇目 | 主题 | 核心独立计算 |
|---|---|---|
| `budget-ev-landed-cost-advantage` | 低价车全成本后是否仍具优势 | MG4/Dolphin/Atto3 五市场落地成本 + 固定成本占比（MG4 27.8% vs 旗舰 10%） |
| `eu-cvd-four-tier-same-price` | 反补贴税四档隔离 | 恒定 $20k 基价下四档 CVD 落地差价（$4,889–$9,680）+ Brazil 对照 |
| `five-market-landed-cost-basket` | 五市场落地成本篮子排名 | 10 车型 × 5 市场总篮子 + 平均溢价排序 |
| `australia-suv-import-guide` | 澳洲市场选型指南 | Atto3/G6/L60/7X 规格对比 + $/kWh、$/km 衍生指标 |

每篇均含：数据表 + 计算过程 + 结论 + Sources 日期 + 与车型页/市场页/方法论页互链。

---

## 4. 询价链路改动（前 → 后）

**盘点现状（前）**：
- 唯一转化入口 = `/contact/`（通用 ContactForm，无后端 demo 模式，subject 下拉为 SaaS 模板残留：sales/support/enterprise/partnership）
- 车型页仅「Report a data issue」mailto，无询价入口
- FAQ 指向「contact us」获取报价，但无结构化车型/数量/目的地收集
- 无 `/quote/` 落地页

**改动（后）**：
1. **新增 `/quote/` 落地页**：静态表单（无后端）——Name/Email/Model/Quantity/Destination（30 市场下拉）/Notes，提交用 `mailto:` 预填车型+数量+目的地到 `info@chinaevmart.com`，无服务器收数据（诚实标注）。
2. **车型页询价按钮带参数**：每个车型页新增「Request export guidance」按钮，`/quote/?vehicle=<slug>&model=<title>&price=<price>` 预填车型。
3. **响应预期可兑现声明**：/quote/ 页「What to expect」明确「24 小时（GMT+8 工作日）响应 + 规格/落地成本指引 + 非销售/非经纪、不提供绑定报价」——与站点「信息平台非卖家」定位一致，可兑现。
4. **导航 + FAQ 接线**：footer 新增「Request Export Guidance」；contact FAQ 与 docs/faq 的报价问题改为指向 /quote/。

---

## 5. GSC 评估框架要点

见 `docs/gsc-measurement-plan.md`，核心：接入后看三类指标——①车型页曝光/点击/CTR/排名/收录；②四类处置页（/quote/、4 篇博客、/markets/、方法论页）效果；③询价转化路径（仅能近似到 /quote/ 页面级流量，mailto 发出不可被 GSC 追踪，需 GA4 补充）。**无 GSC 数据不虚构**，待接入后执行并回填 P6 优先级。

---

## 6. 验证

- `npm run build` exit 0（见收尾 commit 记录）
- sitemap 新增 `/quote/` 与 4 篇博客（blog 共 86 → 90，车辆 517 不变，品牌 72 不变）

---

*报告路径：`docs/p3-conversion-research.md`*
