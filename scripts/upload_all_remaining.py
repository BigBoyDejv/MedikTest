import urllib.request
import urllib.parse
import json

SUPABASE_URL = "https://wuklewurydjemuoxuhoq.supabase.co"
API_KEY = "sb_publishable_OHecNnlYu1zLQ1JnbIn9gQ_ebbcnscl"

def get_admin_token():
    auth_url = f"{SUPABASE_URL}/auth/v1/token?grant_type=password"
    headers = {
        "apikey": API_KEY,
        "Content-Type": "application/json"
    }
    payload = json.dumps({
        "email": "david.rusin@student.tuke.sk",
        "password": "Gow79206"
    }).encode("utf-8")
    req = urllib.request.Request(auth_url, data=payload, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))["access_token"]

def ensure_category(token, subject_id, category_name):
    encoded_name = urllib.parse.quote(category_name)
    url = f"{SUPABASE_URL}/rest/v1/categories?select=id,name&subject_id=eq.{subject_id}&name=eq.{encoded_name}"
    headers = {
        "apikey": API_KEY,
        "Authorization": f"Bearer {token}"
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        existing = json.loads(resp.read().decode("utf-8"))
        if existing:
            return existing[0]["id"]

    # Create category
    create_url = f"{SUPABASE_URL}/rest/v1/categories"
    create_headers = {
        "apikey": API_KEY,
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    payload = json.dumps({
        "subject_id": subject_id,
        "name": category_name
    }).encode("utf-8")
    req2 = urllib.request.Request(create_url, data=payload, headers=create_headers)
    with urllib.request.urlopen(req2) as resp2:
        created = json.loads(resp2.read().decode("utf-8"))
        return created[0]["id"]

def main():
    token = get_admin_token()
    print("Admin authenticated.")

    # Get Chemistry subject_id
    subj_url = f"{SUPABASE_URL}/rest/v1/subjects?select=id,name&name=eq.{urllib.parse.quote('Chémia')}"
    req = urllib.request.Request(subj_url, headers={"apikey": API_KEY, "Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        chem_subject_id = json.loads(resp.read().decode("utf-8"))[0]["id"]

    cat_org_id = ensure_category(token, chem_subject_id, "Organická chémia")
    cat_bio_id = ensure_category(token, chem_subject_id, "Biochémia")
    print(f"Categories ready: Organická chémia ({cat_org_id}), Biochémia ({cat_bio_id})")

    with open("chemia_otazky_641_1500.json", "r", encoding="utf-8") as f:
        questions = json.load(f)

    # Clear any previous questions in these two categories to prevent duplicates
    for cid in [cat_org_id, cat_bio_id]:
        del_req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/questions?category_id=eq.{cid}",
            headers={"apikey": API_KEY, "Authorization": f"Bearer {token}"},
            method="DELETE"
        )
        with urllib.request.urlopen(del_req) as _:
            pass

    insert_url = f"{SUPABASE_URL}/rest/v1/questions"
    insert_headers = {
        "apikey": API_KEY,
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    batch_size = 100
    total = 0
    for i in range(0, len(questions), batch_size):
        batch = questions[i:i+batch_size]
        records = []
        for q in batch:
            cid = cat_org_id if q["category"] == "Organická chémia" else cat_bio_id
            records.append({
                "category_id": cid,
                "content": q["content"],
                "options": q["options"],
                "correct_answers": q["correct_answers"],
                "explanation": q.get("explanation", "")
            })
        req_ins = urllib.request.Request(
            insert_url,
            data=json.dumps(records).encode("utf-8"),
            headers=insert_headers
        )
        with urllib.request.urlopen(req_ins) as _:
            total += len(records)
            print(f"Uploaded {total}/{len(questions)} questions...")

    print("ALL 860 QUESTIONS (641-1500) UPLOADED TO SUPABASE!")

    # Verify total count in Supabase
    count_req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/questions?select=id",
        headers={"apikey": API_KEY, "Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(count_req) as resp:
        all_q = json.loads(resp.read().decode("utf-8"))
        print(f"Total questions now in Supabase DB: {len(all_q)}")

    # Git add, commit, push
    import subprocess
    subprocess.run(["git", "add", "chemia_otazky_641_1500.json", "data_answers_641_1500.json", "scripts/"], check=True)
    subprocess.run(["git", "commit", "-m", "Add remaining chemistry questions 641-1500 (Organic chemistry & Biochemistry)"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("GIT COMMIT AND PUSH COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    main()

