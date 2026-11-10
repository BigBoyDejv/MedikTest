import fitz, io
from PIL import Image
from rapidocr_onnxruntime import RapidOCR
import numpy as np

engine = RapidOCR()
doc = fitz.open("Biológia 2026.pdf")

def read_box(p_num, y1, y2, x1=80, x2=1450):
    p = doc[p_num - 1].get_pixmap(dpi=200)
    img = Image.open(io.BytesIO(p.tobytes()))
    crop = img.crop((x1, y1, x2, y2))
    nw = int(crop.width * (48.0 / crop.height))
    res, _ = engine.text_recognizer([np.array(crop.resize((nw, 48), Image.Resampling.LANCZOS))])
    return res[0][0] if (res and res[0][0]) else ""

print("1488 f (P308 y=500-550):", read_box(308, 500, 550))
print("1491 b (P308 y=1590-1640):", read_box(308, 1590, 1640))
print("1433 b (P296 y=1770-1825):", read_box(296, 1770, 1825))
print("1434 f (P297 y=460-520):", read_box(297, 460, 520))
print("1445 a (P299 y=545-605):", read_box(299, 545, 605))
print("1425 a (P295 y=250-310):", read_box(295, 250, 310))
print("1425 b (P295 y=340-400):", read_box(295, 340, 400))
print("1485 a (P307 y=915-975):", read_box(307, 915, 975))
print("1401 g (P289/P290 y=340-400):", read_box(290, 340, 400))
print("1390 e (P288 y=560-620):", read_box(288, 560, 620, x1=850))

