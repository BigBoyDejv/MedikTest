import sys
import os
sys.path.insert(0, os.path.abspath("."))
import json
import re
import fitz
import io
import numpy as np
from PIL import Image
from rapidocr_onnxruntime import RapidOCR
from scripts.parse_bio_questions_full import clean_slovak_ocr_text

engine = RapidOCR()
doc = fitz.open("Biológia 2026.pdf")

with open("data/ocr_cache_bio_clovek_451_900.json", "r", encoding="utf-8") as f:
    cache = json.load(f)

q_regex = re.compile(r'^(\d{3,4})[\.\,\:]\s*(.*)')
opt_regex = re.compile(r'^([a-hA-H])[\)\.\,\:]\s*(.*)')

# 1. First pass: group by question
all_items = []
for p_num in sorted([int(k) for k in cache.keys()]):
    blocks = cache[str(p_num)]
    blocks.sort(key=lambda b: (b[1], b[0]))
    for bx, by, txt in blocks:
        all_items.append((p_num, bx, by, txt))

questions = {}
current_q = None

for p_num, bx, by, txt in all_items:
    m_q = q_regex.match(txt)
    if m_q:
        num = int(m_q.group(1))
        if 451 <= num <= 900:
            if current_q:
                questions[current_q['num']] = current_q
            current_q = {
                'num': num,
                'page': p_num,
                'by': by,
                'content': f"{num}. {m_q.group(2)}".strip(),
                'options': {},
                'current_opt': None
            }
            continue

    if current_q:
        m_opt = opt_regex.match(txt)
        if m_opt:
            opt_id = m_opt.group(1).lower()
            # If we see option 'a' when current_q already has 'g' or 'h',
            # it means a new question started without its header being detected!
            if opt_id == 'a' and any(k in current_q['options'] for k in ['f', 'g', 'h']):
                next_num = current_q['num'] + 1
                if 451 <= next_num <= 900:
                    questions[current_q['num']] = current_q
                    current_q = {
                        'num': next_num,
                        'page': p_num,
                        'by': by,
                        'content': f"{next_num}.", # placeholder title to be recovered
                        'options': {},
                        'current_opt': None,
                        'recovered': True,
                        'opt_a_by': by
                    }

            if current_q:
                current_q['options'][opt_id] = m_opt.group(2).strip()
                current_q['current_opt'] = opt_id
        else:
            if current_q['current_opt']:
                current_q['options'][current_q['current_opt']] += ' ' + txt
            else:
                current_q['content'] += ' ' + txt

if current_q and 451 <= current_q['num'] <= 900:
    questions[current_q['num']] = current_q

print(f"Total parsed with implicit header recovery: {len(questions)}/450!")
missing = [n for n in range(451, 901) if n not in questions]
print(f"Still missing: {len(missing)} -> {missing}")

# Now for any question with 'recovered' == True, recover the real title from the PDF line right above opt 'a'!
for qnum, q in questions.items():
    if q.get('recovered') or q['content'] == f"{qnum}.":
        p_idx = q['page'] - 1
        page = doc[p_idx]
        pix = page.get_pixmap(dpi=200)
        img = Image.open(io.BytesIO(pix.tobytes()))
        # opt_a_by is the vertical position of option 'a'. The title line is ~60px above it!
        a_y = q.get('opt_a_by', 500)
        y1 = max(0, a_y - 85)
        y2 = min(img.height, a_y - 15)
        crop = img.crop((80, y1, 1400, y2))
        new_w = int(crop.width * (48.0 / crop.height))
        resized = crop.resize((new_w, 48), Image.Resampling.LANCZOS)
        res, _ = engine.text_recognizer([np.array(resized)])
        if res and res[0][0]:
            title_text = clean_slovak_ocr_text(res[0][0].strip())
            # Ensure it starts with number
            if not title_text.startswith(str(qnum)):
                title_text = f"{qnum}. {title_text}"
            q['content'] = title_text
            print(f"Recovered title for Q{qnum}: {q['content']}")
