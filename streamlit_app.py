"""
TOPSIS Web Service — Streamlit app
==================================

Upload a CSV/XLSX file, provide weights and impacts, and get the alternatives
ranked using the TOPSIS (Technique for Order Preference by Similarity to Ideal
Solution) method. Results can be downloaded and optionally emailed.

Deploys on Streamlit Community Cloud (https://streamlit.io) with no server
configuration. Email credentials are read from Streamlit secrets or environment
variables — never hardcoded.

Author: Mahim Katiyar (Roll: 102303958)
"""

import os
import re
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import numpy as np
import pandas as pd
import streamlit as st

EMAIL_RE = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


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


# --------------------------- Email ---------------------------
def _get_credentials():
    """Read sender credentials from Streamlit secrets, then env vars."""
    email = os.environ.get("SENDER_EMAIL")
    password = os.environ.get("SENDER_PASSWORD")
    try:
        email = st.secrets.get("SENDER_EMAIL", email)
        password = st.secrets.get("SENDER_PASSWORD", password)
    except Exception:
        # No secrets file configured — fall back to env vars.
        pass
    return email, password


def send_email(receiver, csv_bytes, filename="topsis_result.csv"):
    """Return (success: bool, error_message: str | None)."""
    sender, password = _get_credentials()
    if not sender or not password:
        return False, "Email is not configured (set SENDER_EMAIL / SENDER_PASSWORD in secrets)."

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = "TOPSIS Result File"
    msg.attach(MIMEText(
        "Hello,\n\nPlease find attached your TOPSIS result file.\n\n"
        "Regards,\nTOPSIS Web Service",
        "plain",
    ))

    part = MIMEBase("application", "octet-stream")
    part.set_payload(csv_bytes)
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={filename}")
    msg.attach(part)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        return True, None
    except Exception as e:
        return False, str(e)


# --------------------------- UI ---------------------------
st.set_page_config(page_title="TOPSIS Web Service", page_icon="📊")
st.title("📊 TOPSIS Web Service")
st.write(
    "Rank alternatives across multiple weighted criteria using the **TOPSIS** "
    "method. Upload your data, set weights and impacts, and get ranked results."
)

with st.expander("How to use / input format"):
    st.markdown(
        "- **File**: CSV or XLSX. First column = names/IDs; remaining columns = numeric criteria.\n"
        "- **Weights**: comma-separated numbers, one per criterion (e.g. `1,1,1,1,1`).\n"
        "- **Impacts**: comma-separated `+` or `-`, one per criterion (e.g. `+,+,-,+,-`).\n"
        "  Use `+` if a higher value is better, `-` if lower is better.\n"
        "- **Email** *(optional)*: receive the result file as an attachment."
    )

uploaded = st.file_uploader("Input data file", type=["csv", "xlsx"])

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

    if df is not None:
        st.subheader("Preview")
        st.dataframe(df.head(), use_container_width=True)
        n_criteria = max(df.shape[1] - 1, 0)
        st.caption(f"Detected **{n_criteria}** criteria (columns after the first).")

col1, col2 = st.columns(2)
with col1:
    weights_str = st.text_input("Weights (comma-separated)", "1,1,1,1,1")
with col2:
    impacts_str = st.text_input("Impacts (+/-, comma-separated)", "+,+,-,+,-")

email = st.text_input("Email (optional — to receive the result file)")

if st.button("Run TOPSIS", type="primary"):
    if df is None:
        st.error("Please upload a valid data file first.")
        st.stop()

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

    result = compute_topsis(df, weights, impacts)
    st.success("TOPSIS analysis complete.")

    st.subheader("Results")
    st.dataframe(
        result.style.highlight_min(subset=["Rank"], color="#2e7d32"),
        use_container_width=True,
    )
    best_row = result.loc[result["Rank"] == 1].iloc[0, 0]
    st.info(f"🏆 Top-ranked alternative: **{best_row}**")

    csv_bytes = result.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download result CSV",
        data=csv_bytes,
        file_name="topsis_result.csv",
        mime="text/csv",
    )

    if email:
        if not re.match(EMAIL_RE, email):
            st.warning("Result is ready above, but the email address looks invalid — not sent.")
        else:
            with st.spinner(f"Emailing result to {email}…"):
                ok, msg = send_email(email, csv_bytes)
            if ok:
                st.success(f"📧 Result also emailed to {email}.")
            else:
                st.info(f"Result is ready above, but email was not sent: {msg}")
