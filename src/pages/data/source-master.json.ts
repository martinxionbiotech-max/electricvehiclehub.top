import sourceMaster from '../../data/source-master.json';

/**
 * /data/source-master.json — machine-readable public export (§16 / §7).
 * Field-level provenance registry: source records + the `_conventions` block
 * (source_type / confidence enums, legacy source_type mapping, field_sources).
 * Re-exported from the single source of truth (src/data/source-master.json).
 *
 * Linked from /docs/data-provenance/ — the machine-readable convention document.
 */
export function GET() {
  return new Response(JSON.stringify(sourceMaster, null, 2), {
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
  });
}
