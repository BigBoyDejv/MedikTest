import fitz, io, re
from PIL import Image
from rapidocr_onnxruntime import RapidOCR
import numpy as np

engine = RapidOCR()
doc = fitz.open("Biológia 2026.pdf")

# Ekológia pages: 284 to 311
# Let's inspect 1390, 1401, 1411, 1424, 1425, 1433, 1434, 1439
eko_q_1 = [1390, 1401, 1411, 1424, 1425, 1433, 1434, 1439]

for p_num in range(286, 299):
    p = doc[p_num - 1].get_pixmap(dpi=200)
    img = Image.open(io.BytesIO(p.tobytes()))
    for y in range(150, 2350, 35):
        sub = img.crop((80, y, 1450, y + 40))
        nw = int(sub.width * (48.0 / sub.height))
        res, _ = engine.text_recognizer([np.array(sub.resize((nw, 48)))])
        if res and res[0][0]:
            t = res[0][0]
            for q in eko_q_1:
                if re.match(rf"^{q}[\.\,\:]", t) or f"{q}." in t:
                    print(f"P{p_num} y={y}: {t}")
                    # print next 10 lines
                    for y2 in range(y + 35, y + 400, 35):
                        sub2 = img.crop((80, y2, 1450, y2 + 40))
                        nw2 = int(sub2.width * (48.0 / sub2.height))
                        r2, _ = engine.text_recognizer([np.array(sub2.resize((nw2, 48)))])
                        if r2 and r2[0][0]:
                            print(f"   y={y2}: {r2[0][0]}")
                    break

