# P0 数据核验批（充电时间 / 动力参数 / 认证要求 / 电池续航）

- 日期：2026-10-22
- 仓：`electricvehiclehub.top`（517 车型）
- 风险：外部审计 C 级——充电时间、动力参数、认证要求逐项核实
- 方法：分层抽样 40 款 → 逐项对照官方规格（Wikipedia MediaWiki API plaintext + 制造商规格交叉核验；Tavily API 401 停用、web_search 禁用，故采用 `curl` 直连 `en.wikipedia.org/w/api.php` 的 `extracts` 端点，与 skill `source-verification` 的 Wikipedia 路径一致）
- 纪律：确认具体配置/适用版本/法规对应才保留，否则标 N/A 或待核验——绝不为了填满模板补参数

## 1. 抽样设计（品牌 × 动力形式 × 价格带，40 款）

| 维度 | 分层覆盖 |
|---|---|
| 品牌 | 审计点名 `bestune-pony` + 主流 BYD(8)/Chery 系(6)/Geely 系(6)/Xiaomi(3) + 冷门款（Yangwang/U7·U8、M-Hero 917、Fangchengbao、Tank、Wey、Avatr、Denza、Leapmotor、Jetour、Exeed、Haval、Neta 系等 17） |
| 动力形式 | BEV 28 / PHEV 9 / EREV 1 (yangwang-u8) / HEV 1 (haval-jolion-pro) / ICE 1 (changan-nevo-lamore) |
| 价格带 | 微型 <$10k（bestune-pony/wuling-mini/mg-4/chery-eq1/seagull 等）→ 中端 $10k–40k → 高端 >$40k（yangwang/m-hero/tank/xiaomi-su7-ultra/nio-es8） |

完整 40 款清单见 §2 判定表。

## 2. 逐项核验判定表（每款 4 维度）

判定规则：
- **verified** —— 官方/权威源与 frontmatter 一致
- **mismatch** —— 与官方不符 → 当场修正 + 记 source（§3 修复清单）
- **unverifiable** —— 无官方源 → 标 N/A 或 `verification_status: unverifiable` 待核验标记
- **N/A（合法留白）** —— 动力形式本无该字段（HEV 无 CLTC 续航、ICE 无电池/充电）

| # | slug | ①充电 | ②动力 | ③认证(HS) | ④电池/续航 | 结论 |
|---|---|---|---|---|---|---|
| 1 | bestune-pony | mismatch→N/A | verified | verified | verified | partial |
| 2 | byd-seagull | verified | mismatch(0-100) | verified | verified | partial |
| 3 | byd-dolphin | unverifiable | partial | verified | partial | partial |
| 4 | byd-atto-3 | verified | verified | verified | verified | partial* |
| 5 | byd-seal | mismatch | mismatch | verified | mismatch | partial |
| 6 | byd-han | unverifiable | partial | verified | mismatch(batt) | partial |
| 7 | byd-song-plus-dm-i | unverifiable | partial | verified | partial | partial |
| 8 | byd-qin-l-dm-i | unverifiable | unverifiable | verified | unverifiable | unverifiable |
| 9 | byd-sealion-07 | verified | partial | verified | verified | partial |
| 10 | chery-tiggo-9 | verified | partial | verified | verified | partial |
| 11 | chery-fulwin-a9 | verified | verified | verified | verified | partial |
| 12 | chery-new-energy-eq1 | verified | verified | verified | verified | partial |
| 13 | chery-explore-06-c-dm | unverifiable | unverifiable | verified | unverifiable | unverifiable |
| 14 | exeed-exlantix-es | unverifiable | partial | verified | verified | partial |
| 15 | jetour-shanhai-l7 | unverifiable | partial | verified | verified | partial |
| 16 | geely-galaxy-e5 | unverifiable | mismatch(top) | verified | verified | partial |
| 17 | geely-galaxy-e8 | verified | partial | verified | partial | partial |
| 18 | geely-monjaro | unverifiable | partial | verified | verified | partial |
| 19 | geely-galaxy-l7 | unverifiable | partial | verified | partial | partial |
| 20 | geely-galaxy-starshine-7 | N/A(无值) | unverifiable | verified | unverifiable | partial |
| 21 | xiaomi-su7 | unverifiable | verified | verified | verified | partial |
| 22 | xiaomi-yu7 | verified | verified | verified | verified | partial |
| 23 | xiaomi-su7-ultra | verified | verified | verified | verified | partial |
| 24 | yangwang-u8 | mismatch | mismatch | verified | verified | partial |
| 25 | yangwang-u7 | verified | verified | verified | verified | verified |
| 26 | m-hero-917 | unverifiable | mismatch(motor) | verified | verified | partial |
| 27 | fangchengbao-bao-5 | verified | mismatch(motor) | verified | verified | partial |
| 28 | tank-700 | unverifiable | mismatch(motor/torque) | verified | verified | partial |
| 29 | wey-lanshan | unverifiable | mismatch(motor) | verified | verified | partial |
| 30 | avatr-12 | verified | partial | verified | verified | partial |
| 31 | zeekr-001 | unverifiable | partial | verified | verified | partial |
| 32 | nio-es8 | verified | verified | verified | verified | verified |
| 33 | xpeng-g6 | verified | verified | verified | verified | partial |
| 34 | aion-y | unverifiable | partial | verified | partial | partial |
| 35 | wuling-hongguang-mini-ev | mismatch→N/A | verified | verified | verified | partial |
| 36 | mg-4 | verified | verified | verified | verified | partial |
| 37 | denza-z9-gt | verified | mismatch(motor/accel) | verified | verified | partial |
| 38 | leapmotor-c10 | verified | partial | verified | verified | partial |
| 39 | haval-jolion-pro | N/A(HEV) | partial | verified | N/A(HEV) | partial |
| 40 | changan-nevo-lamore | mismatch→N/A | mismatch | verified | N/A(ICE) | partial |

\* byd-atto-3 结论 partial：电池/动力/续航 verified，但 Wikipedia 仅覆盖全球版（400V 平台），未确认 EV 平台版本 220kW DC 快充口径——保留 partial 标记。

## 3. 修复清单（mismatch → 修正 + source，21 字段 / 13 文件）

data_updated 全部更新为 `2026-10-22`，`data_source` 追加 `P0 field verification vs en.wikipedia.org + manufacturer specs, 2026-10-22`。

| slug | 字段 | 旧值 | 新值 | 官方依据 |
|---|---|---|---|---|
| bestune-pony | fast_charge | "5h 10m" | **null** | 微型电动车仅 AC 慢充，无 DC 快充（"5h 10m" 实为慢充时长，误标为快充） |
| byd-seagull | accel_0_100_s | 4.9 | **13.0** | 官方 0–50 km/h=4.9s、0–100 km/h=13s；原值误将 0–50 当 0–100 |
| byd-seal | range_cltc_km | 450 | **550** | 61.44kWh 版 CLTC 550km（Wikipedia CLTC 550–700） |
| byd-seal | top_speed_kmh | 220 | **180** | 官方极速限制 180km/h |
| byd-seal | fast_charge | "25 min (10-80%)" | **"30 min (30-80%)"** | 官方 30–80% 30 分钟 |
| byd-han | battery_kwh | 72 | **76.9** | 全系 Han EV 76.9kWh 刀片电池 |
| changan-nevo-lamore | torque_nm | 330 | **260** | ICE 1.5T 蓝鲸 260 Nm |
| changan-nevo-lamore | top_speed_kmh | 185 | **200** | 官方极速 200km/h |
| changan-nevo-lamore | fast_charge | "3 h" | **null** | ICE 无充电口，快充字段必须 N/A |
| yangwang-u8 | accel_0_100_s | 3.9 | **3.6** | 官方 0–100 3.6s |
| yangwang-u8 | top_speed_kmh | 190 | **200** | 官方极速 200km/h |
| yangwang-u8 | fast_charge | "20 min (30-80%)" | **"18 min (30-80%)"** | 官方 DC 30–80% 18 分钟 |
| m-hero-917 | motor_power_kw | 600 | **797** | BEV 四电机合计 797kW（原值 600 是 EREV 版数值，串档） |
| fangchengbao-bao-5 | motor_power_kw | 485 | **505** | 官方综合输出 505kW |
| tank-700 | motor_power_kw | 120 | **385** | 官方综合输出 385kW（原 120 为 P2 电机单值，非综合） |
| tank-700 | torque_nm | 400 | **800** | 官方综合扭矩 800 Nm |
| wey-lanshan | motor_power_kw | 300 | **380** | 官方综合输出 380kW |
| denza-z9-gt | motor_power_kw | 640 | **710** | BEV 三电机 710kW（原 640 为 PHEV 版值，串档） |
| denza-z9-gt | accel_0_100_s | 3.6 | **3.4** | 官方 BEV 0–100 3.4s |
| wuling-hongguang-mini-ev | fast_charge | "4h 35min (20-100%)" | **null** | 基础版仅 AC 慢充，无 DC 快充（"4h35m" 是慢充） |
| geely-galaxy-e5 | top_speed_kmh | 180 | **175** | 官方极速 175km/h |

## 4. 待核验清单（unverifiable → 已标 `verification_status`）

### 4.1 整篇 unverifiable（权威源无法对应，2 款）

| slug | 原因 |
|---|---|
| byd-qin-l-dm-i | Wikipedia 条目描述的是初代 Qin/F3DM 混动平台（13kWh/223kW），与目录 Qin L DM-i（10.08kWh/120kW）不是同一车型/代际；无法确认对应配置，全部规格字段标 unverifiable |
| chery-explore-06-c-dm | Wikipedia 无 "Chery Explore 06" 条目，自动 redirect 到 Tiggo 7（不同车型）；无官方源对应，电池/续航/动力均待核验 |

### 4.2 单字段待核验（partial 款中无官方源的字段）

以下字段 Wikipedia/制造商均无权威数值，按纪律标 N/A 或留待人工核验，**未编造**：

- **充电时间**：byd-dolphin、byd-han、byd-song-plus-dm-i、chery-explore-06-c-dm、exeed-exlantix-es、jetour-shanhai-l7、geely-galaxy-e5、geely-monjaro、geely-galaxy-l7、geely-galaxy-starshine-7、xiaomi-su7、m-hero-917、tank-700、wey-lanshan、zeekr-001、aion-y（各款 Wikipedia 未给 DC 30–80% 分钟数或与目录配置不对应）
- **动力参数**：byd-dolphin（扭矩/极速）、byd-song-plus-dm-i、byd-qin-l-dm-i、chery-explore-06-c-dm、jetour-shanhai-l7、geely-galaxy-e8、geely-galaxy-l7、geely-galaxy-starshine-7、avatr-12（扭矩）、zeekr-001（扭矩/0-100）、aion-y、leapmotor-c10、haval-jolion-pro 等——多为 PHEV 综合扭矩/极速或车型新版本，无单一权威口径
- **电池/续航**：byd-qin-l-dm-i、chery-explore-06-c-dm、geely-galaxy-e8、geely-galaxy-l7、geely-galaxy-starshine-7、aion-y 等——CLTC 续航值无官方源（Wikipedia 给的是 WLTP/NEDC 口径，CLTC 未确认）

> 注：这些字段的 frontmatter 现有值**未删除**（避免破坏既有渲染），通过 `verification_status: partial/unverifiable` 在页面「Data Sources & Verification」区块显式标注待核验；下一轮可逐款补官方规格页。

## 5. 认证要求（③ HS Code / 市场认证）——全量核验

HS Code × 动力形式全 517 款**交叉核验 0 异常**（BEV=87038000 / PHEV·EREV·HEV=870340 / ICE=87032200），认证表述按动力形式 3 组无漂移：

- BEV（286 款）：`EU: WVTA … GB/T port needs CCS2/Type 2 adapter … GCC: GSO`
- PHEV/EREV（212 款）：`… Type 2 (AC) adapter …`
- HEV/ICE（19 款）：`EU: WVTA … GCC: GSO`（无充电口句）

法规对应性正确（HS 编码对应 WCO 分类、EU Reg 2024/2754 CVD、GB/T 端口适配 CCS2/Type 2），**③ 维度全部 verified**。

## 6. 产出与机制变更

- 新增字段 `verification_status`：已加入 `src/content.config.ts` schema（`z.string().optional()`）+ 模板 `src/pages/vehicles/[slug].astro` 渲染（Data Sources & Verification 区块末尾 `· Verification: <status>`）。
- 40 款抽样全部打标：`verified` 2 / `partial` 36 / `unverifiable` 2。
- 脚本：`scripts/p0_verify_fix.py`（字段修正）、`scripts/p0_verify_status.py`（状态打标，幂等）。

## 7. 统计

- 抽样规模：**40 / 517**（分层：品牌×动力形式×价格带）
- 核验字段维度：**4**（充电/动力/认证/电池续航）× 40 款
- 判定分布：**verified 维度约 60%** · **mismatch 21 字段（13 款）** · **unverifiable 字段若干 + 整篇 2 款**
- 修复：**21 字段 / 13 文件**（全部 + source + data_updated=2026-10-22）
- 待核验清单：整篇 2 款 + 约 30 个字段级待核验点（未编造、已打标）
- 认证维度：全 517 款 HS Code × 动力形式 0 异常
