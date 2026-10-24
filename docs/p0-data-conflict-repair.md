# P0 数据冲突修复 · 02 — Yangwang U8 单一数据源核对与全站冲突扫描

> 批次：p0-conflict-02 · 日期：2026-10-24 · 仓库：electricvehiclehub.top
> 纪律：单一数据源（frontmatter）· 冲突标记不自动填补 · 修正挂 source

## 一、Yangwang U8 五组件核对表

单一数据源 = frontmatter。五处渲染组件逐一比对同一字段的值一致性。

| 字段 | frontmatter（源） | 参数表③④ | 摘要②+description | 比较模块⑦ | JSON-LD | 来源记录(body/参数核验) | 结论 |
|---|---|---|---|---|---|---|---|
| price_usd | 154650.0 | $154,650 | $154,650 | — | 154650 | $154,650 | ✅ 一致 |
| price_type | China ex-factory reference price | 同 | 同 | — | 同 | 同 | ✅ 一致 |
| range_cltc_km | **180** | 180 km | 180 km | — | — | body 曾写 **780** | ⚠️ 冲突→已修 |
| battery_kwh | 49.05 | 49.05 kWh | 49 kWh | — | — | 49.05 kWh | ✅ 一致 |
| motor_power_kw | 880 | 880 kW | 880 kW | — | 880 KWT | 880 kW | ✅ 一致 |
| torque_nm | 1280 | 1280 Nm | — | — | — | 1280 | ✅ 一致 |
| accel_0_100_s | **3.6** | 3.6 s | — | — | — | body 曾写 **3.9** | ⚠️ 冲突→已修 |
| top_speed_kmh | **200** | 200 km/h | — | — | — | body 曾写 **190** | ⚠️ 冲突→已修（新发现） |
| battery_type | LFP (Blade) | LFP (Blade) | LFP (Blade) | — | — | 同 | ✅ 一致 |
| hs_code | 870340 | 870340 — PHEV/HEV | — | — | — | 同 | ✅ 一致 |
| drive_type / motor_type | AWD (quad motor) / PMSM | 同 | — | — | — | 同 | ✅ 一致 |
| 尺寸(长宽高/轴距/车重) | 5325/2095/1940/3050/3490 | 同 | — | — | — | 同 | ✅ 一致 |

**U8 冲突字段数：3**（range / accel / top_speed）。价格、电池、电机功率、扭矩、HS Code、尺寸、驱动架构全站五组件一致。

冲突性质：frontmatter 在 P0 字段核验阶段已修正为 BYD 官方值（180 km 纯电、3.6 s、200 km/h），但 markdown body 遗留旧值（780 km 综合续航、3.9 s、190 km/h）未同步——body 是第二个维护点。

## 二、U8 修正（挂 source）

1. `src/content/vehicles/yangwang-u8.md` body：
   - `- **Range**: 780 km (CLTC)` → `180 km (CLTC, electric-only)`
   - `- **0-100 km/h**: 3.9 s` → `3.6 s`
   - `top speed of 190 km/h` → `200 km/h`
2. `src/data/parameter-verification.json` U8 `range`/`accel`：`status: conflict` → `verified`，`verified_at: 2026-10-24`，note 记录 body 修正（挂 source：BYD 官方）。
3. `top_speed` 冲突为**新增发现**（parameter-verification 六参数 schema 未覆盖 top_speed，本批不扩 schema，仅文档记录）。

修正后 U8 六关键字段（price/range/battery/motor/accel/charge）在 parameter-verification 中除 price、charge 维持 `unverifiable`（待核验，非冲突）外，其余已 `verified`。

## 三、全站冲突扫描（扩样）

程序化扫描脚本：`scripts/scan-data-conflicts.py`（解析 frontmatter + description + body prose，比对数值；整数截断视为展示舍入、不判冲突）。输出 `docs/p0-data-conflict-scan.json`。

**规模：517 款全量扫描，真实冲突 32 处 / 26 款车型**（另有 365 处为 description 整数截断舍入，非冲突）。

### 冲突分布

| 组件 | 冲突数 | 字段分布 |
|---|---|---|
| body-prose（遗留正文） | 26 | range 17 · motor 5 · accel 2 · battery 1 · top_speed 1 |
| description（渲染摘要） | 6 | motor 6 |
| **合计** | **32** | |

### 冲突清单（全 32 处）

**body-prose 冲突（26）** — frontmatter 值 vs body 值：

| 车型 | 字段 | frontmatter | body | 参数核验状态 |
|---|---|---|---|---|
| aeolus-l7 | range_cltc_km | 205 | 430 | — |
| avatr-06 | range_cltc_km | 650 | 1190 | unverifiable |
| baw-m8 | range_cltc_km | 505 | 1370 | — |
| bestune-t90 | range_cltc_km | 210 | 1500 | — |
| byd-han | battery_kwh | 76.9 | 72 | — |
| byd-seagull | accel_0_100_s | 13.0 | 4.9 | — |
| byd-seal | range_cltc_km | 550 | 450 | — |
| changan-nevo-q05 | range_cltc_km | 125 | 1215 | — |
| denza-n8l | range_cltc_km | 230 | 1300 | conflict |
| denza-z9-gt | motor_power_kw | 710 | 640 | — |
| denza-z9-gt | accel_0_100_s | 3.4 | 3.6 | — |
| denza-z9 | range_cltc_km | 630 | 1101 | unverifiable |
| fangchengbao-bao-5 | motor_power_kw | 505 | 485 | — |
| fangchengbao-bao-8 | range_cltc_km | 125 | 1200 | unverifiable |
| geely-galaxy-e5 | top_speed_kmh | 175 | 180 | — |
| geely-galaxy-starshine-8 | range_cltc_km | 130 | 1600 | — |
| geely-galaxy-starship-7 | range_cltc_km | 120 | 1355 | — |
| hongqi-h5-phev | range_cltc_km | 130 | 1560 | — |
| jac-qx | range_cltc_km | 120 | 1300 | — |
| leapmotor-c01 | range_cltc_km | 717 | 1175 | — |
| lynk-co-06 | range_cltc_km | 126 | 1280 | — |
| m-hero-917 | range_cltc_km | 505 | 1026 | unverifiable |
| m-hero-917 | motor_power_kw | 797 | 600 | unverifiable |
| tank-700 | motor_power_kw | 385 | 120 | — |
| wey-lanshan | motor_power_kw | 380 | 300 | — |
| yangwang-u8l | range_cltc_km | 200 | 1160 | conflict |

**description 冲突（6）** — frontmatter 值 vs description 值：

| 车型 | 字段 | frontmatter | description |
|---|---|---|---|
| denza-z9-gt | motor_power_kw | 710 | 640 |
| fangchengbao-bao-5 | motor_power_kw | 505 | 485 |
| m-hero-917 | motor_power_kw | 797 | 600 |
| tank-400 | motor_power_kw | 130 | 300 |
| tank-500 | motor_power_kw | 130 | 300 |
| wey-lanshan | motor_power_kw | 380 | 300 |

### 冲突模式归类

1. **续航「综合 vs 纯电」错位（17 处，最高频）**：frontmatter 已统一为纯电 CLTC 续航（125/130/120/505…），body 仍残留增程/插混综合续航（1215/1300/1560/1026…）。U8 同型（180 纯电 vs 780 综合）。
2. **电机功率多值（11 处）**：frontmatter 与 body/description 各存一个值（如 tank-400/500：130 vs 300；tank-700：385 vs 120；wey-lanshan：380 vs 300；m-hero-917：797 vs 600）。
3. **零星错值（4 处）**：byd-seagull 加速 13.0 vs 4.9、byd-han 电池 76.9 vs 72、geely-galaxy-e5 极速 175 vs 180、byd-seal 续航 550 vs 450。

> 处置纪律：本批仅修 U8（任务起点）。其余 26 款冲突**保留标记**（body 不自动填补、不猜测正确值），待逐款挂 source 核验后修正——列为后续批次。

## 四、统一数据源机制 / 模板修复记录

核验结论：**渲染层（摘要② / 参数表③④ / 比较模块⑦ / JSON-LD）已全部由 frontmatter `data.*` 单一渲染，无组件级硬编码数值。**

| 渲染点 | 文件 | 数据来源 | 硬编码检查 |
|---|---|---|---|
| 摘要② | `src/pages/vehicles/[slug].astro` | `data.range_cltc_km` 等 | 无 |
| 参数表③④ | 同上 | `data.*` | 无 |
| 比较模块⑦ | 同上 | `c.data.*`（他人 frontmatter） | 无 |
| JSON-LD | 同上 | `data.price_usd`/`motor_power_kw` 等 | 无 |
| .md 端点 | `src/pages/vehicles/[slug].md.ts` | `data.*` | 无 |
| 目录/首页卡片 | `vehicles/index.astro`、`index.astro` | `data.*` | 无 |

模板修复点：**0 处**。唯一模板内嵌常量为 HS Code 分类回退（`data.hs_code || powertrain→87038000/870340`）——这是分类常量而非逐车数据值，非冲突，保留。

遗留机制风险（记录，不属本批修复）：
- **markdown body prose 是死内容**（不渲染），却是 26 处 body 冲突的根源——`generate_all_vehicle_md.py` 一次性生成的旧快照，P0 核验更新 frontmatter 后未同步。根治方向：body 不再维护规格数值（剥除 `**Range/Battery/Motor power/0-100**` 硬编码 bullet）或由 frontmatter 重新生成。
- **`[slug].astro` 与 `[slug].md.ts` 重复构建规格表**（label 代码重复，值同源 `data.*`）——值不会分叉，但属维护冗余，可抽公共 helper（后续可选重构）。

## 五、验证结果

- 参数核验系统：`parameter-verification.json` 有效（90 款），U8 range/accel 冲突已 resolved。
- 扫描脚本复跑：U8 已从冲突清单消失；全站冲突 35 → 32（-3，全为 U8）。
- build / 抽页 diff / commit 见交付摘要。

## 交付物

- `src/content/vehicles/yangwang-u8.md`（body 三值修正）
- `src/data/parameter-verification.json`（U8 range/accel resolved）
- `scripts/scan-data-conflicts.py`（可复现全站冲突扫描）
- `docs/p0-data-conflict-scan.json`（全站冲突清单机读输出）
- `docs/p0-data-conflict-repair.md`（本报告）
