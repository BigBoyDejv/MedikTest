import sys
import os
sys.path.insert(0, os.path.abspath("."))
import fitz
import numpy as np
import io
import re
from PIL import Image
from rapidocr_onnxruntime import RapidOCR
from scripts.parse_bio_questions_full import clean_slovak_ocr_text

doc = fitz.open('Biológia 2026.pdf')
engine = RapidOCR()
pix = doc[97].get_pixmap(dpi=150)
res, _ = engine(np.array(Image.open(io.BytesIO(pix.tobytes()))))

q_regex = re.compile(r'^(\d{3,4})[\.\,\:]\s*(.*)')
opt_regex = re.compile(r'^([a-hA-H])[\)\.\,\:]\s*(.*)')

questions = {}
current_q = None

for b in res:
    txt = clean_slovak_ocr_text(b[1].strip())
    bx, by = b[0][0]
    if by > 1850 and (txt.isdigit() or len(txt) <= 3):
        continue

    m_q = q_regex.match(txt)
    if m_q and bx < 140:
        if current_q:
            questions[current_q['num']] = current_q
        current_q = {
            'num': int(m_q.group(1)),
            'content': f"{m_q.group(1)}. {m_q.group(2)}".strip(),
            'options': {},
            'current_opt': None
        }
        continue

    if current_q:
        m_opt = opt_regex.match(txt)
        if m_opt:
            opt_id = m_opt.group(1).lower()
            current_q['options'][opt_id] = m_opt.group(2).strip()
            current_q['current_opt'] = opt_id
        else:
            if current_q['current_opt']:
                current_q['options'][current_q['current_opt']] += ' ' + txt
            else:
                current_q['content'] += ' ' + txt

if current_q:
    questions[current_q['num']] = current_q

for qnum in sorted(questions.keys()):
    q = questions[qnum]
    print(f"=== Q{qnum}: {q['content']} ===")
    for l in 'abcdefgh':
        print(f"  {l}) {q['options'].get(l, 'MISSING')}")
