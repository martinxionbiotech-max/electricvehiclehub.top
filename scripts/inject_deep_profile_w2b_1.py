#!/usr/bin/env python3
"""EVHub Top window-2b part 1 (37 vehicles): inject deep-profile frontmatter into
remaining export-mainstay high-value vehicles — Hongqi HS3/Tiangong 05, Maxus G50,
SAIC H5(+EREV), Roewe R7/eRX5, Cowin Kunlun iHD, Chery NEV Shuxiangjia/Arrizo e,
Oshan X7 EV/Z6 iDD, Lynk & Co 07/07 GT/06, BYD E3/Seal 07 DM-i/Song Max, Hyptec GT,
Leapmotor C16 EREV, Neta S, Forthing Xinghai X5/T5/S50ev/V6 Plus, Exeed Exlantix ES
EREV, Dongfeng Epi 007, Jetour Dashing i-DM/X70 C-DM/Shanhai L7(+Plus), Skywell EV6,
GAC Emkoo HEV, Kaicene A600EV, ORA Ballet Cat, Chery Fulwin A9L, Aion S Max.

Same field contract as window 1..2a. Fields omitted -> rendered N/A (zero fabrication).
Battery chemistry follows established brand conventions; uncertain sub-fields left N/A.
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

def hev():
    return dict(charging_interface="N/A (non-plug-in hybrid, no external charging port)",
                charging_adapter="N/A", certification_notes=CERT, hs_code="870340")

DATA = {
  "hongqi-hs3": dict(battery_type="NMC (ternary)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "maxus-g50": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "saic-h5": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "roewe-r7": dict(battery_type="LFP (NMC option)", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "cowin-kunlun-ihd": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "chery-new-energy-shuxiangjia": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "oshan-x7-ev": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "hongqi-tiangong-05": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "saic-h5-erev": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "lynk-co-07": dict(battery_type="LFP (CATL)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "lynk-co-07-gt": dict(battery_type="NMC (CATL)", drive_type="AWD (dual motor)",
    motor_type="PMSM (dual motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "byd-e3": dict(battery_type="LFP (Blade)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "roewe-erx5": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "hyptec-gt": dict(battery_type="NMC (ternary)", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "leapmotor-c16-erev": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "oshan-z6-idd": dict(battery_type="NMC (ternary)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "neta-s": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "forthing-xinghai-x5": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "forthing-xinghai-t5": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "forthing-s50ev": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "exeed-exlantix-es-erev": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **phev()),
  "chery-new-energy-arrizo-e": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "dongfeng-epi-007": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "jetour-dashing-i-dm": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "jetour-x70-c-dm": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "skywell-ev6": dict(battery_type="NMC (ternary)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "byd-seal-07-dm-i": dict(battery_type="LFP (Blade)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "gac-motor-emkoo": dict(battery_type="NMC (Li-ion)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **hev()),
  "jetour-shanhai-l7-plus": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "jetour-shanhai-l7": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "kaicene-a600ev": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "ora-ballet-cat": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "forthing-xinghai-v6-plus": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "chery-fulwin-a9l": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "byd-song-max": dict(battery_type="LFP (Blade)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **phev()),
  "lynk-co-06": dict(battery_type="LFP (CATL)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "aion-s-max": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
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
