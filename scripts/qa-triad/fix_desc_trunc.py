#!/usr/bin/env python3
"""Fix deterministic description truncation (standard template completion). Dry-run by default."""
import glob, re, sys, json
TOP='src/content/vehicles'
STD="Full landed-cost breakdown across 7 export markets for B2B import planning."
APPLY = '--apply' in sys.argv

def parse_desc(txt):
    m=re.match(r'^---\n(.*?)\n---\n', txt, re.DOTALL)
    return m

files=sorted(glob.glob(f'{TOP}/*.md'))
across=[]; eudac=[]; other=[]
for f in files:
    txt=open(f).read()
    m=parse_desc(txt)
    fm=m.group(1)
    # extract description line (unquoted)
    dm=re.search(r'^description:\s*"([^"]*)"\s*$', fm, re.MULTILINE)
    if not dm: continue
    desc=dm.group(1); slug=f.split('/')[-1][:-3]
    if desc.endswith('import planning.'): continue  # already complete
    if 'to the EU' in desc or 'DAC' in desc:
        eudac.append(slug); continue
    # longest suffix matching STD prefix
    k=0
    for kk in range(min(len(STD), len(desc)), 7, -1):
        if desc.endswith(STD[:kk]): k=kk; break
    if k>=8:
        across.append((slug, k, desc[-35:]))
    else:
        other.append((slug, desc[-40:]))

print(f'across-variant (deterministic fix): {len(across)}')
print(f'EU/DAC variant (flag): {len(eudac)}')
print(f'other (hand-written, flag): {len(other)}')
print('\n=== other (hand-written) ===')
for s,t in other: print(f'  {s}: ...{t}')

if APPLY:
    fixed=0
    for f in files:
        txt=open(f).read(); m=parse_desc(txt); fm=m.group(1)
        dm=re.search(r'^description:\s*"([^"]*)"\s*$', fm, re.MULTILINE)
        if not dm: continue
        desc=dm.group(1); slug=f.split('/')[-1][:-3]
        if desc.endswith('import planning.'): continue
        if 'to the EU' in desc or 'DAC' in desc: continue
        k=0
        for kk in range(min(len(STD), len(desc)), 7, -1):
            if desc.endswith(STD[:kk]): k=kk; break
        if k>=8:
            new=desc[:len(desc)-k]+STD
            txt2=txt.replace(f'description: "{desc}"', f'description: "{new}"', 1)
            if txt2!=txt:
                open(f,'w').write(txt2); fixed+=1
    print(f'\nAPPLIED: {fixed} descriptions fixed')
else:
    print('\n(dry-run; pass --apply to write)')
