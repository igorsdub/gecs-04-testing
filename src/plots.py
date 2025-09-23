from pathlib import Path

from loguru import logger
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
import typer

from src.config import ANALYZED_DIR, RESULT_DIR

app = typer.Typer()


def plot_word_counts(df: pd.DataFrame, limit: int = 10) -> None:
    """
    Plot a histogram of word counts from a pandas DataFrame.

    Args:
        df (pd.DataFrame): DataFrame with columns 'word' and 'count'.
        limit (int): Number of top words to plot.
    """
    limited_df = df.head(limit)
    position = range(len(limited_df))
    plt.figure(figsize=(6, 4))
    plt.bar(position, limited_df["count"], width=0.8)
    plt.xticks(position, limited_df["word"].tolist(), rotation=45, ha="right")
    plt.title("Word Counts")
    plt.ylabel("Counts")
    plt.xlabel("Word")
    plt.tight_layout()


@app.command()
def main(
    input_path: Path = ANALYZED_DIR / "word_counts.csv",
    output_path: Path = RESULT_DIR / "histogram.pdf",
    limit: int = 10,
):
    """
    Plot a histogram of word counts from a CSV file and save or show the plot.
    """
    logger.info(f"Reading word counts from {input_path}")
    df = pd.read_csv(input_path)
    plot_word_counts(df, limit)
    if str(output_path) == "show":
        plt.show()
        logger.success("Plot displayed.")
    else:
        plt.savefig(output_path)
        logger.success(f"Plot saved to {output_path}")


@app.command()
def demo(
    input_path: Path = ANALYZED_DIR / "dataset.csv",
    output_path: Path = RESULT_DIR / "plot.png",
):
    """
    Example plot generation function.
    """
    logger.info("Generating plot from data...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Plot generation complete.")


if __name__ == "__main__":
    app()
