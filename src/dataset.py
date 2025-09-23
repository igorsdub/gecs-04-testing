from pathlib import Path
from typing import List

from loguru import logger
from tqdm import tqdm
import typer

from src.config import PROCESSED_DATA_DIR, RAW_DATA_DIR


def load_text(filename: str) -> List[str]:
    """
    Load lines from a plain-text file and return them as a list, with trailing newlines stripped.

    Args:
        filename (str): Path to the input text file.

    Returns:
        List[str]: List of lines from the file.
    """
    with open(filename, encoding="utf-8") as f:
        return f.read().splitlines()


def save_text(filename: str, text: str) -> None:
    """
    Save a string to a plain-text file.

    Args:
        filename (str): Path to the output text file.
        text (str): Text to write to the file.
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)


def strip_headers(text: List[str]) -> str:
    """
    Strip Project Gutenberg headers and footers from the text.

    Args:
        text (List[str]): List of lines from the file.

    Returns:
        str: Cleaned text with headers/footers removed.
    """
    GUTENBERG_TEXT = "PROJECT GUTENBERG EBOOK "
    in_text = False
    output: List[str] = []

    for line in text:
        if GUTENBERG_TEXT in line:
            if not in_text:
                in_text = True
            else:
                break
        elif in_text:
            output.append(line)
    return "\n".join(output).strip()


app = typer.Typer()


@app.command()
def main(
    input_path: Path = RAW_DATA_DIR / "book.txt",
    output_path: Path = PROCESSED_DATA_DIR / "book.txt",
):
    """
    Cleans a Project Gutenberg text file by stripping headers and footers.
    """
    logger.info(f"Loading text from {input_path}")
    text = load_text(str(input_path))
    cleaned_text = strip_headers(text)
    logger.info(f"Saving cleaned text to {output_path}")
    save_text(str(output_path), cleaned_text)
    logger.success("Gutenberg text cleaned and saved.")


@app.command()
def demo(
    input_path: Path = RAW_DATA_DIR / "dataset.csv",
    output_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
):
    """
    Example dataset processing function.
    """
    logger.info("Processing dataset...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Processing dataset complete.")


if __name__ == "__main__":
    app()
