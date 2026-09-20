# CLAUDE.md — Catching Greenwashing from Space
## Instructions for Claude Code

---

## Project Overview

**Thesis:** Catching Greenwashing from Space
**Student:** Ritik Ghoghari
**University:** GISMA University of Applied Sciences, Berlin
**Degree:** M.Sc. Data Science, AI & Digital Business
**Supervisor:** Professor Mohamad Hoseini
**Deadline:** 26 September 2026
**Working directory:** C:\Users\Allah o akbar\thesis\

---

## What This Project Does

Automated pipeline that:
1. Reads palm oil company sustainability reports (PDF)
2. Extracts deforestation claims using NLP models
3. Measures actual forest loss via satellite (Google Earth Engine)
4. Combines both into a mismatch score 0-100
5. High score = company claims zero deforestation but satellites show clearing = greenwashing signal

---

## Project Structure

```
thesis/
├── main.ipynb                    # Main notebook — all analysis here
├── data/
│   ├── mills/
│   │   ├── master_forest_loss.csv    # VERIFIED — 11 companies, 290 mills
│   │   └── all_mills_forest_loss.csv # Per-mill data
│   ├── nlp/
│   │   ├── gar_specific_claims.csv   # GAR claims with scores
│   │   └── claims_with_sentiment.csv # All claims + sentiment (new)
│   └── data_array.js                 # Auto-generated for dashboard
├── Results/
│   ├── master_scores.csv             # Mismatch scores 0-100
│   ├── buffer_sensitivity.csv        # 5-30km analysis (pending)
│   ├── nlp_model_comparison.csv      # 4 model comparison (pending)
│   └── radd_validation_summary.csv   # RADD results (done)
├── latex/                            # Thesis LaTeX (Overleaf upload)
├── scripts/
│   └── build_scores_v2.py            # CANONICAL scoring script
├── .claude/
│   └── agents/                       # All 7 agents here
└── CLAUDE.md                         # This file
```

---

## Verified Numbers — NEVER CHANGE WITHOUT RE-RUNNING

```
Total: 11 companies · 290 mills · 890,168 ha post-2020 loss

GAR:             50 mills | 171,236 ha | 13.87% | 3,425 ha/mill
SD Guthrie:      42 mills | 142,131 ha | 14.41% | 3,384 ha/mill
Wilmar:          45 mills | 127,606 ha | 11.40% | 2,836 ha/mill
KLK:             30 mills |  92,209 ha | 12.18% | 3,074 ha/mill
Astra Agro:      34 mills |  87,198 ha | 10.76% | 2,565 ha/mill
IOI:             15 mills |  74,385 ha | 19.04% | 4,959 ha/mill
Musim Mas:       18 mills |  53,060 ha | 11.45% | 2,948 ha/mill
Genting:         15 mills |  44,362 ha | 11.61% | 2,957 ha/mill
First Resources: 16 mills |  40,090 ha | 10.29% | 2,506 ha/mill
Bumitama:        14 mills |  30,549 ha |  8.66% | 2,182 ha/mill
SIPEF:           11 mills |  27,341 ha | 10.42% | 2,486 ha/mill
```

If any code produces different numbers — STOP and debug before proceeding.

---

## Mismatch Score Ranking — VERIFIED (build_scores_v2.py, 23 tests pass)

```
Rank Company          Mismatch  Loss   Spec   Sent   Spatial
1    KLK              65.6      33.9   100.0  68.4   56.7
2    GAR              63.1      50.2   67.6   91.6   54.0
3    Musim Mas        56.2      26.9   85.1   63.6   50.0
4    IOI              56.1      100.0  0.0    60.3   80.0
5    SD Guthrie       55.2      55.4   32.9   100.0  61.9
6    Wilmar           50.3      26.4   67.2   70.0   46.7
7    First Resources  41.7      15.7   75.6   27.8   37.5
8    Genting          39.5      28.4   46.6   41.4   46.7
9    Bumitama         38.5      0.0    67.1   71.4   28.6
10   SIPEF            26.1      17.0   28.3   41.0   27.3
11   Astra Agro       17.6      20.2   13.8   0.0    38.2
```

---

## NLP Models — Active Stack

```python
# Model 1 — Claim detection (DONE)
climatebert/environmental-claims

# Model 2 — Specificity scoring (DONE)
climatebert/distilroberta-base-climate-specificity

# Model 3 — Sentiment analysis (DONE)
ProsusAI/finbert                                    # feeds mismatch score (sentiment_score)
climatebert/distilroberta-base-climate-sentiment    # comparison signal (climate_sentiment: risk/neutral/opportunity)

# Model 4 — ESG category (DONE)
nbroad/ESG-BERT                                     # esg_category per claim
```

Models 4 + 5 added via `scripts/enrich_claims_models.py` -> `data/nlp/claims_enriched.csv`
(403 claims). New columns only; mismatch score unchanged.

**Load all models:**
```python
from transformers import pipeline

claims_clf = pipeline("text-classification",
    model="climatebert/environmental-claims",
    return_all_scores=True)

specificity_clf = pipeline("text-classification",
    model="climatebert/distilroberta-base-climate-specificity",
    return_all_scores=True)

sentiment_clf = pipeline("text-classification",
    model="climatebert/distilroberta-base-climate-sentiment",
    return_all_scores=True)

esg_clf = pipeline("text-classification",
    model="nbroad/ESG-BERT",
    return_all_scores=True)
```

---

## Satellite Stack — Google Earth Engine

```python
# GEE project
PROJECT = "thesis-greenwashing"

# Primary dataset
HANSEN = "UMD/hansen/global_forest_change_2025_v1_13"

# EUDR cutoff
EUDR_YEAR = 21  # lossyear >= 21 means post-2020

# Buffer
BUFFER_M = 10000  # 10 km primary

# Always include
MAX_PIXELS = 1e10
SCALE = 30
```

**Standard initialization:**
```python
import ee
ee.Initialize(project='thesis-greenwashing')
hansen = ee.Image("UMD/hansen/global_forest_change_2025_v1_13")
pixel_ha = ee.Image.pixelArea().divide(10000)
```

---

## Scoring Formula — CANONICAL (professor-approved, weights sum to 1.0)

This is the ONLY correct version. It matches `scripts/build_scores_v2.py`
(which asserts the weights sum to 1.0), `Results/master_scores.csv`, and the
LaTeX thesis (Methodology Eq. 1, Results Table 4.2). Any 0.30 / 0.20 variant
seen in older planning notes is STALE — do not use it, and do not "fix"
CLAUDE.md toward it.

```python
def mismatch_score(forest_loss_pct, specificity,
                   sentiment_positive, spatial_match):
    score = (
        0.35 * forest_loss_pct +    # % of forest_2000 lost post-2020, normalised 0-100
        0.35 * specificity +        # claim specificity, normalised 0-100
        0.15 * sentiment_positive + # claim positivity, normalised 0-100
        0.15 * spatial_match        # % of company mills above dataset median per-mill loss
    )
    return round(min(100, max(0, score)), 1)
```

**Rule: if the formula ever changes, update all three together in the same
commit — `scripts/build_scores_v2.py`, `latex/chapters/03_Methodology.tex`
+ `04_Results.tex`, and this file. Then re-run `build_scores_v2.py` and paste
the new ranking table above.**

---

## Known Bugs — Already Fixed

1. **UML GPS coordinates** — Latitude/Longitude columns corrupted.
   Fix: Always parse from "GPS coordinates" text column.

2. **UML company matching** — Search BOTH Group Name AND Parent Company.
   Fix: SD Guthrie was 2 mills, now 42 mills after fix.

3. **Dashboard data drift** — JS array was hand-copied.
   Fix: Auto-generate via data/data_array.js script.

4. **Arrow strings** — Use regex=False with .str.contains()

5. **Non-breaking space in UML names** — normalise whitespace before matching.

---

## UML Matching — Correct Code

```python
# ALWAYS use this pattern — never search only one column
def match_company(uml_df, group_col, keyword):
    mask = (
        uml_df[group_col].str.contains(
            keyword, case=False, na=False, regex=False)
        | uml_df["Parent Company"].str.contains(
            keyword, case=False, na=False, regex=False)
    )
    return uml_df[mask].drop_duplicates(subset=["GPS coordinates"])
```

---

## Mill Coordinates — Representative Mills

```python
MILL_COORDS = {
    "GAR":             [110.5158,    -2.1404],
    "SD Guthrie":      [118.060186,   4.704457],
    "Wilmar":          [118.405246,   5.179162],
    "KLK":             [103.270394,   2.204546],
    "Astra Agro":      [121.484959,  -2.129894],
    "IOI":             [117.398389,   6.002431],
    "Musim Mas":       [102.030838,   0.077043],
    "Genting":         [103.209291,   1.856092],
    "First Resources": [100.926111,   0.580556],
    "Bumitama":        [113.060706,  -1.993167],
    "SIPEF":           [151.01097,   -5.311111],
}
```

---

## Standard Tests — Run After Every Code Change

```
python -m pytest scripts/ -q      # 23 tests, all must pass
python scripts/build_scores_v2.py # ranking must match table above, byte-for-byte
```

Master CSV invariants: 11 rows, n_mills sum == 290, loss sum ≈ 890,168 ha.

---

## 7 Agents Available

```
@thesis-planner          — weekly plan, priority, deadlines
@geospatial-scientist    — Python, data, code fixes
@earth-engine-specialist — GEE scripts only (sub-agent)
@satellite-specialist    — satellite images, visualization
@qa-tester               — tests, bugs, validation
@writer-presenter        — thesis writing, emails, slides
@latex-specialist        — LaTeX formatting, compile, PDF
```

---

## Tasks Completion Status — 100% Completed (8 Sep 2026)

```
COMPLETED:
  - 290 high-resolution Sentinel-2 clearing maps generated at 300 DPI (Results/satellite_images/clearing_maps/)
  - Prithvi-EO-2.0 foundation model evaluated across all 290 mills (Results/prithvi_batch_290.csv, mean rho = 0.172)
  - Gold-label NLP evaluation completed across 150 rows (Results/nlp_gold_labeled.csv, Results/nlp_model_comparison.csv)
  - Interactive showcase website fully built in website/ (data exported via scripts/build_website_data.py)
  - All 9 LaTeX chapters drafted in latex/chapters/ (~14,100 prose words; 0 em dashes, 0 buzzwords)
  - Buffer sensitivity 5-30 km completed (Results/buffer_sensitivity.csv)
  - Descals oil palm overlay completed (56.0% loss to oil palm, Results/descals_oilpalm_overlay_*.csv)
  - Overleaf archive refreshed (latex/thesis_latex.zip)
  - 23 unit tests passing (python -m pytest scripts/ -q)

FORMALLY DROPPED / DEFERRED:
  - Production theory: DROPPED per project decisions (industry reporting figures unverified)
  - GLAD-S2 alerts: Deferred as unnecessary (RADD + Descals + buffer + Prithvi provide 4 cross-checks)

REMAINING HUMAN ACTIONS (Deadline: 26 Sep 2026):
  1. Upload latex/thesis_latex.zip to Overleaf and compile PDF
  2. Send compiled PDF draft to Professor Mohamad Hoseini for review
```


## Model comparison — how it works (scripts/model_comparison.py)

The 5 models do different tasks; no single accuracy ranking exists. Three outputs:
- `Results/nlp_model_benchmarks.csv` — each model's published accuracy/F1 (authors' data, cited)
- `Results/nlp_sentiment_agreement.csv` — FinBERT vs climate-sentiment: kappa 0.078 (poor),
  53% agreement -> they measure different things, report both, not interchangeable
- `Results/nlp_gold_labeling_template.csv` — 112 claims, hand-label to get palm-oil-domain
  accuracy (the number the thesis reports)

---

## Writing Rules — Apply Always

- No em dashes — use comma or period
- No AI vocabulary: leverage, robust, comprehensive,
  pivotal, paradigm, foster, delve, seamless, holistic
- Every number cited: "890,168 ha (Hansen et al., 2013)"
- Every figure has caption with data source
- Short sentences — human, not robotic

---

## Research Papers — Cite Correctly

```
Stammbach 2022  → arXiv:2209.00507 → NLP claim model
Webersinke 2022 → arXiv:2110.12010 → ClimateBERT base
Hansen 2013     → Science 342(6160) → every forest loss number
EUDR 2023/1115  → EU law          → 2020 cutoff justification
PalmWatch       → IDI methodology  → 10km buffer + limitation
Calamai 2026    → arXiv:2502.07541 → research gap + design
Ong 2025        → arXiv:2502.15821 → novelty
Bingler 2022    → Finance Research Letters → cheap talk
Araci 2019      → arXiv:1908.10063 → FinBERT / sentiment
```

---

## Satellite-side ML — options (not yet built except Prithvi POC)

Tier 0 — products, no training, fast, high thesis value:
  - Descals et al. global oil palm map (10m, GEE / Zenodo) — overlay on post-2020
    loss = "% of cleared land near each mill now oil palm". Attacks causation gap.
  - JRC Tropical Moist Forest (GEE projects/JRC/TMF) — 2nd deforestation source
  - ESA WorldCover / Google Dynamic World (GEE) — land cover after clearing
  - GLAD-S2 / GLAD-L alerts (GEE) — 2nd alert system next to RADD

Tier 1 — foundation-model embeddings + light classifier (Prithvi POC exists, 1 mill):
  - ibm-nasa-geospatial/Prithvi-EO-2.0-300M via terratorch — scale POC to 30+ mills
  - made-with-clay/Clay v1.5 — alternative geospatial FM, simpler API
  - Allen AI SatlasPretrain — ready land-cover / change heads

Tier 2 — fine-tune segmentation (heavy, skip unless time):
  - Prithvi + UNet head (terratorch), weak labels = Hansen loss pixels ->
    10m clearing masks, catches small clearings Hansen 30m misses

Deadline call: do Descals overlay + scale Prithvi. Skip Tier 2.

DONE: scripts/descals_oilpalm_overlay.py -> Results/descals_oilpalm_overlay_{per_mill,by_company}.csv
  FULL 290 mills: 56.0% of post-2020 loss near mills is oil palm (Descals 2021), 44% industrial.
  Range: IOI 89.8% (highest) -> Bumitama 16.6% (lowest). Add as Results section 4.x.
  CAVEAT: script uses treecover2000>30 mask so its loss_ha totals (~695k) differ from the
  890,168 headline (different mask). Report the PERCENTAGE, not the absolute ha, or re-run
  with the exact mask from the main pipeline for consistency.

## Key Limitation — Always Mention

Forest loss near a mill does not prove causation.
Other actors share the catchment area.
Measuring correspondence — not causation.
Same limitation as PalmWatch — document honestly.

---

## Never Do These

- Never change verified numbers without re-running full pipeline
- Never use the 0.35 / 0.30 / 0.20 / 0.15 weights — that version is stale
- Never cite a number without Hansen et al. 2013 reference
- Never use raw hectares alone — always add % and ha/mill
- Never skip tests after code changes
