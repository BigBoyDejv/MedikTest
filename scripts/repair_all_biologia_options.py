import os
import re
import io
import json
import fitz
import numpy as np
from PIL import Image
from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()

pdf_files = [f for f in os.listdir('.') if 'Biol' in f and f.endswith('.pdf')]
if not pdf_files:
    raise FileNotFoundError("Biologia PDF not found!")
pdf_path = pdf_files[0]
doc = fitz.open(pdf_path)

# 1. Load OCR cache
with open("temp_bio_ocr_7_98.json", "r", encoding="utf-8") as f:
    lines_by_page = json.load(f)

# Helper to split side-by-side options e.g. "a) xxx e) yyy"
def split_options(line):
    matches = list(re.finditer(r'(?:^|\s+)([a-hA-H])[\)\.\,\:]\s*', line))
    if not matches:
        return [(None, line)]
    results = []
    if matches[0].start() > 0:
        prefix = line[:matches[0].start()].strip()
        if prefix:
            results.append((None, prefix))
    for i in range(len(matches)):
        opt_char = matches[i].group(1).lower()
        start_idx = matches[i].end()
        end_idx = matches[i+1].start() if i + 1 < len(matches) else len(line)
        opt_text = line[start_idx:end_idx].strip()
        results.append((opt_char, opt_text))
    return results

def is_q_start(line, expected_num):
    m = re.match(r'^([0-9]{1,3})(?:[\.\,\:\)]\d?|[\.\,\:\)])?\s*(.*)', line)
    if m:
        num = int(m.group(1))
        if abs(num - expected_num) <= 2 and 1 <= num <= 450:
            return num, m.group(2).strip()
    return None, line

# Build initial questions from OCR lines
all_lines = []
for p_num in sorted([int(k) for k in lines_by_page.keys()]):
    for l in lines_by_page[str(p_num)]:
        l_str = l.strip()
        if l_str:
            all_lines.append((p_num, l_str))

questions = {}
current_q = None
expected_q_num = 1
last_opt = None

for p_num, raw_line in all_lines:
    q_num, rest = is_q_start(raw_line, expected_q_num)
    if q_num:
        if current_q:
            questions[current_q['num']] = current_q
        current_q = {
            'num': q_num,
            'page': p_num,
            'content': f"{q_num}. {rest}".strip(),
            'options': {},
            'in_options': False
        }
        expected_q_num = q_num + 1
        last_opt = None
        continue
    if not current_q:
        continue
    parts = split_options(raw_line)
    for opt_char, text in parts:
        if opt_char:
            current_q['in_options'] = True
            current_q['options'][opt_char] = text
            last_opt = opt_char
        else:
            if not current_q['in_options']:
                current_q['content'] = (current_q['content'] + ' ' + text).strip()
            elif last_opt:
                current_q['options'][last_opt] = (current_q['options'][last_opt] + ' ' + text).strip()

if current_q:
    questions[current_q['num']] = current_q

print(f"Initially parsed {len(questions)} questions.")

# Known missing question definitions from our scan
known_missing_questions = {
    152: {
        "page": 37,
        "content": "152. Význam baktérií v prirodzených ekologických systémoch spočíva v tom, že:",
        "options": {
            "a": "produkujú do atmosféry kyslík",
            "b": "spôsobujú infekčné ochorenia",
            "c": "sú schopné žiť vo fyziologicky extrémnych podmienkach",
            "d": "rozkladajú odumreté telá rastlín a živočíchov",
            "e": "obohacujú pôdu o organické zlúčeniny potrebné k fotosyntéze rastlín",
            "f": "zohrávajú nezastupiteľnú úlohu pri cyklickej premene látok v prírode",
            "g": "mineralizujú organický materiál",
            "h": "pomáhajú pri samočistení vodných tokov"
        }
    },
    168: {
        "page": 41,
        "content": "168. Vek stromov môžeme zistiť na základe:",
        "options": {
            "a": "počtu lenticel",
            "b": "letokruhov",
            "c": "borky",
            "d": "rozdielnej štruktúry a farby sekundárneho dreva na jar a v lete",
            "e": "rozdielnej štruktúry a farby primárneho dreva na jar a v lete",
            "f": "hrúbky kmeňa",
            "g": "počtu stržňových lúčov",
            "h": "počtu vetiev"
        }
    },
    189: {
        "page": 44,
        "content": "189. Ktoré metabolické procesy v rastlinách sú spojené s uvoľňovaním energie:",
        "options": {
            "a": "fotosyntéza",
            "b": "dýchanie",
            "c": "anabolické",
            "d": "katabolické",
            "e": "asimilačné",
            "f": "disimilačné",
            "g": "vznik energeticky bohatých látok - asimilátov",
            "h": "syntéza nových organických látok"
        }
    },
    366: {
        "page": 81,
        "content": "366. Ktoré organické látky sú celkovo hmotnostne najviac zastúpené v krvnej plazme človeka?",
        "options": {
            "a": "močovina",
            "b": "nukleové kyseliny",
            "c": "glukóza",
            "d": "monosacharidy",
            "e": "bielkoviny",
            "f": "voda",
            "g": "lipidy",
            "h": "kreatín"
        }
    },
    417: {
        "page": 91,
        "content": "417. Najlepšie vyvinutý sluch so schopnosťou vnímať aj ultrazvukové signály majú:",
        "options": {
            "a": "mačkovité mäsožravce",
            "b": "netopiere",
            "c": "veľryby",
            "d": "psovité mäsožravce",
            "e": "ryby",
            "f": "larvy obojživelníkov",
            "g": "hmyz",
            "h": "obrúčkavce"
        }
    }
}

for q_num, q_data in known_missing_questions.items():
    questions[q_num] = {
        "num": q_num,
        "page": q_data["page"],
        "content": q_data["content"],
        "options": q_data["options"]
    }

# Specific missing options found during high-res analysis
known_missing_options = {
    1: {"e": "živých sústav na úrovni ich základnej štruktúrnej a funkčnej jednotky"},
    4: {
        "content": "4. Ktoré štruktúry prokaryotickej bunky sú zodpovedné za uvoľňovanie energie:",
        "e": "plazmatická membrána"
    },
    20: {"e": "ktoré upravujú látky syntetizované na ribozómoch, aby mohli byť vylúčené z bunky von"},
    34: {"c": "homologické majú rovnaký tvar a vždy rovnaké alely"},
    40: {
        "f": "sú pasívny transport",
        "h": "nevyžadujú spotrebu energie ATP"
    },
    56: {"c": "dochádza k syntéze RNA a bielkovín"},
    59: {
        "b": "v G2 fáze sa zdvojuje genetický materiál",
        "d": "v S fáze nastáva replikácia jadrovej DNA",
        "f": "v M fáze dochádza k deleniu jadra a bunky"
    },
    67: {"a": "sa chromatín špiralizuje a kondenzuje do chromozómov"},
    68: {"h": "dochádza k zániku jadierka a jadrového obalu"},
    105: {
        "e": "sú makromolekulové látky",
        "f": "majú stavebnú funkciu",
        "g": "katalyzujú biochemické reakcie v bunke"
    },
    127: {"h": "obsahuje ribózu alebo deoxyribózu"},
    136: {"f": "je schopná samostatného rozmnožovania mimo hostiteľskej bunky"},
    147: {
        "g": "obsahujú peptidoglykán mureín",
        "h": "majú bunkovú stenu tvorenú celulózou"
    },
    148: {"c": "sú nepohyblivé bez bičíkov"},
    157: {
        "d": "parenchymatické bunky",
        "h": "sklerenchymatické vlákna"
    },
    171: {
        "e": "adventívne korene",
        "h": "hlavný koreň s bočnými koreňmi"
    },
    178: {"a": "kvet"},
    193: {"c": "prebieha v mitochondriách"},
    199: {
        "b": "je spôsob výživy napr. imela bieleho",
        "d": "kombinuje autotrofiu a heterotrofiu",
        "h": "využívajú mäsožravé rastliny"
    },
    221: {"g": "chloroplasty"},
    226: {"a": "sú primárne producenty organickej hmoty"},
    233: {"h": "uvoľňuje sa molekulový kyslík"},
    242: {
        "d": "v stróme chloroplastov",
        "e": "v tylakoidoch chloroplastov"
    },
    252: {"h": "závisí od koncentrácie CO2 a teploty"},
    253: {"a": "glykolýza"},
    267: {"d": "hladké svalové tkanivo"},
    270: {"f": "myoglobín"},
    279: {"e": "sú spojené interkalárnymi diskami"},
    283: {
        "f": "gangliá",
        "g": "nervové vlákna"
    },
    284: {"h": "zabezpečujú prenos vzruchov len jedným smerom"},
    294: {"e": "tráviaca dutina prhlivcov"},
    305: {"c": "gastrovaskulárna sústava"},
    318: {"a": "pečeň"},
    328: {"b": "žlčník"},
    334: {"c": "metanefrídie"},
    339: {"a": "pľúcne vaky"},
    347: {"b": "žiabre"},
    349: {"c": "acetylcholín"},
    356: {"f": "otvorená obehová sústava"},
    370: {"h": "hemoglobín"},
    371: {"f": "vtákov"},
    375: {"g": "leukocyty"},
    390: {
        "c": "monocyty",
        "d": "lymfocyty",
        "e": "neutrofilné granulocyty",
        "f": "eozinofilné granulocyty",
        "g": "bazofilné granulocyty"
    },
    396: {"c": "trombocyty"},
    402: {"g": "predĺžená miecha"},
    414: {"c": "Cortiho orgán"},
    420: {
        "f": "týmus",
        "h": "slezina"
    },
    430: {"g": "tyroxín"},
    435: {"g": "inzulín"},
    436: {
        "g": "glukagón",
        "h": "adrenalín"
    },
    437: {"a": "melatonín"},
    446: {"b": "testosterón"},
    449: {"c": "progesterón"}
}

for q_num, opt_dict in known_missing_options.items():
    if q_num in questions:
        for k, v in opt_dict.items():
            if k == "content":
                questions[q_num]["content"] = v
            else:
                questions[q_num]["options"][k] = v

# Verify every question 1..450 exists and check missing options
missing_overall = []
for i in range(1, 451):
    if i not in questions:
        missing_overall.append((i, "MISSING QUESTION"))
    else:
        opts = questions[i]["options"]
        miss_k = [k for k in 'abcdefgh' if k not in opts or not opts[k].strip()]
        if miss_k:
            missing_overall.append((i, miss_k))

print(f"Total questions with missing options after repair: {len(missing_overall)}")
if missing_overall:
    for m in missing_overall[:20]:
        print(m)
else:
    print("ALL 450 QUESTIONS HAVE 100% OF ALL 8 OPTIONS (a..h)!")

with open("temp_bio_repaired_questions.json", "w", encoding="utf-8") as f:
    json.dump({str(k): v for k, v in sorted(questions.items())}, f, ensure_ascii=False, indent=2)

