# THESIS PROGRESS BRIEFING · SUPERVISOR MEETING 5
### *Catching Greenwashing from Space: Verifying Palm Oil Zero-Deforestation Claims Using Satellite Data and NLP*
**Student:** Ritik Ghoghari · **Degree:** M.Sc. Data Science, AI & Digital Business · **Supervisor:** Professor Mohamad Hoseini  
**University:** GISMA University of Applied Sciences, Berlin · **Submission Deadline:** 26 September 2026  
**Format:** 40-Minute Executive Presentation & Discussion Deck

---

```text
====================================================================================================
                                      EXECUTIVE KPI SCORECARD
====================================================================================================
 [ COMPANIES AUDITED ]       [ MILLS MONITORED ]       [ POST-2020 FOREST LOSS ]   [ PYTEST STATUS ]
       11 Groups                  290 Facilities              890,168 Hectares        23 / 23 PASS  
  (GAR, Wilmar, KLK, etc.)    (UML Registry Verified)     (Hansen GEE Telemetry)     (100% Verified)
----------------------------------------------------------------------------------------------------
 [ NLP CLAIM ACCURACY ]      [ DESCALS OIL PALM ]      [ PALMWATCH BENCHMARK ]     [ THESIS DRAFT ]
        97.3%                      56.0%                      10 / 11 Matches         9 Chapters    
    (F1 = 0.981 Gold Set)     (Overlay Confirmed)       (3 Exact · 7 Near ±1-3)      (19,565 Words) 
====================================================================================================
```

```text
====================================================================================================
               TODAY'S SPECIAL MILESTONE: EXTERNAL PALMWATCH CROSS-VALIDATION
====================================================================================================
 - Completed and integrated external mill registry validation against PalmWatch (Table 4.3).
 - 10 of 11 companies confirmed (IOI 15/15, Bumitama 14/14, SIPEF 11/11 exact; 7 within 1-3 mills).
 - Resolved SD Guthrie absence: PalmWatch tracks downstream consumer brands (Unilever, Nestlé),
   while this thesis audits upstream primary growers. Directly addresses Calamai et al. (2025) gap.
 - Written into LaTeX Chapters 3 (Methodology), 4 (Results Table 4.3), 5 (Discussion), and 8 (Refs).
====================================================================================================
```

---

## SLIDE 1 · 40-MINUTE MEETING AGENDA

```text
[00:00 - 05:00]  PART 1: Context, High-Level Narrative & Status (5 mins)
[05:00 - 14:00]  PART 2: Deep-Dive into the 3 Research Questions (9 mins)
[14:00 - 23:00]  PART 3: Master Rankings & The Astra Agro vs. KLK Paradox (9 mins)
[23:00 - 30:00]  PART 4: Multi-Sensor Validation & Prithvi Foundation Model (7 mins)
[30:00 - 34:00]  PART 5: Engineering Rigor, 23 Unit Tests & LaTeX Manuscript (4 mins)
[34:00 - 40:00]  PART 6: Professor Feedback, Discussion & Sign-off Timeline (6 mins)
```

---

## SLIDE 2 · RESEARCH QUESTIONS & DIRECT EMPIRICAL RESOLUTION

```text
+--------------------------------------------------------------------------------------------------+
| RQ1 (NLP EXTRACTION AND SPECIFICITY)                                                             |
| 'To what extent can transformer NLP reliably extract & classify zero-deforestation commitments?' |
+--------------------------------------------------------------------------------------------------+
  --> YES. Fine-tuned ClimateBERT achieved F1 = 0.981 and 97.3% Accuracy on 150 gold sentences.
  --> 403 claims enriched. Revealed a 50/50 split: 50% concrete targets vs 50% vague 'cheap talk'.

+--------------------------------------------------------------------------------------------------+
| RQ2 (SATELLITE FOREST LOSS TELEMETRY)                                                            |
| 'What magnitude of post-2020 forest loss is observable, and how does it vary across producers?'  |
+--------------------------------------------------------------------------------------------------+
  --> 890,168 ha lost across 290 mills post-2020 (EUDR cutoff 31 Dec 2020).
  --> Universal Loss: 100% of mills show clearing (105 ha to 12,318 ha per mill).
  --> Sharp Variance: IOI lost 19.04% of baseline forest vs Bumitama at 8.66%.

+--------------------------------------------------------------------------------------------------+
| RQ3 (COMPOSITE MISMATCH SCORING)                                                                 |
| 'Can a composite mismatch score produce a defensible and interpretable measure of divergence?'   |
+--------------------------------------------------------------------------------------------------+
  --> YES. 4-weight formula (0.35 Loss + 0.35 Spec + 0.15 Sent + 0.15 Spatial) yields 0-100 gradient.
  --> Separates contradiction from scale: KLK #1 (65.6) vs Astra Agro #11 (17.6).
```

---

## SLIDE 3 · INDEPENDENT DUAL-TRACK ARCHITECTURE

```text
                  ┌──────────────────────────────────────────────────────────┐
                  │          CORPORATE SUSTAINABILITY REPORTS (PDF)          │
                  └─────────────────────────────┬────────────────────────────┘
                                                │
                                                ▼
                  ┌──────────────────────────────────────────────────────────┐
                  │               TRACK 1: TEXTUAL NLP AUDIT                 │
                  │   - ClimateBERT Environmental Claims (F1 = 0.981)        │
                  │   - Continuous Specificity Scoring (0.0 to 1.0)          │
                  │   - FinBERT Promotional Sentiment (Positivity %)         │
                  └─────────────────────────────┬────────────────────────────┘
                                                │
                                                │ (Independent Outputs)
                                                ▼
┌───────────────────────────────────────────────────────────────────────────────────────────────┐
│              COMPOSITE MISMATCH SCORING ENGINE (Asserted Weights Sum = 1.0)                  │
│     Score = 0.35 * Forest Loss + 0.35 * Specificity + 0.15 * Sentiment + 0.15 * Spatial       │
└───────────────────────────────────────────────▲───────────────────────────────────────────────┘
                                                │
                                                │ (Independent Outputs)
                                                │
                  ┌─────────────────────────────┴────────────────────────────┐
                  │             TRACK 2: PHYSICAL SATELLITE AUDIT            │
                  │   - Universal Mill List (290 GPS Verified Mills)         │
                  │   - Google Earth Engine / Hansen GFC v1.13 (Landsat 30m) │
                  │   - 10 km Buffer Radius · EUDR Reference Cutoff (2020)   │
                  └─────────────────────────────▲────────────────────────────┘
                                                │
                  ┌─────────────────────────────┴────────────────────────────┐
                  │           PETABYTE EARTH OBSERVATION SATELLITES          │
                  └──────────────────────────────────────────────────────────┘
```

---

## SLIDE 4 · MASTER COMPANY RANKINGS (MISMATCH SCORE)

| Rank | Company | Mismatch Score | Visual Contradiction Meter | Post-2020 Loss | Matched Mills | Specificity | Sentiment |
|:---:|:---|:---:|:---|:---:|:---:|:---:|:---:|
| **#1** | **KLK** | **65.6** | `[█████████████░░░░░░░]` | 92,209 ha | 30 | 100.0 *(Max)* | 68.4 |
| **#2** | **GAR** | **63.1** | `[████████████░░░░░░░░]` | 171,236 ha | 50 | 67.6 | 91.6 *(Max)* |
| **#3** | **Musim Mas** | **56.2** | `[███████████░░░░░░░░░]` | 53,060 ha | 18 | 85.1 | 63.6 |
| **#4** | **IOI** | **56.1** | `[███████████░░░░░░░░░]` | 74,385 ha | 15 | 0.0 *(Min)* | 60.3 |
| **#5** | **SD Guthrie** | **55.2** | `[███████████░░░░░░░░░]` | 142,131 ha | 42 | 32.9 | 100.0 *(Max)* |
| **#6** | **Wilmar** | **50.3** | `[██████████░░░░░░░░░░]` | 127,606 ha | 45 | 67.2 | 70.0 |
| **#7** | **First Resources** | **41.7** | `[████████░░░░░░░░░░░░]` | 40,090 ha | 16 | 75.6 | 27.8 |
| **#8** | **Genting** | **39.5** | `[████████░░░░░░░░░░░░]` | 44,362 ha | 15 | 46.6 | 41.4 |
| **#9** | **Bumitama** | **38.5** | `[███████░░░░░░░░░░░░░]` | 30,549 ha | 14 | 67.1 | 71.4 |
| **#10** | **SIPEF** | **26.1** | `[█████░░░░░░░░░░░░░░░]` | 27,341 ha | 11 | 28.3 | 41.0 |
| **#11** | **Astra Agro** | **17.6** | `[███░░░░░░░░░░░░░░░░░]` | 87,198 ha | 34 | 13.8 | 0.0 *(Min)* |
| **--** | **Total / Network** | **--** | **--** | **890,168 ha** | **290** | **--** | **--** |

---

## SLIDE 5 · THE ASTRA AGRO VS. KLK PARADOX (SCIENTIFIC NOVELTY)

```text
┌──────────────────────────────────────────────┐  ┌──────────────────────────────────────────────┐
│          RANK #1: KLK (Score: 65.6)          │  │       RANK #11: ASTRA AGRO (Score: 17.6)     │
├──────────────────────────────────────────────┤  ├──────────────────────────────────────────────┤
│ - Forest Loss: 92,209 ha (Mid-pack)          │  │ - Forest Loss: 87,198 ha (5th Largest!)      │
│ - Claim Specificity: 100.0 (Maximum!)        │  │ - Claim Specificity: 13.8 (Near Bottom)      │
│ - Claim Sentiment:   68.4 (Confident)        │  │ - Claim Sentiment:    0.0 (Flat / Zero)     │
│                                              │  │                                              │
│ WHY #1?                                      │  │ WHY #11 DESPITE HEAVY CLEARING?              │
│ KLK promises concrete satellite monitoring   │  │ Astra Agro says almost nothing in public.    │
│ and zero loss. When specific commitments     │  │ Mismatch measures CONTRADICTION, not raw     │
│ clash with 92k ha loss, mismatch peaks!      │  │ harm. Quiet companies give less text to check│
└──────────────────────────────────────────────┘  └──────────────────────────────────────────────┘
```
> **Key Methodological Takeaway:** The mismatch score isolates greenwashing contradiction without punishing companies solely for operating large land banks. The raw loss table must always sit alongside!

---

## SLIDE 6 · MULTI-SENSOR GROUND TRUTH & PALMWATCH BENCHMARK

| Check | Focus | Key Evidence / Metric | Scientific Significance |
|:---|:---|:---:|:---|
| **1. PalmWatch Benchmark** | External Mill Count Validation | **10 of 11 Companies Match** (3 exact, 7 within 1-3 mills) | Confirms UML registry accuracy; clarifies that PalmWatch tracks downstream consumer brands while this thesis audits upstream growers. |
| **2. Descals 10 m Overlay** | Land Cover of Cleared Pixels | **56.0% Converted to Oil Palm** (IOI: 89.8%, SD Guthrie: 70.7%) | Eliminates the defense that buffer clearing was caused by unrelated smallholders or different crops. |
| **3. RADD SAR Radar** | Tropical Cloud Penetration | **4 of 5 Top Mills Confirmed** (GAR, IOI, KLK, SD Guthrie) | Proves active physical canopy disturbance during the monitoring period using radar backscatter. |
| **4. Buffer Sensitivity** | Spatial Radius Stability | **Spearman $\rho = 0.80$ to $0.96$** (Between 10 km and 20 km) | Confirms that 10 km represents an optimal operational FFB catchment without diluting mill attribution. |

### External Mill Count Benchmark against PalmWatch (Table 4.3 in Thesis Manuscript)

```text
+--------------------------------------------------------------------------------------------------+
| Company          This Study (UML)   PalmWatch (IDI, 2023)   Difference   Agreement Status        |
+--------------------------------------------------------------------------------------------------+
| IOI                     15                   15                 0        Exact Match (100%)      |
| Bumitama                14                   14                 0        Exact Match (100%)      |
| SIPEF                   11                   11                 0        Exact Match (100%)      |
| Wilmar                  45                   44                 1        Near Match  (±1 mill)   |
| GAR                     50                   47                 3        Near Match  (±3 mills)  |
| First Resources         16                   15                 1        Near Match  (±1 mill)   |
| Musim Mas               18                   17                 1        Near Match  (±1 mill)   |
| Astra Agro              34                   33                 1        Near Match  (±1 mill)   |
| KLK                     30                   29                 1        Near Match  (±1 mill)   |
| Genting                 15                   13                 2        Near Match  (±2 mills)  |
| SD Guthrie              42                  n/a                 -        Upstream Producer*      |
+--------------------------------------------------------------------------------------------------+
```
> **Theoretical Insight for Supervisor:** PalmWatch was created to trace consumer-facing brand supply chains (e.g., Unilever, Nestlé, PepsiCo). SD Guthrie is an upstream primary plantation grower. Its absence from PalmWatch validates our core research contribution: filling the upstream producer verification gap identified by Calamai et al. (2025). Stated claims are cross-checked against physical satellite loss, providing the missing verification step.

---

## SLIDE 7 · NASA/IBM PRITHVI-EO-2.0 FOUNDATION MODEL BENCHMARK

```text
====================================================================================================
 RESEARCH HYPOTHESIS: Can an out-of-the-box, zero-shot geospatial foundation model detect tropical 
                      deforestation without domain fine-tuning?
====================================================================================================

  [ EXPERIMENT 1: HIGH-CLEARING HOTSPOT (IOI Syarimo) ]
  - Spearman Rank Correlation:  rho = 0.597  (p < 0.0001)
  - Intersection-over-Union:    IoU = 0.55   (Precision: 0.71, Recall: 0.71)
  --> FINDING: Vision Transformer patch dissimilarity detects strong signal in severe clearing zones!

  [ EXPERIMENT 2: NETWORK-WIDE SCALE (All 290 Mills · 11 Companies) ]
  - Network Mean Correlation:   rho = 0.172  (All 11 company networks strictly positive: 0.152 to 0.216)
  - Network Mean Overlap:       IoU = 0.086  (Constrained by fixed 80th-percentile thresholding)
  --> FINDING: Proves directional transferability, but demonstrates that zero-shot models cannot 
      substitute for dedicated operational datasets (Hansen) without supervised domain fine-tuning.

  [ PIPELINE ISOLATION ]
  - The Mismatch Scoring Formula relies 100% on the verified Hansen dataset.
  - Prithvi is documented transparently in Section 4.8 and Appendix A as an exploratory AI benchmark.
====================================================================================================
```

---

## SLIDE 8 · ENGINEERING RIGOR & DATA INTEGRITY

| Problem / Obstacle Encountered | Technical Resolution Implemented & Verified | Pytest Guard / Status |
|:---|:---|:---:|
| **UML Coordinate Corruption** | Parsed composite `GPS coordinates` string directly; enforced geographic bounding box. | `test_mill_matching.py` (**Passed**) |
| **SD Guthrie Mill Undercount** | Dual-column search (`Group Name` + `Parent Company`); recovered 40 mills & 142,131 ha. | `test_sd_guthrie_count` (**Passed**) |
| **GEE Memory Ceiling** | Raised ceiling to `maxPixels = 10^10`, pinned scale to 30m, disk caching. | 290 Mills Complete (**Passed**) |
| **Production Metric Inconsistency** | Dropped inconsistent production volume metrics to protect empirical integrity. | Approved by Supervisor (**Verified**) |
| **Automated Regression Suite** | Continuous automated regression testing across all 11 companies and scoring weights. | **23 of 23 Tests Passed** |

---

## SLIDE 9 · THESIS STRUCTURE & ACADEMIC QUALITY

```text
====================================================================================================
                        MANUSCRIPT SPECIFICATIONS (100% COMPLETED IN LATEX)
====================================================================================================
 Chapter 00: Abstract & Front Matter      [ COMPLETED ]  -- Core findings, word counts, TOC
 Chapter 01: Introduction & 3 RQs        [ COMPLETED ]  -- Greenwashing problem, RQs 1-3, approach
 Chapter 02: Literature Review            [ COMPLETED ]  -- Cheap talk, ClimateBERT, Hansen, Calamai
 Chapter 03: Methodology & Equations      [ COMPLETED ]  -- Dual-track pipeline, PalmWatch validation
 Chapter 04: Results & Multi-Sensor      [ COMPLETED ]  -- 11-company rankings, RADD, Descals, Prithvi
 Chapter 05: Discussion & Policy Context  [ COMPLETED ]  -- Gradient vs binary, EUDR 2020 enforcement
 Chapter 06: Methodological Limitations   [ COMPLETED ]  -- 10 km proximity vs legal causation
 Chapter 07: Conclusion & Future Scope    [ COMPLETED ]  -- Verification gap resolved, future fine-tuning
 Chapter 08: References (APA 7th)         [ COMPLETED ]  -- Verified academic bibliography
 Chapter 09: Engineering Audit Appendix   [ COMPLETED ]  -- 108 engineering hours, code listings
----------------------------------------------------------------------------------------------------
 Total Prose Words: ~14,100 words | Total Manuscript Words: 19,565 words | Overleaf Bundle Ready
 Style Rules: 100% Clean (Zero Em Dashes · Zero AI Buzzwords · All Cross-References Balanced)
====================================================================================================
```

---

## SLIDE 10 · SUBMISSION ROADMAP & SUPERVISOR ACTION ITEMS

```text
TIMELINE TO SUBMISSION (DEADLINE: 26 SEPTEMBER 2026)

  TODAY (Meeting 5)       SEPTEMBER 12 - 16         SEPTEMBER 17 - 22          SEPTEMBER 26
┌──────────────────┐    ┌──────────────────┐      ┌──────────────────┐       ┌──────────────┐
│  Presentation &  │───>│ Professor Draft  │─────>│ Minor Revisions  │──────>│ FINAL THESIS │
│ Methodology Sign-│    │ Reading & Review │      │ & Visual Polish  │       │  SUBMISSION  │
│       Off        │    │  (Overleaf ZIP)  │      │                  │       │  ON PORTAL   │
└──────────────────┘    └──────────────────┘      └──────────────────┘       └──────────────┘
```

### Action Items for Professor Hoseini Today:
1. **Research Questions Confirmation:** Confirm alignment on the 3 formal Research Questions (RQ1, RQ2, RQ3).
2. **Prithvi Foundation Model Approval:** Approve framing of Prithvi as an exploratory zero-shot benchmark in Chapter 4 and Appendix.
3. **Manuscript Review Sign-Off:** Accept the compiled PDF package (`latex/thesis_latex.zip`) for draft review.
