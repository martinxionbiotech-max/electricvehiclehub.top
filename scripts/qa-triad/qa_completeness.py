#!/usr/bin/env python3
"""EVHub Top QA Triad — Completeness scan (517 deep profiles). Fixed counting."""
import glob, re, json
from collections import Counter, defaultdict

VEH = 'src/content/vehicles'
files = sorted(glob.glob(f'{VEH}/*.md'))
N = len(files)

SECTIONS = {
    '① Entity Snapshot': [
        'title','description','slug','brand','type','powertrain','price_usd','currency',
        'range_cltc_km','trim','range_wltp_km','fob_price_usd_min','fob_price_usd_max',
        'battery_type','battery_kwh','total_power_kw','motor_power_kw','fast_charge',
        'publishedDate','author','tags','family','image','image_credit','image_source',
        'data_tier','data_reviewed',
    ],
    '② Powertrain & Architecture': [
        'battery_kwh','motor_power_kw','torque_nm','accel_0_100_s','top_speed_kmh',
        'efficiency_kwh_100km','battery_type','drive_type','motor_type','motor_model',
        'total_power_kw','battery_thermal','heat_pump','suspension_front','suspension_rear',
        'brakes','drag_coefficient',
    ],
    '③ Dimensions & Logistics': [
        'length_mm','width_mm','height_mm','wheelbase_mm','weight_kg','gross_weight_kg',
        'ground_clearance_mm','trunk_l','fast_charge',
    ],
    '④ Market Compliance & Export Profile': [
        'hs_code','charging_interface','charging_adapter','infotainment_language',
        'network_bands','certification_notes','landed_cost','landed_cost_markets',
    ],
    '⑤ Benchmarking Matrix (computed)': [
        'type','brand','price_usd','battery_kwh','wheelbase_mm','fast_charge',
    ],
}

def parse(path):
    txt = open(path).read()
    m = re.match(r'^---\n(.*?)\n---\n', txt, re.DOTALL)
    if not m: return {}, '', txt
    fm = m.group(1); body = txt[m.end():]
    data = {}
    for line in fm.split('\n'):
        mm = re.match(r'^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$', line)
        if mm: data[mm.group(1)] = mm.group(2).strip()
    return data, fm, body

def is_na(v):
    """True if field renders as N/A (missing/empty/null/N/A-marker)."""
    s = v.strip().strip('"').strip("'")
    if s in ('', 'null', 'None', '~', 'N/A', 'N/A (…)', 'N/A(...)', 'N/A（）'):
        return True
    if re.match(r'^(N/A|NA)(\s*[\(（–—-].*)?$', s, re.I):
        return True
    return False

# global per-field stats (once per file)
present = Counter(); missing_files = defaultdict(list); na_count = Counter()
all_keys = Counter()
for f in files:
    data, fm, body = parse(f)
    slug = f.split('/')[-1][:-3]
    for k in data: all_keys[k] += 1
    # union of all fields across sections
    for sec, fields in SECTIONS.items():
        for fld in fields:
            if fld in data:
                present[fld] += 1
                if is_na(data[fld]): na_count[fld] += 1
            else:
                missing_files[fld].append(slug)

# placeholder / residue in body prose ONLY (and in frontmatter string values)
residue_body = defaultdict(list)
residue_fm = defaultdict(list)
for f in files:
    data, fm, body = parse(f)
    slug = f.split('/')[-1][:-3]
    for p in ['{...}', 'undefined', '[object Object]', 'NaN', 'TODO', 'TBD', 'PLACEHOLDER', 'Lorem', 'lorem ipsum', 'XXX']:
        if p in body: residue_body[p].append(slug)
        if p in fm: residue_fm[p].append(slug)

# null literal count in frontmatter — which fields carry literal null?
null_fields = Counter()
for f in files:
    data, fm, body = parse(f)
    for line in fm.split('\n'):
        mm = re.match(r'^([A-Za-z_][A-Za-z0-9_]*):\s*(null|None)\s*$', line)
        if mm: null_fields[mm.group(1)] += 1

# md body sections
md_secs = Counter()
for f in files:
    _, _, body = parse(f)
    for h in re.findall(r'^##\s+(.*)$', body, re.MULTILINE):
        md_secs[h.strip()] += 1

out = {'total_files': N, 'sections': {}, 'md_sections': dict(md_secs.most_common()),
       'residue_body': {k: sorted(v) for k, v in residue_body.items() if v},
       'residue_fm': {k: sorted(v) for k, v in residue_fm.items() if v},
       'null_fields': dict(null_fields.most_common())}

print(f'Total files: {N}\n')
for sec, fields in SECTIONS.items():
    print(f'### {sec}')
    print(f'{"field":<22}{"present":>8}{"miss":>6}{"fill%":>8}{"N/A":>5}{"N/A%":>8}')
    for fld in fields:
        p = present[fld]; m = N - p
        fill = round(p/N*100,1)
        na = na_count[fld]
        nar = round(na/N*100,1) if p else 0
        out['sections'].setdefault(sec, []).append({
            'field': fld, 'present': p, 'missing': m, 'fill_pct': fill,
            'na': na, 'na_pct': nar,
            'missing_files': sorted(missing_files[fld]) if m else None})
        print(f'{fld:<22}{p:>8}{m:>6}{fill:>8}{na:>5}{nar:>8}')
    print()

print('### Markdown body sections (H2)')
for h, c in out['md_sections'].items(): print(f'  {c}\t{h}')

print('\n### Null-literal fields (frontmatter value = null)')
for k, c in null_fields.most_common(): print(f'  {c}\t{k}')

print('\n### Residue in body prose')
for k, v in out['residue_body'].items(): print(f'  {k}: {len(v)}')
print('### Residue in frontmatter')
for k, v in out['residue_fm'].items(): print(f'  {k}: {len(v)}')

json.dump(out, open('scripts/qa-triad/_completeness.json','w'), indent=1, ensure_ascii=False)
