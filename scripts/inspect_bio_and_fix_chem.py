import os
import json
import fitz

# 1. List PDF or new files in workspace
print("=== Files in workspace ===")
for f in os.listdir("."):
    if f.endswith(".pdf") or "bio" in f.lower() or "biolog" in f.lower():
        print(f"Found: {f} ({os.path.getsize(f)} bytes)")

# 2. Apply verified chemistry answers to chemia_otazky_*.json
with open("data_answers_verified_1_1500.json", "r", encoding="utf-8") as f:
    verified = json.load(f)

# Fallback for the 3 edge cases (222, 736, 1012) from previous answer dicts
for fallback_file in ["data_answers_1_300.json", "data_answers_301_600.json", "data_answers_641_1500.json"]:
    if os.path.exists(fallback_file):
        with open(fallback_file, "r", encoding="utf-8") as ff:
            old_d = json.load(ff)
            for k, v in old_d.items():
                if k not in verified:
                    verified[k] = v

total_fixed = 0
for q_file in ["chemia_otazky_1_300.json", "chemia_otazky_301_450.json", "chemia_otazky_641_1500.json"]:
    with open(q_file, "r", encoding="utf-8") as f:
        qs = json.load(f)
    file_fixed = 0
    for q in qs:
        q_num = q["content"].split(".")[0].strip()
        if q_num in verified:
            new_ans = verified[q_num]
            if q["correct_answers"] != new_ans:
                q["correct_answers"] = new_ans
                q["explanation"] = f"Správne odpovede podľa oficiálneho kľúča testovnice UPJŠ LF sú: {', '.join(a.upper() for a in new_ans)}."
                file_fixed += 1
                total_fixed += 1
    with open(q_file, "w", encoding="utf-8") as f:
        json.dump(qs, f, ensure_ascii=False, indent=2)
    print(f"Updated {q_file}: corrected {file_fixed} answer keys.")

print(f"Total chemistry answer keys corrected across all 1260 questions: {total_fixed}")

# Remove temporary png crops
for tmp_img in ["temp_ans_p321_col1.png", "temp_ans_p321_lines8_20.png", "temp_col1.png"]:
    if os.path.exists(tmp_img):
        os.remove(tmp_img)

