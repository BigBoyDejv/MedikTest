import os
import json
import urllib.request

env = {}
with open('.env.local', 'r', encoding='utf-8') as f:
    for l in f:
        if '=' in l and not l.strip().startswith('#'):
            k, v = l.strip().split('=', 1)
            env[k] = v.strip('"\'\n\r')

url = env['NEXT_PUBLIC_SUPABASE_URL']
key = env['NEXT_PUBLIC_SUPABASE_ANON_KEY']
req = urllib.request.Request(f"{url}/rest/v1/categories?select=id,name,subjects(name)", headers={"apikey": key})
with urllib.request.urlopen(req) as r:
    print(json.dumps(json.loads(r.read()), indent=2, ensure_ascii=False))
