#!/usr/bin/env python3
"""EVHub Top window-1g (第七小批): inject deep-profile frontmatter into remaining
export-mainstay premium/flagship brands — Denza Z9 series / IM LS9 / Dayun Y6 / GAC
Trumpchi E9 & Xiangwang M8 / Hycan V09 / Lynk & Co 900 / Stelato S9T / M-Hero M817.

Same field contract as window 1..1f (scripts/inject_deep_profile*.py). Fields omitted
-> rendered N/A by the [slug].astro template (zero fabrication). Specs verified against
manufacturer specs + en.wikipedia.org where available on 2026-10-19 (Denza Z9, Stelato
S9, Lynk & Co 900, Trumpchi M8/E9 all have en.wikipedia entries); IM LS9 / Dayun Y6 /
Hycan V09 / M-Hero M817 lack dedicated entries -> catalog base specs + documented
powertrain facts only; chemistry/drive left N/A where unverified.
"""
import re, os

SRC = "EV Hub catalog + manufacturer specs (verified via en.wikipedia.org, 2026-10-19)"
UPDATED = "2026-10-19"

# China ex-factory basis charging / certification facts (by powertrain form).
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
  # ── Denza Z9 series (3) — BYD e3 platform: GT BEV / GT PHEV / Z9 PHEV ──
  "denza-z9-gt": dict(battery_type="LFP (Blade)", drive_type="AWD (tri-motor)",
    motor_type="PMSM (tri-motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **bev()),
  "denza-z9-gt-dm-i": dict(battery_type="LFP (Blade)", drive_type="AWD (tri-motor)",
    motor_type="PMSM (tri-motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **phev()),
  "denza-z9-dm-i": dict(battery_type="LFP (Blade)", drive_type="AWD (tri-motor)",
    motor_type="PMSM (tri-motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **phev()),

  # ── IM LS9 (1) — SAIC IM flagship EREV large SUV, dual-motor AWD ──
  "im-ls9": dict(drive_type="AWD", motor_type="PMSM (dual motor)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **phev()),

  # ── Dayun Yuanhang Y6 (1) — premium BEV sedan, single-motor RWD ──
  "dayun-y6": dict(drive_type="RWD", motor_type="PMSM (single motor)",
    battery_thermal="Liquid cooling",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **bev()),

  # ── GAC Trumpchi E9 (1) — M8-based PHEV MPV, 2.0T + single motor, 2-speed DHT ──
  "gac-motor-e9": dict(drive_type="FWD", motor_type="PMSM (single motor)",
    battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),

  # ── Hycan V09 (1) — GAC-NIO joint BEV MPV, single-motor FWD ──
  "hycan-v09": dict(drive_type="FWD", motor_type="PMSM (single motor)",
    battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),

  # ── Lynk & Co 900 (1) — SPA Evo PHEV full-size luxury SUV, NMC Freevoy ──
  "lynk-co-900": dict(battery_type="NMC (CALB / CATL Freevoy)", drive_type="AWD (dual/tri-motor)",
    motor_type="PMSM (dual/tri-motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", drag_coefficient=0.291, **phev()),

  # ── Stelato S9T (2) — Huawei HIMA / BAIC BE22: BEV wagon + EREV wagon ──
  "stelato-s9t": dict(battery_type="NMC (Whale, CATL)", drive_type="RWD / AWD",
    motor_type="PMSM (rear) / induction (front, AWD)", battery_thermal="Liquid cooling",
    heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", drag_coefficient=0.193, **bev()),
  "stelato-s9t-erev": dict(battery_type="LFP (CATL) / NMC (CATL)", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", drag_coefficient=0.193, **phev()),

  # ── GAC Trumpchi Xiangwang M8 (1) — M8 PHEV MPV ──
  "gac-motor-xiangwang-m8": dict(drive_type="FWD", motor_type="PMSM (single motor)",
    battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),

  # ── M-Hero M817 (1) — Dongfeng Mengshi off-road PHEV ──
  "m-hero-m817": dict(battery_type="NMC (ternary)", drive_type="AWD", motor_type="PMSM (dual motor)",
    battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **phev()),
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
