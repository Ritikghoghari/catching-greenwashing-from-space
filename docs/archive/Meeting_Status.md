# Meeting Status — Catching Greenwashing from Space
Updated: 2026-08-16. This is the current single source of truth for supervisor meetings.
Older plan docs (`Thesis_6Week_Plan_Handoff.md`, `Thesis_Plan_REVISED.md`) are superseded —
kept for history only. Active plan: `../Thesis_Plan_Professor_Feedback.md`.

---

## 1. Pipeline — what's built and validated

```
PDF Reports → NLP Claims → Claim Strength Score   ─┐
                                                     ├─→ Mismatch Score (0-100)
UML Mills → Earth Engine → Forest Loss (post-2020) ─┘
```

| Layer | Status | Evidence |
|---|---|---|
| 1. NLP claim extraction + strength tagging | ✅ done, 11 companies | `Results/*_tagged.csv`, `Results/master_claims.csv` |
| 2. Hansen forest-loss per mill (post-2020) | ✅ done, 11 companies, 312 mills | `Results/master_forestloss.csv` |
| 3. Satellite images, static + year-by-year, labeled | ✅ done, all 11 | `Results/satellite_images_labeled/` |
| 4. Mismatch score (claim strength + forest loss, 0-100) | ✅ done | `Results/master_scores.csv`, `scripts/scoring.py` |
| 5. Automated tests on scoring + mill-matching + labeling | ✅ 23 tests passing | `scripts/test_*.py` |
| 6. Spatial-match weight, sensitivity analysis (buffer km) | 🔲 not started | Week 2 per active plan |
| 7. External validation, manual NLP audit, case studies | 🔲 not started | Week 3 per active plan |

**Excluded:** Apical — no mills in the Universal Mill List (trading/refining arm, not a
grower). Documented as a transparency-gap limitation, not silently dropped.

---

## 2. Current results — all 11 companies

Sorted by mismatch score (high = claims strongest relative to measured forest loss, i.e.
biggest gap risk). `low_mill_coverage` flags companies with < 5 matched mills, where the
per-mill average is less statistically reliable.

| Company | Claims | Claim Strength | Mills | Post-2020 Loss (ha) | ha/mill | Forest-Loss Score | **Mismatch Score** |
|---|---|---|---|---|---|---|---|
| IOI | 4 | 50.0 | 15 | 74,385 | 4,959 | 100.0 | **75.0** |
| KLK | 1 | 100.0 | 30 | 92,209 | 3,074 | 32.1 | **66.1** |
| SD Guthrie | 15 | 60.0 | 66 | 245,619 | 3,721 | 55.4 | **57.7** |
| Musim Mas | 13 | 61.5 | 18 | 53,060 | 2,948 | 27.6 | **44.6** |
| First Resources | 3 | 66.7 | 16 | 40,090 | 2,506 | 11.7 | **39.2** |
| GAR | 7 | 28.6 | 50 | 171,236 | 3,425 | 44.7 | **36.7** |
| Astra Agro | 2 | 50.0 | 33 | 85,421 | 2,589 | 14.6 | **32.3** |
| SIPEF | 3 | 33.3 | 11 | 27,341 | 2,486 | 10.9 | **22.1** |
| Bumitama | 6 | 33.3 | 14 | 30,549 | 2,182 | 0.0 | **16.7** |
| Genting Plantations | 1 | 0.0 | 14 | 43,054 | 3,075 | 32.2 | **16.1** |
| Wilmar | 3 | 0.0 | 45 | 127,606 | 2,836 | 23.5 | **11.8** |

*Reproduce this table any time with `venv/Scripts/python.exe scripts/compute_scores.py`.*

**How to read it (for the meeting):** the current score is a placeholder 50/50 blend of
claim strength and per-mill forest loss — it is NOT yet the final 3-way weighted score from
the active plan (0.4 forest loss / 0.4 claim specificity / 0.2 spatial match).

**Two UML matching bugs fixed 2026-08-16**, both in `scripts/mill_matching.py` with
regression tests guarding against recurrence:

1. **GAR keyword.** `"GOLDEN AGRI|SMART"` matched only 3 of GAR's 50 real mills — its
   actual UML Group Name is `"SINAR MAS"` (PT SMART Tbk's parent group), not a literal
   "SMART" substring or "GOLDEN AGRI". Fixed keyword: `"GOLDEN AGRI|SINAR MAS"`.
   Tests: `test_gar_keyword_matches_sinar_mas_trading_name`,
   `test_royal_golden_eagle_is_not_matched_as_gar` (the latter guards against
   over-matching "Royal Golden Eagle" — a different, unrelated company group despite the
   similar name).
2. **Non-breaking-space bug.** ~95 UML rows use `\xa0` inside Group Name / Parent Company
   (e.g. `"SIME\xa0DARBY"` — 64 of 65 Sime Darby rows), which a literal-space keyword
   regex silently failed to match. Undercounted SD Guthrie (42→66 mills) and Genting
   (7→14 mills). Fixed with a `normalize_text()` helper (collapses `\xa0` to a regular
   space before matching). Tests: `test_normalize_text_collapses_nonbreaking_space`,
   `test_match_mills_finds_nonbreaking_space_variant`.

Net effect: GAR's mismatch score moved 14.5→36.7, SD Guthrie 52.7→57.7, Genting 0.0→16.1.
Total mills matched across all 11 companies: 234→312. **All downstream files were
regenerated after both fixes:** `master_forestloss.csv`, `master_scores.csv`, dashboard,
and the satellite images for GAR, SD Guthrie, and Genting (bounding boxes changed with
the corrected mill counts).

Audited the other 8 companies' keywords against the UML directly — no further mismatches
found (Astra Agro's 33 vs. an older doc's 34 was checked too: the extra "mill" was a
coincidental "ASTRA" substring match on an unrelated company, Rajawali Nusantara
Indonesia's "Laras Astra Kartika" — 33 is correct, the old 34 was itself wrong).

---

## 3. Satellite image evidence

`Results/satellite_images_labeled/` — 22 images (11 companies × static + year-by-year),
each labeled with company name, mill count, post-2020 loss total, a color legend, and the
Hansen/UMD data-source credit baked directly into the image (band above/below the map, not
overlaid on data pixels).

- `<company>_forestloss.png` — 2-color: forest standing (green) vs. lost after 2020 (red).
- `<company>_forestloss_yearly.png` — year-coded loss, 2019–2025, pale yellow → deep red.

Regenerate labels only (fast, no Earth Engine calls) with:
```
venv/Scripts/python.exe scripts/label_satellite_images.py
```
Regenerate the underlying satellite pulls (slow, needs Earth Engine) with
`generate_satellite_images.py` / `generate_satellite_images_yearly.py`.

---

## 4. Test coverage

23 tests, all passing (`scripts/test_*.py`):

- `test_scoring.py` (6) — claim-strength aggregation, forest-loss normalization including
  the two edge-case bugs fixed this session (`n_mills == 0` division, all-companies-tied
  normalization), mismatch-score combination, inner-join exclusion behavior.
- `test_mill_matching.py` (11) — UML keyword matching against Group Name AND Parent Company
  (catches subsidiaries like Sime Darby's local operator names), case-insensitivity,
  malformed/missing GPS coordinate handling, plus 4 regression tests for the two bugs in
  section 2 (GAR/Sinar Mas keyword, non-breaking-space normalization).
- `test_label_satellite_images.py` (6) — label band sizing, original pixel data left
  untouched by the overlay, legend swatch colors correct.

Run everything:
```
venv/Scripts/python.exe -m pytest scripts/ -v
```

---

## 5. Research paper → methodology map

See `papers_methodology_map.md` — every pipeline decision (claim extraction, hard/soft
split, Hansen dataset choice, 10 km buffer, 2020 cutoff, overall two-track novelty) traced
to a specific paper. Use as the citation spine for the Methodology chapter.

---

## 6. Next (Week 2, per active plan)

- Add spatial-match weight and the real 3-way score:
  `0.4 × forest loss + 0.4 × claim specificity + 0.2 × spatial match`.
- Sensitivity analysis: 5 km vs 10 km vs 15 km buffer — does ranking change?
- Start Methodology chapter (2,000 words).
