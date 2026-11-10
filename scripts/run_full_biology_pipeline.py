import sys
import os
sys.path.insert(0, os.path.abspath("."))
import time
import json
import urllib.request
import re

from scripts.parse_bio_questions_full import ocr_and_parse_bio_chapter
from scripts.upload_biology_category import upload_questions_for_category

PDF_PATH = "Biológia 2026.pdf"

CHAPTERS = [
    {
        "name": "Biológia človeka",
        "start_q": 451,
        "end_q": 900,
        "start_page": 97,
        "end_page": 186,
        "cache_file": "ocr_cache_bio_clovek_451_900.json",
        "output_file": "data/biologia_cloveka_451_900.json"
    },
    {
        "name": "Genetika",
        "start_q": 901,
        "end_q": 1250,
        "start_page": 186,
        "end_page": 261,
        "cache_file": "ocr_cache_bio_genetika_901_1250.json",
        "output_file": "data/genetika_901_1250.json"
    },
    {
        "name": "Systém rastlín a živočíchov",
        "start_q": 1251,
        "end_q": 1365,
        "start_page": 261,
        "end_page": 283,
        "cache_file": "ocr_cache_bio_system_1251_1365.json",
        "output_file": "data/system_rastlin_zivocichov_1251_1365.json"
    },
    {
        "name": "Ekológia a evolúcia",
        "start_q": 1366,
        "end_q": 1500,
        "start_page": 283,
        "end_page": 310,
        "cache_file": "ocr_cache_bio_ekologia_1366_1500.json",
        "output_file": "data/ekologia_evolucia_1366_1500.json"
    }
]

def load_answers():
    path = "data_bio_answers_451_1500.json"
    if not os.path.exists(path):
        print(f"Waiting for {path}...")
        while not os.path.exists(path):
            time.sleep(2)
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return {int(k): v for k, v in raw.items()}

def main():
    print("=" * 60)
    print("STARTING FULL BIOLOGY AUTOMATION PIPELINE (451 -> 1500)")
    print("=" * 60, flush=True)

    answers = load_answers()
    print(f"Loaded answers for {len(answers)} questions from key file.\n", flush=True)

    for ch in CHAPTERS:
        print("\n" + "#" * 60)
        print(f"PROCESSING CHAPTER: {ch['name']} (Questions {ch['start_q']} - {ch['end_q']})")
        print(f"Pages in PDF: {ch['start_page']} to {ch['end_page']}")
        print("#" * 60, flush=True)

        items, parsed_qs = ocr_and_parse_bio_chapter(
            PDF_PATH,
            ch["start_page"],
            ch["end_page"],
            ch["start_q"],
            ch["end_q"],
            ch["name"],
            answers,
            ch["cache_file"]
        )

        expected_count = ch["end_q"] - ch["start_q"] + 1
        print(f"Parsed {len(parsed_qs)}/{expected_count} questions. Total items built: {len(items)}", flush=True)

        # Save to JSON
        with open(ch["output_file"], "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        print(f"Saved {ch['output_file']}", flush=True)

        # Upload to Supabase
        print(f"Uploading to Supabase category '{ch['name']}'...", flush=True)
        ok = upload_questions_for_category(ch["name"], ch["output_file"])
        if ok:
            print(f"Category '{ch['name']}' uploaded successfully!", flush=True)
        else:
            print(f"Warning: Issue uploading category '{ch['name']}'", flush=True)

    print("\n" + "=" * 60)
    print("ALL BIOLOGY CHAPTERS SUCCESSFULLY PROCESSED AND UPLOADED!")
    print("=" * 60, flush=True)

if __name__ == "__main__":
    main()
