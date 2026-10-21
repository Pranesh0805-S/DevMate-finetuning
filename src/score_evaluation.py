
import json
from pathlib import Path
from statistics import mean

INPUT_FILE = Path("results/model-comparison-v3.jsonl")
VARIANTS = ("BASE MODEL", "DEVMATE V1", "DEVMATE V2", "DEVMATE V3")


def load_results():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Results file not found: {INPUT_FILE}. "
            "Run src/evaluate_model.py first."
        )

    records = []

    with INPUT_FILE.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON on line {line_number}: {exc}"
                ) from exc

            if not isinstance(record, dict) or "question" not in record:
                raise ValueError(
                    f"Line {line_number} must contain a question."
                )

            for variant in VARIANTS:
                if variant not in record:
                    raise ValueError(
                        f"Missing '{variant}' on line {line_number}."
                    )

                if not isinstance(record[variant], str):
                    raise ValueError(
                        f"'{variant}' must be text on line {line_number}."
                    )

            records.append(record)

    if not records:
        raise ValueError("The evaluation results file is empty.")

    return records


def summarize_answers(records):
    summaries = {}

    for variant in VARIANTS:
        answers = [record[variant].strip() for record in records]
        nonempty = [answer for answer in answers if answer]

        summaries[variant] = {
            "total": len(answers),
            "nonempty": len(nonempty),
            "empty": len(answers) - len(nonempty),
            "completion_pct": 100 * len(nonempty) / len(answers),
            "avg_words": mean(
                len(answer.split()) for answer in answers
            ),
            "code_block_answers": sum(
                "```" in answer for answer in answers
            ),
        }

    return summaries


def main():
    records = load_results()
    summaries = summarize_answers(records)

    print(f"Evaluation records: {len(records)}")
    print("\nAutomatic diagnostics")
    print("-" * 82)
    print(
        f"{'Variant':<16} {'Nonempty':>9} {'Empty':>7} "
        f"{'Complete %':>12} {'Avg words':>11} {'Code blocks':>12}"
    )
    print("-" * 82)

    for variant, stats in summaries.items():
        print(
            f"{variant:<16} "
            f"{stats['nonempty']:>9} "
            f"{stats['empty']:>7} "
            f"{stats['completion_pct']:>11.1f}% "
            f"{stats['avg_words']:>11.1f} "
            f"{stats['code_block_answers']:>12}"
        )

    report_path = Path("results/evaluation-scorecard.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)

    report = {
        "evaluation_file": str(INPUT_FILE),
        "question_count": len(records),
        "metrics_note": (
            "These are automatic output diagnostics, not measures "
            "of factual correctness or overall model quality."
        ),
        "variants": summaries,
    }

    with report_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)

    print(f"\nScorecard saved to: {report_path}")


if __name__ == "__main__":
    main()
