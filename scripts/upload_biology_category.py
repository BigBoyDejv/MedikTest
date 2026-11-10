import sys
import os
sys.path.insert(0, os.path.abspath("."))
import urllib.request
import json
from scripts.merge_and_upload_bio import env, url, key, get_admin_token

def upload_questions_for_category(category_name, json_file_path):
    if not os.path.exists(json_file_path):
        print(f"Error: {json_file_path} not found!")
        return False

    with open(json_file_path, "r", encoding="utf-8") as f:
        questions = json.load(f)

    print(f"Loaded {len(questions)} questions from {json_file_path}")

    admin_token = get_admin_token()
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    # Fetch Category ID
    quoted_name = urllib.parse.quote(category_name)
    req = urllib.request.Request(f"{url}/rest/v1/categories?name=eq.{quoted_name}&select=id", headers=headers)
    with urllib.request.urlopen(req) as resp:
        cats = json.loads(resp.read().decode())

    if not cats:
        print(f"Error: Category '{category_name}' not found!")
        return False
    cat_id = cats[0]["id"]
    print(f"Target Category: {category_name} (ID: {cat_id})")

    # Fetch existing questions in this category to prevent duplicate insertion
    req_existing = urllib.request.Request(f"{url}/rest/v1/questions?category_id=eq.{cat_id}&select=id,content&limit=1500", headers=headers)
    with urllib.request.urlopen(req_existing) as resp:
        existing_qs = json.loads(resp.read().decode())

    existing_prefixes = set()
    for eq in existing_qs:
        parts = eq["content"].split(".", 1)
        if parts[0].isdigit():
            existing_prefixes.add(int(parts[0]))

    print(f"Existing question numbers in category: {len(existing_prefixes)}")

    # Filter out already existing questions
    to_insert = []
    for q in questions:
        num = None
        parts = q["content"].split(".", 1)
        if parts[0].isdigit():
            num = int(parts[0])

        if num is not None and num in existing_prefixes:
            continue

        to_insert.append({
            "category_id": cat_id,
            "content": q["content"],
            "options": q["options"],
            "correct_answers": q["correct_answers"],
            "explanation": q.get("explanation", "")
        })

    print(f"Questions to insert: {len(to_insert)}")
    if not to_insert:
        print("All questions already present in Supabase!")
        return True

    # Insert in chunks of 50
    batch_size = 50
    total_inserted = 0
    for i in range(0, len(to_insert), batch_size):
        chunk = to_insert[i:i + batch_size]
        post_data = json.dumps(chunk).encode("utf-8")
        req_post = urllib.request.Request(f"{url}/rest/v1/questions", data=post_data, headers=headers)
        try:
            with urllib.request.urlopen(req_post) as resp:
                total_inserted += len(chunk)
                print(f"Inserted {total_inserted}/{len(to_insert)} questions...")
        except Exception as e:
            print(f"Error inserting chunk {i}-{i+batch_size}: {e}")
            return False

    print(f"SUCCESS: Uploaded {total_inserted} questions to category '{category_name}'!")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python upload_biology_category.py <category_name> <json_file_path>")
    else:
        upload_questions_for_category(sys.argv[1], sys.argv[2])

