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
key = env.get("SUPABASE_SERVICE_ROLE_KEY") or env.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")
headers = {
    "apikey": key,
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

def check_batches_status():
    done_count = 0
    total_qs = 0
    for b in range(1, 10):
        path = f"scripts/bio_batches/batch_{b}_explained.json"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # check how many have new explanations
            real_exp = sum(1 for q in data if not q.get("explanation", "").startswith("Správne odpovede podľa oficiálneho"))
            print(f"Batch {b}: {len(data)} questions, {real_exp} real explanations")
            if real_exp == len(data) and len(data) == 50:
                done_count += 1
            total_qs += len(data)
        else:
            print(f"Batch {b}: waiting...")
    print(f"Total batches ready: {done_count}/9")
    return done_count == 9

if __name__ == "__main__":
    check_batches_status()

