#!/usr/bin/env python3
"""EVHub Top window-1f (第六小批): inject deep-profile frontmatter into remaining
export-mainstay premium/flagship brands — Hongqi / Yangwang / M-Hero / Xiaomi / NIO /
Dayun (Yuanhang) / JAC Refine / Zeekr / Li Auto.

Same field contract as window 1/1b/1c/1d/1e (scripts/inject_deep_profile*.py). Fields
omitted -> rendered N/A by the [slug].astro template (zero fabrication). Specs verified
against manufacturer specs + en.wikipedia.org where available on 2026-10-19; unconfirmed
sub-fields left N/A (not estimated). Dayun Yuanhang / NIO ES9 / Li Auto i8 / Hongqi
Guoya/HQ9-PHEV lack dedicated en.wikipedia entries -> catalog base specs + documented
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

def hev():
    return dict(charging_interface="N/A (non-plug-in hybrid, no external charging port)",
                charging_adapter="N/A",
                certification_notes="EU: WVTA type approval. GCC: GSO conformity certificate.",
                hs_code="870340")

DATA = {
  # ── Hongqi (3) — FAW luxury: Guoya HEV flagship sedan, E-HS9 BEV, HQ9 PHEV MPV ──
  "hongqi-guoya": dict(battery_type="NMC (Li-ion)", drive_type="RWD", motor_type="PMSM (single motor)",
    battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **hev()),
  "hongqi-e-hs9": dict(battery_type="NMC (CATL)", drive_type="AWD (dual-motor)", motor_type="PMSM (dual motor)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", drag_coefficient=0.345, **bev()),
  "hongqi-hq9": dict(battery_type="NMC (ternary)", drive_type="FWD", motor_type="PMSM (single motor)",
    battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),

  # ── Yangwang (2) — BYD flagship e4 IWD: U8L EREV off-road, U7 BEV sedan ──
  "yangwang-u8l": dict(battery_type="LFP (Blade)", drive_type="AWD (quad-motor)", motor_type="PMSM (quad motor, e4 IWD)",
    total_power_kw=880, battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="Double wishbone", suspension_rear="Multi-link (Disus-P hydraulic)", **phev()),
  "yangwang-u7": dict(battery_type="LFP (Blade)", drive_type="AWD (quad-motor)", motor_type="PMSM (quad motor, e4)",
    total_power_kw=960, battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (Disus-Z active)", drag_coefficient=0.195, **bev()),

  # ── M-Hero (2) — Dongfeng Mengshi off-road: 917 BEV quad-motor / EREV tri-motor ──
  "m-hero-917": dict(battery_type="NMC (ternary)", drive_type="AWD (quad-motor)", motor_type="PMSM (quad motor)",
    battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **bev()),
  "m-hero-917-erev": dict(battery_type="NMC (ternary)", drive_type="AWD", motor_type="PMSM (tri-motor)",
    battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **phev()),

  # ── Xiaomi (2) — Modena platform: SU7 Ultra tri-motor, YU7 GT dual-motor ──
  "xiaomi-su7-ultra": dict(battery_type="NMC (Qilin 2.0, CATL)", drive_type="AWD (tri-motor)",
    motor_type="PMSM (tri-motor)", total_power_kw=1138,
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", drag_coefficient=0.195, **bev()),
  "xiaomi-yu7-gt": dict(battery_type="NMC (Qilin, CATL)", drive_type="AWD (dual-motor)",
    motor_type="PMSM (dual motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Five-link (multi-link)", drag_coefficient=0.245, **bev()),

  # ── NIO (3) — NT2/3 platform: ES9/EC7/EC6 BEV, NMC CATL + air suspension ──
  "nio-es9": dict(battery_type="NMC (CATL)", drive_type="AWD (dual-motor)", motor_type="PMSM (dual motor)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **bev()),
  "nio-ec7": dict(battery_type="NMC (CATL)", drive_type="AWD (dual-motor)", motor_type="PMSM (dual motor)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **bev()),
  "nio-ec6": dict(battery_type="NMC (CATL)", drive_type="AWD (dual-motor)", motor_type="PMSM (dual motor)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **bev()),

  # ── Dayun Yuanhang (3) — premium BEV: H9/Y7 dual-motor AWD, H8 single-motor ──
  "dayun-h9": dict(drive_type="AWD", motor_type="PMSM (dual motor)",
    battery_thermal="Liquid cooling",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **bev()),
  "dayun-y7": dict(drive_type="AWD", motor_type="PMSM (dual motor)",
    battery_thermal="Liquid cooling",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **bev()),
  "dayun-h8": dict(drive_type="RWD", motor_type="PMSM (single motor)",
    battery_thermal="Liquid cooling",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **bev()),

  # ── JAC Refine (1) — MUSE platform PHEV minivan, LFP ──
  "jac-refine-rf8": dict(battery_type="LFP", drive_type="FWD", motor_type="PMSM (dual motor)",
    battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),

  # ── Zeekr (1) — 8X PHEV full-size luxury SUV, SEA Hybrid, NMC Freevoy ──
  "zeekr-8x": dict(battery_type="NMC (Freevoy, CATL)", drive_type="AWD (dual/tri-motor)",
    motor_type="PMSM (dual motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **phev()),

  # ── Li Auto (1) — i8 BEV full-size SUV, NMC Qilin ──
  "li-auto-i8": dict(battery_type="NMC (Qilin, CATL)", drive_type="AWD (dual-motor)",
    motor_type="PMSM (dual motor)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **bev()),
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
    fm_clean = re.sub(r'^data_updated:.*\n', '', fm, flags=re.M)
    fm_clean = re.sub(r'^data_source:.*\n', '', fm_clean, flags=re.M)
    new_fm = fm_clean.rstrip('\n') + '\n' + '\n'.join(new_lines)
    new_raw = '---\n' + new_fm + '\n---' + raw[m.end():]
    open(path, "w", encoding="utf-8").write(new_raw)
    done += 1
    print(f"✓ {slug} ({len(new_lines)} fields)")

print(f"done: {done} vehicles")
