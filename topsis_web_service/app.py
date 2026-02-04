import os
import re
import smtplib
import pandas as pd
import numpy as np
from flask import Flask, request, render_template, flash
from werkzeug.utils import secure_filename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# ---------------- Flask Setup ----------------
app = Flask(__name__)
app.secret_key = "topsis_secret"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ------------- Email Configuration -----------
SENDER_EMAIL = "mahimkatiyar83@gmail.com"      
SENDER_PASSWORD = "nxyrlbqcztwzdupq"  

# ---------------- Utilities ------------------
def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)

def send_email(receiver, attachment_path):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver
    msg["Subject"] = "TOPSIS Result File"

    body = "Hello,\n\nPlease find the attached TOPSIS result file.\n\nRegards,\nTOPSIS Web Service"
    msg.attach(MIMEText(body, "plain"))

    with open(attachment_path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition",
                        f"attachment; filename={os.path.basename(attachment_path)}")
        msg.attach(part)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print("Email error:", e)
        return False

# ---------------- TOPSIS Logic ----------------
def run_topsis(file_path, weights, impacts):
    df = pd.read_csv(file_path)

    if df.shape[1] < 3:
        return None, "Input file must have at least 3 columns."

    data = df.iloc[:, 1:].apply(pd.to_numeric, errors="coerce")
    if data.isnull().values.any():
        return None, "From 2nd column onwards, values must be numeric."

    if len(weights) != data.shape[1] or len(impacts) != data.shape[1]:
        return None, "Number of weights, impacts, and criteria must be equal."

    norm = data.values / np.sqrt((data.values ** 2).sum(axis=0))
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

    df["Topsis Score"] = score
    df["Rank"] = df["Topsis Score"].rank(ascending=False, method="dense").astype(int)

    output_path = os.path.join(app.config["UPLOAD_FOLDER"], "result.csv")
    df.to_csv(output_path, index=False)

    return output_path, None

# ---------------- Routes ----------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        if "file" not in request.files:
            flash("No file uploaded", "error")
            return render_template("form.html")

        file = request.files["file"]
        if file.filename == "":
            flash("No file selected", "error")
            return render_template("form.html")

        email = request.form["email"]
        weights_str = request.form["weights"]
        impacts_str = request.form["impacts"]

        if not validate_email(email):
            flash("Invalid email format", "error")
            return render_template("form.html")

        try:
            weights = [float(w) for w in weights_str.split(",")]
            impacts = impacts_str.split(",")
            if not all(i in ["+", "-"] for i in impacts):
                raise ValueError
        except:
            flash("Invalid weights or impacts format", "error")
            return render_template("form.html")

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        result_path, error = run_topsis(filepath, weights, impacts)
        if error:
            flash(error, "error")
            return render_template("form.html")

        if send_email(email, result_path):
            flash("Result sent successfully to your email!", "success")
        else:
            flash("TOPSIS done, but email failed.", "error")

    return render_template("form.html")

# ---------------- Run Server ----------------
if __name__ == "__main__":
    app.run(debug=True)
