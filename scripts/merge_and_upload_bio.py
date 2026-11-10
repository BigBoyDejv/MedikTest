import os
import json
import urllib.request
import urllib.parse
import re

env = {}
if os.path.exists(".env.local"):
    with open(".env.local", "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.strip().split("=", 1)
                env[k] = v.strip("\"'\n\r")

url = env.get("NEXT_PUBLIC_SUPABASE_URL")
key = env.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")

def get_admin_token():
    auth_url = f"{url}/auth/v1/token?grant_type=password"
    headers = {"apikey": key, "Content-Type": "application/json"}
    payload = json.dumps({
        "email": "david.rusin@student.tuke.sk",
        "password": "Gow79206"
    }).encode("utf-8")
    req = urllib.request.Request(auth_url, data=payload, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))["access_token"]

admin_token = get_admin_token()
print("Successfully authenticated as admin!")

headers = {
    "apikey": key,
    "Authorization": f"Bearer {admin_token}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

def main():
    merged = []
    for b in range(1, 10):
        path = f"scripts/bio_batches/batch_{b}_explained.json"
        if not os.path.exists(path):
            print(f"ERROR: Missing {path}!")
            return
        with open(path, "r", encoding="utf-8") as f:
            batch = json.load(f)
        if len(batch) != 50:
            print(f"WARNING: Batch {b} has {len(batch)} items, expected 50")
        merged.extend(batch)

    print(f"Total merged questions: {len(merged)}")
    
    # Validation
    placeholder_count = 0
    for idx, q in enumerate(merged):
        exp = q.get("explanation", "").strip()
        if not exp or exp.startswith("Správne odpovede podľa oficiálneho"):
            placeholder_count += 1
            print(f"Missing explanation at index {idx}: {q.get('content')[:40]}")

    if placeholder_count > 0:
        print(f"ERROR: {placeholder_count} questions still have placeholder explanations!")
        return

    print("All 450 questions have detailed medical explanations!")

    # Save to biologia_otazky_1_450.json
    with open("biologia_otazky_1_450.json", "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
    print("Updated biologia_otazky_1_450.json")

    # Fetch Category ID for Biológia bunky, rastlín a živočíchov from Supabase
    req = urllib.request.Request(
        f"{url}/rest/v1/categories?name=eq.{urllib.parse.quote('Biológia bunky, rastlín a živočíchov')}&select=id",
        headers=headers
    )
    with urllib.request.urlopen(req) as resp:
        cats = json.loads(resp.read().decode())
    
    if not cats:
        print("ERROR: Category not found in Supabase!")
        return
    cat_id = cats[0]["id"]
    print(f"Category ID: {cat_id}")

    # Fetch all questions from Supabase for this category
    req = urllib.request.Request(
        f"{url}/rest/v1/questions?category_id=eq.{cat_id}&select=id,content&limit=1000",
        headers=headers
    )
    with urllib.request.urlopen(req) as resp:
        db_qs = json.loads(resp.read().decode())
    print(f"Fetched {len(db_qs)} questions from Supabase for category")

    # Map by leading question number e.g. "1.", "2.", "450."
    db_by_num = {}
    for dbq in db_qs:
        m = re.match(r"^(\d+)\.", dbq["content"].strip())
        if m:
            db_by_num[int(m.group(1))] = dbq["id"]

    print(f"Mapped {len(db_by_num)} questions by number from DB")

    # Upload updates in batches of 50
    updated_count = 0
    for q in merged:
        m = re.match(r"^(\d+)\.", q["content"].strip())
        if not m:
            continue
        num = int(m.group(1))
        db_id = db_by_num.get(num)
        if not db_id:
            print(f"Warning: Question {num} not found in DB by number")
            continue

        # PATCH question explanation
        patch_data = json.dumps({"explanation": q["explanation"]}).encode("utf-8")
        patch_req = urllib.request.Request(
            f"{url}/rest/v1/questions?id=eq.{db_id}",
            data=patch_data,
            headers=headers,
            method="PATCH"
        )
        try:
            with urllib.request.urlopen(patch_req) as resp:
                updated_count += 1
                if updated_count % 50 == 0:
                    print(f"Updated {updated_count}/450 questions in Supabase...")
        except Exception as e:
            print(f"Error updating question {num}: {e}")

    print(f"\nSUCCESS: Successfully updated {updated_count} questions with explanations in Supabase!")

if __name__ == "__main__":
    main()
