import pandas as pd
import pytest

from scoring import compute_claim_strength, compute_forest_loss_score, compute_mismatch_scores


def test_claim_strength_basic():
    claims = pd.DataFrame({
        "company": ["a", "a", "a", "b"],
        "strength": ["hard", "hard", "soft", "soft"],
    })
    out = compute_claim_strength(claims).set_index("company")
    assert out.loc["a", "claim_strength_score"] == pytest.approx(200 / 3)
    assert out.loc["b", "claim_strength_score"] == 0
    assert out.loc["a", "n_claims"] == 3


def test_forest_loss_score_normal_range():
    loss = pd.DataFrame({
        "company": ["a", "b", "c"],
        "n_mills": [1, 2, 5],
        "loss_after_2020_ha": [100, 100, 100],
    })
    out = compute_forest_loss_score(loss).set_index("company")
    # a: 100/1=100 (max->100), c: 100/5=20 (min->0), b: 100/2=50 (mid)
    assert out.loc["a", "forest_loss_score"] == pytest.approx(100)
    assert out.loc["c", "forest_loss_score"] == pytest.approx(0)
    assert 0 < out.loc["b", "forest_loss_score"] < 100


def test_forest_loss_score_zero_mills_no_crash():
    """n_mills == 0 must not raise ZeroDivisionError / produce inf."""
    loss = pd.DataFrame({
        "company": ["a", "b"],
        "n_mills": [0, 5],
        "loss_after_2020_ha": [100, 100],
    })
    out = compute_forest_loss_score(loss).set_index("company")
    assert pd.isna(out.loc["a", "loss_per_mill_ha"])
    finite_vals = out["loss_per_mill_ha"].dropna()
    assert not any(v in (float("inf"), float("-inf")) for v in finite_vals)


def test_forest_loss_score_identical_values_no_nan():
    """When every company ties, hi == lo; must not divide by zero into NaN."""
    loss = pd.DataFrame({
        "company": ["a", "b"],
        "n_mills": [1, 1],
        "loss_after_2020_ha": [50, 50],
    })
    out = compute_forest_loss_score(loss)
    assert (out["forest_loss_score"] == 0).all()
    assert not out["forest_loss_score"].isna().any()


def test_mismatch_score_only_companies_in_both():
    claims = pd.DataFrame({
        "company": ["a", "b", "c"],
        "strength": ["hard", "soft", "hard"],
    })
    loss = pd.DataFrame({
        "company": ["a", "b"],
        "n_mills": [1, 2],
        "loss_after_2020_ha": [100, 50],
    })
    out = compute_mismatch_scores(claims, loss)
    assert set(out["company"]) == {"a", "b"}
    assert "c" not in out["company"].values


def test_mismatch_score_low_mill_coverage_flag():
    claims = pd.DataFrame({"company": ["a"], "strength": ["hard"]})
    loss = pd.DataFrame({"company": ["a"], "n_mills": [3], "loss_after_2020_ha": [10]})
    out = compute_mismatch_scores(claims, loss)
    assert out.loc[0, "low_mill_coverage"] == True  # noqa: E712
