"""Integration and contract tests between data pipeline outputs, models, and application displays."""
import json
import os
import pandas as pd
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_core_artifact_existence():
    """All core pipeline artifacts must exist on disk."""
    required_files = [
        "Results/master_scores.csv",
        "data/mills/all_mills_forest_loss.csv",
        "data/nlp/claims_enriched.csv",
        "Results/nlp_gold_labeled.csv",
        "Results/nlp_model_comparison.csv",
        "Results/descals_oilpalm_overlay_by_company.csv",
        "Results/prithvi_batch_290.csv",
        "website/data/companies.json",
        "website/data/mills.json",
        "website/data/summary.json",
    ]
    for rel_path in required_files:
        full_path = os.path.join(ROOT, rel_path)
        assert os.path.exists(full_path), f"Missing artifact: {rel_path}"
        assert os.path.getsize(full_path) > 0, f"Artifact is empty: {rel_path}"


def test_master_scores_to_website_companies_contract():
    """Website companies.json must faithfully mirror master_scores.csv."""
    scores_df = pd.read_csv(os.path.join(ROOT, "Results/master_scores.csv"))
    with open(os.path.join(ROOT, "website/data/companies.json"), "r", encoding="utf-8") as f:
        web_companies = json.load(f)

    assert len(web_companies) == len(scores_df) == 11
    web_map = {c["company"]: c for c in web_companies}

    for _, row in scores_df.iterrows():
        comp = row["company"]
        assert comp in web_map, f"Company {comp} missing in website JSON"
        web_row = web_map[comp]
        assert web_row["rank"] == int(row["rank"])
        assert web_row["mismatch_score"] == pytest.approx(float(row["mismatch_score"]), abs=0.1)
        assert web_row["n_mills"] == int(row["n_mills"])
        assert web_row["n_claims"] == int(row["n_claims"])


def test_website_summary_metrics():
    """website/data/summary.json must match canonical physical facts."""
    with open(os.path.join(ROOT, "website/data/summary.json"), "r", encoding="utf-8") as f:
        summary = json.load(f)

    assert summary["total_companies"] == 11
    assert summary["total_mills"] == 290
    assert summary["total_loss_ha"] == pytest.approx(890168.0, abs=1.0)
    assert summary["rank_1_company"] == "KLK"
    assert summary["rank_1_score"] == pytest.approx(65.6, abs=0.1)
    assert summary["rank_11_company"] == "Astra Agro"
    assert summary["rank_11_score"] == pytest.approx(17.6, abs=0.1)


def test_website_mills_schema_and_image_linking():
    """All 290 mills in website/data/mills.json must link to valid clearing map images."""
    with open(os.path.join(ROOT, "website/data/mills.json"), "r", encoding="utf-8") as f:
        mills = json.load(f)

    assert len(mills) == 290
    clearing_dir = os.path.join(ROOT, "Results/satellite_images/clearing_maps")

    for m in mills:
        assert "latitude" in m and "longitude" in m and "company" in m and "mill_name" in m
        assert -90 <= m["latitude"] <= 90
        assert -180 <= m["longitude"] <= 180
        # If a map_image is specified, verify it exists and is > 100 KB
        if m.get("has_map") and m.get("map_image"):
            filename = os.path.basename(m["map_image"])
            img_path = os.path.join(clearing_dir, filename)
            assert os.path.exists(img_path), f"Clearing map missing: {filename}"
            assert os.path.getsize(img_path) > 100_000, f"Clearing map corrupted/empty: {img_path}"


def test_prithvi_batch_evaluation_metrics():
    """Prithvi foundation model evaluation must verify network mean metrics."""
    prithvi_path = os.path.join(ROOT, "Results/prithvi_batch_290.csv")
    df = pd.read_csv(prithvi_path)

    assert len(df) == 290
    mean_rho = df["spearman_rho"].mean()
    mean_iou = df["iou"].mean()

    # Reported in thesis: mean Spearman rho = 0.172, mean IoU = 0.086
    assert mean_rho == pytest.approx(0.172, abs=0.005)
    assert mean_iou == pytest.approx(0.086, abs=0.005)
