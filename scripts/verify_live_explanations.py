import os
import json
import urllib.request
import urllib.parse

env = {}
if os.path.exists(".env.local"):
    with open(".env.local", "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.strip().split("=", 1)
                env[k] = v.strip("\"'\n\r")

url = env.get("NEXT_PUBLIC_SUPABASE_URL")
key = env.get("SUPABASE_SERVICE_ROLE_KEY") or env.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")
headers = {"apikey": key, "Authorization": f"Bearer {key}"}

print("=== VERIFYING SUPABASE LIVE DATA ===")
for cat_name in ["Biológia bunky, rastlín a živočíchov", "Všeobecná a anorganická chémia"]:
    req = urllib.request.Request(
        f"{url}/rest/v1/categories?name=eq.{urllib.parse.quote(cat_name)}&select=id,name",
        headers=headers
    )
    with urllib.request.urlopen(req) as resp:
        cat = json.loads(resp.read().decode())[0]

    req = urllib.request.Request(
        f"{url}/rest/v1/questions?category_id=eq.{cat['id']}&select=content,correct_answers,explanation&limit=3",
        headers=headers
    )
    with urllib.request.urlopen(req) as resp:
        sample = json.loads(resp.read().decode())

    print(f"\nCategory: {cat['name']}")
    for q in sample:
        print("  Q:", q["content"][:60])
        print("    Correct:", q["correct_answers"])
        print("    Explanation:", q["explanation"])
