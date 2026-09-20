# THESIS EXECUTION PLAN — UPDATED
## Catching Greenwashing from Space
## Status as of 5 September 2026 — 21 days to submission (26 Sep)

---

## HONEST STATUS TODAY — 5 Sep (corrected from the 4 Sep version)

```
DONE:
✅ NLP pipeline — 55 deforestation claims + 403 total tagged claims scored
✅ Satellite — 890,168 ha, 290 mills, verified, 23 tests pass
✅ Sentiment — FinBERT (feeds score) + climate-sentiment (compare), kappa 0.08 disagreement documented
✅ ESG-BERT — 403 claims categorised (data/nlp/claims_enriched.csv)
✅ Scoring layer 0-100 — Results/master_scores.csv, canonical weights, tests pass
✅ Extended buffer 5-30km — Results/buffer_sensitivity.csv (single-mill test: unstable
   at 10 vs 30km, rho 0.49 — argues FOR the full 290-mill design used in the thesis)
✅ Descals oil-palm overlay — 56% of loss near mills is now oil palm (NEW, not in
   original plan — added because it directly strengthens the causation argument)
✅ RADD SAR cross-validation — 4/5 mills confirmed, documented incl. 1 coverage gap
✅ Prithvi-EO-2.0 — 1-mill POC done (Spearman 0.597); 290-mill batch script written,
   Colab/GPU only, not yet run
✅ NLP model comparison — benchmarks + baseline agreement done; gold-label accuracy
   pending (needs YOU to hand-label 150 rows)
✅ Production theory — script + chart built (Results/production_theory.{csv,png}).
   PRODUCTION FIGURES ARE UNVERIFIED PLACEHOLDERS — see "PRODUCTION THEORY" section
   below. Do not cite until replaced with sourced numbers.
✅ Dashboards — 3 HTML files exist (docs/artifacts/)
✅ Agents — 7 Claude Code agents ready
✅ CLAUDE.md — corrected and current (canonical formula, all pending tasks tracked)
✅ ALL 9 thesis chapters drafted in LaTeX (latex/chapters/) — Abstract through
   References, ~14,000+ words, 3 case-study figures wired in, references verified

NOT DONE:
❌ GLAD S2 alerts — genuinely not built. Optional: RADD + Descals + buffer already
   give 3 independent cross-checks: low priority
❌ Production theory — real (sourced) production volumes not obtained
❌ Gold-label NLP evaluation — Results/nlp_gold_labeling_template.csv needs hand-labeling
❌ Prithvi scaled to 290 mills — script ready, needs Colab GPU run
❌ 290 per-mill satellite figures — script ready (generate_clearing_maps.py), needs
   working GEE session
❌ LaTeX compiled to PDF — no TeX locally, needs Overleaf
❌ Website — not started (lowest priority per rule 9 below)
```

**Remaining actual work is refinement + verification + compilation, not building
the pipeline from zero.** The original plan assumed nothing existed yet; most of
Week 1's tasks are already done.

---

## SCORING FORMULA — CANONICAL, VERIFIED, DO NOT CHANGE

```
Score = 0.35 x Forest Loss (% of forest_2000, normalised 0-100)
      + 0.35 x Claim Specificity (ClimateBERT, normalised 0-100)
      + 0.15 x Sentiment (FinBERT positivity, normalised 0-100)
      + 0.15 x Spatial Match (% mills above median loss)
```

Weights sum to 1.0. This matches `scripts/build_scores_v2.py` (which asserts the
sum), `Results/master_scores.csv`, and every LaTeX chapter. The 4 Sep plan's
`0.35/0.35/0.20/0.15` sums to 1.05 and was never actually implemented anywhere —
do not switch to it.

---

## PRODUCTION THEORY — BUILT, BUT NOT YET CITABLE

`scripts/production_theory.py` implements exactly what the original plan asked:
production-normalised deforestation intensity (ha lost per million tonnes CPO).

**Result with placeholder production figures** (do not cite):
```
Rank  Company          ha per million tonnes CPO
1     SIPEF            124,277
2     Genting          116,743
3     SD Guthrie        67,682
4     IOI               67,623
5     Astra Agro        62,284
6     First Resources   61,677
7     Bumitama          55,544
8     GAR               53,511
9     KLK               51,227
10    Musim Mas         27,926
11    Wilmar            15,012
```

This only partly matches the plan's stated theory. Wilmar (largest, most mills)
is indeed least intense, consistent with the theory. But SIPEF and Genting, not
IOI, come out worst per unit with these numbers — a different finding than the
plan assumed. **This ranking will change once real production data replaces the
placeholders.** Before this can go in the thesis:

1. Get each company's actual CPO production tonnage for the same year as its
   sustainability report (2022 or 2023), from its annual report, RSPO ACOP filing,
   or sustainability report itself — not an estimate.
2. Re-run `python scripts/production_theory.py` with real numbers.
3. Only then decide whether to add it as a Results subsection or a Discussion
   point (it competes conceptually with the mismatch score's own per-mill
   normalisation — worth a paragraph explaining how the two relate, not two
   unexplained competing rankings).

**Until sourced, this stays out of the LaTeX thesis.** Citing an unverifiable
number would violate the "every number cited" rule and risks a factual-accuracy
question in the defense.

---

## REMAINING SCHEDULE — 5 Sep to 26 Sep (21 days)

### Days 1-2 (5-6 Sep) — Close out analysis
- [ ] Hand-label `Results/nlp_gold_labeling_template.csv` (150 rows, ~1 hr) then
      `python scripts/model_comparison.py --evaluate`
- [ ] Get real production tonnage for all 11 companies (if keeping production theory)
- [ ] Fix GEE auth (`earthengine authenticate`), then run:
      `generate_clearing_maps.py` (290 clean clearing maps) and/or
      `generate_before_after_comparisons.py all_mills_s2`
- [ ] Optional: GLAD S2 alerts, if time allows

### Days 3-5 (7-9 Sep) — Prithvi + writing prep
- [ ] Run `scripts/prithvi_batch_colab.py` on Colab (GPU), get 290-mill validation table
- [ ] Read the full LaTeX draft end to end once, list gaps (most content already exists —
      this is a review pass, not a from-scratch write)
- [ ] If production theory is verified, write its Results/Discussion paragraphs

### Days 6-10 (10-14 Sep) — Writing: fill gaps only
Most chapters already have full prose. Remaining writing is:
- [ ] Incorporate gold-label NLP accuracy numbers into Results (once labeled)
- [ ] Incorporate 290-mill Prithvi results into Results 4.7 (once run)
- [ ] Incorporate production theory (once sourced) or formally cut it
- [ ] Any GLAD S2 addition (if built)

### Days 11-13 (15-17 Sep) — Send draft, get feedback
- [ ] Send current LaTeX draft PDF to Professor Hoseini (compile on Overleaf first)
- [ ] Start incorporating feedback as it arrives

### Days 14-17 (18-21 Sep) — Full review pass
- [ ] Read start to finish. Checklist: every number cited to Hansen/source, no em
      dashes, no AI vocabulary, every figure captioned, references complete,
      word count near 17,000
- [ ] Fix all issues found

### Days 18-19 (22-23 Sep) — Final polish
- [ ] Format references, page numbers, TOC/LOF/LOT
- [ ] Compile final PDF on Overleaf, check every figure renders, no overfull boxes
- [ ] Website only if everything above is done (lowest priority — see rules)

### Days 20-21 (24-25 Sep) — Final check
- [ ] Read abstract, introduction, conclusion once more
- [ ] Confirm all figures/tables/references render correctly in the PDF
- [ ] Prepare submission documents, check university portal requirements

### Day 22 (26 Sep) — SUBMIT

---

## RULES (kept from original plan, with #6 corrected)

```
1. Do not rebuild anything already verified working — check CLAUDE.md first
2. Every number cites its source (Hansen et al. 2013 for satellite figures,
   the actual filing for any production figures)
3. No em dashes. No AI vocabulary (leverage, robust, comprehensive, pivotal,
   paradigm, foster, delve, seamless, holistic)
4. Scoring formula: 0.35 / 0.35 / 0.15 / 0.15 — never the 0.20 variant
5. Send draft to professor once LaTeX compiles cleanly — do not wait for perfection
6. Website only after the thesis is otherwise submission-ready — cut it first if short on time
7. Submit 26 September — no delay
8. Production theory does not go in the thesis until production figures are sourced
9. Hard stop each day — protect sleep, 21 days is enough if work is not duplicated
```

---

## IF SOMETHING GOES WRONG

**Prithvi 290-mill run fails on Colab:** the 1-mill POC (Spearman 0.597) already
supports Chapter 4.7 and Limitation 6.4. State the POC result, note the scale-up
was attempted, move on.

**GEE will not authenticate:** the 290-image generation and any new satellite
analysis are blocked, but every number already in the thesis was computed before
this and does not depend on GEE working again. Writing is not blocked by this.

**Writing falls behind:** cut production theory first (it is already optional and
uncited), then reduce Literature Review depth. Never cut Results, Methodology,
or Discussion.

**Gold-labeling does not get done:** report the benchmark + baseline-agreement
comparisons only (already built), state the domain-accuracy gold-set as future
work in Limitations. Do not fabricate an accuracy number.
