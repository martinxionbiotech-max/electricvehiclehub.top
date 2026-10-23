#!/usr/bin/env node
/**
 * Generate src/data/parameter-verification.json — parameter-level source
 * metadata for the key-parameter table (price / range / battery / motor /
 * accel / charge), covering homepage featured 6 + A-tier Tier-1 top 30.
 *
 * Discipline: conflict fields are MARKED, never auto-filled. The three states
 * are verified / mismatch / unverifiable. A `conflict` status means two
 * sources (or the field vs. the rendered body) disagree; the value is left
 * untouched and flagged for manual review.
 */
import { readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const DIR = 'src/content/vehicles';
const OUT = 'src/data/parameter-verification.json';

const FEATURED = ['hongqi-guoya', 'yangwang-u8l', 'yangwang-u8', 'nio-et9', 'maextro-s800', 'aito-m9-ultimate'];

// Read all vehicles to resolve data_tier + quality_tier for the top-30 list.
const files = readdirSync(DIR).filter((f) => f.endsWith('.md'));
const recs = [];
for (const f of files) {
  const raw = readFileSync(join(DIR, f), 'utf8');
  const m = raw.match(/^---\n([\s\S]*?)\n---/);
  if (!m) continue;
  const fm = {};
  for (const line of m[1].split('\n')) {
    const mm = line.match(/^([A-Za-z0-9_]+):\s*(.*)$/);
    if (mm) fm[mm[1]] = mm[2];
  }
  const s = (k) => (fm[k] == null ? undefined : fm[k].replace(/^"|"$/g, '').trim());
  const n = (k) => {
    const v = fm[k];
    if (v == null || v === '' || v === 'null') return null;
    const x = Number(v.replace(/^"|"$/g, ''));
    return Number.isFinite(x) ? x : null;
  };
  recs.push({
    slug: s('slug'),
    tier: s('quality_tier'),
    data_tier: n('data_tier'),
    price: n('price_usd'),
    range: n('range_cltc_km'),
    battery: n('battery_kwh'),
    motor: n('motor_power_kw') ?? n('total_power_kw'),
    accel: n('accel_0_100_s'),
    charge: s('fast_charge'),
    model_year: n('model_year'),
    trim: s('trim'),
    data_source: s('data_source'),
    data_updated: s('data_updated'),
    type: s('type'),
    powertrain: s('powertrain'),
  });
}

const tier1A = recs
  .filter((r) => r.tier === 'A' && r.data_tier === 1)
  .sort((a, b) => b.price - a.price)
  .slice(0, 30)
  .map((r) => r.slug);

const covered = [...new Set([...FEATURED, ...tier1A])];

/** Build one parameter cell. status: verified|mismatch|unverifiable|conflict */
function cell(source, verified_at, status, confidence = 'low', extra = {}) {
  return { source, verified_at, status, confidence, ...extra };
}

/**
 * Hand-verified findings (web search of official/official-adjacent sources,
 * 2026-10-23). Everything not listed here for a given vehicle is `unverifiable`
 * (pending manual review) — never asserted as verified without a source.
 */
const VERIFIED = {
  'yangwang-u8': {
    battery: cell('BYD / Yangwang official spec (bydcn.com) + Wikipedia', '2026-10-23', 'verified', 'high', { value_ref: '49.05 kWh' }),
    motor: cell('BYD / Yangwang official + Wikipedia (4×220 kW)', '2026-10-23', 'verified', 'high', { value_ref: '880 kW' }),
    range: cell('BYD official "180/124 km" electric-only', '2026-10-23', 'conflict', 'medium', { note: 'field=180 km electric-only; body claims "780 km CLTC" (combined range-extended). Value left unchanged; body wording needs correction.' }),
    accel: cell('BYD official 3.6 s', '2026-10-23', 'conflict', 'medium', { note: 'field=3.6 s; body claims 3.9 s. Value left unchanged.' }),
    price: cell('China EV Mart catalog (ex-factory USD)', '2026-10-21', 'unverifiable', 'low'),
    charge: cell('BYD official 18 min 30–80%', '2026-10-23', 'unverifiable', 'low'),
  },
  'nio-et9': {
    battery: cell('Wikipedia / auto-data.net: 100 kWh', '2026-10-23', 'conflict', 'medium', { note: 'field=102 kWh; official specs say 100 kWh. Value left unchanged.' }),
    motor: cell('Wikipedia / auto-data.net: 520 kW dual-motor', '2026-10-23', 'verified', 'high', { value_ref: '520 kW' }),
    range: cell('EV Gulf / official: ~650 km CLTC', '2026-10-23', 'verified', 'high', { value_ref: '650 km CLTC' }),
    type: cell('Wikipedia: full-size luxury SEDAN', '2026-10-23', 'conflict', 'high', { note: 'field type=SUV; ET9 is a sedan. Body-type field needs correction.' }),
    price: cell('China EV Mart catalog (ex-factory USD)', '2026-10-21', 'unverifiable', 'low'),
  },
  'maextro-s800': {
    battery: cell('auto-data.net / CN Auto: BEV 97/120 kWh; EREV 65 kWh', '2026-10-23', 'conflict', 'medium', { note: 'field battery=65 kWh (the EREV pack) but powertrain=BEV. Value left unchanged; needs trim/powertrain reconciliation.' }),
    motor: cell('Wikipedia: 390–635 kW (base 390)', '2026-10-23', 'verified', 'medium', { value_ref: '390 kW (base)' }),
    range: cell('CN Auto: BEV 650–780 km CLTC', '2026-10-23', 'verified', 'medium', { value_ref: '670 km CLTC' }),
    price: cell('China EV Mart catalog (ex-factory USD)', '2026-10-21', 'unverifiable', 'low'),
  },
  'hongqi-guoya': {
    motor: cell('Wikipedia: hybrid system 294–358 kW (V6/V8)', '2026-10-23', 'conflict', 'medium', { note: 'field motor_power_kw=160 kW; official hybrid system output 294–358 kW. Value left unchanged; power basis unclear.' }),
    price: cell('China EV Mart catalog (ex-factory USD)', '2026-10-21', 'unverifiable', 'low'),
    powertrain: cell('Hongqi official / Wikipedia: power-split hybrid (non-plug-in)', '2026-10-23', 'verified', 'high', { note: 'HEV in a new-energy-vehicle catalog is a pre-existing boundary item (P3 U-2).' }),
  },
  'yangwang-u8l': {
    battery: cell('Electrek (Aug 2026): 56.58 kWh Blade', '2026-10-23', 'conflict', 'medium', { note: 'field battery=55.53 kWh; launch report says 56.58 kWh. Value left unchanged.' }),
    range: cell('Electrek: pure-electric CLTC 230 km', '2026-10-23', 'conflict', 'medium', { note: 'field range=200 km; launch report says 230 km. Value left unchanged.' }),
    motor: cell('BYD / Yangwang: 880 kW quad-motor', '2026-10-23', 'verified', 'medium', { value_ref: '880 kW' }),
    price: cell('China EV Mart catalog (ex-factory USD)', '2026-10-21', 'unverifiable', 'low'),
  },
  'aito-m9-ultimate': {
    price: cell('China EV Mart catalog (ex-factory USD)', '2026-10-21', 'unverifiable', 'low'),
    battery: cell('AITO M9 EREV official (no clean single figure for "Ultimate" trim)', '2026-10-23', 'unverifiable', 'low'),
    range: cell('range_long_km=1260 is combined (range-extended), not CLTC electric', '2026-10-23', 'unverifiable', 'low'),
    motor: cell('AITO M9 EREV: ~365 kW dual-motor (not cleanly confirmed)', '2026-10-23', 'unverifiable', 'low'),
  },
};

const PARAMS = ['price', 'range', 'battery', 'motor', 'accel', 'charge'];

const vehicles = {};
for (const slug of covered) {
  const r = recs.find((x) => x.slug === slug);
  if (!r) continue;
  const pv = {};
  for (const p of PARAMS) {
    const hand = VERIFIED[slug]?.[p];
    if (hand) {
      pv[p] = {
        value: r[p] ?? null,
        ...hand,
        model_year: r.model_year ?? null,
        trim: r.trim ?? null,
      };
    } else {
      // Unverified coverage entry — parameter recorded, pending manual review.
      pv[p] = {
        value: r[p] ?? null,
        source: r.data_source || 'China EV Mart catalog',
        verified_at: r.data_updated || null,
        status: 'unverifiable',
        confidence: 'low',
        model_year: r.model_year ?? null,
        trim: r.trim ?? null,
      };
    }
  }
  // Attach the two extra hand-verified non-PARAMS cells (type / powertrain) when present.
  for (const extra of ['type', 'powertrain']) {
    if (VERIFIED[slug]?.[extra]) {
      pv[extra] = { value: r[extra] ?? null, ...VERIFIED[slug][extra] };
    }
  }
  vehicles[slug] = pv;
}

const doc = {
  schema_version: 1,
  generated: '2026-10-23',
  purpose:
    'Parameter-level source metadata for the key-parameter table (price / range / battery / motor / accel / charge). States: verified | mismatch | unverifiable | conflict. Conflict values are flagged, never auto-filled.',
  coverage: {
    total: covered.length,
    featured_homepage: FEATURED.length,
    a_tier_tier1_top30: tier1A.length,
    union_unique: covered.length,
    slugs: covered,
  },
  params: PARAMS,
  status_enum: ['verified', 'mismatch', 'unverifiable', 'conflict'],
  confidence_enum: ['high', 'medium', 'low'],
  vehicles,
};

writeFileSync(OUT, JSON.stringify(doc, null, 2) + '\n');
console.log(`Wrote ${OUT}: ${covered.length} vehicles covered (${FEATURED.length} featured + ${tier1A.length} tier-1 top-30, union ${covered.length}).`);
