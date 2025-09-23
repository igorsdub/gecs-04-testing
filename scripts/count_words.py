
#!/usr/bin/env python
"""
count_words.py
----------------
Counts word frequencies in a plain-text file and saves the results as a CSV file using pandas.
Usage:
    python count_words.py <input-file> <output-file> [min_length]
"""


import sys

from src.analysis import word_count


def main():
    """
    Counts word frequencies in a plain-text file and saves the results as a CSV file using pandas.
    Usage:
        python count_words.py <input-file> <output-file> [min_length]
    """
    if len(sys.argv) < 3:
        print("Usage: python count_words.py <input-file> <output-file> [min_length]")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    min_length = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    word_count(input_file, output_file, min_length)

if __name__ == "__main__":
    main()
