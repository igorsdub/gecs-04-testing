
import pytest
import pandas as pd
import matplotlib.pyplot as plt
from unittest.mock import patch
from src.plots import plot_word_counts



# ------------------- Fixtures -------------------

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "word": ["the", "and", "to", "of", "a", "in", "is", "it", "you", "that"],
        "count": [100, 80, 70, 60, 50, 40, 30, 25, 20, 15]
    })

# ------------------- Tests -------------------

@patch('matplotlib.pyplot.show')
@patch('matplotlib.pyplot.savefig')
def test_plot_word_counts_basic(mock_savefig, mock_show, sample_df):
    plot_word_counts(sample_df, limit=5)
    fig = plt.gcf()
    assert fig is not None
    ax = plt.gca()
    assert ax.get_title() == "Word Counts"
    assert ax.get_ylabel() == "Counts"
    assert ax.get_xlabel() == "Word"
    plt.close()

@patch('matplotlib.pyplot.show')
@patch('matplotlib.pyplot.savefig')
def test_plot_word_counts_limit(mock_savefig, mock_show, sample_df):
    limit = 3
    plot_word_counts(sample_df, limit=limit)
    ax = plt.gca()
    bars = ax.patches
    assert len(bars) == limit
    assert len(ax.get_xticks()) == limit
    plt.close()

@patch('matplotlib.pyplot.show')
@patch('matplotlib.pyplot.savefig')
def test_plot_word_counts_default_limit(mock_savefig, mock_show, sample_df):
    plot_word_counts(sample_df)
    ax = plt.gca()
    bars = ax.patches
    assert len(bars) == 10
    plt.close()

@patch('matplotlib.pyplot.show')
@patch('matplotlib.pyplot.savefig')
def test_plot_word_counts_limit_exceeds_data(mock_savefig, mock_show):
    small_df = pd.DataFrame({"word": ["hello", "world"], "count": [5, 3]})
    plot_word_counts(small_df, limit=10)
    ax = plt.gca()
    bars = ax.patches
    assert len(bars) == 2
    plt.close()

@patch('matplotlib.pyplot.show')
@patch('matplotlib.pyplot.savefig')
def test_plot_word_counts_empty_dataframe(mock_savefig, mock_show):
    empty_df = pd.DataFrame({"word": [], "count": []})
    plot_word_counts(empty_df, limit=10)
    ax = plt.gca()
    bars = ax.patches
    assert len(bars) == 0
    plt.close()

@patch('matplotlib.pyplot.show')
@patch('matplotlib.pyplot.savefig')
def test_plot_word_counts_figure_properties(mock_savefig, mock_show, sample_df):
    plot_word_counts(sample_df, limit=5)
    fig = plt.gcf()
    assert fig.get_size_inches()[0] == 6
    assert fig.get_size_inches()[1] == 4
    ax = plt.gca()
    assert ax.get_title() == "Word Counts"
    plt.close()

@patch('matplotlib.pyplot.show')
@patch('matplotlib.pyplot.savefig')
def test_plot_word_counts_bar_properties(mock_savefig, mock_show, sample_df):
    plot_word_counts(sample_df, limit=3)
    ax = plt.gca()
    bars = ax.patches
    assert len(bars) == 3
    assert len(bars) > 0
    plt.close()

@patch('matplotlib.pyplot.show')
@patch('matplotlib.pyplot.savefig')
def test_plot_word_counts_rotation(mock_savefig, mock_show, sample_df):
    plot_word_counts(sample_df, limit=5)
    ax = plt.gca()
    labels = ax.get_xticklabels()
    assert len(labels) > 0
    for label in labels:
        assert label.get_rotation() == 45
    plt.close()



def test_dataframe_compatibility():
    df1 = pd.DataFrame({"word": ["test", "data"], "count": [10, 5]})
    plot_word_counts(df1, limit=2)
    plt.close()
    df2 = pd.DataFrame({"count": [15, 8], "word": ["hello", "world"]})
    plot_word_counts(df2, limit=2)
    plt.close()