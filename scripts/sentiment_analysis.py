"""FinBERT sentiment scoring for palm-oil company sustainability claims.

Reads every Results/{company}_specific_claims.csv, scores each claim's
sentiment with ProsusAI/finbert (via transformers.pipeline), and writes a
combined table to data/nlp/claims_with_sentiment.csv.

Sentiment score definition
---------------------------
FinBERT returns P(positive), P(negative), P(neutral) for each piece of text.
We collapse these three probabilities into a single sentiment_score in
[0, 1], where 1 = maximally positive-sounding, 0 = maximally negative:

    sentiment_score = (P(positive) - P(negative) + 1) / 2

This centers neutral claims (P(pos) ~= P(neg)) around 0.5 and pushes
strongly positive claims toward 1, strongly negative claims toward 0.

Why this matters for greenwashing detection: a claim that reads as very
positive/upbeat ("we are proud to announce...") paired with a company that
has high measured forest loss is the concerning combination -- confident,
positive language next to bad on-the-ground outcomes. Positive sentiment
alone is not damning; it's the mismatch with forest_loss_score in the
scoring step (see build_scores_v2.py) that signals greenwashing.

Fallback
--------
If the FinBERT model cannot be downloaded/loaded (e.g. no network access to
huggingface.co in this environment), this script falls back to a small
hand-built positive/negative lexicon tuned for sustainability-report
language. This is NOT a silent substitute: every row gets a
`sentiment_method` column ("finbert" or "lexicon_fallback") so downstream
consumers (and you) can see exactly which scores to trust less. The console
log also prints a clear FALLBACK warning.

Usage
-----
    python scripts/sentiment_analysis.py
"""
import glob
import os
import sys

import pandas as pd

RESULTS_DIR = "Results"
OUT_DIR = "data/nlp"
OUT_PATH = os.path.join(OUT_DIR, "claims_with_sentiment.csv")

# Filename-stem -> canonical company key used in data/mills/master_forest_loss.csv.
# Only "gentingplantations" (claims file) vs "genting" (forest-loss table) differs;
# every other stem already matches.
COMPANY_NAME_MAP = {
    "gentingplantations": "genting",
}

BATCH_SIZE = 16
MAX_CHARS = 512  # FinBERT truncates at 512 tokens anyway; keeps batches fast

POSITIVE_WORDS = {
    "committed", "commitment", "achieve", "achieved", "leadership", "leading",
    "sustainable", "sustainability", "responsible", "responsibly", "protect",
    "protection", "conserve", "conservation", "improve", "improved", "improving",
    "empower", "empowered", "empowerment", "reduce", "reduced", "reducing",
    "increase", "increased", "renewable", "recycl", "certified", "compliance",
    "compliant", "transparency", "transparent", "resilient", "resilience",
    "partner", "partnership", "recognised", "recognized", "award", "milestone",
    "target", "ambition", "net zero", "zero-deforestation", "traceability",
    "100%", "best practice", "proud", "progress",
}
NEGATIVE_WORDS = {
    "fail", "failed", "failure", "violation", "breach", "penalty", "fine",
    "deforestation", "illegal", "complaint", "lawsuit", "suspend", "suspended",
    "controversy", "risk", "delay", "delayed", "shortfall", "decline", "declined",
    "loss", "damage", "destroy", "destroyed", "clearance", "cleared", "non-compliance",
}


def company_from_filename(path: str) -> str:
    stem = os.path.basename(path).replace("_specific_claims.csv", "")
    return COMPANY_NAME_MAP.get(stem, stem)


def load_all_claims() -> pd.DataFrame:
    frames = []
    for path in sorted(glob.glob(os.path.join(RESULTS_DIR, "*_specific_claims.csv"))):
        company = company_from_filename(path)
        df = pd.read_csv(path)
        df["company"] = company
        frames.append(df)
    if not frames:
        raise FileNotFoundError(f"No *_specific_claims.csv files found in {RESULTS_DIR}")
    return pd.concat(frames, ignore_index=True)


def try_load_finbert():
    """Attempt to load the FinBERT pipeline. Returns None (not raises) on any failure."""
    try:
        from transformers import pipeline
        clf = pipeline("text-classification", model="ProsusAI/finbert", top_k=None)
        clf("smoke test claim about sustainability")  # force a real forward pass
        return clf
    except Exception as exc:
        print(f"[sentiment_analysis] FinBERT unavailable: {exc}", file=sys.stderr)
        return None


def score_with_finbert(clf, claims: list) -> list:
    scores = []
    for i in range(0, len(claims), BATCH_SIZE):
        batch = [str(c)[:MAX_CHARS] for c in claims[i:i + BATCH_SIZE]]
        results = clf(batch, truncation=True)
        for res in results:
            probs = {r["label"].lower(): r["score"] for r in res}
            pos = probs.get("positive", 0.0)
            neg = probs.get("negative", 0.0)
            scores.append((pos - neg + 1) / 2)
        print(f"[sentiment_analysis]   scored {min(i + BATCH_SIZE, len(claims))}/{len(claims)}")
    return scores


def score_with_lexicon(claims: list) -> list:
    """Documented fallback: fraction of sentiment-word hits that are positive.

    No hits at all -> 0.5 (neutral, no signal either way). This is a coarse
    heuristic, not a substitute for FinBERT -- rows scored this way are
    flagged via the sentiment_method column.
    """
    scores = []
    for c in claims:
        text = str(c).lower()
        pos_hits = sum(1 for w in POSITIVE_WORDS if w in text)
        neg_hits = sum(1 for w in NEGATIVE_WORDS if w in text)
        total = pos_hits + neg_hits
        scores.append(0.5 if total == 0 else pos_hits / total)
    return scores


def main():
    claims_df = load_all_claims()
    print(f"[sentiment_analysis] loaded {len(claims_df)} claims across "
          f"{claims_df['company'].nunique()} companies: "
          f"{sorted(claims_df['company'].unique())}")

    clf = try_load_finbert()
    texts = claims_df["claim"].fillna("").tolist()

    if clf is not None:
        print("[sentiment_analysis] scoring with FinBERT (ProsusAI/finbert)...")
        claims_df["sentiment_score"] = score_with_finbert(clf, texts)
        claims_df["sentiment_method"] = "finbert"
        fallback_used = False
    else:
        print("[sentiment_analysis] FALLBACK IN USE: FinBERT could not be loaded in this "
              "environment. Using a lexicon-based sentiment heuristic instead. Treat "
              "sentiment_score as a rough proxy only until FinBERT can be run.")
        claims_df["sentiment_score"] = score_with_lexicon(texts)
        claims_df["sentiment_method"] = "lexicon_fallback"
        fallback_used = True

    final_cols = ["company", "claim", "specificity_score", "sentiment_score", "sentiment_method"] + \
                 [c for c in claims_df.columns if c not in
                  ("company", "claim", "specificity_score", "sentiment_score", "sentiment_method")]
    result = claims_df[final_cols]

    os.makedirs(OUT_DIR, exist_ok=True)
    result.to_csv(OUT_PATH, index=False)

    print(f"\n[sentiment_analysis] wrote {len(result)} rows to {OUT_PATH} "
          f"(fallback_used={fallback_used})")
    print("[sentiment_analysis] mean sentiment_score by company:")
    print(result.groupby("company")["sentiment_score"].mean().sort_values(ascending=False).round(3))


if __name__ == "__main__":
    main()
