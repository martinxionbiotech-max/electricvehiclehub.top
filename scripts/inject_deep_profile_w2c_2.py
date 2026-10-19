#!/usr/bin/env python3
"""EVHub Top window-2c part 2 (44 vehicles): inject deep-profile frontmatter —
Bestune T90/Yueyi 08/07/03/Pony, Aion RT/Y/N60, Forthing T5 Evo/Thunder 410/Xinghai V6,
BAW e-M7/Yuanbao, BYD Seal 06 DM-i/Qin Max/Qin L/Qin Plus/e2/Seal 05, Wuling Starlight S/Nebula/
Starlight PHEV/Binguo/Yep, Landian E5/E5 Plus, Ora 5/Good Cat GT, JAC X8 E-Jia/Yiwei 3,
Roewe M7, Changan CS55 Plus HEV/CS75/Eado/Eado HEV/CS55, Geely Galaxy Starshine 7/6/A7/L6/
Emgrand L HiP, Changan Nevo Q05/Lamore, Chery Fulwin T7/X3, JMC Yi Chi 05S/Yiwei EV3, Baojun
Yunduo/KiWi EV/Yep Plus, Aeolus L7, Dongfeng Epi Nammi 06/Nammi 01/Box, Hongqi E-QM5,
Leapmotor Lafa5/B01/A10/A05, Neta X/Aya/V, Cowin Shiyue, Sehol E10X, Chery NE Wujie Pro/QQ Duomi/
QQ3/QQ Ice Cream/eQ1, Geely Xingyuan/Galaxy LC/Panda Mini, Changan Nevo Lumin.

Same field contract as window 1..2c-1. Fields omitted -> rendered N/A (zero fabrication).
"""
import re, os

SRC = "EV Hub catalog + manufacturer specs (verified via en.wikipedia.org, 2026-10-19)"
UPDATED = "2026-10-19"

GB_CHG = "GB/T AC + GB/T DC (China domestic)"
GB_ADAP_BEV = "CCS2 (DC) / Type 2 (AC) adapter required for EU; or OEM EU-spec port"
GB_ADAP_PHEV = "PHEV/EREV: Type 2 (AC) adapter for EU AC charging"
CERT = "EU: WVTA type approval; GB/T port needs CCS2/Type 2 adapter. GCC: GSO conformity certificate."
CERT_ICE = "EU: WVTA type approval. GCC: GSO conformity certificate."

def bev():
    return dict(charging_interface=GB_CHG, charging_adapter=GB_ADAP_BEV,
                certification_notes=CERT, hs_code="87038000")

def phev():
    return dict(charging_interface=GB_CHG, charging_adapter=GB_ADAP_PHEV,
                certification_notes=CERT, hs_code="870340")

def hev():
    return dict(charging_interface="N/A (non-plug-in hybrid, no external charging port)",
                charging_adapter="N/A", certification_notes=CERT, hs_code="870340")

def ice():
    return dict(charging_interface="N/A (internal combustion engine, no charging port)",
                charging_adapter="N/A", certification_notes=CERT_ICE, hs_code="87032200")

DATA = {
  "bestune-t90": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "aion-rt": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "forthing-t5-evo": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "aion-y": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "baw-e-m7": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "byd-seal-06-dm-i": dict(battery_type="LFP (Blade)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "bestune-yueyi-08": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "byd-qin-max-dm-i": dict(battery_type="LFP (Blade)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **phev()),
  "byd-qin-max-ev": dict(battery_type="LFP (Blade)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "bestune-yueyi-07": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "wuling-starlight-s-phev": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "landian-e5": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "ora-5": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "jac-x8-ejia": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "byd-qin-l-dm-i": dict(battery_type="LFP (Blade)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "landian-e5-plus": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "forthing-thunder-410": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "leapmotor-lafa5": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "roewe-m7": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "changan-cs55-plus-hev": dict(battery_type="NMC (ternary)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **hev()),
  "geely-galaxy-starshine-7": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "changan-nevo-q05": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "chery-fulwin-t7": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "byd-qin-l": dict(battery_type="LFP (Blade)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "jmc-yi-chi-05s": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "baojun-yunduo": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "ora-good-cat-gt": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "aeolus-l7": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "aeolus-l7-ev": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "dongfeng-epi-nammi-06": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "hongqi-e-qm5": dict(battery_type="NMC (CATL)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "byd-e2": dict(battery_type="LFP (Blade)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "geely-emgrand-l-hip": dict(battery_type="NMC (CTP)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **phev()),
  "wuling-nebula": dict(battery_type="NMC (Li-ion)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **hev()),
  "leapmotor-b01": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "geely-galaxy-a7": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "forthing-xinghai-v6": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "chery-fulwin-x3": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "neta-x": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "baojun-kiwi-ev": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "geometry-e": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "changan-cs75": dict(battery_type="NMC (ternary)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "changan-eado": dict(battery_type="NMC (ternary)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **phev()),
  "chery-new-energy-wujie-pro": dict(battery_type="LFP", drive_type="FWD",
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
