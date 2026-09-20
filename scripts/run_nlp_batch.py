import pdfplumber, re
import pandas as pd
from transformers import pipeline

clf = pipeline("text-classification", model="climatebert/environmental-claims")
specificity_clf = pipeline("text-classification", model="climatebert/distilroberta-base-climate-specificity")


def extract_claims(pdf_path, company_name):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += (page.extract_text() or "") + " "

    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

    claims = []
    for s in sentences:
        result = clf(s, truncation=True, max_length=512)[0]
        if result["label"] == "yes":
            claims.append(s)

    df = pd.DataFrame({"company": company_name, "claim": claims})
    df.to_csv(f"{company_name}_claims.csv", index=False)
    print(f"{company_name}: {len(sentences)} sentences, {len(claims)} claims")
    return df


def tag_claim(text):
    t = text.lower()
    specificity_result = specificity_clf(text, truncation=True, max_length=512)[0]
    return {
        "claim": text,
        "deforestation": "deforestation" in t,
        "traceability": "traceab" in t or "traceable" in t,
        "ndpe": "ndpe" in t or "no deforestation" in t,
        "peat": "peat" in t,
        "deadline": next((y for y in ["2025", "2030", "2050", "2013"] if y in t), None),
        "strength": "hard" if ("no deforestation" in t or "deforestation-free" in t or "zero" in t) else "soft",
        "specificity": specificity_result["label"],
        "specificity_score": specificity_result["score"],
    }


def process_company(pdf_path, company_name):
    df = extract_claims(pdf_path, company_name)
    if len(df) == 0:
        print(f"{company_name}: no claims found, skipping tag step")
        return
    tagged = pd.DataFrame([tag_claim(c) for c in df["claim"]])
    tagged.to_csv(f"{company_name}_tagged.csv", index=False)

    specific_claims = tagged[tagged["specificity"] == "spec"].reset_index(drop=True)
    specific_claims.to_csv(f"{company_name}_specific_claims.csv", index=False)
    print(f"{company_name}: {len(specific_claims)} of {len(tagged)} claims are specific (checkable)")

    final = tagged[
        (tagged["specificity"] == "spec") &
        (tagged["deforestation"] | tagged["ndpe"] | tagged["peat"] | tagged["traceability"])
    ]
    final.to_csv(f"{company_name}_final_claims.csv", index=False)
    print(f"{company_name}: {len(final)} final claims saved")


COMPANIES = [
    ("Reports/musimmas.pdf", "musimmas"),
    ("Reports/ioi.pdf", "ioi"),
    ("Reports/klk_2025.pdf", "klk"),
    ("Reports/Bumitama_2024.pdf", "bumitama"),
    ("Reports/Apical2025.pdf", "apical"),
    ("Reports/astra-agro_2025.pdf", "astraagro"),
    ("Reports/gentingplantations_2025.pdf", "gentingplantations"),
    ("Reports/sipef.pdf", "sipef"),
]

if __name__ == "__main__":
    for pdf_path, company_name in COMPANIES:
        print(f"=== Processing {company_name} ===")
        try:
            process_company(pdf_path, company_name)
        except Exception as e:
            print(f"{company_name}: FAILED - {e}")
