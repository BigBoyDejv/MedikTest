import json
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

def main():
    print("Authenticating admin...")
    token = get_admin_token()
    auth_headers = {"apikey": API_KEY, "Authorization": f"Bearer {token}"}
    print("Authenticated.")

    # 1. Get Biológia subject
    req_s = urllib.request.Request(f"{SUPABASE_URL}/rest/v1/subjects?select=id,name", headers=auth_headers)
    with urllib.request.urlopen(req_s) as resp:
        subjects = {s["name"]: s["id"] for s in json.loads(resp.read().decode("utf-8"))}

    bio_id = subjects["Biológia"]

    # 2. Get or create category "Biológia bunky, rastlín a živočíchov"
    cat_name = "Biológia bunky, rastlín a živočíchov"
    encoded_name = urllib.parse.quote(cat_name)
    url = f"{SUPABASE_URL}/rest/v1/categories?select=id,name&subject_id=eq.{bio_id}&name=eq.{encoded_name}"
    req = urllib.request.Request(url, headers=auth_headers)
    with urllib.request.urlopen(req) as resp:
        existing = json.loads(resp.read().decode("utf-8"))
        if existing:
            cat_id = existing[0]["id"]
        else:
            create_url = f"{SUPABASE_URL}/rest/v1/categories"
            create_headers = {
                "apikey": API_KEY,
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Prefer": "return=representation"
            }
            payload = json.dumps({"subject_id": bio_id, "name": cat_name}).encode("utf-8")
            req2 = urllib.request.Request(create_url, data=payload, headers=create_headers)
            with urllib.request.urlopen(req2) as resp2:
                cat_id = json.loads(resp2.read().decode("utf-8"))[0]["id"]

    print(f"Category '{cat_name}' ID: {cat_id}")

    # 3. Clear existing questions in this category
    print(f"Clearing existing questions in category '{cat_name}'...")
    del_req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/questions?category_id=eq.{cat_id}",
        headers=auth_headers,
        method="DELETE"
    )
    with urllib.request.urlopen(del_req) as _:
        pass

    # 4. Load the 450 verified biology questions
    with open("biologia_otazky_1_450.json", "r", encoding="utf-8") as f:
        questions = json.load(f)

    print(f"Uploading {len(questions)} verified questions with diacritics...")
    insert_url = f"{SUPABASE_URL}/rest/v1/questions"
    insert_headers = {
        "apikey": API_KEY,
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    batch_size = 100
    total_uploaded = 0
    for i in range(0, len(questions), batch_size):
        batch = questions[i:i+batch_size]
        records = [{
            "category_id": cat_id,
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
        print(f"  Uploaded {total_uploaded} / {len(questions)}...")

    # 5. Check total questions in database
    count_req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/questions?select=count",
        headers={"apikey": API_KEY, "Authorization": f"Bearer {token}", "Range": "0-0", "Prefer": "count=exact"}
    )
    with urllib.request.urlopen(count_req) as resp:
        content_range = resp.headers.get("Content-Range", "")
        print(f"\nLive database total questions: {content_range}")

    print("\nALL 450 BIOLOGY QUESTIONS SUCCESSFULLY SYNCED TO SUPABASE!")

if __name__ == "__main__":
    main()
