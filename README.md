# TOPSIS — Multi-Criteria Decision Analysis

Implements **TOPSIS** (Technique for Order Preference by Similarity to Ideal
Solution) in Python — a method that ranks alternatives across several weighted
criteria. The project ships in three forms:

1. **Standalone CLI script** — [`topsis_102303958.py`](topsis_102303958.py)
2. **Installable pip package** — [`Topsis-Mahim-102303958/`](Topsis-Mahim-102303958/)
3. **Streamlit web app** — [`streamlit_app.py`](streamlit_app.py) (deployable on [streamlit.io](https://streamlit.io))

---

## 1. Command-line script

```bash
python topsis_102303958.py <InputDataFile> <Weights> <Impacts> <OutputResultFileName>
```

Example:

```bash
python topsis_102303958.py data.csv "1,1,1,1,1" "+,+,-,+,-" result.csv
```

## 2. Pip package

```bash
cd Topsis-Mahim-102303958
pip install .
```

Then use the `topsis` console command:

```bash
topsis data.csv "1,1,1,1,1" "+,+,-,+,-" result.csv
```

## 3. Streamlit web app

Run locally:

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Opens at `http://localhost:8501`. Upload a file, enter weights and impacts,
view/download the ranked results, and optionally have them emailed.

### Deploy on Streamlit Community Cloud

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) → **Create app** →
   deploy from GitHub, main file `streamlit_app.py`.
3. (Optional, for email) In **Advanced settings → Secrets**, add:
   ```toml
   SENDER_EMAIL = "your_email@gmail.com"
   SENDER_PASSWORD = "your_gmail_app_password"
   ```
   Use a [Gmail App Password](https://myaccount.google.com/apppasswords), not
   your account password. See [`.streamlit/secrets.toml.example`](.streamlit/secrets.toml.example).

---

## Input file format

- CSV or XLSX with **at least 3 columns**.
- **First column** = the alternative name / identifier.
- **Remaining columns** = numeric criteria only.
- **Weights**: comma-separated numbers, one per criterion (e.g. `1,1,1,1,1`).
- **Impacts**: comma-separated `+` or `-`, one per criterion (e.g. `+,+,-,+,-`).
  Use `+` when a higher value is better, `-` when lower is better.
- The number of weights, impacts, and criteria must be equal.

## Output

Two columns are appended to the input data:

- **Topsis Score** — closeness to the ideal solution (0–1).
- **Rank** — 1 = best alternative.

---

## Author

**Mahim Katiyar** · Roll No: 102303958 · mkatiyar_be23@thapar.edu
