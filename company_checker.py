import re

# Some well-known companies for verification
KNOWN_COMPANIES = {
    "google": "google.com",
    "microsoft": "microsoft.com",
    "amazon": "amazon.jobs",
    "infosys": "infosys.com",
    "tcs": "tcs.com",
    "wipro": "wipro.com",
    "accenture": "accenture.com",
    "ibm": "ibm.com",
    "cognizant": "cognizant.com"
}

def verify_company(job_text):
    text = job_text.lower()

    for company, website in KNOWN_COMPANIES.items():
        if company in text:

            # Check if official website is mentioned
            if website in text:
                return True, company.title(), website

            return False, company.title(), website

    return None, "Unknown", ""