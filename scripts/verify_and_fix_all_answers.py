import fitz
import numpy as np
from rapidocr_onnxruntime import RapidOCR
from PIL import Image
import io
import re
import json

engine = RapidOCR()

def extract_all_verified_answers(pdf_path):
    doc = fitz.open(pdf_path)
    all_answers = {}

    # Pages 321 to 330 in book -> 0-based 320 to 329
    for p_num in range(320, 330):
        page = doc[p_num]
        pix = page.get_pixmap(dpi=150)
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

            # Skip footer page number
            if cy > 1800 and (txt.isdigit() or len(txt) <= 3):
                continue

            m = re.match(r'^(\d+)\.?$', txt)
            if m:
                q_val = int(m.group(1))
                if 1 <= q_val <= 1500:
                    q_blocks.append((q_val, cx, cy))
            else:
                clean = txt.replace(' ', '').replace(';', ',').replace('.', ',')
                letters = [c for c in clean.lower() if c in 'abcdefgh']
                if letters and len(clean) <= 18:
                    ans_blocks.append((letters, cx, cy))

        # Pairing
        for q_num, qx, qy in q_blocks:
            candidates = []
            for letters, ax, ay in ans_blocks:
                # Same column: ax is right of qx by 60 to 240px
                # Vertical offset ay is close to qy - 10px (tolerance < 22px)
                dy = ay - (qy - 10)
                if 60 < (ax - qx) < 240 and abs(dy) < 22:
                    candidates.append((abs(dy), letters))

            if candidates:
                candidates.sort(key=lambda c: c[0])
                all_answers[q_num] = candidates[0][1]

        print(f"Extracted verified page {p_num+1}/330 -> total so far: {len(all_answers)}")

    return all_answers

if __name__ == "__main__":
    pdf_path = "Chémia 2026.pdf"
    answers = extract_all_verified_answers(pdf_path)

    # Sort and filter
    sorted_dict = {str(k): v for k, v in sorted(answers.items())}

    with open("data_answers_verified_1_1500.json", "w", encoding="utf-8") as f:
        json.dump(sorted_dict, f, ensure_ascii=False, indent=2)

    print(f"Extraction complete! Total verified answers: {len(sorted_dict)}")

    # Check coverage in our multiple-choice question ranges:
    # 1..340, 391..450, 641..1500 (total = 340 + 60 + 860 = 1260 questions)
    expected = list(range(1, 341)) + list(range(391, 451)) + list(range(641, 1501))
    missing = [q for q in expected if q not in answers]
    print(f"Missing in target 1260 questions: {len(missing)} -> {missing[:30]}")

