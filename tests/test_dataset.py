import json
from pathlib import Path

import pytest

from src.prepare_dataset import validate_dataset


def write_jsonl(path: Path, examples: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(example) + "\n" for example in examples),
        encoding="utf-8",
    )


def valid_example() -> dict:
    return {
        "messages": [
            {"role": "user", "content": "What is a Python function?"},
            {
                "role": "assistant",
                "content": "A function is reusable code defined with def.",
            },
        ]
    }


def test_valid_dataset_returns_example_count(tmp_path: Path) -> None:
    path = tmp_path / "valid.jsonl"
    write_jsonl(path, [valid_example(), valid_example()])

    assert validate_dataset(path) == 2


def test_missing_dataset_raises_error(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        validate_dataset(tmp_path / "missing.jsonl")


def test_invalid_json_raises_error(tmp_path: Path) -> None:
    path = tmp_path / "invalid.jsonl"
    path.write_text("{invalid json}\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid JSON at line 1"):
        validate_dataset(path)


def test_empty_line_raises_error(tmp_path: Path) -> None:
    path = tmp_path / "empty-line.jsonl"
    path.write_text("\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Empty line at line 1"):
        validate_dataset(path)


def test_missing_messages_raises_error(tmp_path: Path) -> None:
    path = tmp_path / "missing-messages.jsonl"
    path.write_text(json.dumps({"text": "hello"}) + "\n", encoding="utf-8")

    with pytest.raises(ValueError, match="expected at least two messages"):
        validate_dataset(path)


def test_wrong_conversation_roles_raise_error(tmp_path: Path) -> None:
    example = valid_example()
    example["messages"][0]["role"] = "assistant"
    path = tmp_path / "wrong-roles.jsonl"
    write_jsonl(path, [example])

    with pytest.raises(ValueError, match="must start with user"):
        validate_dataset(path)


def test_empty_message_content_raises_error(tmp_path: Path) -> None:
    example = valid_example()
    example["messages"][1]["content"] = "   "
    path = tmp_path / "empty-content.jsonl"
    write_jsonl(path, [example])

    with pytest.raises(ValueError, match="content must be non-empty"):
        validate_dataset(path)
