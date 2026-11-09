import urllib.request
import urllib.parse
import json
import subprocess

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

def ensure_category(token, subject_id, category_name):
    encoded_name = urllib.parse.quote(category_name)
    url = f"{SUPABASE_URL}/rest/v1/categories?select=id,name&subject_id=eq.{subject_id}&name=eq.{encoded_name}"
    headers = {"apikey": API_KEY, "Authorization": f"Bearer {token}"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        existing = json.loads(resp.read().decode("utf-8"))
        if existing:
            return existing[0]["id"]

    create_url = f"{SUPABASE_URL}/rest/v1/categories"
    create_headers = {
        "apikey": API_KEY,
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    payload = json.dumps({"subject_id": subject_id, "name": category_name}).encode("utf-8")
    req2 = urllib.request.Request(create_url, data=payload, headers=create_headers)
    with urllib.request.urlopen(req2) as resp2:
        return json.loads(resp2.read().decode("utf-8"))[0]["id"]

def upload_batches(token, questions, cat_map):
    insert_url = f"{SUPABASE_URL}/rest/v1/questions"
    insert_headers = {
        "apikey": API_KEY,
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    batch_size = 150
    for i in range(0, len(questions), batch_size):
        batch = questions[i:i+batch_size]
        records = [{
            "category_id": cat_map[q["category"]],
            "content": q["content"],
            "options": q["options"],
            "correct_answers": q["correct_answers"],
            "explanation": q.get("explanation", "")
        } for q in batch]
        req = urllib.request.Request(
            insert_url,
            data=json.dumps(records).encode("utf-8"),
            headers=insert_headers
        )
        with urllib.request.urlopen(req) as _:
            pass

def main():
    token = get_admin_token()
    print("Admin authenticated.")

    # Get subjects
    req_s = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/subjects?select=id,name",
        headers={"apikey": API_KEY, "Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(req_s) as resp:
        subjects = {s["name"]: s["id"] for s in json.loads(resp.read().decode("utf-8"))}

    chem_id = subjects["Chémia"]
    bio_id = subjects["Biológia"]

    cat_map = {
        "Všeobecná a anorganická chémia": ensure_category(token, chem_id, "Všeobecná a anorganická chémia"),
        "Organická chémia": ensure_category(token, chem_id, "Organická chémia"),
        "Biochémia": ensure_category(token, chem_id, "Biochémia"),
        "Biológia bunky, rastlín a živočíchov": ensure_category(token, bio_id, "Biológia bunky, rastlín a živočíchov"),
    }

    # Clear old questions in these categories to replace with 100% verified ones
    for cid in cat_map.values():
        del_req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/questions?category_id=eq.{cid}",
            headers={"apikey": API_KEY, "Authorization": f"Bearer {token}"},
            method="DELETE"
        )
        with urllib.request.urlopen(del_req) as _:
            pass

    all_files = [
        "chemia_otazky_1_300.json",
        "chemia_otazky_301_450.json",
        "chemia_otazky_641_1500.json",
        "biologia_otazky_1_450.json",
    ]

    for fname in all_files:
        with open(fname, "r", encoding="utf-8") as f:
            qs = json.load(f)
        upload_batches(token, qs, cat_map)
        print(f"Uploaded {fname} ({len(qs)} questions)")

    # Verify total count in Supabase
    count_req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/questions?select=id&limit=1",
        headers={"apikey": API_KEY, "Authorization": f"Bearer {API_KEY}", "Prefer": "count=exact"}
    )
    with urllib.request.urlopen(count_req) as resp:
        print("Exact Supabase Content-Range:", resp.headers.get("Content-Range"))

    # Git commit & push
    subprocess.run([
        "git", "add",
        "chemia_otazky_1_300.json",
        "chemia_otazky_301_450.json",
        "chemia_otazky_641_1500.json",
        "biologia_otazky_1_450.json",
        "data_answers_verified_1_1500.json",
        "data_bio_answers_1_450.json",
        "scripts/"
    ], check=True)
    subprocess.run([
        "git", "commit", "-m",
        "Verify all 1260 chemistry answer keys and add first 450 biology questions (1-450)"
    ], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("ALL DONE AND PUSHED TO GITHUB!")

if __name__ == "__main__":
    main()
