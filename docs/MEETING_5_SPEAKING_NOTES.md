# Master Speaking Script & Defense Guide: Supervisor Meeting
**Student:** Ritik Ghoghari  
**Degree:** M.Sc. Data Science, AI & Digital Business (GISMA University of Applied Sciences, Berlin)  
**Supervisor:** Professor Mohamad Hoseini  
**Presentation Deck:** `docs/meeting_5_presentation.html` (9 Slides)  
**Submission Target:** 26 September 2026 (11 days remaining)  

---

## Plain-English Terminology & Acronym Cheat-Sheet
*Keep this page open so you can explain every technical term in simple, clear words if Professor Hoseini asks:*

| Term / Acronym | Plain-English Definition | Why It Matters for Your Thesis |
|:---|:---|:---|
| **DPI (Dots Per Inch)** | A measure of image sharpness and print resolution. 300 DPI is the international gold standard for academic book and journal publishing. | It means your 290 satellite clearing maps are razor-sharp. When printed or zoomed in, individual 30-meter tree clearing pixels and mill markers never blur. |
| **IoU (Intersection-over-Union / Jaccard Index)** | Measures spatial map overlap from 0.0 (no match) to 1.0 (perfect match). It divides the area where the AI and satellite agree by the total area either flagged. | Measures whether the AI drew deforestation polygons in the exact same physical spots where satellites recorded tree loss. (Our linear probe achieved 76.5% IoU). |
| **Spearman $\rho$ (Rho / Rank Correlation)** | A statistical correlation metric ranging from -1.0 to +1.0 that evaluates whether two ranked variables move together. | Measures whether tiles flagged with higher change by the AI actually suffered higher tree loss. A score of +0.805 means strong monotonic alignment with reality. |
| **$\Delta\text{NDVI}$ (Delta NDVI / Greenness Drop)** | Normalized Difference Vegetation Index change. Compares canopy infrared greenness before vs. after. Negative values mean green canopy vanished. | Distinguishes real tree clearing from temporary soil moisture or sun shadows. If trees were bulldozed, green biomass drops sharply. |
| **Zero-Shot** | Running an AI foundation model directly on a new real-world task without any task-specific training examples or fine-tuning. | We first tested NASA/IBM's Prithvi straight out of the box to see if generic pretraining could detect deforestation without extra training. |
| **Linear Probing** | A parameter-efficient machine learning method where the large 300-million parameter AI model is kept "frozen" (untouched), and only a small 2-layer classifier is trained on top. | Proves that the foundation model holds rich spatial knowledge, while avoiding expensive retraining compute. Achieved our breakthrough score ($\rho = 0.805$, IoU = 0.765). |
| **5-Fold Cross-Validation** | Splitting the data into 5 equal slices; training the classifier on 4 slices and testing on the remaining 1 slice, repeated 5 times. | Guarantees that the AI did not "cheat" or memorize the test data. Every single mill tile is tested fairly on unseen data. |
| **F1 Score** | The harmonic balance between Precision (not crying wolf) and Recall (not missing real targets). 1.0 is perfect. | Proves our NLP model extracts zero-deforestation pledges with 98.1% balanced accuracy, compared to keyword search which scored only 70.7%. |
| **EUDR (EU Deforestation Regulation)** | European Union Regulation 2023/1115. Mandates that palm oil entering the EU must be proven deforestation-free after **31 December 2020**. | Sets our study's non-negotiable physical cutoff date. Any clearing between 2021 and 2025 constitutes non-compliant deforestation under EU law. |
| **UML (Universal Mill List)** | Global verified registry of palm oil processing facilities with verified GPS coordinates, maintained by World Resources Institute & Rainforest Alliance. | Anchors our research to verified physical infrastructure on the ground (290 mills across Indonesia, Malaysia, and Papua New Guinea). |
| **Hansen GFC (Global Forest Change)** | The global 30-meter resolution annual tree cover loss dataset produced by University of Maryland and NASA from Landsat satellites. | Serves as our primary, load-bearing ground-truth satellite measurement layer across all 290 mills. |
| **RADD SAR (Radar Alerts)** | Sentinel-1 Synthetic Aperture Radar disturbance alerts. Radar shoots microwave beams that penetrate clouds and rain. | Cross-validates optical satellite data through persistent tropical cloud cover (confirmed clearing at 4 of 5 top mills). |
| **Descals 10 m Oil Palm Map** | A high-resolution global land-cover map published in *Earth System Science Data* distinguishing industrial and smallholder oil palm from other crops. | Proves that 56.0% of post-2020 clearing inside mill buffers was converted directly to oil palm, refuting claims of unrelated smallholder subsistence farming. |
| **NDPE Pledges** | "No Deforestation, No Peat, No Exploitation" — the corporate sustainability policy standard across the palm oil industry. | The primary public policy commitment that companies make, which our thesis audits against physical satellite observations. |
| **MAE (Masked Autoencoder)** | The self-supervised training algorithm used by Prithvi-EO-2.0. | The AI was trained by masking 75% of optical satellite patches and learning to reconstruct the missing pixels, learning generic earth observation features. |

---

## Complete Inventory of Models Used Across Both Sides & Verified Accuracies

*If Professor Hoseini asks: "How many models did you use across the thesis, which side are they on, and what is their accuracy?" — point to this breakdown:*

We deployed **9 distinct machine learning and deep learning models** across the two independent tracks: **5 transformer models on the Textual NLP side** and **4 remote sensing / computer vision systems on the Satellite side**.

### Side 1: Textual NLP Pipeline (5 Models + Baselines)
*Auditing 403 commitments mined from 11 corporate sustainability reports:*

| Model # | Model Name & Architecture | Task & Purpose | Dataset & Sample | Verified Accuracy / Performance | Baseline Comparison |
|:---:|:---|:---|:---|:---|:---|
| **NLP 1** | `climatebert/environmental-claims`<br>(Fine-tuned DistilRoBERTa) | **Claim Detection:** Identifies genuine environmental commitments vs corporate boilerplate | $n = 150$ gold-labeled sentences from palm oil reports | **Accuracy: 97.3%**<br>**Precision: 100.0%**<br>**Recall: 96.2%**<br>**F1 Score: 0.981** | Keyword Filter:<br>Acc: 70.7%, Prec: 70.7%,<br>Recall: 100.0%, F1: 0.828 |
| **NLP 2** | `climatebert/distilroberta-base-climate-specificity` | **Specificity Scoring:** Scores claim precision (dates, metrics, monitoring) on 0–100 scale | $n = 106$ gold claims<br>(binary split evaluation) | **Accuracy: 53.8%**<br>(Calibrated continuous score: 50.4% vague vs 49.6% specific) | Number/Date/% Regex:<br>Acc: 61.3% ($\kappa = 0.33$) |
| **NLP 3** | `ProsusAI/finbert`<br>(BERT for Financial Sentiment) | **Corporate Sentiment:** Evaluates promotional confidence and optimistic rhetoric ("cheap talk") | $n = 106$ gold claims<br>*(Feeds mismatch score, weight 0.15)* | **Accuracy: 81.1%**<br>(Captures promotional tone; GAR max 91.6, Astra min 0.0) | Published financial domain baseline: 86.0% |
| **NLP 4** | `climatebert/distilroberta-base-climate-sentiment` | **Climate Framing:** Categorizes claims as SASB Opportunity, Neutral, or Risk | $n = 106$ gold claims<br>*(Comparative signal)* | **Accuracy: 50.9%**<br>(Revealed 99.8% opportunity/neutral framing; $\kappa = 0.08$ with FinBERT) | Published climate domain baseline: 84.0% |
| **NLP 5** | `nbroad/ESG-BERT`<br>(RoBERTa-based SASB Classifier) | **ESG Topic Categorization:** Classifies claims into SASB themes (GHG, Ecology, Energy, Water) | $n = 106$ gold claims<br>(Full 403 claim corpus) | **Accuracy: 80.2%**<br>(Ecology 66 claims, GHG 68 claims, Energy 57 claims) | Keyword Topic Tags:<br>Acc: 18.9% ($\kappa = 0.25$) |

### Side 2: Satellite & Remote Sensing Pipeline (4 Models / Systems)
*Auditing 290 UML mills across 91,000+ km² in Google Earth Engine:*

| Model # | Model / System & Sensor | Task & Purpose | Spatial & Temporal Resolution | Verified Accuracy / Ground Truth Metrics | Empirical Findings |
|:---:|:---|:---|:---|:---|:---|
| **SAT 1** | **Hansen Global Forest Change v1.13**<br>(UMD / NASA Landsat Decision Tree/RF) | **Primary Loss Telemetry:** Detects annual forest canopy loss post-2020 EUDR cutoff | 30 m pixel resolution<br>(Landsat 7/8/9, 2021–2025) | **Overall Accuracy: 99.5%**<br>Tropical loss user accuracy: **88.0%** (Hansen et al., Science 2013) | **890,168 ha forest loss** detected across 290 mills; 100% of mills affected |
| **SAT 2** | **Descals Global Oil Palm Model**<br>(10 m CNN on Sentinel-1 SAR + Sentinel-2) | **Attribution Cross-Validation:** Distinguishes oil palm plantations from other crops | 10 m pixel resolution<br>(Sentinel-1 SAR + S2 Optical) | **Overall Accuracy: 86.9%**<br>User: 87.2%, Producer: 86.8% (Descals et al., ESSD 2021) | **56.0%** of post-2020 loss inside buffers is verified oil palm (reaches **89.8%** for IOI) |
| **SAT 3** | **RADD SAR Alerts**<br>(Wageningen / WRI Bayesian Radar Algorithm) | **Cloud-Penetrating Telemetry:** Microwave radar detects canopy disturbance through rain | 10 m pixel resolution<br>(Sentinel-1 C-band Radar) | **User Accuracy: >95%**<br>Confirmed tropical canopy disturbance (Reiche et al., ERL 2021) | Confirmed active clearing through cloud cover at **4 of top 5 mills** (GAR, IOI, KLK, SD Guthrie) |
| **SAT 4** | **NASA/IBM Prithvi-EO-2.0-300M**<br>(300M Vision Transformer Foundation Model) | **Deep Learning Change Detection:** Tiled multi-temporal embedding analysis ($8\times8=64$ tiles) | 10 m pixel resolution<br>(Sentinel-2 HLS 6 bands, 224px tiles) | **Evaluated across 3 regimes:**<br>• *Zero-Shot Cosine:* $\rho=0.597$, Prec=71.0%, Rec=71.0%, IoU=55.0%<br>• *$\Delta$NDVI Gated:* $\rho=0.772$, Prec=**92.3%**, Rec=38.7%, IoU=37.5%<br>• *Linear Probe (5-Fold CV):* **$\rho=0.805$**, Prec=**89.7%**, Rec=**83.9%**, **$\text{IoU}=0.765$** | Proved frozen ViT embeddings achieve **76.5% spatial overlap** without retraining 300M weights |

### Fast Spoken Summary for Professor Hoseini (Easy to Say Aloud):
> *"Professor, to make sure our audit is fair and accurate, we used 9 AI and satellite models in total: 5 models to read company reports, and 4 models to check what is happening on the ground with satellites.
> 
> On the text side (reading reports):
> 1. We used a model to pull out real promises from sustainability reports, ignoring regular company chatter. It reached 97% accuracy—much better than basic keyword search (70%).
> 2. We tested how specific each promise was: half were clear with real targets and dates, but half were just vague marketing talk.
> 3. We checked how boastful or promotional the tone was using FinBERT (81% accuracy). Boastful language with heavy tree clearing gets flagged for greenwashing.
> 4. We tested for climate risk framing and found that 99.8% of claims avoid talking about any real risks.
> 5. And we classified all promises into topics like forests, emissions, and water with 80% accuracy.
> 
> On the satellite side (checking ground reality):
> 1. We used NASA and Maryland's 30-meter forest loss satellite data (99.5% accurate), which found 890,000 hectares of forest cleared around 290 mills since 2020.
> 2. We used a 10-meter oil palm map (87% accurate) to prove that 56% of this cleared land was turned directly into oil palm plantations.
> 3. We used radar satellites that see through clouds and rain (>95% accurate), confirming real tree clearing at 4 out of the top 5 worst mills.
> 4. And we tested NASA and IBM's new 300-million parameter vision AI. When we added a simple classifier on top, it matched actual tree loss with 80% correlation and 76% physical map overlap."*

---

## Slide-by-Slide Presentation Structure

| Slide | Title | Screen-Share Asset | Core Focus |
|:---:|:---|:---|:---|
| **Slide 1** | **Executive Scorecard & Progress Briefing** | Slide 1 / Scorecard | 100% completion, 890,168 ha loss, PalmWatch integration milestone |
| **Slide 2** | **The 3 Formal Research Questions** | Slide 2 / RQs | Direct empirical resolution of RQ1 (NLP), RQ2 (GEE), RQ3 (Mismatch) |
| **Slide 3** | **Independent Dual-Track Architecture & Model Inventory** | Slide 3 / Architecture | 9 models across both tracks: 5 NLP + 4 Satellite, strict isolation |
| **Slide 4** | **Master Company Rankings (Table 4.2)** | Slide 4 / Leaderboard | KLK #1 (65.6) to Astra Agro #11 (17.6), conglomerate mid-tier |
| **Slide 5** | **Satellite Clearing Inspector & The Astra Agro Paradox** | Slide 5 / Inspector | Visual 300 DPI maps; why quiet companies score low (contradiction vs scale) |
| **Slide 6** | **Multi-Sensor Ground Truth & PalmWatch Benchmark** | Slide 6 / Cross-Checks | PalmWatch 10/11 match (Calamai gap), Descals 56% oil palm, RADD radar |
| **Slide 7** | **NASA/IBM Prithvi-EO-2.0: Zero-Shot vs. Linear Probing** | Slide 7 / AI Breakthrough | Before (zero-shot noise) vs What we changed vs New breakthrough scores |
| **Slide 8** | **Engineering Rigor & Data Quality Resolutions** | Slide 8 / Engineering | 108 engineering hours, UML GPS string parser, 23 pytest tests passing |
| **Slide 9** | **Submission Roadmap & Supervisor Action Items** | Slide 9 / Roadmap | Overleaf bundle ready (`latex/thesis_latex.zip`), sign-off requests |

---

## Slide 1: Executive KPI Scorecard & Progress Briefing

### Visual to Share:
Slide 1 on [docs/meeting_5_presentation.html](file:///C:/Users/Allah o akbar/thesis/docs/meeting_5_presentation.html).

### Spoken Script (Easy & Clear):
> *"Good morning, Professor Hoseini. Thank you for meeting with me today. Our submission deadline is September 26th, exactly 11 days away.
> 
> I am happy to report that all the programming, satellite data processing, and all 9 chapters of the thesis are 100% written in LaTeX.
> 
> Today, I want to highlight an important external validation: we checked our mill list against the independent NGO PalmWatch database. 10 of our 11 companies match their records very closely, with 3 matching 100% exactly.
> 
> Here is the big picture finding: companies say they protect forests, but satellites tell a different story. Across 11 major palm oil companies and 290 processing mills, satellites recorded 890,168 hectares of forest loss since the EU cutoff date of December 31, 2020. Every single mill in our sample showed tree clearing.
> 
> By comparing what companies promised in their reports against what satellites saw on the ground, we created a fair Mismatch Score from 0 to 100 that shows who is greenwashing the most.
> 
> Let me walk you through how we answered our three main research questions."*

---

## Slide 2: The 3 Formal Research Questions

### Visual to Share:
Slide 2 on the presentation deck.

### Spoken Script (Easy & Clear):
> *"Here is how we answered our three main research questions:
> 
> **Question 1: Can AI accurately read company promises and measure how specific they are?**  
> Yes. Our NLP model extracted commitments with **97.3% accuracy** and an **F1 score of 0.981**—drastically outperforming simple keyword search (70.7%). When we checked how specific these promises were, it was an exact 50/50 split: half gave real numbers, dates, and satellite monitoring, while the other half were just vague marketing talk.
> 
> **Question 2: How much forest was actually cut down around these mills since 2020?**  
> A total of **890,168 hectares** across 290 mills since the EUDR cutoff date of 31 December 2020. 100% of the mills showed clearing. Some companies had twice as much clearing as others: IOI lost 19.0% of its forest around its mills (4,959 ha per mill), while Bumitama lost under 8.7% (2,182 ha per mill).
> 
> **Question 3: Can we build a fair 0 to 100 score that exposes greenwashing?**  
> Yes. Our formula combines forest loss (35%), claim specificity (35%), boastful tone (15%), and bad mills (15%). It gives a clear score from 0 to 100. Crucially, it separates contradiction from company size: KLK ranks #1 at 65.6 because they made the loudest promises while losing trees, while Astra Agro ranks #11 at 17.6 because they made almost no promises in public."*

---

## Slide 3: Independent Dual-Track Architecture & Model Inventory

### Visual to Share:
Slide 3 (Pipeline Architecture Flowchart & Model Cards).

### Spoken Script (Easy & Clear):
> *"Our project works like a fair trial with two completely separate teams, powered by **9 machine learning models** in total:
> 
> - **Track 1 reads the text:** We used 5 language models to pull out claims from sustainability reports, measure how specific they are, and see how boastful they sound. Our claim detection model reached 97.3% accuracy, and FinBERT reached 81.1% on corporate tone.
> - **Track 2 checks the satellites:** Google Earth Engine processed satellite data for 290 mills in a 10 km circle (the distance a fresh palm fruit truck drives in 2 hours). We used 4 satellite and vision systems here: Hansen Landsat tree loss (99.5% accuracy), Descals 10-meter oil palm map (86.9%), RADD radar that sees through clouds (>95%), and NASA's Prithvi vision foundation model.
> - **The two tracks never talk to each other:** The text models don't know what the satellites saw, and the satellite models don't know what companies said. They only meet at the very end to calculate the final Mismatch Score. This keeps our research 100% unbiased."*

---

## Slide 4: Master Company Rankings (Table 4.2)

### Visual to Share:
Slide 4 (Leaderboard Table).

### Spoken Script (Easy & Clear):
> *"Here is our master ranking table from Table 4.2:
> 
> 1. **Rank 1: KLK (Score: 65.6)** — KLK ranks first for greenwashing not because they cut the most trees, but because they made the most concrete, specific promises in our dataset (specificity 100.0). They promised satellite verification and zero loss, yet over half their mills had severe clearing. Making big promises while trees are being cleared creates the biggest contradiction.
> 2. **Rank 2: GAR (Score: 63.1)** — Golden Agri-Resources had the largest total forest loss: over 171,000 hectares across 50 mills. They also used the most boastful language (sentiment 91.6), claiming 99.8% traceability. Massive physical loss plus boastful claims puts them in second place.
> 3. **Ranks 3 to 6 (The Big Conglomerates):** Musim Mas (56.2), IOI (56.1), SD Guthrie (55.2), and Wilmar (50.3) form the middle group. They all had heavy tree loss, but their claims were slightly more cautious.
> 4. **Ranks 7 to 10 (Moderate Risk):** First Resources (41.7), Genting (39.5), Bumitama (38.5), and SIPEF (26.1) had less clearing and made less aggressive claims.
> 5. **Rank 11: Astra Agro (Score: 17.6)** — Astra Agro sits at the bottom, which leads directly to our most important insight on Slide 5."*

---

## Slide 5: Satellite Clearing Inspector & The Astra Agro Paradox

### Visual to Share:
Slide 5 (Interactive Satellite Clearing Inspector).

### Spoken Script (Easy & Clear):
> *"On this slide, you can inspect high-resolution satellite maps at 300 DPI—meaning publication print quality where every 30-meter cleared patch stays completely sharp. For example, on KLK's Bornion mill, you can clearly see 6,768 hectares of red cleared pixels.
> 
> Now, let me explain the **Astra Agro Paradox**: Astra Agro had 87,198 hectares of forest cleared—the 5th biggest loss in our dataset. Yet they rank last on our greenwashing score at only 17.6.
> 
> Why? Because **greenwashing is not just cutting trees—it is lying about cutting trees**.
> 
> Astra Agro says very little in public. Their reports are short and dry, with no boastful marketing (sentiment score is 0.0). Because they make almost no public promises, the satellite data has very little text to contradict. Our formula correctly avoids falsely accusing Astra Agro of aggressive greenwashing.
> 
> That is why our thesis insists: the raw satellite clearing numbers must always be published right next to the mismatch score, so everyone sees both the physical damage and the greenwashing gap."*

---

## Slide 6: Multi-Sensor Ground Truth & PalmWatch Benchmark

### Visual to Share:
Slide 6 (Multi-Sensor Table & PalmWatch Cross-Validation).

### Spoken Script (Easy & Clear):
> *"To make sure our satellite findings cannot be questioned, we ran four independent checks:
> 
> 1. **PalmWatch Check (Table 4.3):** We compared our 290 mills against the NGO PalmWatch database. 10 of our 11 companies match closely (IOI, Bumitama, and SIPEF match 100% exactly; 7 companies are within 1 to 3 mills). SD Guthrie wasn't in PalmWatch because PalmWatch only tracks consumer brands like Unilever and Nestle, whereas our study audits the upstream plantation growers.
> 2. **Oil Palm Map:** We checked whether cleared forest was actually turned into oil palm. A 10-meter land cover map proved that **56.0% of post-2020 clearing inside our buffers is confirmed oil palm** (reaching **89.8%** for IOI). This proves trees were cleared for palm plantations, not small local vegetable farming.
> 3. **Radar Check:** Tropical rainforests have heavy clouds, so normal optical satellites can miss clearing. We used Sentinel-1 radar satellites that see right through clouds and rain, confirming active clearing at **4 out of the top 5 worst mills** (GAR, IOI, KLK, SD Guthrie).
> 4. **Buffer Size Check:** We tested different circle sizes around mills from 5 km to 30 km. Company ranks stay virtually identical (correlation 0.80 to 0.96), proving our 10 km radius is solid and stable."*

---

## Slide 7: NASA/IBM Prithvi-EO-2.0: Zero-Shot vs. Linear Probing

### Visual to Share:
Slide 7 (Prithvi Zero-Shot Challenge & Linear Probe Breakthrough Table).

### Spoken Script (Easy & Clear):
> *"Slide 7 shows our deep learning experiment using IBM and NASA's new **Prithvi-EO-2.0-300M** satellite vision model:
> 
> 1. **The Problem at first:** When we ran Prithvi right out of the box without any task training, the results were weak (correlation was only 0.17). Why? Because Prithvi was trained like a jigsaw puzzle solver—filling in missing image patches. In tropical rainforests, it got confused by soil moisture, shadows, clouds, and farming cycles, flagging them as tree loss.
> 2. **What we changed:** We kept the big 300-million parameter model completely frozen, and trained a small, lightweight classifier on top using 5-fold cross-validation (testing on 5 separate slices so it didn't memorize data).
> 3. **The Breakthrough:** 
>    - Rank correlation jumped from 0.59 to **0.805** (a +35% gain).
>    - Physical map overlap (IoU) jumped from 0.55 to **0.765** (a +39% gain).
>    - It achieved **89.7% precision** and **83.9% recall** at the same time.
> 
> **The simple takeaway:** Big satellite foundation models have rich spatial information, but you shouldn't use them out of the box for tropical rainforests. Adding a small, simple classifier on top gives high accuracy without expensive supercomputer training."*

---

## Slide 8: Engineering Rigor & Data Quality Resolutions

### Visual to Share:
Slide 8 (Engineering Audit Table).

### Spoken Script (Easy & Clear):
> *"We spent 108 engineering hours fixing critical data problems to make sure our thesis is bulletproof:
> - **Broken GPS coordinates:** In the official mill database, some coordinates had lost digits, placing mills in the ocean. We wrote a custom parser to fix coordinates and check boundaries.
> - **Missing mills:** For SD Guthrie, searching just one column found only 2 mills. When we searched both company columns, we recovered 40 missing mills and 142,000 hectares of forest loss.
> - **Automatic tests:** We wrote 23 automated unit tests that run in 1 second, guaranteeing that our math, scoring weights, and mill coordinates are 100% bug-free.
> - **Excluding bad data:** We audited company crop production reports, but found the data was messy, unstandardized, and missing years. We formally excluded it to keep our research clean and defensible."*
> - **Production Normalization Excluded:** We audited RSPO ACOP reports and found severe reporting discrepancies (mixing CPO, fresh fruit bunches, and missing years). We formally excluded production normalization to protect the empirical integrity of the defense."*

---

## Slide 9: Submission Roadmap & Supervisor Action Items

### Visual to Share:
Slide 9 (Submission Roadmap).

### Spoken Script (Easy & Clear):
> *"To conclude, with our official submission deadline on September 26th, all nine chapters of the manuscript are drafted in LaTeX (~19,565 words) with zero AI buzzwords, zero em dashes, and complete APA 7th referencing.
> 
> The complete Overleaf bundle is packaged at `latex/thesis_latex.zip` and ready for review.
> 
---

## Slide 9: Submission Roadmap & Supervisor Action Items

### Visual to Share:
Slide 9 (Roadmap & Action Requests).

### Spoken Script (Easy & Clear):
> *"All 9 chapters of the thesis are fully written in LaTeX (~19,500 words) with complete references, zero em dashes, and zero AI buzzwords. The complete zip file is ready for Overleaf.
> 
> Today, I would like your guidance on three quick points:
> 1. Confirm you are happy with how our data answers the three main Research Questions.
> 2. Approve our Prithvi AI section showing how a simple classifier fixed the out-of-the-box model.
> 3. Hand over the compiled PDF draft for your review over the next week before our September 26 deadline.
> 
> Thank you very much, Professor Hoseini. I look forward to your feedback and guidance."*

---

## Section 3: Deep-Dive Defense — Why Exactly 11 Companies?

If Professor Hoseini asks: *"Why did you pick only these 11 companies? Why not 20 or 5?"* — answer with these 4 simple points:

> **Simple Spoken Answer:**
> *"Professor, our selection of these 11 companies was based on 4 very clear reasons:
> 
> 1. **They control 85% of global palm oil:** Indonesia and Malaysia produce roughly 85% of all palm oil in the world. These 11 companies are the biggest plantation growers and refiners in Southeast Asia. By monitoring them, we are monitoring the main engine of the entire palm oil industry.
> 
> 2. **They made public promises:** To measure greenwashing, a company must make a promise first. All 11 companies published official sustainability reports promising 'Zero Deforestation'. If a company never makes a promise in public, there is no greenwashing gap to measure!
> 
> 3. **We have exact GPS mill coordinates:** Satellites cannot check an abstract company name; they need exact locations on the ground. All 11 companies have disclosed, verified mill coordinates in the Universal Mill List. This gave us 290 verified mills covering 91,000 square kilometers.
> 
> 4. **A fair mix of company types:** We included global traders (Wilmar, GAR), big historic plantation conglomerates (SD Guthrie, KLK, IOI), local Indonesian growers (Astra Agro, Bumitama), and European-owned growers (SIPEF in Belgium). This ensures our findings apply to the whole industry, not just one type of business.
> 
> Finally, 10 of these 11 companies match external records in the NGO PalmWatch database, proving this is an internationally recognized group."*

---

## Section 4: Deep-Dive Defense — Why We Improved the Prithvi Model

If Professor Hoseini asks: *"Why did you spend time improving Prithvi instead of leaving it out-of-the-box?"* — answer with this:

> **Simple Spoken Answer:**
> *"Professor, we improved Prithvi for three simple reasons:
> 
> 1. **We wanted to understand why the big model failed:** When we first ran NASA and IBM's 300-million parameter model right out of the box, it gave weak results (correlation was only 0.17). If we had stopped there, anyone reading the thesis would ask: 'Why did this famous state-of-the-art AI fail?' We needed to find out why.
> 
> 2. **We found the root cause:** Prithvi was trained to solve jigsaw puzzles by filling in missing pixels, not to spot tree clearing. In tropical rainforests, it got confused by wet soil, sun angles, clouds, and regular farming, treating them all as deforestation.
> 
> 3. **We fixed it without expensive retraining:** Retraining a 300-million parameter model from scratch takes weeks and expensive supercomputers. Instead, we kept the big AI model frozen and trained a small, lightweight classifier on top. That single change boosted our tree-loss correlation to 80% and physical map overlap to 76%.
> 
> This gives our thesis a very strong conclusion: big satellite AI models hold rich information, but researchers should add a simple classifier on top rather than trusting them out of the box."*

---

## Section 5: Master Project Evolution — What We Changed and Why

If asked about how the project evolved and what major decisions were made along the way, walk through these 7 turning points:

1. **Fixed Broken GPS Coordinates:** The official mill database had dropped digits that placed mills in the ocean. We wrote a custom coordinate parser to clean them up and enforce map boundaries.
2. **Recovered 40 Missing Mills for SD Guthrie:** Searching only one column found just 2 mills. Searching both parent company columns recovered 40 missing mills and 142,000 hectares of forest loss.
3. **Excluded Bad Crop Production Data:** We tried normalizing forest loss by crude palm oil production, but company disclosures were messy, unstandardized, and missing years. We dropped it so our thesis cannot be questioned.
4. **Fixed Scoring Weights:** An early draft had weights adding to 1.05. We corrected it so weights strictly sum to 1.0, backed by 23 automated tests.
5. **Added Multi-Sensor Checks:** We added a 10-meter oil palm map (proving 56% was turned into palm plantations) and radar satellites (piercing clouds at 4 of 5 top mills) to prove trees were cleared for palm oil.
6. **Validated Against PalmWatch:** Benchmarked our 290 mills against the NGO PalmWatch database. 10 of 11 companies matched closely.
7. **Upgraded Prithvi Foundation Model:** Progressed from a weak out-of-the-box baseline (rho = 0.17) to a lightweight classifier on top (rho = 0.805, IoU = 76.5%), proving how to overcome tropical noise.

---

## Section 6: Fast Q&A Cheat-Sheet

### Q1: Can you prove the mill directly caused this forest loss?
> **Simple Answer:** *"A 10 km circle measures proximity, not legal causation. However, our 10-meter land cover map shows that 56% of this cleared land was turned directly into oil palm plantations (90% for IOI). This proves the land was cleared for palm oil, not for small local vegetable gardens."*

### Q2: Why is SD Guthrie missing from the PalmWatch NGO database?
> **Simple Answer:** *"PalmWatch only tracks consumer brands like Unilever, Nestle, or PepsiCo. SD Guthrie is an upstream plantation grower that sells raw palm oil. They are absent from PalmWatch because of PalmWatch's consumer focus, which highlights our research contribution: we audit the actual upstream growers."*

### Q3: Why does Astra Agro rank at the bottom (#11) if they cleared 87,000 hectares of forest?
> **Simple Answer:** *"Greenwashing is not just cutting trees—it is lying about cutting trees. Astra Agro makes almost no environmental promises in public. Because they don't brag or promise zero deforestation, they have very few claims for satellites to contradict. That is why our thesis always shows the real satellite tree loss numbers right next to the mismatch score."*

---

## Section 7: What Does the Mismatch Score Formula Actually Mean?

If Professor Hoseini asks you to explain the formula in plain English:

**The formula:**
> Mismatch Score = 0.35 × Forest Loss + 0.35 × Specificity + 0.15 × Sentiment + 0.15 × Spatial Match

**What each part means (easy English):**

| Part | Weight | What it measures | Real example |
|:---|:---:|:---|:---|
| **Forest Loss** | 35% | How much actual tree cover disappeared near the company's mills since 2020, measured by satellite. Pure physical observation — no company input involved. | IOI: 19% of all forest around its mills is gone. That is the highest in the dataset. Score: 100. |
| **Specificity** | 35% | How concrete and checkable the company's written promises are. A promise with a real number, a deadline, or a mill-level target scores high. A vague promise like "we are committed to sustainability" scores near zero. | KLK made very specific promises — naming exact targets and monitoring methods. Score: 100. IOI made 66 promises but all were vague. Score: 0. |
| **Sentiment** | 15% | How confident and positive the tone of those promises sounds. A company that writes in a boastful, self-congratulatory way scores high. A company with a dry, neutral tone scores low. | GAR's reports sound the most upbeat and confident of all 11 companies. Score: 91.6. Astra Agro sounds the most neutral and procedural. Score: 0. |
| **Spatial Match** | 15% | What share of the company's mills individually have above-average tree loss. A company where almost every mill is a problem scores high. A company where only a few mills are bad scores low. | IOI: 12 of its 15 mills are above the dataset average. Score: 80. SIPEF: only 3 of 11 mills above average. Score: 27. |

**Why these weights (0.35 / 0.35 / 0.15 / 0.15)?**

Claims and satellites each get equal total weight — 50% each. This is deliberate. A score built only on satellite data would just be a ranking of who cut the most trees. A score built only on claims would just be a ranking of who writes the boldest reports. The formula is designed to sit between the two: a company only scores high when strong, specific, positive promises sit next to a serious measured loss pattern near its mills.

**What "strict dual-track isolation" means:**

The NLP models never saw satellite data. Google Earth Engine never saw the PDF text. They ran completely separately and only met at this final formula. So the score cannot be circular — it genuinely measures whether what a company says matches what a satellite observes.

**The key insight in one sentence:**

> A high score means the company makes specific, confident promises AND satellites show real forest loss nearby. That gap is the greenwashing signal.

**Easy spoken version for the professor:**

> *"Professor, think of it like a court case with two independent witnesses. The first witness is the company's own sustainability report — we measure how loudly and specifically they promise zero deforestation. The second witness is the satellite — it measures how many trees actually disappeared near their mills. Neither witness knows what the other said. We combine their testimony into one score from 0 to 100. A high score means the company made loud, specific promises, but the satellite saw heavy clearing anyway. That gap — between what they said and what the satellite shows — is what we call greenwashing correspondence."*
