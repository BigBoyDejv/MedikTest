import os
import re
import json
import fitz
import numpy as np
from PIL import Image
import io
from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()

def extract_all_bio_answers(pdf_path="Biológia 2026.pdf"):
    doc = fitz.open(pdf_path)
    all_answers = {}

    # Pages 314 to 322 (1-based) -> 0-based 313 to 321
    # Page 314 (313): 400..534
    # Page 315 (314): 535..669
    # Page 316 (315): 670..804
    # Page 317 (316): 805..939
    # Page 318 (317): 940..1074
    # Page 319 (318): 1075..1209
    # Page 320 (319): 1210..1344
    # Page 321 (320): 1345..1479
    # Page 322 (321): 1480..1500
    page_specs = [
        (313, [(400, 444), (445, 489), (490, 534)]),
        (314, [(535, 579), (580, 624), (625, 669)]),
        (315, [(670, 714), (715, 759), (760, 804)]),
        (316, [(805, 849), (850, 894), (895, 939)]),
        (317, [(940, 984), (985, 1029), (1030, 1074)]),
        (318, [(1075, 1119), (1120, 1164), (1165, 1209)]),
        (319, [(1210, 1254), (1255, 1299), (1300, 1344)]),
        (320, [(1345, 1389), (1390, 1434), (1435, 1479)]),
        (321, [(1480, 1500), (1501, 1520), (1521, 1540)]),
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
                if 451 <= q_val <= 1500 and letters:
                    all_answers[q_val] = sorted(list(set(letters)))
                continue

            m = re.match(r'^([0-9oOlI]{3,4})\.?$', txt)
            if m:
                s_num = m.group(1).replace('o', '0').replace('O', '0').replace('l', '1').replace('I', '1')
                if s_num.isdigit():
                    q_val = int(s_num)
                    if 400 <= q_val <= 1520 and not (q_val in [314, 315, 316, 317, 318, 319, 320, 321, 322] and cy > 2150):
                        q_blocks.append((q_val, cx, cy))
            else:
                clean = txt.replace(' ', '').replace(';', ',').replace('.', ',')
                letters = [c for c in clean.lower() if c in 'abcdefgh']
                if letters and len(clean) <= 20:
                    ans_blocks.append((letters, cx, cy))

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
            if len(pts) < 3:
                continue
            qs = np.array([p[0] for p in pts], dtype=float)
            xs = np.array([p[1] for p in pts], dtype=float)
            ys = np.array([p[2] for p in pts], dtype=float)
            slope_y, inter_y = np.polyfit(qs, ys, 1)
            med_qx = float(np.median(xs))

            for letters, ax, ay in apts:
                est_q = int(round((ay - inter_y) / slope_y))
                if max(451, q_min) <= est_q <= min(1500, q_max):
                    pred_y = slope_y * est_q + inter_y
                    if abs(ay - pred_y) < abs(slope_y) * 0.65:
                        all_answers[est_q] = sorted(list(set(letters)))

            for q_num in range(max(451, q_min), min(1500, q_max) + 1):
                if q_num in all_answers:
                    continue
                pred_y = slope_y * q_num + inter_y
                x1 = max(0, int(med_qx - 45))
                x2 = min(img.width, int(med_qx + 350))
                y1 = max(0, int(pred_y - 24))
                y2 = min(img.height, int(pred_y + 24))
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
                    ans_crop = img.crop((int(med_qx + 50), y1, x2, y2))
                    rec_res, _ = engine.text_recognizer([np.array(ans_crop)])
                    if rec_res:
                        for txt_r, _ in rec_res:
                            for ch in txt_r.lower():
                                if ch in 'abcdefgh' and ch not in letters:
                                    letters.append(ch)
                if letters:
                    all_answers[q_num] = sorted(list(set(letters)))

        print(f"Bio Answer Page {p_idx+1}/322 processed. Total answers in DB so far: {len(all_answers)}", flush=True)

    # Known manual verifications from book scan:
    known_manual = {
        486: ['a', 'c', 'd'],
        489: ['a', 'c', 'e', 'h'],
        547: [], # Official book key has blank
        614: ['e'],
        780: [], # Official book key has blank
        807: ['b']
    }
    for q, ans in known_manual.items():
        all_answers[q] = ans

    with open("data_bio_answers_451_1500.json", "w", encoding="utf-8") as f:
        json.dump({str(k): v for k, v in sorted(all_answers.items())}, f, ensure_ascii=False, indent=2)

    missing = [n for n in range(451, 1501) if n not in all_answers]
    print(f"\nFinal extracted answers 451..1500: {len(all_answers)}/1050! Missing: {len(missing)} -> {missing[:30]}", flush=True)
    return all_answers

if __name__ == "__main__":
    extract_all_bio_answers()

