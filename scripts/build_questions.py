import os
import glob
import re
import json
import fitz
from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()

def render_pages(pdf_path, start_page_1based, end_page_1based):
    doc = fitz.open(pdf_path)
    os.makedirs("temp_pages/q_pages", exist_ok=True)
    for p_num in range(start_page_1based - 1, end_page_1based):
        out_path = f"temp_pages/q_pages/p_{p_num+1}.png"
        if not os.path.exists(out_path):
            page = doc[p_num]
            pix = page.get_pixmap(dpi=140)
            pix.save(out_path)
    print("All pages rendered.")

def ocr_and_collect_lines(start_page, end_page):
    cache_file = "temp_pages/ocr_lines_6_76.json"
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)
            
    all_lines = []
    for p in range(start_page, end_page + 1):
        img_path = f"temp_pages/q_pages/p_{p}.png"
        if not os.path.exists(img_path):
            continue
        res, _ = engine(img_path)
        if not res:
            continue
        sorted_blocks = sorted(res, key=lambda b: sum(pt[1] for pt in b[0]) / 4.0)
        for box, text, _ in sorted_blocks:
            cy = sum(pt[1] for pt in box) / 4.0
            t = text.strip()
            if cy > 1900 and (t.isdigit() or len(t) < 4):
                continue
            all_lines.append(t)
        print(f"OCR finished page {p}/{end_page}")
        
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(all_lines, f, ensure_ascii=False)
    return all_lines

def build_questions_json(lines, answers_map):
    q_start_regex = re.compile(r'^(\d+)\.\s*(.*)')
    opt_regex = re.compile(r'^([a-hA-H])\.\s*(.*)')
    
    questions = []
    current_q = None
    
    for line in lines:
        m_q = q_start_regex.match(line)
        if m_q and int(m_q.group(1)) <= 310:
            q_num = int(m_q.group(1))
            if current_q:
                questions.append(current_q)
            current_q = {
                "num": q_num,
                "content": m_q.group(2).strip(),
                "options_dict": {},
                "current_opt_id": None
            }
            continue
            
        if current_q:
            m_opt = opt_regex.match(line)
            if m_opt:
                opt_id = m_opt.group(1).lower()
                opt_text = m_opt.group(2).strip()
                current_q["options_dict"][opt_id] = opt_text
                current_q["current_opt_id"] = opt_id
            else:
                if current_q["current_opt_id"]:
                    opt_id = current_q["current_opt_id"]
                    current_q["options_dict"][opt_id] += " " + line.strip()
                else:
                    current_q["content"] += " " + line.strip()
                    
    if current_q and current_q["num"] <= 310:
        questions.append(current_q)
        
    final_output = []
    for q in questions:
        q_num = q["num"]
        if q_num > 300:
            continue
        num_str = str(q_num)
        correct = answers_map.get(num_str, [])
        
        options_list = []
        for l in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
            if l in q["options_dict"]:
                options_list.append({
                    "id": l,
                    "text": q["options_dict"][l].strip()
                })
                
        correct_str = ", ".join(sorted(correct)).upper()
        explanation = f"Správne odpovede podľa oficiálneho kľúča testovnice UPJŠ LF sú: {correct_str}."
        
        final_output.append({
            "subject": "Chémia",
            "category": "Všeobecná a anorganická chémia",
            "content": f"{q_num}. {q['content']}",
            "options": options_list,
            "correct_answers": correct,
            "explanation": explanation
        })
        
    return final_output

if __name__ == "__main__":
    pdf_files = glob.glob("*.pdf")
    pdf_path = pdf_files[0]
    
    with open("data_answers_1_300.json", "r", encoding="utf-8") as f:
        answers_map = json.load(f)
        
    render_pages(pdf_path, 6, 76)
    lines = ocr_and_collect_lines(6, 76)
    questions = build_questions_json(lines, answers_map)
    print(f"Total structured questions: {len(questions)}")
    
    with open("chemia_otazky_1_300.json", "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    print("Saved to chemia_otazky_1_300.json")
