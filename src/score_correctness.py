
import json
from pathlib import Path

INPUT_FILE = Path("results/model-comparison-v3.jsonl")
OUTPUT_FILE = Path("results/correctness-review.jsonl")

VARIANTS = ("BASE MODEL", "DEVMATE V1", "DEVMATE V2", "DEVMATE V3")


def load_results():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"{INPUT_FILE} not found. "
            "Run src/evaluate_model.py first."
        )

    records = []

    with INPUT_FILE.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            record = json.loads(line)

            if "question" not in record:
                raise ValueError(
                    f"Missing question on line {line_number}"
                )

            for variant in VARIANTS:
                if variant not in record:
                    raise ValueError(
                        f"Missing {variant} on line {line_number}"
                    )

            records.append(record)

    if not records:
        raise ValueError("No evaluation records found.")

    return records


def main():
    if OUTPUT_FILE.exists():
        raise FileExistsError(
            f"{OUTPUT_FILE} already exists. "
            "Refusing to overwrite review data. "
            "Back it up or use a dedicated merge/resume workflow."
        )

    records = load_results()
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("x", encoding="utf-8") as file:
        for index, record in enumerate(records, start=1):
            review = {
                "id": index,
                "question": record["question"],
                "answers": {
                    variant: record[variant]
                    for variant in VARIANTS
                },
                "scores": {
                    variant: {
                        "technical_correctness": None,
                        "relevance": None,
                        "practical_usefulness": None,
                        "critical_error": None,
                    }
                    for variant in VARIANTS
                },
                "review_notes": {
                    variant: ""
                    for variant in VARIANTS
                },
            }

            file.write(
                json.dumps(review, ensure_ascii=False) + "\n"
            )

    print(f"Questions prepared: {len(records)}")
    print(f"Models per question: {len(VARIANTS)}")
    print(f"Answers to review: {len(records) * len(VARIANTS)}")
    print(f"Review file saved to: {OUTPUT_FILE}")
    print("\nScores are intentionally blank until manually reviewed.")


if __name__ == "__main__":
    main()
