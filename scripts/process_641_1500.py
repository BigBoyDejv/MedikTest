import os
import re
import json
import fitz
import numpy as np
from PIL import Image
import io
from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()

def ocr_pages_112_320(pdf_path):
    cache_file = "temp_ocr_lines_112_320.json"
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            lines_by_page = json.load(f)
    else:
        lines_by_page = {}

    doc = fitz.open(pdf_path)
    # 1-based pages 112 to 320 -> 0-based 111 to 319
    for p_idx in range(111, 320):
        p_str = str(p_idx + 1)
        if p_str in lines_by_page and len(lines_by_page[p_str]) > 0:
            continue

        page = doc[p_idx]
        pix = page.get_pixmap(dpi=130)
        img = Image.open(io.BytesIO(pix.tobytes()))
        res, _ = engine(np.array(img))
        
        page_lines = []
        if res:
            # Sort top-to-bottom
            sorted_blocks = sorted(res, key=lambda b: sum(pt[1] for pt in b[0]) / 4.0)
            for box, text, score in sorted_blocks:
                cy = sum(pt[1] for pt in box) / 4.0
                t = text.strip()
                # Skip footer page number
                if cy > 1750 and (t.isdigit() or len(t) <= 3):
                    continue
                page_lines.append(t)

        lines_by_page[p_str] = page_lines
        if (p_idx + 1) % 10 == 0 or (p_idx + 1) == 320:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(lines_by_page, f, ensure_ascii=False)
            print(f"OCR progress: page {p_idx + 1}/320 saved.", flush=True)

    return lines_by_page

def build_questions_641_1500(lines_by_page, answers):
    all_lines = []
    for p_num in sorted([int(k) for k in lines_by_page.keys()]):
        for l in lines_by_page[str(p_num)]:
            all_lines.append((p_num, l.strip()))

    # Regex na zaciatok otazky (aj ked OCR precita napr. 64l. alebo 800 bez bodky)
    q_start_regex = re.compile(r'^(\d{3,4})[\.\,\:\)]?\s+(.*)')
    opt_regex = re.compile(r'^([a-hA-H])[\.\,\)\:]\s*(.*)')

    parsed_qs = {}
    current_q = None
    expected_next = 641

    for p_num, line in all_lines:
        m_q = q_start_regex.match(line)
        if m_q:
            cand_num = int(m_q.group(1))
            if 641 <= cand_num <= 1500:
                if current_q:
                    parsed_qs[current_q["num"]] = current_q
                current_q = {
                    "num": cand_num,
                    "page": p_num,
                    "content": f"{cand_num}. {m_q.group(2).strip()}",
                    "options_dict": {},
                    "current_opt": None
                }
                expected_next = cand_num + 1
                continue

        if current_q:
            m_opt = opt_regex.match(line)
            if m_opt:
                opt_id = m_opt.group(1).lower()
                current_q["options_dict"][opt_id] = m_opt.group(2).strip()
                current_q["current_opt"] = opt_id
            else:
                if current_q["current_opt"]:
                    current_q["options_dict"][current_q["current_opt"]] += " " + line
                else:
                    current_q["content"] += " " + line

    if current_q and 641 <= current_q["num"] <= 1500:
        parsed_qs[current_q["num"]] = current_q

    # Build final list for all 641..1500
    final_items = []
    missing_nums = []
    for num in range(641, 1501):
        # Rozdelenie kategorii: 641-1150 Organicka chemia, 1151-1500 Biochemia
        category_name = "Organická chémia" if num <= 1150 else "Biochémia"
        correct = answers.get(str(num), [])
        explanation = f"Správne odpovede podľa oficiálneho kľúča testovnice UPJŠ LF sú: {', '.join(a.upper() for a in correct)}."

        if num in parsed_qs:
            q = parsed_qs[num]
            opt_dict = q["options_dict"]
            content = q["content"]
        else:
            missing_nums.append(num)
            opt_dict = {}
            content = f"{num}. Otázka č. {num} z testovnice UPJŠ LF ({category_name}):"

        options_list = []
        for letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
            text = opt_dict.get(letter, f"Možnosť {letter.upper()}").strip()
            if not text:
                text = f"Možnosť {letter.upper()}"
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

    print(f"Compiled {len(final_items)} questions (641..1500).")
    print(f"Directly parsed from OCR: {len(parsed_qs)}/860 (missing headers: {len(missing_nums)})")
    with open("chemia_otazky_641_1500.json", "w", encoding="utf-8") as f:
        json.dump(final_items, f, ensure_ascii=False, indent=2)
    print("Saved chemia_otazky_641_1500.json")

if __name__ == "__main__":
    pdf_path = "Chémia 2026.pdf"
    with open("data_answers_641_1500.json", "r", encoding="utf-8") as f:
        answers = json.load(f)
    lines_by_page = ocr_pages_112_320(pdf_path)
    build_questions_641_1500(lines_by_page, answers)

