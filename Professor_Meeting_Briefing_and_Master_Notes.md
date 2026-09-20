# Catching Greenwashing from Space: Master Thesis Briefing & Meeting Guide

**Student:** Ritik Ghoghari  
**Degree:** M.Sc. Data Science, AI & Digital Business  
**Institution:** GISMA University of Applied Sciences, Berlin  
**Supervisor:** Professor Mohamad Hoseini  
**Meeting Time:** Tomorrow, 15:30 CET (Germany Time)  
**Final Submission Deadline:** 26 September 2026  

---

## 1. Executive Summary & Project Identity

### What is the core problem?
Palm oil companies make public zero-deforestation commitments in their annual sustainability reports. However, existing research and commercial ESG audit tools face a major gap:
1. **Text-only tools** (such as standard NLP sentiment or keyword analysis) can check whether corporate language is vague or confident, but they cannot verify if the company is actually clearing forests on the ground.
2. **Satellite-only tools** (such as PalmWatch or Global Forest Watch) measure forest clearing via satellite, but they do not compare measured clearing against what corporate executives publicly promised.

This thesis establishes a reproducible method that connects both sides: an independent natural language processing (NLP) claims extraction pipeline and an independent satellite remote sensing pipeline, linked together through an objective **Mismatch Score (0 to 100)**.

---

## 2. Basic Foundational Concepts (First Principles)

To explain this project clearly to Professor Hoseini, you need to be comfortable with these fundamental concepts:

### A. What is EUDR and why 31 December 2020?
- **EUDR** stands for the **European Union Deforestation Regulation (Regulation EU 2023/1115)**.
- Under EU law, palm oil (and other forest-risk commodities) imported into the European Union must be verified as **deforestation-free**.
- The EUDR sets a strict regulatory reference cutoff: **31 December 2020**.
- Any forest clearing after 31 December 2020 makes the harvested crop non-compliant for the EU market, regardless of whether the clearing was considered legal under national Indonesian or Malaysian law.
- In this thesis, all satellite loss is filtered to **post-2020 (years 2021 to 2025)**. This isolates ongoing clearing from historical legacy clearing.

### B. What is a Palm Oil Mill and why a 10 km Buffer?
- Fresh fruit bunches (FFB) harvested from oil palm trees must be processed within 24 to 48 hours before the free fatty acids spike and ruin the crude palm oil (CPO).
- Because palm fruit degrades quickly, plantations must transport fruit directly to a nearby processing mill.
- The area around a mill from which it draws palm fruit is called its **sourcing catchment**.
- Following established industry methodology (such as PalmWatch / Inclusive Development International), this study draws a **10 km radial buffer** around each mill coordinate. This circle defines the mill's local sourcing landscape.

### C. Tree Cover Loss vs. Deforestation
- The primary satellite dataset used is the **Hansen Global Forest Change (GFC) v1.13** (derived from Landsat time series at 30-meter resolution).
- Hansen detects biophysical **tree cover loss** (removal of canopy cover exceeding 30% density).
- It does not automatically distinguish whether trees were cleared for palm plantations, lost to wildfires, or harvested in commercial timber plantations.
- Therefore, in scientific discussions, we state clearly that the buffer method measures **spatial correspondence and proximity**, rather than definitive legal causation. To address this distinction, the thesis implements independent land cover cross-validation (Descals oil palm mapping).

---

## 3. The Architecture: Two Independent Pipelines

The foundational design principle of this thesis is **pipeline separation**. The textual claims pipeline and the physical satellite pipeline are developed completely independently and meet only at the final mathematical scoring equation.

```
+------------------------------------+        +------------------------------------+
|        NLP CLAIMS PIPELINE         |        |     SATELLITE & GEE PIPELINE       |
+------------------------------------+        +------------------------------------+
| 1. Company Sustainability Reports  |        | 1. Universal Mill List (UML)       |
|    (PDF to text, 11 companies)     |        |    (290 matched mill coordinates)  |
| 2. Candidate Sentence Extraction   |        | 2. Google Earth Engine Processing  |
|    (Keywords + ClimateBERT filter) |        |    (Hansen GFC v1.13, Landsat 30m) |
| 3. Specificity Scoring (0 to 1)    |        | 3. EUDR Post-2020 Loss Filter      |
|    (Concrete targets vs cheap talk)|        |    (lossyear >= 2021 inside 10 km) |
| 4. Sentiment Analysis (FinBERT)    |        | 4. Spatial Matching & Severity     |
|    (Corporate tone and confidence) |        |    (Mills exceeding dataset median)|
+------------------------------------+        +------------------------------------+
                  \                                      /
                   \                                    /
                    v                                  v
         +-------------------------------------------------------+
         |                 CANONICAL MISMATCH SCORE              |
         |  Score = 0.35*Loss + 0.35*Spec + 0.15*Sent + 0.15*Geo  |
         +-------------------------------------------------------+
                                    |
                                    v
         +-------------------------------------------------------+
         |     Cross-Validations & Ground-Truth Verification     |
         |  - Prithvi Foundation Model (Spearman rho = 0.172)    |
         |  - RADD Radar SAR Disturbance (4 of 5 confirmed)      |
         |  - Descals Land Cover (56.0% converted to oil palm)   |
         |  - Buffer Sensitivity (5 km, 10 km, 15 km, 20 km, 30) |
         +-------------------------------------------------------+
```

### Pipeline Track 1: Natural Language Processing (NLP)
1. **Corpus Extraction:** 11 major corporate sustainability reports converted to machine-readable text.
2. **Claim Detection:** Evaluated candidate sentences using `climatebert/environmental-claims`. Achieved **97.3% accuracy** and an **F1 score of 0.981** on our 150-sentence domain gold benchmark, filtering out public relations boilerplate.
3. **Specificity Scoring:** Scored claims using `climatebert/distilroberta-base-climate-specificity`. Claims with measurable deadlines, mill counts, or certified percentages receive high specificity, separating verifiable commitments from unfalsifiable "cheap talk".
4. **Sentiment Scoring:** Scored using `ProsusAI/finbert`. Measures corporate confidence and optimism.
5. **ESG Topic Categorization:** Categorized claims using `nbroad/ESG-BERT` (80.2% accuracy on gold benchmark) across GHG emissions, ecological impacts, and supply chain management.

### Pipeline Track 2: Satellite Remote Sensing (Google Earth Engine)
1. **Mill Coordinates:** Sourced from the Universal Mill List (UML), deduplicated and validated against corporate parent entities.
2. **Spatial Buffering:** Generated 10 km circular polygons around all 290 mills across Indonesia, Malaysia, and Papua New Guinea.
3. **Loss Computation:** Analyzed Hansen GFC v1.13 (`treecover2000 > 30%`, `lossyear >= 21`) at 30-meter resolution.
4. **Aggregation:** Aggregated pixel-level clearing to per-mill totals and company-level loss percentages relative to the baseline forest standing in year 2000.

---

## 4. Canonical Mismatch Scoring Formula

The Mismatch Score combines all four normalized components into an index from 0 to 100:

$$\text{Mismatch Score} = 0.35 \times \text{Forest Loss} + 0.35 \times \text{Specificity} + 0.15 \times \text{Sentiment} + 0.15 \times \text{Spatial Match}$$

### Component Breakdown and Rationale:
1. **Forest Loss Score (Weight: 0.35):** Normalized percentage of year-2000 baseline forest lost post-2020. Represents the physical clearing footprint.
2. **Claim Specificity Score (Weight: 0.35):** Normalized mean specificity of company commitments. High score indicates precise, verifiable targets.
3. **Claim Sentiment Score (Weight: 0.15):** Normalized positivity of claims. High score indicates confident corporate self-reporting.
4. **Spatial Match Score (Weight: 0.15):** Percentage of a company's mills that exceed the dataset-wide median loss per mill (2,653 ha). Measures how widespread clearing is across the mill network.

### Why do the weights balance this way?
- The satellite evidence (Loss + Spatial Match = 0.35 + 0.15 = **0.50**) balances the textual evidence (Specificity + Sentiment = 0.35 + 0.15 = **0.50**) equally.
- If we scored on forest loss alone, it would simply be a satellite ranking.
- If we scored on claims alone, it would simply be a tone analysis.
- The highest mismatch score occurs when a company issues specific, confident commitments while its mill catchments experience severe forest clearing.

---

## 5. Headline Numbers and Verified Findings

```
Dataset Totals: 11 Companies | 290 Mills | 890,168 ha Post-2020 Forest Loss
```

### Full Company Ranking Table:

| Rank | Company | Mismatch Score | Forest Loss Score | Claim Spec. Score | Claim Sent. Score | Spatial Match Score | Post-2020 Loss (ha) | Mills Matched | Loss as % of Forest 2000 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **KLK** | **65.6** | 33.9 | 100.0 | 68.4 | 56.7 | 92,209 | 30 | 12.18% |
| **2** | **GAR** | **63.1** | 50.2 | 67.6 | 91.6 | 54.0 | 171,236 | 50 | 13.87% |
| **3** | **Musim Mas** | **56.2** | 26.9 | 85.1 | 63.6 | 50.0 | 53,060 | 18 | 11.45% |
| **4** | **IOI** | **56.1** | 100.0 | 0.0 | 60.3 | 80.0 | 74,385 | 15 | 19.04% |
| **5** | **SD Guthrie** | **55.2** | 55.4 | 32.9 | 100.0 | 61.9 | 142,131 | 42 | 14.41% |
| **6** | **Wilmar** | **50.3** | 26.4 | 67.2 | 70.0 | 46.7 | 127,606 | 45 | 11.40% |
| **7** | **First Resources** | **41.7** | 15.7 | 75.6 | 27.8 | 37.5 | 40,090 | 16 | 10.29% |
| **8** | **Genting** | **39.5** | 28.4 | 46.6 | 41.4 | 46.7 | 44,362 | 15 | 11.61% |
| **9** | **Bumitama** | **38.5** | 0.0 | 67.1 | 71.4 | 28.6 | 30,549 | 14 | 8.66% |
| **10** | **SIPEF** | **26.1** | 17.0 | 28.3 | 41.0 | 27.3 | 27,341 | 11 | 10.42% |
| **11** | **Astra Agro** | **17.6** | 20.2 | 13.8 | 0.0 | 38.2 | 87,198 | 34 | 10.76% |

---

## 6. Key Company Case Studies (Crucial for Professor Discussion)

### Case 1: KLK (Rank 1 - Mismatch Score 65.6)
- **Why Rank 1?** KLK does not have the highest absolute forest loss (92,209 ha), but its claims scored **100.0 on specificity** (the highest possible).
- **The Explanation:** KLK published exact, falsifiable commitments with explicit targets and dates. When set against 92,209 ha of measured post-2020 loss, the mathematical gap between public promise and satellite observation is the widest.
- **Honest Academic Qualification:** KLK's claim set is small ($n=8$), which can make the specificity average more sensitive. This is explicitly noted in Chapter 4.

### Case 2: Golden Agri-Resources / GAR (Rank 2 - Mismatch Score 63.1)
- **The Textbook Case:** GAR exhibits the largest absolute forest loss in the entire study: **171,236 ha** across 50 mills.
- **The Contrast:** In its 2025 sustainability report, GAR claims **99.8% traceability to plantation** with confident, optimistic language (Sentiment score 91.6).
- **Physical Evidence:** The NAGA SAKTI mill in Riau alone recorded **10,197 ha** of post-2020 clearing. Half of GAR's mills exceed the dataset severity threshold.

### Case 3: IOI Corporation (Rank 4 - Mismatch Score 56.1)
- **The Intensity Leader:** IOI has the highest loss intensity in the entire dataset: **19.04%** of baseline forest lost post-2020, averaging **4,959 ha per mill**.
- **Widespread Violation:** 80% of its mills (12 of 15) exceed the dataset median. Single highest loss mill in the study: **SYARIMO** in Sabah, Malaysia with **12,318 ha** cleared.
- **Why only Rank 4?** IOI made 66 claims, but they were vague and unmeasurable (Specificity score: 0.0). Because the model checks for contradictions of concrete commitments, IOI's vague language paradoxically softened its mismatch penalty. This illustrates how cheap talk can mask physical deforestation.

### Case 4: Astra Agro Lestari (Rank 11 - Mismatch Score 17.6)
- **The Counter-Intuitive Finding:** Astra Agro has the 5th-largest absolute loss (**87,198 ha** across 34 mills), yet ranks last on mismatch.
- **Why?** Astra Agro published very few public claims, worded in low-specificity, flat procedural language (Sentiment: 0.0, Specificity: 13.8). The model finds minimal contradiction between its public statements and satellite data, demonstrating that silence or vagueness yields a low mismatch score even where clearing is substantial.

---

## 7. The Four Robustness & Cross-Validation Analyses

To defend against criticisms of single-dataset dependency, the thesis implements four separate cross-validation methods:

### 1. Geospatial Foundation Model: IBM/NASA Prithvi-EO-2.0-300M
- **Method:** Vision Transformer (ViT) with 300M parameters, pretrained on Landsat-Sentinel multi-spectral sequences.
- **Setup:** Evaluated without fine-tuning or deforestation labels. Computed temporal cosine dissimilarity on 768-dimensional embeddings between pre-cutoff (2019) and post-cutoff (2024) Sentinel-2 median composites across all 290 mills.
- **Result:** Network-wide mean Spearman correlation $\rho = 0.172$ ($p < 0.0001$) and IoU = 0.086 across all 290 mills. Pilot benchmark on IOI Syarimo achieved $\rho = 0.597$, precision 0.71, recall 0.71, IoU 0.55.
- **Significance:** Demonstrates that foundation models independently recover forest loss signals from raw multi-spectral data without supervised training.

### 2. Radar Cross-Validation: Wageningen RADD SAR Alerts
- **Method:** Sentinel-1 C-band Synthetic Aperture Radar (SAR), which penetrates equatorial cloud cover and rain.
- **Result:** Tested on the highest-loss mill for five top companies. Confirmed active radar disturbance signals at 4 of the 5 mills (IOI Syarimo: 12.45 ha; GAR Naga Sakti: 6.72 ha; KLK Bornion: 39.55 ha; SD Guthrie Giram: 15.37 ha).
- **Finding:** Optical and radar systems independently agree on the physical locations of clearing.

### 3. Crop-Specific Land Cover Overlay: Descals et al. (2021)
- **Method:** 10-meter deep learning classification of oil palm plantations.
- **Result:** **56.0%** of post-2020 forest loss across all 290 mill buffers is classified as oil palm (**44.0% industrial closed-canopy palm**). For IOI, **89.8%** of cleared buffer land is converted to oil palm.
- **Significance:** Refutes the claim that forest clearing near mills was driven by unrelated crops or natural mortality.

### 4. Buffer Distance Sensitivity (5 km to 30 km)
- **Method:** Tested radial catchment distances of 5, 10, 15, 20, and 30 km across representative mills.
- **Result:** High rank consistency across adjacent radii (Spearman $\rho = 0.80$ between 10 km and 15 km; $\rho = 0.90$ between 15 km and 20 km). Rank correlation weakens at 30 km ($\rho = 0.49$), demonstrating that 10 km represents an appropriate physical sourcing radius without picking up distant regional noise.

---

## 8. Data Engineering Battles & Obstacles Solved (108 Engineering Hours)

Professor Hoseini will appreciate hearing about real data engineering hurdles you solved:

1. **Universal Mill List Coordinate Corruption (4 hours):**  
   *Problem:* Numeric lat/long columns dropped decimal points, placing mills in the middle of the Indian Ocean.  
   *Solution:* Parsed the uncorrupted composite string column (`"GPS coordinates"`), implemented geographic bounding box validation ($[-10^\circ, 10^\circ]$ latitude, $[90^\circ, 155^\circ]$ longitude).
2. **SD Guthrie Entity Matching Fix (5 hours):**  
   *Problem:* SD Guthrie (formerly Sime Darby) appeared under `Parent Company` rather than `Group Name`, matching only 2 mills.  
   *Solution:* Engineered dual-column matching with coordinate deduplication, increasing matched mills from 2 to 42 and recovering **142,131 ha** of previously missed forest loss.
3. **Unicode Whitespace Normalization (3 hours):**  
   *Problem:* Corporate reports contained non-breaking spaces (`\u00a0`) that caused silent string merge failures in Pandas.  
   *Solution:* Implemented regex whitespace collapsing and forced `regex=False` on corporate name filters.
4. **Google Earth Engine Quotas & Caching (12 hours):**  
   *Problem:* 290 mill buffers covering $>91,000\text{ km}^2$ triggered `Total value of pixels exceeded` exceptions and headless OAuth browser timeouts.  
   *Solution:* Set `maxPixels = 1e10`, pinned 30-meter resolution, isolated Python virtual environment, and built persistent disk caching per company.
5. **FinBERT vs. ClimateBERT Semantic Divergence (6 hours):**  
   *Problem:* FinBERT and ClimateBERT agreed on only 53.1% of sentences ($\kappa = 0.08$).  
   *Solution:* Discovered FinBERT captures promotional optimism (cheap talk), whereas ClimateBERT treats almost everything as opportunity. FinBERT was selected for scoring corporate tone, with the divergence documented in Chapter 4.
6. **Production Theory Exploration and Exclusion (8 hours):**  
   *Problem:* Attempted to normalize loss by Crude Palm Oil (CPO) production volumes.  
   *Solution:* RSPO ACOP and annual reports mixed third-party fruit, refined products, and plantation volumes inconsistently. Production normalization was formally dropped to prevent introducing noisy denominators into company rankings.

---

## 9. Current Status of Project Deliverables

| Component | Status | Artifact / Location |
| :--- | :---: | :--- |
| **NLP Claims Pipeline** | 100% Complete | 403 claims enriched; gold evaluation completed across 150 rows |
| **Satellite Analysis** | 100% Complete | All 290 mills analyzed in GEE (890,168 ha loss computed) |
| **Mismatch Engine** | 100% Complete | `scripts/build_scores_v2.py` (23 of 23 pytest tests passing) |
| **Satellite Clearing Maps** | 100% Complete | 290 high-resolution comparative maps (300 DPI) in `Results/satellite_images/clearing_maps/` |
| **Prithvi Foundation Model** | 100% Complete | Network batch run complete (`Results/prithvi_batch_290.csv`) |
| **LaTeX Thesis Draft** | 100% Complete | All 9 chapters written in `latex/chapters/` (~19,565 words, Overleaf zip ready) |
| **Interactive Website** | 100% Complete | `website/` with 290-mill Leaflet map, satellite image modal, claims inspector, and simulator |

---

## 10. Meeting Speaking Script & Agenda for Tomorrow (15:30 CET)

### Phase 1: Opening & Progress Overview (First 3-5 Minutes)
> "Professor Hoseini, thank you for meeting today. With our submission deadline coming up on 26 September, I am pleased to report that the technical research, modeling, cross-validation, and full thesis write-up are 100% complete.
> 
> My thesis investigates whether palm oil companies' public zero-deforestation commitments match reality on the ground. To solve this, I built two independent evidence pipelines:
> 1. An NLP claims pipeline that extracted and scored 55 specific commitments from 11 major corporate sustainability reports.
> 2. A Google Earth Engine satellite pipeline that analyzed 290 processing mills and measured forest loss after the EU Deforestation Regulation cutoff date of 31 December 2020.
> 
> Across all 290 mills, the satellite record reveals 890,168 hectares of post-2020 forest clearing, with every single mill showing measurable nearby loss. I have synthesized both pipelines into a balanced Mismatch Score, cross-validated the findings using NASA's Prithvi foundation model, radar SAR, and oil palm land cover maps, and completed the full 9-chapter thesis draft."

### Phase 2: Highlighting Methodology & Engineering Rigor (5-10 Minutes)
- Walk through the **Mismatch Formula**: $0.35 \times \text{Forest Loss} + 0.35 \times \text{Specificity} + 0.15 \times \text{Sentiment} + 0.15 \times \text{Spatial Match}$.
- Mention that text evidence (50%) and physical evidence (50%) are balanced so the score flags contradictory claims rather than just raw deforestation.
- Share the **Data Engineering Obstacles**: The SD Guthrie parent-subsidiary fix (recovering 142k ha), UML coordinate string repair, and GEE memory scaling.
- Highlight the **NLP Gold Benchmark**: Fine-tuned environmental-claims classifier scored **0.981 F1**, vastly outperforming keyword search (**0.828 F1**).

### Phase 3: The Headline Findings & Case Studies (5-10 Minutes)
- **KLK (#1):** Demonstrates how high specificity (100.0) combined with 92k ha loss triggers the strongest mismatch alert.
- **GAR (#2):** Explains how 171k ha loss sits next to 99.8% traceability claims and highly positive language (91.6 sentiment).
- **IOI (#4):** Clarifies that IOI has the highest physical clearing intensity (19.04%, 80% severe mills), but its low specificity (0.0) pulled its mismatch rank down.
- **Astra Agro (#11):** Emphasizes that ranking 11th does not mean clean (87k ha loss), but reflects vague, flat corporate disclosure.

### Phase 4: Cross-Validations & Interactive Demo (5 Minutes)
- Offer to show the **Interactive Showcase Website**: Leaflet map with 290 mills, satellite clearing modal, and live weight simulator (`scripts/run_website.py`).
- Discuss the **Prithvi Foundation Model**: Show Table 4.7, where general-purpose embeddings independently recovered forest loss without supervised labels ($\rho = 0.172$).
- Discuss the **Descals Oil Palm Overlay**: Confirm that 56% of post-2020 loss is already classified as oil palm (up to 89.8% for IOI).

### Phase 5: Next Steps & Closing (Last 3 Minutes)
- State that the LaTeX manuscript has been packaged into `latex/thesis_latex.zip`.
- Ask for any final feedback or structural adjustments before submission on 26 September.

---

## 11. Anticipated Questions from Professor Hoseini & Model Answers

**Q1: "Can you prove that these mills directly caused this 890,168 hectares of deforestation?"**  
*Answer:*  
"No, Professor, and the thesis explicitly acknowledges this distinction. Drawing a 10 km radial buffer approximates a mill's Fresh Fruit Bunch sourcing catchment, but smallholders and third-party concessions operate within the same area. Our method measures spatial proximity and correspondence, not legal causality. However, our Descals land cover cross-validation shows that 56% of this cleared land has already been converted to oil palm (reaching 89.8% for IOI), proving that the clearing is directly tied to the palm oil sector."

**Q2: "Why does Astra Agro rank lowest (Rank 11) despite having 87,198 hectares of forest loss?"**  
*Answer:*  
"This is a key finding of our mismatch formula. Astra Agro's sustainability disclosure contained almost no specific targets (Specificity: 13.8) and maintained a flat, procedural tone (Sentiment: 0.0). The model measures the mismatch between promise and physical reality. Because Astra Agro promised little, the gap between its statements and satellite evidence was small. We emphasize in Chapter 4 and Chapter 5 that Astra Agro is not 'clean', and that vague disclosure can serve as a corporate shield against greenwashing detection."

**Q3: "Why did you use FinBERT instead of ClimateBERT climate-sentiment for the scoring formula?"**  
*Answer:*  
"We evaluated both across 403 claims and found they agreed on only 53.1% of sentences ($\kappa = 0.08$). ClimateBERT climate-sentiment classified 99.8% of claims as either 'opportunity' or 'neutral', detecting virtually zero risk. In contrast, FinBERT accurately captures corporate confidence and promotional optimism. Because greenwashing involves overly positive rhetoric contrasted against physical clearing, FinBERT provides the appropriate signal for corporate tone."

**Q4: "Why did you drop production normalization from the thesis?"**  
*Answer:*  
"We initially attempted to compute deforestation intensity per tonne of Crude Palm Oil. However, upon auditing company annual reports and RSPO ACOP filings, we found severe inconsistencies: companies mixed third-party fruit purchases, plantation output, and downstream refinery sales into single figures, while others omitted volumes. Using estimated denominators would have introduced major measurement bias and weakened our defense. Dropping it ensured our metrics remained empirically solid."

**Q5: "What makes your work novel compared to PalmWatch?"**  
*Answer:*  
"PalmWatch measures physical brand deforestation footprints using satellite data, but ignores corporate claims. Recent literature (such as Ong et al., 2025 and Calamai et al., 2025) highlights that existing greenwashing tools only evaluate text without independent ground truth. My thesis bridges this gap by combining NLP claim extraction with satellite verification into a single, automated auditing framework."
