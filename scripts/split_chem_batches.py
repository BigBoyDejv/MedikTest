import json
import os

os.makedirs("scripts/chem_batches", exist_ok=True)

with open("chemia_otazky_1_300.json", "r", encoding="utf-8") as f:
    q1 = json.load(f)

with open("chemia_otazky_301_450.json", "r", encoding="utf-8") as f:
    q2 = json.load(f)

all_chem_450 = q1 + q2
print(f"Total chem questions: {len(all_chem_450)}")

batch_size = 50
for i in range(0, len(all_chem_450), batch_size):
    batch_num = (i // batch_size) + 1
    batch_qs = all_chem_450[i:i + batch_size]
    out_path = f"scripts/chem_batches/batch_{batch_num}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(batch_qs, f, ensure_ascii=False, indent=2)
    print(f"Wrote chem batch {batch_num}: {len(batch_qs)} questions -> {out_path}")

