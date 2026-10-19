#!/usr/bin/env python3
"""EVHub Top window-1b (续批): inject deep-profile frontmatter into 32 export-mainstay vehicles.

Same field contract as window 1 (scripts/inject_deep_profile.py). Fields omitted ->
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
    return dict(charging_interface=GB_CHG, charging_adapter=GB_ADAP_BEV, certification_notes=CERT)

def phev():
    return dict(charging_interface=GB_CHG, charging_adapter=GB_ADAP_PHEV, certification_notes=CERT)

DATA = {
  # ── BYD (5) ──
  "byd-atto-2": dict(battery_type="LFP (Blade)", drive_type="FWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes (export spec)",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "byd-tang": dict(battery_type="LFP (Blade)", drive_type="FWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "byd-sealion-06-dmi": dict(battery_type="LFP (Blade)", drive_type="FWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "byd-song-l-ev": dict(battery_type="LFP (Blade)", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Five-link", drag_coefficient=0.255, **bev()),
  "byd-han-l": dict(battery_type="LFP (Blade)", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Five-link", **bev()),

  # ── Geely (2) ──
  "geely-monjaro": dict(battery_type="NMC (CTP)", drive_type="FWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "geely-galaxy-starship-7-ev": dict(battery_type="LFP (Aegis Short Blade)", drive_type="FWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),

  # ── Chery group (4) ──
  "chery-tiggo-9": dict(battery_type="LFP / NMC", drive_type="FWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "exeed-exlantix-et": dict(battery_type="LFP (Shenxing 2.0) / NMC (Qilin)", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **bev()),
  "jetour-t2": dict(battery_type="LFP", drive_type="FWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),
  "jaecoo-j7": dict(battery_type="LFP", drive_type="FWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),

  # ── GAC (2) ──
  "aion-s-plus": dict(battery_type="LFP / NMC", drive_type="FWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),
  "hyptec-ht": dict(battery_type="NMC / LFP", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),

  # ── MG (2) ──
  "mg-4x": dict(battery_type="LFP", drive_type="FWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", trunk_l=471, **bev()),
  "mg6-phev": dict(battery_type="NMC", drive_type="FWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **phev()),

  # ── Great Wall (3) ──
  "haval-jolion-pro": dict(battery_type="NMC", drive_type="FWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam",
    charging_interface="N/A (non-plug-in HEV)", certification_notes=CERT),
  "tank-300": dict(battery_type="LFP", drive_type="AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **phev()),
  "ora-good-cat": dict(battery_type="LFP", drive_type="FWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="MacPherson strut", suspension_rear="Torsion beam", **bev()),

  # ── Changan group (3) ──
  "deepal-s07": dict(battery_type="LFP", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "changan-nevo-a07": dict(battery_type="LFP / NMC", drive_type="RWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "avatr-07": dict(battery_type="LFP (Shenxing)", drive_type="RWD / AWD", motor_type="PMSM (rear) + AC induction (front, AWD)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link (H-arm)", trunk_l=500, **bev()),

  # ── Zeekr (2) ──
  "zeekr-7x": dict(battery_type="LFP / NMC", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **bev()),
  "zeekr-x": dict(battery_type="NMC / LFP", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),

  # ── XPeng (2) ──
  "xpeng-p7-plus": dict(battery_type="LFP", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link", drag_coefficient=0.206, **bev()),
  "xpeng-g9": dict(battery_type="LFP", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link", drag_coefficient=0.272, **bev()),

  # ── NIO (2) ──
  "nio-es6": dict(battery_type="NMC", drive_type="AWD", motor_type="PMSM + AC induction (dual motor)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **bev()),
  "onvo-l60": dict(battery_type="LFP / NMC", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", drag_coefficient=0.229, **bev()),

  # ── IM (1) ──
  "im-ls6": dict(battery_type="LFP / NMC", drive_type="RWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link", **bev()),

  # ── Others (4) ──
  "denza-d9": dict(battery_type="LFP (Blade)", drive_type="FWD / AWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "li-auto-l6": dict(battery_type="LFP", drive_type="AWD", motor_type="PMSM (dual motor)", total_power_kw=300,
    battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Multi-link",
    charging_interface=GB_CHG, charging_adapter=GB_ADAP_PHEV, certification_notes=CERT),
  "leapmotor-c10": dict(battery_type="LFP", drive_type="RWD", motor_type="Permanent magnet synchronous (PMSM)",
    battery_thermal="Liquid cooling", heat_pump="N/A",
    suspension_front="MacPherson strut", suspension_rear="Multi-link", **bev()),
  "xiaomi-su7": dict(battery_type="LFP (Blade)", drive_type="RWD / AWD", motor_type="PMSM (HyperEngine V6/V6s)",
    motor_model="HyperEngine V6 (TZ220XS000)", battery_thermal="Liquid cooling", heat_pump="Yes",
    suspension_front="Double wishbone", suspension_rear="Five-link", drag_coefficient=0.195, **bev()),
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
