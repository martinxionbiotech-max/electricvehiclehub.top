#!/usr/bin/env python3
"""Backfill missing hs_code on 52 pre-existing deep-profile files (w1 era) that have
charging_interface but no hs_code. HS Code by powertrain: BEV=87038000, PHEV/EREV/HEV=870340.
Idempotent: skips files that already carry hs_code."""
import re, os, glob

UPDATED = "2026-10-19"
SRC = "EV Hub catalog + manufacturer specs (verified via en.wikipedia.org, 2026-10-19)"

BASE = "src/content/vehicles"
done = 0
for path in sorted(glob.glob(BASE + "/*.md")):
    raw = open(path, encoding="utf-8").read()
    if re.search(r'^hs_code:', raw, re.M):
        continue
    if not re.search(r'^charging_interface:', raw, re.M):
        continue
    m = re.search(r'^powertrain:\s*"([^"]+)"', raw, re.M)
    if not m:
        print(f"!! no powertrain {path}")
        continue
    pt = m.group(1)
    hs = "87038000" if pt == "BEV" else ("870340" if pt in ("PHEV", "EREV", "HEV") else None)
    if hs is None:
        print(f"!! unknown powertrain {pt} {path}")
        continue
    fm_m = re.match(r'^(---\n)([\s\S]*?)(\n---)', raw)
    if not fm_m:
        print(f"!! no frontmatter {path}")
        continue
    fm = fm_m.group(2)
    line = f'hs_code: "{hs}"'
    if re.search(r'^hs_code:', fm, re.M):
        continue
    fm_clean = re.sub(r'^data_updated:[^\n]*(\n|$)', '', fm, flags=re.M)
    fm_clean = re.sub(r'^data_source:[^\n]*(\n|$)', '', fm_clean, flags=re.M)
    new_fm = fm_clean.rstrip('\n') + '\n' + line + '\n' + f'data_updated: "{UPDATED}"' + '\n' + f'data_source: "{SRC}"'
    new_raw = '---\n' + new_fm + '\n---' + raw[fm_m.end():]
    open(path, "w", encoding="utf-8").write(new_raw)
    done += 1
    print(f"✓ {os.path.basename(path)} -> {hs}")

print(f"done: {done} files")
