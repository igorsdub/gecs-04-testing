import pandas as pd
import pytest

from src.analysis import (
    DELIMITERS,
    calculate_word_counts,
    save_word_counts,
    word_count,
)

# ------------------- Fixtures -------------------


@pytest.fixture
def simple_lines():
    return ["hello world", "hello there", "world peace"]


@pytest.fixture
def case_lines():
    return ["Hello HELLO hello", "World WORLD world"]


@pytest.fixture
def delimiter_lines():
    return ["hello,world!", "test.data?", "my-word(test)"]


@pytest.fixture
def min_length_lines():
    return ["a bb ccc dddd"]


@pytest.fixture
def whitespace_lines():
    return ["  hello   world  ", "\t\ntest\r\n"]


# ------------------- Tests -------------------


def test_simple_word_count(simple_lines):
    result = calculate_word_counts(simple_lines)
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ["word", "count"]
    word_counts = dict(zip(result["word"], result["count"]))
    assert word_counts["hello"] == 2
    assert word_counts["world"] == 2
    assert word_counts["there"] == 1
    assert word_counts["peace"] == 1


def test_case_insensitive(case_lines):
    result = calculate_word_counts(case_lines)
    word_counts = dict(zip(result["word"], result["count"]))
    assert word_counts["hello"] == 3
    assert word_counts["world"] == 3


def test_delimiter_removal(delimiter_lines):
    result = calculate_word_counts(delimiter_lines)
    word_counts = dict(zip(result["word"], result["count"]))
    assert "hello" in word_counts
    assert "world" in word_counts
    assert "test" in word_counts
    assert "data" in word_counts
    assert "my" in word_counts
    assert "word" in word_counts
    for word in result["word"]:
        for delimiter in ".,;:?$@^<>#%`!*-=()[]{}/'\"":
            assert delimiter not in word


def test_min_length_filter(min_length_lines):
    result = calculate_word_counts(min_length_lines, min_length=3)
    word_counts = dict(zip(result["word"], result["count"]))
    assert "a" not in word_counts
    assert "bb" not in word_counts
    assert "ccc" in word_counts
    assert "dddd" in word_counts


def test_empty_input():
    result = calculate_word_counts([])
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 0
    assert list(result.columns) == ["word", "count"]


def test_whitespace_handling(whitespace_lines):
    result = calculate_word_counts(whitespace_lines)
    word_counts = dict(zip(result["word"], result["count"]))
    assert word_counts["hello"] == 1
    assert word_counts["world"] == 1
    assert word_counts["test"] == 1


@pytest.fixture
def wordcount_df():
    return pd.DataFrame({"word": ["hello", "world", "test"], "count": [3, 2, 1]})


def test_save_to_csv(wordcount_df, tmp_path):
    file_path = tmp_path / "counts.csv"
    save_word_counts(str(file_path), wordcount_df)
    loaded_df = pd.read_csv(file_path)
    pd.testing.assert_frame_equal(wordcount_df, loaded_df)


def test_word_count_integration(mocker):
    mock_load = mocker.patch("src.analysis.load_text", return_value=["hello world", "hello there"])
    mock_save = mocker.patch("src.analysis.save_word_counts")
    word_count("input.txt", "output.csv", min_length=1)
    mock_load.assert_called_once_with("input.txt")
    assert mock_save.call_count == 1
    output_file = mock_save.call_args[0][0]
    df = mock_save.call_args[0][1]
    assert output_file == "output.csv"
    assert isinstance(df, pd.DataFrame)
    word_counts = dict(zip(df["word"], df["count"]))
    assert word_counts["hello"] == 2
    assert word_counts["world"] == 1
    assert word_counts["there"] == 1


def test_delimiters_constant():
    assert isinstance(DELIMITERS, str)
    expected_chars = ".,;:?$@^<>#%`!*-=()[]{}/'\""
    for char in expected_chars:
        assert char in DELIMITERS or f"\\{char}" in DELIMITERS
