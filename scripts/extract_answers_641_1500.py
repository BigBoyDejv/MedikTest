import os
import re
import json
import fitz
from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()

def extract_answers_641_1500(pdf_path):
    doc = fitz.open(pdf_path)
    all_answers = {}
    os.makedirs("temp_pages", exist_ok=True)
    
    # Pages 323 to 330 (1-based) cover questions 641 to 1500
    for p_num in range(322, 330):
        page = doc[p_num]
        pix = page.get_pixmap(dpi=200)
        temp_img = f"temp_pages/ans_p_{p_num+1}.png"
        if not os.path.exists(temp_img):
            pix.save(temp_img)
            
        res, _ = engine(temp_img)
        if not res:
            continue
            
        blocks = []
        for box, text, score in res:
            clean_text = text.strip()
            cx = sum(pt[0] for pt in box) / 4.0
            cy = sum(pt[1] for pt in box) / 4.0
            blocks.append({
                "cx": cx,
                "cy": cy,
                "text": clean_text,
                "box": box
            })
            
        num_pattern = re.compile(r'^(\d+)\.?$')
        # Niekedy je cislo a odpoved spojene v jednom bloku napr. "645. a,b,c"
        combined_pattern = re.compile(r'^(\d+)\.?\s+([a-hA-H][a-hA-H,\.\s;]*)$')
        
        q_blocks = []
        ans_blocks = []
        for b in blocks:
            m_comb = combined_pattern.match(b["text"])
            if m_comb:
                q_num = int(m_comb.group(1))
                raw_ans = m_comb.group(2)
                letters = [c for c in raw_ans.lower() if c in 'abcdefgh']
                if 641 <= q_num <= 1500 and letters:
                    all_answers[q_num] = letters
                continue
                
            m = num_pattern.match(b["text"])
            if m:
                q_num = int(m.group(1))
                if q_num > 1500 or (q_num in range(320, 335) and b["cy"] > 2300):
                    continue
                q_blocks.append((q_num, b))
            else:
                clean_ans = b["text"].replace(' ', '').replace(';', ',').replace('.', ',')
                letters = [c for c in clean_ans.lower() if c in 'abcdefgh']
                if len(letters) >= 1 and len(clean_ans) <= 18:
                    ans_blocks.append((letters, b))
                    
        for q_num, qb in q_blocks:
            if q_num in all_answers:
                continue
            qx = qb["cx"]
            qy = qb["cy"]
            candidates = []
            for letters, ab in ans_blocks:
                ax = ab["cx"]
                ay = ab["cy"]
                if 35 < (ax - qx) < 340 and abs(ay - qy) < 38:
                    candidates.append((ax - qx, letters))
            if candidates:
                candidates.sort(key=lambda c: c[0])
                all_answers[q_num] = candidates[0][1]
        print(f"Processed answer key page {p_num+1}/330, total answers so far: {len(all_answers)}")
        
    return all_answers

if __name__ == "__main__":
    pdf_path = "Chémia 2026.pdf"
    answers = extract_answers_641_1500(pdf_path)
    filtered = {str(k): v for k, v in sorted(answers.items()) if 641 <= k <= 1500}
    
    missing = [i for i in range(641, 1501) if str(i) not in filtered]
    print(f"Extracted {len(filtered)}/860 answers for 641..1500.")
    print(f"Missing count: {len(missing)} -> {missing[:30]}")
    
    with open("data_answers_641_1500.json", "w", encoding="utf-8") as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)
    print("Saved data_answers_641_1500.json")

