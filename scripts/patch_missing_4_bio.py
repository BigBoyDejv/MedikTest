import json

with open("data/biologia_cloveka_451_900.json", "r", encoding="utf-8") as f:
    items = json.load(f)

with open("data_bio_answers_451_1500.json", "r", encoding="utf-8") as f:
    answers = json.load(f)

missing_data = {
    532: {
        "content": "532. Pri prechode primárneho moču cez stočené kanáliky a Henleho kľučku:",
        "options": [
            {"id": "a", "text": "sa vylučujú do moču niektoré odpadové látky"},
            {"id": "b", "text": "sa spätne vstrebáva časť vody"},
            {"id": "c", "text": "sa spätne vstrebávajú odpadové látky"},
            {"id": "d", "text": "sa spätne vstrebáva časť solí a látok dôležitých pre telo"},
            {"id": "e", "text": "prechádzajú do krvi odpadové látky cez steny kanálikov"},
            {"id": "f", "text": "sa filtruje krv"},
            {"id": "g", "text": "sa filtruje primárny moč"},
            {"id": "h", "text": "sa väčšina látok ako aj vody vstrebáva v stočenom kanáliku II. radu"}
        ]
    },
    533: {
        "content": "533. Ktoré z uvedených látok nemá obsahovať moč zdravého človeka:",
        "options": [
            {"id": "a", "text": "glukózu vo vyššej koncentrácii"},
            {"id": "b", "text": "hnis"},
            {"id": "c", "text": "kreatinín"},
            {"id": "d", "text": "kyselinu močovú"},
            {"id": "e", "text": "erytrocyty"},
            {"id": "f", "text": "leukocyty"},
            {"id": "g", "text": "močovinu"},
            {"id": "h", "text": "NaCl, K+, Na+, Mg2+, Ca2+"}
        ]
    },
    568: {
        "content": "568. Kompletný hrudník človeka tvoria tieto kosti:",
        "options": [
            {"id": "a", "text": "12 hrudníkových stavcov, 7 párov pravých rebier, ktoré sa pripájajú chrupkou alebo väzivom na hrudnú kosť"},
            {"id": "b", "text": "hrudná kosť a rebrá"},
            {"id": "c", "text": "12 hrudníkových stavcov, 14 párov rebier a hrudná kosť"},
            {"id": "d", "text": "hrudníkové stavce, rebrá a hrudná kosť"},
            {"id": "e", "text": "12 hrudníkových stavcov a hrudná kosť"},
            {"id": "f", "text": "12 hrudníkových stavcov, 12 párov rebier a hrudná kosť"},
            {"id": "g", "text": "hrudníkové stavce, rebrá, hrudná kosť a lopatka"},
            {"id": "h", "text": "12 hrudníkových stavcov, 7 párov pravých rebier, 5 párov nepravých rebier a hrudná kosť"}
        ]
    },
    814: {
        "content": "814. Retikulárna formácia mozgu človeka je tvorená:",
        "options": [
            {"id": "a", "text": "rozsiahlym súborom pospájaných nervových buniek roztrúsených v bielej hmote, ktorý prestupuje predĺženou miechou, mostom a stredným mozgom až do medzimozgu"},
            {"id": "b", "text": "nervovými vláknami, ktoré umožňujú prenos vzruchu medzi mozgom a miechou"},
            {"id": "c", "text": "sieťovitou spleťou vlákien siahajúcou od miechy až do medzimozgu"},
            {"id": "d", "text": "len vzostupnými nervovými vláknami"},
            {"id": "e", "text": "nervovými bunkami, ktoré riadia podmienené reflexy"},
            {"id": "f", "text": "dráhami a nervami, ktoré inervujú okohybné svaly"},
            {"id": "g", "text": "descendentnými a ascendentnými dráhami"},
            {"id": "h", "text": "len nervovými vláknami"}
        ]
    },
    859: {
        "content": "859. Prúdením endolymfy v polkruhovitých chodbičkách vnútorného ucha človeka:",
        "options": [
            {"id": "a", "text": "sú dráždené zmyslové bunky, ktorých vlásky vyčnievajú do statického receptora"},
            {"id": "b", "text": "je dráždený kinetický receptor"},
            {"id": "c", "text": "je rozkmitávaná Cortiho platňa"},
            {"id": "d", "text": "je rozkmitávaný bubienok"},
            {"id": "e", "text": "je dráždený guľovitý vačok, v ktorom sú nahromadené zmyslové bunky"},
            {"id": "f", "text": "je dráždený kinetický a statický receptor"},
            {"id": "g", "text": "je dráždený spánkový lalok mozgovej kôry"},
            {"id": "h", "text": "sú dráždené zmyslové bunky kinetického receptora, ktorých vlásky vyčnievajú do dráhy endolymfy"}
        ]
    }
}

for num, d in missing_data.items():
    idx = num - 451
    correct = answers.get(str(num), [])
    exp = f"Správne možnosti podľa oficiálneho kľúča LF UPJŠ: {', '.join([c.upper() for c in correct])}."
    items[idx] = {
        "subject": "Biológia",
        "category": "Biológia človeka",
        "content": d["content"],
        "options": d["options"],
        "correct_answers": correct,
        "explanation": exp
    }

with open("data/biologia_cloveka_451_900.json", "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

placeholders = sum(1 for it in items if "Otázka č." in it["content"])
print(f"Patched Biológia človeka! Placeholders remaining: {placeholders}/450")

