from flask import Flask, render_template, request
import pickle
import os

from utils.risk_calculator import calculate_risk
from utils.company_checker import verify_company
from utils.pdf_reader import extract_text_from_pdf

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Load AI model
with open("scam_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# Load vectorizer
with open("vectorizer.pkl", "rb") as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)


@app.route("/", methods=["GET", "POST"])
def home():

    result = ""
    confidence = 0
    risk = 0
    reasons = []

    company_name = ""
    company_verified = None
    company_website = ""

    if request.method == "POST":

        job_text = ""

        # -------- Text Input --------
        if request.form.get("job_description"):
            job_text = request.form["job_description"]

        # -------- PDF Upload --------
        elif "pdf_file" in request.files:

            pdf = request.files["pdf_file"]

            if pdf.filename != "":

                pdf_path = os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    pdf.filename
                )

                pdf.save(pdf_path)

                job_text = extract_text_from_pdf(pdf_path)

        if job_text != "":

            text = vectorizer.transform([job_text])

            prediction = model.predict(text)[0]

            probability = model.predict_proba(text)

            confidence = round(max(probability[0]) * 100, 2)

            risk, reasons = calculate_risk(job_text, prediction)

            company_verified, company_name, company_website = verify_company(job_text)

            if company_verified is True:

                reasons.append(
                    f"✅ Company Verified : {company_name}"
                )

            elif company_verified is False:

                risk += 20

                reasons.append(
                    "⚠ Company website not found."
                )

            else:

                reasons.append(
                    "⚠ Company could not be verified."
                )

            if risk > 100:
                risk = 100

            if risk >= 60:
                result = "❌ Fraudulent Job"

            elif risk >= 30:
                result = "⚠ Suspicious Job"

            else:
                result = "✅ Genuine Job"

    return render_template(
        "index.html",
        result=result,
        confidence=confidence,
        risk=risk,
        reasons=reasons,
        company_name=company_name,
        company_verified=company_verified,
        company_website=company_website
    )


if __name__ == "__main__":
    app.run(debug=True)