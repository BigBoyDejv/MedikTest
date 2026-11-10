import json

with open('scripts/chem_batches/batch_6.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

with open('scripts/chem_batches/batch_6_readable.txt', 'w', encoding='utf-8') as out:
    for i, q in enumerate(questions):
        out.write(f"=== QUESTION {i+1} (idx {i}) ===\n")
        out.write(f"Content: {q['content']}\n")
        out.write(f"Correct: {q['correct_answers']}\n")
        for opt in q['options']:
            mark = '*' if opt['id'] in q['correct_answers'] else ' '
            out.write(f" [{mark}] {opt['id']}: {opt['text']}\n")
        out.write("\n")

print(f"Dumped {len(questions)} questions.")
