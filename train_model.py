from flask import Flask, render_template, request
import pickle

from utils.risk_calculator import calculate_risk
from utils.company_checker import verify_company

app = Flask(__name__)

# Load trained model
with open("scam_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# Load vectorizer
with open("vectorizer.pkl", "rb") as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)


@app.route("/", methods=["GET", "POST"])
def home():

    result = ""
    risk = 0
    confidence = 0
    reasons = []

    company_name = ""
    company_verified = None
    company_website = ""

    if request.method == "POST":

        job_text = request.form["job_description"]

        # Convert text
        text = vectorizer.transform([job_text])

        # AI Prediction
        prediction = model.predict(text)[0]

        # Confidence Score
        probability = model.predict_proba(text)
        confidence = round(max(probability[0]) * 100, 2)

        # Risk Calculation
        risk, reasons = calculate_risk(job_text, prediction)

        # Company Verification
        company_verified, company_name, company_website = verify_company(job_text)

        if company_verified is True:
            reasons.append(f"✅ Company Verified : {company_name}")

        elif company_verified is False:
            risk += 20
            reasons.append(
                f"⚠ Official website for {company_name} not found in job description."
            )

        else:
            reasons.append("⚠ Company could not be verified.")

        if risk > 100:
            risk = 100

        # Final Result
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