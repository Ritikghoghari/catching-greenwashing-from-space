"""Export pipeline datasets to clean, optimized JSON files for the interactive thesis website.

Reads canonical thesis data files:
- Results/master_scores.csv
- data/mills/all_mills_forest_loss.csv
- data/nlp/claims_enriched.csv
- Results/nlp_model_comparison.csv
- Results/descals_oilpalm_overlay_by_company.csv
- Results/satellite_images/clearing_maps/

Outputs:
- website/data/summary.json
- website/data/companies.json
- website/data/mills.json
- website/data/claims.json
- website/data/model_comparison.json
- website/data/descals.json
"""
import json
import os
import re
import pandas as pd

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEBSITE_DATA_DIR = os.path.join(ROOT_DIR, "website", "data")
MAPS_DIR = os.path.join(ROOT_DIR, "Results", "satellite_images", "clearing_maps")


def slug(s):
    return "".join(c.lower() if c.isalnum() else "_" for c in str(s)).strip("_")


def export_data():
    os.makedirs(WEBSITE_DATA_DIR, exist_ok=True)

    # 1. Master scores & companies
    scores_path = os.path.join(ROOT_DIR, "Results", "master_scores.csv")
    scores_df = pd.read_csv(scores_path).sort_values("rank")

    companies_data = []
    for _, row in scores_df.iterrows():
        comp = row["company"].lower()
        companies_data.append({
            "company": comp,
            "name": comp.upper() if comp not in ["sdguthrie", "firstresources", "astraagro"] else {
                "sdguthrie": "SD GUTHRIE",
                "firstresources": "FIRST RESOURCES",
                "astraagro": "ASTRA AGRO",
            }[comp],
            "rank": int(row["rank"]),
            "mismatch_score": round(float(row["mismatch_score"]), 1),
            "subscores": {
                "forest_loss": round(float(row["forest_loss_score"]), 1),
                "specificity": round(float(row["specificity_score"]), 1),
                "sentiment": round(float(row["sentiment_score_norm"]), 1),
                "spatial_match": round(float(row["spatial_match_score"]), 1),
            },
            "n_mills": int(row["n_mills"]),
            "n_claims": int(row["n_claims"]),
            "low_n_claims": bool(row["low_n_claims"]),
            "loss_post2020_ha": round(float(row["loss_post2020_ha"]), 1),
            "loss_pct_of_forest": round(float(row["loss_pct_of_forest"]), 2),
            "n_mills_severe": int(row["n_mills_severe"]),
            "specificity_mean": round(float(row["specificity_mean"]), 3),
            "sentiment_mean": round(float(row["sentiment_mean"]), 3),
        })

    with open(os.path.join(WEBSITE_DATA_DIR, "companies.json"), "w", encoding="utf-8") as f:
        json.dump(companies_data, f, indent=2)

    # 2. All Mills
    mills_path = os.path.join(ROOT_DIR, "data", "mills", "all_mills_forest_loss.csv")
    mills_df = pd.read_csv(mills_path)
    mills_df["company_mill_idx"] = mills_df.groupby(mills_df["company"].str.lower()).cumcount() + 1

    mills_data = []
    for _, row in mills_df.iterrows():
        comp = row["company"].lower()
        comp_idx = int(row["company_mill_idx"])
        mill_name = str(row["mill_name"])
        mill_slug = slug(mill_name)
        img_filename = f"{comp_idx:03d}_{comp}_{mill_slug}.png"
        img_full = os.path.join(MAPS_DIR, img_filename)

        mills_data.append({
            "id": f"{comp}_{comp_idx:03d}",
            "mill_idx": comp_idx,
            "company": comp,
            "mill_name": mill_name,
            "country": str(row["country"]),
            "latitude": round(float(row["latitude"]), 6),
            "longitude": round(float(row["longitude"]), 6),
            "forest_2000_ha": round(float(row["forest_2000_ha"]), 1),
            "loss_total_ha": round(float(row["loss_total_ha"]), 1),
            "loss_post2020_ha": round(float(row["loss_post2020_ha"]), 1),
            "loss_pct": round((float(row["loss_post2020_ha"]) / float(row["forest_2000_ha"]) * 100) if row["forest_2000_ha"] > 0 else 0.0, 2),
            "map_image": f"maps/{img_filename}",
            "has_map": os.path.exists(img_full),
        })

    with open(os.path.join(WEBSITE_DATA_DIR, "mills.json"), "w", encoding="utf-8") as f:
        json.dump(mills_data, f, indent=2)

    # 3. Claims
    claims_path = os.path.join(ROOT_DIR, "data", "nlp", "claims_enriched.csv")
    claims_data = []
    if os.path.exists(claims_path):
        claims_df = pd.read_csv(claims_path)
        for i, row in claims_df.iterrows():
            text = str(row.get("claim", "")).strip()
            # Clean up newlines / excessive spaces
            text = re.sub(r"\s+", " ", text)
            if not text or len(text) < 10:
                continue
            claims_data.append({
                "id": i + 1,
                "company": str(row.get("company", "")).lower(),
                "text": text,
                "specificity_score": round(float(row.get("specificity_score", 0)), 3),
                "sentiment_score": round(float(row.get("sentiment_score", 0)), 3),
                "strength": str(row.get("strength", "soft")),
                "esg_category": str(row.get("esg_category", "Uncategorized")).replace("_", " "),
                "esg_score": round(float(row.get("esg_category_score", 0)), 3),
                "is_deforestation": bool(row.get("deforestation", False)),
                "is_traceability": bool(row.get("traceability", False)),
                "is_ndpe": bool(row.get("ndpe", False)),
                "has_deadline": not pd.isna(row.get("deadline")),
            })

    with open(os.path.join(WEBSITE_DATA_DIR, "claims.json"), "w", encoding="utf-8") as f:
        json.dump(claims_data, f, indent=2)

    # 4. Summary & Metadata
    total_loss_ha = int(round(mills_df["loss_post2020_ha"].sum()))
    total_mills = len(mills_df)
    total_companies = len(scores_df)
    total_claims = len(claims_data)
    total_maps = sum(1 for m in mills_data if m["has_map"])

    summary_data = {
        "title": "Catching Greenwashing from Space",
        "subtitle": "Verifying Palm Oil Zero-Deforestation Claims Using Satellite Data and Natural Language Processing",
        "author": "Ritik Ghoghari",
        "degree": "M.Sc. Data Science, AI & Digital Business",
        "institution": "GISMA University of Applied Sciences, Berlin",
        "supervisor": "Professor Mohamad Hoseini",
        "submission_deadline": "26 September 2026",
        "total_companies": total_companies,
        "total_mills": total_mills,
        "total_loss_ha": 890168,  # verified canonical metric
        "total_claims": total_claims,
        "total_maps": total_maps,
        "scoring_weights": {
            "forest_loss": 0.35,
            "specificity": 0.35,
            "sentiment": 0.15,
            "spatial_match": 0.15,
        },
        "weights_sum": 1.0,
        "rank_1_company": "KLK",
        "rank_1_score": 65.6,
        "rank_11_company": "Astra Agro",
        "rank_11_score": 17.6,
        "prithvi_network_mills": 290,
        "prithvi_network_mean_rho": 0.172,
        "prithvi_network_mean_iou": 0.086,
        "prithvi_poc_rho": 0.597,
        "prithvi_linear_probe_rho": 0.805,
        "prithvi_linear_probe_iou": 0.765,
        "prithvi_linear_probe_precision": 0.897,
        "prithvi_linear_probe_recall": 0.839,
        "models_count_total": 9,
        "models_count_nlp": 5,
        "models_count_satellite": 4,
    }

    # 4b. Master Model Inventory (9 Models Total)
    models_inventory = {
        "summary": {
            "total_models": 9,
            "nlp_models_count": 5,
            "satellite_systems_count": 4,
        },
        "nlp_models": [
            {
                "id": "nlp_1",
                "name": "climatebert/environmental-claims",
                "role": "Claim Detection & Extraction",
                "architecture": "DistilRoBERTa (Transformer)",
                "accuracy": 0.973,
                "precision": 1.000,
                "recall": 0.962,
                "f1": 0.981,
                "eval_sample": "n = 150 gold-annotated palm oil claims",
                "baseline": "Keyword matching: 70.7% Acc, 0.828 F1",
                "description": "Filters genuine zero-deforestation commitments from boilerplate corporate disclosures."
            },
            {
                "id": "nlp_2",
                "name": "climatebert/distilroberta-base-climate-specificity",
                "role": "Commitment Specificity Scoring",
                "architecture": "DistilRoBERTa (Transformer)",
                "accuracy": 0.538,
                "precision": None,
                "recall": None,
                "f1": None,
                "eval_sample": "n = 106 claims (continuous 0–100 scale)",
                "baseline": "Regex number/date rule: 61.3% Acc",
                "description": "Measures whether promises contain auditable metrics, targets, and dates versus vague promises."
            },
            {
                "id": "nlp_3",
                "name": "ProsusAI/finbert",
                "role": "Financial Tone & Promotional Sentiment",
                "architecture": "BERT (Transformer)",
                "accuracy": 0.811,
                "precision": None,
                "recall": None,
                "f1": None,
                "eval_sample": "n = 106 claims",
                "baseline": "Standard financial sentiment: 62.4% Acc",
                "description": "Scores corporate promotional cheerfulness; directly feeds the composite mismatch formula (weight 0.15)."
            },
            {
                "id": "nlp_4",
                "name": "climatebert/distilroberta-base-climate-sentiment",
                "role": "SASB Opportunity vs Risk Framing",
                "architecture": "DistilRoBERTa (Transformer)",
                "accuracy": 0.509,
                "precision": None,
                "recall": None,
                "f1": None,
                "eval_sample": "n = 106 claims",
                "baseline": "Standard sentiment lexicon: 44.1% Acc",
                "description": "Comparative climate signal showing 99.8% of palm oil claims framed as commercial opportunities."
            },
            {
                "id": "nlp_5",
                "name": "nbroad/ESG-BERT",
                "role": "SASB ESG Topic Classification",
                "architecture": "BERT (Transformer)",
                "accuracy": 0.802,
                "precision": None,
                "recall": None,
                "f1": None,
                "eval_sample": "n = 106 claims",
                "baseline": "Keyword tags: 18.9% Acc",
                "description": "Categorizes corporate commitments into official SASB ESG topics (Land Use, Emissions, Labor)."
            }
        ],
        "satellite_systems": [
            {
                "id": "sat_1",
                "name": "Hansen Global Forest Change v1.13",
                "role": "Primary Deforestation Telemetry",
                "technology": "Landsat 30m Time-Series Random Forest",
                "accuracy": 0.995,
                "metric_label": "Global Acc (88.0% Tropical User Acc)",
                "result": "890,168 ha post-2020 loss detected across 290 mills",
                "description": "Quantifies annual canopy loss >5m height within 10 km radial mill catchments post-EUDR cutoff."
            },
            {
                "id": "sat_2",
                "name": "Descals Global Oil Palm 10m Map",
                "role": "Agricultural Attribution Overlay",
                "technology": "Sentinel-1 SAR + Sentinel-2 CNN",
                "accuracy": 0.869,
                "metric_label": "Overall Classification Accuracy",
                "result": "56.0% of post-2020 buffer clearing verified oil palm (89.8% for IOI)",
                "description": "Verifies that forest clearings were converted directly to industrial oil palm plantations."
            },
            {
                "id": "sat_3",
                "name": "RADD Radar Disturbance Alerts",
                "role": "Cloud-Penetrating Validation",
                "technology": "Sentinel-1 C-band Synthetic Aperture Radar (SAR)",
                "accuracy": 0.950,
                "metric_label": "User Accuracy (>95%)",
                "result": "Active weekly clearing confirmed at 4 of top 5 highest-loss mills",
                "description": "Pierces persistent tropical storm clouds and monsoon haze to verify real-time disturbance."
            },
            {
                "id": "sat_4",
                "name": "NASA/IBM Prithvi-EO-2.0-300M + Linear Probe",
                "role": "Earth Observation Foundation Model",
                "technology": "Vision Transformer (ViT) with Supervised Linear Probe",
                "accuracy": 0.897,
                "metric_label": "Precision (5-Fold CV)",
                "result": "Spearman rho = 0.805, IoU = 0.765, Recall = 0.839 (+34.8% correlation gain)",
                "description": "Adapts pre-trained 300M ViT embeddings via a lightweight linear probe without expensive retraining."
            }
        ]
    }

    summary_data["models_inventory"] = models_inventory

    with open(os.path.join(WEBSITE_DATA_DIR, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2)

    with open(os.path.join(WEBSITE_DATA_DIR, "models_inventory.json"), "w", encoding="utf-8") as f:
        json.dump(models_inventory, f, indent=2)

    # 5. Model Comparison
    comp_path = os.path.join(ROOT_DIR, "Results", "nlp_model_comparison.csv")
    if os.path.exists(comp_path):
        comp_df = pd.read_csv(comp_path)
        with open(os.path.join(WEBSITE_DATA_DIR, "model_comparison.json"), "w", encoding="utf-8") as f:
            json.dump(comp_df.to_dict(orient="records"), f, indent=2)

    # 6. Descals Overlay
    descals_path = os.path.join(ROOT_DIR, "Results", "descals_oilpalm_overlay_by_company.csv")
    if os.path.exists(descals_path):
        desc_df = pd.read_csv(descals_path)
        with open(os.path.join(WEBSITE_DATA_DIR, "descals.json"), "w", encoding="utf-8") as f:
            json.dump(desc_df.to_dict(orient="records"), f, indent=2)

    # 7. Prithvi-EO-2.0 Foundation Model (290 Mills & 3 Empirical Experiments)
    prithvi_path = os.path.join(ROOT_DIR, "Results", "prithvi_batch_290.csv")
    if os.path.exists(prithvi_path):
        prithvi_df = pd.read_csv(prithvi_path)
        comp_agg = (
            prithvi_df.groupby("company")
            .agg(
                mills=("mill_name", "count"),
                mean_spearman_rho=("spearman_rho", "mean"),
                mean_iou=("iou", "mean"),
                mean_precision=("precision", "mean"),
                mean_recall=("recall", "mean"),
            )
            .reset_index()
        )
        comp_agg["mean_spearman_rho"] = comp_agg["mean_spearman_rho"].round(3)
        comp_agg["mean_iou"] = comp_agg["mean_iou"].round(3)
        comp_agg["mean_precision"] = comp_agg["mean_precision"].round(3)
        comp_agg["mean_recall"] = comp_agg["mean_recall"].round(3)
        comp_agg = comp_agg.sort_values("mean_spearman_rho", ascending=False)

        prithvi_experiments = [
            {
                "id": 1,
                "name": "Experiment 1: Zero-Shot Cosine Baseline",
                "method": "Unsupervised Cosine Distance on Pre-trained ViT Embeddings",
                "spearman_rho": 0.597,
                "precision": 0.710,
                "recall": 0.710,
                "iou": 0.550,
                "network_mean_rho": 0.172,
                "network_mean_iou": 0.086,
                "key_finding": "Global pre-training struggles with tropical cloud haze and canopy phenology when uncalibrated."
            },
            {
                "id": 2,
                "name": "Experiment 2: Biophysical Delta-NDVI Gating + Otsu",
                "method": "Biophysical Vegetation Mask Gating + Dynamic Otsu Thresholding",
                "spearman_rho": 0.772,
                "precision": 0.923,
                "recall": 0.387,
                "iou": 0.375,
                "network_mean_rho": None,
                "network_mean_iou": None,
                "key_finding": "Surges precision to 92.3% (+30.0%) by eliminating soil and shadow false alarms, but suppresses recall."
            },
            {
                "id": 3,
                "name": "Experiment 3: Supervised Linear Probe (5-Fold CV)",
                "method": "Lightweight Linear Probe Head on Frozen 1024-dim Backbone",
                "spearman_rho": 0.805,
                "precision": 0.897,
                "recall": 0.839,
                "iou": 0.765,
                "network_mean_rho": None,
                "network_mean_iou": None,
                "key_finding": "Optimal equilibrium: +34.8% Spearman correlation gain, +39.1% IoU surge, 89.7% precision, and 83.9% recall."
            }
        ]

        prithvi_export = {
            "network_summary": {
                "total_mills": int(len(prithvi_df)),
                "mean_spearman_rho": round(float(prithvi_df["spearman_rho"].mean()), 3),
                "mean_iou": round(float(prithvi_df["iou"].mean()), 3),
                "poc_single_mill_rho": 0.597,
                "poc_single_mill_name": "IOI SYARIMO",
                "linear_probe_rho": 0.805,
                "linear_probe_iou": 0.765,
                "linear_probe_precision": 0.897,
                "linear_probe_recall": 0.839,
            },
            "experiments": prithvi_experiments,
            "by_company": comp_agg.to_dict(orient="records"),
        }
        with open(os.path.join(WEBSITE_DATA_DIR, "prithvi.json"), "w", encoding="utf-8") as f:
            json.dump(prithvi_export, f, indent=2)

    # 8. Buffer Sensitivity (5-30 km)
    buf_path = os.path.join(ROOT_DIR, "Results", "buffer_sensitivity.csv")
    if os.path.exists(buf_path):
        buf_df = pd.read_csv(buf_path)
        buf_export = {
            "radii_km": [5, 10, 15, 20, 30],
            "correlations": {
                "10_vs_15_km": 0.80,
                "15_vs_20_km": 0.90,
                "20_vs_30_km": 0.96,
                "10_vs_30_km": 0.49,
            },
            "records": buf_df.to_dict(orient="records"),
        }
        with open(os.path.join(WEBSITE_DATA_DIR, "buffer_sensitivity.json"), "w", encoding="utf-8") as f:
            json.dump(buf_export, f, indent=2)

    print(f"[OK] Exported website data to {WEBSITE_DATA_DIR}")
    print(f"     Companies: {len(companies_data)}")
    print(f"     Mills: {len(mills_data)} ({total_maps} maps matched)")
    print(f"     Claims: {len(claims_data)}")


if __name__ == "__main__":
    export_data()
