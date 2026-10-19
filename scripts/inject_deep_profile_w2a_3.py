#!/usr/bin/env python3
"""EVHub Top window-2a part 3 (33 vehicles): inject deep-profile frontmatter into
remaining export-mainstay high-value vehicles — Hongqi H5 PHEV, Geely Galaxy M9, Forthing
Xinghai V9, BYD Frigate 07, Fangchengbao Ti-7, Hongqi E-HS5/HS6 PHEV/Tiangong 06, Hycan
A06, JAC Refine E4/E3/iEVA60, Lynk & Co 08/10, Geometry A, Changan CS75 Plus iDD,
Dongfeng Epi 008/M8, BYD D1/Sealion 07 DM-i/Qin/Han DM-i, BAW M8(+EREV), iCar V27, Jetour
X90/Shanhai L9/X90 C-DM, MG Pilot PHEV, Oshan Keshan EV, Roewe F7, GAC GS7, Hongqi EH5.

Same field contract as window 1..1h. Fields omitted -> rendered N/A (zero fabrication).
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

DATA = {
  "hongqi-h5-phev": dict(battery_type="NMC (CATL)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "geely-galaxy-m9": dict(battery_type="LFP", drive_type="AWD (dual motor)",
    motor_type="PMSM (dual motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "forthing-xinghai-v9": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "byd-frigate-07": dict(battery_type="LFP (Blade)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "fangchengbao-ti-7": dict(battery_type="LFP (Blade)", drive_type="AWD (dual motor)",
    motor_type="PMSM (dual motor)", battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **phev()),
  "hongqi-e-hs5": dict(battery_type="NMC (CATL)", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "hongqi-hs6-phev": dict(battery_type="NMC (CATL)", drive_type="AWD (dual motor)",
    motor_type="PMSM (dual motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "hongqi-tiangong-06": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "hycan-a06": dict(battery_type="NMC (ternary)", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "jac-refine-e4": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "jac-ieva60": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "lynk-co-08": dict(battery_type="LFP (CATL)", drive_type="AWD (dual motor)",
    motor_type="PMSM (dual motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "lynk-co-10": dict(battery_type="LFP (CATL)", drive_type="AWD (dual motor)",
    motor_type="PMSM (dual motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "geometry-a": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "changan-cs75-plus-idd": dict(battery_type="NMC (ternary)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "dongfeng-epi-008": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "byd-d1": dict(battery_type="LFP (Blade)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "byd-sealion-07-dm-i": dict(battery_type="LFP (Blade)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "byd-qin": dict(battery_type="LFP (Blade)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "baw-m8-erev": dict(battery_type="LFP", drive_type="AWD (dual motor)",
    motor_type="PMSM (dual motor)", battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **phev()),
  "dongfeng-epi-m8": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "icaur-v27": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "jac-refine-e3": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "jetour-x90": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "jetour-shanhai-l9": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "mg-pilot-phev": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "oshan-keshan-ev": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "byd-han-dm-i": dict(battery_type="LFP (Blade)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "roewe-f7": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "jetour-x90-c-dm": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "baw-m8": dict(battery_type="LFP", drive_type="AWD (dual motor)",
    motor_type="PMSM (dual motor)", battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **bev()),
  "gac-motor-gs7": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "hongqi-eh5": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
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
