#!/usr/bin/env python3
"""EVHub Top window-1h (第八小批, final micro-batch): inject deep-profile frontmatter
into remaining export-mainstay high-value vehicles — Maxus EG10 / NIO ET5T / Geely
Galaxy L380 (LEVC) / Hongqi HS7 / Aion LX & LX Plus / Voyah Passion L.

Same field contract as window 1..1g (scripts/inject_deep_profile*.py). Fields omitted
-> rendered N/A by the [slug].astro template (zero fabrication). Verified against
manufacturer specs + en.wikipedia.org where available (NIO ET5, Aion LX, Hongqi HS7,
LEVC L380); uncertain chemistry/thermal sub-fields left N/A.
"""
import re, os

SRC = "EV Hub catalog + manufacturer specs (verified via en.wikipedia.org, 2026-10-19)"
UPDATED = "2026-10-19"

GB_CHG = "GB/T AC + GB/T DC (China domestic)"
GB_ADAP_BEV = "CCS2 (DC) / Type 2 (AC) adapter required for EU; or OEM EU-spec port"
GB_ADAP_PHEV = "PHEV/EREV: Type 2 (AC) adapter for EU AC charging"
CERT = "EU: WVTA type approval; GB/T port needs CCS2/Type 2 adapter. GCC: GSO conformity certificate."

def bev():
    return dict(charging_interface=GB_CHG, charging_adapter=GB_ADAP_BEV,
                certification_notes=CERT, hs_code="87038000")

def phev():
    return dict(charging_interface=GB_CHG, charging_adapter=GB_ADAP_PHEV,
                certification_notes=CERT, hs_code="870340")

DATA = {
  # ── Maxus EG10 (1) — full-size BEV MPV (G10-based), single-motor RWD ──
  "maxus-eg10": dict(drive_type="RWD", motor_type="PMSM (single motor)",
    battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),

  # ── NIO ET5T (1) — NT2.0 BEV wagon, dual-motor AWD ──
  "nio-et5t": dict(battery_type="NMC (CATL)", drive_type="AWD (dual motor)",
    motor_type="PMSM (rear) / induction (front)", battery_thermal="Liquid cooling",
    heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),

  # ── Geely Galaxy L380 (LEVC) (1) — BEV MPV, single-motor RWD ──
  "geely-galaxy-l380": dict(battery_type="NMC (CATL)", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),

  # ── Hongqi HS7 (1) — PHEV midsize SUV, 2.0T + single motor FWD ──
  "hongqi-hs7": dict(drive_type="FWD", motor_type="PMSM (single motor)",
    battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),

  # ── Aion LX (1) — BEV midsize SUV, single-motor RWD ──
  "aion-lx": dict(battery_type="NMC (ternary)", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),

  # ── Aion LX Plus (1) — BEV midsize SUV, single-motor RWD, 144.4 kWh ──
  "aion-lx-plus": dict(battery_type="NMC (ternary)", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),

  # ── Voyah Passion L (1) — EREV/PHEV premium sedan, dual-motor AWD ──
  "voyah-passion-l": dict(battery_type="NMC (CATL)", drive_type="AWD (dual motor)",
    motor_type="PMSM (dual motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **phev()),
}

def yaml_str(v):
    return '"' + str(v).replace('\\', '\\\\').replace('"', '\\"') + '"'

def yaml_val(v):
    if v is None:
        return None
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, (int, float)):
        return str(v)
    return yaml_str(v)

FIELDS_ORDER = [
    "battery_type", "drive_type", "motor_type", "motor_model", "total_power_kw",
    "battery_thermal", "heat_pump", "suspension_front", "suspension_rear", "brakes",
    "drag_coefficient", "range_wltp_km", "gross_weight_kg", "ground_clearance_mm", "trunk_l",
    "fob_price_usd_min", "fob_price_usd_max", "trim",
    "charging_interface", "charging_adapter", "infotainment_language", "network_bands",
    "certification_notes", "hs_code",
]

BASE = "src/content/vehicles"
done = 0
for slug, fields in DATA.items():
    path = os.path.join(BASE, slug + ".md")
    if not os.path.exists(path):
        print(f"!! MISSING {slug}")
        continue
    raw = open(path, encoding="utf-8").read()
    m = re.match(r'^(---\n)([\s\S]*?)(\n---)', raw)
    if not m:
        print(f"!! NO FRONTMATTER {slug}")
        continue
    fm = m.group(2)
    new_lines = []
    for k in FIELDS_ORDER:
        if k not in fields:
            continue
        v = fields[k]
        yv = yaml_val(v)
        if yv is None:
            continue
        if re.search(rf'^{re.escape(k)}:', fm, re.M):
            continue
        new_lines.append(f"{k}: {yv}")
    new_lines.append(f"data_updated: {yaml_str(UPDATED)}")
    new_lines.append(f"data_source: {yaml_str(SRC)}")
    fm_clean = re.sub(r'^data_updated:[^\n]*(\n|$)', '', fm, flags=re.M)
    fm_clean = re.sub(r'^data_source:[^\n]*(\n|$)', '', fm_clean, flags=re.M)
    new_fm = fm_clean.rstrip('\n') + '\n' + '\n'.join(new_lines)
    new_raw = '---\n' + new_fm + '\n---' + raw[m.end():]
    open(path, "w", encoding="utf-8").write(new_raw)
    done += 1
    print(f"✓ {slug} ({len(new_lines)} fields)")

print(f"done: {done} vehicles")
