import json

with open("scripts/chem_batches/batch_1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("scripts/chem_batches/batch_1_overview.txt", "w", encoding="utf-8") as out:
    for i, q in enumerate(data):
        out.write(f"=== Q{i+1}: {q['content']} ===\n")
        out.write(f"Category: {q.get('category', '')}\n")
        out.write(f"Correct: {', '.join(q['correct_answers'])}\n")
        for opt in q['options']:
            mark = "[X]" if opt['id'] in q['correct_answers'] else "[ ]"
            out.write(f"  {mark} {opt['id']}: {opt['text']}\n")
        out.write("\n")
print("Written overview successfully!")
