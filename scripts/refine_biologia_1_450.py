import json
import re
import fitz
import numpy as np
from PIL import Image
import io
from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()

def extract_100pct_bio_answers(pdf_path):
    doc = fitz.open(pdf_path)
    all_answers = {}

    # Pages 311 to 314 (0-based 310 to 313)
    for p_idx in range(310, 314):
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

            # Check if combined "70. a,b,c"
            m_comb = re.match(r'^(\d+)\.?\s*([a-hA-H][a-hA-H,\.\s;]*)$', txt)
            if m_comb:
                q_val = int(m_comb.group(1))
                letters = [c for c in m_comb.group(2).lower() if c in 'abcdefgh']
                if 1 <= q_val <= 450 and letters:
                    all_answers[q_val] = letters
                continue

            m = re.match(r'^([0-9oOlI]{1,3})\.?$', txt)
            if m:
                s_num = m.group(1).replace('o', '0').replace('O', '0').replace('l', '1').replace('I', '1')
                if s_num.isdigit():
                    q_val = int(s_num)
                    if 1 <= q_val <= 550 and not (q_val in [311, 312, 313, 314] and cy > 2150):
                        q_blocks.append((q_val, cx, cy))
            else:
                clean = txt.replace(' ', '').replace(';', ',').replace('.', ',')
                letters = [c for c in clean.lower() if c in 'abcdefgh']
                if letters and len(clean) <= 20:
                    ans_blocks.append((letters, cx, cy))

        # Fit linear model cy = a * q_num + b within each column!
        # On page 311: Col1=1..44, Col2=45..89, Col3=90..134 (approx 44-45 per col)
        # Cluster q_blocks by column based on cx: Col0 (<550), Col1 (550..1050), Col2 (>1050)
        cols = {0: [], 1: [], 2: []}
        ans_cols = {0: [], 1: [], 2: []}
        for q_val, cx, cy in q_blocks:
            c = 0 if cx < 550 else (1 if cx < 1050 else 2)
            cols[c].append((q_val, cx, cy))
        for letters, cx, cy in ans_blocks:
            c = 0 if cx < 550 else (1 if cx < 1050 else 2)
            ans_cols[c].append((letters, cx, cy))

        for c in [0, 1, 2]:
            pts = cols[c]
            apts = ans_cols[c]
            if len(pts) >= 5:
                # Filter outliers in q_val using median
                med_q = np.median([p[0] for p in pts])
                clean_pts = [p for p in pts if abs(p[0] - med_q) < 30]
                if len(clean_pts) >= 4:
                    qs = np.array([p[0] for p in clean_pts], dtype=float)
                    ys = np.array([p[2] for p in clean_pts], dtype=float)
                    slope, intercept = np.polyfit(qs, ys, 1)
                    # Now for every answer block in this column, find its exact question number!
                    for letters, ax, ay in apts:
                        # Expected q_num from ay (accounting for slight ~2px offset)
                        est_q = int(round((ay - intercept) / slope))
                        if 1 <= est_q <= 450:
                            pred_y = slope * est_q + intercept
                            if abs(ay - pred_y) < abs(slope) * 0.65:
                                all_answers[est_q] = letters

            # Also direct match for any detected q_block
            for q_val, qx, qy in pts:
                if 1 <= q_val <= 450 and q_val not in all_answers:
                    cands = [(abs(ay - qy), letters) for letters, ax, ay in apts if abs(ay - qy) < 22]
                    if cands:
                        cands.sort(key=lambda x: x[0])
                        all_answers[q_val] = cands[0][1]

    return all_answers

if __name__ == "__main__":
    pdf_path = "Biológia 2026.pdf"
    answers = extract_100pct_bio_answers(pdf_path)

    # Merge with existing data_bio_answers_1_450.json
    with open("data_bio_answers_1_450.json", "r", encoding="utf-8") as f:
        old_ans = json.load(f)
    for k, v in old_ans.items():
        if int(k) not in answers:
            answers[int(k)] = v

    missing = [n for n in range(1, 451) if n not in answers]
    print(f"Refined Bio answers 1..450: {len(answers)}/450, missing: {len(missing)} -> {missing}")

    with open("data_bio_answers_1_450.json", "w", encoding="utf-8") as f:
        json.dump({str(k): v for k, v in sorted(answers.items()) if 1 <= k <= 450}, f, ensure_ascii=False, indent=2)

    # Also check Q416-418 in temp_bio_ocr_7_98.json
    with open("temp_bio_ocr_7_98.json", "r", encoding="utf-8") as f:
        pages = json.load(f)
    for p in ["90", "91", "92"]:
        for l in pages.get(p, []):
            if any(x in l for x in ["416", "417", "418"]):
                print(f"Page {p}: {l}")

    # Update biologia_otazky_1_450.json with the refined answers
    with open("biologia_otazky_1_450.json", "r", encoding="utf-8") as f:
        bio_qs = json.load(f)

    for q in bio_qs:
        q_num = int(q["content"].split(".")[0])
        if q_num in answers:
            corr = answers[q_num]
            q["correct_answers"] = corr
            q["explanation"] = f"Správne odpovede podľa oficiálneho kľúča testovnice UPJŠ LF sú: {', '.join(a.upper() for a in corr)}."

    with open("biologia_otazky_1_450.json", "w", encoding="utf-8") as f:
        json.dump(bio_qs, f, ensure_ascii=False, indent=2)
    print("Updated biologia_otazky_1_450.json with refined answer keys!")

