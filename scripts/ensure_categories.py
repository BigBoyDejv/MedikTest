import sys
import os
sys.path.insert(0, os.path.abspath("."))
import urllib.request
import json
from scripts.merge_and_upload_bio import env, url, key, get_admin_token

admin_token = get_admin_token()
headers = {
    "apikey": key,
    "Authorization": f"Bearer {admin_token}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

bio_sub_id = "daad804c-2a8e-4a13-bc9e-5b02fa9926a5"

target_categories = [
    "Biológia človeka",
    "Genetika",
    "Systém rastlín a živočíchov",
    "Ekológia a evolúcia"
]

# Check existing categories
req = urllib.request.Request(f"{url}/rest/v1/categories?subject_id=eq.{bio_sub_id}&select=id,name", headers=headers)
with urllib.request.urlopen(req) as resp:
    existing = json.loads(resp.read().decode())

existing_names = {c["name"]: c["id"] for c in existing}
print(f"Existing biology categories: {existing_names}")

for name in target_categories:
    if name not in existing_names:
        print(f"Creating category: {name}")
        post_data = json.dumps({"subject_id": bio_sub_id, "name": name}).encode("utf-8")
        req_post = urllib.request.Request(f"{url}/rest/v1/categories", data=post_data, headers=headers)
        with urllib.request.urlopen(req_post) as r:
            created = json.loads(r.read().decode())
            print(f"Created: {created}")
            existing_names[name] = created[0]["id"]
    else:
        print(f"Already exists: {name} -> {existing_names[name]}")

print("All Biology categories ready!")
