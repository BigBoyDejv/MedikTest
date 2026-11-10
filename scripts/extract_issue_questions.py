import fitz
import io
import json
import numpy as np
from PIL import Image
from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()
doc = fitz.open("Biológia 2026.pdf")

with open("data/system_rastlin_zivocichov_1251_1365.json", "r", encoding="utf-8") as f:
    sys_items = {it["content"].split(".")[0]: it for it in json.load(f)}

sys_issues = [1260, 1265, 1267, 1271, 1275, 1281, 1285, 1286, 1297, 1298, 1302, 1303, 1311, 1312, 1313, 1316, 1321, 1322, 1326, 1332, 1336, 1337, 1340, 1341, 1352, 1362]

with open("data/ocr_cache_bio_system_1251_1365.json", "r", encoding="utf-8") as f:
    c_sys = json.load(f)

for q in sys_issues:
    q_str = str(q)
    curr = sys_items.get(q_str)
    missing = [o["id"] for o in curr["options"] if o["text"].startswith("Možnosť ")]
    print(f"=== Q {q}: missing {missing} ===")
    print("Content:", curr["content"][:80])
    for o in curr["options"]:
        print(f"  {o['id']}: {o['text']}")

