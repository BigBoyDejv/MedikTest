import urllib.request
import json
import subprocess

SUPABASE_URL = "https://wuklewurydjemuoxuhoq.supabase.co"
API_KEY = "sb_publishable_OHecNnlYu1zLQ1JnbIn9gQ_ebbcnscl"

def main():
    headers = {"apikey": API_KEY, "Authorization": f"Bearer {API_KEY}", "Prefer": "count=exact"}
    req = urllib.request.Request(f"{SUPABASE_URL}/rest/v1/questions?select=id&limit=1", headers=headers)
    with urllib.request.urlopen(req) as resp:
        content_range = resp.headers.get("Content-Range")
        print(f"Exact Supabase Content-Range: {content_range}")

    subprocess.run(["git", "add", "src/app/test/page.tsx", "src/app/dashboard/page.tsx", "src/app/test/actions.ts", "scripts/upload_all_remaining.py"], check=True)
    subprocess.run(["git", "commit", "-m", "Support >1000 questions pagination across test builder and dashboard"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("Pushed pagination support to GitHub successfully!")

if __name__ == "__main__":
    main()
