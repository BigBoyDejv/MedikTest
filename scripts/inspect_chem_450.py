import json
import re

files = [
    "chemia_otazky_1_300.json",
    "chemia_otazky_301_450.json",
    "chemia_otazky_641_1500.json"
]

all_chem = []
for fname in files:
    with open(fname, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"File {fname}: {len(data)} items")
    for q in data:
        # extract leading number
        m = re.match(r"^(\d+)\.", q["content"].strip())
        num = int(m.group(1)) if m else None
        all_chem.append((num, q))

all_chem.sort(key=lambda x: (x[0] if x[0] is not None else 99999))
print(f"Total chem questions: {len(all_chem)}")
first_450 = [q for num, q in all_chem if num is not None and 1 <= num <= 450]
print(f"Questions numbered 1 to 450: {len(first_450)}")
if first_450:
    print("Min num:", re.match(r"^(\d+)\.", first_450[0]["content"]).group(1))
    print("Max num:", re.match(r"^(\d+)\.", first_450[-1]["content"]).group(1))

