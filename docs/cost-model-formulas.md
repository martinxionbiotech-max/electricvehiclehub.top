# Cost-Model Formulas（成本模型公式留存）

> 用途：单一真源记录本仓（chinaevmart.com · `electricvehiclehub.top`）与姊妹站
> （electricvehiclehub.net）共享的落地成本公式、输入参数、日期与来源，保证任何数字可复算。
> 本仓不运行计算器（301 → .net），此文档记录公式本身，与 `.net` 方法论文档保持一致。

- 数据日期：2026-09-15（`src/data/tariffs.json` `updated`）
- CVD 复核日期：2026-10-23（`cvd_meta.last_verified`，`consistent_with_definitive_rates`）
- 权威依据：Commission Implementing Regulation (EU) 2024/2754（六档 CVD）· EU TARIC（10% MFN）· 各国 VAT/GST 税法

---

## 1. 核心公式（三处实现一致）

```
duty  = standard_duty_rate × base
cvd   = cvd_rate × (base + duty)        # 仅 EU 且 BEV；PHEV/EREV/HEV/非EU 市场 = 0
vat   = vat_rate × (base + duty + cvd)
fixed = REGION_BASE_FIXED[region] + registration_fee_usd
total = base + duty + cvd + vat + fixed
```

与公开方法页 `base × (1+std_duty) × (1+cvd) × (1+VAT) + 固定项` **代数恒等**。
复合顺序：标准关税 → 反补贴税（duty-inclusive）→ VAT（全栈 duty-inclusive）。
成本构成 = base + 8 项（标准关税 / CVD / VAT / RoRo 海运 / 报关 / 认证 / 内陆运输 / 注册费），各计一次，无遗漏无重复。

## 2. 输入参数

### 2.1 税率

| 参数 | 值 | 来源 | 日期 |
|---|---|---|---|
| EU 标准关税（MFN，BEV） | 10% | EU TARIC / WTO | 2026-09-15 |
| 反补贴税（CVD，六档） | BYD 17.0 · Geely 18.8 · SAIC 35.3 · Tesla 7.8 · other-cooperating 20.7 · non-cooperating 35.3 | Reg (EU) 2024/2754 | 复核 2026-10-23 |
| 品牌映射（`brand_cvd`） | denza/yangwang/fangchengbao→17.0；geely/zeekr/lynk-co/geometry/livan/galaxy→18.8；mg/maxus/roewe/saic/wuling/baojun/im→35.3；tesla→7.8；`_default`→20.7 | Reg (EU) 2024/2754 | 2026-09-15 |
| VAT/GST（分国） | 见 `tariffs.json` markets（DE 19 / FR 20 / NL 21 / SE·DK 25 / UK 20 / AU 10 / …） | 各国税法 | 2026-09-15 |

**范围约束**：CVD 仅 EU 市场 + BEV。PHEV/EREV/HEV 及非 EU 市场（UK/Gulf/Australia 等）`cvd=0`。

### 2.2 固定成本（`fixed_costs`，中心值 · industry benchmark = estimate）

| 参数 | 值（USD） | 口径 |
|---|---|---|
| RoRo 海运 | 2,000 | estimate（China → 北欧主港） |
| 报关费 | 350 | estimate |
| 认证/同质化 | 3,250 | estimate（WVTA 或单车认证，文档区间 1,500–5,000） |
| 内陆运输 | 500 | estimate |

### 2.3 区域固定成本（`REGION_BASE_FIXED`，运费+报关+认证+内陆之和，不含注册费）

| 区域 | 固定成本（USD） |
|---|---|
| EU | 6,100 |
| Non-EU Europe | 5,850 |
| Middle East | 4,150 |
| Oceania | 5,350 |
| Southeast Asia | 4,600 |
| North America | 7,000 |
| Latin America | 6,500 |
| Africa | 6,200 |

注册费逐市场见 `tariffs.json` `registration_fee_usd`（30–3,500，跨度大，未逐市场标注出处 → 待人工复核）。

## 3. 抽核市场（EU + 非欧）

| 市场 | region | 标准关税 | VAT | 注册费 | CVD |
|---|---|---|---|---|---|
| Germany | EU | 10% | 19% | 500 | 品牌六档 |
| France | EU | 10% | 20% | 400 | 品牌六档 |
| United Kingdom | Non-EU Europe | 10% | 20% | 400 | 0 |
| UAE | Middle East | 5% | 5% | 300 | 0 |
| Australia | Oceania | 0% | 10% | 500 | 0 |
| Thailand | Southeast Asia | 0%（ACFTA） | 7% | 50 | 0 |
| Brazil | Latin America | 35% | 17% | 70 | 0 |
| Turkey | Middle East | 40% | 20% | 100 | 0 |

## 4. 复算示例（BYD Seal · base $24,690 · Germany · BYD 17%）

```
duty  = 0.10 × 24690          = 2,469.00
cvd   = 0.17 × (24690+2469)   = 4,617.03
vat   = 0.19 × (24690+2469+4617.03) = 6,037.45
fixed = 6100 + 500            = 6,600.00
total = 24690 + 2469 + 4617.03 + 6037.45 + 6600 = 44,413.48  (→ 显示 $44,413)
```

与 `src/content/vehicles/byd-seal.md` frontmatter `landed_cost.total_landed_usd = 44413.48` 一致；与 `.net` 仓同名车型完全一致（10 款抽核 = 0 差异）。

## 5. 口径披露（诚实声明）

- **应税基数 = 出厂基价（base），非严格 CIF**。严格欧盟海关以 CIF（车价+保险+运费）为应税基数；本模型用 base 是保守简化（文档已披露）。
- **排除项**：保险（CIF 的 "I"）、汇率波动、融资/经销商毛利、滞港/堆存、本地特有税（Turkey SCT / Singapore ARF+COE / Indonesia PPnBM / Brazil IPI+ICMS / Malaysia 消费税）。
- **VAT 可回收性**：B2B 进口商可回收 VAT（EU/UK 注册、AU GST 注册）；关税与 CVD 为永久成本。落地价显示全 VAT-inclusive 数 =「边境现金需求」，非「最终净成本」。
- **非欧关税为近似值**（Turkey 40% / Indonesia 50% / Singapore 20% / Brazil 35% / Mexico 50% 等），标 estimate 待人工复核，不当已确认事实。

## 6. 与 .net 方法论一致性

- 公式、复合顺序、CVD 六档、`brand_cvd`、`markets` 税率与 `.net` `tariffs.json` **逐字段一致**（本仓与 `.net` 抽核 = 0 差异）。
- 10 款车型 frontmatter `landed_cost` / `landed_cost_markets` 与 `.net` **完全一致**。
- 回归脚本（.net）`scripts/test_landed_cost_regression.py`：9 用例 PASS + 全量 517×30 重算 0 真实偏差（±$0.01 取整伪差 78 处，cosmetic）。
