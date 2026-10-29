
import pytest

from devmate import DevMate


def test_dev_mate_import():
    assert DevMate is not None


def test_empty_prompt_is_rejected():
    model = DevMate.__new__(DevMate)

    with pytest.raises(ValueError, match="prompt must be a non-empty string"):
        model.generate("")


def test_whitespace_prompt_is_rejected():
    model = DevMate.__new__(DevMate)

    with pytest.raises(ValueError, match="prompt must be a non-empty string"):
        model.generate("   ")


def test_non_string_prompt_is_rejected():
    model = DevMate.__new__(DevMate)

    with pytest.raises(ValueError, match="prompt must be a non-empty string"):
        model.generate(None)


def test_zero_max_new_tokens_is_rejected():
    with pytest.raises(ValueError, match="max_new_tokens must be at least 1"):
        DevMate(max_new_tokens=0)
