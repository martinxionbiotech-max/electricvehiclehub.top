#!/usr/bin/env python3
"""EVHub Top window-2a part 1 (34 vehicles): inject deep-profile frontmatter into
remaining export-mainstay high-value vehicles — Aito M7/M5/M6, XPeng GX, Lynk & Co 09,
Avatr 12/07L, Hyptec HL, Maxus MIFA 9 PHEV, Xiaomi Skynomad N90, Geely Galaxy V900,
Onvo L90, Roewe i6 Max, Hycan 007, Voyah Passion, Li Auto i6, Luxeed R7/S7, IM LS8,
Leapmotor D99, Deepal S09, Onvo L80, WEY 05/03, GAC Xiangwang S9/ES9/GS8, BYD M9/Tang L,
Avatr 07L, Aito M6, BYD Tang L DM-i.

Same field contract as window 1..1h (scripts/inject_deep_profile*.py). Fields omitted
-> rendered N/A by the [slug].astro template (zero fabrication). Battery chemistry follows
the established brand conventions (Aito/Seres=NMC CATL, Avatr=NMC CATL, Xiaomi=NMC Qilin,
Voyah/IM/Luxeed/Li=NMC CATL, BYD=LFP Blade, Deepal=LFP, Leapmotor=LFP, Onvo=LFP); uncertain
chemistry/thermal sub-fields left N/A.
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
                charging_adapter="N/A",
                certification_notes="EU: WVTA type approval; GCC: GSO conformity certificate.",
                hs_code="870340")

DATA = {
  "aito-m7": dict(battery_type="NMC (CATL)", drive_type="AWD (dual motor)",
    motor_type="PMSM (dual motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "xpeng-gx": dict(battery_type="NMC (CATL)", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **phev()),
  "lynk-co-09": dict(battery_type="NMC (CATL)", drive_type="AWD (dual motor)",
    motor_type="PMSM (dual motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "avatr-12": dict(battery_type="NMC (CATL)", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **bev()),
  "hyptec-hl": dict(battery_type="NMC (ternary)", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "avatr-12-erev": dict(battery_type="NMC (CATL)", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **phev()),
  "maxus-mifa-9-phev": dict(battery_type="NMC (ternary)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "xiaomi-skynomad-n90": dict(battery_type="NMC (Qilin, CATL)", drive_type="AWD (dual motor)",
    motor_type="PMSM (dual motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **phev()),
  "geely-galaxy-v900": dict(battery_type="NMC (CATL)", drive_type="AWD (dual motor)",
    motor_type="PMSM (dual motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "hyptec-hl-erev": dict(battery_type="NMC (ternary)", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "onvo-l90": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "roewe-i6-max": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "hycan-007": dict(battery_type="NMC (ternary)", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "voyah-passion": dict(battery_type="NMC (CATL)", drive_type="AWD (dual motor)",
    motor_type="PMSM (dual motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **bev()),
  "li-auto-i6": dict(battery_type="NMC (CATL)", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **bev()),
  "luxeed-r7": dict(battery_type="NMC (CATL)", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **bev()),
  "voyah-passion-phev": dict(battery_type="NMC (CATL)", drive_type="AWD (dual motor)",
    motor_type="PMSM (dual motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **phev()),
  "im-ls8": dict(battery_type="NMC (CATL)", drive_type="AWD (dual motor)",
    motor_type="PMSM (dual motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **phev()),
  "leapmotor-d99": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "deepal-s09": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "onvo-l80": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "wey-05": dict(battery_type="NMC (CATL)", drive_type="AWD (dual motor)",
    motor_type="PMSM (dual motor)", battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "gac-motor-xiangwang-s9": dict(battery_type="NMC (ternary)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "aito-m5": dict(battery_type="NMC (CATL)", drive_type="AWD (dual motor)",
    motor_type="PMSM (dual motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "byd-m9": dict(battery_type="LFP (Blade)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "byd-tang-l": dict(battery_type="LFP (Blade)", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "gac-motor-es9": dict(battery_type="NMC (ternary)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "luxeed-s7": dict(battery_type="NMC (CATL)", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **bev()),
  "lynk-co-z10": dict(battery_type="NMC (CATL)", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "wey-03": dict(battery_type="NMC (CATL)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "gac-motor-gs8": dict(drive_type="FWD", motor_type="PMSM (THS hybrid system)",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **hev()),
  "avatr-07l": dict(battery_type="NMC (CATL)", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **bev()),
  "aito-m6": dict(battery_type="NMC (CATL)", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "byd-tang-l-dm-i": dict(battery_type="LFP (Blade)", drive_type="FWD",
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
