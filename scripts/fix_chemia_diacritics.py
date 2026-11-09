import os
import re
import json
import urllib.request
import urllib.parse
import unicodedata

def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

# 1. Load dictionaries
print("Loading Slovak wordlist and Hunspell dictionaries...")
word_map = {}

dict_path = "temp_pages/sk_wordlist.txt"
if os.path.exists(dict_path):
    with open(dict_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                w = parts[0]
                try:
                    freq = int(parts[1])
                except:
                    freq = 1
                key = strip_accents(w).lower()
                if key not in word_map or freq > word_map[key][1]:
                    word_map[key] = (w, freq)

hunspell_path = "temp_pages/sk_SK.dic"
if os.path.exists(hunspell_path):
    with open(hunspell_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            w = line.split("/")[0].strip()
            if w:
                key = strip_accents(w).lower()
                if key not in word_map:
                    word_map[key] = (w, 500)

print(f"Dictionary size: {len(word_map)} unique normalized words.")

# 2. Comprehensive Chemistry & Medical dictionary overrides
chemical_overrides = {
    # Otázkové frázy a pokyny
    "priradte": "priraďte", "prirad": "priraď", "vyberte": "vyberte", "oznacte": "označte",
    "spravne": "správne", "spravny": "správny", "spravna": "správna", "spravnu": "správnu",
    "spravnym": "správnym", "spravnych": "správnych", "spravnymi": "správnymi",
    "nespravne": "nesprávne", "nespravny": "nesprávny", "nespravna": "nesprávna", "nespravnu": "nesprávnu",
    "nespravnym": "nesprávnym", "nespravnych": "nesprávnych", "nespravnymi": "nesprávnymi",
    "ktore": "ktoré", "ktory": "ktorý", "ktora": "ktorá", "ktoru": "ktorú", "ktoreho": "ktorého",
    "ktorej": "ktorej", "ktorych": "ktorých", "ktorym": "ktorým", "ktorymi": "ktorými",
    "tvrdenie": "tvrdenie", "tvrdenia": "tvrdenia", "tvrdeni": "tvrdení", "tvrdeniam": "tvrdeniam", "tvrdeniami": "tvrdeniami",
    "moznost": "možnosť", "moznosti": "možnosti", "moznostou": "možnosťou", "moznostiach": "možnostiach",
    "patri": "patrí", "patria": "patria", "nepatri": "nepatrí", "nepatria": "nepatria",
    "moze": "môže", "mozu": "môžu", "nemoze": "nemôže", "nemozu": "nemôžu",
    "obsahuje": "obsahuje", "obsahuju": "obsahujú", "neobsahuje": "neobsahuje", "neobsahuju": "neobsahujú",
    "vznika": "vzniká", "vznikaju": "vznikajú", "reaguje": "reaguje", "reaguju": "reagujú",
    "znazornuje": "znázorňuje", "vyjadruje": "vyjadruje", "predstavuje": "predstavuje",
    "uvadza": "uvádza", "uvadza sa": "uvádza sa", "plati": "platí", "neplati": "neplatí",

    # Zmesi, roztoky, stavy
    "zmes": "zmes", "zmesi": "zmesi", "zmesou": "zmesou", "zmesiach": "zmesiach",
    "roznoroda": "rôznorodá", "roznorode": "rôznorodé", "roznorody": "rôznorodý", "roznorodej": "rôznorodej", "roznorodych": "rôznorodých",
    "rovnoroda": "rovnorodá", "rovnorode": "rovnorodé", "rovnorody": "rovnorodý", "rovnorodej": "rovnorodej", "rovnorodych": "rovnorodých",
    "suspenzia": "suspenzia", "suspenzie": "suspenzie", "suspenziou": "suspenziou",
    "emulzia": "emulzia", "emulzie": "emulzie", "emulziou": "emulziou",
    "aerosol": "aerosól", "aerosoly": "aerosóly", "aerosolu": "aerosólu", "aerosolom": "aerosólom",
    "roztok": "roztok", "roztoku": "roztoku", "roztoky": "roztoky", "roztokov": "roztokov", "roztokom": "roztokom", "roztokoch": "roztokoch",
    "rozpustadlo": "rozpúšťadlo", "rozpustadla": "rozpúšťadlá", "rozpustadiel": "rozpúšťadiel", "rozpustadlach": "rozpúšťadlách",
    "rozpustnost": "rozpustnosť", "rozpustnosti": "rozpustnosti", "rozpustnostou": "rozpustnosťou",
    "rozpustny": "rozpustný", "rozpustna": "rozpustná", "rozpustne": "rozpustné", "rozpustnych": "rozpustných",
    "nerozpustny": "nerozpustný", "nerozpustna": "nerozpustná", "nerozpustne": "nerozpustné", "nerozpustnych": "nerozpustných",
    "nasyteny": "nasýtený", "nasytena": "nasýtená", "nasytene": "nasýtené", "nasytenych": "nasýtených",
    "nenasyteny": "nenasýtený", "nenasytena": "nenasýtená", "nenasytene": "nenasýtené", "nenasytenych": "nenasýtených",
    "presyteny": "presýtený", "presytena": "presýtená", "presytene": "presýtené",

    # Fyzikálno-chemické veličiny
    "hmotnost": "hmotnosť", "hmotnosti": "hmotnosti", "hmotnostou": "hmotnosťou",
    "hmotnostny": "hmotnostný", "hmotnostna": "hmotnostná", "hmotnostne": "hmotnostné", "hmotnostneho": "hmotnostného", "hmotnostnej": "hmotnostnej",
    "objem": "objem", "objemu": "objemu", "objemom": "objemom", "objemovy": "objemový", "objemova": "objemová", "objemove": "objemové",
    "hustota": "hustota", "hustoty": "hustoty", "hustotou": "hustotou",
    "teplota": "teplota", "teploty": "teploty", "teplotou": "teplotou", "teplote": "teplote",
    "tlak": "tlak", "tlaku": "tlaku", "tlakom": "tlakom",
    "latkove": "látkové", "latkovy": "látkový", "latkova": "látková", "latkoveho": "látkového", "latkovej": "látkovej",
    "mnozstvo": "množstvo", "mnozstva": "množstvá", "mnozstvom": "množstvom", "mnozstiev": "množstiev",
    "molarna": "molárna", "molarny": "molárny", "molarne": "molárne", "molarneho": "molárneho", "molarnej": "molárnej",
    "koncentracia": "koncentrácia", "koncentracie": "koncentrácie", "koncentraciou": "koncentráciou", "koncentracii": "koncentrácií",
    "rovnovaha": "rovnováha", "rovnovahy": "rovnováhy", "rovnovahou": "rovnováhou", "rovnovazny": "rovnovážny", "rovnovazna": "rovnovážna", "rovnovazne": "rovnovážne",

    # Väzby a štruktúra
    "vazba": "väzba", "vazby": "väzby", "vazbou": "väzbou", "vazieb": "väzieb", "vazbach": "väzbách", "vazbami": "väzbami",
    "kovalentna": "kovalentná", "kovalentny": "kovalentný", "kovalentne": "kovalentné", "kovalentnej": "kovalentnej", "kovalentnych": "kovalentných",
    "ionova": "iónová", "ionovy": "iónový", "ionove": "iónové", "ionovej": "iónovej", "ionovych": "iónových",
    "vodikova": "vodíková", "vodikovy": "vodíkový", "vodikove": "vodíkové", "vodikovej": "vodíkej", "vodikovych": "vodíkových",
    "koordinacna": "koordinačná", "koordinacny": "koordinačný", "koordinacne": "koordinačné",
    "struktura": "štruktúra", "struktury": "štruktúry", "strukturou": "štruktúrou", "struktur": "štruktúr",
    "strukturny": "štruktúrny", "strukturna": "štruktúrna", "strukturne": "štruktúrne", "strukturnych": "štruktúrnych",
    "cislo": "číslo", "cisla": "čísla", "cislom": "číslom", "cisiel": "čísiel",
    "oxidacne": "oxidačné", "oxidacny": "oxidačný", "oxidacna": "oxidačná", "oxidacneho": "oxidačného", "oxidacnom": "oxidačnom",
    "redukcne": "redukčné", "redukcny": "redukčný", "redukcna": "redukčná",
    "redoxny": "redoxný", "redoxna": "redoxná", "redoxne": "redoxné",

    # Prvky a zlúčeniny
    "zlucenina": "zlúčenina", "zluceniny": "zlúčeniny", "zlucenin": "zlúčenín", "zlucenine": "zlúčenine", "zluceninu": "zlúčeninu", "zluceninou": "zlúčeninou", "zluceninach": "zlúčeninách",
    "prvok": "prvok", "prvku": "prvku", "prvky": "prvky", "prvkov": "prvkov", "prvkom": "prvkom",
    "vodik": "vodík", "vodika": "vodíka", "vodikom": "vodíkom",
    "uhlik": "uhlík", "uhlika": "uhlíka", "uhlikom": "uhlíkom",
    "dusik": "dusík", "dusika": "dusíka", "dusikom": "dusíkom",
    "kyslik": "kyslík", "kyslika": "kyslíka", "kyslikom": "kyslíkom",
    "fosfor": "fosfor", "fosforu": "fosforu",
    "sira": "síra", "siry": "síry", "sirou": "sírou",
    "chlor": "chlór", "chloru": "chlóru", "brom": "bróm", "bromu": "brómu", "jod": "jód", "jodu": "jódu", "fluor": "fluór", "fluoru": "fluóru",
    "sodik": "sodík", "sodika": "sodíka", "draslik": "draslík", "draslika": "draslíka",
    "vapnik": "vápnik", "vapnika": "vápnika", "horcik": "horčík", "horcika": "horčíka",
    "hlinik": "hliník", "hlinika": "hliníka", "zelezo": "železo", "zeleza": "železa",
    "med": "meď", "medi": "medi", "medou": "meďou", "zinok": "zinok", "zinku": "zinku",
    "olovo": "olovo", "olova": "olova", "ortut": "ortuť", "ortuti": "ortuti",

    # Kyseliny, zásady, soli
    "kyselina": "kyselina", "kyseliny": "kyseliny", "kyselin": "kyselín", "kyseline": "kyseline", "kyselinu": "kyselinu", "kyselinou": "kyselinou",
    "sirova": "sírová", "sirovej": "sírovej", "sirovu": "sírovú", "sirovy": "sírový", "sirove": "sírové",
    "dusicna": "dusičná", "dusicnej": "dusičnej", "dusicnu": "dusičnú", "dusicny": "dusičný",
    "chlorovodikova": "chlorovodíková", "chlorovodikovej": "chlorovodíkovej",
    "uhlicita": "uhličitá", "uhlicitej": "uhličitej",
    "fosforecna": "fosforečná", "fosforecnej": "fosforečnej",
    "octova": "octová", "octovej": "octovej", "mravcia": "mravčia", "mravcej": "mravcej",
    "zasada": "zásada", "zasady": "zásady", "zasad": "zásad", "zasadou": "zásadou",
    "sol": "soľ", "soli": "soli", "solou": "soľou", "solach": "soliach",
    "hydroxid": "hydroxid", "hydroxidu": "hydroxidu", "hydroxidy": "hydroxidy",
    "oxid": "oxid", "oxidu": "oxidu", "oxidy": "oxidy", "oxidov": "oxidov",
    "chlorid": "chlorid", "chloridu": "chloridu", "chloridy": "chloridy",
    "bromid": "bromid", "jodid": "jodid", "fluorid": "fluorid", "sulfid": "sulfid",
    "siran": "síran", "siranu": "síranu", "sirany": "sírany", "siranov": "síranov",
    "dusicnan": "dusičnan", "dusicnanu": "dusičnanu", "dusicnany": "dusičnany",
    "uhlicitan": "uhličitan", "uhlicitanu": "uhličitanu", "uhlicitany": "uhličitany",
    "fosforecnan": "fosforečnan", "fosforecnanu": "fosforečnanu",

    # Organika & Biochémia
    "uhlovodik": "uhľovodík", "uhlovodiky": "uhľovodíky", "uhlovodikov": "uhľovodíkov", "uhlovodikom": "uhľovodíkom",
    "alkan": "alkán", "alkany": "alkány", "alkanov": "alkánov",
    "alken": "alkén", "alkeny": "alkény", "alkenov": "alkénov",
    "alkin": "alkín", "alkiny": "alkíny", "alkinov": "alkínov",
    "benzen": "benzén", "benzenu": "benzénu", "toluen": "toluén", "naftalen": "naftalén",
    "alkohol": "alkohol", "alkoholy": "alkoholy", "alkoholov": "alkoholov",
    "fenol": "fenol", "fenoly": "fenoly", "etanol": "etanol", "metanol": "metanol", "glycerol": "glycerol",
    "aldehyd": "aldehyd", "aldehydy": "aldehydy", "keton": "ketón", "ketony": "ketóny", "aceton": "acetón",
    "ester": "ester", "estery": "estery", "esterov": "esterov",
    "sacharid": "sacharid", "sacharidy": "sacharidy", "sacharidov": "sacharidov",
    "glukoza": "glukóza", "glukozy": "glukózy", "fruktoza": "fruktóza", "galaktoza": "galaktóza",
    "sacharoza": "sacharóza", "laktoza": "laktóza", "maltoza": "maltóza",
    "skrob": "škrob", "skrobu": "škrobu", "glykogen": "glykogén", "celuloza": "celulóza",
    "lipid": "lipid", "lipidy": "lipidy", "lipidov": "lipidov", "tuky": "tuky", "oleje": "oleje",
    "bielkovina": "bielkovina", "bielkoviny": "bielkoviny", "bielkovin": "bielkovín", "bielkovinami": "bielkovinami",
    "protein": "proteín", "proteiny": "proteíny", "proteinov": "proteínov",
    "aminokyselina": "aminokyselina", "aminokyseliny": "aminokyseliny", "aminokyselin": "aminokyselín",
    "peptid": "peptid", "peptidy": "peptidy", "peptidova": "peptidová", "peptidove": "peptidové", "peptidovy": "peptidový",
    "nukleova": "nukleová", "nukleove": "nukleové", "nukleovych": "nukleových",
    "nukleotid": "nukleotid", "nukleotidy": "nukleotidy", "baza": "báza", "bazy": "bázy",
    "adenin": "adenín", "guanin": "guanín", "cytozin": "cytozín", "tymin": "tymín", "uracil": "uracil",
    "enzym": "enzým", "enzymy": "enzýmy", "enzymov": "enzýmov", "katalyzator": "katalyzátor", "katalyzatory": "katalyzátory",

    # Separácie a bežné slovenské tvary
    "priklad": "príklad", "prikladu": "príkladu", "priklady": "príklady", "prikladom": "príkladom",
    "vlaknina": "vláknina", "vlakniny": "vlákniny", "vlakninou": "vlákninou",
    "dzus": "džús", "dym": "dym", "hmla": "hmla", "smog": "smog",
    "filtracia": "filtrácia", "filtracie": "filtrácie", "filtraciou": "filtráciou",
    "destilacia": "destilácia", "destilacie": "destilácie", "destilaciou": "destiláciou",
    "krystalizacia": "kryštalizácia", "krystalizacie": "kryštalizácie", "krystalizaciou": "kryštalizáciou",
    "sedimentacia": "sedimentácia", "sedimentacie": "sedimentácie", "sedimentaciou": "sedimentáciou",
    "sublimacia": "sublimácia", "extrakcia": "extrakcia", "chromatografia": "chromatografia",
    "oddeluje": "oddeľuje", "oddeluju": "oddeľujú", "oddelovanie": "oddeľovanie", "oddelovania": "oddeľovania",
    "rozdelujeme": "rozdeľujeme", "rozdeluju": "rozdeľujú", "rozdelenie": "rozdelenie",
    "velkost": "veľkosť", "velkosti": "veľkosti", "castic": "častíc", "castice": "častice",
    "podla": "podľa", "poda": "podľa", "vzhlad": "vzhľad", "chut": "chuť", "vonu": "vôňu",
    "ciste": "čisté", "cisty": "čistý", "cista": "čistá", "zriedka": "zriedka", "prirode": "prírode",
    "zaklade": "základe", "zaklad": "základ", "roznej": "rôznej", "roznych": "rôznych", "rozne": "rôzne",
    "spravidla": "spravidla", "vzdy": "vždy", "nikdy": "nikdy", "niekedy": "niekedy", "zavisi": "závisí", "nezavisi": "nezávisí",
    "zavisia": "závisia", "nezavisia": "nezávisia",
}

for k, v in chemical_overrides.items():
    word_map[k] = (v, 10**9)

# 3. Clean up common OCR artifacts
def pre_clean_ocr(text):
    if not text:
        return ""
    s = text
    # Fix apostrophe-based carons
    s = re.sub(r"\bl'", "ľ", s)
    s = re.sub(r"l'\b", "ľ", s)
    s = re.sub(r"l'", "ľ", s)
    s = re.sub(r"t'", "ť", s)
    s = re.sub(r"d'", "ď", s)
    s = re.sub(r"c'", "č", s)
    s = re.sub(r"s'", "š", s)
    s = re.sub(r"z'", "ž", s)
    s = re.sub(r"L'", "Ľ", s)
    s = re.sub(r"T'", "Ť", s)
    s = re.sub(r"D'", "Ď", s)
    s = re.sub(r"C'", "Č", s)
    s = re.sub(r"S'", "Š", s)
    s = re.sub(r"Z'", "Ž", s)
    
    # Specific OCR misread words
    s = re.sub(r"\baeroso!\b", "aerosól", s)
    s = re.sub(r"\boddePovanie\b", "oddeľovanie", s)
    s = re.sub(r"\bseparaenych\b", "separačných", s)
    s = re.sub(r"\bseparaene\b", "separačné", s)
    s = re.sub(r"\bCiste\b", "čisté", s)
    s = re.sub(r"\bCisty\b", "čistý", s)
    s = re.sub(r"\bCista\b", "čistá", s)
    s = re.sub(r"\bpod'a\b", "podľa", s)
    s = re.sub(r"\bvel'kosti\b", "veľkosti", s)
    s = re.sub(r"\bplet'ove\b", "pleťové", s)
    s = re.sub(r"\bvzhl'ad\b", "vzhľad", s)
    return s

def is_formula_or_symbol(tok):
    if re.search(r'\d', tok):
        return True
    if tok in ['pH', 'pOH', 'pK', 'pKa', 'pKb', 'Ka', 'Kb', 'Kw', 'R', 'T', 'V', 'p', 'm', 'M', 'n', 'c']:
        return True
    if tok in ['Na', 'Cl', 'Fe', 'Cu', 'Ag', 'Au', 'Al', 'Mg', 'Ca', 'Ba', 'K', 'N', 'P', 'O', 'S', 'F', 'Br', 'I', 'H', 'C']:
        return True
    return False

def restore_diacritics_string(text):
    if not text:
        return ""
    text = pre_clean_ocr(text)
    tokens = re.split(r'(\b[a-zA-Z0-9áäčďéíĺľňóôŕšťúýžÁÄČĎÉÍĹĽŇÓÔŔŠŤÚÝŽ]+\b)', text)
    res = []
    for tok in tokens:
        if not tok or not re.match(r'^[a-zA-ZáäčďéíĺľňóôŕšťúýžÁÄČĎÉÍĹĽŇÓÔŔŠŤÚÝŽ]+$', tok):
            res.append(tok)
            continue
        if is_formula_or_symbol(tok):
            res.append(tok)
            continue
        key = strip_accents(tok).lower()
        if key in word_map:
            best = word_map[key][0]
            if tok.isupper() and len(tok) > 1:
                res.append(best.upper())
            elif tok.istitle():
                res.append(best.capitalize())
            else:
                res.append(best.lower())
        else:
            res.append(tok)
    return "".join(res)

def process_file(fname):
    print(f"\nProcessing {fname}...")
    with open(fname, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    count = 0
    for q in data:
        q["content"] = restore_diacritics_string(q["content"])
        for opt in q.get("options", []):
            opt["text"] = restore_diacritics_string(opt["text"])
        count += 1
        
    out_name = fname
    with open(out_name, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Updated {count} questions in {fname}.")
    return data

# Process all 3 chemistry files
files = [
    "chemia_otazky_1_300.json",
    "chemia_otazky_301_450.json",
    "chemia_otazky_641_1500.json"
]

all_processed = {}
for f in files:
    all_processed[f] = process_file(f)

# Upload updated questions to Supabase
print("\nUploading updated Chemistry questions with restored diacritics to Supabase...")
SUPABASE_URL = "https://wuklewurydjemuoxuhoq.supabase.co"
API_KEY = "sb_publishable_OHecNnlYu1zLQ1JnbIn9gQ_ebbcnscl"

def get_admin_token():
    auth_url = f"{SUPABASE_URL}/auth/v1/token?grant_type=password"
    headers = {"apikey": API_KEY, "Content-Type": "application/json"}
    payload = json.dumps({
        "email": "david.rusin@student.tuke.sk",
        "password": "Gow79206"
    }).encode("utf-8")
    req = urllib.request.Request(auth_url, data=payload, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))["access_token"]

token = get_admin_token()
auth_headers = {"apikey": API_KEY, "Authorization": f"Bearer {token}"}

# Get subject and categories
req_sub = urllib.request.Request(f"{SUPABASE_URL}/rest/v1/subjects?select=id,name", headers=auth_headers)
with urllib.request.urlopen(req_sub) as r:
    subs = {s["name"]: s["id"] for s in json.loads(r.read().decode("utf-8"))}

chem_id = subs["Chémia"]

req_cat = urllib.request.Request(f"{SUPABASE_URL}/rest/v1/categories?select=id,name&subject_id=eq.{chem_id}", headers=auth_headers)
with urllib.request.urlopen(req_cat) as r:
    cats = {c["name"]: c["id"] for c in json.loads(r.read().decode("utf-8"))}

print("Chemistry categories in Supabase:", cats)

# Delete existing chemistry questions in Supabase
for cat_name, cat_id in cats.items():
    print(f"Clearing old questions for category '{cat_name}'...")
    del_req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/questions?category_id=eq.{cat_id}",
        headers=auth_headers,
        method="DELETE"
    )
    with urllib.request.urlopen(del_req) as _:
        pass

# Insert updated questions
insert_url = f"{SUPABASE_URL}/rest/v1/questions"
insert_headers = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

total_uploaded = 0
for fname, qlist in all_processed.items():
    print(f"Uploading {len(qlist)} questions from {fname}...")
    batch_size = 100
    for i in range(0, len(qlist), batch_size):
        batch = qlist[i:i+batch_size]
        records = [{
            "category_id": cats[q["category"]],
            "content": q["content"],
            "options": q["options"],
            "correct_answers": q["correct_answers"],
            "explanation": q.get("explanation", "")
        } for q in batch]
        payload = json.dumps(records).encode("utf-8")
        req = urllib.request.Request(insert_url, data=payload, headers=insert_headers)
        with urllib.request.urlopen(req) as resp:
            pass
        total_uploaded += len(batch)
        print(f"  Uploaded {total_uploaded} / 1260 questions...")

print(f"\nALL DONE! Successfully restored diacritics and uploaded {total_uploaded} chemistry questions to Supabase!")

