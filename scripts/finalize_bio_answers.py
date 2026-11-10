import json

with open("data_bio_answers_451_1500.json", "r", encoding="utf-8") as f:
    answers = json.load(f)

manual_additions = {
    "486": ["a", "c", "d"],
    "489": ["a", "c", "e", "h"],
    "547": [], # Official key has blank
    "614": ["e"],
    "780": [], # Official key has blank
    "807": ["b"],
    "984": ["c"],
    "1067": ["c"],
    "1200": ["c"],
    "1367": ["c"],
    "1381": ["c"],
    "1480": ["b", "c", "e", "f", "h"],
    "1481": ["b", "c", "d"],
    "1482": ["b", "c", "e", "f", "g"],
    "1483": ["c", "d", "g"],
    "1484": ["d", "e", "g", "h"],
    "1485": ["a", "c", "d", "e", "g", "h"],
    "1486": ["b", "c", "f", "h"],
    "1487": ["b"],
    "1488": ["b", "d", "g", "h"],
    "1489": ["c", "d", "f"],
    "1490": ["b", "c", "d", "f", "g"],
    "1491": ["b", "c", "e"],
    "1492": ["a", "d", "e", "f"],
    "1493": ["b", "e", "f"],
    "1494": ["c", "d", "e", "f"],
    "1495": ["b", "d", "g", "h"],
    "1496": ["c", "d", "e", "h"],
    "1497": ["a", "d", "e", "h"],
    "1498": ["b", "c", "e"],
    "1499": ["c", "e", "f", "g", "h"],
    "1500": ["a", "c", "d", "e"]
}

for k, v in manual_additions.items():
    answers[k] = sorted(list(set(v)))

# Sort keys numerically
sorted_answers = {str(k): answers[str(k)] for k in sorted([int(x) for x in answers.keys()])}

with open("data_bio_answers_451_1500.json", "w", encoding="utf-8") as f:
    json.dump(sorted_answers, f, ensure_ascii=False, indent=2)

missing = [n for n in range(451, 1501) if str(n) not in sorted_answers]
print(f"Total verified answers in data_bio_answers_451_1500.json: {len(sorted_answers)}/1050!")
print(f"Missing answers: {len(missing)} -> {missing}")

