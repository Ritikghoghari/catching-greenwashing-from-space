# Chapter 4: Results

## 4.1 NLP Claim Extraction Results

The claim extraction pipeline produced 55 deforestation-related claims across the 11 companies (Section 3.2.3). Every claim was drawn from a company sustainability report and passed through the ClimateBERT classifier (Webersinke et al., 2022) using the environmental claim definition of Stammbach et al. (2022).

Claim volume varies sharply by company. Some companies state a single zero-deforestation commitment once, in a policy section. Others repeat similar language across a CEO letter, a policy page, and a progress table, and each repetition is counted as a separate claim instance. This means claim count on its own says little about a company's actual commitment level. It mostly reflects how many times a report restates the same position.

Each claim was scored for specificity on a 0 to 1 scale (Section 3.2.4). A claim that names a percentage, a deadline, a mill count, or a verification method scores toward 1. A claim that offers only general commitment language, with no measurable target, scores toward 0. Across the reviewed claim set, specificity scores ranged from about 0.50 to 0.96, with a mean close to 0.72. Roughly half of the claims were tagged as hard commitments (specific numeric or dated targets) and half as soft commitments (general policy language). This near-even split is itself informative. It shows that vague, unfalsifiable language of the kind Bingler et al. (2022) call "cheap talk" is not the exception in this sector. It sits alongside specific, checkable claims in roughly equal measure.

Tagging by claim content shows deforestation-specific language is the most common category, present in well over half of claims. Peat-related claims are also frequent, reflecting the fact that peatland conversion is a distinct and heavily scrutinised issue in the Indonesian and Malaysian palm sectors. Traceability claims (to plantation or to mill) and explicit NDPE (No Deforestation, No Peat, No Exploitation) policy references appear less often, and usually only in the larger, more established companies' reports.

Company-level specificity and sentiment means, computed from the full scored claim set per company, feed directly into the mismatch score built in Section 4.3. KLK's claims score highest on average specificity (mean specificity_score of 100 on the normalised 0-100 scale used in scoring, drawn from only 8 claims total, the smallest sample in the dataset). IOI's claims score lowest on specificity (normalised specificity_score of 0), meaning IOI's deforestation-related language is the vaguest of the 11 companies despite it making 66 separate claims. This gap between how much a company says and how specific what it says is turns out to matter more for the mismatch score than raw claim volume, and it is discussed further in Sections 4.3 to 4.5.

Sentiment was scored separately using a FinBERT-style classifier applied to each claim (Section 3.2.5), on the reasoning that a claim's emotional register, confident and self-congratulatory versus neutral and procedural, carries its own signal about how a report is trying to be read. GAR's claims read as the most consistently positive of the 11 companies (sentiment_mean 0.79, normalised sentiment_score_norm of 91.6). Astra Agro's claims read as the least positive (sentiment_score_norm of 0, the floor of the normalised scale). These two sentiment extremes recur in the case studies below.

## 4.2 Satellite Forest Loss Results

Across all 11 companies and their 290 matched mills, the Hansen Global Forest Change dataset (Hansen et al., 2013) records 890,168 hectares of forest loss inside 10 km mill buffers since 2020, the EUDR cutoff year (EU Regulation 2023/1115). This is the headline physical measurement the thesis compares claims against.

Table 4.1 breaks this down by company.

| Company | Post-2020 loss (ha) | Mills matched | Loss as % of forest_2000 |
|---|---|---|---|
| GAR | 171,236 | 50 | 13.87 |
| SD Guthrie | 142,131 | 42 | 14.41 |
| Wilmar | 127,606 | 45 | 11.40 |
| KLK | 92,209 | 30 | 12.18 |
| Astra Agro | 87,198 | 34 | 10.76 |
| IOI | 74,385 | 15 | 19.04 |
| Musim Mas | 53,060 | 18 | 11.45 |
| Genting | 44,362 | 15 | 11.61 |
| First Resources | 40,090 | 16 | 10.29 |
| Bumitama | 30,549 | 14 | 8.66 |
| SIPEF | 27,341 | 11 | 10.42 |

GAR has the highest total loss of any company, 171,236 ha across 50 mills, 13.87% of the forest that stood within its mill buffers in 2000. This is the largest raw footprint in the dataset, but it is also spread across the largest mill network. IOI, by contrast, has the highest loss intensity: 74,385 ha across only 15 mills works out to 4,959 ha per mill, and 19.04% of its forest_2000 baseline, both the highest ratios in the dataset. The distinction between total loss and per-mill intensity matters throughout this chapter, because the two measures rank companies differently, and the mismatch score in Section 4.3 is built to be sensitive to both.

Year by year, total loss across all 11 companies was 150,321 ha in 2021, 148,677 ha in 2022, 217,827 ha in 2023, 198,104 ha in 2024, and 175,239 ha in 2025. The 2023 spike is the largest single-year jump in the dataset and appears consistently across most companies rather than being driven by one outlier. The 2025 figure should be read with some caution: for at least one company (IOI, detailed in Section 4.5) the 2025 loss year in the underlying Hansen data is a partial year, so the true 2025 total for the sector is likely somewhat higher than what is recorded here.

One company-specific pattern is worth naming on its own. Wilmar's Sabahmas concession clears forest in every single year from 2021 to 2025, at a broadly consistent rate of roughly 6,675 ha per year. A single concession showing loss in every year of the study period, rather than one large clearing event followed by stability, is a different pattern from most other mills in the dataset and points to ongoing rather than historical clearing at that site.

A spatial finding applies across the entire dataset rather than to any one company: every one of the 290 matched mills across all 11 companies shows measurable post-2020 forest loss within its 10 km buffer, with the smallest single-mill total still recording 105 ha of loss. No mill in this dataset shows zero loss. This does not mean every mill is causally responsible for the loss recorded near it (Section 3.3.2 discusses the buffer method's attribution limits, following PalmWatch's own documented limitation), but it does mean that forest loss near palm oil mill infrastructure, at some scale, is universal in this sample, not confined to a subset of poorly performing companies.

A related, more targeted measure looks at which mills clear an unusually large amount relative to the rest of the dataset. A mill is flagged as "severe" if its own post-2020 loss exceeds the median per-mill loss across all 290 mills. By this measure, IOI has the highest share of severely-violating mills of any company: 12 of its 15 mills, 80%, exceed the dataset-wide median. SIPEF has the lowest share, 3 of its 11 mills, 27%. This severity share becomes one of the four inputs to the mismatch score in Section 4.3.

## 4.3 Mismatch Scores

The mismatch score combines four normalised components, each rescaled to a 0-100 range and weighted as follows:

- **Forest loss score** (weight 0.35): a company's loss intensity relative to the rest of the dataset, capturing both total loss and per-mill loss.
- **Specificity score** (weight 0.35): how concrete and falsifiable a company's deforestation claims are, from Section 4.1.
- **Sentiment score** (weight 0.15): how positively a company's claims read, from Section 4.1.
- **Spatial match score** (weight 0.15): the share of a company's mills flagged as severely-violating, from Section 4.2.

The two claim-derived components (specificity and sentiment) carry equal combined weight (0.50) to the two satellite-derived components (forest loss and spatial match, also combined 0.50). This is deliberate. A mismatch score built only from loss data would just be a ranking of deforestation intensity, and a score built only from claim data would just be a ranking of how confidently a company writes. The score is designed to sit between the two: a company only scores high when strong, specific, positively-worded claims sit next to a severe measured loss pattern near its mills.

Table 4.2 gives the full ranking.

| Rank | Company | Mismatch score | Forest loss score | Specificity score | Sentiment score | Spatial match score |
|---|---|---|---|---|---|---|
| 1 | KLK | 65.6 | 33.9 | 100.0 | 68.4 | 56.7 |
| 2 | GAR | 63.1 | 50.2 | 67.6 | 91.6 | 54.0 |
| 3 | Musim Mas | 56.2 | 26.9 | 85.1 | 63.6 | 50.0 |
| 4 | IOI | 56.1 | 100.0 | 0.0 | 60.3 | 80.0 |
| 5 | SD Guthrie | 55.2 | 55.4 | 32.9 | 100.0 | 61.9 |
| 6 | Wilmar | 50.3 | 26.4 | 67.2 | 70.0 | 46.7 |
| 7 | First Resources | 41.7 | 15.7 | 75.6 | 27.8 | 37.5 |
| 8 | Genting | 39.5 | 28.4 | 46.6 | 41.4 | 46.7 |
| 9 | Bumitama | 38.5 | 0.0 | 67.1 | 71.4 | 28.6 |
| 10 | SIPEF | 26.1 | 17.0 | 28.3 | 41.0 | 27.3 |
| 11 | Astra Agro | 17.6 | 20.2 | 13.8 | 0.0 | 38.2 |

The two companies that lead the raw satellite measurements from Section 4.2 do not top this ranking. GAR has the highest total forest loss of any company, and IOI has the highest loss intensity of any company, but neither is ranked first. KLK, ranked first, has a mid-pack forest loss score (33.9) but the maximum possible specificity score (100.0) and an above-average sentiment score. Its mismatch score is driven almost entirely by how concrete and confident its claims are, not by how much forest was lost near its mills. This is the pattern the composite formula is designed to catch: a company whose language commits to something specific and checkable, positioned next to a loss record that, while not the worst in the dataset, is far from negligible (92,209 ha, 30 mills). GAR follows close behind, and its case is discussed in Section 4.4.

It is worth being direct about a limitation this ranking carries. KLK's specificity score of 100 is built from only 8 scored claims, the smallest sample of any company in the dataset (flagged as low_n_claims in the underlying data). A sample this small is more easily skewed by one or two unusually specific sentences than a company like IOI's 66-claim sample or GAR's 40-claim sample. The KLK result should be read as directionally suggestive rather than as a settled finding, and it would benefit from additional claim extraction in future work. A parallel validation pass, cross-checking these rankings against external sources such as Global Forest Watch alerts, RSPO complaint records, and PalmWatch's own published findings, is documented separately from this chapter and is not assumed here.

## 4.4 Case Study: GAR

GAR is the clearest case in the dataset for how the composite score is meant to work. It has the largest measured forest loss footprint of any company, 171,236 ha across 50 mills, 13.87% of its forest_2000 baseline (Section 4.2). This gives it the second-highest forest loss score in the ranking, 50.2.

Its claims add to that picture rather than offsetting it. GAR makes 40 scored claims, comfortably above the low-sample threshold that limits confidence in KLK's result, and those claims average a specificity score of 67.6, moderately concrete. GAR's claims also carry the highest sentiment score of any company, 91.6, meaning its language is the most consistently upbeat and confident of the 11 companies. GAR's public reporting references a specific traceability figure (99.8% traceability to plantation, cited in its own 2025 sustainability report) alongside NDPE commitments dated to 2025.

A large, well-documented loss footprint sitting next to language that reads as confident and largely positive, from a company that also states a specific, high traceability percentage, is close to a textbook case of the gap this thesis is built to measure: not that GAR's claims are false in a legal sense, but that the tone and specificity of its public reporting sits at odds with the scale of measured loss recorded near its own mill network. GAR's spatial match score (54.0, meaning 27 of its 50 mills exceed the dataset-wide severity threshold) confirms the loss is not confined to one or two outlier sites. It is distributed across roughly half of GAR's entire mill network.

## 4.5 Case Study: IOI

IOI presents a different, and in some ways more troubling, pattern. Its forest loss score is the maximum in the dataset, 100.0, reflecting both the highest loss intensity of any company (19.04% of forest_2000) and the highest share of severely-violating mills (80%, 12 of 15 mills exceed the dataset median). Year by year, IOI's post-2020 loss climbed from 10,115 ha in 2021 to 13,189 ha in 2022, 18,381 ha in 2023, and 20,359 ha in 2024, before the partial 2025 figure of 12,342 ha. This is not a company whose forest loss is concentrated in one bad year and then improving. Across four full recorded years, the trend runs upward, roughly doubling from 2021 to 2024.

Despite this, IOI ranks fourth overall, not first, with a mismatch score of 56.1. The reason is its specificity score: 0.0, the floor of the normalised scale. IOI makes 66 separate deforestation-related claims, the most of any company in the dataset by claim count, but on average those claims are the vaguest. They tend toward general commitment language rather than dated targets, verified percentages, or mill-level detail. Under the scoring formula, this pulls IOI's mismatch score down substantially: at a specificity score of 100 rather than 0, holding everything else fixed, IOI's mismatch score would be roughly 91, comfortably the highest in the dataset.

This result should be stated honestly rather than smoothed over. IOI's satellite record, on both total intensity and mill coverage, is the most severe in this dataset. Its mismatch score does not reflect that severity fully, because the score is built to weight claim specificity equally alongside forest loss, and IOI's claims happen not to give the score much to work with. A company that says little of substance is, by the logic of this particular formula, penalised less than a company that states something specific and wrong. Whether that is the right design choice is a question worth returning to directly in the discussion chapter, because IOI is the clearest example in the dataset of where a specificity-weighted score and a severity-weighted score would disagree.

## 4.6 Case Study: Astra Agro

Astra Agro ranks lowest of the 11 companies, with a mismatch score of 17.6. This result needs to be read carefully, because it does not mean Astra Agro's forest loss is negligible. The company's mills show 87,198 ha of post-2020 loss, the fifth-largest total in the dataset, spread across 34 mills, 10.76% of forest_2000. That is a substantial, real loss footprint, larger in absolute terms than Musim Mas, Genting, First Resources, Bumitama, or SIPEF.

What separates Astra Agro from those companies is not less forest loss. It is what its public claims contribute to the score. Astra Agro's specificity score is 13.8, the second-lowest in the dataset, ahead only of IOI. Its sentiment score is 0.0, the floor of the normalised scale, meaning its claims read as the least positive or confident of any company reviewed, a more neutral or procedural tone than GAR's or SD Guthrie's language. Its forest loss score, 20.2, and spatial match score, 38.2 (13 of 34 mills flagged severe), are both mid-to-low but not the lowest in the dataset.

The combination of low specificity, flat sentiment, and moderate (not extreme) satellite scores is what produces the low composite score, not an absence of forest loss. Under this scoring design, a company that makes fewer forceful claims, and whose loss pattern is not concentrated in the most extreme tail of the dataset, scores lower on mismatch even when its underlying loss total is far from small. This is a direct consequence of measuring correspondence between claims and outcomes rather than measuring outcomes alone. Astra Agro's low rank should be read as "lower relative mismatch between what it says and what the satellite record shows," not as "clean" or "low deforestation." Its 87,198 ha loss figure sits in the results table for exactly this reason: so the two readings cannot be conflated.

## 4.7 RADD SAR Cross-Validation

As an independent check on the optical Hansen findings, a supplementary validation was run using RADD (Radar for Detecting Deforestation) alerts, a near-real-time forest disturbance monitoring system developed by Wageningen University and Research. RADD uses Sentinel-1 C-band Synthetic Aperture Radar (SAR), which penetrates cloud cover and smoke, detecting changes in radar backscatter caused by vegetation removal. Because RADD and Hansen are built on entirely different sensor technologies, optical Landsat versus SAR Sentinel-1, agreement between them provides independent triangulation evidence rather than a circular confirmation of the same underlying signal.

The validation was run for the top mill of each of five companies selected from the mismatch score ranking: Wilmar (Sabahmas), GAR (NAGA SAKTI), IOI (SYARIMO), KLK (BORNION), and SD Guthrie (GIRAM SOU 29). The same 10 km buffer radius used throughout the thesis was applied. RADD confirmed disturbance signals at four of the five mills tested.

Table 4.3 shows the comparison.

| Company | Mill | Hansen post-2020 (ha) | RADD alert area (ha) |
|---|---|---|---|
| Wilmar | Sabahmas | 6,675 | 0 (no signal) |
| GAR | NAGA SAKTI | 10,197 | 6.72 |
| IOI | SYARIMO | 12,318 | 12.45 |
| KLK | BORNION | 6,768 | 39.55 |
| SD Guthrie | GIRAM SOU 29 | 7,775 | 15.37 |

The RADD alert areas are substantially smaller than the Hansen loss figures. This is methodologically expected and does not represent a contradiction. Hansen accumulates tree cover loss across the full post-2020 period at 30 m pixel resolution. RADD detects active disturbance events using changes in SAR backscatter, a threshold-based signal that is more sensitive to sudden clearing events than to gradual canopy thinning, and which may not flag loss that occurs slowly or in plantation transition contexts common in Borneo and Sumatra. Both systems confirm that forest disturbance is occurring at the same geographic locations. The fact that the two independent sensors agree on the location of the signal, even if not on its magnitude, is the validation this step is designed to provide.

The single exception is Wilmar's Sabahmas mill, which returned zero RADD alerts despite the Hansen record showing 6,675 ha of post-2020 loss at that site across all five study years. The most likely explanation is a SAR coverage gap: RADD's per-tile coverage in Sabah state (Malaysian Borneo) is less dense than in Sumatra, and the clearing pattern at Sabahmas (consistent small-area annual clearing rather than large single-event clearing) may fall below the RADD detection threshold. This null result is itself informative. It shows that SAR-based monitoring has coverage and sensitivity limitations that optical monitoring does not, and it supports the thesis's primary reliance on the Hansen dataset rather than SAR as the main evidence layer.

## 4.8 Prithvi-EO-2.0 Proof of Concept

As a supplementary check on the primary Hansen-based pipeline, a small proof of concept compared a frozen geospatial foundation model, IBM and NASA's Prithvi-EO-2.0-300M, against the Hansen ground truth used throughout this thesis, for one representative mill (IOI's SYARIMO site in Malaysia, selected as IOI's single highest-loss mill). Sentinel-2 imagery from before and after the study period was passed through the frozen model with no deforestation-specific fine-tuning, and the resulting embedding-based change signal was compared tile by tile against the Hansen post-2020 loss mask for the same 10 km buffer. The comparison returned a Spearman correlation of 0.597 (p < 0.0001) between the model's change score and the Hansen loss fraction, with precision of 0.71, recall of 0.71, and an intersection-over-union of 0.55 against the Hansen mask. A general-purpose foundation model, used only for its embeddings and never told what deforestation looks like, produces a change signal that lines up moderately well with the Hansen ground truth this thesis is built on. This is offered as corroborating evidence for the primary pipeline, not as a replacement for it or a claim that Prithvi outperforms Hansen-based measurement. Full methodology and notebook details are documented in Results/prithvi_poc_readme.md.
