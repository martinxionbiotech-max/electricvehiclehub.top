#!/usr/bin/env python3
"""
P0 data-conflict scanner — single-source-of-truth audit (v2).

Detects "same field, multiple components, multiple values" across the render
surfaces of each vehicle record:
  1. frontmatter (canonical — the single source of truth)
  2. `description` frontmatter (human-written summary; rendered in meta/JSON-LD/cards/.md)
  3. Markdown body prose (legacy hardcoded spec bullets — dead content, not rendered)

A "conflict" is a genuine divergence (not display rounding). Rounding is reported
separately. Output: docs/p0-data-conflict-scan.json.
"""
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
VEH_DIR = ROOT / "src" / "content" / "vehicles"
PARAM_VERIF = ROOT / "src" / "data" / "parameter-verification.json"

FIELDS = {
    "price_usd": "price",
    "range_cltc_km": "range",
    "battery_kwh": "battery",
    "motor_power_kw": "motor",
    "accel_0_100_s": "accel",
    "top_speed_kmh": "top_speed",
}

# body bullet patterns (legacy hardcoded spec list)
BODY_PATTERNS = {
    "range_cltc_km": [r"-\s*\*\*Range\*\*:\s*([\d.,]+)\s*km\s*\(CLTC\)"],
    "battery_kwh": [r"-\s*\*\*Battery\*\*:\s*([\d.,]+)\s*kWh"],
    "motor_power_kw": [r"-\s*\*\*Motor power\*\*:\s*([\d.,]+)\s*kW"],
    "accel_0_100_s": [r"-\s*\*\*0-100 km/h\*\*:\s*([\d.,]+)\s*s"],
    "top_speed_kmh": [r"\btop speed of\s+([\d.,]+)\s*km/h"],
    "price_usd": [r"\(starting at\s*\$([\d,]+)\)"],
}

# description patterns — precise, matching the actual summary sentence format
DESC_PATTERNS = {
    "range_cltc_km": [
        r"(\d[\d,.]*)\s*km\s+of\s+CLTC\s+range",
        r"CLTC-rated\s+range\s+of\s+(\d[\d,.]*)\s*km",
        r"offering\s+(\d[\d,.]*)\s*km\s+of\s+CLTC",
    ],
    "battery_kwh": [
        r"(\d[\d,.]*)\s*kWh(?:\s+of\s+battery)",
        r"\ba\s+(\d[\d,.]*)\s*kWh\s+battery",
    ],
    "motor_power_kw": [
        r"(\d[\d,.]*)\s*kW\s+peak\s+output",
        r"(\d[\d,.]*)\s*kW\s+of\s+motor\s+power",
    ],
    "accel_0_100_s": [],
    "top_speed_kmh": [],
}


def num(s: str):
    try:
        return float(s.replace(",", ""))
    except (ValueError, AttributeError):
        return None


def parse_frontmatter(text: str):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not m:
        return None, None
    try:
        fm = yaml.safe_load(m.group(1))
    except Exception as e:  # noqa: BLE001
        return None, f"YAML-ERROR: {e}"
    return fm, m.group(2)


def classify(a, b):
    """Return 'conflict' | 'rounding' | None for two numeric values."""
    if a is None or b is None:
        return None
    d = abs(float(a) - float(b))
    if d <= 1e-9:
        return None
    rel = d / max(abs(float(a)), abs(float(b)), 1e-9)
    # Integer-truncation display: description/body shows the whole-number form of a
    # decimal field (e.g. 49.75 -> 49, 18.4 -> 18). Not a data conflict.
    if float(b) == round(float(b)) and d < 1.0:
        return "rounding"
    # Near-identical relative values (<1.5%): rounding.
    if rel < 0.015:
        return "rounding"
    return "conflict"


def main():
    pv = json.loads(PARAM_VERIF.read_text()) if PARAM_VERIF.exists() else {"vehicles": {}}
    pv_vehicles = pv.get("vehicles", {})

    conflicts = []
    roundings = []
    files = sorted(VEH_DIR.glob("*.md"))
    total = len(files)

    for fp in files:
        text = fp.read_text()
        fm, body = parse_frontmatter(text)
        slug = fp.stem
        if fm is None:
            conflicts.append({"slug": slug, "error": body or "no-frontmatter"})
            continue
        pv_entry = pv_vehicles.get(slug, {})

        for field, label in FIELDS.items():
            fm_val = fm.get(field)
            if fm_val is None:
                continue

            # ── body prose ──
            body_val = None
            for pat in BODY_PATTERNS.get(field, []):
                mm = re.search(pat, body or "", re.IGNORECASE)
                if mm:
                    body_val = num(mm.group(1))
                    if body_val is not None:
                        break
            kind = classify(fm_val, body_val)
            if kind:
                rec = {
                    "slug": slug,
                    "field": field,
                    "component": "body-prose",
                    "frontmatter": fm_val,
                    "other": body_val,
                    "kind": kind,
                    "param_verification_status": (pv_entry.get(label) or {}).get("status"),
                }
                (conflicts if kind == "conflict" else roundings).append(rec)

            # ── description ──
            desc = fm.get("description") or ""
            desc_val = None
            for pat in DESC_PATTERNS.get(field, []):
                mm = re.search(pat, desc, re.IGNORECASE)
                if mm:
                    desc_val = num(mm.group(1))
                    if desc_val is not None:
                        break
            kind = classify(fm_val, desc_val)
            if kind:
                rec = {
                    "slug": slug,
                    "field": field,
                    "component": "description",
                    "frontmatter": fm_val,
                    "other": desc_val,
                    "kind": kind,
                    "param_verification_status": (pv_entry.get(label) or {}).get("status"),
                }
                (conflicts if kind == "conflict" else roundings).append(rec)

    summary = {
        "total_vehicles": total,
        "genuine_conflicts": len(conflicts),
        "vehicles_with_conflicts": len({c["slug"] for c in conflicts if "error" not in c}),
        "rounding_only": len(roundings),
        "conflict_by_component": {
            comp: len([c for c in conflicts if c.get("component") == comp])
            for comp in ("body-prose", "description")
        },
    }

    out_path = ROOT / "docs" / "p0-data-conflict-scan.json"
    out_path.write_text(
        json.dumps({"summary": summary, "conflicts": conflicts, "roundings": roundings}, ensure_ascii=False, indent=2)
    )

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"\nWrote {out_path}")

    print("\n=== GENUINE conflicts (body-prose) ===")
    for c in [x for x in conflicts if x.get("component") == "body-prose"]:
        print(f"  {c['slug']:24s} {c['field']:14s} fm={c['frontmatter']!s:>8} body={c['other']!s:>8} pv={c['param_verification_status']}")

    print("\n=== GENUINE conflicts (description) ===")
    for c in [x for x in conflicts if x.get("component") == "description"]:
        print(f"  {c['slug']:24s} {c['field']:14s} fm={c['frontmatter']!s:>8} desc={c['other']!s:>8} pv={c['param_verification_status']}")


if __name__ == "__main__":
    sys.exit(main())
