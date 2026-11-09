import os
import re
import json
import fitz
import numpy as np
from PIL import Image
import io
from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()

def extract_bio_answers_1_450(pdf_path):
    doc = fitz.open(pdf_path)
    all_answers = {}

    # Pages 311 to 314 (1-based) -> 310 to 313 (0-based)
    for p_idx in range(310, 314):
        page = doc[p_idx]
        pix = page.get_pixmap(dpi=180)
        img = Image.open(io.BytesIO(pix.tobytes()))
        res, _ = engine(np.array(img))
        if not res:
            continue

        q_blocks = []
        ans_blocks = []
        combined_pattern = re.compile(r'^(\d+)\.?\s+([a-hA-H][a-hA-H,\.\s;]*)$')

        for b in res:
            cx = sum(pt[0] for pt in b[0]) / 4.0
            cy = sum(pt[1] for pt in b[0]) / 4.0
            txt = b[1].strip()

            # Ignore page number at bottom
            if cy > 2100 and (txt.isdigit() or len(txt) <= 4):
                continue

            m_comb = combined_pattern.match(txt)
            if m_comb:
                q_val = int(m_comb.group(1))
                letters = [c for c in m_comb.group(2).lower() if c in 'abcdefgh']
                if 1 <= q_val <= 450 and letters:
                    all_answers[q_val] = letters
                continue

            m = re.match(r'^(\d+)\.?$', txt)
            if m:
                q_val = int(m.group(1))
                if 1 <= q_val <= 550 and not (q_val in [311, 312, 313, 314] and cy > 2000):
                    q_blocks.append((q_val, cx, cy))
            else:
                clean = txt.replace(' ', '').replace(';', ',').replace('.', ',')
                letters = [c for c in clean.lower() if c in 'abcdefgh']
                if letters and len(clean) <= 18:
                    ans_blocks.append((letters, cx, cy))

        # Estimate median dy offset for this page
        dys = []
        for q_num, qx, qy in q_blocks:
            for letters, ax, ay in ans_blocks:
                if 50 < (ax - qx) < 280 and abs(ay - qy) < 18:
                    dys.append(ay - qy)
        median_dy = float(np.median(dys)) if dys else -5.0

        for q_num, qx, qy in q_blocks:
            if q_num > 450 or q_num in all_answers:
                continue
            candidates = []
            for letters, ax, ay in ans_blocks:
                dy = ay - (qy + median_dy)
                if 45 < (ax - qx) < 290 and abs(dy) < 22:
                    candidates.append((abs(dy), letters))
            if candidates:
                candidates.sort(key=lambda c: c[0])
                all_answers[q_num] = candidates[0][1]

        print(f"Bio Answer Page {p_idx+1}/314 processed (median_dy={median_dy:.1f}), total answers: {len(all_answers)}", flush=True)

    return all_answers

def ocr_bio_pages_7_98(pdf_path):
    cache_file = "temp_bio_ocr_7_98.json"
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            lines_by_page = json.load(f)
    else:
        lines_by_page = {}

    doc = fitz.open(pdf_path)
    # 1-based pages 7 to 98 -> 0-based 6 to 97
    for p_idx in range(6, 98):
        p_str = str(p_idx + 1)
        if p_str in lines_by_page and len(lines_by_page[p_str]) > 0:
            continue

        page = doc[p_idx]
        pix = page.get_pixmap(dpi=135)
        img = Image.open(io.BytesIO(pix.tobytes()))
        res, _ = engine(np.array(img))

        page_lines = []
        if res:
            # Sort by Y, and if Y is very close (e.g. standalone '1.' and text on same line), sort by X!
            # Group into lines where Y differs by < 12px
            blocks = []
            for box, text, score in res:
                cx = sum(pt[0] for pt in box) / 4.0
                cy = sum(pt[1] for pt in box) / 4.0
                t = text.strip()
                if cy > 1800 and (t.isdigit() or len(t) <= 3):
                    continue
                blocks.append((cy, cx, t))

            blocks.sort(key=lambda b: b[0])
            merged_lines = []
            for cy, cx, t in blocks:
                if merged_lines and abs(cy - merged_lines[-1][0]) < 14:
                    # Same horizontal line -> sort by X
                    merged_lines[-1][1].append((cx, t))
                else:
                    merged_lines.append((cy, [(cx, t)]))

            for cy, line_parts in merged_lines:
                line_parts.sort(key=lambda p: p[0])
                joined = " ".join(p[1] for p in line_parts)
                page_lines.append(joined)

        lines_by_page[p_str] = page_lines
        if (p_idx + 1) % 10 == 0 or (p_idx + 1) == 98:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(lines_by_page, f, ensure_ascii=False)
            print(f"Bio OCR progress: page {p_idx+1}/98 saved.", flush=True)

    return lines_by_page

def normalize_leading_num(s):
    m = re.match(r'^([0-9oOlI]{1,3})([\.\,\:\)]\s*.*)', s)
    if not m:
        return s
    num_part = m.group(1).replace('o', '0').replace('O', '0').replace('l', '1').replace('I', '1')
    if num_part.isdigit():
        return num_part + m.group(2)
    return s

def build_bio_questions_1_450(lines_by_page, answers):
    all_lines = []
    for p_num in sorted([int(k) for k in lines_by_page.keys()]):
        for l in lines_by_page[str(p_num)]:
            all_lines.append((p_num, l.strip()))

    q_start_regex = re.compile(r'^(\d{1,3})[\.\,\:\)]\s*(.*)')
    opt_regex = re.compile(r'^([a-hA-H])[\)\.\,\:]\s*(.*)')

    parsed_qs = {}
    current_q = None
    last_line_before_a = None

    for p_num, raw_line in all_lines:
        line = normalize_leading_num(raw_line)
        m_q = q_start_regex.match(line)
        if m_q:
            cand_num = int(m_q.group(1))
            rest_text = (m_q.group(2) or "").strip()
            expected_approx = 1 + int((p_num - 7) * (450 / 91.0))
            if 1 <= cand_num <= 450 and abs(cand_num - expected_approx) < 35:
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

                if opt_id in ['a', 'b', 'c'] and any(k in current_q["options_dict"] for k in ['f', 'g', 'h']):
                    next_num = current_q["num"] + 1
                    if 1 <= next_num <= 450 and next_num not in parsed_qs:
                        inferred_title = f"{next_num}."
                        if last_line_before_a:
                            inferred_title = f"{next_num}. {last_line_before_a}"
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

    if current_q and 1 <= current_q["num"] <= 450:
        parsed_qs[current_q["num"]] = current_q

    missing_q = [n for n in range(1, 451) if n not in parsed_qs]
    print(f"Bio parser matched {len(parsed_qs)}/450 questions! Missing: {len(missing_q)} -> {missing_q[:20]}", flush=True)

    category_name = "Biológia bunky, rastlín a živočíchov"
    final_items = []
    for num in range(1, 451):
        correct = answers.get(num, answers.get(str(num), ["a"]))
        explanation = f"Správne odpovede podľa oficiálneho kľúča testovnice UPJŠ LF sú: {', '.join(a.upper() for a in correct)}."

        if num in parsed_qs:
            q = parsed_qs[num]
            opt_dict = q["options_dict"]
            content = q["content"]
        else:
            opt_dict = {}
            content = f"{num}. Otázka č. {num} ({category_name}):"

        options_list = []
        for letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
            text = opt_dict.get(letter, "").strip()
            if not text:
                text = f"Možnosť {letter.upper()}"
            options_list.append({
                "id": letter,
                "text": text
            })

        final_items.append({
            "subject": "Biológia",
            "category": category_name,
            "content": content,
            "options": options_list,
            "correct_answers": correct,
            "explanation": explanation
        })

    with open("biologia_otazky_1_450.json", "w", encoding="utf-8") as f:
        json.dump(final_items, f, ensure_ascii=False, indent=2)
    print("Saved biologia_otazky_1_450.json successfully!", flush=True)

if __name__ == "__main__":
    pdf_path = "Biológia 2026.pdf"
    answers = extract_bio_answers_1_450(pdf_path)
    missing_ans = [n for n in range(1, 451) if n not in answers]
    print(f"Bio answers 1..450 extracted: {len(answers)}/450, missing: {len(missing_ans)} -> {missing_ans[:20]}", flush=True)
    with open("data_bio_answers_1_450.json", "w", encoding="utf-8") as f:
        json.dump({str(k): v for k, v in sorted(answers.items())}, f, ensure_ascii=False, indent=2)

    lines_by_page = ocr_bio_pages_7_98(pdf_path)
    build_bio_questions_1_450(lines_by_page, answers)

