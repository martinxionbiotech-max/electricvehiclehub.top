/**
 * Powertrain label system — single source for powertrain terminology (P2 style guide §3).
 *
 * The frontmatter `powertrain` enum is BEV / PHEV / EREV / HEV / ICE (content.config.ts).
 * These labels map each code to its full term + short form so UI can distinguish
 * powertrain (how the wheels are driven) from body type (vehicle category).
 */

export const POWERTRAIN_ORDER = ['BEV', 'PHEV', 'EREV', 'HEV', 'ICE'] as const;

export const POWERTRAIN_LABELS: Record<string, string> = {
  BEV: 'Battery electric',
  PHEV: 'Plug-in hybrid',
  EREV: 'Extended-range electric',
  HEV: 'Hybrid (non-plug-in)',
  ICE: 'Internal combustion',
  FCEV: 'Fuel cell electric',
  Unknown: 'Unclassified',
};

/** Short code + full label, e.g. "BEV · Battery electric". */
export function powertrainLabel(code?: string): string {
  if (!code) return 'Unclassified';
  return POWERTRAIN_LABELS[code] ?? code;
}

/** Display code with fallback. */
export function powertrainCode(code?: string): string {
  return code || 'Unknown';
}
