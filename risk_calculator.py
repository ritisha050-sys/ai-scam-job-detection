import re

def calculate_risk(job_text, ml_prediction):

    risk = 0
    reasons = []

    text = job_text.lower()

    # Suspicious keywords
    keywords = [
        "registration fee",
        "processing fee",
        "security deposit",
        "whatsapp",
        "telegram",
        "immediate joining",
        "no experience",
        "earn",
        "guaranteed income",
        "limited seats",
        "work from home"
    ]

    for word in keywords:
        if word in text:
            risk += 10
            reasons.append(f"⚠️ Suspicious keyword: {word}")

    # Gmail/Yahoo check
    if "@gmail.com" in text or "@yahoo.com" in text:
        risk += 15
        reasons.append("⚠️ Personal email used")

    # Unrealistic salary
    salaries = re.findall(r"\d[\d,]*", job_text)

    for s in salaries:
        num = int(s.replace(",", ""))

        if num > 500000:
            risk += 20
            reasons.append("⚠️ Unrealistic salary detected")
            break

    # ML Prediction
    if ml_prediction == 1:
        risk += 30
        reasons.append("🤖 AI model suspects fraud")

    if risk > 100:
        risk = 100

    return risk, reasons