import urllib.request
import urllib.parse
import json

SUPABASE_URL = "https://wuklewurydjemuoxuhoq.supabase.co"
API_KEY = "sb_publishable_OHecNnlYu1zLQ1JnbIn9gQ_ebbcnscl"

# 1. Login as admin
auth_url = f"{SUPABASE_URL}/auth/v1/token?grant_type=password"
headers = {"apikey": API_KEY, "Content-Type": "application/json"}
payload = json.dumps({"email": "david.rusin@student.tuke.sk", "password": "Gow79206"}).encode("utf-8")
req = urllib.request.Request(auth_url, data=payload, headers=headers)
with urllib.request.urlopen(req) as resp:
    token = json.loads(resp.read().decode("utf-8"))["access_token"]

auth_headers = {"apikey": API_KEY, "Authorization": f"Bearer {token}"}

for cat_name in ["Cytológia a bunková biológia", "Genetika"]:
    enc = urllib.parse.quote(cat_name)
    req_cat = urllib.request.Request(f"{SUPABASE_URL}/rest/v1/categories?select=id,name&name=eq.{enc}", headers=auth_headers)
    with urllib.request.urlopen(req_cat) as resp:
        found = json.loads(resp.read().decode("utf-8"))
        for c in found:
            cid = c["id"]
            del_q = urllib.request.Request(f"{SUPABASE_URL}/rest/v1/questions?category_id=eq.{cid}", headers=auth_headers, method="DELETE")
            try:
                urllib.request.urlopen(del_q)
            except Exception:
                pass
            del_c = urllib.request.Request(f"{SUPABASE_URL}/rest/v1/categories?id=eq.{cid}", headers=auth_headers, method="DELETE")
            with urllib.request.urlopen(del_c) as r:
                print(f"Deleted category: {cat_name} ({cid}) -> {r.status}")

# Verify remaining categories
req_all = urllib.request.Request(f"{SUPABASE_URL}/rest/v1/categories?select=id,name,subject_id", headers=auth_headers)
with urllib.request.urlopen(req_all) as resp:
    cats = json.loads(resp.read().decode("utf-8"))
    print("Aktuálne kategórie v DB:")
    for c in cats:
        print(f" - {c['name']}")
