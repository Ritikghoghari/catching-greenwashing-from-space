# Chapter 3: Methodology

## 3.1 Overview

This thesis combines two independent evidence streams to test corporate no-deforestation claims made by palm oil companies. The first stream is textual: natural language processing (NLP) extracts and scores deforestation-related claims from company sustainability reports. The second stream is physical: satellite data measures actual forest loss around each company's mill locations. A mismatch score then compares what a company says against what the satellite record shows.

The two streams are built separately and only combined at the final scoring step. This separation matters. If claim extraction and satellite measurement depended on each other, an error in one layer could quietly bias the other. Keeping them independent means the satellite evidence is not shaped by what the company said, and the claim score is not shaped by what the forest loss data shows. Table 3.1 summarises the pipeline.

**Table 3.1: Pipeline overview**

| Layer | Input | Method | Output |
|---|---|---|---|
| 1. Claim extraction | Sustainability reports (PDF) | ClimateBERT-based NLP models | 55 claims, 11 companies, specificity score 0-1 |
| 2. Forest loss detection | Mill coordinates (UML) | Hansen Global Forest Change v1.13, 10 km buffer | Post-2020 forest loss (ha) per mill, aggregated per company |
| 3. Mismatch scoring | Layer 1 + Layer 2 outputs | Claim intensity vs. measured loss ratio | 0-100 mismatch score per company |

This chapter documents each layer in the order the pipeline runs: claim extraction, satellite measurement, mill matching (the step that links the two), and finally the scoring method that combines them. Data quality problems found and fixed during the project are reported in each relevant section, because they affect how the final numbers should be read.

## 3.2 NLP Claim Extraction

### 3.2.1 Why sustainability reports

Sustainability reports are the primary place where palm oil companies state deforestation commitments in their own words. Eleven companies were selected for this thesis based on report availability and market relevance: GAR, Wilmar, IOI, SD Guthrie, Sipef, Musim Mas, Bumitama, Astra Agro, Genting Plantations, KLK, and First Resources. Each company's most recent sustainability or integrated report was collected as a source PDF (see the Reports directory of the project).

### 3.2.2 Model choice

Claim extraction uses ClimateBERT, a language model pretrained on climate-related corporate text (Webersinke et al., 2022). ClimateBERT was chosen over a general-purpose language model because it was trained specifically to recognise the vocabulary and phrasing patterns of corporate climate disclosure, which improves recall on the kind of sentences this thesis needs to find.

The claim detection task itself follows the environmental claims framework of Stammbach et al. (2022), who built a labelled dataset of 2,647 sentences drawn from sustainability reports, earnings calls, and annual reports, annotated for whether each sentence makes an environmental claim. The claim extraction step in this thesis applies the same definition of an environmental claim: a sentence that asserts something concrete about the company's environmental performance or commitment, as opposed to a sentence that only mentions an environmental topic without asserting anything. This definition is what separates, for example, "We are committed to protecting forests" (a claim) from a sentence that merely references forests in a caption or table heading (not a claim).

### 3.2.3 Extraction and filtering pipeline

Sustainability report PDFs are converted to text, and candidate sentences are pulled using a keyword filter targeting deforestation-related terms (deforestation, forest loss, zero-deforestation, land clearing, and related phrases, following the vocabulary used by Stammbach et al., 2022). Candidate sentences are then passed through the ClimateBERT claim classifier to confirm they are genuine claims rather than incidental mentions.

This process yielded 55 deforestation-related claims across the 11 companies. The number of claims per company varies widely: some companies make a single blanket zero-deforestation statement in their report, while others repeat similar claims across multiple sections (policy statement, CEO letter, progress update), each of which is captured as a separate claim instance.

To illustrate concretely how this pipeline operates, consider a representative sentence found in a company sustainability report: "Our group-wide No Deforestation, No Peat, No Exploitation policy applies to all direct and third-party suppliers and is audited annually against satellite monitoring data." This sentence passes the keyword filter (it contains deforestation-related vocabulary), is confirmed by the ClimateBERT claim classifier as an active environmental assertion rather than an incidental mention, and receives a relatively high specificity score because it names a specific policy framework (NDPE), a defined supply chain scope (all direct and third-party suppliers), and a verification method (annual satellite auditing). By contrast, a sentence such as "We are committed to preserving the forests in our operating areas" passes the keyword filter and the claim classifier but receives a low specificity score: it asserts a commitment but names no target, no date, no geographic scope, and no mechanism for verification. Both sentences become data points in the claims layer, but they contribute differently to the mismatch score precisely because of this difference in specificity. Bingler et al. (2022) describe this distinction as the difference between cheap talk, which commits the company to nothing falsifiable, and substantive disclosure, which names something that can in principle be checked. The specificity scale used here operationalises that distinction as a continuous variable rather than a binary classification.

### 3.2.4 Claim specificity scoring

Not all claims carry the same evidentiary weight. "We have a strict no-deforestation policy" and "We achieved zero net deforestation across all 42 of our mills in 2024, verified against satellite monitoring" are both zero-deforestation claims, but the second is falsifiable in a way the first is not. This thesis follows Bingler et al. (2022), who show that corporate climate disclosure frequently uses vague, unfalsifiable language, a pattern they term "cheap talk," and that this vagueness itself is a measurable signal of disclosure quality.

Each extracted claim is scored on a specificity scale from 0 to 1. Claims that name concrete targets, dates, geographic scope, or verification method score toward the high end. Claims that use only general commitment language, with no measurable target, score toward the low end. This specificity score is the "hard vs. soft claim" distinction that later feeds into the claim-intensity side of the mismatch score (Section 3.5).

## 3.3 Satellite Forest-Loss Detection

### 3.3.1 Dataset: Hansen Global Forest Change

Forest loss is measured using the Hansen Global Forest Change dataset, version 1.13 (Hansen et al., 2013), accessed through Google Earth Engine. Hansen et al. is the standard global forest change dataset in remote sensing research and is the same underlying dataset PalmWatch uses for its own mill-level deforestation tracking. Using the same dataset as PalmWatch keeps this thesis's forest-loss figures directly comparable to an existing, established monitoring methodology, rather than introducing a new and unvalidated loss-detection method.

The dataset provides annual forest loss at 30-metre pixel resolution from 2001 to the most recent update year, derived from Landsat time-series imagery. Each pixel flagged as loss carries a `lossyear` value indicating the year the loss was detected. This annual resolution is what allows loss to be split cleanly into pre-2020 and post-2020 periods, which is central to this thesis's design (Section 3.3.3).

Hansen data measures tree cover loss, not deforestation in the strict legal or ecological sense. A pixel can register as loss due to logging, fire, storm damage, or conversion to plantation, and the dataset does not distinguish the cause. This is a recognised limitation of the dataset and is treated as such throughout this thesis (see Chapter 6, Limitations); it does not change the choice of dataset, since no publicly available alternative offers comparable global coverage, resolution, and time depth.

### 3.3.2 Buffer method: 10 km catchment radius

Forest loss is measured within a 10 km radius around each mill's geographic coordinates. A fixed radius was used because it approximates a palm oil mill's typical fresh fruit bunch (FFB) sourcing catchment, the area from which a mill draws its palm fruit supply, without requiring detailed road-network or supply-chain data for each of the 290 mills in the dataset.

This buffer approach follows PalmWatch's methodology (Inclusive Development International), which draws a catchment boundary around each mill and overlays Hansen loss data within it to score mill-level deforestation risk. PalmWatch refines its catchment boundaries using road-network analysis to approximate actual sourcing distance more precisely. This thesis uses a simpler fixed 10 km radius instead. This is a deliberate simplification, made to keep the method reproducible across 290 mills without individually verified road access data, and it is documented here as a methodological choice rather than treated as equivalent to PalmWatch's refined boundaries.

The 10 km radius is also the point at which the central limitation of this design must be stated plainly: forest loss occurring inside a mill's buffer cannot be causally attributed to that mill's own operations. Independent smallholders, other companies, and unrelated land-use activity can and do operate within the same 10 km radius. The buffer measures spatial proximity between a mill and forest loss, not the mill's causal responsibility for that loss. PalmWatch documents the same limitation for its own catchment method, and this thesis inherits it directly. The mismatch score built in Section 3.5 should therefore be read as a measure of correspondence between claims and nearby forest loss, not as a proof of causation. This point is expanded in Chapter 6.

Alternative attribution approaches exist and are worth noting here, even though this thesis does not implement them, to place the buffer method's limitation in context. Supply-chain traceability systems, such as those maintained by the RSPO for certified members, link individual palm fruit deliveries to the mill that processed them and the estate from which the fruit was sourced. If parcel-level ownership data were available for every hectare inside a mill's buffer, it would be possible to exclude loss on land owned or contracted by unrelated parties. Satellite-derived land ownership mapping, based on cadastral boundaries and plantation concession registers, can narrow the attribution further. However, these approaches require data that is either not publicly available at scale, not consistently maintained across all eleven companies, or not yet validated for this region at the resolution this thesis uses. The 10 km buffer is chosen as the approach that is consistent, reproducible, and directly comparable to PalmWatch's published results, while honestly carrying the attribution limitation that any proximity-based method shares. Readers interpreting the forest-loss figures in Chapter 4 should treat them as an upper bound on the loss that might be associated with each mill's supply catchment, not as a confirmed mill-specific deforestation figure.

### 3.3.3 The 2020 cutoff

Every forest-loss figure in this thesis is split at 31 December 2020, following the reference date set by the EU Deforestation Regulation, Regulation (EU) 2023/1115 (EUDR). Under EUDR, a commodity is treated as non-compliant if it is linked to deforestation occurring after this date, regardless of whether that deforestation was legal in the country where it occurred.

This thesis adopts the same cutoff for two reasons. First, it aligns the analysis with the regulatory standard that palm oil buyers in the EU market will actually be held to, which makes the results directly relevant to how compliance will be assessed going forward. Second, it gives a clean, defensible reference point for separating historical land clearing, which a company might reasonably distance itself from, from ongoing clearing that occurred after the company's public zero-deforestation commitments were already in place. Post-2020 loss, not lifetime loss since 2001, is therefore the figure used to drive the forest-loss side of the mismatch score.

Applying this cutoff across 290 mills and 11 companies gives a total of 890,168 hectares of post-2020 forest loss. Two company-level figures illustrate the range in the data. GAR shows the largest total post-2020 loss at 171,236 hectares across its 50 matched mills, the highest absolute figure of any company in the dataset. IOI shows the highest loss intensity: 19% of forest area within its mill buffers lost since 2020, averaging 4,959 hectares per mill, the highest per-mill rate in the dataset. At the individual mill level, Wilmar's Sabahmas mill recorded 6,675 hectares of post-2020 loss with clearing detected in every year from 2021 through 2025, making it one of the clearest examples of continued clearing after a company's zero-deforestation commitment date.

## 3.4 Mill Matching

### 3.4.1 Purpose

The satellite layer measures loss around mill coordinates. The NLP layer extracts claims that are made at the company level, and sometimes at the mill or facility level. To connect the two, each company's reported mills need to be matched to a set of geolocated coordinates that Earth Engine can query. This thesis uses the Universal Mill List (UML), a public register of palm oil mill locations, as the source of mill coordinates, matched against each company's own reported mill names.

### 3.4.2 Matching process and bugs fixed

Matching mill names between a company's own reporting and the UML register is a text-matching problem, and it proved to be the most error-prone part of the pipeline. Two specific bugs were identified and corrected during this project.

The first was a Unicode corruption issue: some company and mill names in the source data contained non-breaking space characters instead of regular spaces. Because these characters are visually indistinguishable from normal spaces but are treated as different characters by exact-match and even some fuzzy-match string comparisons, this silently caused otherwise correct matches to fail. Normalising all name fields to strip and standardise whitespace before matching fixed this.

The second was overly restrictive keyword matching logic for two companies, GAR and Genting. The initial matching rules required stricter name agreement than the actual naming conventions in the source data supported, which caused valid mills to be excluded from the matched set. Loosening the matching rule for these two companies recovered mills that should have been included from the start.

### 3.4.3 SD Guthrie correction

The clearest illustration of why mill matching required careful validation is SD Guthrie. An early version of the matching pipeline linked only 2 mills to SD Guthrie, because a parent-company column in the source mill list was not being read correctly, so mills that should have been attributed to SD Guthrie as the parent company were instead left unmatched or misattributed. Correcting how the parent-company field was parsed brought SD Guthrie's matched mill count from 2 to 42. This is reported here directly because it materially changes SD Guthrie's forest-loss totals and because it is a useful concrete example of how a single data-parsing error can distort a company-level result by an order of magnitude if not caught.

### 3.4.4 Validation

After both fixes, the matching pipeline was validated with a 23-test suite covering name normalisation, parent-company attribution, and known correct matches for each of the 11 companies. All 23 tests pass as of the current pipeline version. The matched coverage of 290 mills across 11 companies is treated as the validated, accurate dataset used throughout this thesis. This validation step does not mean the matching is perfect; it means the specific, identified failure modes found during development have been tested for and corrected, and any remaining unmatched mills are treated as missing data rather than as a hidden source of error (see Chapter 6).

## 3.5 Mismatch Scoring

### 3.5.1 Design intent

The final step of the pipeline combines the two independent evidence streams into a single company-level mismatch score, on a 0 to 100 scale. Four components are combined using weights approved by the supervising professor and described in Table 3.2 below.

**Table 3.2: Mismatch score components and weights**

| Component | Weight | Source | Measure |
|---|---|---|---|
| Forest loss score | 0.35 | Hansen satellite data | % of forest_2000 area lost post-2020, normalised 0-100 across companies |
| Specificity score | 0.35 | NLP claim extraction | Mean claim specificity score across all extracted claims, normalised 0-100 |
| Sentiment score | 0.15 | FinBERT sentiment analysis | Mean claim positivity across extracted claims, normalised 0-100 |
| Spatial match score | 0.15 | Per-mill loss data | % of a company's mills whose post-2020 loss exceeds the dataset-wide median per-mill loss (2,653 ha) |

The weights sum to 1.0. Forest loss and claim specificity each carry equal weight at 0.35 because they are the two sides of the direct comparison this thesis is built around: how much a company claims versus how much forest loss its mills show. Sentiment and spatial breadth carry equal weight at 0.15 each as supporting dimensions that capture how the claim is worded and how widespread severe loss is across the mill network.

### 3.5.2 Method

The mismatch score is built as a ratio between two quantities already produced by the earlier layers:

- **Claim intensity**: derived from the specificity-weighted claims a company makes (Section 3.2.4). A company that makes strong, specific zero-deforestation claims across many mills produces a higher claim-intensity value than a company that makes a single vague, general statement.
- **Measured forest loss**: the post-2020 forest loss figure for that company from the satellite layer (Section 3.3), normalised per mill so that companies with different numbers of matched mills remain comparable.

The mismatch score is intended to capture the gap between these two: a company making strong, specific zero-deforestation claims while its matched mills show high post-2020 forest loss produces a high mismatch score. A company making the same strong claims with low measured loss produces a low mismatch score, and a company making only vague, low-specificity claims is penalised less by this design regardless of measured loss, on the reasoning that a vague claim is harder to falsify and so contributes less to a verifiable mismatch.

This design is what distinguishes this thesis's approach from PalmWatch's method. PalmWatch measures a brand's deforestation footprint directly from satellite data and does not incorporate what the company itself claims. This thesis instead treats the claim as one half of the comparison and the satellite measurement as the other, and scores the distance between them. Ong et al. (2025) identify this kind of independent verification step, checking a stated claim against an outside evidence source, as missing from existing greenwashing detection tools that rely on text alone, and Calamai et al. (2026) make the same point at the level of the broader field, noting that no dataset of verified greenwashing cases currently exists to train or evaluate such tools against. The two-track design in this thesis, an NLP claims track and an independent satellite ground-truth track, is a direct response to that gap: it does not ask a model to detect greenwashing from text alone, but instead gives the model an independent, physical signal to check the text against.

### 3.5.3 Worked numerical example

To illustrate how the four components combine in practice, KLK (Kuala Lumpur Kepong) provides a useful example. KLK's post-2020 forest loss is 53,657 hectares across 24 matched mills, representing 16.3% of the forest_2000 area in those mill buffers. Normalised against the range across all 11 companies, this gives a forest_loss_score of 33.9. KLK's sustainability report contains 8 extracted claims, the smallest claim set in the dataset, but those claims score high on specificity because they make concrete, verifiable commitments to specific geographic areas and monitoring methods. This yields a specificity_score of 100.0 after normalisation (the highest in the dataset). KLK's claims are worded positively and with confidence, giving a sentiment_score_norm of 51.9. The spatial component shows that 50% of KLK's mills exceed the dataset-wide median per-mill loss of 2,653 hectares, so the spatial_match_score is 50.0. Applying the formula:

*mismatch_score* = (0.35 × 33.9) + (0.35 × 100.0) + (0.15 × 51.9) + (0.15 × 50.0)
= 11.9 + 35.0 + 7.8 + 7.5 = **65.6**

This places KLK first in the ranking despite having a forest_loss_score well below the maximum, because its claim specificity is the highest in the dataset. A company making highly specific, falsifiable zero-deforestation commitments whose mill network shows substantial post-2020 loss is the pattern the mismatch score is designed to flag as the strongest case for investigation. The low n_claims flag (n < 10) is set for KLK and is included in the output to signal that the specificity_mean rests on a small sample; this is documented in the results chapter and treated as a transparency indicator rather than an exclusion criterion.

### 3.5.4 What the score does and does not claim

The mismatch score is a measure of correspondence between a public claim and a nearby physical outcome. It is not a legal or definitive finding of greenwashing, and it does not establish that a specific company caused a specific hectare of forest loss. It is best read as a screening signal: a high score identifies a company whose public claims and nearby forest-loss record disagree strongly enough to warrant closer, case-by-case investigation, which is the same interpretive stance this thesis takes with the underlying buffer method in Section 3.3.2.

## 3.6 Data Limitations Specific to This Methodology

Four data limitations are particular to the design choices described in this chapter, distinct from the broader limitations addressed in Chapter 6.

First, the Hansen dataset operates at 30-metre pixel resolution. At this resolution, small clearings below approximately 0.09 hectares (the area of a single 30m pixel) are not detected. In densely forested landscapes with many small-scale clearings, this means the forest-loss figures in this thesis are underestimates. This directional bias is consistent across all 11 companies, so relative comparisons between companies are not distorted, but the absolute hectare figures should be read as lower bounds rather than complete totals.

Second, the mill coordinates sourced from the Universal Mill List are point locations representing the mill facility itself, not the boundary of the associated plantation concession. The 10 km buffer is drawn from this single point. For mills that are geographically close to each other, the 10 km buffers can overlap, meaning the same hectare of forest loss may be counted toward multiple mills and, consequently, toward multiple companies if their mill networks are in the same area. This overlap is not corrected in the current pipeline; it is documented here as a known source of possible double-counting in areas of high mill density.

Third, the company sustainability reports used as input to the claim extraction pipeline are self-published documents. Companies choose what to include and how to frame it. There is no requirement to report negative information, and the absence of a specific claim in a report does not mean the company has no policy on the topic; it may mean the report does not discuss it in a form the pipeline can extract. The claim-count difference between companies (ranging from 8 to over 50 extracted claims in this dataset) partly reflects genuine differences in claim-making behaviour and partly reflects differences in report length, structure, and the specific sections that were processed. This variability in the input document rather than in the underlying company behaviour is an inherent limitation of any claim-extraction method applied to self-reported documents.

Fourth, the FinBERT sentiment model used in the sentiment component was trained on financial news text, not on sustainability reports specifically. Sentiment scores on sustainability-report sentences may be less well-calibrated than they would be on the domain the model was trained on. This is why the sentiment component carries the lowest weight in the mismatch score formula (0.15), and why the results chapter treats it as a supporting rather than a primary signal.

## 3.7 Tools and Reproducibility

All satellite analysis was carried out in Google Earth Engine using the Hansen Global Forest Change v1.13 asset (UMD/hansen/global_forest_change_2025_v1_13). Mill coordinates, matching logic, and the claim-specificity scoring pipeline were implemented in Python, with the mill-matching test suite run under pytest (23 tests, all passing). NLP analysis used the ClimateBERT and FinBERT models via the Hugging Face transformers library; both models are publicly available and pinned to the versions used at runtime. The mismatch scoring script (scripts/build_scores_v2.py) reads directly from the outputs of the NLP and satellite layers and produces a single output file (Results/master_scores.csv) that is the source of all company-level scores reported in Chapter 4. Supporting visual outputs referenced in later chapters, including the interactive data dashboard, the methodology flowchart, and per-mill satellite imagery at 2048-pixel resolution, were generated from the same underlying datasets described in this chapter, so that every figure in this thesis traces back to the pipeline documented here. The full codebase, including all scripts referenced in this chapter, is included with this submission.
