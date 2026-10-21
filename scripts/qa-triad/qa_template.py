#!/usr/bin/env python3
"""EVHub Top QA Triad — Template/originality detection (Overview + description + prose fields)."""
import glob, re, json
from collections import Counter, defaultdict

VEH='src/content/vehicles'; files=sorted(glob.glob(f'{VEH}/*.md'))

def parse(p):
    t=open(p).read(); m=re.match(r'^---\n(.*?)\n---\n',t,re.DOTALL)
    if not m: return {},'',t
    fm=m.group(1); body=t[m.end():]
    d={}
    for ln in fm.split('\n'):
        mm=re.match(r'^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$',ln)
        if mm: d[mm.group(1)]=mm.group(2).strip()
    return d,fm,body

def get_overview(body):
    i=body.find('## Overview')
    if i<0: return ''
    rest=body[i+len('## Overview'):]
    nxt=re.search(r'\n## ',rest)
    return rest[:nxt.start()].strip() if nxt else rest.strip()

def mask(s, title='', brand=''):
    """Mask numbers, title, brand -> skeleton."""
    s=s.replace(title,' {TITLE} ').replace(brand,' {BRAND} ').replace(brand.upper(),' {BRAND} ')
    s=re.sub(r'\$[\d,.]+',' {PRICE} ',s)
    s=re.sub(r'\b\d+(\.\d+)?%?([,\d\.]*)\b',' {N} ',s)
    s=re.sub(r'\s+',' ',s).strip()
    return s

def sentences(txt):
    txt=re.sub(r'\s+',' ',txt).strip()
    # split on sentence boundaries
    parts=re.split(r'(?<=[.!?])\s+', txt)
    return [p.strip() for p in parts if len(p.strip())>15]

# collect overview sentences + skeletons
ov_sent_counter=Counter()       # exact sentence -> count (verbatim reuse)
ov_skel_counter=Counter()       # masked skeleton -> count
ov_skel_files=defaultdict(list) # skeleton -> files
desc_counter=Counter()
desc_skel=Counter()
desc_skel_files=defaultdict(list)
cert_counter=Counter()
adapter_counter=Counter()

for f in files:
    d,fm,body=parse(f)
    slug=f.split('/')[-1][:-3]
    title=d.get('title','').strip('"')
    brand=d.get('brand','').strip('"')
    ov=get_overview(body)
    for s in sentences(ov):
        ov_sent_counter[s]+=1
        sk=mask(s,title,brand)
        ov_skel_counter[sk]+=1
        ov_skel_files[sk].append(slug)
    desc=d.get('description','').strip('"')
    desc_counter[desc]+=1
    sk=mask(desc,title,brand)
    desc_skel[sk]+=1
    desc_skel_files[sk].append(slug)
    cert_counter[d.get('certification_notes','').strip('"')]+=1
    adapter_counter[d.get('charging_adapter','').strip('"')]+=1

# ---- verbatim reused sentence pairs (exact, with real numbers) ----
reused = {s:c for s,c in ov_sent_counter.items() if c>=2}
# ---- skeleton reuse (masked) ----
skel_reuse = {s:c for s,c in ov_skel_counter.items() if c>=2}

# template rate: fraction of overview SENTENCES whose masked skeleton appears in >=2 files
total_ov_sentences=sum(ov_sent_counter.values())
templated_sentences=sum(c for s,c in ov_skel_counter.items() if ov_skel_counter[s]>=2)

print(f'Overview total sentences: {total_ov_sentences}')
print(f'Overview unique exact sentences: {len(ov_sent_counter)}')
print(f'Exact verbatim-reused sentences (>=2 files): {len(reused)}')
print(f'Overview unique masked skeletons: {len(ov_skel_counter)}')
print(f'Skeleton-reused sentences (>=2 files): {sum(1 for s,c in ov_skel_counter.items() if c>=2)}')
print(f'Template rate (templated sentences / total sentences): {templated_sentences/total_ov_sentences*100:.1f}%')

print('\n=== TOP OVERVIEW SKELETONS (masked, reused >=2) ===')
for s,c in sorted(skel_reuse.items(), key=lambda x:-x[1])[:20]:
    print(f'{c:>4}  {s[:140]}')

print('\n=== DESCRIPTION: exact duplicates (top 10) ===')
for d,c in desc_counter.most_common(10):
    print(f'{c:>4}  {d[:110]}')

print('\n=== DESCRIPTION skeleton reuse: top 10 ===')
for s,c in desc_skel.most_common(10):
    print(f'{c:>4}  {s[:130]}')

print('\n=== CERTIFICATION NOTES: exact duplicates (top 15) ===')
for d,c in cert_counter.most_common(15):
    print(f'{c:>4}  {d[:120]}')

print('\n=== CHARGING ADAPTER: exact duplicates (top 15) ===')
for d,c in adapter_counter.most_common(15):
    print(f'{c:>4}  {d[:120]}')

json.dump({
 'overview_total_sentences': total_ov_sentences,
 'overview_unique_exact': len(ov_sent_counter),
 'verbatim_reused': {s:c for s,c in reused.items()},
 'skeleton_reused': {s:{'count':c,'files':files2} for s,(c,files2) in
                     [(s,(ov_skel_counter[s],ov_skel_files[s])) for s,_ in skel_reuse.most_common()]},
 'template_rate_pct': round(templated_sentences/total_ov_sentences*100,1),
 'description_dupes': dict(desc_counter.most_common(20)),
 'cert_dupes': dict(cert_counter.most_common(20)),
 'adapter_dupes': dict(adapter_counter.most_common(20)),
}, open('scripts/qa-triad/_template.json','w'), indent=1, ensure_ascii=False)
print('\nSAVED _template.json')
