
import json
import os
import shutil
import tempfile
from datetime import datetime
from pathlib import Path

import argparse

DEFAULT_REVIEW_FILE = Path("results/correctness-review.fresh.jsonl")
DEFAULT_BACKUP_DIR = Path("results/review-backups")
REVIEW_FILE = DEFAULT_REVIEW_FILE
BACKUP_DIR = DEFAULT_BACKUP_DIR

VARIANTS = ("BASE MODEL", "DEVMATE V1", "DEVMATE V2", "DEVMATE V3")
RATING_FIELDS = (
    "technical_correctness",
    "relevance",
    "practical_usefulness",
)
SCORE_FIELDS = (*RATING_FIELDS, "critical_error")
REQUIRED_FIELDS = ("id", "question", "answers", "scores", "review_notes")


def validate_record(record, line_number):
    if not isinstance(record, dict):
        raise ValueError(f"Record on line {line_number} must be a JSON object.")

    missing = [field for field in REQUIRED_FIELDS if field not in record]
    if missing:
        raise ValueError(
            f"Missing fields on line {line_number}: {', '.join(missing)}"
        )

    if not isinstance(record["answers"], dict):
        raise ValueError(f"'answers' must be an object on line {line_number}.")
    if not isinstance(record["scores"], dict):
        raise ValueError(f"'scores' must be an object on line {line_number}.")
    if not isinstance(record["review_notes"], dict):
        raise ValueError(f"'review_notes' must be an object on line {line_number}.")

    for model in VARIANTS:
        if model not in record["answers"] or model not in record["scores"]:
            raise ValueError(
                f"Missing model data for {model} on line {line_number}."
            )

        score = record["scores"][model]
        if not isinstance(score, dict):
            raise ValueError(
                f"Scores for {model} must be an object on line {line_number}."
            )

        missing_scores = [field for field in SCORE_FIELDS if field not in score]
        if missing_scores:
            raise ValueError(
                f"Missing score fields for {model} on line {line_number}: "
                f"{', '.join(missing_scores)}"
            )

        for field in RATING_FIELDS:
            value = score[field]
            if value is not None and (
                isinstance(value, bool)
                or not isinstance(value, int)
                or not 1 <= value <= 5
            ):
                raise ValueError(
                    f"{field} for {model} on line {line_number} "
                    "must be null or an integer from 1 to 5."
                )

        critical_error = score["critical_error"]
        if critical_error is not None and not isinstance(critical_error, bool):
            raise ValueError(
                f"critical_error for {model} on line {line_number} "
                "must be null or a Boolean."
            )

        if model not in record["review_notes"]:
            record["review_notes"][model] = ""

        if not isinstance(record["review_notes"][model], str):
            raise ValueError(
                f"Review notes for {model} must be text on line {line_number}."
            )


def load_reviews():
    if not REVIEW_FILE.exists():
        raise FileNotFoundError(
            f"Review file not found: {REVIEW_FILE}\n"
            "Generate the expected review data before running this tool. "
            "This script will not create or overwrite a review dataset."
        )

    records = []
    with REVIEW_FILE.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc

            validate_record(record, line_number)
            records.append(record)

    if not records:
        raise ValueError("No review records found.")

    return records


def is_complete(record, model):
    score = record["scores"][model]
    return all(score.get(field) is not None for field in SCORE_FIELDS)


def get_rating(label):
    while True:
        value = input(f"{label} (1-5): ").strip()
        try:
            rating = int(value)
        except ValueError:
            print("Enter a whole number from 1 to 5.")
            continue

        if 1 <= rating <= 5:
            return rating

        print("Rating must be between 1 and 5.")


def get_boolean(label):
    while True:
        value = input(f"{label} (y/n): ").strip().lower()
        if value in ("y", "yes"):
            return True
        if value in ("n", "no"):
            return False
        print("Enter y or n.")


def save_reviews(records):
    if not REVIEW_FILE.is_file():
        raise FileNotFoundError(
            f"Review file disappeared before saving: {REVIEW_FILE}"
        )

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    backup_path = BACKUP_DIR / f"correctness-review-{timestamp}.jsonl"
    temp_path = None

    # Create the backup before replacing the original file.
    shutil.copy2(REVIEW_FILE, backup_path)

    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            newline="\n",
            dir=REVIEW_FILE.parent,
            delete=False,
        ) as temp_file:
            temp_path = Path(temp_file.name)
            for record in records:
                temp_file.write(json.dumps(record, ensure_ascii=False) + "\n")
            temp_file.flush()
            os.fsync(temp_file.fileno())

        os.replace(temp_path, REVIEW_FILE)
    except Exception:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink()
        raise

    print(f"Saved review data. Backup: {backup_path}")


def main():
    records = load_reviews()
    total_answers = len(records) * len(VARIANTS)

    while True:
        pending = [
            (record, model)
            for record in records
            for model in VARIANTS
            if not is_complete(record, model)
        ]

        completed = total_answers - len(pending)
        print(
            f"\nDevMate Model Review — "
            f"{completed}/{total_answers} answers completed"
        )

        if not pending:
            print("All answers have been scored.")
            return

        print("\nPending answers:")
        for index, (record, model) in enumerate(pending[:10], start=1):
            print(f"{index}. Question {record['id']} — {model}")

        print(
            "Enter a listed number to review an answer, "
            "'q' to quit, or 's' for status."
        )
        choice = input("Choice: ").strip().lower()

        if choice == "q":
            print("Goodbye!")
            return

        if choice == "s":
            continue

        try:
            selected_number = int(choice)
        except ValueError:
            print("Choose a listed number, s, or q.")
            continue

        visible_count = min(10, len(pending))
        if not 1 <= selected_number <= visible_count:
            print(f"Choose a number from 1 to {visible_count}.")
            continue

        record, model = pending[selected_number - 1]

        print("\n" + "=" * 72)
        print(f"Question {record['id']}: {record['question']}")
        print(f"\nModel: {model}\n")
        print(record["answers"][model])
        print("\n" + "=" * 72)
        print(
            "Rate the answer based on correctness, relevance, "
            "and practical value."
        )

        if input("Score this answer now? (y/n): ").strip().lower() not in (
            "y", "yes"
        ):
            continue

        new_score = {
            "technical_correctness": get_rating("Technical correctness"),
            "relevance": get_rating("Relevance"),
            "practical_usefulness": get_rating("Practical usefulness"),
            "critical_error": get_boolean("Contains a critical technical error"),
        }
        notes = input("Review notes (brief reason; Enter to skip): ").strip()

        old_score = record["scores"][model].copy()
        old_notes = record["review_notes"].get(model, "")
        record["scores"][model] = new_score
        record["review_notes"][model] = notes

        try:
            save_reviews(records)
        except Exception:
            record["scores"][model] = old_score
            record["review_notes"][model] = old_notes
            raise

        print("Answer scored successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Review DevMate model answers.")
    parser.add_argument(
        "--review-file",
        type=Path,
        default=DEFAULT_REVIEW_FILE,
        help="Path to the JSONL review file.",
    )
    parser.add_argument(
        "--backup-dir",
        type=Path,
        default=None,
        help="Directory for backups. Defaults to a review-backups folder beside the review file.",
    )
    args = parser.parse_args()

    REVIEW_FILE = args.review_file
    BACKUP_DIR = args.backup_dir or REVIEW_FILE.parent / "review-backups"

    main()
