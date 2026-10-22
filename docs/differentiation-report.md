# Differentiation Report — EVHub Top 转型纯产品信息站

日期：2026-10-22 · 仓：electricvehiclehub.top · 定位分离：.net 保留出口情报（落地成本/关税/计算器）· .top 转型纯产品信息站

## 四步改动摘要

### 1. differentiate-home — 首页定位切换
- 标题/描述：`The Real Landed Cost of Importing Chinese EVs` → `Chinese EV Product Database`（deep specifications / versions / technology）。
- Hero 文案移除 landed-cost 主打与「$14,000 落地价」示例，改为产品数据库定位。
- 移除「落地成本示例条」（BYD Qin Plus/Seal/Xiaomi SU7 +112.7% 等 3 卡）与「From factory price to landed price, in 3 layers」三步成本拆解。
- 新增车型发现区：品牌 / 车身类型 / 动力形式 / 价格带四维客户端筛选 + 深度档案精选区块（电池化学/驱动/电机/充电四字段齐全的旗舰车型）。
- `site.ts` 站点描述与公司描述同步去成本导向措辞。

### 2. differentiate-template — 车型页模板五段重配权
- 五段：① Entity Snapshot ② Powertrain ③ Dimensions & Logistics ④ Technology（增强）⑤ Market Compliance & Export Profile（降权）。
- 移除 landed-cost 数据表（Estimated Landed Cost by Market / Breakdown）与出口成本块（.net 专属）。
- ⑤ 降权为精简「Export notes → electricvehiclehub.net」指引行 + 保留 HS Code / 认证合规事实。
- 517 篇车型 description 去「landed cost」三种结尾措辞（脚本幂等，零 diff）。

### 3. differentiate-calculator — 计算器页移除
- `/landed-cost-calculator/` 从 .top 删除，`_redirects` 加跨域一对一 301 → `https://electricvehiclehub.net/landed-cost-calculator/`（含无尾斜杠变体）。
- nav/footer 移除「Landed Cost」「Landed Cost Calculator」链接；markets 页计算器链接改为跨域外链。
- sitemap 中 calculator URL 已移除（899 页，较 900 减 1）。

### 4. differentiate-product-info — 产品信息丰富化
- trim/版本差异表：有 trim 数据的车型（81 款）在 Entity Snapshot 下渲染「Versions / trims」列表。
- 规格总表补全渲染层缺失字段：Family/nameplate、Currency、Price、FOB price range、Range (long, CLTC)、Battery thermal、Drive layout、Motor model、Total power、Suspension、Brakes、Cd、Charging、Infotainment、Network、Certification、HS code、Data tier、Verification status 等（63 字段全量）。
- 技术实体互链：电池类型/驱动架构/电机类型/Cd → `/docs/glossary/#technology-terms`，充电接口 → `/blog/ccs2-vs-gbt-charging/`。
- 术语表新增「Technology terms」段（电池化学/电机类型/驱动架构/充电接口/热管理/热泵/Cd）。
- 模块页 meta 去成本导向：about / contact / faq / vehicles / brands / disclaimer / accessibility。

## URL 变更（calculator 301）
| 原 URL | 新 URL | 状态 |
|---|---|---|
| `/landed-cost-calculator/` | `https://electricvehiclehub.net/landed-cost-calculator/` | 301 |
| `/landed-cost-calculator` | `https://electricvehiclehub.net/landed-cost-calculator/` | 301 |

## 标题措辞前后对比（3 例）
| 位置 | 前 | 后 |
|---|---|---|
| 首页 title | EVHub Top — The Real Landed Cost of Importing Chinese EVs | EVHub Top — Chinese EV Product Database |
| 车型 description（517 篇统一结尾） | "…Full landed-cost breakdown across 30 export markets for B2B import planning." | "…Full product specification in the Chinese EV database." |
| about 页 description | "independent information platform for importing Chinese electric vehicles, built on transparent landed-cost data and verified export compliance." | "independent Chinese EV product database — deep, source-verified specifications, versions, and technology data across 72 brands." |

## 产品信息增强点
- trim/版本列表（81 款有据渲染）。
- 63 字段全量规格表（补全 Family/Currency/FOB range/long range/thermal/drive/motor/suspension/brakes/Cd/charging/infotainment/network/cert/HS/data tier/verification）。
- 技术实体互链（电池/电机/驱动/充电 → 术语表 + CCS2 对比文）。
- 术语表 Technology terms 8 词条。

## 验证
- `npm run build`：899 页，exit 0。
- 首页渲染抽检：产品库标题 + 发现筛选 + 0 landed-cost 命中。
- 车型 5 篇抽检（byd-seal / xiaomi-su7 / zeekr-001 / yangwang-u8 / wuling-hongguang-mini-ev）：landed-cost 表 0 命中，Export notes 各 1。
- sitemap：calculator URL 已移除，0 命中。
- 计算器重定向：`_redirects` 两条跨域 301 就位。

## 残留（已知，本批范围外）
- 车型 frontmatter `landed_cost` / `landed_cost_markets` 数据字段保留（模板已不渲染；数据层未动，符合「只改渲染、不破坏数据」纪律）。
- 品牌/文档/博客正文中的「landed cost」措辞与 `/landed-cost-calculator/` 内链由 301 兜底，未逐篇改写（属出口情报内容，.net 定位）。

## Commit 列表
- `6c97b1e` differentiate-home
- `02f578e` differentiate-template
- `b14cc6b` differentiate-calculator
- `5694cfa` differentiate-product-info
