# Thesis Plan — REVISED
### Catching Greenwashing from Space · 6 weeks to submission

> **This supersedes the earlier 6-week plan.** The pipeline design has not changed.
> The *order of work* has. Five things were wrong in the previous version and are
> corrected here. Section 2 explains what changed and why.

---

## 1. What has not changed

The project, the 4-layer pipeline, the models, the datasets, the EUDR framing, and the
novelty claim vs. PalmWatch are all unchanged and correct. See the previous handoff
document for the pipeline description and working code — those sections remain valid.

---

## 2. What changed, and why

| # | Previous plan | Problem | Revised |
|---|---|---|---|
| 1 | No validation step anywhere | The examiner's first question — *"how do you know the score is right?"* — had no answer allocated to it | Validation gets its own dedicated block in Week 3 |
| 2 | Writing starts Week 5 | 17,000 words in the final two weeks, alongside a website and unfinished analysis. This is the most common cause of thesis failure, and it is not a research problem | Writing starts Week 1 and runs in parallel throughout |
| 3 | Website gets a full week (Week 5) | Lowest-value item for the grade, given equal billing with writing | Moved to optional, end-of-project, only if Weeks 1–4 complete on time |
| 4 | Prithvi gets a full week (Week 4) | Highest-risk item, scheduled before validation and before writing | Time-boxed to 3 days, scheduled after validation, explicitly droppable |
| 5 | No reproducibility checkpoint | Multi-company results exist, but the multi-mill loop has not been demonstrably re-run end to end | Day 1 task: reproduce one company's number from raw UML, by hand |

**The principle behind all five changes:** the thesis is graded on a written document that
defends a method. It is not graded on how many components were built. Everything that does
not end up as defensible text in the document is optional.

---

## 3. Revised week-by-week plan

### WEEK 1 — Lock the foundation, start writing

**Priority A — Reproducibility (Days 1–2)**

Write and run a script that, for a single named company, reads the Universal Mill List,
filters to that company's mills (remembering former names — SD Guthrie appears as
"SIME DARBY"), loops `mill_forest_loss` over every mill, and returns a company total split
before/after 2020.

Run it on Wilmar. Check the output against the figure already on record. If it matches,
the results are yours and reproducible. If it does not, find out why now, not in the viva.

Then run it across the full sample and save one master CSV:

```
company | n_mills | forest_2000_ha | loss_total_ha | loss_post2020_ha | loss_pct_of_forest
```

**Priority B — Start the Methodology chapter (Days 3–5)**

Every decision needed to write this chapter has already been made: sample selection, the
10 km buffer, the 2020 cut-off, the two ClimateBERT models, the Hansen dataset, the
secondary-data design, the attribution limitation. Write it now, while it is fresh.

Target: 2,000 words drafted by end of week. It does not need to be good yet.

**End of week:** master CSV reproducible from raw data + Methodology draft started.

---

### WEEK 2 — Scoring layer + keep writing

Build Layer 3. Combine three components into a 0–100 mismatch score per company:

- **Evidence magnitude** — post-2020 loss, normalised across the sample
- **Claim strength** — from the specificity model's continuous score, not the binary label
- **Spatial-temporal correspondence** — does the observed loss fall within the region and
  timeframe the claim actually covers

Document every weighting choice as you make it, in the Methodology chapter. Undocumented
weights are indefensible weights.

Also run the sensitivity check: recompute scores at 5 km and 15 km buffers. If the ranking
holds, that is a robustness finding worth a paragraph. If it does not, that is a limitation
worth a paragraph. Either outcome is useful.

**Writing in parallel:** finish Methodology (3,500 words), start Results.

**End of week:** scores for all companies + Methodology chapter complete in draft.

---

### WEEK 3 — Validation (the block that was missing)

This is the week that determines whether the thesis is defensible.

**Task 1 — External case comparison.** Take the highest-scoring companies and check them
against independent records: Global Forest Watch alerts and investigations, published NGO
reports, PalmWatch findings, RSPO complaint records. If high-score companies recur in
documented cases and low-score companies do not, the score has construct validity. Write
down what you find either way, including disconfirming cases.

**Task 2 — Manual claim audit.** Take a random sample of 20 extracted claims. Open the
source PDFs. Check whether each was correctly classified and whether the sentence was
cleanly extracted or garbled by the PDF parser. Report the error rate honestly. This is
your answer to *"how reliable is your NLP layer?"*

**Task 3 — Case studies.** Two high-score and one low-score company, written up properly
with the claim text, the measured loss, the imagery, and the score.

**Writing in parallel:** Results chapter (3,000 words).

**End of week:** validation evidence + Results drafted. **At this point the thesis is
defensible even if nothing else gets built.**

---

### WEEK 4 — Prithvi (time-boxed) + Literature Review

**Prithvi: 3 days maximum, hard stop.**

Run Prithvi-EO-2.0 on Sentinel-2 for one region on Colab. Compare its detection against
Hansen for the same area. Report precision, recall, F1. That is enough for a
proof-of-concept section.

If it is not working by day 3, stop and write it up as an attempted extension with an
honest account of the constraints encountered. An examiner respects a time-boxed, honestly
reported negative result far more than a half-finished component described as complete.

**Remaining 2 days:** Literature Review. The three verified papers (Calamai 2026,
Ong et al. 2025, and the 2026 UK ESG study), plus Stammbach, Webersinke, Hansen, Bingler,
EUDR, and PalmWatch. Use Calamai's survey as the structural spine — it maps the field and
identifies the gap you fill.

**End of week:** Prithvi resolved either way + Literature Review drafted.

---

### WEEK 5 — Complete the document

Write Introduction, Discussion, Limitations, and Conclusion. Integrate all chapters. Check
that every number in Results traces back to the master CSV, and that every claim in the
text has a citation.

The Limitations section is not a weakness — write it deliberately and fully. Attribution
uncertainty, PDF extraction noise, keyword baseline, non-probabilistic sample, single
commodity. Naming these yourself is what separates a strong thesis from an average one.

**End of week:** complete draft, all chapters, ~17,000 words.

---

### WEEK 6 — Revise and submit

Full read-through. Fix references. Proofread. Send to your supervisor early enough in the
week that their feedback can still be incorporated.

**Website: build only if this week has genuine slack.** It is a presentation layer for
results that already exist in the document. If it does not get built, nothing is lost.

---

## 4. Priority order, if time runs short

Cut from the bottom up:

1. Reproducible results and master CSV — **cannot be cut**
2. Scoring layer — **cannot be cut** (this is the contribution)
3. Validation — **cannot be cut** (this is the defence)
4. The written document — **cannot be cut** (this is the deliverable)
5. Literature Review depth — reduce to the core papers if needed
6. Prithvi — reduce to an honest attempt write-up
7. Website — drop entirely without consequence

---

## 5. Standing rules

- Write during the week you produce the result, not afterwards
- Every number in the thesis must be reproducible from a script you can re-run
- Document limitations as you encounter them, not at the end
- Do not add new components. The scope is fixed.
- If a task is taking longer than its allocation, stop and write up what you have

---

## 6. First action

Write the multi-mill loop and reproduce one company's forest-loss total from the raw
Universal Mill List. Verify it matches the figure on record.

Nothing else starts until that number reproduces.
