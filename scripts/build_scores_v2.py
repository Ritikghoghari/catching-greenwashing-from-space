"""Rebuild the 4-component greenwashing mismatch score (professor-approved formula).

    mismatch_score = 0.35 * forest_loss_score       (% of forest_2000 lost, normalized 0-100)
                    + 0.35 * specificity_score        (claim specificity, normalized 0-100)
                    + 0.15 * sentiment_score           (claim positivity, normalized 0-100)
                    + 0.15 * spatial_match_score       (see note below)

Spatial match component
------------------------
Companies claim "zero deforestation" across their mill network as a whole,
not mill-by-mill. spatial_match_score operationalizes how spatially
widespread SEVERE mismatch is: the percentage of a company's mills
(data/mills/all_mills_forest_loss.csv) whose post-2020 loss exceeds the
dataset-wide median per-mill loss (~2,653 ha). "Any loss > 0" was tried
first and rejected -- every one of the 290 mills has post-2020 loss (min
105 ha), so that definition is universal and does not differentiate
companies; it is itself a real finding, worth stating in the thesis
separately, just not usable as a scoring component. The median-severity
threshold does differentiate: a company where most mills are above-median
violators scores higher here than one where severe loss is concentrated in
a few outlier mills -- a distinct signal from total hectares (already
captured by forest_loss_score) or ha/mill intensity (reported separately).

This was previously zeroed out because no spatial-agreement metric existed
in the codebase; the per-mill breakdown now exists (all_mills_forest_loss.csv,
290 rows) and is used directly, so the full professor-approved 4-component
weights are used as written -- no redistribution.

Company-name normalization
---------------------------
Results/gentingplantations_specific_claims.csv uses "gentingplantations";
data/mills/master_forest_loss.csv uses "genting". Both scripts in this
pipeline (sentiment_analysis.py and this one) apply the same
COMPANY_NAME_MAP so the two tables join cleanly.

"apical" is excluded from the final score: it is a trading/refining arm
with no mills in the UML, so it has no forest-loss row to compare against
(same exclusion mill_matching.py already documents).

Usage
-----
    python scripts/sentiment_analysis.py      # must run first
    python scripts/build_scores_v2.py
"""
import os

import pandas as pd

CLAIMS_WITH_SENTIMENT = "data/nlp/claims_with_sentiment.csv"
FOREST_LOSS_PATH = "data/mills/master_forest_loss.csv"
PER_MILL_LOSS_PATH = "data/mills/all_mills_forest_loss.csv"
OUT_PATH = "Results/master_scores.csv"

# Professor-approved weights, used as written -- no redistribution.
W_FOREST_LOSS = 0.35
W_SPECIFICITY = 0.35
W_SENTIMENT = 0.15
W_SPATIAL = 0.15

assert abs((W_FOREST_LOSS + W_SPECIFICITY + W_SENTIMENT + W_SPATIAL) - 1.0) < 1e-9


def min_max_100(s: pd.Series) -> pd.Series:
    """Min-max normalize a series to 0-100. Flat series (all equal) -> all 0."""
    lo, hi = s.min(), s.max()
    if pd.isna(lo) or hi == lo:
        return pd.Series(0.0, index=s.index)
    return (s - lo) / (hi - lo) * 100


def compute_spatial_match(per_mill_path: str) -> pd.DataFrame:
    """Percentage of each company's mills showing SEVERE post-2020 forest loss.

    Every one of the 290 mills in this dataset has some post-2020 loss
    (min 105 ha) -- "loss > 0" is universal and does not differentiate
    companies, so it is not usable as a scoring component (see
    Results/master_scores.csv's Aug 27 note / thesis methodology section
    for this explicitly, since it is itself a real, separate finding worth
    stating: 100% of mills across all 11 companies show post-2020 loss).

    Instead this measures spatial breadth of SEVERE violation: the percent
    of a company's mills whose post-2020 loss exceeds the dataset-wide
    median per-mill loss. A company where most mills are above-median
    violators has a more spatially widespread severe mismatch than one
    where violation is concentrated in a few outlier mills.
    """
    mills = pd.read_csv(per_mill_path)
    global_median_ha = mills["loss_post2020_ha"].median()
    per_mill = mills.groupby("company").agg(
        n_mills_total=("mill_name", "size"),
        n_mills_severe=("loss_post2020_ha", lambda s: (s > global_median_ha).sum()),
    ).reset_index()
    per_mill["spatial_match_pct"] = (
        per_mill["n_mills_severe"] / per_mill["n_mills_total"] * 100
    )
    print(f"[build_scores_v2] spatial_match_score = %% of mills above global median "
          f"per-mill loss ({global_median_ha:.0f} ha)")
    return per_mill[["company", "n_mills_total", "n_mills_severe", "spatial_match_pct"]]


def main():
    claims = pd.read_csv(CLAIMS_WITH_SENTIMENT)
    loss = pd.read_csv(FOREST_LOSS_PATH)
    spatial = compute_spatial_match(PER_MILL_LOSS_PATH)

    per_company = claims.groupby("company").agg(
        n_claims=("claim", "size"),
        specificity_mean=("specificity_score", "mean"),
        sentiment_mean=("sentiment_score", "mean"),
    ).reset_index()

    scores = loss.merge(per_company, on="company", how="inner")
    scores = scores.merge(spatial, on="company", how="left")
    excluded = set(claims["company"]) - set(scores["company"])
    if excluded:
        print(f"[build_scores_v2] excluded (no forest-loss row): {sorted(excluded)}")
    missing_spatial = scores[scores["spatial_match_pct"].isna()]["company"].tolist()
    if missing_spatial:
        print(f"[build_scores_v2] WARNING no per-mill data for: {missing_spatial} -- spatial_match_score set to 0")
        scores["spatial_match_pct"] = scores["spatial_match_pct"].fillna(0.0)

    scores["forest_loss_score"] = min_max_100(scores["loss_pct_of_forest"])
    scores["specificity_score"] = min_max_100(scores["specificity_mean"])
    # normalized 0-100 aggregate, distinct from claims_with_sentiment.csv's raw [0,1] per-claim sentiment_score
    scores["sentiment_score_norm"] = min_max_100(scores["sentiment_mean"])
    # spatial_match_pct is already 0-100 (a true percentage), not re-normalized
    # via min-max -- min-max would distort the meaningful "% of mills" scale
    # (e.g. compress a real 80%-vs-95% gap into an artificial 0-100 spread).
    scores["spatial_match_score"] = scores["spatial_match_pct"]

    scores["mismatch_score"] = (
        W_FOREST_LOSS * scores["forest_loss_score"]
        + W_SPECIFICITY * scores["specificity_score"]
        + W_SENTIMENT * scores["sentiment_score_norm"]
        + W_SPATIAL * scores["spatial_match_score"]
    ).round(1)

    scores = scores.sort_values("mismatch_score", ascending=False).reset_index(drop=True)
    scores["rank"] = scores.index + 1

    # Transparency flag: a company-level mean (specificity_mean, sentiment_mean) built
    # from very few claims is a noisy estimate -- e.g. klk has only 8 claims, so its
    # specificity_mean (and the mismatch_score it drives) is less statistically robust
    # than sdguthrie's, which rests on 50 claims. Mirrors the old scoring.py's
    # low_mill_coverage flag pattern.
    LOW_N_CLAIMS_THRESHOLD = 10
    scores["low_n_claims"] = scores["n_claims"] < LOW_N_CLAIMS_THRESHOLD

    out_cols = [
        "company", "mismatch_score", "rank",
        "forest_loss_score", "specificity_score", "sentiment_score_norm", "spatial_match_score",
        "n_claims", "low_n_claims", "n_mills", "loss_pct_of_forest", "loss_post2020_ha",
        "specificity_mean", "sentiment_mean",
        "n_mills_total", "n_mills_severe",
    ]
    result = scores[out_cols]

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    result.to_csv(OUT_PATH, index=False)

    print(f"[build_scores_v2] weights (professor-approved, no redistribution): "
          f"forest_loss={W_FOREST_LOSS:.2f} specificity={W_SPECIFICITY:.2f} "
          f"sentiment={W_SENTIMENT:.2f} spatial={W_SPATIAL:.2f}")
    print(f"[build_scores_v2] wrote {len(result)} rows to {OUT_PATH}\n")
    print(result.to_string(index=False))


if __name__ == "__main__":
    main()
