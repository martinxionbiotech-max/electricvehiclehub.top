#!/usr/bin/env python3
"""EVHub Top QA Triad — Data accuracy: cross-check vs CNEVhub (.net) base + HS code + landed_cost recompute."""
import glob, re, json, os
from collections import Counter, defaultdict

TOP='src/content/vehicles'
NET='/root/.openclaw/workspace/repos/CNEVhub/src/content/vehicles'

def parse(p):
    t=open(p).read(); m=re.match(r'^---\n(.*?)\n---\n',t,re.DOTALL)
    if not m: return {},t
    fm=m.group(1); d={}
    for ln in fm.split('\n'):
        mm=re.match(r'^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$',ln)
        if mm: d[mm.group(1)]=mm.group(2).strip()
    return d,fm

def num(v):
    try:
        s=v.strip().strip('"').strip("'")
        if s in ('null','None',''): return None
        return float(s)
    except: return None

# base fields to cross-check
BASE=['price_usd','battery_kwh','motor_power_kw','torque_nm','range_cltc_km',
      'length_mm','width_mm','height_mm','wheelbase_mm','weight_kg',
      'accel_0_100_s','top_speed_kmh','efficiency_kwh_100km','powertrain','type']

top_files={f.split('/')[-1]:f for f in glob.glob(f'{TOP}/*.md')}
net_files={f.split('/')[-1]:f for f in glob.glob(f'{NET}/*.md')}
print(f'top files={len(top_files)}  net files={len(net_files)}')

mismatches=[]  # (slug, field, top_val, net_val)
missing_net=[] # slug not in net
for slug, f in sorted(top_files.items()):
    if slug not in net_files:
        missing_net.append(slug); continue
    dtop,_=parse(f); dnet,_=parse(net_files[slug])
    for fld in BASE:
        tv=dtop.get(fld); nv=dnet.get(fld)
        # compare raw (string) to catch formatting drift too; numeric where possible
        if tv is None and nv is None: continue
        if tv is None or nv is None:
            mismatches.append((slug,fld,tv,nv,'one-sided')); continue
        tn=num(tv); nn=num(nv)
        if tn is not None and nn is not None:
            if abs(tn-nn)>0.005:
                mismatches.append((slug,fld,tv,nv,'num'))
        else:
            if tv.strip('"').strip("'").strip()!=nv.strip('"').strip("'").strip():
                mismatches.append((slug,fld,tv,nv,'str'))

print(f'\nBase-field mismatches (top vs net): {len(mismatches)}')
for m in mismatches[:60]:
    print('  ', m)

# ---- HS code × powertrain full rerun ----
hs_rules={'BEV':'87038000','PHEV':'870340','EREV':'870340','HEV':'870340','ICE':'87032200'}
hs_err=[]; hs_dist=Counter()
for slug,f in sorted(top_files.items()):
    d,_=parse(f); pt=d.get('powertrain'); hs=d.get('hs_code')
    hs_dist[pt]+=1
    exp=hs_rules.get(pt)
    if exp is None:
        continue
    if hs!=exp:
        hs_err.append((slug,pt,hs,exp))
print(f'\nHS code × powertrain: distribution={dict(hs_dist)}')
print(f'HS code mismatches: {len(hs_err)}')
for e in hs_err[:30]: print('  ',e)

# ---- landed_cost recompute (Germany): base + duty + vat + freight + clearance + cert + reg + inland ----
def recompute(d):
    lc=d.get('landed_cost')
    if not lc: return None
    try: lc=json.loads(lc)
    except: return 'parse-err'
    b=lc.get('breakdown',{})
    base=num(d.get('price_usd'))
    if base is None: return 'no-base'
    items=[b.get('duty_cif_usd'),b.get('countervailing_duty_usd'),b.get('vat_usd'),
           b.get('freight_roro_usd'),b.get('customs_clearance_usd'),b.get('certification_usd'),
           b.get('registration_usd'),b.get('inland_transport_usd')]
    if any(v is None for v in items): return 'missing-items'
    total=sum(items)
    return {'stored':lc.get('total_landed_usd'),'recomputed':round(total,2),'diff':round(total-(lc.get('total_landed_usd') or 0),2)}

import random
random.seed(20261021)
sample=random.sample(sorted(top_files.items()),5)
print('\n=== landed_cost Germany recompute (5 sample) ===')
for slug,f in sample:
    d,_=parse(f); r=recompute(d)
    print(f'  {slug}: {r}')

json.dump({
 'base_mismatches': mismatches,
 'missing_net': missing_net,
 'hs_distribution': dict(hs_dist),
 'hs_errors': hs_err,
}, open('scripts/qa-triad/_accuracy.json','w'), indent=1, ensure_ascii=False)
print('\nSAVED _accuracy.json')
