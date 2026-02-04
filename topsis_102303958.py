import sys
import os
import pandas as pd
import numpy as np


def validate_inputs():

    if len(sys.argv) != 5:
        print("Error: Incorrect number of parameters.")
        print("Usage: python topsis.py <InputDataFile> <Weights> <Impacts> <OutputResultFileName>")
        sys.exit(1)

    input_file, weights_str, impacts_str, output_file = sys.argv[1:]

    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    try:
        if input_file.endswith(".csv"):
            df = pd.read_csv(input_file)
        elif input_file.endswith(".xlsx"):
            df = pd.read_excel(input_file)
        else:
            print("Error: Input file must be .csv or .xlsx")
            sys.exit(1)
    except:
        print("Error: Unable to read input file.")
        sys.exit(1)

    if df.shape[1] < 3:
        print("Error: Input file must contain at least 3 columns.")
        sys.exit(1)

    numeric_data = df.iloc[:, 1:].apply(pd.to_numeric, errors="coerce")
    if numeric_data.isnull().values.any():
        print("Error: From 2nd to last columns must contain numeric values only.")
        sys.exit(1)

    try:
        weights = [float(w) for w in weights_str.split(",")]
        impacts = impacts_str.split(",")
    except:
        print("Error: Weights must be numeric and comma separated.")
        sys.exit(1)

    if not all(i in ["+", "-"] for i in impacts):
        print("Error: Impacts must be either '+' or '-'.")
        sys.exit(1)

    if len(weights) != df.shape[1] - 1 or len(impacts) != df.shape[1] - 1:
        print("Error: Number of weights, impacts and criteria must be the same.")
        sys.exit(1)

    return df, weights, impacts, output_file


def topsis_calculation(df, weights, impacts):

    data = df.iloc[:, 1:].values.astype(float)

    norm = data / np.sqrt((data ** 2).sum(axis=0))
    weighted = norm * weights

    best, worst = [], []

    for i in range(len(impacts)):
        if impacts[i] == "+":
            best.append(weighted[:, i].max())
            worst.append(weighted[:, i].min())
        else:
            best.append(weighted[:, i].min())
            worst.append(weighted[:, i].max())

    best = np.array(best)
    worst = np.array(worst)

    d_pos = np.sqrt(((weighted - best) ** 2).sum(axis=1))
    d_neg = np.sqrt(((weighted - worst) ** 2).sum(axis=1))

    return d_neg / (d_pos + d_neg)


def main():

    df, weights, impacts, output_file = validate_inputs()
    scores = topsis_calculation(df, weights, impacts)

    df["Topsis Score"] = scores
    df["Rank"] = df["Topsis Score"].rank(ascending=False, method="dense").astype(int)

    df.to_csv(output_file, index=False)
    print(f"TOPSIS analysis completed. Results saved in '{output_file}'.")


if __name__ == "__main__":
    main()
