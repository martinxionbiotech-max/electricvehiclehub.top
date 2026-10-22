# China EV Mart — Editorial & Terminology Style Guide

> 定位声明、术语统一表、数据口径约定。本文档是全站文案与数据的单一术语来源（Single Source of Truth for terminology）。
> 站点：China EV Mart · 域名：chinaevmart.com（品牌显示名 **China EV Mart**，机器标识/域名 **ChinaEVMart** / **chinaevmart.com**）

---

## 1. 定位声明（Positioning）

> “An independent information platform for discovering Chinese new-energy vehicles, comparing vehicle specifications, researching automotive technology, and evaluating export-market requirements.”

**我们是信息平台，不是卖家。** 以下定位必须如实表述，不夸大服务能力：

- ✅ **如实表述**：China EV Mart 是独立的中国新能源车信息平台——提供车型发现、规格对比、技术研究与出口市场评估。
- ✅ 平台由 Chengguang Energy（Jinzhou Chengguang Power Source Co., Ltd.）运营，作者 Wei Wang（EV & Battery Industry Analyst）。这些是真实可审计的主体，全站统一引用。
- ❌ **禁止声称**：不称自己是经销商/进口商/报关行/法律顾问；不称提供“代购”“代办清关”“成交价”“实时库存”。
- ⚠️ **谨慎表述**：仅在服务真实可提供时才提及 sourcing/quotation/supplier matching/export coordination。当前定位下，凡涉及“代找车源”“提供报价”等表述应降级为“规格指导 / 信息澄清”，并明确“我们不作为采购代理或经纪人”。

### 1.1 平台 vs 卖家边界（FAQ 已对齐）

| 问题 | 正确回答口径 |
|---|---|
| 你们卖车吗？ | 不卖。我们是独立信息平台，不代卖、不代理任何厂商。 |
| 能帮我找某款车吗？ | 可提供规格指导；不充当采购代理或经纪人。 |
| 价格是成交价吗？ | 不是。价格是 ex-factory（中国出厂参考价），需向供应商确认实际报价。 |

---

## 2. 品牌名写法规范

| 场景 | 写法 | 反例 |
|---|---|---|
| 正文/标题/OG/描述中的站点名 | **China EV Mart** | EVHub Top、EV Hub、CNEVhub |
| 域名 / URL / canonical | **chinaevmart.com** | electricvehiclehub.top |
| 机器标识（JSON-LD @id、实体 id） | `china-ev-mart` | `ev-hub` |
| 代码注释中的简称（可接受） | China EV Mart / CEM | EVHub Top |
| Logo SVG 文字 | China EV Mart | EV Hub |

**历史引用规则**：旧品牌（EVHub Top / EV Hub / CNEVhub / electricvehiclehub.top）仅允许出现在**历史准确语境**中——例如描述旧域迁移、旧数据批次来源说明等；不得作为当前站点名出现。线上 electricvehiclehub.net 是**独立的姐妹站**（landed-cost 计算器），跨域链接保留 `.net`，不改写。

---

## 3. 车型与动力形式术语表

| 术语 | 标准写法 | 说明 |
|---|---|---|
| 纯电动 | **BEV** | Battery Electric Vehicle |
| 插电混动 | **PHEV** | Plug-in Hybrid Electric Vehicle |
| 增程式 | **EREV**（别名 REEV） | Extended-Range Electric Vehicle |
| 油电混动（非插电） | **HEV** | Hybrid Electric Vehicle |
| 燃油 | **ICE** | Internal Combustion Engine（数据库边界：仅 3 台，需显式标注“燃油对照”） |

**规范**：
- frontmatter `powertrain` 枚举严格使用 `BEV / PHEV / EREV / HEV / ICE`（schema 已限定）。
- 正文提及动力形式时用全称 + 缩写（首次出现），后续可只用缩写。
- 不混淆 EREV 与 PHEV：增程是“电驱为主、发动机仅发电”；插混是“发动机可直驱”。写文案时不得混用。

---

## 4. 价格口径表（禁止静默替换）

| 口径 | 定义 | 使用场景 |
|---|---|---|
| **China ex-factory price (MSRP)** | 中国出厂参考价（含税出厂） | 站点当前默认口径（frontmatter `price_type` 默认值，517 条全走此默认） |
| Chinese market transaction price | 中国市场成交参考价 | 仅在来源明确标注时使用 |
| FOB price | 离岸价（含国内运费+港口费） | 仅在 `fob_price_usd_min/max` 有值时显示；**当前 0/517 有值，禁止凭空生成** |
| Landed cost | 到岸落地价（含关税/VAT/运费/认证） | 仅存在于 `.net` 姐妹站；本平台不渲染，只外链 |

**红线**：
- ❌ 禁止把 ex-factory 伪装成 FOB 或成交价。
- ❌ 禁止把出厂价冒充“落地价”。
- ⚠️ `price_type` 若未显式声明，一律回退 `China ex-factory price (MSRP)` 并如实标注，不得改写为其他口径。

---

## 5. 续航与测试标准术语

| 标准 | 写法 | 说明 |
|---|---|---|
| 中国工况 | **CLTC** | 中国轻型车测试工况；数据字段 `range_cltc_km` |
| 欧洲工况 | **WLTP** | 数据字段 `range_wltp_km` |
| 美国工况 | **EPA** | 本站几乎不采用，引用时标注来源 |
| 旧欧洲工况 | **NEDC** | 引用历史数据时标注，不默认 |

**规范**：
- 所有续航数字必须携带测试标准标签（`range_cltc_km` / `range_wltp_km`），不写无标准的裸续航值。
- CLTC 数值普遍高于 WLTP，比较车型时必须同标准，禁止 CLTC 对 WLTP 直接比。
- 无法确认标准时如实标 N/A，不得补写猜测值。

---

## 6. 数据溯源与可信度口径

| 字段 | 规范 |
|---|---|
| `data_source` | 车辆级来源描述；当前统一为 `China EV Mart catalog + manufacturer specs (…)`，标注核验日期 |
| `data_updated` | 最后更新/核验日期（YYYY-MM-DD） |
| `data_reviewed` | 是否人工复核（当前 517/517 = false，如实呈现） |
| `verification_status` | `verified / partial / unverifiable / None`，不得把未核验标为已核验 |
| `confidence` | `high / medium / low`，缺失时渲染层默认 medium |

**红线**：禁止把未复核数据标为已核验；禁止把二手来源标为一手来源。

---

## 7. 事实与作者诚信（Discipline）

- ❌ 不虚构员工、资质、认证、测试设施、客户关系、合作关系、销量、海外布局。
- ✅ 作者仅 Wei Wang（真实）；无虚构编辑/审稿人（authors.astro 已明确“written & reviewed by same person 时会说明，而非发明第二个名字”）。
- ✅ 来源分级（Tier 1–4）已在 methodology 页公开，写引用时遵守对应层级。
- ✅ 历史准确引用保留；当前品牌统一为 China EV Mart。

---

## 8. 一致性审计清单（每次发布前）

1. `grep -rn "EVHub Top\|EV Hub\|CNEVhub\|electricvehiclehub.top" src/ public/` → 应为 0（或仅历史语境 + 邮箱域名待运营确认）。
2. 首页 / 车型 / 品牌 / About 的 `<title>` 与 `og:site_name` → 全部 `China EV Mart`。
3. `siteConfig.name === 'China EV Mart'` · `siteConfig.url === 'https://chinaevmart.com'`。
4. 价格/续航数字均带口径标签（ex-factory / CLTC / WLTP）。
5. `PUBLIC_INDEXABLE` 开关未被误改（预览 noindex 策略保留）。

---

*本文档随品牌迁移批生成（Phase 2），后续 Phase 3–5 数据/内容批沿用本术语表。*
