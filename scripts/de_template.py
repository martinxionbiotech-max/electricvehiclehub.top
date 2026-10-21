#!/usr/bin/env python3
"""
EVHub Top — De-template Overview / description / certification_notes / charging_adapter.

Deterministic rewrite driven by each vehicle's own frontmatter data. Facts and
numbers are preserved; only sentence structure, emphasis, and (for enum fields)
powertrain-factual wording are varied. Industrial-report tone, zero marketing words.

Usage:
  python3 scripts/de_template.py --slugs <file>   # one slug per line
  python3 scripts/de_template.py --all             # every vehicle

Idempotent: re-running on the same slugs produces byte-identical output.
"""
import glob, re, sys, yaml, hashlib, random

VEH = 'src/content/vehicles'
BRANDS = 'src/content/brands'

# ---------------------------------------------------------------- brand display map
def load_brand_map():
    bm = {}
    for f in glob.glob(f'{BRANDS}/*.md'):
        t = open(f, encoding='utf-8').read()
        m = re.match(r'^---\n(.*?)\n---\n', t, re.DOTALL)
        if not m:
            continue
        slug = f.split('/')[-1][:-3]
        bn = None
        for ln in m.group(1).split('\n'):
            mm = re.match(r'^brand_name:\s*"?(.*?)"?$', ln)
            if mm:
                bn = mm.group(1).strip()
        bm[slug] = bn or slug
    return bm

BRAND_MAP = load_brand_map()

# ---------------------------------------------------------------- parsing
def parse_file(path):
    t = open(path, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---\n', t, re.DOTALL)
    fm = m.group(1)
    body = t[m.end():]
    d = {}
    for ln in fm.split('\n'):
        mm = re.match(r'^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$', ln)
        if mm:
            d[mm.group(1)] = mm.group(2).strip()
    return d, fm, body, t

def clean(d, k):
    v = d.get(k, '').strip()
    if v.startswith('"') and v.endswith('"'):
        v = v[1:-1]
    return v

def num(d, k):
    v = clean(d, k)
    if v in ('', 'null', 'N/A', 'None'):
        return None
    try:
        return float(v)
    except (ValueError, TypeError):
        return None

def rng_for(slug):
    return random.Random(int(hashlib.sha256(slug.encode()).hexdigest()[:16], 16))

def display_brand(slug):
    return BRAND_MAP.get(slug, slug)

def type_noun(ty):
    t = (ty or '').strip()
    if t.upper() in ('SUV', 'MPV'):
        return t.upper()
    return t.lower()

def article_for_noun(noun):
    if noun in ('SUV', 'MPV'):
        return 'an'
    return 'an' if noun[:1] in 'aeiou' else 'a'

# ---------------------------------------------------------------- derived facts
PW_WORDS = {
    'BEV':  ['battery-electric', 'fully electric'],
    'PHEV': ['plug-in hybrid', 'plug-in hybrid electric'],
    'EREV': ['extended-range electric', 'range-extended electric'],
    'HEV':  ['non-plug-in hybrid', 'hybrid'],
    'ICE':  ['petrol', 'internal-combustion'],
}

def price_band(p):
    if p is None:
        return 'mid'
    if p < 15000: return 'entry'
    if p < 25000: return 'value'
    if p < 40000: return 'mid'
    if p < 60000: return 'premium'
    return 'flagship'

BAND_IMPORT = {
    'entry':    ['an entry-level import', 'a budget import', 'an affordable-end import'],
    'value':    ['a value-focused import', 'a value-segment import', 'a mainstream-value import'],
    'mid':      ['a mid-market import', 'a mid-tier import'],
    'premium':  ['a premium import', 'an upper-mid import'],
    'flagship': ['a flagship import', 'a top-tier import'],
}
BAND_SEGMENT = {
    'entry': 'entry-level', 'value': 'value', 'mid': 'mid-market',
    'premium': 'premium', 'flagship': 'flagship',
}

def cheapest_market(d):
    lcm = d.get('landed_cost_markets', '')
    arr = yaml.safe_load(lcm) if lcm else []
    if not isinstance(arr, list) or not arr:
        return None
    return min(arr, key=lambda x: x.get('premium_pct', 99))

def germany(d):
    lcm = d.get('landed_cost_markets', '')
    arr = yaml.safe_load(lcm) if lcm else []
    if not isinstance(arr, list):
        return None
    for it in arr:
        if it.get('market') == 'Germany':
            return it
    return None

def fmt_price(p):
    if p is None:
        return 'N/A'
    return f'{int(round(p)):,}'

def fmt_float(v):
    if v is None:
        return None
    if abs(v - round(v)) < 0.005:
        return f'{int(round(v))}'
    return f'{v:g}'

# ---------------------------------------------------------------- certification / adapter (powertrain-factual)
def gen_cert(d):
    pt = clean(d, 'powertrain')
    ci = clean(d, 'charging_interface').lower()
    ad = clean(d, 'charging_adapter').lower()
    if pt == 'ICE' or 'non-plug' in ci or 'internal combustion' in ci:
        return "EU: WVTA type approval. GCC: GSO conformity certificate."
    if 'ccs2' in ci and 'native' in ad:
        return "EU: WVTA type approval (CCS2 native, no adapter required). GCC: GSO conformity certificate."
    if pt == 'BEV':
        return "EU: WVTA type approval; GB/T port needs CCS2/Type 2 adapter. GCC: GSO conformity certificate."
    # PHEV / EREV
    return "EU: WVTA type approval; GB/T port needs Type 2 (AC) adapter. GCC: GSO conformity certificate."

def gen_adapter(d):
    pt = clean(d, 'powertrain')
    ci = clean(d, 'charging_interface').lower()
    if pt == 'ICE' or 'non-plug' in ci or 'internal combustion' in ci:
        return "N/A"
    if pt == 'BEV':
        return "CCS2 (DC) / Type 2 (AC) adapter required for EU; or OEM EU-spec port"
    return "Type 2 (AC) adapter for EU AC charging"

# ---------------------------------------------------------------- prose helpers
def _pick(r, seq):
    return seq[r.randrange(len(seq))]

def sanitize(s):
    return s.replace('"', "'")

def title_has_brand(title, brand):
    return bool(brand) and title.lower().startswith(brand.lower())

def ident_variants(title, brand, tn, pw, art):
    """Identification sentence variants; avoid 'Brand's Title' when title already
    contains the brand (mirrors brand-label.ts titleHasBrand guard)."""
    v = [
        f"The {title} is {art} {tn} {pw} from {brand}",
        f"The {title} is {brand}'s {tn} {pw}",
        f"{title} is {art} {tn} {pw} offered by {brand}",
    ]
    if not title_has_brand(title, brand):
        v.append(f"{brand}'s {title} is {art} {tn} {pw}")
    return v

def join_list(items):
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return ", ".join(items[:-1]) + f", and {items[-1]}"

def _audience(ty, band):
    t = (ty or '').lower()
    seg = []
    if t == 'suv':
        seg += ['family and fleet buyers needing practical space',
                'families and commercial fleet operators',
                'importers targeting the family-SUV segment',
                'private buyers and fleet managers',
                'regional distributors serving family and logistics demand']
    elif t == 'sedan':
        seg += ['business fleets and long-distance commuters',
                'executive and corporate fleet buyers',
                'private buyers and ride-hailing operators',
                'importers serving the executive-sedan segment']
    elif t == 'hatchback':
        seg += ['urban commuters and fleet operators',
                'city-focused buyers and delivery fleets',
                'importers targeting urban runabout demand']
    elif t == 'mpv':
        seg += ['people-carrier operators and family buyers',
                'shuttle and charter fleet operators',
                'importers serving the multi-passenger segment']
    else:
        seg += ['family and fleet buyers', 'private and commercial buyers']
    if band in ('entry', 'value'):
        seg += ['price-sensitive importers', 'budget-conscious fleet buyers']
    elif band in ('premium', 'flagship'):
        seg += ['premium-tier importers', 'high-spec private buyers']
    return seg

# ---------------------------------------------------------------- description
def gen_description(d, prof, r):
    pt = prof['pt']; ty = prof['type']; brand = prof['brand_label']; title = prof['title']
    pw = _pick(r, PW_WORDS.get(pt, [pt.lower()]))
    tn = type_noun(ty)
    art = article_for_noun(tn)

    rng = num(d, 'range_cltc_km'); bat = num(d, 'battery_kwh')
    pwr = num(d, 'total_power_kw') or num(d, 'motor_power_kw')
    chem = clean(d, 'battery_type')

    ident = _pick(r, ident_variants(title, brand, tn, pw, art))
    spec = []
    if rng is not None:
        spec.append(_pick(r, [f"{int(rng):,} km of CLTC range",
                              f"a CLTC-rated range of {int(rng):,} km"]))
    if bat is not None:
        spec.append(_pick(r, [f"a {int(bat):,} kWh battery", f"{int(bat):,} kWh of battery"]))
    if pwr is not None:
        spec.append(_pick(r, [f"{int(pwr):,} kW of motor power", f"{int(pwr):,} kW peak output"]))
    if chem and chem not in ('N/A', ''):
        spec.append(_pick(r, [f"{chem} chemistry", f"a {chem} pack"]))

    s1 = ident
    if spec:
        s1 += _pick(r, [f", offering {join_list(spec)}", f" with {join_list(spec)}"])
    s1 += "."

    s2 = _pick(r, [
        "Full landed-cost breakdown across 30 export markets for B2B import planning.",
        "Per-market landed-cost modeling across 30 export destinations.",
        "Landed-cost analysis across 30 key export markets for importers.",
    ])
    return sanitize(f"{s1} {s2}")

# ---------------------------------------------------------------- overview
def gen_overview(d, prof, r):
    pt = prof['pt']; ty = prof['type']; brand = prof['brand_label']; title = prof['title']
    p = prof['price']; band = prof['band']
    pw = _pick(r, PW_WORDS.get(pt, [pt.lower()]))
    bandw = _pick(r, BAND_IMPORT[band])
    seg = BAND_SEGMENT[band]
    cheap = prof['cheap']; ger = prof['germany']
    tn = type_noun(ty)
    art = article_for_noun(tn)

    sents = []

    # S1 — identification (complete sentence)
    sents.append(_pick(r, ident_variants(title, brand, tn, pw, art)) + ".")

    # S2 — powertrain & performance (1-3 clauses)
    clauses = []
    rng = num(d, 'range_cltc_km'); bat = num(d, 'battery_kwh')
    pwr = num(d, 'total_power_kw') or num(d, 'motor_power_kw')
    tor = num(d, 'torque_nm'); acc = num(d, 'accel_0_100_s'); top = num(d, 'top_speed_kmh')
    if rng is not None:
        clauses.append(_pick(r, [
            f"a CLTC-rated range of {int(rng):,} km",
            f"{int(rng):,} km of CLTC range",
            f"a rated range of {int(rng):,} km (CLTC)",
        ]))
    if bat is not None:
        clauses.append(_pick(r, [
            f"a {int(bat):,} kWh battery",
            f"{int(bat):,} kWh of battery capacity",
        ]))
    if pwr is not None:
        clauses.append(_pick(r, [
            f"peak output of {int(pwr):,} kW",
            f"a {int(pwr):,} kW electric motor",
        ]))
    if tor is not None:
        clauses.append(_pick(r, [
            f"{int(tor):,} Nm of torque",
            f"peak torque of {int(tor):,} Nm",
        ]))
    if acc is not None:
        clauses.append(_pick(r, [
            f"a {fmt_float(acc)}-second 0–100 km/h time",
            f"0–100 km/h in {fmt_float(acc)} seconds",
        ]))
    if top is not None:
        clauses.append(_pick(r, [
            f"a top speed of {int(top):,} km/h",
            f"{int(top):,} km/h top speed",
        ]))
    if clauses:
        r.shuffle(clauses)
        n = min(len(clauses), 2 if r.random() < 0.7 else 3)
        chosen = clauses[:n]
        if n == 1:
            sents.append(f"Its specification includes {chosen[0]}.")
        else:
            sents.append(_pick(r, [
                f"It carries {join_list(chosen)}.",
                f"Specification highlights are {join_list(chosen)}.",
            ]))

    # S3 — chassis / battery / aero (1-2 clauses)
    c3 = []
    chem = clean(d, 'battery_type'); drv = clean(d, 'drive_type')
    sf = clean(d, 'suspension_front'); sr = clean(d, 'suspension_rear')
    cd = num(d, 'drag_coefficient')
    if chem and chem not in ('N/A', ''):
        c3.append(_pick(r, [f"{chem} cells", f"{chem} chemistry"]))
    if drv and drv not in ('N/A', ''):
        c3.append(_pick(r, [f"{drv} drivetrain", f"{drv} drive"]))
    if sf and sf not in ('N/A', ''):
        sfx = f"{sf} front" + (f" / {sr} rear" if sr and sr not in ('N/A', '') else "")
        c3.append(_pick(r, [f"{sfx} suspension", f"a {sfx} suspension setup"]))
    if cd is not None:
        c3.append(_pick(r, [f"a drag coefficient of {fmt_float(cd)}", f"a Cd of {fmt_float(cd)}"]))
    if c3:
        r.shuffle(c3)
        n = min(len(c3), 2)
        if n == 1:
            sents.append(_pick(r, [
                f"The platform uses {c3[0]}.",
                f"Underpinning the car is {c3[0]}.",
            ]))
        else:
            sents.append(_pick(r, [
                f"The platform pairs {c3[0]} with {c3[1]}.",
                f"Chassis details include {c3[0]}, plus {c3[1]}.",
            ]))

    # S4 — positioning / price
    sents.append(_pick(r, [
        f"It is positioned as {bandw}, priced from ${fmt_price(p)} ex-factory.",
        f"At an ex-factory price of ${fmt_price(p)}, it sits in the {seg} segment of the Chinese EV export range.",
        f"Pricing starts at ${fmt_price(p)} ex-factory, placing it in the {seg} tier.",
        f"The ex-factory price of ${fmt_price(p)} positions it as {bandw}.",
    ]))

    # S5 — export / landed cost (single flowing sentence, variable lead-in)
    cheap_clause = None
    if cheap:
        mkt = cheap.get('market'); prem = cheap.get('premium_pct'); landed = cheap.get('total_landed_usd')
        if mkt and prem is not None and landed is not None:
            cheap_clause = _pick(r, [
                f"the lowest landed premium is {mkt} at roughly +{fmt_float(prem)}% over base (about ${int(landed):,} landed)",
                f"{mkt} offers the cheapest entry at about +{fmt_float(prem)}% over base (≈ ${int(landed):,} landed)",
                f"the least-costly destination is {mkt}, near +{fmt_float(prem)}% over base (${int(landed):,} landed)",
            ])
    ger_clause = None
    if ger:
        std = ger.get('standard_duty_rate'); cvd = ger.get('countervailing_duty_rate')
        if cvd is not None and cvd > 0 and std is not None:
            ger_clause = _pick(r, [
                f"Germany applies a {fmt_float(cvd*100)}% countervailing duty on top of the {fmt_float(std*100)}% standard tariff",
                f"Germany's estimate carries a {fmt_float(cvd*100)}% countervailing duty over the {fmt_float(std*100)}% base tariff",
            ])
        elif cvd == 0 and std is not None:
            ger_clause = _pick(r, [
                f"Germany applies the {fmt_float(std*100)}% standard tariff with no countervailing duty",
                f"Germany levies only the {fmt_float(std*100)}% standard tariff",
            ])
    if cheap_clause:
        lead = _pick(r, ["For importers, ", "On landed cost, ", "Across export markets, "])
        s5 = lead + cheap_clause
        if ger_clause:
            s5 += _pick(r, [", while ", "; meanwhile, ", " — "]) + ger_clause
        s5 += "."
        sents.append(s5)

    # S6 — audience
    aud = _pick(r, _audience(ty, band))
    sents.append(_pick(r, [
        f"It suits {aud}.",
        f"The profile suits {aud}.",
        f"This positions it for {aud}.",
    ]))

    para = re.sub(r'\s+', ' ', ' '.join(sents)).strip()
    return sanitize(para)

# ---------------------------------------------------------------- rewrite a file
def rewrite(path):
    d, fm, body, raw = parse_file(path)
    slug = d.get('slug', '').strip('"')
    pt = clean(d, 'powertrain')
    title = clean(d, 'title')
    brand_slug = clean(d, 'brand')
    ty = clean(d, 'type')
    p = num(d, 'price_usd')
    band = price_band(p)

    prof = {
        'pt': pt, 'title': title, 'brand_label': display_brand(brand_slug),
        'type': ty, 'price': p, 'band': band,
        'cheap': cheapest_market(d), 'germany': germany(d),
    }
    r = rng_for(slug)

    new_desc = gen_description(d, prof, r)
    new_cert = gen_cert(d)
    new_adapter = gen_adapter(d)
    new_ov = gen_overview(d, prof, r)

    def repl_field(text, key, value):
        assert '"' not in value, f'double quote in {key} for {slug}: {value!r}'
        pat = re.compile(rf'^{key}:\s*[^\n]*', re.M)
        return pat.sub(f'{key}: "{value}"', text, count=1)

    out = raw
    out = repl_field(out, 'description', new_desc)
    out = repl_field(out, 'certification_notes', new_cert)
    out = repl_field(out, 'charging_adapter', new_adapter)

    m = re.search(r'(## Overview\s*\n\n)(.*?)(\n## Landed Cost by Market)', out, re.DOTALL)
    if m:
        out = out[:m.start(2)] + new_ov + out[m.end(2):]
    else:
        sys.stderr.write(f'!! no Overview block found for {slug}\n')

    if out == raw:
        return False, slug
    open(path, 'w', encoding='utf-8').write(out)
    return True, slug

# ---------------------------------------------------------------- main
if __name__ == '__main__':
    slugs = []
    if '--all' in sys.argv:
        slugs = sorted(glob.glob(f'{VEH}/*.md'))
    elif '--slugs' in sys.argv:
        i = sys.argv.index('--slugs')
        fname = sys.argv[i+1]
        slugs = [f'{VEH}/{s.strip()}.md' for s in open(fname) if s.strip()]
    else:
        slugs = [f'{VEH}/{s}.md' for s in sys.argv[1:]]

    changed = 0
    for p in slugs:
        ok, slug = rewrite(p)
        if ok:
            changed += 1
    print(f'de_template: {changed}/{len(slugs)} files rewritten')
