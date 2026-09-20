"""Tests for the canonical 4-component greenwashing mismatch scoring engine (scripts/build_scores_v2.py)."""
import os
import pandas as pd
import pytest

from build_scores_v2 import (
    W_FOREST_LOSS,
    W_SPECIFICITY,
    W_SENTIMENT,
    W_SPATIAL,
    min_max_100,
    compute_spatial_match,
    OUT_PATH,
)


def test_canonical_weights_sum_to_one():
    """Canonical weights must sum strictly to 1.0. Reject any 1.05 variant."""
    total = W_FOREST_LOSS + W_SPECIFICITY + W_SENTIMENT + W_SPATIAL
    assert total == pytest.approx(1.0, abs=1e-9)
    # Explicitly test each component value
    assert W_FOREST_LOSS == 0.35
    assert W_SPECIFICITY == 0.35
    assert W_SENTIMENT == 0.15
    assert W_SPATIAL == 0.15


def test_min_max_100_normal():
    s = pd.Series([10.0, 20.0, 30.0])
    res = min_max_100(s)
    assert res.iloc[0] == pytest.approx(0.0)
    assert res.iloc[1] == pytest.approx(50.0)
    assert res.iloc[2] == pytest.approx(100.0)


def test_min_max_100_flat_series_returns_zeros():
    """Flat series (all identical values) must return 0.0, never NaN or Inf."""
    s = pd.Series([42.0, 42.0, 42.0])
    res = min_max_100(s)
    assert (res == 0.0).all()
    assert not res.isna().any()


def test_min_max_100_single_value():
    s = pd.Series([100.0])
    res = min_max_100(s)
    assert (res == 0.0).all()


def test_spatial_match_computation(tmp_path):
    """Synthetic test for compute_spatial_match logic."""
    csv_file = tmp_path / "test_mills.csv"
    # 4 mills across 2 companies:
    # Median of [100, 200, 300, 400] is 250
    # co1 has [100, 300] -> 1 above median out of 2 -> 50%
    # co2 has [200, 400] -> 1 above median out of 2 -> 50%
    df = pd.DataFrame({
        "company": ["co1", "co1", "co2", "co2"],
        "mill_name": ["m1", "m2", "m3", "m4"],
        "loss_post2020_ha": [100.0, 300.0, 200.0, 400.0],
    })
    df.to_csv(csv_file, index=False)
    out = compute_spatial_match(str(csv_file)).set_index("company")
    assert out.loc["co1", "n_mills_total"] == 2
    assert out.loc["co1", "n_mills_severe"] == 1
    assert out.loc["co1", "spatial_match_pct"] == pytest.approx(50.0)
    assert out.loc["co2", "spatial_match_pct"] == pytest.approx(50.0)


def test_master_scores_canonical_ground_truth():
    """Verify master_scores.csv matches the verified ground truth."""
    assert os.path.exists(OUT_PATH), f"Missing {OUT_PATH}"
    df = pd.read_csv(OUT_PATH)

    # 1. Company count
    assert len(df) == 11, f"Expected 11 companies, found {len(df)}"

    # 2. Rank 1 is KLK with 65.6
    rank_1 = df[df["rank"] == 1].iloc[0]
    assert rank_1["company"] == "klk"
    assert rank_1["mismatch_score"] == pytest.approx(65.6, abs=0.1)

    # 3. Rank 11 is Astra Agro with 17.6
    rank_11 = df[df["rank"] == 11].iloc[0]
    assert rank_11["company"] == "astraagro"
    assert rank_11["mismatch_score"] == pytest.approx(17.6, abs=0.1)

    # 4. Total mill count sum across companies equals 290
    assert df["n_mills"].sum() == 290

    # 5. All scores bounded in [0, 100]
    for col in ["mismatch_score", "forest_loss_score", "specificity_score", "sentiment_score_norm", "spatial_match_score"]:
        assert (df[col] >= 0.0).all(), f"Negative values in {col}"
        assert (df[col] <= 100.0).all(), f"Values > 100 in {col}"

    # 6. Strict monotonic descending order for mismatch_score
    scores = df["mismatch_score"].tolist()
    assert scores == sorted(scores, reverse=True)
