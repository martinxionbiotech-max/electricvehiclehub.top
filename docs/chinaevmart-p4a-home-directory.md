# ChinaEVMart Phase 4a — 首页 + 车型目录模板重建

> 仓库：`electricvehiclehub.top`（chinaevmart.com 代码库）
> 阶段：Phase 4-A 首页 / 4-B 车型目录
> 日期：2026-10-22 · 单一数据源 = `src/content/vehicles/*.md` + `src/content/brands/*.md`
> 校验：`npm run build` → **899 页, exit 0** · sitemap **700 URL 不变** · 无新增可索引筛选 URL

---

## 0. 结论摘要

| 维度 | 结果 |
|---|---|
| 首页定位 | 车型发现为主入口 + 定位句按 P2 规范（信息平台非卖家） |
| 精选车型 | 仅 `quality_tier = A`（433 款中取 6 款），无达标项不硬凑 |
| 品牌墙 | 硬编码 72 项数组 → **品牌集合实时推导**（P2-4 关闭） |
| 目录筛选器 | 动力/车身/品牌/价格带 4 维，**纯客户端 JS，零可索引筛选 URL** |
| 动力标签体系 | BEV/PHEV/EREV/HEV/ICE 全称+缩写，新增 `lib/powertrain.ts` 单一术语源 |
| 数据集范围说明 | 口径（ex-factory reference）/ 价格含义 / 续航标准 CLTC / 完整度分级，4 条明示 |
| 公开计数对账 | 517 车型 / 72 品牌，均从数据集实时计算（`site-stats.ts` 扩展 HEV/ICE 分列） |
| 移除无支撑项 | 「complete product database」「source-verified」「500+」「58 品牌墙」注释，全部清除 |

---

## 1. 首页区块清单（4-A）

| 区块 | 前 | 后 |
|---|---|---|
| HERO | 「The complete product database for Chinese EVs」+「source-verified product record」+「500+」 | 定位句「Discover Chinese new-energy vehicles by the data」+ P2 规范句，移除「complete / source-verified / 500+」 |
| 车型发现 | 4 维客户端筛选（品牌/动力/车身/价格带） | 保留，动力 chips 按枚举顺序 + title 全称，新增动力/口径注释 |
| 精选车型 | 按 `battery_type && drive_type && motor_type && charging_interface` 四字段齐全筛选 | **按 `quality_tier === 'A'`** 筛选（433 款中取 6 款），注明「A-tier data-completeness bar」，空态有兜底文案 |
| 入口导航 | 无独立入口区 | 新增「Explore further」：品牌浏览 / 对比（blog comparison tag）/ 技术专题（glossary）/ 出口指南（外链 .net） |
| 品牌墙 | 硬编码 72 项数组 + `// 58 品牌墙` 错误注释 | `brands` 集合实时推导 + 计数 `{brandCount} Chinese EV brands` |
| B2B 联系 | 「Every model, one structured record」泛化 CTA | 「Researching at scale? Talk to us」+ 如实标注 Chengguang Energy / 信息平台非卖家 |

### 移除的无支撑统计/模糊最高级（P1 登记项逐清）

| 项 | 位置 | 处置 |
|---|---|---|
| `The complete product database` | hero H1 | 改为定位句，去「complete」 |
| `source-verified product record` | hero 副文 | 移除（517/517 `data_reviewed=false`，无法支撑「verified」） |
| `500+ Chinese EVs` | meta description | 改为「517 vehicles across 72 brands」（实时计数） |
| `complete Chinese EV product database` | meta description 尾句 | 改为 ex-factory/CLTC 口径说明 |
| `// 58 品牌墙` 注释 vs 72 项 | 首页脚本区 | 硬编码数组整体删除，改集合推导（P2-4） |
| `Every model, one structured record` | 末 CTA | 改为 B2B 联系如实表述 |

---

## 2. 车型目录筛选器与防近重复机制（4-B）

### 2.1 筛选字段（对接规范化字段）

| 维度 | 数据字段 | 呈现 |
|---|---|---|
| 动力形式 | `powertrain`（枚举 BEV/PHEV/EREV/HEV/ICE） | chips 按 `POWERTRAIN_ORDER` 顺序 + `title` 全称，仅呈现数据中存在的值 |
| 车身类型 | `type`（13 类枚举，当前 4 类有值） | chips 仅呈现 SUV/Sedan/MPV/Hatchback |
| 品牌 | `brand` → `brandLabelMap` 显示名 | `<select>` 下拉 |
| 价格带 | `price_usd` | Under $10k / $10k–20k / $20k–30k / $30k+ |

### 2.2 防近重复机制（零可索引筛选 URL）

- 筛选**纯客户端 JS**（`render()` 过滤内存中的 `items` 数组），**不写 URL 参数、不产出 `?powertrain=...` 等查询串页面**。
- 目录页 `href` 仅车型详情页 + 静态资源（favicon `?v=` 缓存参数），**无任何可索引筛选组合 URL**。
- 与首页 discovery 同策略：筛选交互用 JS/片段，不新增路由、不改 sitemap。
- 验证：sitemap 仍 700 URL 不变；`dist/vehicles/index.html` 无 `?powertrain=/&type=` 等参数链接。

### 2.3 数据集范围说明（口径/价格含义/续航标准）

目录页顶部新增「About this dataset」4 条：

1. **Scope**：517 记录 / 72 品牌，含 BEV/PHEV/EREV/HEV + 少量 ICE 对照。
2. **Prices**：USD，China ex-factory reference（起始价），非零售/FOB/landed，须向供应商确认。
3. **Range**：按测试标准标注（CLTC 默认，WLTP/EPA/NEDC 分列），CLTC 高于 WLTP。
4. **Completeness**：记录按 A/B/C 分级，缺失字段标 N/A 不估算。

---

## 3. 公开计数对账（实时计算）

| 计数 | 值 | 来源 |
|---|---|---|
| 车型 | **517** | `vehicles.length`（内容集合） |
| 品牌 | **72** | `brands.length`（内容集合） |
| 精选（A 层） | **433** | `vehicles.filter(quality_tier==='A').length` |
| BEV / PHEV / EREV / HEV / ICE | 286 / 154 / 58 / 16 / 3 | `site-stats.ts`（新增 `hevCount`/`iceCount` 分列） |

- `site-stats.ts` 原 `otherPowertrainCount`（HEV+ICE 合并）拆分为 `hevCount` + `iceCount` 分列，保留 `otherPowertrainCount` 兼容（about 页引用 `bev+phev+erev+other`）。
- 首页/目录所有公开数字均从数据集实时推导，**无硬编码计数**。

---

## 4. 新增/修改文件

| 文件 | 变更 |
|---|---|
| `src/lib/powertrain.ts` | **新增**：动力标签单一术语源（POWERTRAIN_ORDER / POWERTRAIN_LABELS / powertrainLabel / powertrainCode） |
| `src/lib/site-stats.ts` | HEV/ICE 分列（`hevCount`/`iceCount`） |
| `src/pages/index.astro` | 首页重建（定位句 / 精选 A 层 / 品牌墙动态 / 入口区 / B2B / 移除无支撑项） |
| `src/pages/vehicles/index.astro` | 目录重建（筛选器 / 数据集说明 / 实时计数 / 动力标签） |

---

## 5. 验证结果

| 检查 | 结果 |
|---|---|
| `npm run build` | ✅ 899 页, exit 0 |
| 首页 title/desc | ✅ 「China EV Mart — Chinese New-Energy Vehicle Database」+ 定位句 |
| 首页计数 | ✅ 517 vehicles / 72 brands / 6 精选（全 A-tier） |
| 首页最高级残留扫描 | ✅ 0 命中（complete product database / source-verified / 500+ / 58 brand 均清除） |
| 目录 title | ✅ 单 `<title>`（移除冗余 `<SEO>`，消除一页双 title） |
| 目录筛选 chips | ✅ BEV/EREV/HEV/ICE/PHEV 全呈现 |
| 目录数据集说明 | ✅ 4 条明示 |
| 无新增可索引筛选 URL | ✅ 目录/首页无 `?param=` 链接 |
| sitemap | ✅ 700 URL 不变 |

---

## 6. 分离声明

- **已完成（已验证）**：首页 + 目录两模板重建、动力标签体系、实时计数对账、无支撑统计清除、零可索引筛选 URL。均有文件/行号证据 + build 抽检。
- **未覆盖**：线上逐页 HTTP 抓取、about 页/landed-cost-methodology 页等其余模块页的「complete/source-verified」措辞（属 Phase 6 内容优先批）、landed-cost 数据字段残留决策（属 Phase 5）、价格/税率权威溯源（待人工）。
- **顺延**：`data_reviewed: false` 517/517、`verification_status` 几乎全 None（P1-8，Phase 3 复核流水线）。

---

*报告路径：`docs/chinaevmart-p4a-home-directory.md`*
