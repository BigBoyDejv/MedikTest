import json

with open("biologia_otazky_1_450.json", "r", encoding="utf-8") as f:
    qs = json.load(f)

for q in qs[:5]:
    print("=" * 60)
    print(q["content"])
    for opt in q["options"]:
        mark = "[X]" if opt["id"] in q["correct_answers"] else "[ ]"
        print(f"  {mark} {opt['id'].upper()}) {opt['text']}")

