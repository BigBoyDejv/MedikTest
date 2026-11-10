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

print("1411 d (P291/292):", read_box(292, 170, 230))
print("1411 e (P291/292):", read_box(292, 230, 290))
print("1424 h (P294/295):", read_box(295, 150, 220))
print("1439 e (P298):", read_box(298, 480, 540))
print("1444 b (P299):", read_box(299, 230, 290))
print("1449 b (P300):", read_box(300, 1400, 1460))
print("1449 c (P300):", read_box(300, 1460, 1520))
print("1459 e (P302):", read_box(302, 330, 390))
print("1464 h (P302):", read_box(302, 1780, 1840))
print("1466 a (P303):", read_box(303, 350, 410))
print("1473 g (P305):", read_box(305, 590, 650))

