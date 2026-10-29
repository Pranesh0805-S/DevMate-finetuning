import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "review_cli.py"
SPEC = importlib.util.spec_from_file_location("review_cli", MODULE_PATH)
review_cli = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(review_cli)


def valid_record():
    return {
        "id": 1,
        "question": "Explain a Python list.",
        "answers": {
            model: "A list is an ordered collection."
            for model in review_cli.VARIANTS
        },
        "scores": {
            model: {
                "technical_correctness": None,
                "relevance": None,
                "practical_usefulness": None,
                "critical_error": None,
            }
            for model in review_cli.VARIANTS
        },
        "review_notes": {model: "" for model in review_cli.VARIANTS},
    }


def test_valid_record_passes_validation():
    review_cli.validate_record(valid_record(), 1)


@pytest.mark.parametrize("value", [0, 6, -1, True, 2.5, "4"])
def test_invalid_rating_is_rejected(value):
    record = valid_record()
    record["scores"]["BASE MODEL"]["relevance"] = value

    with pytest.raises(ValueError, match="relevance"):
        review_cli.validate_record(record, 1)


def test_invalid_critical_error_type_is_rejected():
    record = valid_record()
    record["scores"]["BASE MODEL"]["critical_error"] = "no"

    with pytest.raises(ValueError, match="critical_error"):
        review_cli.validate_record(record, 1)


def test_missing_model_is_rejected():
    record = valid_record()
    del record["answers"]["DEVMATE V3"]

    with pytest.raises(ValueError, match="Missing model data"):
        review_cli.validate_record(record, 1)


def test_incomplete_score_is_not_complete():
    record = valid_record()

    assert not review_cli.is_complete(record, "BASE MODEL")

    record["scores"]["BASE MODEL"] = {
        "technical_correctness": 4,
        "relevance": 4,
        "practical_usefulness": 3,
        "critical_error": False,
    }

    assert review_cli.is_complete(record, "BASE MODEL")
