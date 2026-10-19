#!/usr/bin/env python3
"""EV Hub Top — final QA analysis v2 (correct nested dist layout)."""
import json, os, random, re, glob
import yaml

ROOT = "/root/.openclaw/workspace/repos/electricvehiclehub.top"
VEH = os.path.join(ROOT, "src/content/vehicles")
DIST = os.path.join(ROOT, "dist")
SITE = "https://electricvehiclehub.top"

random.seed(20261019)

vehicles = {}
for fp in sorted(glob.glob(os.path.join(VEH, "*.md"))):
    raw = open(fp, encoding="utf-8").read()
    m = re.match(r"^---\n([\s\S]*?)\n---\n?", raw)
    if not m: continue
    fm = yaml.safe_load(m.group(1))
    body = raw[m.end():]
    slug = fm.get("slug") or os.path.basename(fp)[:-3]
    vehicles[slug] = {"fm": fm, "body": body, "file": os.path.basename(fp)}

print(f"TOTAL vehicle files: {len(vehicles)}")

# ── 1. HS code vs powertrain ──
hs_expected = {"BEV":"87038000","PHEV":"870340","EREV":"870340","HEV":"870340","ICE":"87032200"}
hs_bad, hs_missing = [], []
pt_counts = {}
for slug, v in vehicles.items():
    fm = v["fm"]; pt = fm.get("powertrain"); pt_counts[pt] = pt_counts.get(pt,0)+1
    hs = fm.get("hs_code"); exp = hs_expected.get(pt)
    if not hs: hs_missing.append(slug)
    elif exp and str(hs) != exp: hs_bad.append((slug,pt,hs,exp))
print(f"\n[HS] dist={pt_counts} missing={len(hs_missing)} mismatch={len(hs_bad)}")
for x in hs_bad[:40]: print("   ", x)

# ── 2. Five-section core fields ──
core = ["battery_type","drive_type","motor_type","battery_thermal","suspension_front",
        "suspension_rear","charging_interface","charging_adapter","certification_notes","hs_code"]
missing_core = {}
for slug, v in vehicles.items():
    miss = [f for f in core if v["fm"].get(f) in (None,"")]
    if miss: missing_core[slug] = miss
print(f"\n[CORE FIELDS] vehicles missing any core field: {len(missing_core)}")
for s, m in sorted(missing_core.items()): print(f"    {s}: {m}")

# ── 3. Placeholder residue in md body ──
body_residue = []
for slug, v in vehicles.items():
    b = v["body"]
    for pat, label in [(r"undefined","undefined"),(r"\bnull\b","null"),(r"\bNaN\b","NaN"),
                       (r"\[object Object\]","[object Object]")]:
        for mm in re.finditer(pat, b, re.IGNORECASE):
            body_residue.append((slug,label,mm.group(0)))
print(f"\n[MD BODY RESIDUE] {len(body_residue)} hits")
for x in body_residue[:20]: print("    ", x)

# ── 4. Rendered HTML checks (vehicle detail pages = dist/vehicles/<slug>/index.html) ──
detail_pages = sorted(glob.glob(os.path.join(DIST, "vehicles", "*", "index.html")))
detail_pages = [p for p in detail_pages if os.path.basename(os.path.dirname(p)) != "index"]
print(f"\n[DETAIL PAGES] {len(detail_pages)} vehicle detail HTML")

html_residue, na_pages, schema_issues, canon_bad, og_bad = [], [], [], [], []
offers_total = 0
rating_found = 0

for fp in detail_pages:
    slug = os.path.basename(os.path.dirname(fp))
    html = open(fp, encoding="utf-8").read()
    # residue
    for pat, label in [(r"undefined","undefined"),(r"\bnull\b","null"),(r"\bNaN\b","NaN"),
                       (r"\[object Object\]","[object Object]")]:
        if re.search(pat, html, re.IGNORECASE):
            html_residue.append((slug,label))
            break
    # N/A
    if "N/A" in html:
        na_pages.append(slug)
    # schema JSON-LD
    m = re.search(r'<script type="application/ld\+json"[^>]*>\s*([\s\S]*?)</script>', html)
    if m:
        try:
            ld = json.loads(m.group(1))
            if ld.get("@type") == "Vehicle":
                offers_total += 1
                o = ld.get("offers")
                if not o:
                    schema_issues.append((slug,"Vehicle no offers"))
                else:
                    if o.get("price") in (None,""): schema_issues.append((slug,"offers.price missing"))
                    if o.get("priceCurrency") in (None,""): schema_issues.append((slug,"offers.priceCurrency missing"))
                if ld.get("aggregateRating") or ld.get("rating"):
                    rating_found += 1
                    schema_issues.append((slug,"has aggregateRating (fabricated?)"))
        except Exception as e:
            schema_issues.append((slug,f"JSON parse: {e}"))
    # canonical
    cm = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    if not cm: canon_bad.append((slug,"no canonical"))
    else:
        expect = f"{SITE}/vehicles/{slug}/"
        if cm.group(1) != expect: canon_bad.append((slug,f"canonical={cm.group(1)} exp={expect}"))
    rm = re.search(r'<meta name="robots" content="([^"]+)"', html)
    if rm and "noindex" in rm.group(1): canon_bad.append((slug,f"noindex={rm.group(1)}"))
    # og/meta
    og_img = re.search(r'<meta property="og:image" content="([^"]+)"', html)
    og_title = re.search(r'<meta property="og:title" content="([^"]+)"', html)
    og_desc = re.search(r'<meta property="og:description" content="([^"]+)"', html)
    desc = re.search(r'<meta name="description" content="([^"]+)"', html)
    if not (og_img and og_title and og_desc and desc):
        og_bad.append((slug, f"og_img={bool(og_img)} og_title={bool(og_title)} og_desc={bool(og_desc)} meta_desc={bool(desc)}"))

print(f"[RESIDUE in HTML] {len(html_residue)} pages")
for x in html_residue[:20]: print("    ", x)
print(f"[N/A RENDERED] {len(na_pages)} pages contain 'N/A'")
print(f"[SCHEMA] Vehicle JSON-LD found: {offers_total}, issues: {len(schema_issues)}, rating found: {rating_found}")
for x in schema_issues[:30]: print("    ", x)
print(f"[CANONICAL/ROBOTS] issues: {len(canon_bad)}")
for x in canon_bad[:20]: print("    ", x)
print(f"[OG/META] issues: {len(og_bad)}")
for x in og_bad[:20]: print("    ", x)

# ── 5. Sitemap reconciliation (correct) ──
sx = open(os.path.join(DIST, "sitemap-0.xml"), encoding="utf-8").read()
sitemap_urls = set(re.findall(r"<loc>([^<]+)</loc>", sx))
print(f"\n[SITEMAP] total urls: {len(sitemap_urls)}")

veh_exp = {f"{SITE}/vehicles/{s}/" for s in vehicles}
print(f"  vehicles in sitemap: {len(veh_exp & sitemap_urls)}/{len(veh_exp)}; missing: {len(veh_exp - sitemap_urls)}")

blog_slugs = set()
for bf in glob.glob(os.path.join(ROOT,"src/content/blog","*.md*")):
    blog_slugs.add(re.sub(r"\.mdx?$","",os.path.basename(bf)))
# published blogs (not draft)
published = set()
for bf in glob.glob(os.path.join(ROOT,"src/content/blog","*.md*")):
    raw = open(bf, encoding="utf-8").read()
    if re.search(r"^draft:\s*true", raw, re.M): continue
    published.add(re.sub(r"\.mdx?$","",os.path.basename(bf)))
drafts = blog_slugs - published
print(f"  blog files: {len(blog_slugs)}, published: {len(published)}, drafts: {len(drafts)}")
blog_exp = {f"{SITE}/blog/{s}/" for s in published}
print(f"  published blogs in sitemap: {len(blog_exp & sitemap_urls)}/{len(blog_exp)}; missing: {len(blog_exp - sitemap_urls)}")
for u in sorted(blog_exp - sitemap_urls)[:20]: print("     MISSING:", u)
print(f"  drafts: {sorted(drafts)}")

for u in [f"{SITE}/", f"{SITE}/vehicles/", f"{SITE}/brands/", f"{SITE}/blog/"]:
    print(f"  index {'OK' if u in sitemap_urls else 'MISSING'}: {u}")

# dist html overall (all html, exclude error + noindex)
dist_urls = set()
for fp in glob.glob(os.path.join(DIST,"**","*.html"), recursive=True):
    rel = os.path.relpath(fp, DIST)
    if rel in ("404.html","500.html"): continue
    if "index.html" in rel:
        path = os.path.dirname(rel)
    else:
        path = rel[:-5]
    if not path: path = ""
    dist_urls.add(f"{SITE}/{path}/")
print(f"  dist HTML (non-error): {len(dist_urls)}")
noindex_pfx = ("/blog/page/","/blog/tag/")
missing_sitemap = []
for u in sorted(dist_urls):
    if u in sitemap_urls: continue
    p = u.replace(SITE,"")
    if any(p.startswith(x) for x in noindex_pfx): continue
    missing_sitemap.append(u)
print(f"  dist pages absent from sitemap (excl noindex page/tag): {len(missing_sitemap)}")
for u in missing_sitemap[:60]: print("    ", u)

# ── 6. Orphan detection (indexes) ──
print("\n[ORPHAN]")
idx = {
  "home": open(os.path.join(DIST,"index.html"),encoding="utf-8").read(),
  "vehicles_index": open(os.path.join(DIST,"vehicles","index.html"),encoding="utf-8").read(),
  "brands_index": open(os.path.join(DIST,"brands","index.html"),encoding="utf-8").read(),
  "blog_index": open(os.path.join(DIST,"blog","index.html"),encoding="utf-8").read(),
}
linked = set()
for name, h in idx.items():
    f = set(re.findall(r'href="/vehicles/([^/"#]+)/"', h))
    linked |= f
    print(f"  {name}: {len(f)} vehicle links")
orphans = set(vehicles) - linked
print(f"  linked total: {len(linked)}, ORPHANS: {len(orphans)}")
for s in sorted(orphans): print("    ", s)

# brand pages link their vehicles?
brand_orphan = []
for fp in sorted(glob.glob(os.path.join(DIST,"brands","*","index.html"))):
    brand_slug = os.path.basename(os.path.dirname(fp))
    if brand_slug == "index": continue
    h = open(fp,encoding="utf-8").read()
    bv = {s for s,v in vehicles.items() if v["fm"].get("brand")==brand_slug}
    lk = set(re.findall(r'href="/vehicles/([^/"#]+)/"', h))
    miss = bv - lk
    if miss: brand_orphan.append((brand_slug, sorted(miss)))
print(f"  brands missing own-vehicle links: {len(brand_orphan)}")
for b,m in brand_orphan[:20]: print(f"    {b}: {m}")

print("\n=== DONE ===")
