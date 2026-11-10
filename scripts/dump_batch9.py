import json

with open('scripts/bio_batches/batch_9.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('scripts/bio_batches/batch_9_readable.txt', 'w', encoding='utf-8') as out:
    for i, q in enumerate(data):
        out.write(f"=== Q{i+401}: {q.get('content')} ===\n")
        out.write(f"Correct: {q.get('correct_answers')}\n")
        for opt in q.get('options', []):
            mark = "[X]" if opt['id'] in q.get('correct_answers', []) else "[ ]"
            out.write(f"  {mark} {opt['id']}: {opt['text']}\n")
        out.write("\n")

print(f"Dumped {len(data)} questions.")
