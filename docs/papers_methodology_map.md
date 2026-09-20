# Papers → Methodology Map

Every pipeline decision traced to a source. Use this as the citation spine for the Methodology chapter — each row is a paragraph, not a footnote.

## Layer 1 — Claim extraction (NLP)

**Stammbach, D., Webersinke, N., Bingler, J. A., Kraus, M., & Leippold, M. (2023).**
*A Dataset for Detecting Real-World Environmental Claims.* arXiv:2209.00507.
https://arxiv.org/abs/2209.00507 (also: `climatebert/environmental-claims` on Hugging Face)

- Source of the environmental-claims dataset (2,647 expert-annotated sentences from sustainability reports, earnings calls, annual reports) that the claim-extraction keyword filter and tagging approach is modeled on.
- Justifies: pulling candidate sentences from PDF sustainability reports, the definition of "environmental claim" used to filter Layer 1 output.

**Bingler, J. A., Kraus, M., & Leippold, M. (2022).**
*Cheap Talk and Cherry-Picking: What ClimateBert has to say on Corporate Climate Risk Disclosures.* Finance Research Letters. https://www.sciencedirect.com/science/article/pii/S1544612322000897

- Establishes "cheap talk" — vague, unfalsifiable climate language — as a measurable NLP category, and that firms cherry-pick which risks/claims to disclose.
- Justifies: the hard/soft claim-strength split (specific, measurable claims vs. vague aspirational ones) that feeds the 0.4 claim-specificity weight in the mismatch score.

## Layer 2 — Forest-loss detection (satellite)

**Hansen, M. C., Potapov, P. V., Moore, R., Hancher, M., Turubanova, S. A., Tyukavina, A., Thau, D., Stehman, S. V., Goetz, S. J., Loveland, T. R., Kommareddy, A., Egorov, A., Chini, L., Justice, C. O., & Townshend, J. R. (2013).**
*High-Resolution Global Maps of 21st-Century Forest Cover Change.* Science, 342(6160), 850–853. DOI: 10.1126/science.1244693

- The source dataset (UMD Global Forest Change, `lossyear` band) used directly in Google Earth Engine for every mill-level loss figure in this thesis.
- Justifies: 30 m pixel resolution, annual `lossyear` classification (2001–2025), and the choice of Hansen over commercial alternatives — it is the standard ground-truth dataset the field benchmarks against, including PalmWatch itself.

## Layer 2 — Buffer / catchment method

**PalmWatch (Inclusive Development International).** *Tracking the Impact of Big Brands' Palm Oil Use.*
https://palmwatch.inclusivedevelopment.net/about

- Draws a catchment boundary around each mill approximating its fruit-sourcing radius (refined with road-network analysis), then overlays 20 years of Hansen deforestation data within that boundary to score each mill.
- Justifies: the 10 km buffer radius used here as a simplified version of PalmWatch's catchment method (this thesis uses a fixed radius rather than road-network refinement — documented as a limitation), and the general design of "buffer mill location → overlay Hansen loss."
- **This is also where the novelty claim is argued**: PalmWatch measures a brand's deforestation footprint. This thesis instead extracts each company's *own claims* via NLP and scores the *gap* between claim and measured footprint — PalmWatch has no claims layer.

## Cutoff date — EUDR

**Regulation (EU) 2023/1115** (EU Deforestation Regulation, EUDR).

- Sets 31 December 2020 as the reference date: commodities linked to deforestation after that date are non-compliant, regardless of legality in the country of production.
- Justifies: the before/after-2020 split applied to every forest-loss figure, and why post-2020 loss (not lifetime loss) drives the forest-loss score — it is the same cutoff regulators use.

## Methodology justification / survey anchor

**Calamai, T., Balalau, O., Le Guenedal, T., & Suchanek, F. M. (2026).**
*Corporate Greenwashing Detection in Text — A Survey* (also circulated as *Detecting Greenwashing: A Natural Language Processing Literature Survey*). arXiv:2502.07541. https://arxiv.org/abs/2502.07541

- Surveys the NLP tasks researchers use to approximate greenwashing detection (topic detection → deceptive-pattern identification) and states plainly that **no dataset of verified greenwashing cases exists** — automated detection needs principled methodology combining reliable annotation with interpretable model design, not just a bigger classifier.
- Justifies: the overall two-track design of this thesis (claims vs. independent satellite ground-truth) as a direct answer to Calamai's stated gap — this project sidesteps the "no verified-case dataset" problem by using satellite data as the verification signal instead of asking a model to detect greenwashing from text alone. Use Calamai's survey as the literature-review spine; it maps the field and identifies the gap this thesis fills.

---

## One-line summary table

| Pipeline decision | Paper |
|---|---|
| Claim extraction / dataset design | Stammbach et al. 2023 |
| Hard vs. soft claim strength | Bingler et al. 2022 (cheap talk) |
| Forest-loss source, 30 m / annual bands | Hansen et al. 2013 |
| 10 km mill buffer | PalmWatch catchment method |
| Post-2020 cutoff | EUDR, Regulation (EU) 2023/1115 |
| Overall two-track methodology, gap filled | Calamai et al. 2026 |
