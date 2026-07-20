# TOPSIS — Multi-Criteria Decision Analysis

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![PyPI](https://img.shields.io/badge/PyPI-Topsis--Mahim--102303958-3775A9?logo=pypi&logoColor=white)](https://pypi.org/project/Topsis-Mahim-102303958/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-Academic-green)](Topsis-Mahim-102303958/LICENSE.txt)

An implementation of **TOPSIS** (*Technique for Order Preference by Similarity to
Ideal Solution*) — a multi-criteria decision-making method that ranks a set of
alternatives by how close each one is to the ideal solution and how far it is from
the worst one.

**Live app:** https://topsispackage-mahim.streamlit.app

The project ships in three forms, all sharing the same core algorithm:

| # | Form | Entry point | Best for |
|---|------|-------------|----------|
| 1 | Command-line script | [`topsis_102303958.py`](topsis_102303958.py) | Quick one-off runs |
| 2 | Installable pip package | [`Topsis-Mahim-102303958/`](Topsis-Mahim-102303958/) | Reuse via the `topsis` command |
| 3 | Streamlit web app | [`streamlit_app.py`](streamlit_app.py) | Interactive UI, deployed online |

---

## Features

- Accepts **CSV or XLSX** input
- Full input **validation** (column count, numeric checks, matching weights/impacts)
- Interactive web UI: upload, configure, view a ranked table and chart, download CSV
- Zero-config deployment on **Streamlit Community Cloud**

---

## How TOPSIS works

1. **Normalize** the decision matrix (vector normalization).
2. **Weight** each normalized column by its criterion weight.
3. Determine the **ideal best** and **ideal worst** value per criterion
   (depending on whether the impact is `+` or `-`).
4. Compute each alternative's **Euclidean distance** to the ideal best (`d+`) and
   ideal worst (`d-`).
5. **Score** = `d- / (d+ + d-)` — higher is better. Rank by score.

---

## Usage

### 1. Command-line script

```bash
python topsis_102303958.py <InputDataFile> <Weights> <Impacts> <OutputResultFileName>
```

```bash
python topsis_102303958.py data.csv "1,1,1,1,1" "+,+,-,+,-" result.csv
```

### 2. Pip package (install on your own device)

The package is published on **PyPI**, so anyone can install it on any machine
(Windows, macOS, or Linux) with Python 3.7+ and pip. No need to clone this repo.

**Prerequisite:** Python 3.7 or newer with `pip`. Check with `python --version` and
`pip --version`.

**Install from PyPI:**

```bash
pip install Topsis-Mahim-102303958
```

This installs a `topsis` command that is available system-wide. Run it from any
folder that contains your input file:

```bash
topsis <InputDataFile> <Weights> <Impacts> <OutputResultFileName>
```

```bash
topsis data.csv "1,1,1,1,1" "+,+,-,+,-" result.csv
```

**Upgrade to the latest version:**

```bash
pip install --upgrade Topsis-Mahim-102303958
```

> **Tip:** if the `topsis` command isn't found after installing, make sure your
> Python `Scripts`/`bin` directory is on your `PATH`, or run it via
> `python -m topsis_mahim_102303958.topsis <args>`.

### 3. Streamlit web app (run locally)

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Opens at `http://localhost:8501`. Upload a file, set weights and impacts, then
view and download the ranked results.

---

## Deployment

The app is already deployed on Streamlit Community Cloud and runs live at
**https://topsispackage-mahim.streamlit.app**. Every push to `main` redeploys it
automatically — `requirements.txt` and `.streamlit/config.toml` handle the setup.

---

## Input format

- CSV or XLSX with **at least 3 columns**.
- **First column** — the alternative name / identifier.
- **Remaining columns** — numeric criteria only.
- **Weights** — comma-separated numbers, one per criterion (e.g. `1,1,1,1,1`).
- **Impacts** — comma-separated `+` or `-`, one per criterion (e.g. `+,+,-,+,-`).
  Use `+` when a higher value is better, `-` when lower is better.
- The number of weights, impacts, and criteria must be equal.

## Output

Two columns are appended to your data:

- **Topsis Score** — closeness to the ideal solution (0–1).
- **Rank** — `1` = best alternative.

Example (`data.csv` with weights `1,1,1,1,1` and impacts `+,+,-,+,-`):

| Fund Name | Topsis Score | Rank |
|-----------|-------------:|:----:|
| M7        | 0.7097       | 1    |
| M4        | 0.6952       | 2    |
| M5        | 0.4776       | 3    |
| …         | …            | …    |
| M8        | 0.3928       | 8    |

---

## Project structure

```
.
├── streamlit_app.py            # Streamlit web app (deployed)
├── requirements.txt            # Web-app dependencies
├── .streamlit/config.toml      # Theme and upload settings
├── topsis_102303958.py         # Standalone CLI script
├── data.csv                    # Sample input
├── topsis_result.csv           # Sample output
└── Topsis-Mahim-102303958/     # Installable pip package
    ├── setup.py
    ├── README.md
    ├── LICENSE.txt
    └── topsis_mahim_102303958/
        ├── __init__.py
        └── topsis.py
```

---

## License

Developed for academic and educational purposes — see
[`LICENSE.txt`](Topsis-Mahim-102303958/LICENSE.txt).

## Author

**Mahim Katiyar** · Roll No. 102303958 · mkatiyar_be23@thapar.edu
