
import json
from pathlib import Path


def validate_dataset(path: Path) -> int:
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    count = 0

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                raise ValueError(f"Empty line at line {line_number}")

            try:
                example = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Invalid JSON at line {line_number}: {error}"
                ) from error

            messages = example.get("messages")

            if not isinstance(messages, list) or len(messages) < 2:
                raise ValueError(
                    f"Line {line_number}: expected at least two messages"
                )

            roles = [message.get("role") for message in messages]

            if roles[0] != "user" or roles[-1] != "assistant":
                raise ValueError(
                    f"Line {line_number}: conversation must start "
                    "with user and end with assistant"
                )

            for message in messages:
                if (
                    not isinstance(message.get("content"), str)
                    or not message["content"].strip()
                ):
                    raise ValueError(
                        f"Line {line_number}: message content must be non-empty"
                    )

            count += 1

    print(f"Dataset: {path}")
    print(f"Validation passed: {count} examples")
    return count


if __name__ == "__main__":
    validate_dataset(Path("data/train.jsonl"))
    validate_dataset(Path("data/eval.jsonl"))
