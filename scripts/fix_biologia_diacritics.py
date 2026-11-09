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

# 2. Comprehensive Biology dictionary overrides
bio_overrides = {
    # Otázkové frázy a pokyny
    "priradte": "priraďte", "prirad": "priraď", "vyberte": "vyberte", "oznacte": "označte",
    "spravne": "správne", "spravny": "správny", "spravna": "správna", "spravnu": "správnu",
    "spravnym": "správnym", "spravnych": "správnych", "spravnymi": "správnymi", "spravnej": "správnej",
    "nespravne": "nesprávne", "nespravny": "nesprávny", "nespravna": "nesprávna", "nespravnu": "nesprávnu",
    "nespravnym": "nesprávnym", "nespravnych": "nesprávnych", "nespravnymi": "nesprávnymi", "nespravnej": "nesprávnej",
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
    "pocas": "počas", "su": "sú", "nie su": "nie sú", "su to": "sú to", "podla": "podľa",

    # Bunka a cytológia
    "cytologia": "cytológia", "cytologie": "cytológie", "cytologii": "cytológii", "cytologiu": "cytológiu",
    "bunka": "bunka", "bunky": "bunky", "bunke": "bunke", "bunku": "bunku", "bunkou": "bunkou",
    "buniek": "buniek", "bunkam": "bunkám", "bunkach": "bunkách", "bunkami": "bunkami",
    "bunkovy": "bunkový", "bunkova": "bunková", "bunkove": "bunkové", "bunkoveho": "bunkového",
    "bunkovej": "bunkovej", "bunkovych": "bunkových", "bunkovym": "bunkovým", "bunkovymi": "bunkovými",
    "prokaryoticka": "prokaryotická", "prokaryoticky": "prokaryotický", "prokaryoticke": "prokaryotické",
    "prokaryotickej": "prokaryotickej", "prokaryotickych": "prokaryotických", "prokaryotickym": "prokaryotickým",
    "eukaryoticka": "eukaryotická", "eukaryoticky": "eukaryotický", "eukaryoticke": "eukaryotické",
    "eukaryotickej": "eukaryotickej", "eukaryotickych": "eukaryotických", "eukaryotickym": "eukaryotickým",
    "membrana": "membrána", "membrany": "membrány", "membrane": "membráne", "membranu": "membránu",
    "membranou": "membránou", "membran": "membrán", "membranam": "membránam", "membranach": "membránach", "membranami": "membránami",
    "membranovy": "membránový", "membranova": "membránová", "membranove": "membránové", "membranovych": "membránových",
    "biomembrana": "biomembrána", "biomembrany": "biomembrány", "biomembranu": "biomembránu", "biomembran": "biomembrán",
    "plazmalema": "plazmaléma", "plazmalemy": "plazmalémy", "karyolema": "karyoléma", "karyolemy": "karyolémy",
    "jadro": "jadro", "jadra": "jadra", "jadru": "jadru", "jadrom": "jadrom", "jadier": "jadier", "jadre": "jadre",
    "jadierko": "jadierko", "jadierka": "jadierka", "jadierok": "jadierok", "jadierkom": "jadierkom",
    "nukleoid": "nukleoid", "nukleolus": "nukleolus", "nukleoly": "nukleoly",
    "ribozom": "ribozóm", "ribozomy": "ribozómy", "ribozomov": "ribozómov", "ribozomoch": "ribozómoch", "ribozomami": "ribozómami",
    "mitochondria": "mitochondria", "mitochondrie": "mitochondrie", "mitochondrii": "mitochondrií", "mitochondriam": "mitochondriám",
    "mitochondriach": "mitochondriách", "mitochondriami": "mitochondriami",
    "chloroplast": "chloroplast", "chloroplasty": "chloroplasty", "chloroplastov": "chloroplastov", "chloroplastoch": "chloroplastoch",
    "tylakoid": "tylakoid", "tylakoidy": "tylakoidy", "tylakoidov": "tylakoidov", "tylakoidoch": "tylakoidoch",
    "plastid": "plastid", "plastidy": "plastidy", "plastidov": "plastidov", "plastidoch": "plastidoch",
    "chromoplast": "chromoplast", "chromoplasty": "chromoplasty", "leukoplast": "leukoplast", "leukoplasty": "leukoplasty",
    "diktyozom": "diktyozóm", "diktyozomy": "diktyozómy", "diktyozomov": "diktyozómov",
    "lyzozom": "lyzozóm", "lyzozomy": "lyzozómy", "lyzozomov": "lyzozómov",
    "vakuola": "vakuola", "vakuoly": "vakuoly", "vakuolou": "vakuolou", "vakuol": "vakuol", "vakuolach": "vakuolách",
    "centriol": "centriol", "centrioly": "centrioly", "centrozom": "centrozóm",
    "cytoplazma": "cytoplazma", "cytoplazmy": "cytoplazmy", "cytoplazme": "cytoplazme", "cytoplazmu": "cytoplazmu", "cytoplazmou": "cytoplazmou",
    "cytoskelet": "cytoskelet", "mikrotubuly": "mikrotubuly", "mikrofilamenty": "mikrofilamenty",
    "pelikula": "pelikula", "pelikuly": "pelikuly", "kutikula": "kutikula", "kutikuly": "kutikuly",

    # Delenie bunky a genetika
    "mitoza": "mitóza", "mitozy": "mitózy", "mitoze": "mitóze", "mitozu": "mitózu", "mitozou": "mitózou",
    "meioza": "meióza", "meiozy": "meiózy", "meioze": "meióze", "meiozu": "meiózu", "meiozou": "meiózou",
    "amitoza": "amitóza", "interfaza": "interfáza", "interfazy": "interfázy", "interfaze": "interfáze",
    "profaza": "profáza", "profazy": "profázy", "profaze": "profáze",
    "metafaza": "metafáza", "metafazy": "metafázy", "metafaze": "metafáze",
    "anafaza": "anafáza", "anafazy": "anafázy", "anafaze": "anafáze",
    "telofaza": "telofáza", "telofazy": "telofázy", "telofaze": "telofáze",
    "karyokineza": "karyokinéza", "cytokineza": "cytokinéza",
    "chromozom": "chromozóm", "chromozomy": "chromozómy", "chromozomov": "chromozómov", "chromozomoch": "chromozómoch", "chromozomami": "chromozómami",
    "chromatida": "chromatída", "chromatidy": "chromatídy", "chromatid": "chromatíd", "chromatidami": "chromatídami",
    "centromera": "centroméra", "centromery": "centroméry", "centromere": "centromére",
    "homologicky": "homologický", "homologicka": "homologická", "homologicke": "homologické", "homologickych": "homologických",
    "alela": "alela", "alely": "alely", "alel": "alel", "alelami": "alelami",
    "gen": "gén", "geny": "gény", "genov": "génov", "genom": "genóm",
    "geneticky": "genetický", "geneticka": "genetická", "geneticke": "genetické", "geneticku": "genetickú", "genetickych": "genetických",

    # Chemické zloženie a biochémia
    "bielkovina": "bielkovina", "bielkoviny": "bielkoviny", "bielkovinu": "bielkovinu", "bielkovin": "bielkovín", "bielkovinami": "bielkovinami",
    "bielkovinovy": "bielkovinový", "bielkovinova": "bielkovinová", "bielkovinove": "bielkovinové", "bielkovinoveho": "bielkovinového", "bielkovinovych": "bielkovinových",
    "aminokyselina": "aminokyselina", "aminokyseliny": "aminokyseliny", "aminokyselin": "aminokyselín", "aminokyselinami": "aminokyselinami",
    "peptid": "peptid", "peptidy": "peptidy", "peptidov": "peptidov", "peptidovy": "peptidový", "peptidova": "peptidová", "peptidove": "peptidové",
    "nukleova": "nukleová", "nukleove": "nukleové", "nukleovych": "nukleových", "nukleotidy": "nukleotidy", "nukleotidov": "nukleotidov",
    "fosfolipid": "fosfolipid", "fosfolipidy": "fosfolipidy", "fosfolipidov": "fosfolipidov", "lipid": "lipid", "lipidy": "lipidy", "lipidov": "lipidov",
    "sacharid": "sacharid", "sacharidy": "sacharidy", "sacharidov": "sacharidov", "monosacharid": "monosacharid", "monosacharidy": "monosacharidy",
    "glukoza": "glukóza", "glukozy": "glukózy", "glukozu": "glukózu", "riboza": "ribóza", "ribozy": "ribózy", "deoxyriboza": "deoxyribóza",
    "enzym": "enzým", "enzymy": "enzýmy", "enzymov": "enzýmov", "enzymaticky": "enzymatický", "enzymaticka": "enzymatická", "enzymaticke": "enzymatické",
    "vitamin": "vitamín", "vitaminy": "vitamíny", "vitaminov": "vitamínov",
    "hormon": "hormón", "hormony": "hormóny", "hormonov": "hormónov",

    # Fyziológia a metabolizmus
    "fotosynteza": "fotosyntéza", "fotosyntezy": "fotosyntézy", "fotosynteze": "fotosyntéze", "fotosyntezu": "fotosyntézu", "fotosyntezou": "fotosyntézou",
    "fotosynteticky": "fotosyntetický", "fotosynteticka": "fotosyntetická", "fotosynteticke": "fotosyntetické",
    "fotolyza": "fotolýza", "fotolyzy": "fotolýzy", "glykolyza": "glykolýza", "glykolyzy": "glykolýzy",
    "dychanie": "dýchanie", "dychania": "dýchania", "dychanim": "dýchanim", "dychaci": "dýchací", "dychacie": "dýchacie", "dychacich": "dýchacích",
    "kvasenie": "kvasenie", "kvasenia": "kvasenia", "fermentacia": "fermentácia",
    "asimilacia": "asimilácia", "disimilacia": "disimilácia", "asimilatov": "asimilátov",
    "asimilacny": "asimilačný", "asimilacna": "asimilačná", "asimilacne": "asimilačné", "asimilacnych": "asimilačných",
    "anabolicky": "anabolický", "anabolicka": "anabolická", "anabolicke": "anabolické",
    "katabolicky": "katabolický", "katabolicka": "katabolická", "katabolicke": "katabolické",
    "endergonicky": "endergonický", "endergonicke": "endergonické", "exergonicky": "exergonický", "exergonicke": "exergonické",
    "difuzia": "difúzia", "difuzie": "difúzie", "osmoza": "osmóza", "osmozy": "osmózy",
    "osmoticky": "osmotický", "osmoticka": "osmotická", "osmoticke": "osmotické",
    "plazmolyza": "plazmolýza", "deplazmolyza": "deplazmolýza", "turgor": "turgor",
    "pinocytoza": "pinocytóza", "fagocytoza": "fagocytóza", "fagocytozy": "fagocytózy",
    "endocytoza": "endocytóza", "exocytoza": "exocytóza",

    # Rastliny a pletivá
    "pletivo": "pletivo", "pletiva": "pletivá", "pletiv": "pletív", "pletivach": "pletivách", "pletivami": "pletivami",
    "parenchym": "parenchým", "kolenchym": "kolenchým", "sklerenchym": "sklerenchým", "prozenchym": "prozenchým",
    "meristem": "meristém", "meristemy": "meristémy", "meristematicky": "meristematický", "meristematicka": "meristematická", "meristematicke": "meristematické",
    "koren": "koreň", "korene": "korene", "korena": "koreňa", "korenov": "koreňov", "korenovy": "koreňový", "korenova": "koreňová", "korenove": "koreňové",
    "stonka": "stonka", "stonky": "stonky", "stonke": "stonke", "stonku": "stonku", "stonkou": "stonkou",
    "list": "list", "listy": "listy", "listov": "listov", "listoch": "listoch", "listami": "listami",
    "kvet": "kvet", "kvety": "kvety", "kvetov": "kvetov", "plod": "plod", "plody": "plody", "plodov": "plodov",
    "semeno": "semeno", "semena": "semená", "semien": "semien",
    "cieva": "cieva", "cievy": "cievy", "ciev": "ciev", "cievami": "cievami", "cievny": "cievny", "cievna": "cievna", "cievne": "cievne", "cievnych": "cievnych",
    "prieduch": "prieduch", "prieduchy": "prieduchy", "prieduchov": "prieduchov", "prieduchoch": "prieduchoch",
    "gutacia": "gutácia", "gutacie": "gutácie", "transpiracia": "transpirácia", "transpiracie": "transpirácie",
    "autotrofny": "autotrofný", "autotrofna": "autotrofná", "autotrofne": "autotrofné", "autotrofnych": "autotrofných",
    "heterotrofny": "heterotrofný", "heterotrofna": "heterotrofná", "heterotrofne": "heterotrofné", "heterotrofnych": "heterotrofných",
    "mixotrofia": "mixotrofia", "parazitizmus": "parazitizmus", "mykoriza": "mykoríza", "mykorizy": "mykorízy", "symbioza": "symbióza",

    # Živočíchy, tkanivá a sústavy
    "zivocich": "živočích", "zivocichy": "živočíchy", "zivocichov": "živočíchov", "zivocichom": "živočíchom", "zivocichoch": "živočíchoch", "zivocichmi": "živočíchmi",
    "zivocisny": "živočíšny", "zivocisna": "živočíšna", "zivocisne": "živočíšne", "zivocisneho": "živočíšneho", "zivocisnej": "živočíšnej", "zivocisnych": "živočíšnych",
    "tkanivo": "tkanivo", "tkaniva": "tkanivá", "tkaniv": "tkanív", "tkanivach": "tkanivách", "tkanivami": "tkanivami",
    "epitel": "epitel", "epitely": "epitely", "epitelove": "epitelové", "epitelovych": "epitelových",
    "spojivo": "spojivo", "spojiva": "spojivá", "spojivove": "spojivové", "spojivovych": "spojivových",
    "sval": "sval", "svaly": "svaly", "svalov": "svalov", "svalovy": "svalový", "svalova": "svalová", "svalove": "svalové", "svalovych": "svalových",
    "nerv": "nerv", "nervy": "nervy", "nervov": "nervov", "nervovy": "nervový", "nervova": "nervová", "nervove": "nervové", "nervoveho": "nervového", "nervovej": "nervovej", "nervovych": "nervových",
    "miecha": "miecha", "miechy": "miechy", "mieche": "mieche", "miechu": "miechu",
    "mozog": "mozog", "mozgu": "mozgu", "mozgom": "mozgom", "mozgova": "mozgová", "mozgove": "mozgové", "mozgovej": "mozgovej", "mozgovych": "mozgových",
    "mozocek": "mozoček", "mozocku": "mozočku",
    "kora": "kôra", "kory": "kôry", "kore": "kôre", "koru": "kôru", "korove": "korové", "korovych": "korových",
    "srdce": "srdce", "srdca": "srdca", "srdcu": "srdcu", "srdcom": "srdcom", "srdcovy": "srdcový", "srdcova": "srdcová", "srdcove": "srdcové",
    "krv": "krv", "krvi": "krvi", "krvou": "krvou", "krvny": "krvný", "krvna": "krvná", "krvne": "krvné", "krvneho": "krvného", "krvnej": "krvnej", "krvnych": "krvných",
    "erytrocyt": "erytrocyt", "erytrocyty": "erytrocyty", "erytrocytov": "erytrocytov",
    "leukocyt": "leukocyt", "leukocyty": "leukocyty", "leukocytov": "leukocytov",
    "trombocyt": "trombocyt", "trombocyty": "trombocyty", "trombocytov": "trombocytov",
    "hemoglobin": "hemoglobín", "hemoglobinu": "hemoglobínu",
    "imunita": "imunita", "imunity": "imunity", "imunite": "imunite", "imunitu": "imunitu", "imunitou": "imunitou", "imunitny": "imunitný", "imunitna": "imunitná", "imunitne": "imunitné",
    "protilatka": "protilátka", "protilatky": "protilátky", "protilatok": "protilátok", "protilatkami": "protilátkami",
    "antigen": "antigén", "antigeny": "antigény", "antigenov": "antigénov",
    "pluca": "pľúca", "pluc": "pľúc", "plucach": "pľúcach", "plucami": "pľúcami", "plucny": "pľúcny", "plucna": "pľúcna", "plucne": "pľúcne", "plucnych": "pľúcnych",
    "ziabre": "žiabre", "ziabier": "žiabier", "ziabrami": "žiabrami",
    "vzdusnice": "vzdušnice", "vzdusnic": "vzdušníc", "vzdusnicami": "vzdušnicami",
    "zaludok": "žalúdok", "zaludka": "žalúdka", "zaludku": "žalúdku", "zaludkom": "žalúdkom",
    "crevo": "črevo", "creva": "čreva", "crevu": "črevu", "crevom": "črevom", "criev": "čriev", "crevny": "črevný", "crevna": "črevná", "crevne": "črevné",
    "pecen": "pečeň", "pecene": "pečene", "peceni": "pečeni", "pecenou": "pečeňou",
    "oblicka": "oblička", "oblicky": "obličky", "obliciek": "obličiek", "oblickach": "obličkách", "oblickami": "obličkami",
    "moc": "moč", "mocu": "moču", "mocom": "močom", "mocovy": "močový", "mocova": "močová", "mocove": "močové", "mocovina": "močovina", "mocoviny": "močoviny",
    "receptory": "receptory", "receptorov": "receptorov", "receptoroch": "receptoroch", "receptor": "receptor",
    "chemoreceptor": "chemoreceptor", "chemoreceptory": "chemoreceptory", "chemoreceptorov": "chemoreceptorov",
    "mechanoreceptor": "mechanoreceptor", "mechanoreceptory": "mechanoreceptory",
    "proprioreceptor": "proprioreceptor", "proprioreceptory": "proprioreceptory",
    "fotoreceptor": "fotoreceptor", "fotoreceptory": "fotoreceptory",
    "termoreceptor": "termoreceptor", "termoreceptory": "termoreceptory",
    "bylinozravce": "bylinožravce", "bylinozravcov": "bylinožravcov", "bylinozravy": "bylinožravý", "bylinozrave": "bylinožravé", "bylinozravych": "bylinožravých",
    "masozravce": "mäsožravce", "masozravcov": "mäsožravcov", "masozravy": "mäsožravý", "masozrave": "mäsožravé", "masozravych": "mäsožravých",
    "vsezravce": "všežravce", "vsezravcov": "všežravcov", "vsezravy": "všežravý", "vsezrave": "všežravé", "vsezravych": "všežravých",
    "stavovce": "stavovce", "stavovcov": "stavovcov", "stavovcom": "stavovcom", "bezstavovce": "bezstavovce", "bezstavovcov": "bezstavovcov",
    "obruckavce": "obrúčkavce", "obruckavcov": "obrúčkavcov", "clankonozce": "článkonožce", "clankonozcov": "článkonožcov",
    "hmyz": "hmyz", "hmyzu": "hmyzu", "vtaky": "vtáky", "vtakov": "vtákov", "cicavce": "cicavce", "cicavcov": "cicavcov",
    "ryby": "ryby", "ryb": "rýb", "plazy": "plazy", "plazov": "plazov", "obojzivelniky": "obojživelníky", "obojzivelnikov": "obojživelníkov"
}

# Update word_map with bio_overrides
for k, v in bio_overrides.items():
    norm_key = strip_accents(k).lower()
    word_map[norm_key] = (v, 9999999)

def pre_clean_ocr(text):
    s = text
    # Fix broken quotes & apostrophes used for palatalization
    s = re.sub(r"t'", "ť", s)
    s = re.sub(r"d'", "ď", s)
    s = re.sub(r"l'", "ľ", s)
    s = re.sub(r"T'", "Ť", s)
    s = re.sub(r"D'", "Ď", s)
    s = re.sub(r"L'", "Ľ", s)
    s = re.sub(r"c'", "č", s)
    s = re.sub(r"s'", "š", s)
    s = re.sub(r"z'", "ž", s)
    s = re.sub(r"C'", "Č", s)
    s = re.sub(r"S'", "Š", s)
    s = re.sub(r"Z'", "Ž", s)
    
    # Specific OCR misread words
    s = re.sub(r"\bvnuitorny\b", "vnútorný", s)
    s = re.sub(r"\bvnuitorna\b", "vnútorná", s)
    s = re.sub(r"\bvnuitorne\b", "vnútorné", s)
    s = re.sub(r"\bvnuitorneho\b", "vnútorného", s)
    s = re.sub(r"\brozeleneny\b", "rozčlenený", s)
    s = re.sub(r"\brozelenena\b", "rozčlenená", s)
    s = re.sub(r"\brozelenene\b", "rozčlenené", s)
    s = re.sub(r"\bfunkene\b", "funkčné", s)
    s = re.sub(r"\bfunkena\b", "funkčná", s)
    s = re.sub(r"\bfunkeny\b", "funkčný", s)
    s = re.sub(r"\bfunkenu\b", "funkčnú", s)
    s = re.sub(r"\bfunkenych\b", "funkčných", s)
    s = re.sub(r"\birovni\b", "úrovni", s)
    s = re.sub(r"\biroven\b", "úroveň", s)
    s = re.sub(r"\bstistava\b", "sústava", s)
    s = re.sub(r"\bstistavy\b", "sústavy", s)
    s = re.sub(r"\bstistave\b", "sústave", s)
    s = re.sub(r"\bstistavu\b", "sústavu", s)
    s = re.sub(r"\bstistavou\b", "sústavou", s)
    s = re.sub(r"\bstistav\b", "sústav", s)
    s = re.sub(r"\bstistavam\b", "sústavám", s)
    s = re.sub(r"\bstistavach\b", "sústavách", s)
    s = re.sub(r"\bstistavami\b", "sústavami", s)
    s = re.sub(r"\bst\b", "sú", s) # OCR misread 'sú' as 'st'
    s = re.sub(r"\bsui\b", "sú", s)
    s = re.sub(r"\bpod'a\b", "podľa", s)
    s = re.sub(r"\bvel'kosti\b", "veľkosti", s)
    s = re.sub(r"\bvel'ky\b", "veľký", s)
    s = re.sub(r"\bvel'ka\b", "veľká", s)
    s = re.sub(r"\bvel'ke\b", "veľké", s)
    s = re.sub(r"\bvel'kych\b", "veľkých", s)
    s = re.sub(r"\bštruktiry\b", "štruktúry", s)
    s = re.sub(r"\bstruktiry\b", "štruktúry", s)
    s = re.sub(r"\bštruktira\b", "štruktúra", s)
    s = re.sub(r"\bstruktira\b", "štruktúra", s)
    s = re.sub(r"\bštruktire\b", "štruktúre", s)
    s = re.sub(r"\bštruktiru\b", "štruktúru", s)
    s = re.sub(r"\buvol'rovanim\b", "uvoľňovaním", s)
    s = re.sub(r"\buvol'novanim\b", "uvoľňovaním", s)
    s = re.sub(r"\buvol'rovani\b", "uvoľňovaní", s)
    s = re.sub(r"\buvol'novani\b", "uvoľňovaní", s)
    s = re.sub(r"\buvol'nuje\b", "uvoľňuje", s)
    s = re.sub(r"\buvol'nuju\b", "uvoľňujú", s)
    s = re.sub(r"\bmolekul'arny\b", "molekulárny", s)
    s = re.sub(r"\bmolekul'arna\b", "molekulárna", s)
    s = re.sub(r"\bmolekul'arne\b", "molekulárne", s)
    s = re.sub(r"\bmolekul'arnych\b", "molekulárnych", s)
    return s

def is_preserved_token(tok):
    # Biological / chemical / cell cycle codes
    if tok in ['DNA', 'RNA', 'mRNA', 'tRNA', 'rRNA', 'ATP', 'ADP', 'AMP', 'G1', 'G2', 'S', 'M']:
        return True
    if tok in ['pH', 'pOH', 'CO2', 'O2', 'H2O', 'N2', 'Ca2+', 'Mg2+', 'Fe2+', 'Fe3+', 'Na+', 'K+', 'Cl-']:
        return True
    if re.search(r'\d', tok):
        return True
    return False

def restore_diacritics_string(text):
    if not text:
        return ""
    text = pre_clean_ocr(text)
    tokens = re.split(r'(\b[a-zA-Z0-9áäčďéíĺľňóôŕšťúýžÁÄČĎÉÍĹĽŇÓÔŔŠŤÚÝŽ\+\-]+\b)', text)
    res = []
    for tok in tokens:
        if not tok or not re.match(r'^[a-zA-ZáäčďéíĺľňóôŕšťúýžÁÄČĎÉÍĹĽŇÓÔŔŠŤÚÝŽ\+\-]+$', tok):
            res.append(tok)
            continue
        if is_preserved_token(tok):
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

# 3. Load repaired questions
with open("temp_bio_repaired_questions.json", "r", encoding="utf-8") as f:
    raw_qs = json.load(f)

# 4. Load verified answer keys
with open("data_bio_answers_1_450.json", "r", encoding="utf-8") as f:
    ans_keys = {int(k): v for k, v in json.load(f).items()}

final_questions = []

for i in range(1, 451):
    q_data = raw_qs[str(i)]
    q_content = restore_diacritics_string(q_data["content"])
    # Ensure starts with "i. "
    q_content = re.sub(r'^\d+[\.\,\:\)]?\s*', f'{i}. ', q_content)

    opts = []
    for opt_char in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
        raw_opt_text = q_data["options"].get(opt_char, "")
        clean_opt_text = restore_diacritics_string(raw_opt_text)
        opts.append({
            "id": opt_char,
            "text": clean_opt_text
        })

    correct = ans_keys[i]
    correct_upper = ", ".join([c.upper() for c in sorted(correct)])
    explanation = f"Správne odpovede podľa oficiálneho kľúča testovnice UPJŠ LF sú: {correct_upper}."

    final_questions.append({
        "subject": "Biológia",
        "category": "Biológia bunky, rastlín a živočíchov",
        "content": q_content,
        "options": opts,
        "correct_answers": correct,
        "explanation": explanation
    })

print(f"\nSuccessfully processed {len(final_questions)} questions with restored diacritics.")

# Save to biologia_otazky_1_450.json
with open("biologia_otazky_1_450.json", "w", encoding="utf-8") as f:
    json.dump(final_questions, f, ensure_ascii=False, indent=2)

print("Saved biologia_otazky_1_450.json.")

# Print sample questions
print("\nSample Question 1:")
print(json.dumps(final_questions[0], indent=2, ensure_ascii=False))

print("\nSample Question 11:")
print(json.dumps(final_questions[10], indent=2, ensure_ascii=False))

print("\nSample Question 152:")
print(json.dumps(final_questions[151], indent=2, ensure_ascii=False))
