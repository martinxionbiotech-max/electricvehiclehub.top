#!/usr/bin/env python3
"""Inject EVHub Top deep-profile frontmatter fields into pilot-batch vehicle .md files."""
import re, json, os

SRC = "EV Hub catalog + manufacturer specs (verified via en.wikipedia.org, 2026-10-19)"
UPDATED = "2026-10-19"

# Common charging / certification facts (China ex-factory basis).
GB_CHG = "GB/T AC + GB/T DC (China domestic)"
GB_ADAP = "CCS2 (DC) / Type 2 (AC) adapter required for EU; or OEM EU-spec port"
CERT_EU_GCC = "EU: WVTA type approval; GB/T port needs CCS2/Type 2 adapter. GCC: GSO conformity certificate."

# Deep-profile fields per pilot vehicle. None -> omitted (renders N/A in template).
DATA = {
  "byd-atto-3": dict(battery_type="LFP (Blade)", drive_type="FWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes (export spec)", suspension_front="MacPherson strut",
    suspension_rear="Multi-link", range_wltp_km=345, drag_coefficient=0.29,
    charging_interface=GB_CHG, charging_adapter=GB_ADAP, certification_notes=CERT_EU_GCC),
  "byd-seal": dict(battery_type="LFP (Blade)", drive_type="RWD / AWD", motor_type="PMSM (rear) + induction (front, AWD)",
    battery_thermal="Liquid cooling", heat_pump="Yes (export spec)", suspension_front="Double wishbone",
    suspension_rear="Five-link", range_wltp_km=460, drag_coefficient=0.219,
    charging_interface=GB_CHG, charging_adapter=GB_ADAP, certification_notes=CERT_EU_GCC),
  "byd-dolphin": dict(battery_type="LFP (Blade)", drive_type="FWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes (export spec)", suspension_front="MacPherson strut",
    suspension_rear="Torsion beam", range_wltp_km=340,
    charging_interface=GB_CHG, charging_adapter=GB_ADAP, certification_notes=CERT_EU_GCC),
  "byd-seagull": dict(battery_type="LFP (Blade)", drive_type="FWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="N/A", suspension_front="MacPherson strut",
    suspension_rear="Torsion beam", range_wltp_km=225,
    charging_interface=GB_CHG, charging_adapter=GB_ADAP, certification_notes=CERT_EU_GCC),
  "byd-han": dict(battery_type="LFP (Blade)", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes", suspension_front="MacPherson strut",
    suspension_rear="Multi-link", range_wltp_km=521, drag_coefficient=0.233,
    charging_interface=GB_CHG, charging_adapter=GB_ADAP, certification_notes=CERT_EU_GCC),
  "byd-sealion-07": dict(battery_type="LFP (Blade)", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes", suspension_front="Double wishbone",
    suspension_rear="Five-link", range_wltp_km=482,
    charging_interface=GB_CHG, charging_adapter=GB_ADAP, certification_notes=CERT_EU_GCC),
  "byd-song-plus": dict(battery_type="LFP (Blade)", drive_type="FWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes", suspension_front="MacPherson strut",
    suspension_rear="Multi-link",
    charging_interface=GB_CHG, charging_adapter=GB_ADAP, certification_notes=CERT_EU_GCC),
  "geely-galaxy-e5": dict(battery_type="LFP", drive_type="FWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes", suspension_front="MacPherson strut",
    suspension_rear="Multi-link",
    charging_interface=GB_CHG, charging_adapter=GB_ADAP, certification_notes=CERT_EU_GCC),
  "geely-galaxy-e8": dict(battery_type="LFP / NMC", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes", suspension_front="Double wishbone",
    suspension_rear="Five-link", drag_coefficient=0.199,
    charging_interface=GB_CHG, charging_adapter=GB_ADAP, certification_notes=CERT_EU_GCC),
  "geely-galaxy-starship-7": dict(battery_type="LFP", drive_type="FWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes", suspension_front="MacPherson strut",
    suspension_rear="Multi-link",
    charging_interface=GB_CHG, charging_adapter="PHEV: Type 2 (AC) adapter for EU AC charging", certification_notes=CERT_EU_GCC),
  "mg-4": dict(battery_type="LFP", drive_type="RWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes (LR trim)", suspension_front="MacPherson strut",
    suspension_rear="Five-link", range_wltp_km=350, drag_coefficient=0.28,
    charging_interface="CCS2 (DC) + Type 2 (AC) — EU export spec; GB/T (China)",
    charging_adapter="EU-spec CCS2 native; no adapter required in EU", certification_notes=CERT_EU_GCC),
  "mg-s5-ev": dict(battery_type="LFP", drive_type="FWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="N/A", suspension_front="MacPherson strut",
    suspension_rear="Multi-link",
    charging_interface=GB_CHG, charging_adapter=GB_ADAP, certification_notes=CERT_EU_GCC),
  "zeekr-001": dict(battery_type="NMC", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes", suspension_front="Double wishbone",
    suspension_rear="Multi-link", range_wltp_km=620, drag_coefficient=0.23,
    charging_interface=GB_CHG, charging_adapter=GB_ADAP, certification_notes=CERT_EU_GCC),
  "xpeng-g6": dict(battery_type="LFP / NMC (CALB)", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes", suspension_front="Double wishbone",
    suspension_rear="Five-link", range_wltp_km=570, drag_coefficient=0.248,
    charging_interface=GB_CHG, charging_adapter=GB_ADAP, certification_notes=CERT_EU_GCC),
  "aion-y-plus": dict(battery_type="LFP", drive_type="FWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="N/A", suspension_front="MacPherson strut",
    suspension_rear="Torsion beam",
    charging_interface=GB_CHG, charging_adapter=GB_ADAP, certification_notes=CERT_EU_GCC),
  "aion-v-plus": dict(battery_type="LFP", drive_type="FWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="N/A", suspension_front="MacPherson strut",
    suspension_rear="Torsion beam",
    charging_interface=GB_CHG, charging_adapter=GB_ADAP, certification_notes=CERT_EU_GCC),
  "wuling-hongguang-mini-ev": dict(battery_type="LFP", drive_type="RWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="N/A", heat_pump="No", suspension_front="MacPherson strut",
    suspension_rear="Torsion beam",
    charging_interface="GB/T AC (China domestic, slow charge)",
    charging_adapter="Type 2 (AC) adapter for EU slow charging", certification_notes=CERT_EU_GCC),
  "chery-tiggo-7-c-dm": dict(battery_type="LFP", drive_type="FWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="N/A", suspension_front="MacPherson strut",
    suspension_rear="Multi-link",
    charging_interface=GB_CHG, charging_adapter="PHEV: Type 2 (AC) adapter for EU AC charging", certification_notes=CERT_EU_GCC),
  "chery-tiggo-8-plus-c-dm": dict(battery_type="LFP", drive_type="FWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="N/A", suspension_front="MacPherson strut",
    suspension_rear="Multi-link",
    charging_interface=GB_CHG, charging_adapter="PHEV: Type 2 (AC) adapter for EU AC charging", certification_notes=CERT_EU_GCC),
  "haval-h6": dict(battery_type="LFP / NMC", drive_type="FWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="N/A", suspension_front="MacPherson strut",
    suspension_rear="Multi-link",
    charging_interface=GB_CHG, charging_adapter="PHEV: Type 2 (AC) adapter for EU AC charging", certification_notes=CERT_EU_GCC),
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
    # Build new field lines (skip None, skip keys already present)
    new_lines = []
    for k in FIELDS_ORDER:
        if k not in fields:
            continue
        v = fields[k]
        yv = yaml_val(v)
        if yv is None:
            continue
        # skip if key already present in frontmatter
        if re.search(rf'^{re.escape(k)}:', fm, re.M):
            continue
        new_lines.append(f"{k}: {yv}")
    # Update data_updated and data_source
    new_lines.append(f"data_updated: {yaml_str(UPDATED)}")
    new_lines.append(f"data_source: {yaml_str(SRC)}")
    # Remove existing data_updated/data_source lines to avoid duplicates
    fm_clean = re.sub(r'^data_updated:.*\n', '', fm, flags=re.M)
    fm_clean = re.sub(r'^data_source:.*\n', '', fm_clean, flags=re.M)
    new_fm = fm_clean.rstrip('\n') + '\n' + '\n'.join(new_lines)
    new_raw = '---\n' + new_fm + '\n---' + raw[m.end():]
    open(path, "w", encoding="utf-8").write(new_raw)
    print(f"✓ {slug} ({len(new_lines)} fields)")

print("done")
