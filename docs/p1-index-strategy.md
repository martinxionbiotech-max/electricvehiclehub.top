# P1 新旧站索引策略决策建议（p1-index-strategy）

- 日期：2026-10-22
- 风险：外部审计 D 级——新旧站内容重合（.top 与 .net 517 车型近同源）
- 性质：**决策建议文档，不擅自执行**。所有 noindex / 跨域 canonical 改动待用户批准后另行批执行。

## 1. 现状核查（三域名）

| 域名 | 关系 | canonical | robots.txt | sitemap | 结论 |
|---|---|---|---|---|---|
| `electricvehiclehub.top` | 新仓（参照仓） | 自指 `.top` | `Allow: /` 全放行 + `Sitemap: .top` | `.top` sitemap-index | 可索引 |
| `electricvehiclehub.net` | 生产仓 CNEVhub（源站） | 自指 `.net` | `Allow: /` 全放行 + `Sitemap: .net` | `.net` sitemap-index | 可索引 |
| `<project>.pages.dev` | Cloudflare Pages 默认域名（.top 的自定义域映射其上） | 无处理（同 .top 内容） | 无处理 | 无处理 | **可索引（重复）** |

**关键事实**：

- 两仓 canonical 均自指、均全放行，**无任何跨域 canonical 互指**。517 车型页内容近同源（.top 做了深度档案五段 + 去模板化，.net 为基底），两域各自独立进索引 → 重复内容 / 索引稀释。
- `.pages.dev` 是 Cloudflare Pages 自动分配的默认子域，与 `.top` 服务同一构建产物，但**未设 noindex/canonical**，形成第三个可索引副本。
- 两站 robots 均 `Allow: /`（含 GPTBot/ClaudeBot/PerplexityBot 等 AI crawler 显式放行），无抓取矛盾。

## 2. 三个方案

### 方案 A：`.top` 全面 canonical 指向 `.net`（或反之）

**做法**：在 SEO.astro 的 canonical 生成处，让次要域（.top）每页 `<link rel="canonical">` 指向主域（.net）同路径；保留单站 robots/sitemap。

**利**：索引信号集中到单一域，直接消除 .top/.net 重复竞争；改动集中（一处 canonical 逻辑）；对源站 .net 零破坏。

**弊**：.top 作为「深度档案」新站失去独立收录机会，新站差异化内容（五段、landed cost 明细、/compare、/technology）无法建立自己的排名资产；若 .top 定位是「新版主站」则方向相反；域名切换前反复横跳会浪费已积累的 .top 信号。

**适用**：.top 仅作为 .net 的临时占位/镜像，不打算独立运营。

### 方案 B：`.top` 保持独立 + 差异化内容路线（推荐）

**做法**：不跨域 canonical，两站各自独立；.top 持续深化**独有**内容（深度五段档案、landed-cost 明细、/compare、/technology 实体页、/data 端点），形成与 .net 的可区分信号面；.net 作为「目录/基底」逐步退化为索引入口或只保留品牌/市场页。

**利**：符合 .top 已投入的差异化建设方向（517 深度档案 + 去模板化 + 五段结构正是为此）；长期看两站内容面拉开后重复判定自然下降；无一次性大改动风险。

**弊**：短期（数月）两站 517 页仍高度相似，重复风险持续；需要持续内容投入才见效；需人工监控 Search Console 重复报告。

**适用**：.top 是长期主站/深度站定位（当前总纲方向）。

### 方案 C：`.pages.dev` 加 noindex 待域名切换

**做法**：给 Cloudflare Pages 默认域（`.pages.dev`）加 `X-Robots-Tag: noindex`（经 `_headers` 或 Pages 规则），待 `.top` 自定义域完全接管后移除；`.top`/`.net` 之间的 canonical 关系另走 A 或 B。

**利**：消除第三方副本（.pages.dev）的索引污染，**独立于 A/B 决策、可先做**；风险极低（不影响 .top/.net 主域）；纯增量。

**弊**：不解决 .top vs .net 的重复本身（只解决 .pages.dev 副本）；若未来要换域名到别的 pages 项目需重新配置。

**适用**：任何情况下都应执行（.pages.dev 副本本就不该进索引）。

## 3. 建议

**分两步走，低风险先行**：

1. **先执行方案 C**（可立即、独立、零风险）：`.pages.dev` 默认域加 `X-Robots-Tag: noindex`。这是纯治理副本，无需在 A/B 间取舍。
2. **再在 A / B 间二选一**（需用户决策）：
   - 若 .top 定位是**新版主站/深度站**（当前总纲方向）→ **选 B**，保持独立、继续差异化，用内容拉开与 .net 的重复面。
   - 若 .top 只是 .net 的**临时占位** → **选 A**，.top 全面 canonical 指向 .net，把信号让给源站。

**当前证据倾向 B**：.top 已投入 517 深度档案、五段结构、去模板化、landed-cost 明细、/compare、/technology、/data 端点——这些是 .net 没有的差异化资产，说明 .top 是长期独立运营的深度站，而非镜像。故 .top 保持独立 + 持续差异化（B）比「把信号让回 .net」（A）更符合已建成的方向。

## 4. 各方案执行步骤（待批准）

### 方案 C 执行步骤（.pages.dev noindex）
1. 确认 Cloudflare Pages 项目默认域名（`.pages.dev`）确切名称。
2. 在 `public/_headers` 或 Cloudflare Pages 侧加规则：对 `.pages.dev` 请求返回 `X-Robots-Tag: noindex`（`_headers` 可用 `https://<project>.pages.dev/*` 路径限定，或 Pages 控制台 Response Header 规则按 host 匹配）。
3. 部署后 `curl -I https://<project>.pages.dev/vehicles/byd-seal/` 确认 `X-Robots-Tag: noindex` 返回。
4. Search Console 提交 .pages.dev 域名验证，观察索引下降。

### 方案 A 执行步骤（.top → .net canonical）
1. `src/components/common/SEO.astro` 的 `canonicalURL` 改为按环境/域名映射到 .net 同路径（或引入 `CROSS_DOMAIN_CANONICAL` 开关）。
2. `og:url` / JSON-LD `url` / `@id` 同步指向 .net。
3. build 全量抽查 canonical 指向正确、无自指残留。
4. 观察 Search Console 覆盖报告，.top 逐步退出索引、.net 承载。

### 方案 B 执行步骤（独立 + 差异化）
1. 保持现状 canonical（各自自指）。
2. 继续差异化内容批：深度档案补全 31 款 C 层缺失字段、B 层 53 款去模板化、/compare 与 /technology 实体页扩写。
3. 定期 Search Console 对比两站重复报告，跟踪差异化对重复判定的降低效果。

## 5. 待用户决策

- 是否先执行 **方案 C**（.pages.dev noindex）？
- .top 定位是「新版主站/深度站」→ **方案 B**，还是「.net 临时占位」→ **方案 A**？
