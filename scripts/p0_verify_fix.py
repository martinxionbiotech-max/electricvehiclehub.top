#!/usr/bin/env python3
"""P0 data verification batch — apply verified field corrections + add
verification_status marker + bump data_updated. Idempotent.

Source: en.wikipedia.org (MediaWiki API plaintext) + manufacturer spec cross-check,
2026-10-22. Only unambiguous mismatches are corrected; ambiguous/trim-dependent
values are marked `partial`/`unverifiable` (never fabricated).
"""
import re, glob, os

ROOT = os.path.join(os.path.dirname(__file__), "..")

# Field corrections (mismatch -> verified official value). None = set to null (N/A).
FIXES = {
    "bestune-pony":           {"fast_charge": None},  # AC-only micro EV, no DC fast charge ("5h 10m" is AC)
    "byd-seagull":            {"accel_0_100_s": 13.0},  # 4.9 is 0-50 km/h; 0-100 = 13 s
    "byd-seal":               {"range_cltc_km": 550, "top_speed_kmh": 180, "fast_charge": "30 min (30-80%)"},
    "byd-han":                {"battery_kwh": 76.9},  # all Han EV = 76.9 kWh pack
    "changan-nevo-lamore":    {"torque_nm": 260, "top_speed_kmh": 200, "fast_charge": None},  # ICE: 260 Nm / 200 km/h / no charging
    "yangwang-u8":            {"accel_0_100_s": 3.6, "top_speed_kmh": 200, "fast_charge": "18 min (30-80%)"},
    "m-hero-917":             {"motor_power_kw": 797},  # BEV quad-motor total 797 kW (600 kW is the EREV value)
    "fangchengbao-bao-5":     {"motor_power_kw": 505},  # combined 505 kW
    "tank-700":               {"motor_power_kw": 385, "torque_nm": 800},  # combined 385 kW / 800 Nm
    "wey-lanshan":            {"motor_power_kw": 380},  # combined 380 kW
    "denza-z9-gt":            {"motor_power_kw": 710, "accel_0_100_s": 3.4},  # BEV tri-motor 710 kW / 3.4 s
    "wuling-hongguang-mini-ev": {"fast_charge": None},  # base Mini EV AC-only, no DC fast charge
    "geely-galaxy-e5":        {"top_speed_kmh": 175},  # EX5/E5 top speed 175 km/h
}

# Record-level verification outcome (all 40 sampled vehicles).
# verified = all four dimensions confirmed, no unverifiable field.
# partial = some fields confirmed, some unverifiable/trim-dependent.
# unverifiable = authoritative source unavailable/wrong model -> nothing confirmable.
STATUS = {
    "bestune-pony": "partial", "byd-seagull": "partial", "byd-dolphin": "partial",
    "byd-atto-3": "partial", "byd-seal": "partial", "byd-han": "partial",
    "byd-song-plus-dm-i": "partial", "byd-qin-l-dm-i": "unverifiable",
    "byd-sealion-07": "partial", "chery-tiggo-9": "partial", "chery-fulwin-a9": "partial",
    "chery-new-energy-eq1": "partial", "chery-explore-06-c-dm": "unverifiable",
    "exeed-exlantix-es": "partial", "jetour-shanhai-l7": "partial",
    "geely-galaxy-e5": "partial", "geely-galaxy-e8": "partial",
    "geely-monjaro": "partial", "geely-galaxy-l7": "partial",
    "geely-galaxy-starshine-7": "partial", "xiaomi-su7": "partial",
    "xiaomi-yu7": "partial", "xiaomi-su7-ultra": "partial",
    "yangwang-u8": "partial", "yangwang-u7": "verified",
    "m-hero-917": "partial", "fangchengbao-bao-5": "partial",
    "tank-700": "partial", "wey-lanshan": "partial", "avatr-12": "partial",
    "zeekr-001": "partial", "nio-es8": "verified", "xpeng-g6": "partial",
    "aion-y": "partial", "wuling-hongguang-mini-ev": "partial",
    "mg-4": "partial", "denza-z9-gt": "partial", "leapmotor-c10": "partial",
    "haval-jolion-pro": "partial", "changan-nevo-lamore": "partial",
}

SRC = "en.wikipedia.org + manufacturer specs (P0 field verification, 2026-10-22)"
DATE = "2026-10-22"

def load_fm(path):
    raw = open(path).read()
    m = re.match(r"^---\n(.*?)\n---\n", raw, re.S)
    if not m:
        raise RuntimeError(f"no frontmatter: {path}")
    return raw, m.group(1)

def set_field(fm, key, val):
    """Replace a scalar frontmatter field value. Returns (fm, changed)."""
    if val is None:
        # set to null
        if re.search(rf"^{key}:\s*$", fm, re.M):
            return fm, False
        new, n = re.subn(rf"^{key}:.*$", f"{key}: null", fm, flags=re.M)
        return new, n > 0
    # numeric
    if isinstance(val, (int, float)) and not isinstance(val, bool):
        new, n = re.subn(rf"^{key}:.*$", f"{key}: {val}", fm, flags=re.M)
        return new, n > 0
    # string (quote)
    new, n = re.subn(rf"^{key}:.*$", f'{key}: "{val}"', fm, flags=re.M)
    return new, n > 0

def set_meta(fm, key, val):
    new, n = re.subn(rf"^{key}:.*$", f'{key}: "{val}"', fm, flags=re.M)
    return new, n > 0

fixed_count = 0
changed_fields = []

for slug, fixes in FIXES.items():
    path = os.path.join(ROOT, "src/content/vehicles", f"{slug}.md")
    raw, fm = load_fm(path)
    for key, val in fixes.items():
        fm2, changed = set_field(fm, key, val)
        if changed:
            fm = fm2
            changed_fields.append((slug, key, val))
    # bump data_updated
    fm, _ = set_meta(fm, "data_updated", DATE)
    # append source note if any fix applied this round
    if any(c[0] == slug for c in changed_fields):
        fixed_count += 1
        # append to data_source
        if "P0 field verification" not in fm:
            fm = fm.rstrip("\n") + " · P0 field verification (corrected vs " + SRC + ")\n"
    # add/replace verification_status
    if re.search(r"^verification_status:", fm, re.M):
        fm, _ = set_meta(fm, "verification_status", STATUS[slug])
    else:
        # insert after data_reviewed line
        fm = re.sub(r"(^data_reviewed:.*$)",
                    r"\1\nverification_status: \"" + STATUS[slug] + "\"",
                    fm, flags=re.M)
    start = raw.index("---\n") + 4
    end = raw.index("\n---\n", 4)
    out = raw[:start] + fm + raw[end:]
    open(path, "w").write(out)

print(f"applied fixes: {fixed_count} files, {len(changed_fields)} field corrections")
for slug, key, val in changed_fields:
    print(f"  {slug}: {key} -> {val!r}")
