import json

with open('scripts/bio_batches/batch_6.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('scripts/bio_batches/batch_6_readable.txt', 'w', encoding='utf-8') as out:
    for i, q in enumerate(data):
        out.write(f"=== Otázka {i+1} ({q['content']}) ===\n")
        out.write(f"Správne odpovede: {q['correct_answers']}\n")
        for opt in q['options']:
            mark = "[X]" if opt['id'] in q['correct_answers'] else "[ ]"
            out.write(f"  {mark} {opt['id']}) {opt['text']}\n")
        out.write("\n")
print(f"Dumped {len(data)} questions.")
