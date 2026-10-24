#!/usr/bin/env node
/**
 * China EV Mart indexation quality gate (P2 §21).
 * Run: npm run quality:gate
 * Checks 5 gates per vehicle: identity / brand / powertrain / specs / source.
 * Produces docs/indexation-quality-gate.md (report only — does NOT noindex anything).
 */
import { readFileSync, readdirSync, writeFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const ROOT = new URL('..', import.meta.url).pathname;
const SITE = 'https://chinaevmart.com';
const load = (p) => JSON.parse(readFileSync(join(ROOT, p), 'utf8'));

const ALLOWED_POWERTRAINS = new Set(['BEV','PHEV','EREV','HEV','ICE','FCEV','Unknown']);
const ALLOWED_BODY_TYPES = new Set([
  'Sedan','Hatchback','SUV','Crossover','MPV','Wagon','Pickup','Van',
  'Coupe','Convertible','Sports Car','Other','Unknown',
]);

const vehicles = load('src/data/vehicle-master.json').vehicles;
const brands = load('src/data/brand-master.json').brands;
const brandMap = new Map(brands.map((b) => [b.brand_id, b]));
const mdDir = join(ROOT, 'src/content/vehicles');
const brandMdDir = join(ROOT, 'src/content/brands');

const gateNames = ['identity', 'brand', 'powertrain', 'specs', 'source'];
const results = { identity: 0, brand: 0, powertrain: 0, specs: 0, source: 0 };
const incomplete = [];
const suggestions = new Map();

for (const v of vehicles) {
  const id = v.vehicle_id;
  const url = `${SITE}/vehicles/${id}/`;
  const problems = [];
  let raw = null;
  const mdPath = join(mdDir, id + '.md');
  if (existsSync(mdPath)) raw = readFileSync(mdPath, 'utf8');
  const fm = raw ? (raw.match(/^---\n([\s\S]*?)\n---/)?.[1] ?? '') : '';
  const fmField = (name) => fm.match(new RegExp(`^${name}:\\s*["\u201d]?([^"\\n]*)`,'m'))?.[1] ?? null;

  // 1. identity gate
  if (!v.vehicle_id || !v.model) {
    problems.push('identity: vehicle_id/model 缺失');
  } else if (!raw) {
    problems.push('identity: md 文件不存在（缺页面）');
    suggestions.set('identity', '缺失 md 的车辆无法生成页面，需补写 md 或从 master 删除');
  } else {
    const slug = fmField('slug');
    const title = fmField('title');
    if (!slug || slug !== id) problems.push('identity: md slug 与 vehicle_id 不一致');
    if (!title) problems.push('identity: md title 缺失');
    if (!fm.includes('publishedDate')) problems.push('identity: md publishedDate 缺失');
  }

  // 2. brand gate
  const b = brandMap.get(v.brand);
  if (!b) {
    problems.push('brand: brand 不在 brand-master');
  } else {
    if (!existsSync(join(brandMdDir, v.brand + '.md'))) {
      problems.push('brand: 品牌页 md 不存在（面包屑/品牌墙会断链）');
      suggestions.set('brand', `为缺失品牌页的品牌创建 src/content/brands/{brand}.md`);
    }
  }

  // 3. powertrain gate
  if (!ALLOWED_POWERTRAINS.has(v.powertrain)) {
    problems.push(`powertrain: 非法值 ${v.powertrain}`);
  } else if (v.powertrain === 'Unknown') {
    problems.push('powertrain: Unknown（无法索引分类）');
    suggestions.set('powertrain', 'Unknown powertrain 车辆标注需人工查证（如 Hongqi Guoya）');
  }

  // 4. specs gate
  const specIssues = [];
  if (typeof v.price_usd !== 'number' || v.price_usd <= 0) specIssues.push('price_usd 无效');
  if (v.range_cltc_km == null && v.range_long_km == null) specIssues.push('range 全空');
  if (v.battery_kwh == null) specIssues.push('battery_kwh 空');
  if (!ALLOWED_BODY_TYPES.has(v.body_type)) specIssues.push(`body_type 非法 ${v.body_type}`);
  if (v.motor_power_kw == null) specIssues.push('motor_power_kw 空');
  if (specIssues.length) {
    problems.push(`specs: ${specIssues.join('; ')}`);
    if (specIssues.some((s) => s.startsWith('range'))) suggestions.set('specs', 'range 全空的车辆建议补充 CLTC/WLTP 数据或标注 Unknown');
  }

  // 5. source gate
  const srcIssues = [];
  if (!v.source) srcIssues.push('master source 空');
  if (!/^https?:\/\//.test(v.source_url || '')) srcIssues.push('master source_url 空/非法');
  if (raw && !fm.includes('data_source')) srcIssues.push('md data_source 空');
  if (srcIssues.length) {
    problems.push(`source: ${srcIssues.join('; ')}`);
    suggestions.set('source', 'source 继承自品牌级来源；如需逐车官网规格页 url 需人工补充');
  }

  for (const g of gateNames) if (!problems.some((p) => p.startsWith(g))) results[g]++;
  if (problems.length) {
    incomplete.push({ id, url, brand: v.brand, problems });
  }
}

// ── 6. P2 pre-publish checks (⑤ conflict / ⑥ canonical / ⑦ structured data) ──
const p2 = { conflictUnresolved: 0, conflictDocumented: 0, canonicalBad: 0, ldForbidden: 0 };
const p2ConflictList = [];
const p2CanonicalList = [];
const p2LdList = [];

// ⑤ conflict interception (parameter-verification.json `conflict` status)
{
  const pv = load('src/data/parameter-verification.json');
  for (const [slug, cells] of Object.entries(pv.vehicles ?? {})) {
    for (const [param, c] of Object.entries(cells)) {
      if (c?.status !== 'conflict') continue;
      const documented = !!c.note && c.note.trim().length > 0;
      if (documented) p2.conflictDocumented++;
      else { p2.conflictUnresolved++; p2ConflictList.push(`${slug}.${param}`); }
    }
  }
}

// ⑥ canonical domain
{
  const SITE = 'https://chinaevmart.com';
  const siteTs = existsSync(join(ROOT, 'src/config/site.ts'))
    ? readFileSync(join(ROOT, 'src/config/site.ts'), 'utf8')
    : '';
  const astroCfg = existsSync(join(ROOT, 'astro.config.mjs'))
    ? readFileSync(join(ROOT, 'astro.config.mjs'), 'utf8')
    : '';
  const env = existsSync(join(ROOT, '.env.example'))
    ? readFileSync(join(ROOT, '.env.example'), 'utf8')
    : '';
  const grab = (src, re) => { const m = src.match(re); return m ? m[1] : null; };
  const checks = [
    ['.env.example SITE_URL', grab(env, /SITE_URL\s*=\s*(\S+)/)],
    ['site.ts url fallback', grab(siteTs, /url\s*=\s*import\.meta\.env\.SITE_URL\s*\|\|\s*'([^']+)'/)],
    ['site.ts company.url', grab(siteTs, /url:\s*'([^']+)',\s*\n\s*logo/s)],
    ['astro.config siteUrl fallback', grab(astroCfg, /siteUrl\s*=\s*process\.env\.SITE_URL\s*\|\|\s*'([^']+)'/)],
  ];
  for (const [label, v] of checks) {
    if (!v) { p2.canonicalBad++; p2CanonicalList.push(`${label} not found`); }
    else if (v !== SITE) { p2.canonicalBad++; p2CanonicalList.push(`${label}=${v}`); }
  }
}

// ⑦ structured data — no fabricated fields
{
  const LD_FORBIDDEN = ['rating', 'review', 'aggregateRating', 'award', 'sku', 'mpn', 'gtin', 'productID'];
  for (const rel of ['src/components/common/SEO.astro', 'src/pages/vehicles/[slug].astro']) {
    const p = join(ROOT, rel);
    if (!existsSync(p)) continue;
    const src = readFileSync(p, 'utf8');
    for (const key of LD_FORBIDDEN) {
      if (new RegExp(`\\b${key}\\s*:`).test(src)) {
        p2.ldForbidden++;
        p2LdList.push(`${rel}: ${key}`);
      }
    }
  }
}

// ── 报告输出 ──
const today = new Date().toISOString().split('T')[0];
const lines = [];
lines.push('# China EV Mart Indexation Quality Gate');
lines.push('');
lines.push(`> 生成：${today} ｜ 车辆总数：${vehicles.length} ｜ 工具：scripts/quality-gate.mjs（\`npm run quality:gate\`）`);
lines.push('> 本报告仅产出不完整清单，**不自动 noindex**（无既有政策支持）。');
lines.push('');
lines.push('## 五门槛通过率');
lines.push('');
lines.push('| Gate | 通过 | 未通过 | 说明 |');
lines.push('|---|---|---|---|');
for (const g of gateNames) {
  const desc = {
    identity: 'vehicle_id/model/slug/title/publishedDate 完整',
    brand: 'brand 在 brand-master 且品牌页存在',
    powertrain: '受控词表内且非 Unknown',
    specs: 'price/range/battery/body_type/motor_power 有效',
    source: 'master source/source_url + md data_source 存在',
  }[g];
  lines.push(`| ${g} | ${results[g]} | ${vehicles.length - results[g]} | ${desc} |`);
}
lines.push('');
lines.push(`## 不完整记录清单（${incomplete.length} 台）`);
lines.push('');
if (incomplete.length === 0) {
  lines.push('✅ 全部通过五门槛。');
} else {
  for (const r of incomplete) {
    lines.push(`- [${r.id}](${r.url}) (${r.brand})`);
    for (const p of r.problems) lines.push(`  - ${p}`);
  }
}
lines.push('');
lines.push('## 建议（非阻塞）');
lines.push('');
if (suggestions.size === 0) {
  lines.push('- 无。');
} else {
  for (const [k, v] of suggestions) lines.push(`- **${k}**: ${v}`);
}

// ── P2 pre-publish checks section ──
lines.push('');
lines.push('## P2 发布前检查（⑤ conflict / ⑥ canonical / ⑦ structured data）');
lines.push('');
lines.push(`- ⑤ conflict 未解决（无 note）：**${p2.conflictUnresolved}**`);
lines.push(`- ⑤ conflict 已标注（有 note，仍待人工）：**${p2.conflictDocumented}**`);
lines.push(`- ⑥ canonical 域异常：**${p2.canonicalBad}**`);
lines.push(`- ⑦ JSON-LD 虚构字段：**${p2.ldForbidden}**`);
if (p2ConflictList.length) lines.push(`- conflict 未解决项：${p2ConflictList.join('、')}`);
if (p2CanonicalList.length) lines.push(`- canonical 异常：${p2CanonicalList.join('、')}`);
if (p2LdList.length) lines.push(`- 虚构字段：${p2LdList.join('、')}`);
writeFileSync(join(ROOT, 'docs/indexation-quality-gate.md'), lines.join('\n') + '\n');

console.log(`=== Quality Gate ===`);
for (const g of gateNames) console.log(`  ${g}: ${results[g]}/${vehicles.length} pass`);
console.log(`  incomplete records: ${incomplete.length}`);
console.log(`  P2: conflict-unresolved=${p2.conflictUnresolved} conflict-documented=${p2.conflictDocumented} canonical-bad=${p2.canonicalBad} ld-forbidden=${p2.ldForbidden}`);
console.log(`→ docs/indexation-quality-gate.md written`);
