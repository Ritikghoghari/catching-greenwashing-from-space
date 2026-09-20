# Thesis Project Plan & Handoff — Catching Greenwashing from Space
### 6-week execution plan for an AI-based palm-oil deforestation greenwashing detector

> **For the agent reading this:** this document is a complete handoff. It covers the goal,
> the 4-layer pipeline, exactly what is already built and validated, the working code, and a
> week-by-week plan. Continue from Section "Current status" and follow the 6-week plan.

---

## 1. Project overview

- **Goal:** detect corporate greenwashing by comparing palm-oil companies' *stated*
  deforestation claims (from sustainability reports) against *observed* forest loss
  (satellite data), producing a 0–100 mismatch score per company.
- **Approach:** quantitative, computational, secondary data only. No human participants.
- **Scope:** palm oil (EUDR-covered commodity), global producing regions (Indonesia,
  Malaysia, Ghana, Nigeria, etc.). EUDR (Regulation (EU) 2023/1115) is the policy framing;
  the **31 Dec 2020 cutoff** matters — forest loss after 2020 is the EUDR-relevant signal.
- **Novelty vs. PalmWatch:** PalmWatch measures a brand's deforestation *footprint*. This
  project extracts each company's *own claims* via NLP and scores the *gap* between claim
  and reality. That mismatch score is the contribution.
- **Deadline:** ~1.5 months remaining (6 weeks).
- **Report length target:** 16,000–18,000 words.

---

## 2. The 4-layer pipeline

1. **Layer 1 — NLP task:** extract deforestation claims from each company's report,
   classify specificity (specific vs vague), keep deforestation-relevant claims. ✅ BUILT
2. **Layer 2 — Satellite task:**
   - **2a. Hansen forest-loss** — for each company's mills (from the Universal Mill List),
     measure hectares of forest loss, split before/after 2020. ✅ VALIDATED on 1 mill
   - **2b. Prithvi-EO-2.0 deep-learning model** — detect deforestation from Sentinel-2
     imagery as a proof-of-concept (needs GPU → Google Colab). 🔲 NOT STARTED
3. **Layer 3 — Comparison layer:** combine claim strength + forest loss + spatial-temporal
   overlap into a 0–100 mismatch score per company. 🔲 NOT STARTED
4. **Layer 4 — Website:** present the full flow (NLP → satellite → comparison → final
   decision) with real satellite image proof. 🔲 NOT STARTED (build LAST, on real data)

---

## 3. Environment

- **Language:** Python 3.10+
- **Editor:** Jupyter Notebook (via Anaconda) — moved from marimo to avoid its
  "redefine variable" restriction. Local dev on Windows (`C:\Users\<user>\thesis\`).
- **Heavy work (Prithvi):** Google Colab (free GPU) — laptop is low-powered.
- **Models (Hugging Face):**
  - `climatebert/environmental-claims` — claim detection
  - `climatebert/distilroberta-base-climate-specificity` — specificity
  - (later) `ibm-nasa-geospatial/Prithvi-EO-2.0` — geospatial foundation model
- **Satellite:** Google Earth Engine, project ID `thesis-greenwashing`.
  Asset: `UMD/hansen/global_forest_change_2025_v1_13`.
- **Key install:**
  ```bash
  pip install pdfplumber transformers torch pandas openpyxl earthengine-api geemap
  ```

---

## 4. Current status (what is already done)

| Item | Status |
|------|--------|
| NLP claim pipeline (extract → tag → specificity → filter) | ✅ Built & working |
| Wilmar processed | ✅ 27 claims extracted |
| GAR processed | ✅ 141 claims → 40 specific |
| Universal Mill List downloaded | ✅ (has Wilmar, Sime Darby, IOI, Musim Mas, etc.) |
| Earth Engine connected | ✅ project `thesis-greenwashing` |
| First forest-loss test (1 Wilmar mill, 10 km) | ✅ ~22,096 ha total loss |
| Satellite image proof (green/red map) | ✅ generated in Earth Engine |
| Companies remaining | 🔲 ~6–8 more to process |
| Automatic multi-mill forest loss | 🔲 to build (Week 2) |
| 0–100 scoring | 🔲 to build (Week 3) |
| Prithvi model | 🔲 to build (Week 4) |
| Website | 🔲 to build (Week 5) |

**Note on company names in the UML:** SD Guthrie appears as **"SIME DARBY"** (former name).
Always try former names / parent groups when a company isn't found by its current name.

---

## 5. Working code (Layer 1 — NLP, already validated)

```python
import pdfplumber, re
import pandas as pd
from transformers import pipeline

# Load models ONCE
clf      = pipeline("text-classification", model="climatebert/environmental-claims")
clf_spec = pipeline("text-classification", model="climatebert/distilroberta-base-climate-specificity")

def extract_claims(pdf_path, company_name):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += (page.extract_text() or "") + " "
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    claims = []
    for s in sentences:
        if clf(s, truncation=True, max_length=512)[0]["label"] == "yes":
            claims.append(s)
    df = pd.DataFrame({"company": company_name, "claim": claims})
    df.to_csv(f"{company_name}_claims.csv", index=False)
    return df

def tag_company_claims(claims_df, company_name):
    def tag(text):
        t = text.lower()
        return {"company": company_name, "claim": text,
                "deforestation": "deforestation" in t,
                "traceability": "traceab" in t,
                "ndpe": "ndpe" in t or "no deforestation" in t,
                "peat": "peat" in t,
                "deadline": next((y for y in ["2025","2030","2050","2013"] if y in t), None),
                "strength": "hard" if ("no deforestation" in t or "deforestation-free" in t or "zero" in t) else "soft"}
    tagged = pd.DataFrame([tag(c) for c in claims_df["claim"]])
    tagged.to_csv(f"{company_name}_tagged.csv", index=False)
    return tagged

def add_specificity(df):
    labels, scores = [], []
    for c in df["claim"]:
        r = clf_spec(c, truncation=True, max_length=512)[0]
        labels.append(r["label"]); scores.append(r["score"])
    df = df.copy(); df["specificity"] = labels; df["specificity_score"] = scores
    return df

# Run per company (2 lines):
# df = extract_claims("wilmar.pdf", "wilmar")
# spec = add_specificity(tag_company_claims(df, "wilmar"))
```

## 6. Working code (Layer 2a — Hansen forest loss, validated on 1 mill)

```python
import ee
ee.Initialize(project='thesis-greenwashing')

gfc = ee.Image("UMD/hansen/global_forest_change_2025_v1_13")
lossyear = gfc.select("lossyear")
pixel_ha = ee.Image.pixelArea().divide(10000)

def mill_forest_loss(lon, lat, buffer_m=10000):
    region = ee.Geometry.Point([lon, lat]).buffer(buffer_m)
    after_2020 = lossyear.gte(21).multiply(pixel_ha)   # lossyear 21 = 2021+
    total = lossyear.gt(0).multiply(pixel_ha)
    a = after_2020.reduceRegion(ee.Reducer.sum(), region, 30, maxPixels=1e10).getInfo()
    t = total.reduceRegion(ee.Reducer.sum(), region, 30, maxPixels=1e10).getInfo()
    return t.get("lossyear", 0), a.get("lossyear", 0)   # (total_ha, after2020_ha)
```

**To build in Week 2:** loop `mill_forest_loss` over all of a company's mills (from the UML)
and sum → one total per company.

---

## 7. The 6-week plan

### Week 1 — Layer 1: all companies' claims
- Download 6–8 more reports (SD Guthrie, Musim Mas, IOI, KLK, First Resources, Bumitama).
  Use SPOTT (spott.org/palm-oil/) as the stable source for each report link.
- Run each through the NLP pipeline (2 lines per company).
- Save all claims together.
- **End of week:** 8–10 companies' structured claims ready.

### Week 2 — Layer 2a: all companies' forest loss
- Build an automatic script: for each company, pull its mills from the UML (match by
  Group/Parent name, including former names like "SIME DARBY"), run `mill_forest_loss`
  on every mill, sum to a company total (split before/after 2020).
- Run for all companies.
- **End of week:** each company's forest-loss number ready (one master CSV).

### Week 3 — Layer 3: comparison + score
- Combine claim strength (Layer 1) + forest loss after 2020 (Layer 2a) + overlap into a
  0–100 mismatch score.
- Save all companies' scores in one master table.
- Save satellite images (Earth Engine green/red + Google Earth Pro before/after per key mill).
- **End of week:** one master CSV with each company's full result + images folder.

### Week 4 — Layer 2b: Prithvi model (Colab)
- On Google Colab (free GPU), run/fine-tune Prithvi-EO-2.0 on Sentinel-2 for one or two 
  regions to detect deforestation.
- Compare to Hansen as ground truth → accuracy metrics (proof-of-concept).
- **End of week:** model-chapter data ready.
- *Hardest week. If it slips, keep it a small demo — Hansen is the real evidence layer.*

### Week 5 — Website + start writing
- With real data ready, build the website: NLP → satellite → comparison → decision, with
  real image proof. (Build only after data exists — it displays data, it doesn't compute it.)
- In parallel, start writing the Methodology and Results chapters.
- **End of week:** website ready + 2 chapters drafted.

### Week 6 — Finish writing + revision
- Write remaining chapters (Introduction, Literature Review, Conclusion).
- Integrate, revise, fix references, proofread.
- Show professor, get feedback.
- **End of week:** full thesis draft ready.

---

## 8. Rules & constraints (important for the agent)

- **No fabricated data.** The website/dashboard must display only real computed results.
  Placeholder numbers are not acceptable in the thesis.
- **Build the website LAST**, on real data. It presents pre-computed results; it does not
  compute live.
- **Prithvi runs on Colab (GPU), not the local laptop.** Laptop is low-powered.
- **Run heavy models once, then work from saved CSVs** — don't re-process PDFs repeatedly.
- **EUDR 2020 cutoff:** always split forest loss into before-2020 and after-2020;
  after-2020 is the EUDR-relevant figure that drives the score.
- **Known limitations to document:** attribution (loss near a mill isn't proven to be that
  company's fault), noisy PDF extraction, keyword tagging is a simple baseline.

---

## 9. Two milestones to show the professor

- **After Week 2:** claims + forest loss for all companies (data complete).
- **After Week 4:** scores + Prithvi proof-of-concept (analysis complete).

---

## 10. Immediate next action

Week 1 is in progress. Next concrete step: process **SD Guthrie** (in the UML as
"SIME DARBY"). Download its Sustainability Report 2024, save as `sdguthrie.pdf`, run:
```python
df = extract_claims("sdguthrie.pdf", "sdguthrie")
spec = add_specificity(tag_company_claims(df, "sdguthrie"))
```
Then repeat for the remaining companies.
