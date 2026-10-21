import json
from pathlib import Path

REVIEW_FILE = Path("results/correctness-review.fresh.jsonl")
OUTPUT_FILE = Path("results/final-scorecard.json")

RATING_FIELDS = (
    "technical_correctness",
    "relevance",
    "practical_usefulness",
)
EXPECTED_MODELS = (
    "BASE MODEL",
    "DEVMATE V1",
    "DEVMATE V2",
    "DEVMATE V3",
)

if not REVIEW_FILE.exists():
    raise FileNotFoundError(f"Review file not found: {REVIEW_FILE}")

records = []
seen_ids = set()

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

        record_id = record.get("id")
        if record_id in seen_ids:
            raise ValueError(f"Duplicate question ID: {record_id}")
        seen_ids.add(record_id)

        scores_by_model = record.get("scores", {})
        for model in EXPECTED_MODELS:
            if model not in scores_by_model:
                raise ValueError(
                    f"Question {record_id}: missing scores for {model}"
                )

            scores = scores_by_model[model]

            for field in RATING_FIELDS:
                value = scores.get(field)
                if type(value) is not int or not 1 <= value <= 5:
                    raise ValueError(
                        f"Question {record_id}, {model}: "
                        f"{field} must be an integer from 1 to 5; "
                        f"got {value!r}"
                    )

            if type(scores.get("critical_error")) is not bool:
                raise ValueError(
                    f"Question {record_id}, {model}: "
                    "critical_error must be true or false"
                )

        records.append(record)

if not records:
    raise ValueError("No review records found.")

EXPECTED_QUESTION_COUNT = 21

if len(records) != EXPECTED_QUESTION_COUNT:
    raise ValueError(
        f"Expected {EXPECTED_QUESTION_COUNT} reviewed questions, "
        f"but found {len(records)}. Complete the review before scoring."
    )

expected_ids = set(range(1, EXPECTED_QUESTION_COUNT + 1))
if seen_ids != expected_ids:
    missing = sorted(expected_ids - seen_ids)
    unexpected = sorted(seen_ids - expected_ids)
    raise ValueError(
        f"Question IDs do not match the expected set. "
        f"Missing: {missing}; unexpected: {unexpected}"
    )

totals = {}

for model in EXPECTED_MODELS:
    model_scores = [record["scores"][model] for record in records]

    correctness = sum(s["technical_correctness"] for s in model_scores)
    relevance = sum(s["relevance"] for s in model_scores)
    usefulness = sum(s["practical_usefulness"] for s in model_scores)
    rated = len(model_scores)
    max_points = rated * len(RATING_FIELDS) * 5
    earned_points = correctness + relevance + usefulness

    totals[model] = {
        "answers": len(records),
        "rated_answers": rated,
        "correctness": correctness,
        "relevance": relevance,
        "usefulness": usefulness,
        "critical_errors": sum(
            s["critical_error"] for s in model_scores
        ),
        "earned_points": earned_points,
        "max_points": max_points,
        "score_percentage": round(
            100 * earned_points / max_points, 2
        ),
    }

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE.write_text(
    json.dumps(totals, indent=2),
    encoding="utf-8",
)

print(json.dumps(totals, indent=2))
print(f"\nValidated {len(records)} questions across "
      f"{len(EXPECTED_MODELS)} models.")
print(f"Saved scorecard to: {OUTPUT_FILE}")
