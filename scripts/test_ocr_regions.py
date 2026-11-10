import fitz, io, json
import numpy as np
from PIL import Image
from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()
doc = fitz.open("Biológia 2026.pdf")

def ocr_region(page_num, y_start, y_end):
    pix = doc[page_num - 1].get_pixmap(dpi=200)
    img = Image.open(io.BytesIO(pix.tobytes()))
    crop = img.crop((50, y_start, 1550, y_end))
    res, _ = engine(np.array(crop))
    lines = []
    if res:
        for r in res:
            bx = sum(pt[0] for pt in r[0]) / 4.0
            by = sum(pt[1] for pt in r[0]) / 4.0
            lines.append((int(bx), int(by + y_start), r[1]))
    return lines

# Let's inspect 1265 on page 264
print("=== 1265 (page 264, y=1900-2350) ===")
for b in ocr_region(264, 1950, 2350):
    print(b)

# 1267 (page 265)
print("=== 1267 (page 265, y=500-1100) ===")
for b in ocr_region(265, 500, 1100):
    print(b)

