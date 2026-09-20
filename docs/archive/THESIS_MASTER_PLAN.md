# Thesis Master Plan — Catching Greenwashing from Space
GISMA University · M.Sc. · Submission Sep 2026
21 Aug – 18 Sep 2026 (28 days) · Updated 27 Aug — 22 days left

---

## Status

**Done:** NLP pipeline (55 claims, ClimateBERT), Satellite layer (890,168 ha post-2020 loss, 290 mills), SD Guthrie bug fixed (2→42 mills), methodology flowchart, literature review HTML, data dashboard (7 charts + explainer), speaking notes, QA guide, methodology chapter drafted (`docs/chapters/03_Methodology.md`, ~2,700 words), year-by-year loss verified for all 11 companies 2021-2025 (`Results/all_companies_yearly_loss_summary.csv`), 55 labeled before/after satellite comparison images, Prithvi-EO-2.0 POC **completed with positive result** (rho=0.597 p<0.0001, precision=0.71, recall=0.71, IoU=0.55, on IOI/SYARIMO mill).

**Professor approved (4th meeting, 21 Aug):**
1. Sentiment analysis in NLP pipeline
2. Prithvi-EO-2.0 model ✅ done, successful
3. Scoring layer 0-100 — **not started, critical path, do first**
4. Start writing NOW, parallel with analysis — methodology chapter done, Results chapter next

---

## Never Cut
Scoring layer · Validation · Methodology chapter · Results chapter

## Cut Order (if time runs short)
1. Website — drop entirely
2. Prithvi — done and successful, don't gold-plate further. One paragraph + numbers in appendix is enough.
3. Sentiment depth — mention model + basic result only
4. Literature Review depth — core 8 papers only
5. Discussion — cut to 1,500 words
6. Buffer sensitivity analysis (5/10/15km) — nice-to-have, cut first if squeezed

---

## Key Numbers (every chapter must trace to master_forest_loss.csv)

```
11 companies · 290 mills · 890,168 ha post-2020 loss
GAR: 171,236 ha · 50 mills · 13.9% · 3,425 ha/mill (highest TOTAL)
IOI: 74,385 ha · 15 mills · 19.0% · 4,959 ha/mill (highest INTENSITY)
Wilmar Sabahmas: 6,675 ha · cleared every year 2021-2025
All 11 companies claim zero deforestation
EUDR cutoff: 31 Dec 2020 · Buffer: 10 km · Hansen: 30 m resolution
```

## Scoring Formula
```
Score = 0.35 × Forest Loss (% of forest_2000)
      + 0.35 × Claim Specificity
      + 0.15 × Sentiment (positive = more concerning)
      + 0.15 × Spatial Match
```
Output: `Results/master_scores.csv` — columns: company, mismatch_score, rank

## Citation Map
| Topic | Cite |
|---|---|
| NLP claim detection | Stammbach et al. 2022 — arXiv:2209.00507 |
| ClimateBERT base | Webersinke et al. 2022 — arXiv:2110.12010 |
| Sentiment analysis | FinBERT — Araci 2019 |
| Every forest loss number | Hansen et al. 2013 — Science 342(6160) |
| 2020 cutoff | EUDR Regulation (EU) 2023/1115 |
| 10 km buffer method | PalmWatch methodology |
| Research gap | Calamai et al. 2026 — arXiv:2502.07541 |
| Verification novelty | Ong et al. 2025 — arXiv:2502.15821 |
| Vague corporate language | Bingler et al. 2022 |
| Attribution limitation | PalmWatch methodology |

---

## Week 1 (21–26 Aug) — DONE

Sentiment analysis, methodology chapter draft, dashboard, all-companies yearly loss, 55 satellite images, Prithvi POC (success). See Status above.

## Week 2 (27 Aug–2 Sep) — Scoring + Validation + Results Draft

| Day | Task |
|---|---|
| 1 (27, TODAY) | Rebuild `scripts/compute_scores.py` for the 3-way formula (below) — currently still 2-way. Everything else blocks on this. |
| 2 (28) | Finish scoring, regenerate `Results/master_scores.csv`, sanity-check (GAR #1 total, IOI #1 intensity should still hold under new scores) |
| 3 (29) | Validation pass — 3-4 case comparisons against GFW GLAD, RSPO complaints, PalmWatch. Doesn't need to be exhaustive. |
| 4-6 (30 Aug-1 Sep) | Write Results chapter, 3,000 words (4.1 NLP, 4.2 Satellite, 4.3 Mismatch scores, 4.4 GAR case, 4.5 IOI case, 4.6 lowest-score case, 4.7 Prithvi POC appendix note) |
| 7 (2) | Buffer day — catch up, review drafts, send to professor if ready |

## Week 3 (3–9 Sep) — Literature Review + Discussion

| Day | Task |
|---|---|
| 8-10 (3-5) | Literature Review, 3,000 words (2.1 Greenwashing/Bingler, 2.2 NLP-ESG/Stammbach+Webersinke, 2.3 Satellite/Hansen+PalmWatch, 2.4 EUDR, 2.5 Gap/Calamai+Ong, 2.6 Novelty) |
| 11-13 (6-8) | Discussion, 2,000 words (5.1 meaning, 5.2 size vs intensity, 5.3 sentiment effect, 5.4 vs PalmWatch/GFW, 5.5 EUDR risk, 5.6 limitations) |
| 14 (9) | Introduction, 1,500 words — write last so it flows from finished chapters |

## Week 4 (10–18 Sep) — Conclusion + Polish + Submit

| Day | Task |
|---|---|
| 15-16 (10-11) | Conclusion (1,000w: findings, gap filled, policy implications, future work) + Abstract (300w, 1 sentence/chapter) |
| 17-18 (12-13) | Full review: every number traces to CSV, every claim cited, no em dashes/AI vocab, figures captioned with Hansen citation, references consistent |
| 19-21 (14-16) | Final polish, reference formatting, word count check (~17,000), proofread |
| 22 (17-18) | **SUBMIT** |

---

## Word Count Target
| Chapter | Words |
|---|---|
| Abstract | 300 |
| Introduction | 1,500 |
| Literature Review | 3,000 |
| Methodology | 3,500 |
| Results | 3,000 |
| Discussion | 2,000 |
| Limitations | 500 |
| Conclusion | 1,000 |
| **Total** | **~17,000** |

---

## Daily Rules
1. Write every day, even 200 words
2. Every number traces back to master_forest_loss.csv
3. Run tests after code change — @qa-tester
4. No em dashes, no AI vocabulary
5. Stuck on analysis → switch to writing. Stuck on writing → switch to analysis.
6. No new features after 4 Sep

---

## Start Now
`scripts/compute_scores.py` → build 3-way formula → regenerate `Results/master_scores.csv` → sanity-check → validation → Results chapter.
