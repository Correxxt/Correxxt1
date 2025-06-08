# Correxxt1

Correxxt1 is a simple command-line spell checking tool built with Python.
It uses the [`pyspellchecker`](https://pyspellchecker.readthedocs.io/) library
to detect misspelled words and suggest corrections.

## Installation

Install the Python dependencies with pip:

```bash
pip install pyspellchecker
```

## Usage

You can check text passed as arguments, read from a file, or via standard input.

```bash
# Check text arguments
python correxxt.py This is a smple txt

# Check a file
python correxxt.py -f path/to/file.txt

# Or via stdin
cat file.txt | python correxxt.py
```

The tool will output each misspelled word along with the most likely
correction and a list of candidate suggestions.
