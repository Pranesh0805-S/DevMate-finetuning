import json
import os
import shutil
import tempfile
from datetime import datetime
from pathlib import Path

REVIEW_FILE = Path("results/correctness-review.fresh.jsonl")
BACKUP_DIR = Path("results/review-backups")
VARIANTS = ("BASE MODEL", "DEVMATE V1", "DEVMATE V2", "DEVMATE V3")
RATING_FIELDS = (
    "technical_correctness",
    "relevance",
    "practical_usefulness",
)
SCORE_FIELDS = (*RATING_FIELDS, "critical_error")


def load_reviews():
    records = []
    with REVIEW_FILE.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, 1):
            if not line.strip():
                continue
            record = json.loads(line)
            for key in ("id", "question", "answers", "scores", "review_notes"):
                if key not in record:
                    raise ValueError(f"Missing {key} on line {line_number}")
            for model in VARIANTS:
                if model not in record["answers"] or model not in record["scores"]:
                    raise ValueError(f"Missing {model} on line {line_number}")
                if not all(k in record["scores"][model] for k in SCORE_FIELDS):
                    raise ValueError(f"Missing score fields on line {line_number}")
                record["review_notes"].setdefault(model, "")
            records.append(record)
    if not records:
        raise ValueError("No review records found.")
    return records


def complete(record, model):
    scores = record["scores"].get(model, {})

    for field in ("technical_correctness", "relevance", "practical_usefulness"):
        value = scores.get(field)
        if type(value) is not int or not 1 <= value <= 5:
            return False

    return type(scores.get("critical_error")) is bool


def save_reviews(records):
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    backup = BACKUP_DIR / f"correctness-review-{stamp}.jsonl"
    shutil.copy2(REVIEW_FILE, backup)
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", newline="\n",
            dir=REVIEW_FILE.parent, delete=False
        ) as f:
            temp_path = Path(f.name)
            for record in records:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_path, REVIEW_FILE)
    except Exception:
        if temp_path and temp_path.exists():
            temp_path.unlink()
        raise
    print(f"Saved. Backup created: {backup}")


def ask_rating(label, previous):
    while True:
        raw = input(f"  {label} (1-5, required): ").strip()
        try:
            value = int(raw)
            if 1 <= value <= 5:
                return value
        except ValueError:
            pass
        print("  Please enter a number from 1 to 5.")


def ask_boolean(previous):
    while True:
        raw = input("  Critical technical error? (y/n, required): ").strip().lower()
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("  Please enter y or n.")


def review_question(records, record):
    print("\n" + "=" * 88)
    print(f"QUESTION {record['id']}: {record['question']}")
    print("=" * 88)

    for model in VARIANTS:
        score = record["scores"][model]
        status = "COMPLETE" if complete(record, model) else "PENDING"
        print(f"\n--- {model} | {status} ---")
        print(record["answers"][model])
        print("\nCurrent ratings:", score)
        if record["review_notes"].get(model):
            print("Current note:", record["review_notes"][model])

    print("\nReview each model. Enter new ratings, or press Enter to keep existing ratings.")
    changed = False
    snapshots = {
        model: (record["scores"][model].copy(), record["review_notes"].get(model, ""))
        for model in VARIANTS
    }

    for model in VARIANTS:
        print(f"\nScoring {model}:")
        old = record["scores"][model]
        new = old.copy()
        for field, label in (
            ("technical_correctness", "Technical correctness"),
            ("relevance", "Relevance"),
            ("practical_usefulness", "Practical usefulness"),
        ):
            new[field] = ask_rating(label, old.get(field))
        new["critical_error"] = ask_boolean(old.get("critical_error"))

        old_note = record["review_notes"].get(model, "")
        note = input(f"  Review note [Enter=keep; type - to clear] [{old_note}]: ").strip()
        if note == "-":
            note = ""
        elif not note:
            note = old_note

        if new != old or note != old_note:
            changed = True
            record["scores"][model] = new
            record["review_notes"][model] = note

    if changed:
        try:
            save_reviews(records)
        except Exception:
            for model, (old_score, old_note) in snapshots.items():
                record["scores"][model] = old_score
                record["review_notes"][model] = old_note
            raise
        print("Question review saved.")
    else:
        print("No changes made.")


def main():
    if not REVIEW_FILE.exists():
        raise FileNotFoundError(f"Review file not found: {REVIEW_FILE}")
    records = load_reviews()
    while True:
        pending = [r for r in records if any(not complete(r, m) for m in VARIANTS)]
        done = sum(complete(r, m) for r in records for m in VARIANTS)
        total = len(records) * len(VARIANTS)
        print(f"\nDevMate Batch Review — {done}/{total} answers scored")
        print("Questions: " + ", ".join(
            f"{r['id']}{'*' if any(not complete(r, m) for m in VARIANTS) else ''}"
            for r in records
        ))
        print("* = at least one model answer pending")
        choice = input("Enter question ID to review/edit, 'p' for progress, or 'q' to quit: ").strip().lower()

        if choice == "q":
            print("All saved progress is preserved. Goodbye!")
            return
        if choice == "p":
            for record in records:
                statuses = ", ".join(
                    f"{m}: {'done' if complete(record, m) else 'pending'}"
                    for m in VARIANTS
                )
                print(f"Q{record['id']}: {statuses}")
            continue
        try:
            question_id = int(choice)
            record = next(r for r in records if r["id"] == question_id)
        except (ValueError, StopIteration):
            print("Enter a listed question ID, p, or q.")
            continue
        review_question(records, record)


if __name__ == "__main__":
    main()
