import fitz, io, json, re
import numpy as np
from PIL import Image
from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()
doc = fitz.open("Biológia 2026.pdf")

def read_line(p_num, y1, y2, x1=80, x2=1450):
    page = doc[p_num - 1]
    pix = page.get_pixmap(dpi=200)
    img = Image.open(io.BytesIO(pix.tobytes()))
    crop = img.crop((x1, y1, x2, y2))
    nw = int(crop.width * (48.0 / crop.height))
    res, _ = engine.text_recognizer([np.array(crop.resize((nw, 48), Image.Resampling.LANCZOS))])
    if res and res[0][0]:
        return res[0][0].strip()
    return ""

# Let's check 1340 on page 279 (between y=1640 and 1730)
print("1340 d on p279:", read_line(279, 1660, 1720))

# 1285 a on p268 (between y=1520 and 1600)
print("1285 a on p268:", read_line(268, 1540, 1600))

# 1286 b and d on p268 (between y=2000 and 2200)
print("1286 b on p268:", read_line(268, 2040, 2100))
print("1286 d on p268:", read_line(268, 2120, 2180))

# 1302 f on p271
print("1302 f on p271:", read_line(271, 1480, 1560))

# 1303 h on p271
print("1303 h on p271:", read_line(271, 2100, 2200))

# 1311 e and h on p273
print("1311 e on p273:", read_line(273, 1100, 1180))
print("1311 h on p273:", read_line(273, 1260, 1340))

