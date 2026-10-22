#!/usr/bin/env python3
"""De-cost 517 vehicle descriptions: replace the 3 landed-cost endings with
product-info endings. Idempotent — re-running yields zero diff."""
import glob, re, sys

REPLACEMENTS = [
    (
        "Full landed-cost breakdown across 30 export markets for B2B import planning.",
        "Full product specification in the Chinese EV database.",
    ),
    (
        "Landed-cost analysis across 30 key export markets for importers.",
        "Complete product specifications, versions and technology data in the Chinese EV database.",
    ),
    (
        "Per-market landed-cost modeling across 30 export destinations.",
        "Deep product specifications, versions and technology data in the Chinese EV database.",
    ),
]

files = sorted(glob.glob("src/content/vehicles/*.md"))
changed = 0
remaining = []
for fp in files:
    with open(fp, "r", encoding="utf-8") as f:
        raw = f.read()
    new = raw
    for old, repl in REPLACEMENTS:
        new = new.replace(old, repl)
    if new != raw:
        changed += 1
        with open(fp, "w", encoding="utf-8") as f:
            f.write(new)
    # verify no landed-cost ending remains
    for old, _ in REPLACEMENTS:
        if old in new:
            remaining.append(fp)

print(f"changed={changed}/{len(files)}")
print(f"remaining_with_old_endings={len(remaining)}")
if remaining:
    for r in remaining[:20]:
        print("REMAIN:", r)
    sys.exit(1)
