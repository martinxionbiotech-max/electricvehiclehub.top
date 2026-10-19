# EVHub Top — Index Readiness Final QA

- **Site**: electricvehiclehub.top (Astro)
- **Repository**: `electricvehiclehub.top`
- **Date**: 2026-10-19
- **Scope**: 终检 + 索引就绪收尾（517 深度档案全量完成后的三查）
- **Result**: ✅ **PASS — 索引就绪**（1 个 P0 断链已修，其余全绿）

---

## 一、五段一致性抽检

### 1.1 随机 15 篇深度档案（seed=20261019）

15/15 通过：五段结构完整（Entity Snapshot / Powertrain & Architecture / Dimensions &
Logistics / Market Compliance & Export Profile / Benchmarking Matrix）· 核心字段无缺失 · HS
Code 与动力形式一致。

| Vehicle | Powertrain | HS Code | 五段 | 核心字段 |
|---|---|---|---|---|
| jetour-x90-c-dm | PHEV | 870340 | ✅ | 完整 |
| changan-nevo-e07-erev | EREV | 870340 | ✅ | 完整 |
| forthing-xinghai-s7 | BEV | 87038000 | ✅ | 完整 |
| wuling-starlight-730 | BEV | 87038000 | ✅ | 完整 |
| im-ls6 | BEV | 87038000 | ✅ | 完整 |
| hongqi-eh5 | BEV | 87038000 | ✅ | 完整 |
| aito-m9-erev | EREV | 870340 | ✅ | 完整 |
| leapmotor-t03 | BEV | 87038000 | ✅ | 完整 |
| chery-fulwin-t6 | PHEV | 870340 | ✅ | 完整 |
| aeolus-mage | HEV | 870340 | ✅ | 完整 |
| im-ls7 | BEV | 87038000 | ✅ | 完整 |
| tank-400 | PHEV | 870340 | ✅ | 完整 |
| hongqi-hq9 | PHEV | 870340 | ✅ | 完整 |
| jetour-shanhai-l7 | PHEV | 870340 | ✅ | 完整 |
| byd-qin-l | BEV | 87038000 | ✅ | 完整 |

### 1.2 HS Code × 动力形式（全量 517 交叉核验，非仅抽 20）

| Powertrain | 数量 | 期望 HS Code | 结果 |
|---|---|---|---|
| BEV | 286 | 87038000 | ✅ 0 异常 |
| PHEV | 154 | 870340 | ✅ 0 异常 |
| EREV | 58 | 870340 | ✅ 0 异常 |
| HEV | 16 | 870340 | ✅ 0 异常 |
| ICE | 3 | 87032200 | ✅ 0 异常 |

- `hs_code` 缺失：**0**；不匹配：**0**。全量 517 通过（比任务要求的抽 20 篇更强）。

### 1.3 占位残留扫描（全站）

- md 正文残留（`{…}` / `undefined` / `null` / `NaN` / `[object Object]`）：**0**
- 构建后 HTML 渲染残留：**0 页**
- N/A 标注：经 `na()` helper 统一渲染，无 `undefined`/`null`/空值泄漏。

### 1.4 N/A 标注规范（27 篇子字段 N/A，非占位残留）

27 篇深度档案有子字段渲染为 N/A（与 deep-profile-completion.md 的填充率一致，
zero-fabrication 契约：不确定值留 N/A，不虚构）。分类：

- **合法 N/A（非电气化动力）**：3 ICE（changan-nevo-lamore / changan-x5-plus /
  wuling-jiachen）缺 battery_type/motor_type/battery_thermal；1 HEV（gac-motor-gs8）
  缺 battery_type/battery_thermal；1 HEV（haval-jolion-pro）缺 charging_adapter。
- **待补数据缺口（电气化车型，P2 非阻断）**：
  - `battery_type` 缺：6 BEV（dayun-h8/h9/y6/y7、hycan-v09、maxus-eg10）+
    3 PHEV（gac-motor-e9、gac-motor-xiangwang-m8、hongqi-hs7）+ 1 EREV（im-ls9）
  - `battery_thermal` 缺：3 BEV（baojun-yep、wuling-binguo、wuling-hongguang-bev）
  - `suspension_front/rear` 缺：9 BEV（baojun-xiangjing/yep/yunhai、maxus-mifa-7/9、
    wuling-binguo/hongguang-bev/starlight/starlight-s）+ 3 PHEV（chery-fulwin-a8、
    gac-motor-e8、gac-motor-xiangwang-s7）

> 上述均为 N/A 正常渲染，非残留占位、非断链，不阻断索引就绪。建议后续批次按品牌回填。

---

## 二、索引就绪

### 2.1 Sitemap 覆盖（对账 dist 实际页 vs sitemap）

- `sitemap-0.xml` 总 URL：**701**
- 车型页：**517 / 517** ✅（0 漏页）
- 博客：**77 / 77** 已发布 ✅（blog 文件 86，其中 9 篇 `draft: true` 正确排除于构建与 sitemap）
- 索引页：首页 `/` · `/vehicles/` · `/brands/` · `/blog/` **4/4** ✅
- 品牌页 72 · docs 14 · 静态页 16 · 其余 1 各归位

> 说明：任务背景「86 博客」为源文件总数；9 篇草稿（australia-import-guide、
> byd-seagull-vs-wuling-binguo、deepal-s07-vs-byd-sealion-06、denza-d9-vs-zeekr-009、
> geely-galaxy-e5-vs-byd-atto-3、onvo-l90-vs-nio-es8、xpeng-g9-vs-nio-es8、
> xpeng-mona-m03-vs-byd-dolphin、zeekr-7x-vs-tesla-model-y）按 `draft` 语义正确排除，
> 属预期行为，非漏页。

### 2.2 Canonical / Robots

- 车型页 canonical 指向 `https://electricvehiclehub.top/vehicles/<slug>/`：**517/517 正确**
- 无 `noindex` 误设于车型页；robots.txt 允许抓取，仅 `Disallow: /api/`，并正确保留
  `/_astro/` 可抓取 + AI 爬虫（GPTBot/ClaudeBot/PerplexityBot/Google-Extended 等）Allow。

### 2.3 Vehicle Schema 抽检（全量 517，非仅抽 10）

- `Vehicle` JSON-LD：**517/517** 存在
- `offers` 完整性：**0 异常**（`price` 与 `priceCurrency` 均有值，`availability` 为 InStock，
  `itemCondition` 为 NewCondition）
- 虚构 rating：**0**（无 `aggregateRating` / `rating`）
- `fuelType` 按动力形式正确映射（BEV→Electric / PHEV→Plug-in hybrid / EREV→Extended-range
  electric / HEV→Hybrid / ICE→Gasoline）。

### 2.4 Hreflang

- 全站 `hreflang` 链接：**0** —— 无多语种变体，单语（en）站点，无需 hreflang。✅

---

## 三、站点级收尾

### 3.1 深度档案链接入口（孤立页检测）

- `/vehicles/` 索引页链接：**517/517** 车型 slug ✅
- 孤立页（未从 home/vehicles-index/brands-index/blog-index 任何入口链接）：**0**
- 品牌页自身车型链接缺失：**0**（72 品牌页均链接其全部车型）
- 首页精选入口：11 个车型卡片（正常，首页为精选非全量）。

### 3.2 OG 图与 Meta 抽检（全量 517）

- `og:image` / `og:title` / `og:description` / `meta description` 缺失：**0 页**
- 引用图片文件存在于 `public/`：**0 缺失**（517 篇 image 路径全部可解析）。

---

## 四、异常清单与修复

| # | 级别 | 异常 | 处置 |
|---|---|---|---|
| 1 | **P0** | `/data/source-master.json` 断链（`docs/data-provenance` 链接到未发布的数据文件） | **已修**：新增 `src/pages/data/source-master.json.ts` 数据路由，发布该文件（与 brands/vehicles/tariffs 一致） |
| 2 | P2 | 27 篇深度档案子字段 N/A（见 §1.4） | 记录，非阻断（合法 N/A + 待回填） |

- P0 修复后全站内部断链（剥离 `<script>` 避免 JS 模板字面量误报）：**0**。

---

## 五、Build / 提交

- `npm run build`：**900 pages**（898 内容页 + 404/500），exit **0**，164.76s
- 数据端点：`dist/data/` 现有 4 个（brands.json / source-master.json / tariffs.json / vehicles.json）
- Commit 标记：`final-qa`
- Push + 同步：`0 0`（见收尾命令输出）
