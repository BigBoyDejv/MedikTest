import json

with open("data/genetika_901_1250.json", "r", encoding="utf-8") as f:
    items = json.load(f)

with open("data_bio_answers_451_1500.json", "r", encoding="utf-8") as f:
    answers = json.load(f)

missing_genetika = {
    1078: {
        "content": "1078. U dvojnásobných heterozygotov (AaBb) pri väzbe génov v polohe trans:",
        "options": [
            {"id": "a", "text": "nemôžu vzniknúť gaméty s kombináciou Ab a aB za predpokladu úplnej väzby"},
            {"id": "b", "text": "sa najčastejšie tvoria gaméty AABB, aabb"},
            {"id": "c", "text": "sa tvoria rovnakí rekombinanti ako pri väzbe génov v polohe cis"},
            {"id": "d", "text": "sa častejšie tvoria gaméty rekombinované ako gaméty s rodičovskou zostavou génov"},
            {"id": "e", "text": "sa častejšie tvoria gaméty s rodičovskou zostavou génov ako gaméty rekombinované"},
            {"id": "f", "text": "sa častejšie tvoria gaméty Ab a aB ako gaméty AB a ab"},
            {"id": "g", "text": "sú dominantné alely dvoch sledovaných génov na jednom chromozóme a recesívne na druhom párovom chromozóme"},
            {"id": "h", "text": "vznikajú gaméty AB a ab len v dôsledku crossing-overu"}
        ]
    },
    1083: {
        "content": "1083. Koľko rôznych fenotypov bude vytvárať potomstvo parentálnej generácie AABB x aabb v F2 generácii, ak sú gény A a B v úplnej väzbe (za predpokladu úplnej dominancie):",
        "options": [
            {"id": "a", "text": "1"},
            {"id": "b", "text": "2"},
            {"id": "c", "text": "4"},
            {"id": "d", "text": "2^2"},
            {"id": "e", "text": "8"},
            {"id": "f", "text": "3"},
            {"id": "g", "text": "6"},
            {"id": "h", "text": "3^2"}
        ]
    },
    1108: {
        "content": "1108. Označte správnu odpoveď:",
        "options": [
            {"id": "a", "text": "pri chromozómovom určení pohlavia typu drozofila je samičie pohlavie heterogametné XY"},
            {"id": "b", "text": "pri chromozómovom určení pohlavia typu drozofila je samičie pohlavie homogametné XX"},
            {"id": "c", "text": "pri chromozómovom určení pohlavia typu drozofila je samičie pohlavie heterogametné XX"},
            {"id": "d", "text": "pri chromozómovom určení pohlavia typu drozofila je samičie pohlavie homogametné XY"},
            {"id": "e", "text": "pri chromozómovom určení pohlavia typu abraxas je samičie pohlavie homogametné XX"},
            {"id": "f", "text": "pri chromozómovom určení pohlavia typu abraxas je samičie pohlavie heterogametné XY"},
            {"id": "g", "text": "pri chromozómovom určení pohlavia typu abraxas je samičie pohlavie homogametné XY"},
            {"id": "h", "text": "pri chromozómovom určení pohlavia typu abraxas je samičie pohlavie heterogametné XX"}
        ]
    },
    1111: {
        "content": "1111. Vyberte správne tvrdenie:",
        "options": [
            {"id": "a", "text": "pri dedičnosti viazanej na X chromozóm sú gény lokalizované v homologickom úseku X chromozómu"},
            {"id": "b", "text": "pri dedičnosti viazanej na X chromozóm sú gény lokalizované v nehomologickom úseku X chromozómu"},
            {"id": "c", "text": "pri holandrickom type dedičnosti sú gény lokalizované na homologickom úseku Y chromozómu"},
            {"id": "d", "text": "pri holandrickom type dedičnosti sú gény lokalizované na nehomologickom úseku Y chromozómu"},
            {"id": "e", "text": "chromozómy X a Y nemajú navzájom homologické úseky"},
            {"id": "f", "text": "chromozómy X a Y majú navzájom homologické úseky"},
            {"id": "g", "text": "pri dedičnosti neúplne viazanej na pohlavie sú gény lokalizované v homologickom úseku X a Y chromozómu"},
            {"id": "h", "text": "pri dedičnosti neúplne viazanej na pohlavie sú gény lokalizované v nehomologickom úseku X a Y chromozómu"}
        ]
    },
    1183: {
        "content": "1183. V malej populácii vplyvom génového posunu sa môže po určitom počte generácií:",
        "options": [
            {"id": "a", "text": "meniť genofond populácie v zmysle vymiznutia niektorých alel a zvýšenia frekvencie iných"},
            {"id": "b", "text": "genofond stať variabilný, frekvencia všetkých alel stúpa a pribúda homozygotov v dôsledku panmixie"},
            {"id": "c", "text": "genofond stať variabilný, pričom stúpa počet heterozygotov"},
            {"id": "d", "text": "meniť genofond populácie v zmysle vymiznutia niektorých alel pri zvýšení počtu heterozygotov"},
            {"id": "e", "text": "niektorá alela fixovať"},
            {"id": "f", "text": "znížiť počet homozygotov"},
            {"id": "g", "text": "zvýšiť počet heterozygotov"},
            {"id": "h", "text": "ustáliť genetická rovnováha"}
        ]
    },
    1211: {
        "content": "1211. Zmeny genofondu môžu byť spôsobené:",
        "options": [
            {"id": "a", "text": "vplyvom faktorov vonkajšieho prostredia"},
            {"id": "b", "text": "mutáciami"},
            {"id": "c", "text": "selekciou"},
            {"id": "d", "text": "panmixiou"},
            {"id": "e", "text": "inbrídingom"},
            {"id": "f", "text": "somatickými mutáciami"},
            {"id": "g", "text": "genetickou izoláciou"},
            {"id": "h", "text": "autogamiou"}
        ]
    },
    1221: {
        "content": "1221. Dedičná hemofília sa vyskytuje:",
        "options": [
            {"id": "a", "text": "nezávisle od výskytu krvnej skupiny A"},
            {"id": "b", "text": "u žien, ktorých otec bol zdravý"},
            {"id": "c", "text": "často v potomstve zdravých žien, ktorých otec mal hemofíliu"},
            {"id": "d", "text": "u mužov, ktorých otec bol tiež postihnutý"},
            {"id": "e", "text": "prevažne u mužov"},
            {"id": "f", "text": "rovnako často u oboch pohlaví"},
            {"id": "g", "text": "prevažne u žien"},
            {"id": "h", "text": "u žien, ktorých obaja rodičia boli zdraví"}
        ]
    },
    1250: {
        "content": "1250. Génové inžinierstvo sa zaoberá:",
        "options": [
            {"id": "a", "text": "identifikáciou osôb"},
            {"id": "b", "text": "analýzou karyotypov"},
            {"id": "c", "text": "šľachtením zvierat a rastlín"},
            {"id": "d", "text": "tvorbou hybridných molekúl DNA a ich klonovaním"},
            {"id": "e", "text": "technológiou vytvárania rekombinantných molekúl DNA"},
            {"id": "f", "text": "štiepením izolovaných molekúl DNA na krátke úseky pomocou restrikčných endonukleáz"},
            {"id": "g", "text": "génovými manipuláciami"},
            {"id": "h", "text": "vnášaním cudzorodej DNA do hostiteľskej bunky pomocou vektorov"}
        ]
    }
}

for num, d in missing_genetika.items():
    idx = num - 901
    correct = answers.get(str(num), [])
    exp = f"Správne možnosti podľa oficiálneho kľúča LF UPJŠ: {', '.join([c.upper() for c in correct])}."
    items[idx] = {
        "subject": "Biológia",
        "category": "Genetika",
        "content": d["content"],
        "options": d["options"],
        "correct_answers": correct,
        "explanation": exp
    }

with open("data/genetika_901_1250.json", "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

placeholders = sum(1 for it in items if "Otázka č." in it["content"])
print(f"Patched Genetika! Placeholders remaining: {placeholders}/350")

