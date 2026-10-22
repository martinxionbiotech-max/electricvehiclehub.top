# P0 成本一致性修复报告（p0-cost-consistency）

- 日期：2026-10-22
- 仓：`electricvehiclehub.top`（参照仓）· 同修生产仓 `CNEVhub`（electricvehiclehub.net）
- 风险：外部审计 B 级——同一页面同一市场落地成本出现两套不一致数字

## 1. 根因

每个车型的 markdown 正文（frontmatter 之后的 `<Content />` 正文区）在早期由
`generate_all_vehicle_md.py` 生成时，**硬编码了两段落地成本表格**：

1. `## Landed Cost by Market` —— 30 市场总价表（与 frontmatter `landed_cost_markets` 同源）
2. `## Detailed Breakdown — Germany` —— 德国逐项明细表（与 frontmatter `landed_cost` 同源）

与此同时，模板 `src/pages/vehicles/[slug].astro` 又从 frontmatter 的
`landed_cost`（德国明细）+ `landed_cost_markets`（30 市场）**再渲染两块相同内容**
（"Estimated Landed Cost by Market" 卡片列表 + "Estimated Landed Cost
Breakdown — Germany" 明细表）。

因此每页存在 **4 处落地成本渲染**（正文 2 处硬编码 + 模板 2 处 frontmatter 驱动），
同一字段重复展示。

**数字漂移来源**：`fix_brand_cvd.py` / `recompute_from_tariffs.py` 后续按
EU Reg 2024/2754 修正了 frontmatter 的反补贴税率（default 18.8%→20.7%、
部分品牌 17% / 0 等），但**只改了 frontmatter，从未重新生成正文硬编码表格**。
正文明细表停留在旧税率（CV duty 标 "18%"、总值 $12,043），而 frontmatter 已是新税率
（20.7%、总值 $12,129.87 → 渲染 $12,130）。

## 2. 两处数字来源（以 bestune-pony 为例）

| 来源 | 区块 | 德国总值 | 反补贴 | VAT |
|---|---|---|---|---|
| 正文硬编码（旧） | `## Detailed Breakdown — Germany` | **$12,043** | "18%" $724 | 19% $869 |
| frontmatter（新） | `landed_cost` + `landed_cost_markets` | **$12,129.87** → 渲染 **$12,130** | 20.7% $796.95 | 19% $882.92 |

- 正文 `## Landed Cost by Market` 表数值与 frontmatter `landed_cost_markets` 基本一致（仅舍入差异），
  但仍属重复渲染。
- `## Overview` 散文中的数字（"Germany applies a 20.7% countervailing duty…"）已由
  `de_template.py` 与 frontmatter 对齐，**无漂移**（全量核验 0 命中），不属本次不一致来源。

## 3. 受影响页数

- **517 / 517 页全部存在双渲染**（正文硬编码 + 模板 frontmatter 驱动各渲染一遍）。
- 其中 **266 页数值真漂移**（正文 "Total landed" 与 frontmatter `total_landed_usd` 差 > $1）。
- 101 页仅舍入差异（正文截断 vs 模板 `Math.round` 半进位，差值 ≤ $1）。
- 149 页数值一致但仍重复渲染。

真漂移最大案例（正文旧值 vs frontmatter 新值）：

| slug | 正文旧总值 | frontmatter 新总值 | 差 |
|---|---|---|---|
| yangwang-u8l | $286,952 | $242,587 | −$44,365 |
| yangwang-u8 | $247,095 | $209,037 | −$38,058 |
| zeekr-9x | $108,645 | $92,497 | −$16,148 |
| tank-700 | $100,341 | $85,507 | −$14,834 |
| bestune-pony | $12,043 | $12,130 | +$87 |

完整漂移清单见 `scripts/` 运行时输出；受影响品牌集中在 Yangwang/Tank/Zeekr/Li Auto/
Voyah/Fangchengbao/JAC/Hongqi 等高价值 SUV 与 Bestune/Aeolus/Aion/Arcfox/Avatr/Baojun 等
default-CVD 品牌（18.8%→20.7% 修正后正文未同步）。

## 4. 修复方式

**单一数据源 + 单一渲染**：保留信息最全的呈现（模板的 "Estimated Landed Cost by
Market" 30 市场卡片 + "Estimated Landed Cost Breakdown" 逐项明细，含置信度、EV Hub
estimate 标注、最低价高亮、计算器互链），删除正文硬编码的两段表格。

- 脚本 `scripts/remove_landed_cost_dup.py`：正文从 `## Landed Cost by Market` 起截断，
  只保留 H1 + 简介 + `## Overview` 散文；frontmatter（`landed_cost` + `landed_cost_markets`）
  完全不动，成为唯一数据源。
- 幂等：重跑 0 diff（正文已无该区块则跳过）。
- 数字口径统一：模板 `Math.round` 半进位、USD 千分位、含税标注（"VAT" / "Total landed"）
  由模板统一渲染，正文不再有第二套口径。

## 5. 验证结果

- `npm run build`：**.top 900 页**、**CNEVhub 1040 页**，均 exit 0。
- 全量 517 页核验 `scripts/verify_cost_consistency.py`（.top 与 CNEVhub 各跑一遍）：
  - 渲染 "Estimated Landed Cost Breakdown" 总价 == `Math.round(frontmatter.total_landed_usd)`
  - 渲染德国市场卡片价 == `Math.round(frontmatter.markets[Germany].total_landed_usd)`
  - 正文源文件与渲染 HTML 均无 `## Detailed Breakdown` / `## Landed Cost by Market` 残留
  - 结果：**issues=0（两仓均 0）**
- bestune-pony 渲染抽验：$12,130 出现 2 次（市场卡片 + 明细总价，同源一致）、
  陈旧 $12,043 = 0、`Detailed Breakdown` 正文标题 = 0、CV duty $797 / VAT $883 正确渲染。
- 抽 10 页成本区块一致性：随全量 517 页核验覆盖（强于抽样），0 异常。
- 无残留占位（`undefined`/`null`/`NaN`/`{…}` 未新增）。

## 6. 生产仓 CNEVhub 核查

`repos/CNEVhub`（electricvehiclehub.net）**存在完全相同问题**：517 页均双渲染，
266 页真漂移、101 页舍入差异、149 页数值一致但重复；bestune-pony 同样 $12,043 vs $12,129.87。
已用同一脚本 `remove_landed_cost_dup.py` 修复（517 页），build 1040 页 exit 0，
`verify_cost_consistency.py` issues=0。

## 7. Commit

- `.top`：`p0-cost-consistency: single-source landed cost — remove hardcoded markdown body tables (517 files); 266 stale pages reconciled to frontmatter`
- `CNEVhub`：同标记 `p0-cost-consistency`（同步修复生产仓）。
