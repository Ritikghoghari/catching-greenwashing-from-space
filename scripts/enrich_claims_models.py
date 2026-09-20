"""Add the remaining two NLP models to the claim table.

The claim pipeline already applies:
  1. climatebert/environmental-claims            -> which sentences are claims (*_claims.csv)
  2. climatebert/distilroberta-base-climate-specificity -> specificity_score  (claims_with_sentiment.csv)
  3. ProsusAI/finbert                            -> sentiment_score           (claims_with_sentiment.csv)

This script adds the last two from the CLAUDE.md model stack, as new columns
only -- it does NOT touch specificity_score or sentiment_score, so the
professor-approved mismatch score in build_scores_v2.py is unchanged:

  4. nbroad/ESG-BERT                              -> esg_category   (+ esg_category_score)
  5. climatebert/distilroberta-base-climate-sentiment -> climate_sentiment (risk/neutral/opportunity,
                                                        + climate_sentiment_score)

climate_sentiment is kept as a comparison signal against the FinBERT
sentiment_score that actually feeds scoring; esg_category lets the results
chapter report what topics the extracted claims cluster on
(Ecological_Impacts vs GHG_Emissions vs Human_Rights ...).

Input : data/nlp/claims_with_sentiment.csv   (run sentiment_analysis.py first)
Output: data/nlp/claims_enriched.csv

Usage:
    python scripts/enrich_claims_models.py
"""
import os
import sys
import warnings

warnings.filterwarnings("ignore")
import pandas as pd

IN_PATH = "data/nlp/claims_with_sentiment.csv"
OUT_PATH = "data/nlp/claims_enriched.csv"

ESG_MODEL = "nbroad/ESG-BERT"
CLIMATE_SENTIMENT_MODEL = "climatebert/distilroberta-base-climate-sentiment"

BATCH_SIZE = 16
MAX_CHARS = 512


def load_clf(model_name):
    from transformers import pipeline
    clf = pipeline("text-classification", model=model_name, top_k=None)
    clf("smoke test claim about sustainable palm oil")
    return clf


def top_label(clf, texts):
    """Return (label, score) for the highest-probability class of each text."""
    out = []
    for i in range(0, len(texts), BATCH_SIZE):
        batch = [str(t)[:MAX_CHARS] for t in texts[i:i + BATCH_SIZE]]
        for res in clf(batch, truncation=True):
            best = max(res, key=lambda r: r["score"])
            out.append((best["label"], round(float(best["score"]), 4)))
        print(f"  scored {min(i + BATCH_SIZE, len(texts))}/{len(texts)}")
    return out


def main():
    if not os.path.exists(IN_PATH):
        sys.exit(f"missing {IN_PATH} -- run scripts/sentiment_analysis.py first")

    df = pd.read_csv(IN_PATH)
    texts = df["claim"].fillna("").tolist()
    print(f"[enrich] {len(df)} claims, {df['company'].nunique()} companies")

    print(f"[enrich] loading {ESG_MODEL} ...")
    esg = load_clf(ESG_MODEL)
    print(f"[enrich] scoring ESG category ...")
    esg_out = top_label(esg, texts)
    df["esg_category"] = [l for l, _ in esg_out]
    df["esg_category_score"] = [s for _, s in esg_out]

    print(f"[enrich] loading {CLIMATE_SENTIMENT_MODEL} ...")
    cs = load_clf(CLIMATE_SENTIMENT_MODEL)
    print(f"[enrich] scoring climate sentiment ...")
    cs_out = top_label(cs, texts)
    df["climate_sentiment"] = [l for l, _ in cs_out]
    df["climate_sentiment_score"] = [s for _, s in cs_out]

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    df.to_csv(OUT_PATH, index=False)
    print(f"\n[enrich] wrote {len(df)} rows to {OUT_PATH}\n")

    print("ESG category distribution:")
    print(df["esg_category"].value_counts().to_string())
    print("\nClimate sentiment distribution:")
    print(df["climate_sentiment"].value_counts().to_string())
    print("\nClimate sentiment by company (share 'opportunity'):")
    share = (df.assign(opp=df["climate_sentiment"].eq("opportunity"))
               .groupby("company")["opp"].mean().sort_values(ascending=False).round(3))
    print(share.to_string())


if __name__ == "__main__":
    main()
