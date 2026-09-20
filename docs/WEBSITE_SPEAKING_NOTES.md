# Website Speaking Notes — Catching Greenwashing from Space
**Student:** Ritik Ghoghari | **Supervisor:** Prof. Mohamad Hoseini | **GISMA Berlin, 2026**

---

## How to Use This Script
Open `website/index.html` in Chrome **before** the meeting. Scroll through each section as you speak.

---

## Section 1 — Hero (Top of Page)

> *"Professor, this is the interactive showcase website for my thesis. At the top you can see the title — Catching Greenwashing from Space — and a quick summary of what the research does: we audit 11 palm oil companies across 290 mills, and compare what they promise in their sustainability reports against what satellites actually show on the ground. The result is a score from 0 to 100. The higher the score, the bigger the gap between their promises and reality."*

---

## Section 2 — Scoreboard

> *"This table shows the full ranking of all 11 companies. KLK is ranked number 1 with a score of 65.6 — not because they cut the most trees, but because they made the most specific public promises while satellites still recorded heavy clearing near their mills. Astra Agro is ranked last at 17.6 — they have real forest loss, but they made almost no public promises, so there is less of a contradiction to measure."*

---

## Section 3 — 290-Mill Interactive Map

> *"This is an interactive map showing all 290 palm oil mills we studied, spread across Indonesia, Malaysia, and Papua New Guinea. You can click on any mill to see its name, which company owns it, and how much forest was lost around it since 2020. This makes it easy to see that the problem is not in one place — it is spread across the entire region."*

---

## Section 4 — Satellite Gallery

> *"These are before-and-after satellite images for each mill, captured at 10-metre resolution using Sentinel-2. The left side shows 2019 — before the EU cutoff date. The right side shows 2024 with red pixels marking exactly where trees disappeared. For example, IOI's Syarimo mill lost 12,318 hectares — you can clearly see the red clearing spreading across the catchment area."*

---

## Section 5 — NLP Claims

> *"This section shows the actual sentences we extracted from company sustainability reports using AI. You can see the company name, the exact promise they made, and two scores — how specific the promise is, and how confident the tone sounds. GAR, for example, claims 99.8% traceability to plantation. Our satellite data shows 171,000 hectares of forest loss near their mills. That gap between the promise and the satellite observation is exactly what this thesis measures."*

---

## Section 6 — Weight Simulator

> *"This is an interactive tool where you can change the formula weights yourself — for example, give more importance to forest loss and less to claim tone — and watch the company ranking update in real time. This shows that our ranking is not sensitive to one specific weight choice. The top companies stay near the top regardless of how you adjust the weights."*

---

## Section 7 — Model Stack & Methodology

> *"The last two sections list all 9 machine learning models we used — 5 on the text side reading company reports, and 4 on the satellite side checking the ground. The methodology section explains every step transparently so the research is fully reproducible."*

---

## Closing Line

> *"The website brings together every part of the thesis in one place — the claims, the satellites, the scores, and the maps — so the results can be explored interactively rather than just read as numbers in a table. I can hand you the link or the local file to explore after our meeting."*

---

## Key Numbers to Remember

| Fact | Number |
|:---|:---|
| Companies audited | 11 |
| Mills studied | 290 |
| Total forest loss since 2020 | 890,168 ha |
| Highest mismatch score | KLK — 65.6 |
| Lowest mismatch score | Astra Agro — 17.6 |
| Oil palm land cover confirmed | 56% of cleared land |
| ML models used | 9 total (5 NLP + 4 satellite) |
| Prithvi AI correlation | ρ = 0.805 |
