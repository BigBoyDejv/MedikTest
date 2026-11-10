import os
import re
import json
import fitz
import numpy as np
from PIL import Image
import io
from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()

def clean_slovak_ocr_text(text):
    if not text:
        return ""
    replacements = [
        ("t'", "ť"), ("d'", "ď"), ("l'", "ľ"), ("c'", "č"),
        ("T'", "Ť"), ("D'", "Ď"), ("L'", "Ľ"), ("C'", "Č"),
        ("a'", "á"), ("e'", "é"), ("i'", "í"), ("o'", "ó"), ("u'", "ú"), ("y'", "ý"),
        ("Zivoichov", "živočíchov"), ("zivoichov", "živočíchov"),
        ("Zivochov", "živočíchov"), ("zivochov", "živočíchov"),
        ("Zivocich", "živočích"), ("zivocich", "živočích"),
        ("crenove", "črenové"), ("Crenove", "Črenové"),
        ("Crenovych", "črenových"), ("crenovych", "črenových"),
        ("rezakov", "rezákov"), ("Rezakov", "Rezákov"),
        ("stoliciek", "stoličiek"), ("Stoliciek", "Stoličiek"),
        ("diet'at'a", "dieťaťa"), ("dietata", "dieťaťa"), ("dietatu", "dieťaťu"),
        ("zl'azy", "žľazy"), ("zl'az", "žliaz"), ("zlaza", "žľaza"),
        ("travenie", "trávenie"), ("traviace", "tráviace"), ("traviaci", "tráviaci"),
        ("zaludok", "žalúdok"), ("zaludka", "žalúdka"), ("zaludocna", "žalúdočná"),
        ("pecen", "pečeň"), ("pecene", "pečene"),
        ("oblicky", "obličky"), ("obliciek", "obličiek"),
        ("priusna", "príušná"), ("priusne", "príušné"), ("priusnymi", "príušnými"),
        ("podsankova", "podsánková"), ("podsankove", "podsánkové"), ("podsankovymi", "podsánkovými"),
        ("podjazykova", "podjazyková"), ("podjazykove", "podjazykové"), ("podjazykovymi", "podjazykovými"),
        ("mocove", "močové"), ("mocovy", "močový"), ("moc", "moč"),
        ("dychacie", "dýchacie"), ("dychanie", "dýchanie"), ("pluca", "pľúca"), ("pluc", "pľúc"),
        ("krvny", "krvný"), ("cievy", "cievy"), ("srdce", "srdce"), ("srdca", "srdca"),
        ("komora", "komora"), ("predsien", "predsieň"), ("chlopna", "chlopňa"), ("chlopne", "chlopne"),
        ("erytrocyty", "erytrocyty"), ("leukocyty", "leukocyty"), ("trombocyty", "trombocyty"),
        ("imunita", "imunita"), ("protilatky", "protilátky"),
        ("kostra", "kostra"), ("kosti", "kosti"), ("lebka", "lebka"), ("chrbtica", "chrbtica"),
        ("svaly", "svaly"), ("sval", "sval"),
        ("mozog", "mozog"), ("miecha", "miecha"), ("nervy", "nervy"), ("nervova", "nervová"),
        ("zmysly", "zmysly"), ("oko", "oko"), ("ucho", "ucho"),
        ("chromozom", "chromozóm"), ("chromozomy", "chromozómy"), ("chromozomov", "chromozómov"),
        ("struktura", "štruktúra"), ("strukturny", "štruktúrny"),
        ("gen", "gén"), ("geny", "gény"), ("genov", "génov"),
        ("dedicnost", "dedičnosť"), ("premenlivost", "premenlivosť"),
        ("krizenie", "kríženie"), ("alela", "alela"), ("alely", "alely"),
        ("dominantny", "dominantný"), ("recesivny", "recesívny"),
        ("homozygot", "homozygot"), ("heterozygot", "heterozygot"),
        ("uplathuju", "uplatňujú"), ("uplatnuje", "uplatňuje"),
        ("ovplyvnuju", "ovplyvňujú"), ("ovplyvnuje", "ovplyvňuje"),
        ("zbranuju", "zabraňujú"), ("zabrani", "zabráni"),
        ("spravanie", "správanie"), ("spravania", "správania")
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text.strip()

def ocr_and_parse_bio_chapter(pdf_path, start_page, end_page, start_q, end_q, category_name, answers, cache_file):
    os.makedirs("data", exist_ok=True)
    cache_path = os.path.join("data", cache_file)

    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            blocks_by_page = json.load(f)
    else:
        blocks_by_page = {}

    doc = fitz.open(pdf_path)
    total_pages = end_page - start_page + 1

    for p_idx in range(start_page - 1, end_page):
        p_str = str(p_idx + 1)
        if p_str in blocks_by_page and len(blocks_by_page[p_str]) > 0:
            continue

        page = doc[p_idx]
        pix = page.get_pixmap(dpi=200)
        img = Image.open(io.BytesIO(pix.tobytes()))
        res, _ = engine(np.array(img))

        raw_blocks = []
        if res:
            for box, text, score in res:
                bx = sum(pt[0] for pt in box) / 4.0
                by = sum(pt[1] for pt in box) / 4.0
                t = clean_slovak_ocr_text(text.strip())
                if by > 2400 and (t.isdigit() or len(t) <= 4):
                    continue
                raw_blocks.append((int(bx), int(by), t))

        blocks_by_page[p_str] = raw_blocks
        if len(blocks_by_page) % 10 == 0 or (p_idx + 1) == end_page:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(blocks_by_page, f, ensure_ascii=False)
            print(f"OCR progress ({category_name}): Page {p_idx+1}/{end_page} ({len(blocks_by_page)}/{total_pages})", flush=True)

    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(blocks_by_page, f, ensure_ascii=False)

    q_regex = re.compile(r'^(\d{3,4})[\.\,\:]\s*(.*)')
    opt_regex = re.compile(r'^([a-hA-H])[\)\.\,\:]\s*(.*)')

    parsed_qs = {}
    current_q = None

    for p_num in sorted([int(k) for k in blocks_by_page.keys()]):
        page_blocks = blocks_by_page[str(p_num)]
        page_blocks.sort(key=lambda b: (b[1], b[0]))
        for bx, by, txt in page_blocks:
            m_q = q_regex.match(txt)
            if m_q:
                cand_num = int(m_q.group(1))
                if start_q <= cand_num <= end_q:
                    if current_q:
                        parsed_qs[current_q["num"]] = current_q
                    current_q = {
                        "num": cand_num,
                        "page": p_num,
                        "by": by,
                        "content": f"{cand_num}. {m_q.group(2)}".strip(),
                        "options": {},
                        "current_opt": None
                    }
                    continue

            if current_q:
                m_opt = opt_regex.match(txt)
                if m_opt:
                    opt_id = m_opt.group(1).lower()
                    if opt_id == 'a' and any(k in current_q["options"] for k in ['f', 'g', 'h']):
                        next_num = current_q["num"] + 1
                        if start_q <= next_num <= end_q:
                            parsed_qs[current_q["num"]] = current_q
                            current_q = {
                                "num": next_num,
                                "page": p_num,
                                "by": by,
                                "content": f"{next_num}.",
                                "options": {},
                                "current_opt": None,
                                "recovered": True,
                                "opt_a_by": by
                            }

                    if current_q:
                        current_q["options"][opt_id] = m_opt.group(2).strip()
                        current_q["current_opt"] = opt_id
                else:
                    if current_q["current_opt"]:
                        current_q["options"][current_q["current_opt"]] += " " + txt
                    else:
                        current_q["content"] += " " + txt

    if current_q and start_q <= current_q["num"] <= end_q:
        parsed_qs[current_q["num"]] = current_q

    # Recover any missed question titles by reading the line right above option 'a'
    for qnum, q in parsed_qs.items():
        if q.get("recovered") or q["content"] == f"{qnum}.":
            p_idx = q["page"] - 1
            if 0 <= p_idx < len(doc):
                page = doc[p_idx]
                pix = page.get_pixmap(dpi=200)
                img = Image.open(io.BytesIO(pix.tobytes()))
                a_y = q.get("opt_a_by", 500)
                y1 = max(0, a_y - 85)
                y2 = min(img.height, a_y - 15)
                crop = img.crop((80, y1, 1400, y2))
                new_w = int(crop.width * (48.0 / crop.height))
                resized = crop.resize((new_w, 48), Image.Resampling.LANCZOS)
                res, _ = engine.text_recognizer([np.array(resized)])
                if res and res[0][0]:
                    title_text = clean_slovak_ocr_text(res[0][0].strip())
                    if not title_text.startswith(str(qnum)):
                        title_text = f"{qnum}. {title_text}"
                    q["content"] = title_text

    final_items = []
    letters_all = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

    for num in range(start_q, end_q + 1):
        correct = answers.get(num, answers.get(str(num), []))
        if correct:
            exp_text = f"Správne možnosti podľa oficiálneho kľúča LF UPJŠ: {', '.join([c.upper() for c in correct])}."
        else:
            exp_text = "Táto otázka nemá v oficiálnom kľúči LF UPJŠ vyznačenú správnu odpoveď (otázka bola vyradená/uznaná plným počtom bodov)."

        if num in parsed_qs:
            q = parsed_qs[num]
            opt_dict = q["options"]
            content = q["content"]
        else:
            opt_dict = {}
            content = f"{num}. Otázka č. {num} ({category_name}):"

        options_list = []
        for l in letters_all:
            txt = opt_dict.get(l, "").strip()
            options_list.append({
                "id": l,
                "text": txt if txt else f"Možnosť {l.upper()}"
            })

        final_items.append({
            "subject": "Biológia",
            "category": category_name,
            "content": content,
            "options": options_list,
            "correct_answers": correct,
            "explanation": exp_text
        })

    return final_items, parsed_qs
