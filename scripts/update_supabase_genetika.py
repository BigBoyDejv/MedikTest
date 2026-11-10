import sys
import os
sys.path.insert(0, os.path.abspath("."))
import urllib.request
import json
import re
from scripts.merge_and_upload_bio import env, url, key, get_admin_token

def update_genetika():
    with open("data/genetika_901_1250.json", "r", encoding="utf-8") as f:
        questions = json.load(f)

    admin_token = get_admin_token()
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    cat_id = "c4fba202-b5d0-4104-a418-c2b358043fb3" # Genetika
    req = urllib.request.Request(f"{url}/rest/v1/questions?category_id=eq.{cat_id}&select=id,content&limit=1000", headers=headers)
    with urllib.request.urlopen(req) as resp:
        db_qs = json.loads(resp.read().decode())

    print(f"Fetched {len(db_qs)} questions from Supabase for category 'Genetika'")

    db_by_num = {}
    for dbq in db_qs:
        m = re.match(r"^(\d+)\.", dbq["content"].strip())
        if m:
            db_by_num[int(m.group(1))] = dbq["id"]

    updated = 0
    for q in questions:
        m = re.match(r"^(\d+)\.", q["content"].strip())
        if not m:
            continue
        num = int(m.group(1))
        db_id = db_by_num.get(num)
        if not db_id:
            continue

        patch_data = json.dumps({
            "content": q["content"],
            "options": q["options"],
            "correct_answers": q["correct_answers"],
            "explanation": q.get("explanation", "")
        }).encode("utf-8")

        patch_req = urllib.request.Request(
            f"{url}/rest/v1/questions?id=eq.{db_id}",
            data=patch_data,
            headers=headers,
            method="PATCH"
        )
        try:
            with urllib.request.urlopen(patch_req):
                updated += 1
                if updated % 50 == 0:
                    print(f"Updated {updated}/350 questions in Supabase...")
        except Exception as e:
            print(f"Error updating Q{num}: {e}")

    print(f"SUCCESS: Updated {updated}/350 questions in Supabase for Genetika!")

if __name__ == "__main__":
    update_genetika()

