import os
import tempfile
from unittest.mock import patch

import pandas as pd

from src.analysis import (
    DELIMITERS,
    calculate_word_counts,
    save_word_counts,
    word_count,
)


class TestCalculateWordCounts:
    """Test the calculate_word_counts function."""
    
    def test_simple_word_count(self):
        """Test basic word counting functionality."""
        lines = ["hello world", "hello there", "world peace"]
        result = calculate_word_counts(lines)
        
        # Check that result is a DataFrame with correct columns
        assert isinstance(result, pd.DataFrame)
        assert list(result.columns) == ["word", "count"]
        
        # Check specific word counts
        word_counts = dict(zip(result["word"], result["count"]))
        assert word_counts["hello"] == 2
        assert word_counts["world"] == 2
        assert word_counts["there"] == 1
        assert word_counts["peace"] == 1
        
    def test_case_insensitive(self):
        """Test that word counting is case-insensitive."""
        lines = ["Hello HELLO hello", "World WORLD world"]
        result = calculate_word_counts(lines)
        
        word_counts = dict(zip(result["word"], result["count"]))
        assert word_counts["hello"] == 3
        assert word_counts["world"] == 3
        
    def test_delimiter_removal(self):
        """Test that delimiters are properly removed."""
        lines = ["hello,world!", "test.data?", "my-word(test)"]
        result = calculate_word_counts(lines)
        
        word_counts = dict(zip(result["word"], result["count"]))
        assert "hello" in word_counts
        assert "world" in word_counts
        assert "test" in word_counts
        assert "data" in word_counts
        assert "my" in word_counts
        assert "word" in word_counts
        
        # Check that no delimiters remain
        for word in result["word"]:
            for delimiter in ".,;:?$@^<>#%`!*-=()[]{}/'\"":
                assert delimiter not in word
                
    def test_min_length_filter(self):
        """Test that words shorter than min_length are filtered out."""
        lines = ["a bb ccc dddd"]
        result = calculate_word_counts(lines, min_length=3)
        
        word_counts = dict(zip(result["word"], result["count"]))
        assert "a" not in word_counts
        assert "bb" not in word_counts
        assert "ccc" in word_counts
        assert "dddd" in word_counts
        
    def test_empty_input(self):
        """Test behavior with empty input."""
        result = calculate_word_counts([])
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0
        assert list(result.columns) == ["word", "count"]
        
    def test_whitespace_handling(self):
        """Test proper handling of whitespace."""
        lines = ["  hello   world  ", "\t\ntest\r\n"]
        result = calculate_word_counts(lines)
        
        word_counts = dict(zip(result["word"], result["count"]))
        assert word_counts["hello"] == 1
        assert word_counts["world"] == 1
        assert word_counts["test"] == 1


class TestSaveWordCounts:
    """Test the save_word_counts function."""
    
    def test_save_to_csv(self):
        """Test saving DataFrame to CSV file."""
        df = pd.DataFrame({
            "word": ["hello", "world", "test"],
            "count": [3, 2, 1]
        })
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            tmp_path = tmp.name
            
        try:
            save_word_counts(tmp_path, df)
            
            # Read back the saved file
            loaded_df = pd.read_csv(tmp_path)
            pd.testing.assert_frame_equal(df, loaded_df)
            
        finally:
            os.unlink(tmp_path)


class TestWordCount:
    """Test the word_count function integration."""
    
    @patch('src.analysis.load_text')
    @patch('src.analysis.save_word_counts')
    def test_word_count_integration(self, mock_save, mock_load):
        """Test the complete word_count function."""
        # Mock the input
        mock_load.return_value = ["hello world", "hello there"]
        
        # Call the function
        word_count("input.txt", "output.csv", min_length=1)
        
        # Verify load_text was called correctly
        mock_load.assert_called_once_with("input.txt")
        
        # Verify save_word_counts was called
        assert mock_save.call_count == 1
        call_args = mock_save.call_args
        output_file = call_args[0][0]
        df = call_args[0][1]
        
        assert output_file == "output.csv"
        assert isinstance(df, pd.DataFrame)
        
        # Check the DataFrame content
        word_counts = dict(zip(df["word"], df["count"]))
        assert word_counts["hello"] == 2
        assert word_counts["world"] == 1
        assert word_counts["there"] == 1


class TestDelimiters:
    """Test the DELIMITERS constant."""
    
    def test_delimiters_constant(self):
        """Test that DELIMITERS constant is properly defined."""
        assert isinstance(DELIMITERS, str)
        # Check that it includes common delimiters
        expected_chars = ".,;:?$@^<>#%`!*-=()[]{}/'\"" 
        for char in expected_chars:
            assert char in DELIMITERS or f"\\{char}" in DELIMITERS