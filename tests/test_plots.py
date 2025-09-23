from unittest.mock import patch

import matplotlib.pyplot as plt
import pandas as pd

from src.plots import plot_word_counts


class TestPlotWordCounts:
    """Test the plot_word_counts function."""
    
    def setup_method(self):
        """Set up test data for each test."""
        self.sample_df = pd.DataFrame({
            "word": ["the", "and", "to", "of", "a", "in", "is", "it", "you", "that"],
            "count": [100, 80, 70, 60, 50, 40, 30, 25, 20, 15]
        })
        
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.savefig')
    def test_plot_word_counts_basic(self, mock_savefig, mock_show):
        """Test basic plotting functionality."""
        plot_word_counts(self.sample_df, limit=5)
        
        # Check that a figure was created
        fig = plt.gcf()
        assert fig is not None
        
        # Check that axes were configured
        ax = plt.gca()
        assert ax.get_title() == "Word Counts"
        assert ax.get_ylabel() == "Counts"
        assert ax.get_xlabel() == "Word"
        
        plt.close()
        
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.savefig')
    def test_plot_word_counts_limit(self, mock_savefig, mock_show):
        """Test that limit parameter works correctly."""
        limit = 3
        plot_word_counts(self.sample_df, limit=limit)
        
        ax = plt.gca()
        # Check that only 'limit' number of bars are plotted
        bars = ax.patches
        assert len(bars) == limit
        
        # Check the number of ticks
        assert len(ax.get_xticks()) == limit
        
        plt.close()
        
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.savefig')
    def test_plot_word_counts_default_limit(self, mock_savefig, mock_show):
        """Test default limit of 10."""
        plot_word_counts(self.sample_df)  # Uses default limit=10
        
        ax = plt.gca()
        bars = ax.patches
        # Sample data has exactly 10 words, so should plot all
        assert len(bars) == 10
        
        plt.close()
        
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.savefig')
    def test_plot_word_counts_limit_exceeds_data(self, mock_savefig, mock_show):
        """Test when limit exceeds available data."""
        small_df = pd.DataFrame({
            "word": ["hello", "world"],
            "count": [5, 3]
        })
        
        plot_word_counts(small_df, limit=10)  # Limit > data size
        
        ax = plt.gca()
        bars = ax.patches
        # Should only plot available data (2 bars)
        assert len(bars) == 2
        
        plt.close()
        
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.savefig')
    def test_plot_word_counts_empty_dataframe(self, mock_savefig, mock_show):
        """Test behavior with empty DataFrame."""
        empty_df = pd.DataFrame({"word": [], "count": []})
        
        plot_word_counts(empty_df, limit=10)
        
        ax = plt.gca()
        bars = ax.patches
        # Should have no bars
        assert len(bars) == 0
        
        plt.close()
        
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.savefig')
    def test_plot_word_counts_figure_properties(self, mock_savefig, mock_show):
        """Test that figure properties are set correctly."""
        plot_word_counts(self.sample_df, limit=5)
        
        fig = plt.gcf()
        # Check figure size
        assert fig.get_size_inches()[0] == 6
        assert fig.get_size_inches()[1] == 4
        
        ax = plt.gca()
        # Check that tight_layout was applied (this affects the subplot params)
        # We can't directly test tight_layout, but we can check basic properties
        assert ax.get_title() == "Word Counts"
        
        plt.close()
        
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.savefig')
    def test_plot_word_counts_bar_properties(self, mock_savefig, mock_show):
        """Test bar chart properties."""
        plot_word_counts(self.sample_df, limit=3)
        
        ax = plt.gca()
        bars = ax.patches
        
        # Check bar count
        assert len(bars) == 3
        
        # Check that bars exist
        assert len(bars) > 0
            
        plt.close()
        
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.savefig')
    def test_plot_word_counts_rotation(self, mock_savefig, mock_show):
        """Test that x-axis labels are rotated correctly."""
        plot_word_counts(self.sample_df, limit=5)
        
        ax = plt.gca()
        # Check x-axis label rotation
        labels = ax.get_xticklabels()
        assert len(labels) > 0
        
        # Check that rotation was applied (basic check)
        for label in labels:
            # Rotation should be 45 degrees
            assert label.get_rotation() == 45
            
        plt.close()


class TestPlotIntegration:
    """Test integration with pandas DataFrame."""
    
    def test_dataframe_compatibility(self):
        """Test that function works with different DataFrame structures."""
        # Test with standard DataFrame
        df1 = pd.DataFrame({
            "word": ["test", "data"],
            "count": [10, 5]
        })
        
        # Should not raise any exceptions
        plot_word_counts(df1, limit=2)
        plt.close()
        
        # Test with different column order (should still work)
        df2 = pd.DataFrame({
            "count": [15, 8],
            "word": ["hello", "world"]
        })
        
        plot_word_counts(df2, limit=2)
        plt.close()