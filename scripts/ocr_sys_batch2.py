import fitz, io
from PIL import Image
from rapidocr_onnxruntime import RapidOCR
import numpy as np

engine = RapidOCR()
doc = fitz.open("Biológia 2026.pdf")

def ocr_full(p_num, y1, y2):
    p = doc[p_num - 1].get_pixmap(dpi=200)
    img = Image.open(io.BytesIO(p.tobytes()))
    crop = img.crop((60, y1, 1550, y2))
    res, _ = engine(np.array(crop))
    for r in (res or []):
        print(f"P{p_num}: {r[1]}")

print("=== 1321 & 1322 (P275 & P276) ===")
ocr_full(275, 1800, 2350)
ocr_full(276, 150, 600)

print("=== 1326 (P276 & P277) ===")
ocr_full(276, 1900, 2350)
ocr_full(277, 150, 500)

print("=== 1332 (P277 & P278) ===")
ocr_full(277, 1900, 2350)
ocr_full(278, 150, 500)

print("=== 1336 & 1337 (P278 & P279) ===")
ocr_full(278, 1900, 2350)
ocr_full(279, 150, 600)

print("=== 1352 (P281 & P282) ===")
ocr_full(281, 1900, 2350)
ocr_full(282, 150, 500)

