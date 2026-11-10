import json

with open("scripts/chem_batches/batch_1.json", "r", encoding="utf-8") as f:
    d = json.load(f)

for q in d[:3]:
    print("=" * 60)
    print(q["content"])
    for opt in q["options"]:
        mark = "[X]" if opt["id"] in q["correct_answers"] else "[ ]"
        print(f"  {mark} {opt['id'].upper()}) {opt['text']}")

