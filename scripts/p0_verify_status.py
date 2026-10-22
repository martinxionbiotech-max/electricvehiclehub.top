#!/usr/bin/env python3
"""P0 data verification batch (corrected) — apply verification_status to all 40
sampled vehicles + fix the malformed quote from the first run. Idempotent.
"""
import re, os

ROOT = os.path.join(os.path.dirname(__file__), "..")

STATUS = {
    "bestune-pony": "partial", "byd-seagull": "partial", "byd-dolphin": "partial",
    "byd-atto-3": "partial", "byd-seal": "partial", "byd-han": "partial",
    "byd-song-plus-dm-i": "partial", "byd-qin-l-dm-i": "unverifiable",
    "byd-sealion-07": "partial", "chery-tiggo-9": "partial", "chery-fulwin-a9": "partial",
    "chery-new-energy-eq1": "partial", "chery-explore-06-c-dm": "unverifiable",
    "exeed-exlantix-es": "partial", "jetour-shanhai-l7": "partial",
    "geely-galaxy-e5": "partial", "geely-galaxy-e8": "partial",
    "geely-monjaro": "partial", "geely-galaxy-l7": "partial",
    "geely-galaxy-starshine-7": "partial", "xiaomi-su7": "partial",
    "xiaomi-yu7": "partial", "xiaomi-su7-ultra": "partial",
    "yangwang-u8": "partial", "yangwang-u7": "verified",
    "m-hero-917": "partial", "fangchengbao-bao-5": "partial",
    "tank-700": "partial", "wey-lanshan": "partial", "avatr-12": "partial",
    "zeekr-001": "partial", "nio-es8": "verified", "xpeng-g6": "partial",
    "aion-y": "partial", "wuling-hongguang-mini-ev": "partial",
    "mg-4": "partial", "denza-z9-gt": "partial", "leapmotor-c10": "partial",
    "haval-jolion-pro": "partial", "changan-nevo-lamore": "partial",
}

DATE = "2026-10-22"

for slug, status in STATUS.items():
    path = os.path.join(ROOT, "src/content/vehicles", f"{slug}.md")
    raw = open(path).read()
    m = re.match(r"^---\n(.*?)\n---\n", raw, re.S)
    fm = m.group(1)
    # 1. fix malformed quote from first run:  verification_status: \"partial"  ->  "partial"
    fm = re.sub(r'^verification_status:\s*\\?"?([a-z]+)"?$',
                r'verification_status: "\1"', fm, flags=re.M)
    # 2. if still absent, insert after data_reviewed
    if not re.search(r'^verification_status:', fm, re.M):
        fm = re.sub(r'(^data_reviewed:.*$)',
                    f'\\1\nverification_status: "{status}"',
                    fm, flags=re.M)
    else:
        fm = re.sub(r'^verification_status:.*$',
                    f'verification_status: "{status}"', fm, flags=re.M)
    # 3. bump data_updated
    fm = re.sub(r'^data_updated:.*$', f'data_updated: "{DATE}"', fm, flags=re.M)
    start = raw.index("---\n") + 4
    end = raw.index("\n---\n", 4)
    open(path, "w").write(raw[:start] + fm + raw[end:])

print("done")
