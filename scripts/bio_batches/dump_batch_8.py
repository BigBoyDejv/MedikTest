import json

data = json.load(open('scripts/bio_batches/batch_8.json', encoding='utf-8'))
with open('scripts/bio_batches/batch_8_overview.txt', 'w', encoding='utf-8') as f:
    for i, q in enumerate(data):
        f.write(f"=== {i+1}. {q['content']} ===\n")
        f.write(f"CORRECT: {q['correct_answers']}\n")
        for opt in q['options']:
            mark = '*' if opt['id'] in q['correct_answers'] else ' '
            f.write(f" [{mark}] {opt['id']}: {opt['text']}\n")
        f.write('\n')
print("Done overview, total questions:", len(data))
