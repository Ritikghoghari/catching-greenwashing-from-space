"""Core scoring logic for greenwashing mismatch score. Pure functions, no I/O."""
import pandas as pd


def compute_claim_strength(claims: pd.DataFrame) -> pd.DataFrame:
    """Per-company share of 'hard' claims (0-100) and claim count."""
    strength = (
        claims.groupby("company")["strength"]
        .apply(lambda s: (s == "hard").mean() * 100)
        .rename("claim_strength_score")
        .reset_index()
    )
    n_claims = claims.groupby("company").size().rename("n_claims").reset_index()
    return strength.merge(n_claims, on="company")


def compute_forest_loss_score(loss: pd.DataFrame) -> pd.DataFrame:
    """Per-mill average post-2020 loss, min-max normalized to 0-100.

    Companies with n_mills == 0 get NaN loss_per_mill_ha (can't divide by zero).
    If every company has identical loss_per_mill_ha, everyone scores 0 (no
    spread to normalize) instead of NaN from a 0/0 division.
    """
    loss = loss.copy()
    loss["loss_per_mill_ha"] = loss["loss_after_2020_ha"].where(
        loss["n_mills"] > 0
    ) / loss["n_mills"].replace(0, pd.NA)

    lo, hi = loss["loss_per_mill_ha"].min(), loss["loss_per_mill_ha"].max()
    if pd.isna(lo) or hi == lo:
        loss["forest_loss_score"] = 0.0
    else:
        loss["forest_loss_score"] = (loss["loss_per_mill_ha"] - lo) / (hi - lo) * 100
    return loss


def compute_mismatch_scores(claims: pd.DataFrame, loss: pd.DataFrame) -> pd.DataFrame:
    """Combine claim-strength and forest-loss scores into the mismatch score."""
    strength = compute_claim_strength(claims)
    loss_scored = compute_forest_loss_score(loss)

    scores = loss_scored.merge(strength, on="company", how="inner")
    scores["mismatch_score"] = (
        0.5 * scores["claim_strength_score"] + 0.5 * scores["forest_loss_score"]
    ).round(1)
    scores["low_mill_coverage"] = scores["n_mills"] < 5

    return scores[[
        "company", "n_claims", "claim_strength_score", "n_mills", "loss_after_2020_ha",
        "loss_per_mill_ha", "forest_loss_score", "mismatch_score", "low_mill_coverage",
    ]].sort_values("mismatch_score", ascending=False).reset_index(drop=True)
