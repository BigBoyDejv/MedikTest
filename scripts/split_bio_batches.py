import json
import os

os.makedirs("scripts/bio_batches", exist_ok=True)

with open("biologia_otazky_1_450.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

print(f"Total questions: {len(questions)}")

batch_size = 50
for i in range(0, len(questions), batch_size):
    batch_num = (i // batch_size) + 1
    batch_qs = questions[i:i + batch_size]
    out_path = f"scripts/bio_batches/batch_{batch_num}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(batch_qs, f, ensure_ascii=False, indent=2)
    print(f"Wrote batch {batch_num}: {len(batch_qs)} questions -> {out_path}")
