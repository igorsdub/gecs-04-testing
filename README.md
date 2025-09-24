# Good Enough Computing in Science (GECS) | Session 3 | Tutorial 4 | Testing

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

A tutorial on code testing using pytest.

## Project Organization

```text
├── LICENSE             <- MIT open-source licencense
├── README.md           <- Project description, structure and refernces
│
├── data                
│   ├── analyzed        <- The final, canonical data sets for modeling
│   ├── processed       <- The processed texts
│   └── raw             <- The original book texts downloaded from The Project Gutenberg
│
├── notebooks           <- Jupyter notebooks
│
├── pyproject.toml      <- Pyhton project configuration file with package metadata
│
├── results             <- Generated histogram of word counts
│
├── tests               <- Tests for the source code
├   ├── test_clean_book.py
│   ├── test_count_words.py
│   └── test_plot_counts.py
│
├── scripts
├   ├── clean_book.py   <- Clean raw book text
│   ├── count_words.py  <- Count words in a cleaned book text
│   └── plot_counts.py  <- Plot a word count histogram
│
└── src
    ├── __init__.py     <- Tells Python that src/ is a module
    ├── config.py       <- Stores useful variables and configuration
    ├── dataset.py      <- Processes raw book text
    ├── analysis.py     <- Analyze processed text
    └── plots.py        <- Generates plots from the analyzed data
```

## Installation

Use the package manager [pixi](https://pixi.sh) to install a virtual enviroemnet for this project.

```bash
pixi install
```

## Usage

To execute the project pipeline via command-line interface (CLI), first active the virtual environement shell

```bash
pixi shell
```

Next, run the following commands in the given order:

```bash
python src/dataset.py main
python src/analysis.py main
python src/plots.py main
```

The word count histogram, `histogram.pdf`, can be found in `results` folder.

For running each of the steps using [Pixi tasks](https://pixi.sh/latest/workspace/advanced_tasks) execute the following:

```bash
pixi run process
pixi run analyze
pixi run plot
```

In order to run all of these tasks together, use a convieniet task that combines the above together:

```bash
pixi run all
```

You might wish to clean the folders before you do so with

```bash
pixi run clean
```

To see how the pipeline has been refactored, you can run the same commands as in the Tutorial 1:

```bash
python src/dataset.py data/raw/book.txt data/processed/book.txt
python count_words.py data/processed/book.txt analyzed/word_count.csv
python plot_histogram.py analyzed/word_count.csv results/histogram.pdf
```

The commands above are scripted versions of src layout run code using [Typer](https://typer.tiangolo.com/).

`notebooks/0.01-igorsdub-generate_book_word_count_histogram.ipynb` contains the whole pipeline from start to finish but without any file saving. `## Local library import` section very well illustractes the power of src layout. You don't need to edit code in the notebook or relaoed it upon every edit of the module.

## Tests

Run tests on the source code to verify correctness of the method. 

```bash
pytest --cov
```

`pytest` will automatically find files that start with `test_` across the repository. `--cov` generates a coverage report that shows how much of the source code has been covered by the tests.

Alternatively, you can run a Pixi task:

```bash
pixi run test
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## References

1. [AY2025_T1_GECS_Session01_VirtualEnvAndProjectTemplate](https://docs.google.com/presentation/d/1ibLj6rD1ChZBS5Bze_0ej7ZD4ASjWr5mLCBI7scfi48/edit?usp=sharing)
2. [Make a README](https://www.makeareadme.com/)
3. [Pixi](https://pixi.sh)
4. [The Project Gutenberg](https://www.gutenberg.org/)
5. [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/)
