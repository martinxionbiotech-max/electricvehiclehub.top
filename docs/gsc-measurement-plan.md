# GSC 评估框架（接入后执行）

> 仓库：`electricvehiclehub.top`（chinaevmart.com 代码库）
> 阶段：Phase 3 · 商业转化与原创研究（收官批）
> 日期：2026-10-23
> 状态：**框架就绪，待 GSC 接入后执行**。本文件只定义「接入后要看什么、怎么算」，**不包含任何 GSC 数据**——当前 Search Console 未接入，任何 impressions/clicks/CTR 数值都会是虚构，故一律不写。

---

## 0. 诚实边界

- **无 GSC 数据**：本批未接入 Search Console。本计划不含任何数值，只定义指标与口径。
- **不预判结论**：哪类页获流、哪类页零曝光，一律待真实数据校准后再判断，不预先断言。
- **执行前提**：用户在 GSC 中完成域名/URL-prefix 资源验证（推荐 URL-prefix，匹配 `https://chinaevmart.com/` 与 www 版本）。

---

## 1. 三类核心指标组

### 1.1 车型页（P1 主攻对象）

| 指标 | 口径 | 用途 |
|---|---|---|
| 曝光量 (Impressions) | 按车型页 URL 聚合，4 周窗口 | 发现层覆盖：哪些 Tier 1 车型被搜索看见 |
| 点击量 (Clicks) | 同上 | 实际进入量 |
| CTR | Clicks / Impressions | 标题/描述吸引力 |
| 平均排名 (Position) | 按页聚合均值 | 排序健康度，识别 8–20 位可提升页 |
| 收录状态 | Coverage 报告「已收录/已发现未收录/被排除」 | 识别未被索引的车型页 |

**优先下钻**：`quality_tier = "A"` 的 Tier 1 旗舰（见 `docs/p3-vehicle-market-selection.md` 十款），按品牌 + 车身 + 动力切分。

### 1.2 四类处置页（本批 P3 产出）效果跟踪

四类页面族的曝光/点击/CTR 单独统计，用于验证「强化商业转化」是否生效：

| 页面族 | URL 模式 | 跟踪目标 |
|---|---|---|
| 询价落地页 | `/quote/` | 商业转化入口曝光/点击 |
| 原创分析博客 | `/blog/budget-ev-landed-cost-advantage/`、`/blog/eu-cvd-four-tier-same-price/`、`/blog/five-market-landed-cost-basket/`、`/blog/australia-suv-import-guide/` | 原创研究是否获流 |
| 市场对比页 | `/markets/` | 关税结构页是否承接选型意图 |
| 方法论页 | `/landed-cost-methodology/`、`/data-methodology/` | 信任层是否被查询 |

### 1.3 询价转化路径（无后端，mailto 链路）

> 注意：mailto 方案下，「邮件实际发出」无法被 GSC 追踪——GSC 只有「页面级」的曝光/点击/查询。转化路径**只能近似**到「询价落地页的流量与来源查询」，不能声称「询价量」。

| 近似指标 | 口径 | 说明 |
|---|---|---|
| `/quote/` 曝光/点击 | 页面级 | 入口被看到/点进 |
| 带来 `/quote/` 点击的查询词 | Search Performance 按查询过滤 URL=/quote/ | 识别高意图询价词 |
| 车型页 → /quote/ 内链来源 | 无法在 GSC 直接追踪（需 GA4 事件，若有） | 标注为「需 GA4 补充，GSC 不覆盖」 |

---

## 2. 待接入后的执行清单（顺序）

1. 验证资源 → 等 3–7 天数据积累。
2. 导出 Search Performance（4 周，按页聚合），另存为 CSV 归档到 `docs/`（文件名带日期）。
3. 跑 §1.1 车型页指标，识别「有曝光无点击」（CTR 低）与「无曝光」（未被发现）两类，各列 Top 20。
4. 跑 §1.2 四类处置页指标，判断 P3 新页面是否被索引、是否获流。
5. 跑 §1.3 询价词下钻，汇总带来 /quote/ 点击的真实查询词。
6. 用真实数据回填 P6 优先级（`docs/chinaevmart-p6-priorities.md` 的 P6 层「待 GSC 接入后校准」）。
7. 产出 `docs/gsc-measurement-report-<date>.md`（真实数据，标注数据窗口）。

---

## 3. 不做什么

- **不虚构**任何 impressions/clicks/CTR/position 数值。
- **不把 mailto 点击当成可追踪转化**——除非后续接入 GA4 事件，否则只报告「/quote/ 页面级流量」。
- **不基于直觉预排优先级**——GSC 数据出来前，P6 层保持「待校准」状态。

*报告路径：`docs/gsc-measurement-plan.md`*
