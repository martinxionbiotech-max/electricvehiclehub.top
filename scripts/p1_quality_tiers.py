#!/usr/bin/env python3
"""EVHub Top P1 — 517 quality tiering (independent decision value).

A = data complete + verified + differentiated narrative (keep)
B = data complete but narrative isomorphic (mark pending differentiation)
C = data missing / many unverified (add visible "partial data" annotation)

Metrics per vehicle:
  - completeness: fraction of CORE decision fields filled (powertrain-aware)
  - tmpl_rate:    fraction of Overview sentences whose masked skeleton is shared (>=2 files)
  - verif:        verification_status field (verified/partial/unverifiable/None)

Usage:
  python3 scripts/p1_quality_tiers.py           # dry-run: print distribution + write JSON
  python3 scripts/p1_quality_tiers.py --apply   # also write `quality_tier:` into frontmatter
"""
import glob, re, json, sys
from collections import Counter, defaultdict

VEH = 'src/content/vehicles'
APPLY = '--apply' in sys.argv

# ── Core decision fields (expected-complete for a full profile) ──
CORE = [
    'range_cltc_km', 'battery_kwh', 'battery_type',
    'motor_power_kw', 'torque_nm', 'drive_type', 'motor_type',
    'accel_0_100_s', 'top_speed_kmh', 'efficiency_kwh_100km',
    'length_mm', 'width_mm', 'height_mm', 'wheelbase_mm', 'weight_kg',
    'battery_thermal', 'suspension_front', 'suspension_rear', 'brakes',
    'hs_code', 'charging_interface', 'charging_adapter', 'certification_notes',
    'infotainment_language',
]
# Legitimately-absent fields by powertrain (not penalized)
NA_BY_PT = {
    'BEV': set(),
    'PHEV': set(),
    'EREV': set(),
    'HEV': {'range_cltc_km', 'battery_kwh', 'charging_interface', 'charging_adapter'},
    'ICE': {'range_cltc_km', 'battery_kwh', 'battery_type', 'motor_type',
            'motor_power_kw', 'charging_interface', 'charging_adapter', 'battery_thermal'},
}

# ── thresholds ──
COMPLETE_MIN = 0.72
PARTIAL_COMPLETE_MIN = 0.85   # a "partial" vehicle needs near-full data to avoid C
TMPL_ISOMORPHIC = 0.50        # >= 50% of overview sentences share a skeleton

files = sorted(glob.glob(f'{VEH}/*.md'))

def parse(path):
    t = open(path).read()
    m = re.match(r'^---\n(.*?)\n---\n', t, re.DOTALL)
    if not m:
        return {}, '', t
    fm = m.group(1)
    body = t[m.end():]
    d = {}
    for ln in fm.split('\n'):
        mm = re.match(r'^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$', ln)
        if mm:
            d[mm.group(1)] = mm.group(2).strip()
    return d, fm, body

def get_overview(body):
    i = body.find('## Overview')
    if i < 0:
        return ''
    rest = body[i + len('## Overview'):]
    nxt = re.search(r'\n## ', rest)
    return rest[:nxt.start()].strip() if nxt else rest.strip()

def mask(s, title='', brand=''):
    s = s.replace(title, ' {TITLE} ').replace(brand, ' {BRAND} ').replace(brand.upper(), ' {BRAND} ')
    s = re.sub(r'\$[\d,.]+', ' {PRICE} ', s)
    s = re.sub(r'\b\d+(\.\d+)?%?([,\d.]*)\b', ' {N} ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def sentences(txt):
    txt = re.sub(r'\s+', ' ', txt).strip()
    parts = re.split(r'(?<=[.!?])\s+', txt)
    return [p.strip() for p in parts if len(p.strip()) > 15]

def filled(v):
    if v is None:
        return False
    s = v.strip().strip('"').strip("'")
    if s in ('', 'null', 'None', 'N/A'):
        return False
    if s.startswith('N/A'):
        return False
    return True

# ── pass 1: parse + build global overview skeleton counter ──
recs = []
ov_skel_counter = Counter()
for f in files:
    d, fm, body = parse(f)
    slug = f.split('/')[-1][:-3]
    title = d.get('title', '').strip('"')
    brand = d.get('brand', '').strip('"')
    ov = get_overview(body)
    sents = sentences(ov)
    skels = [mask(s, title, brand) for s in sents]
    for sk in skels:
        ov_skel_counter[sk] += 1
    recs.append(dict(slug=slug, d=d, sents=sents, skels=skels, f=f))

# ── pass 2: score + classify ──
tiers = defaultdict(list)
rows = []
for r in recs:
    d = r['d']
    slug = r['slug']
    pt = d.get('powertrain', '').strip('"').strip("'")
    excl = NA_BY_PT.get(pt, set())
    required = [k for k in CORE if k not in excl]
    missing = [k for k in required if not filled(d.get(k))]
    filled_n = len(required) - len(missing)
    completeness = filled_n / len(required) if required else 1.0

    # narrative template rate
    shared = sum(1 for sk in r['skels'] if ov_skel_counter[sk] >= 2)
    tmpl_rate = shared / len(r['skels']) if r['skels'] else 0.0

    verif = d.get('verification_status', '').strip('"').strip("'")
    if verif in ('', 'null', 'None'):
        verif = None

    # ── decision tree ──
    if verif == 'unverifiable':
        tier = 'C'
        reason = 'unverifiable (no authoritative source)'
    elif completeness < COMPLETE_MIN:
        tier = 'C'
        reason = f'data incomplete ({completeness:.0%}, missing {len(missing)}: {", ".join(missing[:6])})'
    elif verif == 'partial' and completeness < PARTIAL_COMPLETE_MIN:
        tier = 'C'
        reason = f'partial-verified + incomplete ({completeness:.0%})'
    elif tmpl_rate >= TMPL_ISOMORPHIC:
        tier = 'B'
        reason = f'narrative isomorphic (template rate {tmpl_rate:.0%})'
    else:
        tier = 'A'
        reason = 'complete + differentiated narrative'

    tiers[tier].append(slug)
    rows.append(dict(slug=slug, tier=tier, completeness=round(completeness, 3),
                     tmpl_rate=round(tmpl_rate, 3), verif=verif,
                     missing=missing, reason=reason, powertrain=pt))

rows.sort(key=lambda x: x['slug'])

# ── report ──
print(f'Total vehicles: {len(rows)}')
for t in ('A', 'B', 'C'):
    print(f'  Tier {t}: {len(tiers[t])}')
print()
print('Verification status distribution:')
vc = Counter(r['verif'] for r in rows)
for k, c in vc.most_common():
    print(f'  {k!r}: {c}')
print()
print('Completeness distribution (min/med/max):')
cs = sorted(r['completeness'] for r in rows)
print(f'  min={cs[0]:.2f}  p25={cs[len(cs)//4]:.2f}  med={cs[len(cs)//2]:.2f}  p75={cs[3*len(cs)//4]:.2f}  max={cs[-1]:.2f}')
print()
print('Template rate distribution:')
ts = sorted(r['tmpl_rate'] for r in rows)
print(f'  min={ts[0]:.2f}  p25={ts[len(ts)//4]:.2f}  med={ts[len(ts)//2]:.2f}  p75={ts[3*len(ts)//4]:.2f}  max={ts[-1]:.2f}')
print()
print('=== Tier C (lowest completeness first) ===')
crows = sorted([r for r in rows if r['tier'] == 'C'], key=lambda x: x['completeness'])
for r in crows:
    print(f"  {r['slug']:32s} comp={r['completeness']:.2f} verif={r['verif']!r} tmpl={r['tmpl_rate']:.2f}  {r['reason']}")

json.dump({
    'total': len(rows),
    'tiers': {t: sorted(tiers[t]) for t in ('A', 'B', 'C')},
    'rows': rows,
    'thresholds': {'COMPLETE_MIN': COMPLETE_MIN, 'PARTIAL_COMPLETE_MIN': PARTIAL_COMPLETE_MIN, 'TMPL_ISOMORPHIC': TMPL_ISOMORPHIC},
}, open('scripts/p1_quality_tiers.json', 'w'), indent=1, ensure_ascii=False)
print('\nSAVED scripts/p1_quality_tiers.json')

# ── apply quality_tier into frontmatter ──
if APPLY:
    applied = 0
    tier_by_slug = {r['slug']: r['tier'] for r in rows}
    for f in files:
        slug = f.split('/')[-1][:-3]
        tier = tier_by_slug.get(slug)
        if tier is None:
            continue
        txt = open(f).read()
        m = re.match(r'^---\n(.*?)\n---\n', txt, re.DOTALL)
        if not m:
            continue
        fm = m.group(1)
        if re.search(r'^quality_tier:', fm, re.M):
            # already present: replace value in place
            newfm = re.sub(r'^quality_tier:.*$', f'quality_tier: "{tier}"', fm, flags=re.M)
        else:
            # append after data_source / data_updated (end of fm)
            newfm = fm.rstrip() + f'\nquality_tier: "{tier}"'
        txt2 = txt.replace(fm, newfm, 1)
        if txt2 != txt:
            open(f, 'w').write(txt2)
            applied += 1
    print(f'\nAPPLIED quality_tier to {applied} files')
