import os
import glob
import re
import json
import fitz
from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()

def build_complete_300():
    pdf_files = glob.glob("*.pdf")
    pdf_path = pdf_files[0]
    doc = fitz.open(pdf_path)
    
    with open("data_answers_1_300.json", "r", encoding="utf-8") as f:
        answers_map = json.load(f)
        
    with open("temp_pages/ocr_lines_6_76.json", "r", encoding="utf-8") as f:
        lines = json.load(f)
        
    # Načítame existujúce vygenerované otázky
    with open("chemia_otazky_1_300.json", "r", encoding="utf-8") as f:
        existing_qs = json.load(f)
        
    by_num = {}
    for q in existing_qs:
        num = int(q["content"].split(".")[0])
        by_num[num] = q
        
    print(f"Already have: {len(by_num)} questions.")
    
    # Prejdeme všetky strany a nájdeme kde chýbajú otázky
    # 20 chýbajúcich: [17, 36, 40, 78, 80, 85, 86, 104, 105, 106, 158, 160, 181, 195, 211, 228, 234, 267, 277, 282]
    # Otázka 40 bola napísaná ako '4o.'
    # Otázka 78: '78. Vyberte zluceniny, ktorych nazov aj vzorec predstavuje zmiesanu sol:'
    
    # Doplníme otázku 40:
    if 40 not in by_num:
        by_num[40] = {
            "subject": "Chémia",
            "category": "Všeobecná a anorganická chémia",
            "content": "40. Ak n je latkove mnozstvo, m je hmotnost, M je molekulova hmotnost danej zluceniny a V je celkovy objem roztoku, potom vyberte spravny vztah pre vypocet latkovej koncentracie a jej moznu jednotku:",
            "options": [
                {"id": "a", "text": "c = n/V, mol.l-1"},
                {"id": "b", "text": "c = m/M.V, mol.cm-3"},
                {"id": "c", "text": "c = m.M/V, kg"},
                {"id": "d", "text": "c = n.V, mol.dm-3"},
                {"id": "e", "text": "c = m.M.V, mol.l"},
                {"id": "f", "text": "c = n/V, mmol/l"},
                {"id": "g", "text": "c = m.V, g/l"},
                {"id": "h", "text": "c = m/M.V, mol/dm3"}
            ],
            "correct_answers": answers_map.get("40", ["a", "f", "h"]),
            "explanation": f"Správne odpovede podľa oficiálneho kľúča testovnice UPJŠ LF sú: {', '.join(sorted(answers_map.get('40', []))).upper()}."
        }
        
    # Doplníme otázku 78:
    if 78 not in by_num:
        by_num[78] = {
            "subject": "Chémia",
            "category": "Všeobecná a anorganická chémia",
            "content": "78. Vyberte zluceniny, ktorych nazov aj vzorec predstavuje zmiesanu sol:",
            "options": [
                {"id": "a", "text": "(NH4)2Pb(SO4)2 siran amonno-olovnaty"},
                {"id": "b", "text": "FeCl(OH)2 hydroxid-chlorid zelezity"},
                {"id": "c", "text": "[Cu(NH3)4]SO4 . H2O monohydrat siranu tetraammin med'neho"},
                {"id": "d", "text": "KHS hydrid sulfid draselny"},
                {"id": "e", "text": "NaTl(NO3)2 dusicnan sodno-talny"},
                {"id": "f", "text": "KCr(SO4)2 siran draselno-chromity"},
                {"id": "g", "text": "K[Au(OH)4] hydroxid draselno-zlatity"},
                {"id": "h", "text": "BiCl(O) oxid chlorid bizmutity"}
            ],
            "correct_answers": answers_map.get("78", ["a", "e", "f"]),
            "explanation": f"Správne odpovede podľa oficiálneho kľúča testovnice UPJŠ LF sú: {', '.join(sorted(answers_map.get('78', []))).upper()}."
        }

    # Vygenerujeme zoznam chýbajúcich
    missing = [i for i in range(1, 301) if i not in by_num]
    print(f"Remaining missing: {len(missing)} -> {missing}")
    
    # Pre zvyšné čísla nájdeme zodpovedajúce strany a text priamo z PDF
    # Uložíme zatiaľ aktualizovaný stav
    ordered = [by_num[i] for i in sorted(by_num.keys()) if i <= 300]
    with open("chemia_otazky_1_300.json", "w", encoding="utf-8") as f:
        json.dump(ordered, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    build_complete_300()

