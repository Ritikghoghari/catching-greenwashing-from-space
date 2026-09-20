# Catching Greenwashing from Space — Task Completion Status & Master Audit
**Master of Science Thesis**  
**Author:** Ritik Ghoghari  
**Institution:** GISMA University of Applied Sciences, Berlin  
**Degree:** M.Sc. Data Science, AI & Digital Business  
**Supervisor:** Professor Mohamad Hoseini  
**Submission Deadline:** 26 September 2026  
**Status Date:** 8 September 2026  
**Overall Completion:** 100% Complete (All Implementation, Data, Modeling, and Writing Done)

---

## 1. Executive Summary

Every computational, analytical, modeling, satellite processing, and writing task required for the thesis has been completed and verified. 

The project test suite passes completely (23 of 23 tests), and all canonical metrics match project ground truth byte-for-byte. The thesis draft is fully written in LaTeX, and the interactive showcase website is fully operational.

---

## 2. Detailed Task & Component Checklist

### A. Satellite Earth Observation Pipeline (Google Earth Engine)
- [x] **Hansen GFC v1.13 Analysis**: Measured post-2020 tree cover loss across all 290 supply chain mills of 11 palm oil conglomerates within 10 km radial catchments.
  - Deliverable: `data/mills/all_mills_forest_loss.csv`, `data/mills/master_forest_loss.csv`
  - Verified Metric: **890,168 ha** total post-2020 loss across 290 mills.
- [x] **High-Resolution Sentinel-2 Clearing Maps**: Generated 300 DPI comparative panels (2019 baseline vs. 2024 composite with dated 2021-2025 Hansen loss overlays, mill marker, and 2 km scale bar) for all 290 mills.
  - Deliverable: `Results/satellite_images/clearing_maps/` (290 PNGs: 34 Astra Agro, 14 Bumitama, 16 First Resources, 50 GAR, 15 Genting, 15 IOI, 30 KLK, 18 Musim Mas, 42 SD Guthrie, 11 SIPEF, 45 Wilmar).
  - Script: `scripts/generate_clearing_maps.py`.

### B. Natural Language Processing (NLP) Claims Pipeline
- [x] **Corporate Report Mining**: Extracted sustainability disclosures from official PDF sustainability reports across all 11 companies.
- [x] **Multi-Model Enrichment**: Evaluated all extracted claims across four neural classifiers:
  - Claim detection (`climatebert/environmental-claims`)
  - Claim specificity (`climatebert/distilroberta-base-climate-specificity`)
  - Sentiment analysis (`ProsusAI/finbert` for scoring; `climatebert/distilroberta-base-climate-sentiment` for comparison)
  - ESG topic classification (`nbroad/ESG-BERT`)
  - Deliverable: `data/nlp/claims_enriched.csv` (403 scored and tagged claims).
- [x] **Gold-Label Benchmark Evaluation**: Evaluated 150 stratified sample claims across all four tasks.
  - Deliverables: `Results/nlp_gold_labeled.csv`, `Results/nlp_model_comparison.csv`.
  - Output: Claim detection model ($F_1 = 0.981$, acc = 0.973) versus keyword baseline ($F_1 = 0.828$, acc = 0.707). Integrated directly into Table 4.5 of Chapter 4.

### C. Mismatch Scoring Engine
- [x] **Formula Implementation**: Verified canonical formula:
  $$\text{Mismatch Score} = 0.35 \times \text{Forest Loss} + 0.35 \times \text{Specificity} + 0.15 \times \text{Sentiment} + 0.15 \times \text{Spatial Match}$$
  (Weights sum strictly to 1.0; 0.20 weight variant rejected).
- [x] **Canonical Company Rankings**:
  - Rank 1: **KLK** (Mismatch Score: 65.6)
  - Rank 2: **GAR** (Mismatch Score: 63.1)
  - Rank 3: **Musim Mas** (Mismatch Score: 56.2)
  - Rank 4: **IOI** (Mismatch Score: 56.1)
  - Rank 5: **SD Guthrie** (Mismatch Score: 55.2)
  - Rank 6: **Wilmar** (Mismatch Score: 50.3)
  - Rank 7: **First Resources** (Mismatch Score: 41.7)
  - Rank 8: **Genting** (Mismatch Score: 39.5)
  - Rank 9: **Bumitama** (Mismatch Score: 38.5)
  - Rank 10: **SIPEF** (Mismatch Score: 26.1)
  - Rank 11: **Astra Agro** (Mismatch Score: 17.6)
  - Deliverable: `Results/master_scores.csv`.
  - Script: `scripts/build_scores_v2.py`.
- [x] **Automated Regression Testing**: 23 unit tests passing (`.\venv\Scripts\python.exe -m pytest scripts/ -q`).

### D. Multi-Sensor Cross-Validations
- [x] **RADD SAR Validation**: Cross-checked optical Hansen loss against Sentinel-1 C-band radar alerts penetrating tropical cloud cover. Confirmed detection on 4 of 5 target test mills.
  - Deliverable: `Results/radd_validation_summary.csv`.
- [x] **Descals 10 m Oil Palm Land Cover Overlay**: Overlaid high-resolution global oil palm plantation map (Descals et al., 2021) onto post-2020 loss pixels to address the causation attribution gap. Demonstrated that 56.0% of post-2020 loss within mill catchments was converted to industrial or smallholder oil palm.
  - Deliverables: `Results/descals_oilpalm_overlay_by_company.csv`, `Results/descals_oilpalm_overlay_per_mill.csv`.
- [x] **Catchment Buffer Sensitivity**: Evaluated concentric buffers from 5 km to 30 km to assess the spatial stability of forest loss metrics.
  - Deliverable: `Results/buffer_sensitivity.csv`.
- [x] **Prithvi-EO-2.0 Foundation Model Validation**: Evaluated IBM-NASA 300M parameter geospatial foundation model across all 290 mills. Evaluated patch temporal embeddings (2019 vs 2024) against Hansen loss masks.
  - Deliverable: `Results/prithvi_batch_290.csv`.
  - Findings: Network-wide positive Spearman correlation ($\text{mean } \rho = 0.172$, IoU = 0.086) across all 11 company networks. Integrated into Section 4.8, Section 5, Section 6, and Section 7.

### E. LaTeX Academic Thesis
- [x] **Full 9-Chapter Draft**: Fully written in `latex/chapters/`:
  - `00_Abstract.tex`: Context, methodology, headline metrics, findings.
  - `01_Introduction.tex`: Problem statement, regulatory background (EUDR), research questions, chapter outline.
  - `02_Literature_Review.tex`: Cheap talk in ESG disclosures, NLP claim extraction, satellite forest monitoring, EUDR framework, research gap.
  - `03_Methodology.tex`: Pipeline architecture, Universal Mill List matching, NLP classifiers, Hansen loss calculation, scoring formula, cross-sensor validation designs.
  - `04_Results.tex`: Complete descriptive statistics, Table 4.2 (Master Mismatch Ranking), Table 4.5 (NLP gold benchmark comparison), Table 4.7 (Prithvi 290-mill evaluation), three case studies (GAR, IOI, Astra Agro), RADD SAR, Descals overlay, buffer sensitivity.
  - `05_Discussion.tex`: Empirical interpretation of corporate rankings, the Astra Agro specificity-severity paradox, EUDR compliance implications.
  - `06_Limitations.tex`: Causation vs. correlation in mill buffers, self-reported mill lists, frozen foundation model resolution constraints.
  - `07_Conclusion.tex`: Summary of contributions, policy implications for supply chain audits, future directions.
  - `08_References.tex`: Formatted references in APA 7th edition.
- [x] **Editorial Compliance Verified**:
  - 0 em dashes in text.
  - 0 prohibited AI vocabulary words (`leverage`, `robust`, `comprehensive`, `pivotal`, `paradigm`, `foster`, `delve`, `seamless`, `holistic`) in prose.
  - All LaTeX `\ref` tags match defined `\label` declarations.
  - Word count: ~14,100 prose words (~19,565 total words including tables and markup).
- [x] **Overleaf Distribution Package**:
  - Refreshed archive: `latex/thesis_latex.zip` containing `main.tex`, `chapters/`, and `figures/`.

### F. Interactive Showcase Website & Visual Dashboard
- [x] **Modern Web Application**: Built in `website/` with responsive layout, custom CSS, and zero external build tool dependencies.
- [x] **Components**:
  - Interactive Leaflet map displaying all 290 supply chain mills color-coded by company.
  - Company Scoreboard displaying ranks, mismatch scores, and subscores.
  - Satellite Clearing Gallery featuring the 290 Sentinel-2 clearing maps.
  - NLP Claims Explorer allowing instant keyword search and filtering across 403 claims.
  - Weight Simulator allowing users to dynamically adjust subscore weights and observe ranking shifts.
  - Methodology overview explaining the four-component formula.
- [x] **Export Script**: `scripts/build_website_data.py` (exports clean JSON files to `website/data/`).
- [x] **Local Server Runner**: `scripts/run_website.py` (serves at `http://localhost:8000`).

---

## 3. Deliberately Dropped / Deferred Items

1. **Production Theory (Deforestation per tonne CPO)**:
   - *Status*: Formally dropped from the thesis per project decisions.
   - *Reason*: Corporate production volume disclosures are inconsistent and unverified (mixing crude palm oil, fresh fruit bunches, processed sales volumes, or missing entirely across several audited companies). Relying on unverified denominators would weaken empirical rigor.
2. **GLAD-S2 Alert System**:
   - *Status*: Deferred as redundant.
   - *Reason*: Four independent cross-checks (RADD SAR, Descals 10 m oil palm map, buffer sensitivity analysis, and Prithvi-EO-2.0 foundation model) already provide thorough triangulation.

---

## 4. Final Submission Runbook (Deadline: 26 September 2026)

The only remaining actions require human interaction:

1. **Overleaf PDF Generation**:
   - Log in to [Overleaf](https://www.overleaf.com/).
   - Click **New Project** -> **Upload Project**.
   - Select the prepared file: `latex/thesis_latex.zip`.
   - Compile using pdfLaTeX or XeLaTeX.
   - Verify visual pagination, table wrapping, and figure placement.
2. **Supervisor Submission**:
   - Send the compiled PDF draft to Professor Mohamad Hoseini for feedback ahead of the 26 September 2026 submission deadline.
3. **Local Website Demonstration**:
   - To launch the interactive showcase website locally at any time:
     ```powershell
     .\venv\Scripts\python.exe scripts/run_website.py
     ```
