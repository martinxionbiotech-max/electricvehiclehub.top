#!/usr/bin/env python3
"""EVHub Top window-2b part 2 (37 vehicles): inject deep-profile frontmatter into
remaining export-mainstay high-value vehicles — Deepal S07 EREV/L07, Cowin Xuandu EV,
JAC iC5, Leapmotor C11 EREV/C01 EREV, Geometry M6, Geely Emgrand EV, Changan Nevo Q06,
Exeed TXL/ET5/RX C-DM/LX C-DM, Skywell HT-i, BYD Sealion 06/Song L DM-i, Aeolus E70/Huge,
Aion S, Bestune NAT, Geely Galaxy TT, Sehol Aipao, iCar 03T, Venucia D60EV, Landian E5
Plus Gen3/E3, JAC iEVA50/iEVS4, BYD Seal 06 GT, Leapmotor C01, Chery Tiggo 8 Pro NE,
Livan 8, Deepal L06.

Same field contract as window 1..2a. Fields omitted -> rendered N/A (zero fabrication).
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
  "deepal-s07-erev": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "cowin-xuandu-ev": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "jac-ic5": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "leapmotor-c11-erev": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **phev()),
  "geometry-m6": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "geely-emgrand-ev": dict(battery_type="NMC (CTP)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "deepal-l07": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "changan-nevo-q06": dict(battery_type="LFP", drive_type="AWD (dual motor)",
    motor_type="PMSM (dual motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "exeed-txl": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **phev()),
  "skywell-ht-i": dict(battery_type="NMC (ternary)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "byd-sealion-06": dict(battery_type="LFP (Blade)", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "leapmotor-c01-erev": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="Double wishbone", suspension_rear="Five-link", **phev()),
  "exeed-et5": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **phev()),
  "aeolus-e70": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "aeolus-huge": dict(battery_type="NMC (Li-ion)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **hev()),
  "exeed-rx-c-dm": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "aion-s": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "bestune-nat": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "byd-song-l-dmi": dict(battery_type="LFP (Blade)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "exeed-lx-c-dm": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "geely-galaxy-tt": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "sehol-aipao": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "icaur-03t": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "venucia-d60ev": dict(battery_type="NMC (ternary)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "landian-e5-plus-gen3": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "landian-e3": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "jac-ieva50": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "jac-ievs4": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "byd-seal-06-gt": dict(battery_type="LFP (Blade)", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "leapmotor-c01": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="Double wishbone", suspension_rear="Five-link", **bev()),
  "chery-tiggo-8-pro-new-energy": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "livan-8": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "deepal-l06": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "jetour-t1": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "roewe-i6-max-phev": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **phev()),
  "deepal-l07-erev": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "byd-song-plus-dm-i": dict(battery_type="LFP (Blade)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
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
