from pathlib import Path
import re
from typing import List

from loguru import logger
import pandas as pd
from tqdm import tqdm
import typer

from src.config import ANALYZED_DIR, PROCESSED_DATA_DIR
from src.dataset import load_text

app = typer.Typer()



DELIMITERS = r"[\.\,;:\?\$@\^<>#%`!\*\-=\(\)\[\]\{\}/\\\"']"

def save_word_counts(filename: str, df: pd.DataFrame) -> None:
    """
    Save a DataFrame of word counts to a CSV file.
    """
    df.to_csv(filename, index=False)

def calculate_word_counts(lines: List[str], min_length: int = 1) -> pd.DataFrame:
    """
    Given a list of strings, parse each string and create a DataFrame of word counts.
    DELIMITERS are removed before the string is parsed. The function is case-insensitive
    and words in the dictionary are in lower-case.
    """
    words = []
    for line in lines:
        # Remove delimiters and split into words
        clean_line = re.sub(DELIMITERS, " ", line)
        words.extend([w.lower().strip() for w in clean_line.split() if len(w) >= min_length])
    word_series = pd.Series(words)
    counts = word_series.value_counts().reset_index()
    counts.columns = ["word", "count"]
    return counts

def word_count(input_file: str, output_file: str, min_length: int = 1) -> None:
    """
    Load a file, calculate the frequencies of each word in the file and
    save in a new file the words, counts and percentages of the total in
    descending order. Only words whose length is >= min_length are included.
    """
    lines = load_text(input_file)
    df = calculate_word_counts(lines, min_length)
    save_word_counts(output_file, df)



@app.command()
def main(
    input_path: Path = PROCESSED_DATA_DIR / "book.txt",
    output_path: Path = ANALYZED_DIR / "word_counts.csv",
    min_length: int = 1,
):
    """
    Count word frequencies in a plain-text file and save the results as a CSV file.
    """
    logger.info(f"Counting words in {input_path} (min_length={min_length})")
    word_count(str(input_path), str(output_path), min_length)
    logger.success(f"Word counts saved to {output_path}")

@app.command()
def demo(
    input_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    output_path: Path = ANALYZED_DIR / "features.csv",
):
    """
    Example feature generation function.
    """
    logger.info("Generating features from dataset...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Features generation complete.")


if __name__ == "__main__":
    app()
