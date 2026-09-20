"""Unit and integrity tests for NLP model evaluation routines and gold dataset schemas."""
import os
import pandas as pd
import pytest

from model_comparison import (
    _acc_prf,
    cohen_kappa,
    rule_specificity,
    keyword_topic,
    GOLD_FILLED,
    ENRICHED,
)


def test_acc_prf_binary_perfect():
    pred = [1, 0, 1, 1]
    gold = [1, 0, 1, 1]
    acc, p, r, f, n = _acc_prf(pred, gold, positive=1)
    assert acc == 1.0
    assert p == 1.0
    assert r == 1.0
    assert f == 1.0
    assert n == 4


def test_acc_prf_binary_imperfect():
    pred = [1, 1, 0, 0]
    gold = [1, 0, 1, 0]
    acc, p, r, f, n = _acc_prf(pred, gold, positive=1)
    assert acc == 0.5
    assert p == 0.5
    assert r == 0.5
    assert f == 0.5


def test_cohen_kappa_perfect_agreement():
    a = ["yes", "no", "yes", "yes"]
    b = ["yes", "no", "yes", "yes"]
    k, po = cohen_kappa(a, b)
    assert k == pytest.approx(1.0)
    assert po == 1.0


def test_cohen_kappa_independent():
    a = ["yes", "no"] * 50
    b = ["no", "yes"] * 50
    k, po = cohen_kappa(a, b)
    assert k == pytest.approx(-1.0)
    assert po == 0.0


def test_rule_specificity():
    # Contains number/unit -> specific
    assert rule_specificity("We conserved 5,000 hectares of peatland by 2025.") == "spec"
    assert rule_specificity("Achieved 98% traceability to mill level.") == "spec"
    assert rule_specificity("Traceable across 45 mills.") == "spec"
    assert rule_specificity("Targeting 1000 tonnes CPO.") == "spec"

    # Vague qualitative statements -> non-specific
    assert rule_specificity("We are dedicated to sustainable palm oil production.") == "non"
    assert rule_specificity("Continuous efforts to maintain good agricultural practices.") == "non"


def test_keyword_topic():
    assert keyword_topic({"deforestation": True, "peat": False}) == "deforestation"
    assert keyword_topic({"peat": True}) == "peat"
    assert keyword_topic({"ndpe": True}) == "ndpe"
    assert keyword_topic({"traceability": True}) == "traceability"
    assert keyword_topic({}) == "other"


def test_gold_dataset_schema_and_distribution():
    """Verify nlp_gold_labeled.csv schema and completeness."""
    assert os.path.exists(GOLD_FILLED), f"Missing {GOLD_FILLED}"
    df = pd.read_csv(GOLD_FILLED)

    assert len(df) == 150
    assert set(df["gold_is_claim"].dropna().astype(int)) == {0, 1}

    # Exactly 106 claims are labeled for downstream sub-tasks
    gs = df[df["gold_specificity"].astype(str).str.lower().isin(["high", "medium", "low"])]
    assert len(gs) == 106

    gse = df[df["gold_sentiment"].astype(str).str.lower().isin(["positive", "neutral", "negative"])]
    assert len(gse) == 106

    gt = df[df["gold_esg_topic"].astype(str).str.upper().isin(["E", "S", "G", "NONE"])]
    assert len(gt) == 106


def test_enriched_claims_corpus():
    """Verify data/nlp/claims_enriched.csv contains 403 claims across 11 companies."""
    assert os.path.exists(ENRICHED), f"Missing {ENRICHED}"
    df = pd.read_csv(ENRICHED)

    assert len(df) == 403
    # Check all 11 companies are present
    assert df["company"].nunique() >= 11

    # Check specificity and sentiment scores
    assert (df["specificity_score"] >= 0.0).all() and (df["specificity_score"] <= 1.0).all()
    assert (df["sentiment_score"] >= 0.0).all() and (df["sentiment_score"] <= 1.0).all()
