import os
import glob
import re
import json
import fitz
from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()

def extract_answers_from_pages(pdf_path, start_page_1based, end_page_1based):
    doc = fitz.open(pdf_path)
    all_answers = {}
    
    # Kľúč odpovedí je na stranách rozdelený do stĺpcov
    # Na strane je typicky 3 alebo 4 stĺpce (číslo otázky a vedľa odpoveď)
    for p_num in range(start_page_1based - 1, end_page_1based):
        page = doc[p_num]
        pix = page.get_pixmap(dpi=200)
        temp_img = f"temp_pages/ans_p_{p_num+1}.png"
        pix.save(temp_img)
        
        res, _ = engine(temp_img)
        if not res:
            continue
            
        # Získame všetky detegované bloky so stredovými súradnicami
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
            
        # Hľadáme čísla otázok: '1.', '2.', ... '1500.'
        num_pattern = re.compile(r'^(\d+)\.?$')
        
        q_blocks = []
        ans_blocks = []
        for b in blocks:
            m = num_pattern.match(b["text"])
            if m:
                q_num = int(m.group(1))
                # Odfiltrujeme číslo strany (napr. 321, 322)
                if q_num > 1600 or (q_num in [321, 322, 323, 324, 325, 326, 327, 328, 329, 330] and b["cy"] > 2300):
                    continue
                q_blocks.append((q_num, b))
            else:
                # Blok odpovede: obsahuje písmená a čiarky, napr. 'a,b,c', 'e,f,g,h', 'c,d'
                clean_ans = b["text"].replace(' ', '').replace(';', ',').replace('.', ',')
                # Overíme či obsahuje písmená a až h
                letters = [c for c in clean_ans.lower() if c in 'abcdefgh']
                if len(letters) >= 1 and len(clean_ans) <= 18:
                    ans_blocks.append((letters, b))
                    
        # Pre každé číslo otázky hľadáme najbližší blok odpovede napravo (cx_ans > cx_q) a s podobným Y
        for q_num, qb in q_blocks:
            qx = qb["cx"]
            qy = qb["cy"]
            
            candidates = []
            for letters, ab in ans_blocks:
                ax = ab["cx"]
                ay = ab["cy"]
                # Odpoveď je napravo vo vzdialenosti 50 až 300 px a výškovo v tolerancii +-35 px
                if 40 < (ax - qx) < 320 and abs(ay - qy) < 35:
                    candidates.append((ax - qx, letters))
                    
            if candidates:
                # Vyberieme ten najbližší napravo
                candidates.sort(key=lambda c: c[0])
                all_answers[q_num] = candidates[0][1]
                
    return all_answers

if __name__ == "__main__":
    os.makedirs("temp_pages", exist_ok=True)
    pdf_files = glob.glob("*.pdf")
    if not pdf_files:
        print("PDF not found!")
        exit(1)
        
    pdf_path = pdf_files[0]
    print(f"Extracting answer keys for questions 1-350 from {pdf_path}...")
    # Strany 321, 322, 323 pokrývajú otázky 1 až cca 410
    answers = extract_answers_from_pages(pdf_path, 321, 323)
    
    print(f"Total answers extracted: {len(answers)}")
    missing = [i for i in range(1, 301) if i not in answers]
    print(f"Missing answers between 1 and 300: {len(missing)} -> {missing[:15]}")
    
    with open("data_answers_1_300.json", "w", encoding="utf-8") as f:
        json.dump({str(k): v for k, v in sorted(answers.items())}, f, ensure_ascii=False, indent=2)
    print("Saved to data_answers_1_300.json")

