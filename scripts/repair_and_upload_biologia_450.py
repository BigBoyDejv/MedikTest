import json
import re
import urllib.request
import urllib.parse

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

def clean_typos(text: str) -> str:
    if not text:
        return ""
    
    # Specific OCR error replacements
    replacements = [
        (r'\b21\b:', 'Žlč:'),
        (r'\bObjaviteP\b', 'Objaviteľ'),
        (r'\bsistava\b', 'sústava'),
        (r'\bsistavu\b', 'sústavu'),
        (r'\bsistavy\b', 'sústavy'),
        (r'\bsistave\b', 'sústave'),
        (r'\bzalidok\b', 'žalúdok'),
        (r'\bzalidka\b', 'žalúdka'),
        (r'\bzalidku\b', 'žalúdku'),
        (r'\bzPaza\b', 'žľaza'),
        (r'\bzPazy\b', 'žľazy'),
        (r'\bzPazu\b', 'žľazu'),
        (r'\bžaza\b', 'žľaza'),
        (r'\bžazy\b', 'žľazy'),
        (r'\bzaza\b', 'žľaza'),
        (r'\bzazy\b', 'žľazy'),
        (r'\bČrevo\b', 'črevo'),
        (r'\bČreve\b', 'čreve'),
        (r'\bČreva\b', 'čreva'),
        (r'\bhrubé revo\b', 'hrubé črevo'),
        (r'\btenké revo\b', 'tenké črevo'),
        (r'\btenkom Čreve\b', 'tenkom čreve'),
        (r'\bhrubom Čreve\b', 'hrubom čreve'),
        (r'\bČím\b', 'čím'),
        (r'\bČom\b', 'čom'),
        (r'\bČloveka\b', 'človeka'),
        (r'\bloveka\b', 'človeka'),
        (r'\blovek\b', 'človek'),
        (r'\burych\'uje\b', 'urýchľuje'),
        (r'\bodde\'ovanie\b', 'oddeľovanie'),
        (r'\bodde\'ujú\b', 'oddeľujú'),
        (r'\bpodmie\'uje\b', 'podmieňuje'),
        (r'\bprezivavcov\b', 'prežúvavcov'),
        (r'\bprezivavce\b', 'prežúvavce'),
        (r'\bbylinozravcov\b', 'bylinožravcov'),
        (r'\bmasozravce\b', 'mäsožravce'),
        (r'\bmasozravcov\b', 'mäsožravcov'),
        (r'\bmackovité\b', 'mačkovité'),
        (r'\bpsovité\b', 'psovité'),
        (r'\bvel\'ryby\b', 'veľryby'),
        (r'\bobruckavce\b', 'obrúčkavce'),
        (r'\bobruckavcov\b', 'obrúčkavcov'),
        (r'\bKrvna\b', 'Krvná'),
        (r'\bkrvna\b', 'krvná'),
        (r'\bkrvne\b', 'krvné'),
        (r'\bVacsina\b', 'Väčšina'),
        (r'\bpeceni\b', 'pečeni'),
        (r'\bpecenou\b', 'pečeňou'),
        (r'\bpeceň\b', 'pečeň'),
    ]
    
    res = text
    for pat, rep in replacements:
        res = re.sub(pat, rep, res)
    return res

def main():
    print("Loading data files...")
    with open("biologia_otazky_1_450.json", "r", encoding="utf-8") as f:
        questions = json.load(f)
        
    with open("data_bio_answers_1_450.json", "r", encoding="utf-8") as f:
        answers_map = {int(k): v for k, v in json.load(f).items()}

    # Verified corrections based on the official UPJŠ LF answer key pages 311-314
    manual_answers = {
        4: ["e"],       # Q4: uvoľňovanie energie v prokaryotoch -> plazmatická membrána (e)
        5: ["b"],       # Q5: najmenší systém schopný samostatného života -> bunka (b)
        271: ["d"],     # Q271: celom -> druhotná telová dutina uzavretá mezodermom (d)
        314: ["b"],     # Q314: trávenie bielkovín začína v žalúdku pepsínom (b)
        316: ["a"],     # Q316: žalúdok prežúvavcov: bachor, čepiec, kniha + slez (a)
        317: ["c"],     # Q317: celulóza rozkladaná symbiotickými mikroorganizmami (c)
        319: ["d"],     # Q319: vstrebávanie látok -> tenké črevo (d)
        320: ["d"],     # Q320: trávenie bielkovín stavovcov -> žalúdok pepsín (d)
        336: ["d"],     # Q336: najefektívnejšia dýchacia sústava -> vtáky (d)
        351: ["c"],     # Q351: do čreva vyúsťujú -> Malpighiho žľazy hmyzu (c)
        352: ["b"],     # Q352: protonefrídie -> ploskavce (b)
        353: ["e"],     # Q353: vylučovacie orgány stavovcov -> obličky (e)
        365: ["e"],     # Q365: plazmatické bielkoviny vznikajú v pečeni (e)
        366: ["e"],     # Q366: najviac zastúpené organické látky plazmy -> bielkoviny (e)
    }

    for q_num, ans in manual_answers.items():
        answers_map[q_num] = ans

    # 1. Fix Question 365 options (page 80/81)
    q365 = questions[364]
    q365["content"] = "365. Väčšina plazmatických bielkovín vzniká v:"
    q365["options"] = [
        {"id": "a", "text": "červených krvinkách"},
        {"id": "b", "text": "slezine"},
        {"id": "c", "text": "kostnej dreni"},
        {"id": "d", "text": "srdci"},
        {"id": "e", "text": "pečeni"},
        {"id": "f", "text": "tkanivovom moku"},
        {"id": "g", "text": "lymfatických uzlinách"},
        {"id": "h", "text": "bunkách cievnych stien"}
    ]

    # 2. Fix Question 416 options (page 90)
    q416 = questions[415]
    q416["content"] = "416. Objaviteľ fagocytózy bol:"
    q416["options"] = [
        {"id": "a", "text": "P. Ehrlich"},
        {"id": "b", "text": "I. I. Mečnikov"},
        {"id": "c", "text": "I. M. Sečenov"},
        {"id": "d", "text": "I. P. Pavlov"},
        {"id": "e", "text": "N. Tinbergen"},
        {"id": "f", "text": "L. Pasteur"},
        {"id": "g", "text": "W. Harvey"},
        {"id": "h", "text": "S. W. Fox"}
    ]

    # 3. Clean typos and apply answers across all 450 questions
    for idx, q in enumerate(questions):
        q_num = idx + 1
        q["content"] = clean_typos(q["content"])
        
        # Ensure correct prefix
        if q_num == 324 and q["content"].startswith("324. 21:"):
            q["content"] = "324. Žlč:"
            
        for opt in q["options"]:
            opt["text"] = clean_typos(opt["text"])
            
        correct = answers_map.get(q_num, q.get("correct_answers", []))
        # Ensure clean unique sorted list of valid letters a..h
        clean_correct = sorted(list(set(c for c in correct if c in "abcdefgh")))
        q["correct_answers"] = clean_correct
        
        if len(clean_correct) == 1:
            q["explanation"] = f"Správna odpoveď podľa oficiálneho kľúča testovnice UPJŠ LF je: {clean_correct[0].upper()}."
        else:
            q["explanation"] = f"Správne odpovede podľa oficiálneho kľúča testovnice UPJŠ LF sú: {', '.join(a.upper() for a in clean_correct)}."

    print("Saving updated json files...")
    with open("biologia_otazky_1_450.json", "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
        
    with open("data_bio_answers_1_450.json", "w", encoding="utf-8") as f:
        json.dump({str(k): v for k, v in sorted(answers_map.items())}, f, ensure_ascii=False, indent=2)

    print("Saved files successfully.")

    # Authenticate and upload to Supabase
    print("Authenticating admin in Supabase...")
    token = get_admin_token()
    auth_headers = {
        "apikey": API_KEY,
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    print("Authenticated successfully.")

    # Get category ID for 'Biológia bunky, rastlín a živočíchov'
    cat_id = "cbfbcc37-6a82-49fe-b8ef-236d2e6ea3a7"

    # Delete existing questions in this category
    print(f"Clearing existing questions in category {cat_id}...")
    del_req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/questions?category_id=eq.{cat_id}",
        headers=auth_headers,
        method="DELETE"
    )
    with urllib.request.urlopen(del_req) as _:
        pass
    print("Old questions deleted.")

    # Upload all 450 verified questions in batches of 50
    print("Uploading 450 verified questions...")
    batch_size = 50
    for i in range(0, len(questions), batch_size):
        batch = questions[i:i+batch_size]
        payload = []
        for q in batch:
            payload.append({
                "category_id": cat_id,
                "content": q["content"],
                "options": q["options"],
                "correct_answers": q["correct_answers"],
                "explanation": q["explanation"]
            })
            
        req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/questions",
            data=json.dumps(payload).encode("utf-8"),
            headers=auth_headers,
            method="POST"
        )
        with urllib.request.urlopen(req) as resp:
            pass
        print(f"Uploaded batch {i+1} to {min(i+batch_size, len(questions))}...")

    print("All 450 biology questions verified and successfully uploaded to Supabase!")

if __name__ == "__main__":
    main()
