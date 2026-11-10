import fitz
import io
import json
import numpy as np
from PIL import Image

with open("data/ekologia_evolucia_1366_1500.json", "r", encoding="utf-8") as f:
    eko_items = {it["content"].split(".")[0]: it for it in json.load(f)}

eko_issues = [1366, 1378, 1390, 1401, 1411, 1424, 1425, 1433, 1434, 1439, 1444, 1445, 1449, 1459, 1464, 1466, 1468, 1473, 1477, 1483, 1485, 1488, 1491]

for q in eko_issues:
    q_str = str(q)
    curr = eko_items.get(q_str)
    if not curr:
        for k, v in eko_items.items():
            if k.startswith(q_str):
                curr = v
                break
    if not curr:
        print(f"=== Q {q}: NOT FOUND! ===")
        continue
    missing = [o["id"] for o in curr["options"] if o["text"].startswith("Možnosť ")]
    print(f"=== Q {q}: missing {missing} ===")
    print("Content:", curr["content"][:80])
    for o in curr["options"]:
        print(f"  {o['id']}: {o['text']}")

