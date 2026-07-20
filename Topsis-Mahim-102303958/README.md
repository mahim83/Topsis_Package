# Topsis-Mahim-102303958

This package implements the **TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)** method in Python.  
It provides a command-line tool to rank alternatives based on multiple criteria, weights, and impacts.

---

## Installation

To install the package locally, go to the project directory and run:

```bash
pip install .
```

If installed from PyPI, use:

```bash
pip install Topsis-Mahim-102303958
```

---

## Usage

The package provides a command-line tool named `topsis`.

```bash
topsis <InputDataFile> <Weights> <Impacts> <OutputResultFileName>
```

### Example

```bash
topsis data.csv "1,1,1,1,1" "+,+,-,+,-" output-result.csv
```

---

## Input File Requirements

- Input file must be in CSV or XLSX format.
- The file must contain at least three columns.
- The first column is treated as an identifier.
- All columns from the second to the last must contain numeric values only.
- Weights must be numeric and comma-separated.
- Impacts must be comma-separated and should be either `+` or `-`.
- The number of weights, impacts, and criteria must be the same.

---

## Output

The output file contains two additional columns:
- **Topsis Score**
- **Rank** (Rank 1 indicates the best alternative)

---

## Author

Mahim Katiyar  
Roll Number: 102303958  
Email: mkatiyar_be23@thapar.edu
