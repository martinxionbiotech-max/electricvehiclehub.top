#!/usr/bin/env node
/**
 * China EV Mart — pre-publish quality gate (P2 收官批).
 * Run: npm run gate
 *
 * The content frontmatter (.md) is the single source of truth. This gate reads
 * frontmatter directly (never the stale `src/data/*-master.json` snapshots) plus
 * `src/data/parameter-verification.json` for conflict interception.
 *
 * Seven pre-publish checks + a high-risk-field manual-review gate:
 *   ① trim / version consistency
 *   ② parameter unit enum (kg / kWh / mm / kW / Nm …)
 *   ③ test-standard labels (CLTC / WLTP / EPA / NEDC)
 *   ④ source + price-date presence (data_source / data_updated)
 *   ⑤ conflict interception (parameter-verification.json `conflict` → 待人工)
 *   ⑥ canonical domain (https://chinaevmart.com)
 *   ⑦ structured-data (JSON-LD) — no fabricated fields
 *
 * Unknown / unverified values are NEVER auto-filled: a high-risk field that
 * carries a value without source + date + verification status is blocked.
 *
 * Exit code: 0 = gate passed; 1 = blocking issues (resolve or explicitly mark
 * them "known / pending manual review" before publishing).
 */
import { readFileSync, readdirSync, writeFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const ROOT = new URL('..', import.meta.url).pathname;
const VEH_DIR = join(ROOT, 'src/content/vehicles');
const SITE = 'https://chinaevmart.com';

// ── registries ─────────────────────────────────────────────────────────────
/** Field name → canonical unit. Any numeric field outside this registry is a typo. */
const UNIT_REGISTRY = {
  price_usd: 'USD', fob_price_usd_min: 'USD', fob_price_usd_max: 'USD',
  battery_kwh: 'kWh', range_cltc_km: 'km', range_wltp_km: 'km', range_epa_km: 'km',
  range_nedc_km: 'km', range_long_km: 'km', motor_power_kw: 'kW', total_power_kw: 'kW',
  torque_nm: 'Nm', accel_0_100_s: 's', top_speed_kmh: 'km/h', length_mm: 'mm',
  width_mm: 'mm', height_mm: 'mm', wheelbase_mm: 'mm', weight_kg: 'kg',
  gross_weight_kg: 'kg', ground_clearance_mm: 'mm', trunk_l: 'L',
  efficiency_kwh_100km: 'kWh/100km', drag_coefficient: '(dimensionless)',
};

/** Fields that directly affect a procurement decision → require manual review. */
const HIGH_RISK = {
  price_usd: 'Price', price_type: 'Price', currency: 'Price',
  range_cltc_km: 'Range', range_wltp_km: 'Range', range_epa_km: 'Range',
  range_nedc_km: 'Range', range_long_km: 'Range',
  certification_notes: 'Certification', hs_code: 'HS Code',
};

const TEST_STANDARDS = new Set(['CLTC', 'WLTP', 'EPA', 'NEDC']);
const POWERTRAINS = new Set(['BEV', 'PHEV', 'EREV', 'HEV', 'ICE', 'FCEV', 'Unknown']);
// Chinese-only trim keywords (unambiguous; avoids 'ev'/'hev' substring traps).
const PT_KW_CN = { BEV: ['纯电'], EREV: ['增程'], PHEV: ['插混', '插电'], HEV: ['油混', '非插电'] };
// Range field → the test standard it implies.
const RANGE_FIELD_STD = {
  range_cltc_km: 'CLTC', range_wltp_km: 'WLTP', range_epa_km: 'EPA', range_nedc_km: 'NEDC',
};

// ── structured-data (JSON-LD) allowlist ────────────────────────────────────
const LD_TYPES = new Set([
  'WebSite', 'Organization', 'BreadcrumbList', 'ListItem', 'Article', 'Vehicle',
  'Brand', 'EngineSpecification', 'QuantitativeValue', 'Offer', 'Person',
  'PostalAddress', 'ContactPoint', 'ImageObject', 'WebPage',
]);
// Schema.org keys that would be a FABRICATION on a B2B reference/quotation site.
const LD_FORBIDDEN = ['rating', 'review', 'aggregateRating', 'award', 'sku', 'mpn', 'gtin', 'productID'];

// ── helpers ────────────────────────────────────────────────────────────────
const issues = []; // { check, severity: 'block'|'warn', id, message }
const block = (check, id, msg) => issues.push({ check, severity: 'block', id, message: msg });
const warn = (check, id, msg) => issues.push({ check, severity: 'warn', id, message: msg });

function parseFrontmatter(raw) {
  const m = raw.match(/^---\n([\s\S]*?)\n---/);
  if (!m) return null;
  const fm = {};
  for (const line of m[1].split('\n')) {
    const mm = line.match(/^([A-Za-z0-9_]+):\s*(.*)$/);
    if (mm) fm[mm[1]] = mm[2];
  }
  return fm;
}
const str = (fm, k) => (fm[k] != null ? fm[k].replace(/^"|"$/g, '').trim() : undefined);
const has = (fm, k) => fm[k] != null && fm[k] !== '' && fm[k] !== 'null' && fm[k] !== '""';
const num = (fm, k) => {
  const v = fm[k];
  if (v == null || v === '' || v === 'null') return null;
  const n = Number(v.replace(/^"|"$/g, ''));
  return Number.isFinite(n) ? n : null;
};
const isDate = (s) => /^\d{4}-\d{2}-\d{2}$/.test(s ?? '');
const loadJson = (p) => JSON.parse(readFileSync(join(ROOT, p), 'utf8'));

// ── load data ──────────────────────────────────────────────────────────────
const vehFiles = readdirSync(VEH_DIR).filter((f) => f.endsWith('.md'));
const records = vehFiles.map((f) => {
  const raw = readFileSync(join(VEH_DIR, f), 'utf8');
  return { slug: f.replace(/\.md$/, ''), fm: parseFrontmatter(raw) };
});

const paramVerification = loadJson('src/data/parameter-verification.json');
const conflictCells = [];
for (const [slug, cells] of Object.entries(paramVerification.vehicles ?? {})) {
  for (const [param, c] of Object.entries(cells)) {
    if (c && c.status === 'conflict') conflictCells.push({ slug, param, cell: c });
  }
}

const today = new Date().toISOString().split('T')[0];

// ── ① trim / version consistency ───────────────────────────────────────────
let trimNoYear = 0;
let trimPowertrainMismatch = 0;
for (const { slug, fm } of records) {
  if (!fm) continue;
  const trim = str(fm, 'trim');
  const pt = str(fm, 'powertrain');
  if (trim && num(fm, 'model_year') == null) {
    trimNoYear++;
    warn('① trim/version', slug, `trim present but model_year missing (version unpinned)`);
  }
  if (trim && pt && POWERTRAINS.has(pt)) {
    const tl = trim.toLowerCase();
    for (const [other, kws] of Object.entries(PT_KW_CN)) {
      if (other === pt) continue;
      if (kws.some((k) => tl.includes(k))) {
        trimPowertrainMismatch++;
        block('① trim/version', slug, `trim "${trim.slice(0, 40)}" spans powertrain ${other} but field powertrain=${pt}`);
        break;
      }
    }
  }
}

// ── ② unit enum ────────────────────────────────────────────────────────────
let unitBad = 0;
for (const { slug, fm } of records) {
  if (!fm) continue;
  for (const line of Object.keys(fm)) {
    if (!(line in UNIT_REGISTRY)) continue;
    const rawVal = fm[line].trim();
    if (rawVal === '' || rawVal === 'null') continue;
    if (!/^-?\d+(\.\d+)?$/.test(rawVal.replace(/^"|"$/g, ''))) {
      unitBad++;
      block('② unit enum', slug, `${line}=${rawVal.slice(0, 24)} is not a bare number (unit must live in field name)`);
    }
  }
}
// Detect unknown numeric-looking fields (typo'd unit-bearing field name).
const numericKeyRe = /^(price|battery|range|motor|total_power|torque|accel|top_speed|length|width|height|wheelbase|weight|gross_weight|ground_clearance|trunk|efficiency|fob_price|drag|model_year)/;
let unknownUnitFields = 0;
for (const { slug, fm } of records) {
  if (!fm) continue;
  for (const k of Object.keys(fm)) {
    if (k in UNIT_REGISTRY) continue;
    if (!numericKeyRe.test(k)) continue;
    if (['model_year', 'data_tier', 'model_count', 'vehicle_count', 'established'].includes(k)) continue;
    const rawVal = fm[k].trim();
    if (rawVal !== '' && rawVal !== 'null' && /^-?\d+(\.\d+)?$/.test(rawVal.replace(/^"|"$/g, ''))) {
      unknownUnitFields++;
      warn('② unit enum', slug, `numeric field "${k}" not in unit registry (verify unit)`);
    }
  }
}

// ── ③ test-standard labels ─────────────────────────────────────────────────
let rangeAmbiguous = 0;
for (const { slug, fm } of records) {
  if (!fm) continue;
  const stdFields = ['range_cltc_km', 'range_wltp_km', 'range_epa_km', 'range_nedc_km'].filter((k) => has(fm, k));
  const hasLong = has(fm, 'range_long_km');
  if (hasLong && stdFields.length === 0) {
    rangeAmbiguous++;
    block('③ test standard', slug, 'range_long_km present with no CLTC/WLTP/EPA/NEDC field — standard ambiguous');
  }
}
// param_verification.test_standard must be a known standard.
let paramStdBad = 0;
for (const [slug, cells] of Object.entries(paramVerification.vehicles ?? {})) {
  for (const [param, c] of Object.entries(cells)) {
    if (c?.test_standard && !TEST_STANDARDS.has(c.test_standard)) {
      paramStdBad++;
      block('③ test standard', `${slug}.${param}`, `test_standard=${c.test_standard} not in CLTC/WLTP/EPA/NEDC`);
    }
  }
}

// ── ④ source + price-date presence ─────────────────────────────────────────
let srcMissing = 0;
let dateMissing = 0;
let dateBad = 0;
let dateFuture = 0;
for (const { slug, fm } of records) {
  if (!fm) continue;
  const ds = str(fm, 'data_source');
  if (!ds) { srcMissing++; block('④ source/date', slug, 'data_source missing'); }
  const du = str(fm, 'data_updated');
  if (!du) { dateMissing++; block('④ source/date', slug, 'data_updated missing (price has no date basis)'); }
  else if (!isDate(du)) { dateBad++; block('④ source/date', slug, `data_updated=${du} not YYYY-MM-DD`); }
  else if (du > today) { dateFuture++; block('④ source/date', slug, `data_updated=${du} is a future date`); }
}

// ── ⑤ conflict interception ────────────────────────────────────────────────
// Every `conflict` cell is a publish blocker unless explicitly resolved
// (status changed) or documented (note present + still marked pending).
const conflictResolved = conflictCells.filter((c) => c.cell.note && c.cell.note.trim());
const conflictUnresolved = conflictCells.filter((c) => !c.cell.note || !c.cell.note.trim());
for (const c of conflictUnresolved) {
  block('⑤ conflict', c.slug, `param ${c.param}: conflict with no note — must be manually resolved or documented before publish`);
}
for (const c of conflictResolved) {
  warn('⑤ conflict', c.slug, `param ${c.param}: conflict documented (note present) — still pending manual resolution`);
}

// ── ⑥ canonical domain ─────────────────────────────────────────────────────
const canonicalChecks = [];
{
  const envExample = existsSync(join(ROOT, '.env.example'))
    ? readFileSync(join(ROOT, '.env.example'), 'utf8')
    : '';
  const siteTs = readFileSync(join(ROOT, 'src/config/site.ts'), 'utf8');
  const astroCfg = readFileSync(join(ROOT, 'astro.config.mjs'), 'utf8');
  const extract = (src, re) => {
    const m = src.match(re);
    return m ? m[1] : null;
  };
  const envUrl = extract(envExample, /SITE_URL\s*=\s*(\S+)/);
  const siteFallback = extract(siteTs, /url\s*=\s*import\.meta\.env\.SITE_URL\s*\|\|\s*'([^']+)'/);
  const companyUrl = extract(siteTs, /url:\s*'([^']+)',\s*\n\s*logo/s);
  const astroSite = extract(astroCfg, /siteUrl\s*=\s*process\.env\.SITE_URL\s*\|\|\s*'([^']+)'/);

  const isCanonical = (label, v) => {
    if (!v) { block('⑥ canonical', label, 'canonical URL not found'); return; }
    if (v !== SITE) block('⑥ canonical', label, `expected ${SITE}, got ${v}`);
    else canonicalChecks.push(`${label}=${v}`);
  };
  isCanonical('.env.example SITE_URL', envUrl);
  isCanonical('site.ts url fallback', siteFallback);
  isCanonical('site.ts company.url', companyUrl);
  isCanonical('astro.config siteUrl fallback', astroSite);
  // The sister site electricvehiclehub.net must only appear as an outbound link,
  // never as a canonical URL (already enforced by the exact-match above).
}

// ── ⑦ structured-data (JSON-LD) — no fabricated fields ─────────────────────
const ldSourceFiles = ['src/components/common/SEO.astro', 'src/pages/vehicles/[slug].astro'];
let ldForbiddenHits = 0;
let ldUnknownTypes = 0;
for (const rel of ldSourceFiles) {
  const p = join(ROOT, rel);
  if (!existsSync(p)) continue;
  const src = readFileSync(p, 'utf8');
  for (const key of LD_FORBIDDEN) {
    if (new RegExp(`\\b${key}\\s*:`).test(src)) {
      ldForbiddenHits++;
      block('⑦ structured data', rel, `forbidden JSON-LD key "${key}" (would fabricate rating/review/award/identifier)`);
    }
  }
  for (const m of src.matchAll(/'@type':\s*'([^']+)'/g)) {
    if (!LD_TYPES.has(m[1])) {
      ldUnknownTypes++;
      warn('⑦ structured data', rel, `unregistered @type "${m[1]}"`);
    }
  }
}

// ── ⑧ high-risk manual-review gate (no AI auto-fill) ───────────────────────
let highRiskUnverified = 0;
let highRiskNoSource = 0;
for (const { slug, fm } of records) {
  if (!fm) continue;
  for (const [field, label] of Object.entries(HIGH_RISK)) {
    if (!has(fm, field)) continue; // absent → renders N/A, nothing fabricated
    const ds = str(fm, 'data_source');
    const du = str(fm, 'data_updated');
    const vs = str(fm, 'verification_status');
    if (!ds || !du) {
      highRiskNoSource++;
      block('⑧ high-risk', `${slug}.${field}`, `${label} value present without data_source/data_updated (unverified value would be silently asserted)`);
      continue;
    }
    if (vs === 'unverifiable' || vs === 'partial') {
      highRiskUnverified++;
      warn('⑧ high-risk', `${slug}.${field}`, `${label} marked ${vs} — 待核验 (pending manual review)`);
    }
  }
}

// ── baseline tally ─────────────────────────────────────────────────────────
const blockingIds = new Set(issues.filter((i) => i.severity === 'block').map((i) => i.id));
const warnIds = new Set(issues.filter((i) => i.severity === 'warn').map((i) => i.id));
// A vehicle PASSes only if it has zero blocking issues (warn-only still passes,
// but is counted separately for the manual-review queue).
const passCount = records.filter((r) => r.fm && !blockingIds.has(r.slug)).length;
const blockCount = records.filter((r) => r.fm && blockingIds.has(r.slug)).length;
const warnCount = records.filter((r) => r.fm && !blockingIds.has(r.slug) && warnIds.has(r.slug)).length;
const cleanCount = records.filter((r) => r.fm && !blockingIds.has(r.slug) && !warnIds.has(r.slug)).length;
const blockTotal = issues.filter((i) => i.severity === 'block').length;
const warnTotal = issues.filter((i) => i.severity === 'warn').length;

// ── checklist output ───────────────────────────────────────────────────────
const lines = [];
lines.push('# China EV Mart — 发布前检查单 (Pre-publish Checklist)');
lines.push('');
lines.push(`> 生成：${today} ｜ 工具：\`npm run gate\`（scripts/pre-publish-gate.mjs）`);
lines.push('> 单一真源：`src/content/vehicles/*.md` frontmatter（**不读** 陈旧的 `src/data/*-master.json`）。');
lines.push('> 纪律：未知/未核验数值**一律 N/A 或 待核验**，绝不静默填充。');
lines.push('');
lines.push('## 检查项');
lines.push('');
lines.push('| # | 检查 | 判定 |');
lines.push('|---|---|---|');
lines.push('| ① | 车型版本/trim 一致性 | trim 有值必须可定位年款；trim 不得横跨与 powertrain 字段矛盾的动力形式 |');
lines.push('| ② | 参数单位规范 | 数值字段必须为裸数字，单位由字段名承载（kg/kWh/mm/kW/Nm 枚举）；未知数值字段告警 |');
lines.push('| ③ | 测试标准标注 | 续航值必须归属 CLTC/WLTP/EPA/NEDC；range_long_km 无标准字段 = 阻断 |');
lines.push('| ④ | 来源与价格日期 | data_source + data_updated 必填；data_updated 须 YYYY-MM-DD 且非未来 |');
lines.push('| ⑤ | conflict 拦截 | parameter-verification.json 的 conflict 必须人工处理或带 note 明确标注 |');
lines.push('| ⑥ | canonical 域 | 四处 canonical 来源统一为 https://chinaevmart.com |');
lines.push('| ⑦ | 结构化数据 | JSON-LD 无虚构字段（rating/review/award/sku 等一律禁止） |');
lines.push('| ⑧ | 高风险字段人工审核 | 价格/续航/认证/HS Code：有值必须带来源+日期+核验状态；否则 N/A |');
lines.push('');
lines.push('## 基线结果');
lines.push('');
lines.push(`- 车型总数：**${records.length}**`);
lines.push(`- PASS（零阻断）：**${passCount}**`);
lines.push(`- BLOCK（≥1 阻断）：**${blockCount}**`);
lines.push(`- 仅 WARN（可发布但待复核）：**${warnCount}**`);
lines.push(`- 完全 clean：**${cleanCount}**`);
lines.push(`- 阻断项合计：**${blockTotal}** ｜ 告警项合计：**${warnTotal}**`);
lines.push('');
lines.push('## 待人工清单（conflict + 高风险未核验）');
lines.push('');
lines.push(`- conflict 单元：**${conflictCells.length}**（已带 note ${conflictResolved.length} / 未带 note ${conflictUnresolved.length}）`);
lines.push(`- 高风险字段未核验（unverifiable/partial）：**${highRiskUnverified}**`);
lines.push(`- 高风险字段缺来源/日期：**${highRiskNoSource}**`);
lines.push('');
if (issues.length === 0) {
  lines.push('✅ 全部检查通过，可发布。');
} else {
  const bySev = (sev) => issues.filter((i) => i.severity === sev);
  for (const [label, sev] of [['阻断 (block)', 'block'], ['告警 (warn)', 'warn']]) {
    const list = bySev(sev);
    lines.push(`## ${label}（${list.length}）`);
    lines.push('');
    for (const i of list.slice(0, 200)) lines.push(`- [${i.check}] **${i.id}**: ${i.message}`);
    if (list.length > 200) lines.push(`- … 及另外 ${list.length - 200} 项`);
    lines.push('');
  }
}

writeFileSync(join(ROOT, 'docs/pre-publish-checklist.md'), lines.join('\n') + '\n');

// ── console summary ────────────────────────────────────────────────────────
console.log('=== China EV Mart Pre-publish Gate (P2) ===');
console.log(`vehicles: ${records.length}`);
console.log(`PASS: ${passCount} | BLOCK: ${blockCount} | warn-only: ${warnCount} | clean: ${cleanCount}`);
console.log(`blocking issues: ${blockTotal} | warnings: ${warnTotal}`);
console.log(`待人工: conflict=${conflictCells.length} (unresolved=${conflictUnresolved.length}) high-risk-unverified=${highRiskUnverified} high-risk-no-source=${highRiskNoSource}`);
console.log(`→ docs/pre-publish-checklist.md written`);
if (blockTotal > 0) {
  console.log('\n❌ GATE FAILED — resolve blocking issues or mark them "known / pending manual review".');
  process.exit(1);
}
console.log('\n✅ GATE PASSED');
process.exit(0);
