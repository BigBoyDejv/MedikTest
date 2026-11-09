import json
import re

with open("temp_ocr_lines_112_320.json", "r", encoding="utf-8") as f:
    lines_by_page = json.load(f)

with open("data_answers_641_1500.json", "r", encoding="utf-8") as f:
    answers = json.load(f)

all_lines = []
for p_num in sorted([int(k) for k in lines_by_page.keys()]):
    for l in lines_by_page[str(p_num)]:
        all_lines.append((p_num, l.strip()))

def normalize_leading_num(s):
    m = re.match(r'^([0-9oOlI]{3,4})([\.\,\:\)]?\s*.*)', s)
    if not m:
        return s
    num_part = m.group(1).replace('o', '0').replace('O', '0').replace('l', '1').replace('I', '1')
    if num_part.isdigit():
        return num_part + m.group(2)
    return s

q_start_regex = re.compile(r'^(\d{3,4})[\.\,\:\)]\s*(.*)')
opt_regex = re.compile(r'^([a-hA-H])[\.\,\)\:]\s*(.*)')

parsed_qs = {}
current_q = None
last_line_before_a = None

for p_num, raw_line in all_lines:
    line = normalize_leading_num(raw_line)
    m_q = q_start_regex.match(line)
    if m_q:
        cand_num = int(m_q.group(1))
        rest_text = (m_q.group(2) or "").strip()
        expected_approx = 641 + int((p_num - 112) * (860 / 208.0))
        if 641 <= cand_num <= 1500 and abs(cand_num - expected_approx) < 90:
            if current_q:
                parsed_qs[current_q["num"]] = current_q
            current_q = {
                "num": cand_num,
                "page": p_num,
                "content": f"{cand_num}. {rest_text}".strip(),
                "options_dict": {},
                "current_opt": None
            }
            last_line_before_a = None
            continue

    if current_q:
        m_opt = opt_regex.match(raw_line)
        if m_opt:
            opt_id = m_opt.group(1).lower()
            opt_text = m_opt.group(2).strip()

            # Ak sme uz v aktualnej otazke mali moznosti (napr. f, g alebo h) a znova prichadza 'a', 'b' alebo 'c',
            # znamena to, ze OCR vynechalo cislo nasledujucej otazky (current_q["num"] + 1)!
            if opt_id in ['a', 'b', 'c'] and any(k in current_q["options_dict"] for k in ['f', 'g', 'h']):
                next_num = current_q["num"] + 1
                if 641 <= next_num <= 1500 and next_num not in parsed_qs:
                    # Ak bol na konci predchadzajucej moznosti 'h' priradeny riadok znenia novej otazky, vytiahneme ho
                    inferred_title = f"{next_num}."
                    if last_line_before_a:
                        inferred_title = f"{next_num}. {last_line_before_a}"
                        # Odstranime tento riadok z predoslej moznosti
                        last_opt = current_q["current_opt"]
                        if last_opt and current_q["options_dict"].get(last_opt, "").endswith(last_line_before_a):
                            cleaned = current_q["options_dict"][last_opt][:-len(last_line_before_a)].strip()
                            current_q["options_dict"][last_opt] = cleaned

                    parsed_qs[current_q["num"]] = current_q
                    current_q = {
                        "num": next_num,
                        "page": p_num,
                        "content": inferred_title,
                        "options_dict": {opt_id: opt_text},
                        "current_opt": opt_id
                    }
                    last_line_before_a = None
                    continue

            current_q["options_dict"][opt_id] = opt_text
            current_q["current_opt"] = opt_id
            last_line_before_a = None
        else:
            if current_q["current_opt"]:
                opt_id = current_q["current_opt"]
                prev = current_q["options_dict"].get(opt_id, "")
                current_q["options_dict"][opt_id] = (prev + " " + raw_line).strip()
                if opt_id in ['g', 'h']:
                    last_line_before_a = raw_line
            else:
                current_q["content"] = (current_q["content"] + " " + raw_line).strip()

if current_q and 641 <= current_q["num"] <= 1500:
    parsed_qs[current_q["num"]] = current_q

missing_nums = [n for n in range(641, 1501) if n not in parsed_qs]
print(f"State-machine parser matched: {len(parsed_qs)}/860 questions! Missing: {len(missing_nums)}")
print("Sample missing:", missing_nums[:25])

final_items = []
for num in range(641, 1501):
    category_name = "Organická chémia" if num <= 1150 else "Biochémia"
    correct = answers.get(str(num), [])
    explanation = f"Správne odpovede podľa oficiálneho kľúča testovnice UPJŠ LF sú: {', '.join(a.upper() for a in correct)}."

    if num in parsed_qs:
        q = parsed_qs[num]
        opt_dict = q["options_dict"]
        content = q["content"]
        if content == f"{num}.":
            content = f"{num}. Vyberte správne tvrdenia / vzorce ({category_name}):"
    else:
        opt_dict = {}
        content = f"{num}. Otázka č. {num} ({category_name} – chemické vzorce / štruktúry):"

    options_list = []
    for letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
        text = opt_dict.get(letter, "").strip()
        if not text:
            text = f"Možnosť {letter.upper()} (pozri vzorec v testovnici)"
        options_list.append({
            "id": letter,
            "text": text
        })

    final_items.append({
        "subject": "Chémia",
        "category": category_name,
        "content": content,
        "options": options_list,
        "correct_answers": correct,
        "explanation": explanation
    })

with open("chemia_otazky_641_1500.json", "w", encoding="utf-8") as f:
    json.dump(final_items, f, ensure_ascii=False, indent=2)
print("Saved chemia_otazky_641_1500.json successfully!")
