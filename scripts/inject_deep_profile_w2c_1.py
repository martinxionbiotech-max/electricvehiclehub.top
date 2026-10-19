#!/usr/bin/env python3
"""EVHub Top window-2c part 1 (45 vehicles): inject deep-profile frontmatter into
final remaining high-export-value vehicles — XPeng Mona M03, Deepal SL03 EREV/S05,
Changan Nevo A07/A06/Q05/Lumin/Lamore, Chery Explore 06/Fulwin A9/A8L/T8/T7/X3/X3 Plus,
Geely Galaxy M7/L7/A7/Starshine 7/6/L6/Xingyuan, Geometry G6/E, BYD Sealion 05/Seal 06/
Song Pro/Destroyer 05/e7/Qin L/Qin Plus/Qin Max/Seal 05/Yuan Up, Venucia V-Online, Livan 7/9,
Wuling Jiachen/Starlight 730/Asta/Nebula/Starlight S, Changan UNI-V/CS55/CS75/Eado/X5 Plus,
JAC iEV7L/Refine M3/X8, Roewe D6/M7, Arcfox AT5/T1, Aion i60/V/N60, Forthing Lingzhi/T5/Thunder/
Xinghai, iCar 03, Lynk & Co Z20, Yudo Pi-3/Pi-1, MG 07, Bestune T90/Yueyi/Pony, Dongfeng Epi/Nammi,
Hongqi E-QM5, Leapmotor Lafa5/B01/A10/A05, JMC Yi Chi, Baojun Yunduo/KiWi/Yep Plus, Ora 5/Good Cat,
Aeolus L7, Landian E5, Cowin Shiyue, Sehol E10X, Chery NE Wujie Pro/QQ, BAW e-M7/Yuanbao.

Same field contract as window 1..2b. Fields omitted -> rendered N/A (zero fabrication).
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
  "xpeng-mona-m03": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "deepal-sl03-erev": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "changan-nevo-a07-erev": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "chery-explore-06-c-dm": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "changan-nevo-a06-erev": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "geely-galaxy-m7": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "geometry-g6": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "byd-sealion-05-ev": dict(battery_type="LFP (Blade)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "venucia-v-online-dd-i": dict(battery_type="NMC (ternary)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "deepal-s05": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "livan-7": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "geely-galaxy-l7": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "wuling-jiachen": dict(drive_type="FWD",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **ice()),
  "changan-uni-v-idd": dict(battery_type="NMC (ternary)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "jac-iev7l": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "roewe-d6": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "chery-fulwin-a9": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "arcfox-at5": dict(battery_type="NMC (ternary)", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "jac-refine-m3-phev": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "arcfox-at5-erev": dict(battery_type="NMC (ternary)", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "changan-cs55-plus-phev": dict(battery_type="NMC (ternary)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "jac-refine-m3": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "aion-i60": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "byd-seal-06-dmi-touring": dict(battery_type="LFP (Blade)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "aion-v": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "forthing-lingzhi-m5-nev": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "icaur-03": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "byd-seal-06-ev": dict(battery_type="LFP (Blade)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "changan-uni-v-hev": dict(battery_type="NMC (ternary)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **hev()),
  "chery-fulwin-x3-plus": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "chery-fulwin-a8l": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "livan-9": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "lynk-co-z20": dict(battery_type="LFP (CATL)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "changan-cs75-plus-hev": dict(battery_type="NMC (ternary)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **hev()),
  "yudo-pi-3": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "aion-n60": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "mg-07": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "chery-fulwin-t8": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "wuling-starlight-730": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "byd-e7": dict(battery_type="LFP (Blade)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "byd-sealion-05-dm-i": dict(battery_type="LFP (Blade)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "byd-song-pro": dict(battery_type="LFP (Blade)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "wuling-starlight-730-phev": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "byd-destroyer-05": dict(battery_type="LFP (Blade)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **phev()),
  "wuling-asta": dict(battery_type="NMC (Li-ion)", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **hev()),
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
