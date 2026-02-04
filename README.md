# Topsis_Assignment


This project implements the **TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)** method using Python.

The project is developed in **three parts**:
1. Learning the mathematics of TOPSIS  
2. Implementing TOPSIS as a command-line Python program and publishing it as a PyPI package  
3. Designing a web-based TOPSIS service with email-based result delivery  

TOPSIS is a widely used **Multi-Criteria Decision Making (MCDM)** technique that ranks alternatives based on their distance from the ideal best and ideal worst solutions.

---

## Part I – Learning & Implementing TOPSIS

### Learning the Mathematics of TOPSIS

The TOPSIS methodology involves the following steps:
- Construction of the decision matrix  
- Normalization of the decision matrix  
- Creation of weighted normalized matrix  
- Determination of ideal best and ideal worst solutions  
- Distance calculation from ideal solutions  
- Computation of TOPSIS score and ranking  

---

### Command Line Implementation (Standalone Script)

The TOPSIS algorithm is implemented as a **command-line Python program**.

#### Command Format

```bash
python <program.py> <InputDataFile> <Weights> <Impacts> <OutputResultFileName>
```



## Part 2 – Develop a python package and upload it to the pypi.org

## Topsis-Mahim-102303958

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
python -m pip install Topsis-Mahim-102303958
```

---

## Usage

The package provides a command-line tool named `topsis`.

```bash
topsis <InputDataFile> <Weights> <Impacts> <OutputResultFileName>
```

### Example

```bash
python -m topsis_mahim_102303958.topsis data.csv "1,1,1,1,1" "+,+,-,+,-" output.csv
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




## Part III – Web Service for TOPSIS

### Web-Based TOPSIS Service

In this part, a **web service** is developed to provide the TOPSIS functionality through an online interface.  
The service allows users to upload data and receive ranked results via **email**, making TOPSIS accessible without using the command line.

---

### User Inputs

The user is required to provide the following inputs through the web interface:

- Input data file (CSV format)
- Weights (comma-separated values)
- Impacts (comma-separated values)
- Email ID

---

### Validation Rules

The web service performs the following validations before processing the request:

- Number of **weights must be equal to number of impacts**
- Weights must be **numeric and comma-separated**
- Impacts must be **comma-separated** and should be either:
  - `+` (beneficial criteria)
  - `-` (non-beneficial criteria)
- Input file must contain **at least three columns**
- All columns from **second to last** must contain **numeric values**
- Email ID must be in a **valid format**

If any validation fails, the user is notified with an appropriate error message.

---

### Processing Flow

- User uploads the input file and enters weights, impacts, and email ID
- Input validations are performed
- TOPSIS algorithm is applied on the uploaded data
- Result file is generated in CSV format
- TOPSIS score and rank are added to the result file

---

### Output Delivery

- The final TOPSIS result file is sent to the **user’s email ID** as an attachment
- This enables users to receive results without downloading them manually from the website

---

### Assumptions

- Internet connectivity is available
- Email service credentials are properly configured on the server
- Uploaded files are small to medium-sized CSV files

---

### Future Enhancements

- REST API support
- Authentication and user login
- Support for large datasets
- Result visualization on the web interface
- History of previously processed files

## Author

Mahim Katiyar  
Roll Number: 102303958  
Email: mkatiyar_be23@thapar.edu


