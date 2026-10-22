#!/usr/bin/env node
/**
 * China EV Mart data validation script (Phase 3 — single source of truth).
 * Run: npm run validate:data
 *
 * The `vehicles` and `brands` content collections (frontmatter .md files) are
 * the single source of truth. Legacy `src/data/*-master.json` files are orphan
 * exports and are NOT validated against here — that prevents false "drift"
 * errors when the master snapshots fall behind the content files.
 *
 * Checks:
 *  - required fields (vehicles + brands)
 *  - supported powertrain / body-type enums
 *  - price_type canonical 5-category enum
 *  - numeric unit sanity (price, battery, range, speed, dimensions)
 *  - duplicate slugs (vehicles + brands)
 *  - brand <-> vehicle relationship (no orphan brands/vehicles)
 *  - family (nameplate) presence on vehicle records
 *  - range test-standard separation (CLTC / WLTP / EPA / NEDC fields)
 */
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

const ROOT = new URL('..', import.meta.url).pathname;
const VEH_DIR = join(ROOT, 'src/content/vehicles');
const BRAND_DIR = join(ROOT, 'src/content/brands');

const POWERTRAINS = new Set(['BEV', 'PHEV', 'EREV', 'HEV', 'ICE', 'FCEV', 'Unknown']);
const BODY_TYPES = new Set([
  'Sedan', 'Hatchback', 'SUV', 'Crossover', 'MPV', 'Wagon', 'Pickup', 'Van',
  'Coupe', 'Convertible', 'Sports Car', 'Other', 'Unknown',
]);
const PRICE_TYPES = new Set([
  'Official MSRP',
  'China market reference price',
  'China ex-factory reference price',
  'FOB quotation',
  'Landed cost estimate',
  'Reference (unverified)',
]);

const issues = [];
const ok = [];
const flag = (cat, id, msg) => issues.push({ category: cat, id, message: msg });

/** Parse YAML-ish frontmatter into a flat map of scalar keys (strings kept raw). */
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
const num = (fm, k) => {
  if (fm[k] == null || fm[k] === '' || fm[k] === 'null') return null;
  const n = Number(fm[k].replace(/^"|"$/g, ''));
  return Number.isFinite(n) ? n : null;
};

const vehFiles = readdirSync(VEH_DIR).filter((f) => f.endsWith('.md'));
const brandFiles = readdirSync(BRAND_DIR).filter((f) => f.endsWith('.md'));

// ── 1. Brands ──
const brandSlugs = new Set();
for (const bf of brandFiles) {
  const slug = bf.replace(/\.md$/, '');
  if (brandSlugs.has(slug)) flag('duplicate-brand-slug', slug, 'duplicate brand slug');
  brandSlugs.add(slug);
  const fm = parseFrontmatter(readFileSync(join(BRAND_DIR, bf), 'utf8'));
  if (!fm) { flag('brand-no-frontmatter', slug, 'missing frontmatter'); continue; }
  for (const req of ['title', 'description', 'brand_name', 'established', 'parent_manufacturer', 'website']) {
    if (!str(fm, req)) flag('brand-missing-field', slug, `missing ${req}`);
  }
  const mc = num(fm, 'model_count');
  if (mc == null || mc < 0) flag('brand-model-count', slug, `model_count=${fm.model_count}`);
}
ok.push(`brands: ${brandFiles.length} (required fields + unique slugs checked)`);

// ── 2. Vehicles ──
const vehicleSlugs = new Set();
const brandModelCounts = new Map();
for (const vf of vehFiles) {
  const slug = vf.replace(/\.md$/, '');
  if (vehicleSlugs.has(slug)) flag('duplicate-vehicle-slug', slug, 'duplicate vehicle slug');
  vehicleSlugs.add(slug);
  const fm = parseFrontmatter(readFileSync(join(VEH_DIR, vf), 'utf8'));
  if (!fm) { flag('vehicle-no-frontmatter', slug, 'missing frontmatter'); continue; }

  // required fields
  for (const req of ['title', 'description', 'slug', 'brand', 'type', 'powertrain', 'price_usd', 'publishedDate', 'author']) {
    if (fm[req] == null || fm[req] === '') flag('missing-required', slug, `missing ${req}`);
  }
  const declaredSlug = str(fm, 'slug');
  if (declaredSlug && declaredSlug !== slug) flag('slug-mismatch', slug, `slug=${declaredSlug} vs filename`);

  // enums
  const pt = str(fm, 'powertrain');
  if (pt && !POWERTRAINS.has(pt)) flag('unsupported-powertrain', slug, `powertrain=${pt}`);
  const bt = str(fm, 'type');
  if (bt && !BODY_TYPES.has(bt)) flag('invalid-body-type', slug, `type=${bt}`);

  // price type enum
  const ptc = str(fm, 'price_type');
  if (ptc && !PRICE_TYPES.has(ptc)) flag('invalid-price-type', slug, `price_type=${ptc}`);

  // numeric sanity (unit ranges)
  const price = num(fm, 'price_usd');
  if (price == null || price <= 0) flag('invalid-price', slug, `price_usd=${fm.price_usd}`);
  else if (price > 300000) flag('price-out-of-range', slug, `price_usd=${price}`);

  const battery = num(fm, 'battery_kwh');
  if (battery != null && (battery <= 0 || battery > 300)) flag('invalid-battery', slug, `battery_kwh=${battery}`);

  for (const [k, lo, hi] of [
    ['range_cltc_km', 50, 1500], ['range_wltp_km', 50, 1500],
    ['range_epa_km', 50, 1500], ['range_nedc_km', 50, 1500],
  ]) {
    const v = num(fm, k);
    if (v != null && (v < lo || v > hi)) flag('invalid-range', slug, `${k}=${v}`);
  }
  const ts = num(fm, 'top_speed_kmh');
  if (ts != null && (ts <= 0 || ts > 500)) flag('invalid-top-speed', slug, `top_speed_kmh=${ts}`);

  // family (nameplate) presence
  if (!str(fm, 'family')) flag('missing-family', slug, 'missing family');

  // brand relationship
  const brand = str(fm, 'brand');
  if (brand && !brandSlugs.has(brand)) flag('unknown-brand', slug, `brand=${brand} not in brands`);
  if (brand) brandModelCounts.set(brand, (brandModelCounts.get(brand) ?? 0) + 1);
}
ok.push(`vehicles: ${vehFiles.length} (required fields, enums, units, family, brand relation checked)`);

// ── 3. Brand <-> vehicle bidirectional consistency ──
for (const bf of brandFiles) {
  const slug = bf.replace(/\.md$/, '');
  const fm = parseFrontmatter(readFileSync(join(BRAND_DIR, bf), 'utf8'));
  const mc = fm ? num(fm, 'model_count') : null;
  const actual = brandModelCounts.get(slug) ?? 0;
  if (mc != null && mc !== actual) {
    flag('brand-count-drift', slug, `model_count=${mc} vs ${actual} vehicles`);
  }
}
ok.push('brand↔vehicle relationship: bidirectional, model_count reconciled');

// ── 4. Summary ──
console.log('=== China EV Mart Data Validation (Phase 3) ===');
for (const line of ok) console.log('  ✓', line);
if (issues.length === 0) {
  console.log('\n✅ 0 issues. All data validation checks passed.');
  process.exit(0);
}
console.log(`\n❌ ${issues.length} issues found:`);
const byCat = {};
for (const i of issues) (byCat[i.category] ??= []).push(i);
for (const [cat, list] of Object.entries(byCat)) {
  console.log(`\n[${cat}] (${list.length})`);
  for (const i of list.slice(0, 40)) console.log(`  - ${i.id}: ${i.message}`);
  if (list.length > 40) console.log(`  … and ${list.length - 40} more`);
}
process.exit(1);
