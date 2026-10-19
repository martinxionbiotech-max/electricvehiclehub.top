#!/usr/bin/env python3
"""EVHub Top window-1e (第五小批): inject deep-profile frontmatter into remaining
export-mainstay volume/NEV brands — Haval (remaining) / Wuling / Baojun NEV / GAC Trumpchi /
SAIC Roewe / Maxus / Chery Fulwin / ORA.

Same field contract as window 1/1b/1c/1d (scripts/inject_deep_profile*.py). Fields omitted ->
rendered N/A by the [slug].astro template (zero fabrication). Specs verified against
manufacturer specs + en.wikipedia.org on 2026-10-19; unconfirmed sub-fields left N/A
(not estimated). Battery chemistry / drive layout / motor architecture only where sourced;
suspension only for mainstream platforms where axle layout is documented.
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
  # ── Haval (4) — Great Wall Hi4 / DHT, NMC ternary, MacPherson + multi-link ──
  "haval-big-dog-plus": dict(battery_type="NMC (ternary)", drive_type="AWD",
    motor_type="PMSM (dual motor, Hi4)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "haval-shenshou": dict(battery_type="NMC (Li-ion)", drive_type="FWD",
    motor_type="PMSM (DHT hybrid)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **hev()),
  "haval-xiaolong-max": dict(battery_type="NMC", drive_type="AWD",
    motor_type="PMSM (dual motor, Hi4)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "haval-xiaolong": dict(battery_type="NMC", drive_type="FWD",
    motor_type="PMSM (single motor, DHT)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),

  # ── Wuling (4) — SGMW LFP, FWD/RWD single-motor ──
  "wuling-starlight": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", **bev()),
  "wuling-starlight-s": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", **bev()),
  "wuling-binguo": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", **bev()),
  "wuling-hongguang-bev": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", **bev()),

  # ── Baojun (3) — SGMW LFP ──
  "baojun-yunhai": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", **bev()),
  "baojun-xiangjing": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", **bev()),
  "baojun-yep": dict(battery_type="LFP", drive_type="RWD",
    motor_type="PMSM (single motor)", **bev()),

  # ── GAC Trumpchi (3) — NMC PHEV MPV/SUV ──
  "gac-motor-m8": dict(battery_type="NMC", drive_type="FWD",
    motor_type="PMSM (single motor, DHT)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "gac-motor-e8": dict(battery_type="NMC", drive_type="FWD",
    motor_type="PMSM (single motor, DHT)", battery_thermal="Liquid cooling", **phev()),
  "gac-motor-xiangwang-s7": dict(battery_type="NMC", drive_type="FWD / AWD",
    motor_type="PMSM (DHT hybrid)", battery_thermal="Liquid cooling", **phev()),

  # ── SAIC Roewe (2) — D7 sedan (BEV RWD / PHEV FWD) ──
  "roewe-d7": dict(battery_type="LFP (NMC option)", drive_type="RWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "roewe-d7-phev": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor, DMH)", battery_thermal="Liquid cooling",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),

  # ── SAIC Maxus (2) — MIFA electric MPV, NMC FWD ──
  "maxus-mifa-7": dict(battery_type="NMC", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", **bev()),
  "maxus-mifa-9": dict(battery_type="NMC", drive_type="FWD",
    motor_type="PMSM (single motor)", battery_thermal="Liquid cooling", **bev()),

  # ── Chery Fulwin / ORA (2) ──
  "chery-fulwin-a8": dict(battery_type="LFP", drive_type="FWD",
    motor_type="PMSM (single motor, DHT)", battery_thermal="Liquid cooling", **phev()),
  "ora-lightning-cat": dict(battery_type="NMC (ternary)", drive_type="FWD / AWD",
    motor_type="PMSM (single motor FWD / dual motor AWD)", battery_thermal="Liquid cooling",
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
    fm_clean = re.sub(r'^data_updated:.*\n', '', fm, flags=re.M)
    fm_clean = re.sub(r'^data_source:.*\n', '', fm_clean, flags=re.M)
    new_fm = fm_clean.rstrip('\n') + '\n' + '\n'.join(new_lines)
    new_raw = '---\n' + new_fm + '\n---' + raw[m.end():]
    open(path, "w", encoding="utf-8").write(new_raw)
    done += 1
    print(f"✓ {slug} ({len(new_lines)} fields)")

print(f"done: {done} vehicles")
