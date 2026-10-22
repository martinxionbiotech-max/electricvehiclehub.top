# P1 溯源补强报告（p1-provenance-audit）

- 日期：2026-10-22
- 仓：`electricvehiclehub.top`（517 车型）
- 风险：外部审计 P1——补充官方来源 / 更新时间 / 数据责任人 / 估算边界
- 脚本：`scripts/p1_provenance_audit.py`（幂等，输出 `scripts/p1_provenance_audit.json`）

## 1. 溯源字段覆盖核验（517 全量）

| 字段 | 覆盖 | 缺失 | 结论 |
|---|---|---|---|
| `data_source`（来源说明） | 517 / 517 | 0 | ✅ 全覆盖 |
| `data_updated`（更新时间） | 517 / 517 | 0 | ✅ 全覆盖（日期 `2026-10-19`~`2026-10-22`） |
| `image_source`（图片来源 URL） | 517 / 517 | 0 | ✅ 全覆盖（Wikimedia Commons 完整 URL） |
| `author`（数据责任人） | 517 / 517 | 0 | ✅ 一致，全部 `Wei Wang` |

**缺失清单：`data_source` / `data_updated` / `image_source` / `author` 四字段缺失均为 0。**

## 2. 发现的唯一溯源缺口：data_source 无完整 URL

- 517 / 517 的 `data_source` 均为**域名提及**（`…verified via en.wikipedia.org…`），**0 / 517 含可解析完整 URL**。
- 即：数据来源「有出处说明、无可点击深链」。图片来源（`image_source`）有完整 URL，但规格数据来源无。
- **诚实处置**：不改写、不编造 per-vehicle URL（多数冷门款无 Wikipedia 条目，见 p0-data-verification §4「整篇 unverifiable 2 款」）。本批仅记录缺口，建议后续「来源深链补强批」：对确有 Wikipedia/制造商规格页的高价值款（BYD Seal/Atto 3/Dolphin/Han、MG4、Zeekr 001、XPeng G6 等）逐款补 `data_source` 完整 URL，无条目款诚实留域名提及。

## 3. 估算边界声明（已落地）

在模板 `[slug].astro` 的 ④ Market Compliance 区块，「Confidence · Last verified」行下统一追加估算口径句（517 页全部渲染）：

> Landed-cost figures are indicative planning estimates (base price + duty, countervailing duty, VAT, freight and compliance fees); final totals vary with shipping route, insurance and supplier quotation — verify before purchase decisions.

与既有「EV Hub estimate」徽标、`Confidence` 字段、Data Sources 区块「EV Hub calculation」清单共同构成完整估算边界披露。

## 4. 数据责任人一致性

- `author` 字段 517 / 517 = `Wei Wang`，与 `src/config/site.ts` 的 `company.author`（Wei Wang, EV & Battery Industry Analyst, Chengguang Energy）一致。
- 页面页脚「Author: Wei Wang (EV & Battery Industry Analyst) · Chengguang Energy」、Article JSON-LD `author.name`、`<meta name="author">` 三处同源，无漂移。

## 5. 相关机制字段

| 字段 | 覆盖 |
|---|---|
| `verification_status` | `verified` 2 · `partial` 36 · `unverifiable` 2 · 未抽检 477 |
| `quality_tier`（本批新增） | `A` 433 · `B` 53 · `C` 31（517/517） |
| `data_reviewed` | 517 均 `false`（渲染为 `Status: Pending review`，诚实声明未人工复核） |

## 6. 结论

- 溯源字段（来源说明 / 更新时间 / 图片来源 / 责任人）**四字段全覆盖、零缺失**，责任人一致。
- 唯一结构性缺口：`data_source` 无完整 URL（0/517），列为后续「来源深链补强批」。
- 估算边界句已统一挂 Market Compliance 区块（517 页）。
