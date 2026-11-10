import fitz, io, json, re
import numpy as np
from PIL import Image
from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()
doc = fitz.open("Biológia 2026.pdf")

sys_issues = [1260, 1265, 1267, 1271, 1275, 1281, 1285, 1286, 1297, 1298, 1302, 1303, 1311, 1312, 1313, 1316, 1321, 1322, 1326, 1332, 1336, 1337, 1340, 1341, 1352, 1362]

with open("data/ocr_cache_bio_system_1251_1365.json", "r", encoding="utf-8") as f:
    c_sys = json.load(f)

# For each issue question, let's look at all blocks on the page where it resides and the next page
print("=== DUMPING RAW OCR TEXT FOR ALL 26 ISSUES ===")
for q in sys_issues:
    # search q in c_sys
    found_p = None
    for p, blocks in c_sys.items():
        for b in blocks:
            if re.match(rf"^{q}[\.\,\:]", b[2]):
                found_p = int(p)
                break
        if found_p:
            break
    print(f"\n--- QUESTION {q} (Page {found_p}) ---")
    if found_p:
        # print blocks around it
        p_blocks = sorted(c_sys.get(str(found_p), []), key=lambda x: (x[1], x[0]))
        # also next page top blocks
        next_blocks = sorted(c_sys.get(str(found_p + 1), []), key=lambda x: (x[1], x[0]))[:10]
        # find index of q
        q_idx = -1
        for idx, b in enumerate(p_blocks):
            if re.match(rf"^{q}[\.\,\:]", b[2]):
                q_idx = idx
                break
        if q_idx != -1:
            for b in p_blocks[q_idx:q_idx+25]:
                print(f"  P{found_p} ({b[0]}, {b[1]}): {b[2]}")
            for b in next_blocks:
                print(f"  P{found_p+1} ({b[0]}, {b[1]}): {b[2]}")
        else:
            print(f"  q_idx not found directly, showing all blocks on P{found_p} with {q}:")
            for b in p_blocks:
                if str(q) in b[2]:
                    print(f"  {b}")
    else:
        print(f"  Page not found directly in cache")

