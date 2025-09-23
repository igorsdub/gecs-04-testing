
#!/usr/bin/env python
"""
clean_book.py
----------------
Removes Project Gutenberg headers and footers from a plain-text file, saving the cleaned text to a new file.
Usage:
    python clean_book.py <input-file> <output-file>
"""


import sys

from src.dataset import load_text, save_text, strip_headers


def main():
    """
    Cleans a Project Gutenberg text file using src.dataset functions.
    """
    if len(sys.argv) < 3:
        print("Usage: python clean_book.py <input-file> <output-file>")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    text = load_text(input_file)
    cleaned_text = strip_headers(text)
    save_text(output_file, cleaned_text)

if __name__ == "__main__":
    main()
