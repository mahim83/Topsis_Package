"""
TOPSIS Analyzer — Streamlit app
===============================

Upload a CSV/XLSX file, provide weights and impacts, and get the alternatives
ranked using the TOPSIS (Technique for Order Preference by Similarity to Ideal
Solution) method. Results are shown on screen (table + chart) and can be
downloaded as CSV.

Deploys on Streamlit Community Cloud (https://streamlit.io) with no server
configuration.

Author: Mahim Katiyar (Roll: 102303958)
"""

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

BAR_COLOR = "#4C78A8"  # single accessible hue — reads on light and dark surfaces


# --------------------------- TOPSIS core ---------------------------
def validate(df, weights, impacts):
    """Return an error message string, or None if the inputs are valid."""
    if df.shape[1] < 3:
        return "Input file must contain at least 3 columns (1 identifier + 2 criteria)."

    numeric = df.iloc[:, 1:].apply(pd.to_numeric, errors="coerce")
    if numeric.isnull().values.any():
        return "From the 2nd column onward, all values must be numeric."

    n_criteria = df.shape[1] - 1
    if len(weights) != n_criteria:
        return f"Expected {n_criteria} weights (one per criterion), got {len(weights)}."
    if len(impacts) != n_criteria:
        return f"Expected {n_criteria} impacts (one per criterion), got {len(impacts)}."
    if not all(i in ("+", "-") for i in impacts):
        return "Impacts must be '+' or '-', comma-separated."
    return None


def compute_topsis(df, weights, impacts):
    """Return a copy of df with 'Topsis Score' and 'Rank' columns appended."""
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

    best, worst = np.array(best), np.array(worst)

    d_pos = np.sqrt(((weighted - best) ** 2).sum(axis=1))
    d_neg = np.sqrt(((weighted - worst) ** 2).sum(axis=1))
    score = d_neg / (d_pos + d_neg)

    result = df.copy()
    result["Topsis Score"] = score
    result["Rank"] = result["Topsis Score"].rank(ascending=False, method="dense").astype(int)
    return result


def ranking_chart(result):
    """Sorted horizontal bar chart of Topsis scores (magnitude, single hue)."""
    label_col = result.columns[0]
    data = result[[label_col, "Topsis Score", "Rank"]]

    base = alt.Chart(data).encode(
        y=alt.Y(f"{label_col}:N", sort="-x", title=None),
        x=alt.X("Topsis Score:Q", title="Topsis Score",
                scale=alt.Scale(domain=[0, 1])),
    )
    bars = base.mark_bar(cornerRadiusEnd=4, size=20, color=BAR_COLOR).encode(
        tooltip=[
            alt.Tooltip(f"{label_col}:N"),
            alt.Tooltip("Topsis Score:Q", format=".4f"),
            alt.Tooltip("Rank:Q"),
        ],
    )
    labels = base.mark_text(align="left", dx=4, fontSize=12).encode(
        text=alt.Text("Topsis Score:Q", format=".3f"),
    )
    return (bars + labels).properties(height=alt.Step(34))


# --------------------------- UI ---------------------------
st.set_page_config(page_title="TOPSIS Analyzer", page_icon="📊", layout="wide")

# ---- Sidebar: inputs ----
with st.sidebar:
    st.header("⚙️ Inputs")
    uploaded = st.file_uploader("Data file (CSV or XLSX)", type=["csv", "xlsx"])
    weights_str = st.text_input("Weights", "1,1,1,1,1", help="Comma-separated numbers, one per criterion.")
    impacts_str = st.text_input("Impacts", "+,+,-,+,-", help="Comma-separated '+' or '-', one per criterion.")
    run = st.button("🚀 Run TOPSIS", type="primary", use_container_width=True)

    with st.expander("ℹ️ Input format"):
        st.markdown(
            "- **File**: first column = names/IDs; other columns = numeric criteria.\n"
            "- **Weights**: e.g. `1,1,1,1,1`.\n"
            "- **Impacts**: `+` (higher is better) or `-` (lower is better), e.g. `+,+,-,+,-`.\n"
            "- Number of weights, impacts, and criteria must match."
        )

# ---- Main: header ----
st.title("📊 TOPSIS Analyzer")
st.caption("Rank alternatives across multiple weighted criteria using the TOPSIS method.")

# ---- Read the uploaded file ----
df = None
if uploaded is not None:
    try:
        if uploaded.name.lower().endswith(".xlsx"):
            df = pd.read_excel(uploaded)
        else:
            df = pd.read_csv(uploaded)
    except Exception as e:
        st.error(f"Could not read the file: {e}")
        df = None

# ---- Empty state ----
if df is None:
    st.info("👈 Upload a data file in the sidebar to get started.")
    st.stop()

# ---- Preview / summary ----
n_alt, n_crit = df.shape[0], max(df.shape[1] - 1, 0)
m1, m2 = st.columns(2)
m1.metric("Alternatives", n_alt)
m2.metric("Criteria", n_crit)

if not run:
    st.subheader("Data preview")
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.info("Set your weights and impacts in the sidebar, then click **Run TOPSIS**.")
    st.stop()

# ---- Run TOPSIS ----
try:
    weights = [float(w.strip()) for w in weights_str.split(",")]
except ValueError:
    st.error("Weights must be numeric and comma-separated.")
    st.stop()

impacts = [i.strip() for i in impacts_str.split(",")]

err = validate(df, weights, impacts)
if err:
    st.error(err)
    st.stop()

result = compute_topsis(df, weights, impacts).sort_values("Rank")
label_col = result.columns[0]
best_row = result.loc[result["Rank"] == 1].iloc[0]

st.success("TOPSIS analysis complete.")

# Winner highlight
w1, w2 = st.columns(2)
w1.metric("🏆 Top-ranked", str(best_row[label_col]))
w2.metric("Best score", f"{best_row['Topsis Score']:.4f}")

tab_table, tab_chart = st.tabs(["📋 Results table", "📊 Ranking chart"])

with tab_table:
    st.dataframe(
        result,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Topsis Score": st.column_config.ProgressColumn(
                "Topsis Score", format="%.4f", min_value=0.0, max_value=1.0,
            ),
            "Rank": st.column_config.NumberColumn("Rank", format="%d"),
        },
    )
    csv_bytes = result.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download result CSV",
        data=csv_bytes,
        file_name="topsis_result.csv",
        mime="text/csv",
    )

with tab_chart:
    st.altair_chart(ranking_chart(result), use_container_width=True)
