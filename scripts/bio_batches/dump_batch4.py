import json

data = json.load(open('scripts/bio_batches/batch_4.json', encoding='utf-8'))
with open('scripts/bio_batches/batch_4_readable.txt', 'w', encoding='utf-8') as f:
    for i, q in enumerate(data):
        qid = q.get('id', '-')
        f.write(f"=== #{i+1} (Q: {q['content']}) ===\n")
        f.write(f"Correct: {q['correct_answers']}\n")
        for opt in q['options']:
            f.write(f"  {opt['id']}) {opt['text']}\n")
        f.write("\n")

print(f"Dumped {len(data)} questions to scripts/bio_batches/batch_4_readable.txt")
