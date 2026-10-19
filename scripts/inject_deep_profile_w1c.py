#!/usr/bin/env python3
"""EVHub Top window-1c (第三小批): inject deep-profile frontmatter into high-export-value
new-energy/premium vehicles (Zeekr / XPeng / NIO / Li Auto / IM / Leapmotor / Arcfox / Exeed /
Huawei premium + low landed-cost-premium pool vehicles).

Same field contract as window 1/1b (scripts/inject_deep_profile*.py). Fields omitted ->
rendered N/A by the [slug].astro template (zero fabrication). Specs verified against
en.wikipedia.org + manufacturer specs on 2026-10-19.
"""
import re, os

SRC = "EV Hub catalog + manufacturer specs (verified via en.wikipedia.org, 2026-10-19)"
UPDATED = "2026-10-19"

# China ex-factory basis charging / certification facts.
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
  # ── Zeekr (5) ──
  "zeekr-009": dict(battery_type="NMC (Qilin)", drive_type="RWD / AWD", motor_type="PMSM (dual motor, AWD)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", drag_coefficient=0.27, **bev()),
  "zeekr-007": dict(battery_type="LFP (Golden) / NMC", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link", drag_coefficient=0.219, **bev()),
  "zeekr-007-gt": dict(battery_type="LFP / NMC", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link", drag_coefficient=0.219, **bev()),
  "zeekr-mix": dict(battery_type="LFP / NMC", drive_type="RWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", drag_coefficient=0.229, **bev()),
  "zeekr-9x": dict(battery_type="LFP", drive_type="AWD", motor_type="PMSM (dual motor)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **phev()),

  # ── XPeng (4) ──
  "xpeng-x9": dict(battery_type="LFP / NMC", drive_type="RWD / AWD", motor_type="PMSM (dual motor, AWD)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **bev()),
  "xpeng-p7": dict(battery_type="LFP / NMC", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link", drag_coefficient=0.236, **bev()),
  "xpeng-g7": dict(battery_type="LFP", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **bev()),
  "xpeng-g9l": dict(battery_type="LFP / NMC", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link", drag_coefficient=0.272, **bev()),

  # ── NIO (5) ──
  "nio-et9": dict(battery_type="NMC (900V)", drive_type="AWD", motor_type="PMSM (dual motor)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air, SkyRide)", **bev()),
  "nio-es8": dict(battery_type="NMC", drive_type="AWD", motor_type="PMSM + AC induction (dual motor)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **bev()),
  "nio-et7": dict(battery_type="NMC", drive_type="AWD", motor_type="PMSM + AC induction (dual motor)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **bev()),
  "nio-et5": dict(battery_type="NMC / LFP", drive_type="AWD", motor_type="PMSM + AC induction (dual motor)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **bev()),
  "nio-es7": dict(battery_type="NMC", drive_type="AWD", motor_type="PMSM + AC induction (dual motor)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **bev()),

  # ── Li Auto (4) ──
  "li-auto-mega": dict(battery_type="NMC (Qilin)", drive_type="AWD", motor_type="PMSM (dual motor)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **bev()),
  "li-auto-l9": dict(battery_type="LFP", drive_type="AWD", motor_type="PMSM (dual motor)", total_power_kw=330,
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **phev()),
  "li-auto-l8": dict(battery_type="LFP", drive_type="AWD", motor_type="PMSM (dual motor)", total_power_kw=330,
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **phev()),
  "li-auto-l7": dict(battery_type="LFP", drive_type="AWD", motor_type="PMSM (dual motor)", total_power_kw=330,
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **phev()),

  # ── IM (3) ──
  "im-ls7": dict(battery_type="NMC / LFP", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **bev()),
  "im-l7": dict(battery_type="NMC", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **bev()),
  "im-l6": dict(battery_type="LFP / NMC", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **bev()),

  # ── Leapmotor (4) ──
  "leapmotor-c16": dict(battery_type="LFP", drive_type="RWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "leapmotor-c11": dict(battery_type="LFP / NMC", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Five-link", **bev()),
  "leapmotor-b10": dict(battery_type="LFP", drive_type="RWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "leapmotor-t03": dict(battery_type="LFP", drive_type="FWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="No",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),

  # ── Arcfox (3) ──
  "arcfox-as": dict(battery_type="NMC", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "arcfox-at": dict(battery_type="NMC", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "arcfox-kaola": dict(battery_type="LFP", drive_type="FWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),

  # ── Exeed (2) ──
  "exeed-exlantix-es": dict(battery_type="LFP / NMC", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **bev()),
  "exeed-exlantix-et-erev": dict(battery_type="LFP", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **phev()),

  # ── Premium / Huawei + high-value (7) ──
  "yangwang-u8": dict(battery_type="LFP (Blade)", drive_type="AWD (quad motor)", motor_type="PMSM (four independent motors)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone (hydraulic, DiSus-P)", suspension_rear="Multi-link (hydraulic, DiSus-P)", **phev()),
  "maextro-s800": dict(battery_type="NMC", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **bev()),
  "stelato-s9": dict(battery_type="LFP / NMC", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **bev()),
  "xiaomi-yu7": dict(battery_type="LFP / NMC", drive_type="RWD / AWD", motor_type="PMSM (HyperEngine V6/V6s)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Five-link", drag_coefficient=0.195, **bev()),
  "denza-n9": dict(battery_type="NMC (LFP option)", drive_type="AWD", motor_type="PMSM (dual motor)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **bev()),
  "avatr-11": dict(battery_type="NMC", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **bev()),
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
