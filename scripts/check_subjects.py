import os
import json
import urllib.request

env = {}
if os.path.exists(".env.local"):
    with open(".env.local", "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.strip().split("=", 1)
                env[k] = v.strip("\"'")

url = env.get("NEXT_PUBLIC_SUPABASE_URL")
key = env.get("SUPABASE_SERVICE_ROLE_KEY") or env.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")
headers = {"apikey": key, "Authorization": f"Bearer {key}"}

req = urllib.request.Request(f"{url}/rest/v1/subjects?select=id,name", headers=headers)
with urllib.request.urlopen(req) as resp:
    subjects = json.loads(resp.read().decode())
print("Subjects:", subjects)

for s in subjects:
    sid = s["id"]
    req = urllib.request.Request(f"{url}/rest/v1/categories?subject_id=eq.{sid}&select=id,name", headers=headers)
    with urllib.request.urlopen(req) as resp:
        cats = json.loads(resp.read().decode())
    print(f"\nSubject: {s['name']} ({len(cats)} categories)")
    total_q = 0
    with_exp = 0
    for c in cats:
        cid = c["id"]
        req = urllib.request.Request(f"{url}/rest/v1/questions?category_id=eq.{cid}&select=id,content,explanation&limit=1000", headers=headers)
        with urllib.request.urlopen(req) as resp:
            qs = json.loads(resp.read().decode())
        total_q += len(qs)
        with_exp += sum(1 for q in qs if q.get("explanation"))
        print(f"  Category: {c['name']} - {len(qs)} questions (explanations: {sum(1 for q in qs if q.get('explanation'))})")
    print(f"Total in {s['name']}: {total_q} questions, with explanation: {with_exp}")

req = urllib.request.Request(f"{url}/rest/v1/questions?select=content,options,correct_answers,explanation&limit=10", headers=headers)
with urllib.request.urlopen(req) as resp:
    sample_qs = json.loads(resp.read().decode())
print("\n--- SAMPLE QUESTIONS ---")
for q in sample_qs:
    print("Q:", q["content"][:60])
    print("  Correct:", q["correct_answers"])
    print("  Explanation:", repr(q["explanation"]))
