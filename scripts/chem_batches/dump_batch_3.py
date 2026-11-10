import json

data = json.load(open('scripts/chem_batches/batch_3.json', encoding='utf-8'))
with open('scripts/chem_batches/batch_3_overview.txt', 'w', encoding='utf-8') as f:
    for i, q in enumerate(data):
        f.write(f"=== Q{i+1}: {q['content']} ===\n")
        f.write(f"Category: {q.get('category')}\n")
        f.write(f"Correct: {', '.join(q.get('correct_answers', []))}\n")
        for opt in q.get('options', []):
            mark = '[X]' if opt['id'] in q.get('correct_answers', []) else '[ ]'
            f.write(f"  {mark} {opt['id']}: {opt['text']}\n")
        f.write('\n')
print(f"Dumped {len(data)} questions.")
