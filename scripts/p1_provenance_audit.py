#!/usr/bin/env python3
"""EVHub Top P1 — Provenance audit (Data Sources block coverage).

Checks across all 517 vehicle frontmatter:
  - data_source  present + whether it carries a full URL vs domain mention only
  - data_updated present (update time)
  - image_source present (full Wikimedia URL)
  - author       present + consistent (data responsible person)
  - verification_status / quality_tier coverage

Outputs scripts/p1_provenance_audit.json + a summary to stdout.
"""
import glob, re, json
from collections import Counter

VEH = 'src/content/vehicles'
files = sorted(glob.glob(f'{VEH}/*.md'))

def parse(p):
    t = open(p).read()
    m = re.match(r'^---\n(.*?)\n---\n', t, re.DOTALL)
    fm = m.group(1)
    d = {}
    for ln in fm.split('\n'):
        mm = re.match(r'^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$', ln)
        if mm:
            d[mm.group(1)] = mm.group(2).strip()
    return d

def strip(v):
    return (v or '').strip('"').strip("'")

authors = Counter()
missing = {k: [] for k in ('data_source', 'data_updated', 'image_source', 'author')}
ds_full_url, ds_domain_only = [], []

for f in files:
    d = parse(f)
    slug = f.split('/')[-1][:-3]
    authors[strip(d.get('author'))] += 1
    ds = strip(d.get('data_source'))
    du = strip(d.get('data_updated'))
    isrc = strip(d.get('image_source'))
    au = strip(d.get('author'))
    for key, val in (('data_source', ds), ('data_updated', du), ('image_source', isrc), ('author', au)):
        if not val:
            missing[key].append(slug)
    if re.search(r'https?://', ds):
        ds_full_url.append(slug)
    elif re.search(r'\.(org|com|net|gov|eu|wikipedia)\b', ds):
        ds_domain_only.append(slug)

verif = Counter(strip(parse(f).get('verification_status')) or None for f in files)
tier = Counter(strip(parse(f).get('quality_tier')) or None for f in files)

report = {
    'total': len(files),
    'authors': dict(authors),
    'missing': {k: sorted(v) for k, v in missing.items()},
    'data_source_full_url': len(ds_full_url),
    'data_source_domain_only': len(ds_domain_only),
    'verification_status': {str(k): v for k, v in verif.items()},
    'quality_tier': {str(k): v for k, v in tier.items()},
}
json.dump(report, open('scripts/p1_provenance_audit.json', 'w'), indent=1, ensure_ascii=False)

print(f"total: {len(files)}")
print(f"author distribution: {dict(authors)}")
for k in ('data_source', 'data_updated', 'image_source', 'author'):
    print(f"missing {k}: {len(missing[k])}")
print(f"data_source with full URL: {len(ds_full_url)}")
print(f"data_source domain-mention only: {len(ds_domain_only)}")
print(f"verification_status: {dict(verif)}")
print(f"quality_tier: {dict(tier)}")
print('SAVED scripts/p1_provenance_audit.json')
