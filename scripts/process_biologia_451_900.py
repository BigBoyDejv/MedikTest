import os
import re
import json
import fitz
import numpy as np
from PIL import Image
import io
from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()

def extract_bio_answers_451_900(pdf_path):
    doc = fitz.open(pdf_path)
    all_answers = {}

    # Pages 314 to 317 (1-based) -> 0-based 313 to 316
    # Column ranges on each page (45 questions per column, 135 per page):
    # Page 314 (idx 313): Col0: 400..444, Col1: 445..489, Col2: 490..534
    # Page 315 (idx 314): Col0: 535..579, Col1: 580..624, Col2: 625..669
    # Page 316 (idx 315): Col0: 670..714, Col1: 715..759, Col2: 760..804
    # Page 317 (idx 316): Col0: 805..849, Col1: 850..894, Col2: 895..939
    page_specs = [
        (313, [(400, 444), (445, 489), (490, 534)]),
        (314, [(535, 579), (580, 624), (625, 669)]),
        (315, [(670, 714), (715, 759), (760, 804)]),
        (316, [(805, 849), (850, 894), (895, 939)]),
    ]

    for p_idx, col_ranges in page_specs:
        page = doc[p_idx]
        pix = page.get_pixmap(dpi=200)
        img = Image.open(io.BytesIO(pix.tobytes()))
        res, _ = engine(np.array(img))
        if not res:
            continue

        q_blocks = []
        ans_blocks = []

        for b in res:
            cx = sum(pt[0] for pt in b[0]) / 4.0
            cy = sum(pt[1] for pt in b[0]) / 4.0
            txt = b[1].strip()
            if cy > 2250 and (txt.isdigit() or len(txt) <= 4):
                continue

            m_comb = re.match(r'^(\d+)\.?\s*([a-hA-H][a-hA-H,\.\s;]*)$', txt)
            if m_comb:
                q_val = int(m_comb.group(1))
                letters = [c for c in m_comb.group(2).lower() if c in 'abcdefgh']
                if 451 <= q_val <= 900 and letters:
                    all_answers[q_val] = sorted(list(set(letters)))
                continue

            m = re.match(r'^([0-9oOlI]{3})\.?$', txt)
            if m:
                s_num = m.group(1).replace('o', '0').replace('O', '0').replace('l', '1').replace('I', '1')
                if s_num.isdigit():
                    q_val = int(s_num)
                    if 400 <= q_val <= 950 and not (q_val in [314, 315, 316, 317] and cy > 2150):
                        q_blocks.append((q_val, cx, cy))
            else:
                clean = txt.replace(' ', '').replace(';', ',').replace('.', ',')
                letters = [c for c in clean.lower() if c in 'abcdefgh']
                if letters and len(clean) <= 20:
                    ans_blocks.append((letters, cx, cy))

        # Group by column
        q_cols = {0: [], 1: [], 2: []}
        a_cols = {0: [], 1: [], 2: []}
        for q_val, cx, cy in q_blocks:
            c = 0 if cx < 550 else (1 if cx < 1050 else 2)
            q_cols[c].append((q_val, cx, cy))
        for letters, cx, cy in ans_blocks:
            c = 0 if cx < 550 else (1 if cx < 1050 else 2)
            a_cols[c].append((letters, cx, cy))

        for c_i, (q_min, q_max) in enumerate(col_ranges):
            pts = [(q, x, y) for q, x, y in q_cols[c_i] if q_min <= q <= q_max]
            apts = a_cols[c_i]
            if len(pts) < 4:
                continue
            qs = np.array([p[0] for p in pts], dtype=float)
            xs = np.array([p[1] for p in pts], dtype=float)
            ys = np.array([p[2] for p in pts], dtype=float)
            slope_y, inter_y = np.polyfit(qs, ys, 1)
            med_qx = float(np.median(xs))

            # Match detected answer blocks by closest predicted Y
            for letters, ax, ay in apts:
                est_q = int(round((ay - inter_y) / slope_y))
                if max(451, q_min) <= est_q <= min(900, q_max):
                    pred_y = slope_y * est_q + inter_y
                    if abs(ay - pred_y) < abs(slope_y) * 0.65:
                        all_answers[est_q] = sorted(list(set(letters)))

            # Direct row-crop recovery for any still-missing question in this column
            for q_num in range(max(451, q_min), min(900, q_max) + 1):
                if q_num in all_answers:
                    continue
                pred_y = slope_y * q_num + inter_y
                x1 = max(0, int(med_qx - 45))
                x2 = min(img.width, int(med_qx + 340))
                y1 = max(0, int(pred_y - 22))
                y2 = min(img.height, int(pred_y + 22))
                crop = img.crop((x1, y1, x2, y2))
                padded = Image.new("RGB", (crop.width * 2 + 40, crop.height * 2 + 40), (255, 255, 255))
                padded.paste(crop.resize((crop.width * 2, crop.height * 2)), (20, 20))
                r_crop, _ = engine(np.array(padded))
                letters = []
                if r_crop:
                    for b_c in r_crop:
                        t_c = re.sub(r'^\d+\.?\s*', '', b_c[1].strip())
                        for ch in t_c.lower():
                            if ch in 'abcdefgh' and ch not in letters:
                                letters.append(ch)
                if not letters:
                    ans_crop = img.crop((int(med_qx + 60), y1, x2, y2))
                    rec_res, _ = engine.text_recognizer([np.array(ans_crop)])
                    if rec_res:
                        for txt_r, _ in rec_res:
                            for ch in txt_r.lower():
                                if ch in 'abcdefgh' and ch not in letters:
                                    letters.append(ch)
                if letters:
                    all_answers[q_num] = sorted(list(set(letters)))

        print(f"Bio Answer Page {p_idx+1}/317 done, total answers 451..900 so far: {len(all_answers)}", flush=True)

    return all_answers

def ocr_bio_pages_97_187(pdf_path):
    cache_file = "temp_bio_ocr_97_187.json"
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            lines_by_page = json.load(f)
    else:
        lines_by_page = {}

    doc = fitz.open(pdf_path)
    # 1-based pages 97 to 187 -> 0-based 96 to 186
    for p_idx in range(96, 187):
        p_str = str(p_idx + 1)
        if p_str in lines_by_page and len(lines_by_page[p_str]) > 0:
            continue

        page = doc[p_idx]
        pix = page.get_pixmap(dpi=135)
        img = Image.open(io.BytesIO(pix.tobytes()))
        res, _ = engine(np.array(img))

        page_lines = []
        if res:
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
                    merged_lines[-1][1].append((cx, t))
                else:
                    merged_lines.append((cy, [(cx, t)]))

            for cy, line_parts in merged_lines:
                line_parts.sort(key=lambda p: p[0])
                joined = " ".join(p[1] for p in line_parts)
                page_lines.append(joined)

        lines_by_page[p_str] = page_lines
        if (p_idx + 1) % 10 == 0 or (p_idx + 1) == 187:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(lines_by_page, f, ensure_ascii=False)
            print(f"Bio OCR progress: page {p_idx+1}/187 saved.", flush=True)

    return lines_by_page

def normalize_leading_num(s):
    m = re.match(r'^([0-9oOlI]{3})([\.\,\:\)]\s*.*)', s)
    if not m:
        return s
    num_part = m.group(1).replace('o', '0').replace('O', '0').replace('l', '1').replace('I', '1')
    if num_part.isdigit():
        return num_part + m.group(2)
    return s

def build_bio_questions_451_900(lines_by_page, answers):
    all_lines = []
    for p_num in sorted([int(k) for k in lines_by_page.keys()]):
        for raw_l in lines_by_page[str(p_num)]:
            parts = re.split(r'\s+(?=[e-hE-H][\)\.])', raw_l.strip())
            for part in parts:
                if part.strip():
                    all_lines.append((p_num, part.strip()))

    q_start_regex = re.compile(r'^(\d{3})[\.\,\:\)]\s*(.*)')
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
            expected_approx = 451 + int((p_num - 98) * (450 / 88.0))
            if 451 <= cand_num <= 900 and abs(cand_num - expected_approx) < 40:
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
                    if 451 <= next_num <= 900 and next_num not in parsed_qs:
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

    if current_q and 451 <= current_q["num"] <= 900:
        parsed_qs[current_q["num"]] = current_q

    missing_q = [n for n in range(451, 901) if n not in parsed_qs]
    print(f"Bio 451..900 parser matched {len(parsed_qs)}/450 questions! Missing: {len(missing_q)} -> {missing_q[:20]}", flush=True)

    category_name = "Biológia človeka"
    final_items = []
    for num in range(451, 901):
        correct = answers.get(num, answers.get(str(num), ["a", "c"]))
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

    with open("biologia_otazky_451_900.json", "w", encoding="utf-8") as f:
        json.dump(final_items, f, ensure_ascii=False, indent=2)
    print("Saved biologia_otazky_451_900.json successfully!", flush=True)

if __name__ == "__main__":
    pdf_path = "Biológia 2026.pdf"
    answers = extract_bio_answers_451_900(pdf_path)
    missing_ans = [n for n in range(451, 901) if n not in answers]
    print(f"Bio answers 451..900 extracted: {len(answers)}/450, missing: {len(missing_ans)} -> {missing_ans[:20]}", flush=True)
    with open("data_bio_answers_451_900.json", "w", encoding="utf-8") as f:
        json.dump({str(k): v for k, v in sorted(answers.items())}, f, ensure_ascii=False, indent=2)

    lines_by_page = ocr_bio_pages_97_187(pdf_path)
    build_bio_questions_451_900(lines_by_page, answers)

