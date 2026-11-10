import sys
import os
sys.path.insert(0, os.path.abspath("."))
import json
import urllib.request

from scripts.parse_bio_questions_full import ocr_and_parse_bio_chapter
from scripts.upload_biology_category import upload_questions_for_category

PDF_PATH = "Biológia 2026.pdf"

def main():
    print("=" * 60)
    print("STARTING PHASE 2: GENETIKA (Otázky 901 -> 1250)")
    print("Pages in PDF: 186 to 261 (76 pages)")
    print("=" * 60, flush=True)

    with open("data_bio_answers_451_1500.json", "r", encoding="utf-8") as f:
        answers = {int(k): v for k, v in json.load(f).items()}

    print(f"Loaded {len(answers)} verified answers.", flush=True)

    items, parsed_qs = ocr_and_parse_bio_chapter(
        pdf_path=PDF_PATH,
        start_page=186,
        end_page=261,
        start_q=901,
        end_q=1250,
        category_name="Genetika",
        answers=answers,
        cache_file="ocr_cache_bio_genetika_901_1250.json"
    )

    print(f"\nParsing complete: {len(parsed_qs)}/350 questions parsed. Total items: {len(items)}", flush=True)
    placeholders = sum(1 for it in items if "Otázka č." in it["content"])
    print(f"Placeholder questions: {placeholders}/350", flush=True)

    output_path = "data/genetika_901_1250.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print(f"Saved {output_path}", flush=True)

    # Upload to Supabase category 'Genetika'
    print("\nUploading to Supabase category 'Genetika'...", flush=True)
    ok = upload_questions_for_category("Genetika", output_path)
    if ok:
        print("\n" + "=" * 60)
        print("PHASE 2 (GENETIKA 901 -> 1250) SUCCESSFULLY COMPLETED!")
        print("=" * 60, flush=True)
    else:
        print("Warning: Issue during upload of Genetika!")

if __name__ == "__main__":
    main()

