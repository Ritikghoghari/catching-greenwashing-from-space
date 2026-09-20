# GEMINI.md — Catching Greenwashing from Space
## Instructions for Antigravity & AI Assistants

---

## Project Overview

- **Thesis:** Catching Greenwashing from Space: Verifying Palm Oil Zero-Deforestation Claims Using Satellite Data and Natural Language Processing
- **Student:** Ritik Ghoghari
- **University:** GISMA University of Applied Sciences, Berlin
- **Degree:** M.Sc. Data Science, AI & Digital Business
- **Supervisor:** Professor Mohamad Hoseini
- **Deadline:** 26 September 2026
- **Working directory:** `C:\Users\Allah o akbar\thesis\`
- **Skill Path:** `.agents/skills/thesis-greenwashing/SKILL.md` (verified present and active)

---

## Canonical Rules & Ground Truth (Do Not Change Without Re-running)

1. **Python Environment**:
   - ALWAYS execute using the dedicated project virtual environment:
     ```powershell
     .\venv\Scripts\python.exe <script>
     ```
   - Google Earth Engine (`ee`), PyTorch, transformers, and geospatial dependencies are installed in `.\venv\`. Global system python does not have `ee` installed.

2. **Scoring Formula (Asserted by scripts, tests, and LaTeX)**:
   $$\text{Mismatch Score} = 0.35 \times \text{Forest Loss} + 0.35 \times \text{Specificity} + 0.15 \times \text{Sentiment} + 0.15 \times \text{Spatial Match}$$
   - Sum of weights = 1.0. The 0.20 variant is strictly invalid.

3. **Core Verified Metrics**:
   - 11 companies · 290 mills · 890,168 ha post-2020 forest loss.
   - KLK rank 1 (65.6), Astra Agro rank 11 (17.6).
   - Test suite: `.\venv\Scripts\python.exe -m pytest scripts/ -q` must show 23 passed.

4. **Tone & Style Rules**:
   - No em dashes (use hyphens, commas, colons, or periods).
   - No AI buzzwords: `leverage`, `robust`, `comprehensive`, `pivotal`, `paradigm`, `foster`, `delve`, `seamless`, `holistic`.
   - Production theory is DROPPED from the thesis pipeline.

---

## Current Project Status (8 September 2026 — 100% Completed)

- **NLP Pipeline**: Complete. 403 claims enriched in `data/nlp/claims_enriched.csv`. Gold evaluation done across 150 rows (`Results/nlp_gold_labeled.csv` & `Results/nlp_model_comparison.csv`). Table 4.5 integrated in Chapter 4.
- **Satellite Maps**: High-res Sentinel-2 clearing maps generator (`scripts/generate_clearing_maps.py`) complete. All 290 mills across all 11 companies generated in `Results/satellite_images/clearing_maps/` (300 DPI comparative maps).
- **Prithvi Foundation Model**: 290-mill batch evaluation complete (`Results/prithvi_batch_290.csv`, network mean Spearman $\rho = 0.172$, IoU = 0.086). Integrated into Chapters 1, 3, 4 (Table 4.7), 5, 6, and 7.
- **Cross-Validations**: RADD SAR radar validation (4/5 mills confirmed), Descals oil palm land cover overlay (56.0% conversion to oil palm), buffer sensitivity (5-30 km) complete.
- **LaTeX Thesis Draft**: All 9 chapters written in `latex/chapters/` (~14,100 prose words; 19,565 total words). Zero em dashes, zero AI buzzwords, zero broken refs. Packaged for Overleaf at `latex/thesis_latex.zip`.
- **Interactive Showcase Website**: Complete in `website/` with Leaflet 290-mill map, satellite image modal, claims explorer, and weight simulator. Data exported via `scripts/build_website_data.py`. Local runner at `scripts/run_website.py`.

---

## Verified Headline Numbers

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

---

## Mismatch Score Ranking — Verified (`scripts/build_scores_v2.py`, 23 tests pass)

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

## Active NLP Model Stack

```python
# Model 1: Claim detection
climatebert/environmental-claims

# Model 2: Specificity scoring
climatebert/distilroberta-base-climate-specificity

# Model 3: Sentiment analysis
ProsusAI/finbert                                    # Feeds mismatch score (sentiment_score)
climatebert/distilroberta-base-climate-sentiment    # Comparison signal (risk/neutral/opportunity)

# Model 4: ESG category
nbroad/ESG-BERT                                     # Topic categorization per claim
```

**Standard pipeline loader:**
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
EUDR_YEAR = 21  # lossyear >= 21 indicates post-2020

# Buffer
BUFFER_M = 10000  # 10 km primary catchment

# Earth Engine evaluation settings
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

## Scoring Formula — Python Reference

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

---

## Known Bugs & Handling Rules

1. **UML GPS coordinates**: Latitude and Longitude columns are frequently corrupt in raw UML exports. Always parse from the "GPS coordinates" text string column.
2. **UML company matching**: Search both `Group Name` AND `Parent Company` columns. Searching only Group Name misses mills (for example, SD Guthrie was 2 mills, now 42 mills after fix).
3. **Dashboard data drift**: Always auto-generate website JSONs via `scripts/build_website_data.py`. Never hand-edit values.
4. **Arrow strings**: Use `regex=False` with `.str.contains()`.
5. **Non-breaking space in UML names**: Normalise whitespace before matching strings.

---

## UML Matching Pattern

```python
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

## Remaining Human Actions Before Submission (Deadline: 26 September 2026)

1. **Overleaf PDF Compilation**:
   - Upload `latex/thesis_latex.zip` to Overleaf.
   - Compile PDF and inspect visual page breaks, table column widths, and figure placement.
2. **Supervisor Review**:
   - Submit the compiled PDF draft to Professor Mohamad Hoseini for feedback.
