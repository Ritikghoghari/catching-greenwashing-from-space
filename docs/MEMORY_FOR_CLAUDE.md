# Memory File — Ritik Ghoghari Thesis Session (Sep 15, 2026)
## Paste this into Claude when starting a new conversation

---

## Who I Am
- Name: Ritik Ghoghari
- Degree: M.Sc. Data Science, AI & Digital Business — GISMA University of Applied Sciences, Berlin
- Supervisor: Professor Mohamad Hoseini
- Deadline: 26 September 2026
- Working directory: C:\Users\Allah o akbar\thesis\

---

## Thesis: Catching Greenwashing from Space

Automated pipeline that:
1. Reads palm oil company sustainability reports (PDF)
2. Extracts deforestation claims using NLP models
3. Measures actual forest loss via satellite (Google Earth Engine)
4. Combines both into a mismatch score 0–100
5. High score = company claims zero deforestation but satellites show clearing = greenwashing signal

---

## Verified Numbers — Never Change Without Re-Running

- 11 companies, 290 mills, 890,168 ha post-2020 forest loss
- GAR: 50 mills | 171,236 ha | 13.87%
- SD Guthrie: 42 mills | 142,131 ha | 14.41%
- Wilmar: 45 mills | 127,606 ha | 11.40%
- KLK: 30 mills | 92,209 ha | 12.18%
- Astra Agro: 34 mills | 87,198 ha | 10.76%
- IOI: 15 mills | 74,385 ha | 19.04% (highest intensity)
- Musim Mas: 18 mills | 53,060 ha | 11.45%
- Genting: 15 mills | 44,362 ha | 11.61%
- First Resources: 16 mills | 40,090 ha | 10.29%
- Bumitama: 14 mills | 30,549 ha | 8.66%
- SIPEF: 11 mills | 27,341 ha | 10.42%

---

## Mismatch Score Ranking — Verified

1. KLK — 65.6
2. GAR — 63.1
3. Musim Mas — 56.2
4. IOI — 56.1
5. SD Guthrie — 55.2
6. Wilmar — 50.3
7. First Resources — 41.7
8. Genting — 39.5
9. Bumitama — 38.5
10. SIPEF — 26.1
11. Astra Agro — 17.6

---

## Scoring Formula (CANONICAL — professor approved)

```
Mismatch Score = 0.35 × Forest Loss
              + 0.35 × Specificity
              + 0.15 × Sentiment
              + 0.15 × Spatial Match
```
Weights sum to 1.0. Never use 0.30/0.20 variant — that is stale.

---

## NLP Models (5 total)

1. climatebert/environmental-claims — claim detection (F1 0.981)
2. climatebert/distilroberta-base-climate-specificity — specificity scoring
3. ProsusAI/finbert — sentiment (feeds mismatch score, weight 0.15)
4. climatebert/distilroberta-base-climate-sentiment — comparison signal only
5. nbroad/ESG-BERT — ESG category per claim

---

## Satellite Stack (4 total)

1. Hansen GFC v1.13 via Google Earth Engine — primary loss (30m, 99.5% accuracy)
2. Descals oil palm map — 56% of cleared land = oil palm; IOI 89.8%, Bumitama 16.6%
3. RADD SAR alerts — radar cross-check, confirmed 4 of 5 top mills
4. Prithvi-EO-2.0-300M — foundation model, linear probe ρ=0.805, IoU=0.765

---

## Key Files

- main.ipynb — all analysis
- scripts/build_scores_v2.py — canonical scoring (23 tests pass)
- Results/master_scores.csv — final mismatch scores
- Results/satellite_images/clearing_maps/ — 290 Sentinel-2 clearing maps at 300 DPI
- latex/thesis_latex.zip — Overleaf upload ready
- data/mills/master_forest_loss.csv — 11 companies, 290 mills verified
- docs/MEETING_5_SPEAKING_NOTES.md — full supervisor meeting script
- docs/WEBSITE_SPEAKING_NOTES.md — website walkthrough script
- latex/defense_speaking_notes.html — architecture diagram speaking notes
- diagrams/thesis_architecture.html — pipeline architecture diagram
- website/index.html — interactive showcase website

---

## Best Satellite Images to Show Supervisor

1. Results/satellite_images/clearing_maps/ → ioi_syarimo_clearing_map.png (12,318 ha — highest single mill)
2. gar_nagasakti_clearing_map.png (10,197 ha — GAR worst mill, company claims 99.8% traceability)
3. wilmar_sabahmas_clearing_map.png (clearing every year 2021–2025, unique continuous pattern)
4. astraagro_gunungsejahtera_clearing_map.png (counter-example — big loss, low mismatch score)

---

## Architecture Diagram — 3 Lanes

- Top lane: 11 PDFs → ClimateBERT claim extractor → 55 claims → specificity + sentiment scoring
- Bottom lane: 290 mill GPS → Google Earth Engine → Hansen 10km buffer → forest loss ha
- Two lanes NEVER share data until final scoring engine
- Scoring engine outputs: rankings CSV + website + validation (RADD, Prithvi, Descals)

---

## Buffer Sensitivity

- Tested at 5, 10, 15, 20, 30 km
- 10km canonical (professor approved, matches PalmWatch methodology)
- Adjacent radii stable (ρ=0.80 to 0.96); 10km vs 30km unstable (ρ=0.49)
- NO 2km or 3km buffer images exist in this project

---

## What's 100% Done (as of Sep 8, 2026)

- 290 Sentinel-2 clearing maps at 300 DPI
- Prithvi evaluated across all 290 mills
- Gold-label NLP evaluation (150 rows)
- Interactive website (website/)
- All 9 LaTeX chapters (~14,100 words, 0 em dashes, 0 AI buzzwords)
- Buffer sensitivity 5–30km
- Descals oil palm overlay
- Overleaf zip ready (latex/thesis_latex.zip)
- 23 unit tests passing

## Remaining Human Actions

1. Upload latex/thesis_latex.zip to Overleaf → compile PDF
2. Send compiled PDF to Professor Mohamad Hoseini

---

## Key Limitation (Always Mention)

Forest loss near a mill does not prove causation. Other actors share the catchment area. This measures correspondence, not causation. Same limitation as PalmWatch — documented honestly in the thesis.

---

## Writing Rules

- No em dashes
- No AI vocabulary: leverage, robust, comprehensive, pivotal, holistic, seamless, delve
- Every number cited with Hansen et al. 2013
- Short sentences, human tone

---

## User Preferences

- Communicates in Hinglish (Hindi + English mix)
- Wants visual, supervisor-ready artifacts
- Caveman mode active (terse responses)
- Likes before/after satellite image comparisons for supervisor demos
