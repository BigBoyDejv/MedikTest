import fitz
import numpy as np
from rapidocr_onnxruntime import RapidOCR
from PIL import Image
import io
import re

ocr = RapidOCR()

doc = fitz.open("Biológia 2026.pdf")
print("Total pages in Biológia 2026.pdf:", len(doc))

# Check first 8 pages for Obsah and where Question 1 starts
for p in range(0, 8):
    pix = doc[p].get_pixmap(dpi=110)
    img = Image.open(io.BytesIO(pix.tobytes()))
    res, _ = ocr(np.array(img))
    lines = [r[1].strip() for r in res] if res else []
    print(f"Page {p+1} first 6 lines:", lines[:6])

# Check where Q450 is (likely around page 85-105)
for p in [75, 85, 90, 95, 100, 105]:
    if p < len(doc):
        pix = doc[p].get_pixmap(dpi=110)
        img = Image.open(io.BytesIO(pix.tobytes()))
        res, _ = ocr(np.array(img))
        lines = [r[1].strip() for r in res] if res else []
        q_nums = [int(m.group(1)) for l in lines for m in [re.match(r'^(\d+)\.', l)] if m]
        print(f"Page {p+1} question numbers:", q_nums)

# Check last 15 pages for Answer Keys (Kľúč)
for p in range(len(doc) - 15, len(doc)):
    pix = doc[p].get_pixmap(dpi=100)
    img = Image.open(io.BytesIO(pix.tobytes()))
    res, _ = ocr(np.array(img))
    lines = [r[1].strip() for r in res] if res else []
    nums = [int(m.group(1)) for l in lines for m in [re.match(r'^(\d+)\.?$', l)] if m and int(m.group(1)) <= 1600]
    print(f"End page {p+1}: count_nums={len(nums)}, min={min(nums) if nums else None}, max={max(nums) if nums else None}, header={lines[:3]}")

