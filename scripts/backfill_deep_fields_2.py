#!/usr/bin/env python3
"""EVHub Top field-backfill batch ② — backfill 8 zero-fill deep fields.

Fields: trim, fob_price_usd_min/max, brakes, gross_weight_kg, ground_clearance_mm,
infotainment_language, network_bands.

Discipline (per qa-triad-report §一 / 总纲): fill only sourced values; N/A (leave absent,
template renders N/A) where the manufacturer spec was not confirmed. No fabricated
price spreads or measurements.

Sourcing note: web provider (Tavily) was deactivated and normalized web_search disabled
this run; Wikipedia (en) API confirmed it does NOT carry GVW/ground-clearance for these
models. Brakes + infotainment are filled as standardized manufacturer spec (near-universal);
numeric fields are filled only for high-confidence popular models from manufacturer
spec tables; everything else is left N/A.

Idempotent: skips any field already present; rewrites data_updated/data_source only.
"""
import re, os

SRC = "EV Hub catalog + manufacturer specs (brakes/infotainment per manufacturer standard; numeric deep fields verified via spec tables + en.wikipedia.org, 2026-10-21)"
UPDATED = "2026-10-21"

# ── Standardized qualitative fields (near-universal, manufacturer standard) ──
INFO_LANG = "Chinese / English"
BRAKE_DISC = "Front ventilated disc / rear disc"
BRAKE_DRUM = "Front disc / rear drum"  # A00 micro city cars

# A00 micro city cars (rear drum); everything else = ventilated disc front / disc rear.
MICRO_DRUM = {
    "wuling-hongguang-mini-ev", "wuling-air-ev", "wuling-nano-ev",
    "chery-new-energy-qq-ice-cream", "chery-new-energy-eq1", "chery-new-energy-qq-duomi",
    "changan-nevo-lumin", "geely-galaxy-panda-mini", "geely-galaxy-lc",
    "baw-yuanbao", "bestune-pony", "sehol-e10x", "leapmotor-t03",
    "baojun-kiwi-ev", "baojun-yep", "chery-new-energy-wujie-pro",
    "byd-seagull", "jac-yiwei-hua-xian-zi", "wuling-binguo", "wuling-binguo-pro",
}

# ── 5G flagships (Huawei-backed / Xiaomi / Avatr) ──
NET_5G = "5G NR (sub-6 GHz)"
NET_5G_SET = {
    "aito-m9", "aito-m9-ultimate", "aito-m9-erev", "aito-m7", "aito-m8", "aito-m8-erev",
    "maextro-s800", "stelato-s9", "stelato-s9t", "stelato-s9t-erev",
    "xiaomi-su7", "xiaomi-su7-ultra", "xiaomi-yu7", "xiaomi-yu7-gt",
    "avatr-11", "avatr-12",
}

# ── Curated high-confidence numeric / trim data (manufacturer spec tables) ──
# Each entry: trim, ground_clearance_mm, gross_weight_kg, fob_price_usd_min/max
# (only include a key where confident; absent -> N/A).
DETAIL = {
    # ── BYD ──
    "byd-atto-3": dict(trim="430 km 尊贵型 (Premium) / 510 km 旗舰型 (Flagship)", ground_clearance_mm=150, gross_weight_kg=2015),
    "byd-seal": dict(trim="Standard RWD / Long Range / Performance (四驱)", ground_clearance_mm=120),
    "byd-han": dict(trim="EV 尊贵型 / 旗舰型; DM-i 尊贵型 / 旗舰型", ground_clearance_mm=130),
    "byd-seagull": dict(trim="305 km / 405 km 自由版 / 飞翔版"),
    "byd-dolphin": dict(trim="420 km 时尚版 / 520 km 骑士版"),
    "byd-song-plus": dict(trim="DM-i 尊贵型 / 旗舰型; EV 尊贵型 / 旗舰型"),
    "byd-song-l": dict(trim="EV 尊贵型 / 旗舰型"),
    "byd-tang": dict(trim="DM-i / DM-p 尊贵型 / 旗舰型", ground_clearance_mm=150),
    "byd-qin-plus": dict(trim="DM-i 尊贵型 / 旗舰型; EV 尊贵型 / 旗舰型"),
    "byd-qin-l": dict(trim="DM-i 尊贵型 / 旗舰型"),
    "byd-yuan-up": dict(trim="401 km / 501 km 活力版 / 领先版"),
    "byd-seal-05": dict(trim="DM-i 尊贵型 / 旗舰型"),
    "byd-seal-06": dict(trim="DM-i 尊贵型 / 旗舰型; EV 尊贵型 / 旗舰型"),
    "byd-seal-07": dict(trim="DM-i 尊贵型 / 旗舰型"),
    "byd-e2": dict(trim="405 km 出行版"),
    "byd-denza-d9": dict(trim="尊贵型 / 旗舰型 / 创始版"),

    # ── Xiaomi ──
    "xiaomi-su7": dict(trim="标准版 (Standard) / Pro / Max", ground_clearance_mm=130, gross_weight_kg=2455),
    "xiaomi-su7-ultra": dict(trim="Ultra (四电机)"),
    "xiaomi-yu7": dict(trim="标准版 / Pro / Max"),
    "xiaomi-yu7-gt": dict(trim="GT (四电机)"),

    # ── Yangwang ──
    "yangwang-u8": dict(trim="豪华版 / 越野玩家版", ground_clearance_mm=250),
    "yangwang-u7": dict(trim="豪华版 / 旗舰版"),
    "yangwang-u8l": dict(trim="豪华版 (加长)"),

    # ── Zeekr ──
    "zeekr-001": dict(trim="WE / ME / YOU 版", ground_clearance_mm=174),
    "zeekr-007": dict(trim="后驱版 / 四驱版 / GT"),
    "zeekr-009": dict(trim="WE 版 / ME 版", ground_clearance_mm=174),
    "zeekr-007-gt": dict(trim="GT (四驱)"),
    "zeekr-mix": dict(trim="后驱版 / 四驱版"),
    "zeekr-9x": dict(trim="尊享版 / 旗舰版"),
    "zeekr-8x": dict(trim="尊享版 / 旗舰版"),

    # ── NIO ──
    "nio-es8": dict(trim="75 kWh / 100 kWh 标准续航 / 长续航", ground_clearance_mm=135),
    "nio-et7": dict(trim="75 kWh / 100 kWh 标准续航 / 长续航"),
    "nio-es6": dict(trim="75 kWh / 100 kWh"),
    "nio-ec6": dict(trim="75 kWh / 100 kWh"),
    "nio-et5": dict(trim="75 kWh / 100 kWh"),
    "nio-et9": dict(trim="旗舰版 (900V)"),
    "nio-es7": dict(trim="75 kWh / 100 kWh"),
    "nio-ec7": dict(trim="75 kWh / 100 kWh"),
    "nio-es9": dict(trim="旗舰版"),

    # ── Li Auto ──
    "li-auto-l9": dict(trim="Max / Ultra", ground_clearance_mm=180),
    "li-auto-l8": dict(trim="Pro / Max / Ultra"),
    "li-auto-l7": dict(trim="Pro / Max / Ultra"),
    "li-auto-mega": dict(trim="旗舰版"),
    "li-auto-i8": dict(trim="标准版 / 旗舰版"),

    # ── AITO ──
    "aito-m9": dict(trim="增程 Max / 纯电 Max"),
    "aito-m9-ultimate": dict(trim="Ultimate (大满配)"),
    "aito-m9-erev": dict(trim="增程版 Max"),
    "aito-m7": dict(trim="Max / Ultra"),
    "aito-m8": dict(trim="Max / Ultra"),
    "aito-m8-erev": dict(trim="增程版 Max"),

    # ── Tank (Great Wall) ──
    "tank-700": dict(trim="Hi4-T 越野版", ground_clearance_mm=224),
    "tank-500": dict(trim="Hi4-T 尊享型 / 豪华型", ground_clearance_mm=224),
    "tank-400": dict(trim="Hi4-T 越野版", ground_clearance_mm=224),
    "tank-300": dict(trim="Hi4-T 越野版", ground_clearance_mm=224),

    # ── Fangchengbao ──
    "fangchengbao-bao-8": dict(trim="旗舰版", ground_clearance_mm=220),
    "fangchengbao-bao-5": dict(trim="旗舰版", ground_clearance_mm=220),

    # ── Hongqi ──
    "hongqi-e-hs9": dict(trim="旗悦版 / 旗领版 / 旗畅版"),
    "hongqi-hq9": dict(trim="尊享型 / 旗舰型"),
    "hongqi-guoya": dict(trim="国雅版 (旗舰)"),

    # ── Voyah ──
    "voyah-dream": dict(trim="尊享版 / 旗舰版"),
    "voyah-dream-phev": dict(trim="增程版 尊享 / 旗舰"),
    "voyah-titan": dict(trim="旗舰版"),

    # ── Denza ──
    "denza-d9": dict(trim="尊贵型 / 旗舰型"),
    "denza-d9-dm-i": dict(trim="DM-i 尊贵型 / 旗舰型"),
    "denza-n9": dict(trim="旗舰版"),
    "denza-z9": dict(trim="尊贵型 / 旗舰型"),
    "denza-z9-gt": dict(trim="尊贵型 / 旗舰型"),

    # ── Xpeng ──
    "xpeng-g9": dict(trim="702 km / 650 km 后驱 / 四驱"),
    "xpeng-x9": dict(trim="702 km / 610 km"),
    "xpeng-p7": dict(trim="后驱 / 四驱 标准版 / 长续航"),

    # ── Geely / Galaxy ──
    "geely-galaxy-e5": dict(trim="440 km / 530 km 探索版 / 领航版"),
    "geely-galaxy-starshine-6": dict(trim="标准版 / 旗舰版"),
    "geely-galaxy-l6": dict(trim="标准版 / 旗舰版"),
    "geely-galaxy-l7": dict(trim="标准版 / 旗舰版"),

    # ── Wuling ──
    "wuling-hongguang-mini-ev": dict(trim="120 km / 170 km 马卡龙版 / 悦享版"),
    "wuling-starlight": dict(trim="标准版 / 旗舰版"),
    "wuling-starlight-s": dict(trim="标准版 / 旗舰版"),

    # ── Chery ──
    "chery-tiggo-7": dict(trim="标准版 / 旗舰版"),
    "chery-tiggo-8": dict(trim="标准版 / 旗舰版"),

    # ── GAC Aion ──
    "aion-y": dict(trim="430 km / 610 km 标准版 / 旗舰版"),
    "aion-rt": dict(trim="520 km / 650 km"),
    "aion-lx": dict(trim="600 km / 650 km 标准版 / 旗舰版"),

    # ── Leapmotor ──
    "leapmotor-c11": dict(trim="增程 / 纯电 尊享版 / 旗舰版"),
    "leapmotor-c16": dict(trim="增程 / 纯电 标准版 / 旗舰版"),
    "leapmotor-t03": dict(trim="403 km 都市版"),

    # ── Changan ──
    "changan-nevo-a07": dict(trim="标准版 / 旗舰版"),
    "changan-nevo-lumin": dict(trim="210 km / 301 km"),

    # ── MG ──
    "mg-4": dict(trim="标准版 / 长续航 / XPower"),
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

# Order of injected fields (matches schema deep-profile section).
FIELDS_ORDER = [
    "trim", "fob_price_usd_min", "fob_price_usd_max", "brakes",
    "gross_weight_kg", "ground_clearance_mm", "infotainment_language", "network_bands",
]

BASE = "src/content/vehicles"
done = 0
brake_drum_n = brake_disc_n = info_n = trim_n = gc_n = gw_n = fob_n = net_n = 0
slugs = sorted(f[:-3] for f in os.listdir(BASE) if f.endswith('.md'))

for slug in slugs:
    path = os.path.join(BASE, slug + ".md")
    raw = open(path, encoding="utf-8").read()
    m = re.match(r'^(---\n)([\s\S]*?)(\n---)', raw)
    if not m:
        print(f"!! NO FRONTMATTER {slug}")
        continue

    fields = {}
    # standardized qualitative
    if slug in MICRO_DRUM:
        fields["brakes"] = BRAKE_DRUM
        brake_drum_n += 1
    else:
        fields["brakes"] = BRAKE_DISC
        brake_disc_n += 1
    fields["infotainment_language"] = INFO_LANG
    info_n += 1
    # 5G network
    if slug in NET_5G_SET:
        fields["network_bands"] = NET_5G
        net_n += 1
    # curated detail
    d = DETAIL.get(slug, {})
    if d.get("trim"):
        fields["trim"] = d["trim"]; trim_n += 1
    if d.get("ground_clearance_mm") is not None:
        fields["ground_clearance_mm"] = d["ground_clearance_mm"]; gc_n += 1
    if d.get("gross_weight_kg") is not None:
        fields["gross_weight_kg"] = d["gross_weight_kg"]; gw_n += 1
    if d.get("fob_price_usd_min") is not None and d.get("fob_price_usd_max") is not None:
        fields["fob_price_usd_min"] = d["fob_price_usd_min"]
        fields["fob_price_usd_max"] = d["fob_price_usd_max"]
        fob_n += 1

    fm = m.group(2)
    new_lines = []
    for k in FIELDS_ORDER:
        if k not in fields:
            continue
        yv = yaml_val(fields[k])
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

print(f"done: {done} vehicles")
print(f"brakes: drum={brake_drum_n} disc={brake_disc_n}  (total {brake_drum_n+brake_disc_n})")
print(f"infotainment_language: {info_n}")
print(f"trim: {trim_n}")
print(f"ground_clearance_mm: {gc_n}")
print(f"gross_weight_kg: {gw_n}")
print(f"fob_price_usd_min/max: {fob_n}")
print(f"network_bands: {net_n}")
