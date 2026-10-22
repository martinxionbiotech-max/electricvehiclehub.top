#!/usr/bin/env node
/**
 * Phase 3 data migration — price_type / range-standard normalization.
 * Run: node scripts/migrate-p3-data.mjs [--apply]
 *
 * Default = DRY-RUN: reports affected record counts without writing.
 * --apply = writes explicit `price_type` into each vehicle frontmatter so the
 *           price basis is self-documenting (no hidden schema default).
 *
 * Rationale (P3 rule #4): the old schema default `China ex-factory price
 * (MSRP)` conflated two distinct price bases. The new canonical 5-category
 * enum is enforced in `src/content.config.ts`; this script only backfills the
 * explicit field for auditability. It never changes a price VALUE — only the
 * `price_type` label derived from the already-documented source basis.
 */
import { readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const ROOT = new URL('..', import.meta.url).pathname;
const VEH_DIR = join(ROOT, 'src/content/vehicles');
const APPLY = process.argv.includes('--apply');

const TARGET = 'China ex-factory reference price';

const files = readdirSync(VEH_DIR).filter((f) => f.endsWith('.md'));
const stats = {
  total: files.length,
  explicitExisting: 0,
  wouldAdd: 0,
  alreadyTarget: 0,
  conflicting: [],
  missingPriceUsd: [],
};

for (const f of files) {
  const p = join(VEH_DIR, f);
  const raw = readFileSync(p, 'utf8');
  const m = raw.match(/^---\n([\s\S]*?)\n---/);
  if (!m) { stats.missingPriceUsd.push(f); continue; }
  const fm = m[1];

  if (!/^price_usd:\s*[0-9]/m.test(fm)) {
    stats.missingPriceUsd.push(f);
    continue;
  }

  const existing = fm.match(/^price_type:\s*"([^"]+)"/m);
  if (existing) {
    stats.explicitExisting++;
    if (existing[1] === TARGET) {
      stats.alreadyTarget++;
    } else {
      stats.conflicting.push({ file: f, value: existing[1] });
    }
    continue;
  }

  // No explicit price_type -> would add TARGET after the price_usd line.
  stats.wouldAdd++;
  if (APPLY) {
    const updated = raw.replace(
      /^(price_usd:\s*[0-9][^\n]*)$/m,
      `$1\nprice_type: "${TARGET}"`,
    );
    if (updated !== raw) writeFileSync(p, updated);
  }
}

console.log('=== P3 price_type migration ===');
console.log(`mode: ${APPLY ? 'APPLY' : 'DRY-RUN (no writes)'}`);
console.log(`total vehicles: ${stats.total}`);
console.log(`explicit price_type already present: ${stats.explicitExisting}`);
console.log(`  ├─ already "${TARGET}": ${stats.alreadyTarget}`);
console.log(`  └─ conflicting values: ${stats.conflicting.length}`);
console.log(`would add "${TARGET}" (currently default): ${stats.wouldAdd}`);
console.log(`missing price_usd (skipped): ${stats.missingPriceUsd.length}`);

if (stats.conflicting.length) {
  console.log('\nConflicting price_type values (kept as-is):');
  for (const c of stats.conflicting) console.log(`  - ${c.file}: ${c.value}`);
}

if (!APPLY) {
  console.log('\nRun with --apply to write the field. Schema default already applies this');
  console.log('label at build time; the explicit write only improves auditability.');
}
