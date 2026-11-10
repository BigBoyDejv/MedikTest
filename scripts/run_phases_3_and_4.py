import sys
import os
sys.path.insert(0, os.path.abspath("."))
import json
import urllib.request

from scripts.parse_bio_questions_full import ocr_and_parse_bio_chapter
from scripts.upload_biology_category import upload_questions_for_category

PDF_PATH = "Biológia 2026.pdf"

PHASES = [
    {
        "name": "Systém rastlín a živočíchov",
        "start_q": 1251,
        "end_q": 1365,
        "start_page": 262,
        "end_page": 284,
        "cache_file": "ocr_cache_bio_system_1251_1365.json",
        "output_file": "data/system_rastlin_zivocichov_1251_1365.json"
    },
    {
        "name": "Ekológia a evolúcia",
        "start_q": 1366,
        "end_q": 1500,
        "start_page": 284,
        "end_page": 311,
        "cache_file": "ocr_cache_bio_ekologia_1366_1500.json",
        "output_file": "data/ekologia_evolucia_1366_1500.json"
    }
]

def main():
    print("=" * 60)
    print("STARTING EXECUTION OF PHASES 3 & 4 (Questions 1251 -> 1500)")
    print("=" * 60, flush=True)

    with open("data_bio_answers_451_1500.json", "r", encoding="utf-8") as f:
        answers = {int(k): v for k, v in json.load(f).items()}

    print(f"Loaded answers for {len(answers)} questions.\n", flush=True)

    for p in PHASES:
        print("\n" + "#" * 60)
        print(f"RUNNING: {p['name']} (Questions {p['start_q']} - {p['end_q']})")
        print(f"Pages in PDF: {p['start_page']} to {p['end_page']}")
        print("#" * 60, flush=True)

        items, parsed_qs = ocr_and_parse_bio_chapter(
            pdf_path=PDF_PATH,
            start_page=p["start_page"],
            end_page=p["end_page"],
            start_q=p["start_q"],
            end_q=p["end_q"],
            category_name=p["name"],
            answers=answers,
            cache_file=p["cache_file"]
        )

        expected = p["end_q"] - p["start_q"] + 1
        print(f"Parsing complete: {len(parsed_qs)}/{expected} questions. Total items built: {len(items)}", flush=True)
        placeholders = sum(1 for it in items if "Otázka č." in it["content"])
        print(f"Placeholders: {placeholders}/{expected}", flush=True)

        with open(p["output_file"], "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        print(f"Saved {p['output_file']}", flush=True)

        print(f"Uploading to Supabase category '{p['name']}'...", flush=True)
        ok = upload_questions_for_category(p["name"], p["output_file"])
        if ok:
            print(f"Uploaded {p['name']} successfully!", flush=True)
        else:
            print(f"Warning: Issue uploading {p['name']}", flush=True)

    print("\n" + "=" * 60)
    print("PHASES 3 & 4 SUCCESSFULLY PROCESSED AND UPLOADED!")
    print("=" * 60, flush=True)

if __name__ == "__main__":
    main()

