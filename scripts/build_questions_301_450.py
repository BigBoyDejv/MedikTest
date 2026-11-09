import json
import re

# Načítanie OCR riadkov a kľúča
with open('temp_ocr_lines_76_100.json', 'r', encoding='utf-8') as f:
    pages = json.load(f)

with open('data_answers_301_600.json', 'r', encoding='utf-8') as f:
    answers = json.load(f)

# Všetky riadky zoradené podľa strán
all_lines = []
for p in sorted([int(k) for k in pages.keys()]):
    for l in pages[str(p)]:
        all_lines.append(l.strip())

q_start_regex = re.compile(r'^(\d+)\.\s*(.*)')
opt_regex = re.compile(r'^([a-hA-H])\.\s*(.*)')

parsed_qs = {}
current_q = None

for line in all_lines:
    m_q = q_start_regex.match(line)
    if m_q:
        q_num = int(m_q.group(1))
        if (301 <= q_num <= 340) or (391 <= q_num <= 450):
            if current_q:
                parsed_qs[current_q['num']] = current_q
            current_q = {
                'num': q_num,
                'content': f"{q_num}. {m_q.group(2).strip()}",
                'options_dict': {},
                'current_opt': None
            }
            continue
        else:
            if current_q:
                parsed_qs[current_q['num']] = current_q
                current_q = None
            continue

    if current_q:
        m_opt = opt_regex.match(line)
        if m_opt:
            opt_id = m_opt.group(1).lower()
            current_q['options_dict'][opt_id] = m_opt.group(2).strip()
            current_q['current_opt'] = opt_id
        else:
            if current_q['current_opt']:
                current_q['options_dict'][current_q['current_opt']] += ' ' + line
            else:
                current_q['content'] += ' ' + line

if current_q:
    parsed_qs[current_q['num']] = current_q

# Doplnenie chýbajúcich otázok (page boundaries)
manual_questions = {
    309: {
        "content": "309. V ktorych reakciach vystupuje voda ako kyselina?",
        "options_dict": {
            "a": "(HCO3)- + H2O → (CO3)2- + (H3O)+",
            "b": "CH3NH2 + H2O → CH3NH3+ + (OH)-",
            "c": "(HCOO)- + H2O → HCOOH + (OH)-",
            "d": "C6H5OH + H2O → (C6H5O)- + (H3O)+",
            "e": "(HSO3)- + H2O → (SO3)2- + (H3O)+",
            "f": "(CH3COO)- + H2O → CH3COOH + (OH)-",
            "g": "NH3 + H2O → (NH4)+ + (OH)-",
            "h": "(HSO4)- + H2O → (SO4)2- + (H3O)+"
        }
    },
    313: {
        "content": "313. Medzi silne kyseliny zaradujeme:",
        "options_dict": {
            "a": "kyselinu citronovu",
            "b": "CCl3COOH",
            "c": "kyselinu trichloroctovu",
            "d": "kyselinu chlornu",
            "e": "kyselinu manganistu",
            "f": "kyselinu siricitu",
            "g": "kyselinu kyanovodikovu",
            "h": "kyselinu chloristu"
        }
    },
    314: {
        "content": "314. Ktoré castice mozu vo vodnom prostredi posobit len ako bazy?",
        "options_dict": {
            "a": "H2O",
            "b": "OH-",
            "c": "NH4+",
            "d": "NH3",
            "e": "S2-",
            "f": "HS-",
            "g": "(PO4)3-",
            "h": "Cl-"
        }
    },
    322: {
        "content": "322. Pri redukcii latka:",
        "options_dict": {
            "a": "sa redukuje",
            "b": "sa oxiduje",
            "c": "je redukovadlo",
            "d": "je oxidovadlo",
            "e": "meni svoje oxidacne cislo",
            "f": "nemeni svoje oxidacne cislo",
            "g": "prijima elektrony",
            "h": "odovzdava elektrony"
        }
    },
    323: {
        "content": "323. Oxidacia je dej, pri ktorom dochadza k:",
        "options_dict": {
            "a": "odovzdavaniu elektronov",
            "b": "prijimaniu elektronov",
            "c": "zvyseniu oxidacneho cisla",
            "d": "znizeniu oxidacneho cisla",
            "e": "redukcii danej latky",
            "f": "oxidacii danej latky",
            "g": "adiciu kyslika",
            "h": "zmensovaniu oxidacneho cisla"
        }
    },
    336: {
        "content": "336. Vyberte zodpovedajuce ciastkove reakcie a spravne stechiometricke koeficienty oxidacno-redukcnej reakcie As2O3 + Zn + H2SO4 → AsH3 + ZnSO4 + H2O:",
        "options_dict": {
            "a": "su koeficienty 6, 1, 12 → 6, 2, 3",
            "b": "su koeficienty 1, 6, 6 → 2, 6, 3",
            "c": "je ciastkova reakcia AsIII + 6e- → As-III",
            "d": "vznikaju 3 moly vody",
            "e": "sa vymiena 12 elektronov",
            "f": "je ciastkova reakcia Zn0 - 2e- → ZnII",
            "g": "je ciastkova reakcia Zn0 + 2e- → ZnII",
            "h": "arzen sa redukuje"
        }
    },
    447: {
        "content": "447. Striebro:",
        "options_dict": {
            "a": "Ag je biogenny makroprvok",
            "b": "Ag sa pouziva na vyrobu zrkadiel",
            "c": "Ag je reaktivnejsie ako med",
            "d": "reaguje s kyselinou chlorovodikovou",
            "e": "vytvara zliatinu amalgam",
            "f": "je najlepsim vodicom elektrickeho prudu",
            "g": "v zluceninach ma najcastejsie oxidacne cislo +I",
            "h": "reaguje s koncentrovanou kyselinou dusicnou"
        }
    }
}

for num, qdata in manual_questions.items():
    parsed_qs[num] = {
        'num': num,
        'content': qdata['content'],
        'options_dict': qdata['options_dict'],
        'current_opt': None
    }

# Vytvorenie finálnych 100 otázok (301-340 a 391-450)
final_items = []
expected_nums = list(range(301, 341)) + list(range(391, 451))

for num in expected_nums:
    if num not in parsed_qs:
        print(f"CRITICAL: Question {num} still missing!")
        continue
    
    q = parsed_qs[num]
    opt_dict = q['options_dict']
    
    # Zoradenie options a-h
    options_list = []
    for letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
        text = opt_dict.get(letter, f"Možnosť {letter.upper()}")
        options_list.append({
            'id': letter,
            'text': text
        })
        
    correct = answers.get(str(num), [])
    explanation = f"Správne odpovede podľa oficiálneho kľúča testovnice UPJŠ LF sú: {', '.join(a.upper() for a in correct)}."
    
    final_items.append({
        'subject': 'Chémia',
        'category': 'Všeobecná a anorganická chémia',
        'content': q['content'],
        'options': options_list,
        'correct_answers': correct,
        'explanation': explanation
    })

print(f"Total compiled questions: {len(final_items)}")
with open('chemia_otazky_301_450.json', 'w', encoding='utf-8') as f:
    json.dump(final_items, f, ensure_ascii=False, indent=2)

print("Saved chemia_otazky_301_450.json successfully!")

