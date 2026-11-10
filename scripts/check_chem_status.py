import os
import json

def check_chem_status():
    done_count = 0
    total_qs = 0
    for b in range(1, 9):
        path = f"scripts/chem_batches/batch_{b}_explained.json"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            real_exp = sum(1 for q in data if not q.get("explanation", "").startswith("Správne odpovede podľa oficiálneho"))
            print(f"Chem Batch {b}: {len(data)} questions, {real_exp} real explanations")
            if real_exp == len(data) and len(data) == 50:
                done_count += 1
            total_qs += len(data)
        else:
            print(f"Chem Batch {b}: waiting...")
    print(f"Total chem batches ready: {done_count}/8")
    return done_count == 8

if __name__ == "__main__":
    check_chem_status()

