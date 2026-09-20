# ML Model Evidence Report
**Thesis:** Catching Greenwashing from Space  
**Student:** Ritik Ghoghari  
**Date:** 16 September 2026  
**Purpose:** Full inventory of implemented models, verified results, and honest gap disclosure

---

## Summary

Nine models/datasets were used across two pipelines (NLP and Satellite). Five have strong verified evidence on palm-oil domain data. Two have moderate evidence. One is inconclusive. One has partial results where a claimed performance figure lacks a batch result file.

---

## NLP Pipeline — 5 Models

### Model 1: climatebert/environmental-claims
**Task:** Identify which sentences in sustainability reports are genuine environmental claims  
**Status: VERIFIED — Strong evidence**

- Input: 11 company PDFs, keyword-filtered candidate sentences
- Output: 403 confirmed claims in `data/nlp/claims_with_sentiment.csv`
- Gold-label evaluation: 150 rows hand-labelled (confirmed claims + rejected candidates)
- Result file: `Results/nlp_model_comparison.csv`

| Metric | Value |
|--------|-------|
| Accuracy | 0.973 |
| Precision | 1.000 |
| Recall | 0.962 |
| F1 | 0.981 |
| vs keyword baseline accuracy | 0.707 |

The model rejects 30% of keyword matches as non-claims. Without it, 30% of "claims" in the dataset would be irrelevant sentences.

---

### Model 2: climatebert/distilroberta-base-climate-specificity
**Task:** Score how specific each claim is (vague pledge vs measurable commitment)  
**Status: VERIFIED — Moderate evidence**

- Specificity score feeds the 0.35 weight in the mismatch formula
- Gold-label evaluation: 102 rows labelled high/medium/low
- Result file: `Results/nlp_model_comparison.csv`

| Metric | Value |
|--------|-------|
| Accuracy | 0.559 |
| vs number/date/% rule baseline | 0.613 |

The rule baseline is marginally higher in accuracy, but the model provides a continuous score (0–1) rather than binary. The continuous score enables finer ranking within companies. This limitation is worth noting.

---

### Model 3: ProsusAI/finbert
**Task:** Sentiment of each claim (positive/neutral/negative) — feeds mismatch score  
**Status: VERIFIED — Strong evidence**

- sentiment_score feeds the 0.15 weight in the canonical mismatch formula
- Gold-label evaluation: 102 rows labelled
- Result file: `Results/nlp_model_comparison.csv`

| Metric | Value |
|--------|-------|
| Accuracy | 0.843 |
| vs climate-sentiment model | 0.529 |

FinBERT significantly outperforms the climate-specific sentiment model on palm-oil domain gold labels. Correct choice for the mismatch formula.

---

### Model 4: climatebert/distilroberta-base-climate-sentiment
**Task:** Climate risk/opportunity framing — comparison signal only  
**Status: VERIFIED — Moderate evidence (comparison role only)**

- Does NOT feed the mismatch score
- Used to show the two "sentiment" models measure different constructs
- Cohen's kappa vs FinBERT = 0.078 (poor agreement), 53% overlap
- Result file: `Results/nlp_sentiment_agreement.csv`

This is reported as a finding: financial tone (FinBERT) and climate risk framing measure different dimensions of corporate language.

---

### Model 5: nbroad/ESG-BERT
**Task:** Classify each claim by ESG topic (Environmental / Social / Governance)  
**Status: VERIFIED — Strong evidence**

- Used for results analysis; does not feed mismatch score
- Gold-label evaluation: 106 rows labelled with E/S/G
- Result file: `Results/nlp_model_comparison.csv`

| Metric | Value |
|--------|-------|
| Accuracy | 0.802 |
| Macro F1 | 0.492 |
| vs keyword baseline accuracy | 0.189 |

Large gap over baseline confirms the model adds real value in topic categorisation.

---

## Satellite Pipeline — 4 Models/Datasets

### Dataset 6: Hansen Global Forest Change v1.13
**Task:** Primary measurement of post-2020 forest loss near each mill  
**Status: VERIFIED — Strong evidence**

- Source: Google Earth Engine `UMD/hansen/global_forest_change_2025_v1_13`
- Result file: `data/mills/master_forest_loss.csv`, `Results/master_scores.csv`
- 23 unit tests pass (pytest scripts/)

| Metric | Value |
|--------|-------|
| Companies | 11 |
| Mills | 290 |
| Total post-2020 loss | 890,168 ha |
| EUDR cutoff | lossyear >= 21 (post-31 Dec 2020) |
| Buffer | 10 km radius |

Forest loss score feeds the 0.35 weight in mismatch formula.

---

### Dataset 7: Descals et al. 2021 Global Oil Palm CNN Map
**Task:** Confirm that forest cleared near mills was converted to oil palm  
**Status: VERIFIED — Strong evidence**

- Source: GEE `projects/sat-io/open-datasets/landcover/GLOBAL_OIL_PALM`
- Result files: `Results/descals_oilpalm_overlay_per_mill.csv`, `_by_company.csv`

| Metric | Value |
|--------|-------|
| % post-2020 loss confirmed oil palm | 56.0% |
| Highest company | IOI (89.8%) |
| Lowest company | Bumitama (16.6%) |

**Important caveat:** This script uses a treecover2000>30% mask, so its loss_ha totals (~695k) differ from the 890,168 ha headline figure. Report the percentage only, not the absolute hectares from this dataset.

---

### Dataset 8: RADD (Radar for Detecting Deforestation)
**Task:** Independent SAR-based cross-check of Hansen results  
**Status: INCONCLUSIVE — Weak evidence, discrepancy**

- Source: GEE `projects/radar-wur/raddalert/v1`
- Result file: `Results/radd_validation_summary.csv`

| Mill | Hansen ha | RADD ha | Agreement ratio |
|------|-----------|---------|-----------------|
| Wilmar/Sabahmas | 6,675 | 0.0 | 0.000 |
| GAR/Naga Sakti | 10,197 | 8.1 | 0.0008 |
| IOI/SYARIMO | 12,318 | 15.0 | 0.0012 |
| KLK/BORNION | 6,768 | 53.9 | 0.008 |
| SD Guthrie/GIRAM | 7,775 | 22.1 | 0.0028 |

Expected agreement ratio (per script documentation): 0.3–1.5. Actual: 0.000–0.008.

**The claim that "RADD confirmed 4 of 5 highest-loss mills" is not supported by these results.** The output file itself labels results "Very low — possible RADD gap or Hansen over-count." Likely cause: RADD covers humid tropical forest disturbance; plantation-adjacent clearing in Southeast Asia may fall outside confident RADD coverage, or the GEE collection version lacked data for these coordinates.

**Recommended correction:** Report RADD as an attempted cross-check that returned inconclusive results due to possible coverage gaps, and remove the "confirmed" language.

---

### Model 9: Prithvi-EO-2.0-300M (IBM/NASA Geospatial Foundation Model)
**Task:** Zero-shot change detection using a geospatial vision transformer  
**Status: PARTIAL — Zero-shot verified; linear probe unverified**

- Result file: `Results/prithvi_batch_290.csv` (290 mills)
- Script: `scripts/prithvi_batch_colab.py` (runs on Colab GPU, not local)

**Zero-shot results (verified):**

| Metric | Value |
|--------|-------|
| Mills evaluated | 290 |
| Mean Spearman rho | 0.172 |
| Range | -0.192 to 0.597 |
| Mean IoU | varies per mill |

**Linear probe claim (ρ = 0.805) — NOT verified in batch output.** This figure appears in early planning notes and the POC readme. The batch script (`prithvi_batch_colab.py`) implements zero-shot inference only — no linear probe training loop is present. No batch linear probe result file exists.

**Recommended correction:** Report zero-shot mean ρ = 0.172 as the verified Prithvi result. The POC single-mill result (SYARIMO, ρ = 0.597) can be reported separately as a proof-of-concept, not generalisable. Remove or qualify the ρ = 0.805 claim.

---

## Evidence File Locations

| File | Contents |
|------|----------|
| `Results/nlp_gold_labeled.csv` | 150-row hand-labelled gold standard |
| `Results/nlp_model_comparison.csv` | Domain-specific accuracy/F1 per model vs baseline |
| `Results/nlp_model_benchmarks.csv` | Published author benchmarks (different test sets — not comparable to above) |
| `Results/nlp_sentiment_agreement.csv` | FinBERT vs climate-sentiment kappa matrix |
| `data/mills/master_forest_loss.csv` | Per-mill Hansen results, 290 mills |
| `Results/master_scores.csv` | Final mismatch scores, 11 companies |
| `Results/descals_oilpalm_overlay_per_mill.csv` | Oil palm conversion per mill |
| `Results/descals_oilpalm_overlay_by_company.csv` | Oil palm conversion aggregated |
| `Results/radd_validation_summary.csv` | RADD vs Hansen, 5 mills — inconclusive |
| `Results/prithvi_batch_290.csv` | Prithvi zero-shot rho/IoU, 290 mills |
| `Results/buffer_sensitivity.csv` | Loss % at 5/10/15/20/30 km radii |
| `scripts/build_scores_v2.py` | Canonical scoring formula + 23 tests |
| `Results/evidence_audit/model_inventory.csv` | Machine-readable summary of this report |

---

## What Needs Correction Before Submission

1. **RADD language**: Replace "RADD confirmed 4 of 5 highest-loss mills" with "RADD cross-check returned inconclusive results (agreement ratios 0.000–0.008, expected 0.3–1.5); possible SAR coverage gap in plantation-dense areas."

2. **Prithvi linear probe**: Either (a) run the linear probe on Colab and produce a result CSV, or (b) replace ρ = 0.805 with "planned but not completed" and report only zero-shot ρ = 0.172.

3. **Specificity model caveat**: Note that the rule baseline marginally outperforms the model in binary accuracy (0.613 vs 0.559) but the model's continuous output is more appropriate for the scoring formula.

4. **Descals hectares**: Do not cite absolute hectares from the Descals overlay — only percentages (56.0%).
