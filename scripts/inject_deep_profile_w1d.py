#!/usr/bin/env python3
"""EVHub Top window-1d (第四小批): inject deep-profile frontmatter into remaining export-mainstay
premium brands (Aito / Tank / Voyah / Denza / Fangchengbao / WEY / Jetour / Seres / Haval).

Same field contract as window 1/1b/1c (scripts/inject_deep_profile*.py). Fields omitted ->
rendered N/A by the [slug].astro template (zero fabrication). Specs verified against
manufacturer specs + en.wikipedia.org where available on 2026-10-19; unconfirmed sub-fields
left N/A (not estimated).
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
  # ── Aito / Seres (6) — Huawei HIMA, double wishbone flagship + MacPherson mid-size ──
  "aito-m9": dict(battery_type="NMC (Qilin)", drive_type="AWD", motor_type="PMSM (dual motor)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", drag_coefficient=0.264, **bev()),
  "aito-m9-erev": dict(battery_type="NMC (CATL)", drive_type="AWD", motor_type="PMSM (dual motor)", total_power_kw=365,
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **phev()),
  "aito-m9-ultimate": dict(battery_type="NMC (CATL)", drive_type="AWD", motor_type="PMSM (dual motor)", total_power_kw=365,
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **phev()),
  "aito-m8": dict(battery_type="NMC (CATL)", drive_type="AWD", motor_type="PMSM (dual motor)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **bev()),
  "aito-m8-erev": dict(battery_type="NMC (CATL)", drive_type="AWD", motor_type="PMSM (dual motor)", total_power_kw=365,
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **phev()),
  "aito-m7-erev": dict(battery_type="NMC (CATL)", drive_type="RWD / AWD", motor_type="PMSM (dual motor)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "aito-m5-erev": dict(battery_type="NMC (CATL)", drive_type="RWD / AWD", motor_type="PMSM (dual motor)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "seres-sf5": dict(battery_type="NMC (CATL)", drive_type="RWD / AWD", motor_type="PMSM (dual motor)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),

  # ── Tank (3) — Great Wall body-on-frame Hi4-T PHEV, double wishbone off-road ──
  "tank-700": dict(battery_type="NMC (ternary)", drive_type="AWD", motor_type="PMSM (P2 motor, Hi4-T)", total_power_kw=385,
    battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **phev()),
  "tank-500": dict(battery_type="NMC (ternary)", drive_type="AWD", motor_type="PMSM (P2 motor, Hi4-T)", total_power_kw=300,
    battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **phev()),
  "tank-400": dict(battery_type="NMC (ternary)", drive_type="AWD", motor_type="PMSM (P2 motor, Hi4-T)", total_power_kw=300,
    battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **phev()),

  # ── Voyah (4) — Dongfeng premium, air-suspended large SUV / MPV ──
  "voyah-titan": dict(battery_type="NMC", drive_type="AWD", motor_type="PMSM (dual motor)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **phev()),
  "voyah-dream": dict(battery_type="NMC", drive_type="AWD", motor_type="PMSM (dual motor)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "voyah-dream-phev": dict(battery_type="NMC", drive_type="AWD", motor_type="PMSM (dual motor)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "voyah-free": dict(battery_type="NMC", drive_type="RWD / AWD", motor_type="PMSM (dual motor)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **phev()),

  # ── Fangchengbao (2) — BYD DMO off-road PHEV, LFP Blade ──
  "fangchengbao-bao-8": dict(battery_type="LFP (Blade)", drive_type="AWD", motor_type="PMSM (dual motor, DMO)",
    battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **phev()),
  "fangchengbao-bao-5": dict(battery_type="LFP (Blade)", drive_type="AWD", motor_type="PMSM (dual motor, DMO)",
    battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **phev()),

  # ── Denza (4) — BYD premium, e³ tri-motor sedan + Blade SUV/MPV ──
  "denza-d9-dm-i": dict(battery_type="LFP (Blade)", drive_type="FWD / AWD", motor_type="PMSM (dual motor)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "denza-z9": dict(battery_type="NMC (LFP option)", drive_type="AWD (tri-motor)", motor_type="PMSM (tri-motor, e3)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **bev()),
  "denza-n8l": dict(battery_type="LFP (Blade)", drive_type="AWD", motor_type="PMSM (dual motor)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", **phev()),
  "denza-n7": dict(battery_type="LFP (Blade)", drive_type="RWD / AWD", motor_type="PMSM (dual motor)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (air)", drag_coefficient=0.263, **bev()),

  # ── WEY (2) — Great Wall premium Hi4 PHEV SUV ──
  "wey-lanshan": dict(battery_type="NMC (ternary)", drive_type="AWD", motor_type="PMSM (dual motor, Hi4)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "wey-80": dict(battery_type="NMC (ternary)", drive_type="AWD", motor_type="PMSM (dual motor, Hi4)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),

  # ── Jetour / Haval (2) — off-road flagship + Hi4 PHEV ──
  "jetour-zongheng-g700": dict(battery_type="NMC", drive_type="AWD", motor_type="PMSM (dual motor)",
    battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **phev()),
  "haval-raptor": dict(battery_type="NMC", drive_type="AWD", motor_type="PMSM (dual motor, Hi4)", total_power_kw=220,
    battery_thermal="Liquid cooling", heat_pump="N/A",
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
    fm_clean = re.sub(r'^data_updated:.*\n', '', fm, flags=re.M)
    fm_clean = re.sub(r'^data_source:.*\n', '', fm_clean, flags=re.M)
    new_fm = fm_clean.rstrip('\n') + '\n' + '\n'.join(new_lines)
    new_raw = '---\n' + new_fm + '\n---' + raw[m.end():]
    open(path, "w", encoding="utf-8").write(new_raw)
    done += 1
    print(f"✓ {slug} ({len(new_lines)} fields)")

print(f"done: {done} vehicles")
