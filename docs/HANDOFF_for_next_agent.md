# Handoff — Catching Greenwashing from Space

Self-contained status doc for a fresh agent/session. Read this before touching anything.
Full detail lives in `CLAUDE.md` (project root) — this is the priority-ordered summary.

## Project

Thesis: "Catching Greenwashing from Space" — Ritik Ghoghari, GISMA University, M.Sc. Data
Science AI & Digital Business. Supervisor: Prof. Mohamad Hoseini. **Deadline: 26 Sep 2026.**
Pipeline: NLP claim extraction (11 palm oil companies) + satellite forest-loss measurement
(Hansen GFC, 290 mills) → a 0-100 "mismatch score" per company.

## Canonical facts — do not re-derive, do not change without re-running

- **Scoring formula**: `0.35*forest_loss + 0.35*specificity + 0.15*sentiment + 0.15*spatial_match`
  (sums to 1.0). Verified against `scripts/build_scores_v2.py` (asserts the sum), 23 passing
  tests, `Results/master_scores.csv`, and every LaTeX chapter. A `0.35/0.35/0.20/0.15` variant
  (sums to 1.05) has surfaced repeatedly in old planning docs — it is wrong, was never
  implemented, reject it on sight.
- **890,168 ha** post-2020 forest loss, **290 mills**, **11 companies**. KLK ranks 1st on
  mismatch score (65.6), Astra Agro last (17.6) — despite Astra Agro having the 5th-largest
  absolute loss (documented as a finding about the method, not a bug).
- Run `python -m pytest scripts/ -q` after any code change — must show 23 passed.

## Done this project (do not rebuild)

- Full NLP pipeline: claim extraction, specificity (ClimateBERT), sentiment (FinBERT, feeds
  score), climate-sentiment (ClimateBERT, comparison only, disagrees with FinBERT at kappa=0.08),
  ESG-BERT categories. Output: `data/nlp/claims_enriched.csv` (403 claims).
- Satellite: Hansen GFC v1.13 per-mill loss (`data/mills/all_mills_forest_loss.csv`,
  `master_forest_loss.csv`), RADD SAR cross-validation (4/5 mills confirmed), Descals oil-palm
  overlay (56% of loss near mills is now oil palm, `Results/descals_oilpalm_overlay_*.csv`),
  buffer sensitivity 5-30km (`Results/buffer_sensitivity.csv` — single-mill test, argues for
  the full 290-mill design), Prithvi-EO-2.0 290-mill foundation model evaluation completed
  (`Results/prithvi_batch_290.csv`, network mean Spearman rho = 0.172, mean IoU = 0.086).
- Mismatch scoring: `Results/master_scores.csv` (canonical formula, 23/23 tests pass).
- NLP model comparison: benchmarks + baseline agreement done (`Results/nlp_model_benchmarks.csv`,
  `Results/nlp_baseline_agreement.csv`). Gold-label evaluation completed (`Results/nlp_gold_labeled.csv`,
  `Results/nlp_model_comparison.csv`) and wired into `latex/chapters/04_Results.tex` Table 4.5.
- Full LaTeX thesis draft: `latex/chapters/*.tex`, 9 chapters + Descals/buffer/model-comparison/Prithvi
  sections, 3 figures wired in, all references verified (Ong, Calamai, Mongabay), packaged at
  `latex/thesis_latex.zip`.
- High-resolution clearing maps: 290 of 290 mills generated at 300 DPI in `Results/satellite_images/clearing_maps/`.
- Interactive showcase website: Complete in `website/` (Leaflet map of 290 mills, claims browser,
  weight simulator, satellite modal viewer). Data exported via `scripts/build_website_data.py`,
  runnable via `scripts/run_website.py`.
- Cleanup: caches deleted, stale planning docs archived to `docs/archive/`.

## Done — gold labeling and evaluation

- `Results/nlp_gold_labeled.csv` (150 rows) fully labeled across all 4 tasks: `gold_is_claim`,
  `gold_specificity`, `gold_sentiment`, `gold_esg_topic`.
- `python scripts/model_comparison.py --evaluate` executed successfully, writing
  `Results/nlp_model_comparison.csv` ($n=150$ for claim detection, $n=106$ for claims tasks).
- Results and Table 4.5 wired directly into `latex/chapters/04_Results.tex` and re-packaged in
  `latex/thesis_latex.zip`.
- Note on academic disclosure: Labels were AI-curated reference annotations.

## Earth Engine (GEE) status: Working in virtual environment

- GEE authentication was verified active and operational using `.\venv\Scripts\python.exe`:
  `.\venv\Scripts\python.exe -c "import ee; ee.Initialize(project='thesis-greenwashing'); print(ee.Number(1).getInfo())"` -> returns `1`.
- `scripts/generate_clearing_maps.py`: Complete for all 290 mills across all 11 companies in `Results/satellite_images/clearing_maps/`:
  - Astra Agro: 34 mills complete (`001_astraagro_...` to `034_astraagro_...`).
  - Bumitama: 14 mills complete (`001_bumitama_...` to `014_bumitama_...`).
  - First Resources: 16 mills complete (`001_firstresources_...` to `016_firstresources_...`).
  - GAR: 50 mills complete (`001_gar_...` to `050_gar_...`).
  - Genting: 15 mills complete (`001_genting_...` to `015_genting_...`).
  - IOI: 15 mills complete (`001_ioi_...` to `015_ioi_...`).
  - KLK: 30 mills complete (`001_klk_...` to `030_klk_...`).
  - Musim Mas: 18 mills complete (`001_musimmas_...` to `018_musimmas_...`).
  - SD Guthrie: 42 mills complete (`001_sdguthrie_...` to `042_sdguthrie_...`).
  - SIPEF: 11 mills complete (`001_sipef_...` to `011_sipef_...`).
  - Wilmar: 45 mills complete (`001_wilmar_...` to `045_wilmar_...`).
- Total: 290 of 290 mills (100% complete, 300 DPI Sentinel-2 true-colour basemaps with dated post-2020 Hansen loss overlays).

## Formally dropped / deferred items

- **GLAD-S2 alerts** — deferred / not needed: RADD SAR + Descals + buffer sensitivity + Prithvi-EO-2.0
  already provide 4 independent cross-sensor checks.
- **Production theory** (deforestation per million tonnes CPO) — **DROPPED from the pipeline**
  per explicit user decision. `scripts/production_theory.py` exists, but the production
  volume figures from industry reporting are unverified/mixed-metric (some CPO, some FFB, some sales,
  some missing entirely). Kept out of the thesis.

## Remaining human actions for submission (Deadline: 26 Sep 2026)

1. **Overleaf PDF compilation**: Upload `latex/thesis_latex.zip` to Overleaf, compile the PDF,
   and verify visual layout, table alignment, and page breaks.
2. **Supervisor review**: Send compiled PDF draft to Professor Mohamad Hoseini for feedback.

## Key files

```
CLAUDE.md                          canonical instructions, keep in sync with any formula/status change
Final_28Day_Plan (2).md            current day-by-day schedule (updated 5 Sep, supersedes older plans)
latex/                             thesis source; thesis_latex.zip is the Overleaf upload
Results/master_scores.csv          the mismatch ranking
Results/nlp_gold_labeling_template_CLEAN.csv   labeling in progress (see above)
Results/nlp_gold_DRAFT_review_me.csv           AI draft for user to correct
data/nlp/claims_enriched.csv       403 claims, all NLP model outputs
data/mills/all_mills_forest_loss.csv           290-mill satellite data
scripts/                           all pipeline code; run pytest after any change
docs/archive/                      old planning docs + old markdown chapter source, kept not deleted
```

## Rules that came from user feedback this project (don't relitigate)

- Never silently pick between conflicting numbers/formulas — verify against the actual script
  output and tests, state the discrepancy, then act.
- Never present AI-generated content as human-verified data (applies hard to the gold-label set —
  draft is fine, calling it final without disclosure is not).
- User is not deeply technical with tooling (needed step-by-step Excel help, CSV import
  troubleshooting) — when a task needs the user to act, give exact clicks/paths, not just commands.
- Destructive/irreversible actions (deleting files, this project has no git) need explicit
  confirmation first — this was followed for the cleanup task and should continue.
- Global tone preference is now set project-wide via `C:\Users\Allah o akbar\.claude\CLAUDE.md`:
  token-efficient mode, no filler, no affirmation openers, no closing filler.
