import urllib.request
import json
import os

env = {}
with open('.env.local', 'r', encoding='utf-8') as f:
    for line in f:
        if '=' in line and not line.strip().startswith('#'):
            k, v = line.strip().split('=', 1)
            env[k] = v.strip("\"'\n\r")

url = env.get('NEXT_PUBLIC_SUPABASE_URL')
key = env.get('NEXT_PUBLIC_SUPABASE_ANON_KEY')
headers = {'apikey': key, 'Authorization': f'Bearer {key}'}

# Subjects
r = urllib.request.Request(f'{url}/rest/v1/subjects?select=id,name', headers=headers)
with urllib.request.urlopen(r) as resp:
    subjects = json.loads(resp.read().decode())

print('=== AKTUÁLNY STAV DATABÁZY OTÁZOK ===\n')
total_db = 0
for s in subjects:
    print(f'Predmet: {s["name"]}')
    r = urllib.request.Request(f'{url}/rest/v1/categories?subject_id=eq.{s["id"]}&select=id,name', headers=headers)
    with urllib.request.urlopen(r) as resp:
        cats = json.loads(resp.read().decode())
    total_s = 0
    for c in cats:
        r = urllib.request.Request(f'{url}/rest/v1/questions?category_id=eq.{c["id"]}&select=id,content,explanation,options&limit=1000', headers=headers)
        with urllib.request.urlopen(r) as resp:
            qs = json.loads(resp.read().decode())
        has_real_exp = sum(1 for q in qs if q.get('explanation') and not q['explanation'].startswith('Správne odpovede podľa oficiálneho'))
        has_8_opt = sum(1 for q in qs if len(q.get('options', [])) == 8)
        print(f'  - Okruh: "{c["name"]}"')
        print(f'      Počet otázok: {len(qs)}')
        print(f'      S odborným vysvetlením: {has_real_exp}/{len(qs)}')
        print(f'      S kompletnými 8 možnosťami (A-H): {has_8_opt}/{len(qs)}')
        total_s += len(qs)
    print(f'  >> SPOLU V {s["name"].upper()}: {total_s} otázok\n')
    total_db += total_s

print(f'CELKOVO V DATABÁZE: {total_db} otázok')

