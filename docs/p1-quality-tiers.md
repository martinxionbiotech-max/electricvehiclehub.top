# P1 质量分层报告（p1-quality-tiers）

- 日期：2026-10-22
- 仓：`electricvehiclehub.top`（517 车型）
- 风险：外部审计 A 级——页面结构相似、缺独立决策价值
- 目标：按「独立决策价值」把 517 页分成 A / B / C 三层，C 层加诚实「数据待补」标注（不删除、不隐藏）

## 1. 判据（三个可复现指标）

每页程序化算三个指标（脚本 `scripts/p1_quality_tiers.py`，幂等）：

| 指标 | 定义 | 阈值 |
|---|---|---|
| **完整性 completeness** | 24 个「决策字段」中已填比例（按动力形式排除合法留白：HEV/ICE 无纯电续航/电池/充电口） | < 0.72 判「数据缺」 |
| **叙事模板化 tmpl_rate** | Overview 散文句子的掩码骨架被 ≥2 篇复用的比例 | ≥ 0.50 判「同构」 |
| **核验状态 verification_status** | `verified` / `partial` / `unverifiable`（P0 抽 40 款打标） | `unverifiable` → 直接 C |

**决策树**：

1. `verification_status = unverifiable` → **C**（整篇无权威源）
2. `completeness < 0.72` → **C**（数据待补）
3. `partial 且 completeness < 0.85` → **C**（待核验多 + 数据不全）
4. `tmpl_rate ≥ 0.50` → **B**（数据完整但叙事同构）
5. 其余 → **A**（完整 + 有据 + 差异化叙事）

## 2. 分层统计

| 层 | 数量 | 占比 | 处置 |
|---|---|---|---|
| **A 层**（直接保留） | **433** | 83.8% | 数据完整 + 差异化叙事，保留 |
| **B 层**（标待差异化） | **53** | 10.3% | 数据完整但叙事同构，进入去模板化队列 |
| **C 层**（数据待补标注） | **31** | 6.0% | 加可见「Data status: partial」标注块 |

核验状态分布：`verified` 2 · `partial` 36 · `unverifiable` 2 · 未抽检 477。

## 3. 渲染层落地

- 新增 frontmatter 字段 `quality_tier: "A"|"B"|"C"`（517/517 已写入，`src/content.config.ts` schema + `[slug].astro` 模板支持）。
- **C 层页**标题下方渲染醒目琥珀色标注块：

> **Data status: partial — verify before purchase decisions**
> Key specifications (range, battery, power, or performance) are not fully confirmed for this model. Figures shown are indicative and should be verified against the manufacturer or a supplier quote before ordering.

- A / B 层不加可见标注（B 的「待差异化」是编辑队列标记，非用户可见数据缺陷；`quality_tier` 字段已持久化供后续批使用）。

## 4. C 层清单（31 款，含判据）

- `byd-qin-l-dm-i`、`chery-explore-06-c-dm` —— **unverifiable**（Wikipedia 无对应车型/代际，全字段待核验，P0 已标）。
- 其余 29 款 —— **数据缺**（缺 battery_kwh / motor_power_kw / torque_nm / accel_0_100_s / top_speed_kmh / range_cltc_km 等核心规格，完整性 0.46–0.71）：

`aion-v-plus`, `byd-qin-max-dm-i`, `chery-fulwin-t6`, `chery-fulwin-x3`, `chery-fulwin-x3-plus`,
`cowin-kunlun-ihd`, `dongfeng-epi-007-plus`, `dongfeng-epi-m8`, `forthing-xinghai-v6-plus`,
`gac-motor-xiangwang-m8`, `gac-motor-xiangwang-s7`, `geely-galaxy-starshine-7`, `geely-galaxy-starship-7-ev`,
`icaur-03t`, `im-ls8`, `jac-ieva50`, `jetour-shanhai-l9`, `jmc-yi-chi-05`, `jmc-yi-chi-05s`,
`jmc-yi-chi-06`, `jmc-yichi-ev3`, `kaicene-changxing-ev`, `landian-e5`, `maxus-mifa-5`,
`maxus-mifa-9-phev`, `ora-5`, `roewe-i6-max-phev`, `roewe-imax8-dmh`, `seres-sf5`

C 层品牌集中：JMC(4)、Chery Fulwin(3)、BYD(2)、Dongfeng(2)、GAC(2)、Geely Galaxy(2)、Maxus(2)、Roewe(2) 等冷门/新款/子型号。

## 5. B 层清单（53 款，数据完整但叙事同构）

`aion-n60`, `aion-rt`, `aion-s`, `aion-s-max`, `aion-s-plus`, `aion-y`, `aito-m6`, `arcfox-t1`,
`baw-yuanbao`, `bestune-nat`, `byd-sealion-05-dm-i`, `byd-sealion-06`, `byd-sealion-06-dmi`,
`byd-sealion-07-dm-i`, `byd-song-l-dmi`, `byd-song-plus`, `byd-xia`, `byd-yuan-up`,
`chery-fulwin-a9l`, `chery-fulwin-t11`, `chery-fulwin-t9`, `chery-tiggo-7-c-dm`,
`chery-tiggo-8-plus-c-dm`, `deepal-s07`, `exeed-exlantix-et`, `forthing-xinghai-t5`,
`geely-galaxy-a7`, `geely-galaxy-starship-7`, `geely-galaxy-xingyuan`, `geometry-g6`,
`hongqi-e-hs7`, `hongqi-eh5`, `jac-ic5`, `jac-ievs4`, `jac-yiwei-hua-xian-zi`,
`jetour-shanhai-l7`, `jetour-t1`, `jetour-x70-c-dm`, `leapmotor-a10`, `leapmotor-b01`,
`leapmotor-b10`, `leapmotor-c10`, `lynk-co-05`, `mg-07`, `mg-pilot-phev`, `mg-s5-ev`,
`neta-aya`, `skywell-ev6`, `tank-400`, `venucia-v-online-dd-i`, `wey-03`, `xpeng-g9l`, `zeekr-x`

## 6. A 层（433 款，完整清单）

A 层 433 款按品牌分布：BYD(36)、Wuling(19)、Changan(14)、Geely Galaxy(14)、Hongqi(12)、Leapmotor(12)、Lynk & Co(11) 等。完整 slug 清单见 `scripts/p1_quality_tiers.json` 的 `tiers.A`（433 项，程序化可复现）。

## 7. 发现的其他问题（不在本批修复范围，记录待后续批）

- **正文散文与 frontmatter 漂移（P0 遗留）**：P0 数据核验只改了 frontmatter，未同步正文 `<Content />` 的「简介列表 + Overview 散文」。实测约 11 款 P0 修正款正文仍含旧值（`byd-seagull` 0-100 4.9s、`byd-seal` 450km/17% CVD、`byd-han` 72kWh、`changan-nevo-lamore` 330Nm/9.07kWh、`yangwang-u8` 3.9s、`m-hero-917` 600kW、`fangchengbao-bao-5` 485kW、`tank-700` 120kW/400Nm、`wey-lanshan` 300kW、`denza-z9-gt` 640kW/3.6s、`geely-galaxy-e5` 180km/h/18.8% CVD）→ 页面前端指标卡（frontmatter）与正文散文出现**同页数字矛盾**，需单独「正文散文同步批」（P2）。
- **data_source 无完整 URL**：517/517 有 `data_source` 但均为域名提及（`en.wikipedia.org`），0/517 含可解析完整 URL（详见 p1-provenance-audit）。

## 8. 验证

- `npm run build` 900 页 exit 0。
- 抽 10 页渲染（A×4 / B×3 / C×3）：五段标题齐全、C 层标注块仅 C 层出现、0 残留占位（`undefined`/`null`/`NaN`/`{…}`）——全 OK。
- sitemap 不变（517 车型 + 其余页，无增删页）。
