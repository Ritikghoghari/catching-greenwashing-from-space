"""Compare the NLP models used in this thesis.

The five models do DIFFERENT tasks, so there is no single accuracy ranking.
This script produces every comparison that is actually valid:

  A. Published benchmark table
     Each model's reported accuracy / F1 from its own paper / model card.
     Domain = the authors' test data, NOT palm-oil claims. Citation included.
     -> Results/nlp_model_benchmarks.csv

  B. Sentiment model agreement  (FinBERT  vs  climatebert climate-sentiment)
     Same task -> directly comparable. Cohen's kappa + percent agreement +
     confusion matrix on all 403 confirmed claims. No gold labels needed.
     -> Results/nlp_sentiment_agreement.csv

  D. Model vs cheap baseline  (no gold labels needed -- agreement only)
     Each of the three "unpartnered" models gets a rule-based baseline so it
     has something to be compared against:
       - environmental-claims model   vs  keyword filter alone
       - climate-specificity model    vs  hard/soft heuristic (regex: number/date/%)
       - ESG-BERT topic model         vs  keyword topic tags (deforestation/peat/...)
     -> Results/nlp_baseline_agreement.csv

  C. Gold-set template
     ~160 sentences (confirmed claims + rejected candidates) with blank label
     columns. Fill by hand, save as Results/nlp_gold_labeled.csv, then run
     with --evaluate to get precision / recall / F1 / accuracy per model AND
     per baseline ON PALM-OIL DATA. That is the number the thesis reports.
     -> Results/nlp_gold_labeling_template.csv

Usage:
    python scripts/model_comparison.py               # builds A, B, C, D
    python scripts/model_comparison.py --evaluate     # after filling the template
"""
import glob
import os
import re
import sys
import warnings

warnings.filterwarnings("ignore")
import pandas as pd

RESULTS_DIR = "Results"
ENRICHED = "data/nlp/claims_enriched.csv"
BENCH_OUT = "Results/nlp_model_benchmarks.csv"
AGREE_OUT = "Results/nlp_sentiment_agreement.csv"
BASELINE_OUT = "Results/nlp_baseline_agreement.csv"
GOLD_TEMPLATE = "Results/nlp_gold_labeling_template.csv"
GOLD_FILLED = "Results/nlp_gold_labeled.csv"
COMPARISON_OUT = "Results/nlp_model_comparison.csv"

BATCH = 16
MAX_CHARS = 512
SEED = 42
COMPANY_NAME_MAP = {"gentingplantations": "genting"}

# ---------------------------------------------------------------- A. benchmarks
BENCHMARKS = [
    dict(model="climatebert/environmental-claims", task="environmental claim detection (binary)",
         metric="F1", value=0.90,
         test_data="Stammbach et al. 2022 environmental-claims test split",
         source="Stammbach et al. 2022, arXiv:2209.00507"),
    dict(model="climatebert/distilroberta-base-climate-specificity", task="claim specificity (specific vs non-specific)",
         metric="accuracy", value=0.87,
         test_data="ClimateBERT climate-specificity test split",
         source="Bingler et al. 2022, Finance Research Letters 47"),
    dict(model="ProsusAI/finbert", task="financial sentiment (3-class)",
         metric="accuracy", value=0.86,
         test_data="Financial PhraseBank (Malo et al. 2014)",
         source="Araci 2019, arXiv:1908.10063"),
    dict(model="climatebert/distilroberta-base-climate-sentiment", task="climate sentiment (risk/neutral/opportunity)",
         metric="accuracy", value=0.84,
         test_data="ClimateBERT climate-sentiment test split",
         source="Webersinke et al. 2022, arXiv:2110.12010"),
    dict(model="nbroad/ESG-BERT", task="ESG topic classification (26 SASB classes)",
         metric="accuracy", value=0.90,
         test_data="author's SASB-labelled sustainability-report corpus",
         source="nbroad/ESG-BERT model card"),
]


def build_benchmarks():
    df = pd.DataFrame(BENCHMARKS)
    df.to_csv(BENCH_OUT, index=False)
    print(f"[A] wrote {BENCH_OUT}")
    print(df[["model", "task", "metric", "value"]].to_string(index=False))
    print("    (authors' own test sets, not palm-oil -- see part C for domain accuracy)\n")


# ------------------------------------------------------------------ pipelines
def _clf(model_name):
    from transformers import pipeline
    p = pipeline("text-classification", model=model_name, top_k=None)
    p("smoke test claim about sustainable palm oil")
    return p


def _top(clf, texts):
    out = []
    for i in range(0, len(texts), BATCH):
        batch = [str(t)[:MAX_CHARS] for t in texts[i:i + BATCH]]
        for res in clf(batch, truncation=True):
            best = max(res, key=lambda r: r["score"])
            out.append(best["label"].lower())
        print(f"    {min(i + BATCH, len(texts))}/{len(texts)}")
    return out


def cohen_kappa(a, b):
    a, b = list(a), list(b)
    cats = sorted(set(a) | set(b))
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(c) / n) * (b.count(c) / n) for c in cats)
    return ((po - pe) / (1 - pe) if pe != 1 else 1.0), po


def kappa_word(k):
    return ("poor" if k < 0.2 else "fair" if k < 0.4 else
            "moderate" if k < 0.6 else "substantial" if k < 0.8 else "almost perfect")


# ------------------------------------------------ B. sentiment model agreement
CLIMATE_MAP = {"opportunity": "positive", "risk": "negative", "neutral": "neutral"}


def build_agreement(df):
    print("[B] running FinBERT on 403 confirmed claims ...")
    fin = _top(_clf("ProsusAI/finbert"), df["claim"].fillna("").tolist())
    clim = [CLIMATE_MAP[c] for c in df["climate_sentiment"]]
    kappa, po = cohen_kappa(fin, clim)
    conf = pd.crosstab(pd.Series(fin, name="FinBERT"),
                       pd.Series(clim, name="climate-sentiment"))
    conf.to_csv(AGREE_OUT)
    print(conf.to_string())
    print(f"    percent agreement : {po*100:.1f}%")
    print(f"    Cohen's kappa     : {kappa:.3f} ({kappa_word(kappa)})")
    print(f"    -> the two 'sentiment' models measure different things: FinBERT = generic")
    print(f"       tone, climate-sentiment = risk vs opportunity framing. Report both.\n")
    return fin


# ------------------------------------------------------ load full tagged corpus
def load_tagged_corpus():
    """All keyword-positive candidate sentences, flagged claim / rejected."""
    frames = []
    for path in sorted(glob.glob(os.path.join(RESULTS_DIR, "*_tagged.csv"))):
        stem = os.path.basename(path).replace("_tagged.csv", "")
        company = COMPANY_NAME_MAP.get(stem, stem)
        t = pd.read_csv(path)
        sp = path.replace("_tagged.csv", "_specific_claims.csv")
        confirmed = set(pd.read_csv(sp)["claim"]) if os.path.exists(sp) else set()
        t["company"] = company
        t["classifier_confirmed"] = t["claim"].isin(confirmed)
        frames.append(t)
    return pd.concat(frames, ignore_index=True)


# --------------------------------------------------- D. model vs baseline
SPEC_RE = re.compile(r"\d|\bby 20\d\d\b|per ?cent|%|\bhectares?\b|\bha\b|\bmills?\b|\btonnes?\b",
                     re.IGNORECASE)


def rule_specificity(text):
    """Baseline: a claim is 'specific' if it contains a number, date, %, or unit."""
    return "spec" if SPEC_RE.search(str(text)) else "non"


KEYWORD_TOPIC_COLS = ["deforestation", "peat", "ndpe", "traceability"]


def keyword_topic(row):
    for c in KEYWORD_TOPIC_COLS:
        if bool(row.get(c)):
            return c
    return "other"


# ESG-BERT SASB label -> coarse bucket that lines up with the keyword tags
ESG_TO_TOPIC = {
    "ecological_impacts": "deforestation",
    "ghg_emissions": "other", "air_quality": "other", "energy_management": "other",
    "water_and_wastewater_management": "other", "waste_and_hazardous_materials_management": "other",
    "supply_chain_management": "traceability",
    "human_rights_and_community_relations": "ndpe",
}

# ESG-BERT SASB label -> E / S / G, for the gold_esg_topic scheme
ESG_TO_EGS = {
    "ecological_impacts": "E", "ghg_emissions": "E", "air_quality": "E",
    "energy_management": "E", "water_and_wastewater_management": "E",
    "waste_and_hazardous_materials_management": "E", "physical_impacts_of_climate_change": "E",
    "human_rights_and_community_relations": "S", "employee_health_and_safety": "S",
    "customer_welfare": "S", "employee_engagement_inclusion_and_diversity": "S",
    "access_and_affordability": "S",
    "business_ethics": "G", "management_of_legal_and_regulatory_framework": "G",
    "systemic_risk_management": "G", "data_security": "G", "business_model_resilience": "G",
    "selling_practices_and_product_labeling": "G", "supply_chain_management": "G",
    "product_design_and_lifecycle_management": "G", "product_quality_and_safety": "G",
}
# keyword tag -> E / S / G
KEYWORD_TO_EGS = {"deforestation": "E", "peat": "E", "ndpe": "S", "traceability": "G", "other": "NONE"}


def build_baseline_agreement(enr, tagged):
    rows = []

    # 1. claim detection: environmental-claims model vs keyword filter
    print("[D] running environmental-claims model on full tagged corpus "
          f"({len(tagged)} candidates) ...")
    model_lab = _top(_clf("climatebert/environmental-claims"), tagged["claim"].fillna("").tolist())
    model_claim = pd.Series([l == "yes" for l in model_lab])
    keyword_claim = pd.Series([True] * len(tagged))   # every tagged row passed the keyword filter
    k, po = cohen_kappa(model_claim.astype(str), keyword_claim.astype(str))
    rows.append(dict(comparison="claim detection: model vs keyword-filter",
                     agreement_pct=round(po * 100, 1), kappa=round(k, 3),
                     note=f"model labels {model_claim.mean()*100:.0f}% of keyword hits 'yes' -- "
                          f"keyword filter already does most of the selection; near-constant, "
                          f"kappa uninformative, use gold set"))

    # 2. specificity: climate-specificity model vs regex rule
    # NOTE: enriched holds only CONFIRMED claims, all scored >= 0.5, so a 0.5
    # cutoff is constant. Split at the corpus median instead -> "more specific
    # than the median claim". True calibrated accuracy needs the gold set (part C).
    m = enr.copy()
    spec_thr = m["specificity_score"].median()
    model_spec = (m["specificity_score"] >= spec_thr).map({True: "spec", False: "non"})
    rule_spec = m["claim"].map(rule_specificity)
    k, po = cohen_kappa(model_spec, rule_spec)
    rows.append(dict(comparison="specificity: model(>=0.5) vs number/date/% rule",
                     agreement_pct=round(po * 100, 1), kappa=round(k, 3),
                     note=f"model 'spec' rate {model_spec.eq('spec').mean()*100:.0f}%, "
                          f"rule 'spec' rate {rule_spec.eq('spec').mean()*100:.0f}%"))

    # 2b. specificity: model vs the existing hard/soft 'strength' heuristic
    if "strength" in m.columns:
        strength_spec = m["strength"].map({"hard": "spec", "soft": "non"})
        k, po = cohen_kappa(model_spec, strength_spec)
        rows.append(dict(comparison="specificity: model vs hard/soft strength tag",
                         agreement_pct=round(po * 100, 1), kappa=round(k, 3),
                         note="hard/soft tag is the existing heuristic in the tagged pipeline"))

    # 3. ESG topic: ESG-BERT vs keyword topic tags
    esg_bucket = enr["esg_category"].str.lower().map(lambda x: ESG_TO_TOPIC.get(x, "other"))
    kw_bucket = enr.apply(keyword_topic, axis=1)
    k, po = cohen_kappa(esg_bucket, kw_bucket)
    rows.append(dict(comparison="ESG topic: ESG-BERT(bucketed) vs keyword tags",
                     agreement_pct=round(po * 100, 1), kappa=round(k, 3),
                     note="ESG-BERT 26-class mapped down to deforestation/traceability/ndpe/other"))

    out = pd.DataFrame(rows)
    out.to_csv(BASELINE_OUT, index=False)
    print(out.to_string(index=False))
    print(f"\n[D] wrote {BASELINE_OUT}")
    print("    Low kappa vs a rule does NOT mean the model is wrong -- it means the model")
    print("    captures cases the rule misses. Part C settles which is actually right.\n")


# --------------------------------------------------- C. gold labeling template
def build_gold_template(enr, tagged):
    # confirmed claims, stratified by company
    per = max(1, 110 // enr["company"].nunique())
    claim_parts = [g.sample(min(len(g), per), random_state=SEED)
                   for _, g in enr.groupby("company")]
    claims = pd.concat(claim_parts, ignore_index=True)[["company", "claim"]]
    claims["source"] = "confirmed_claim"

    # rejected candidates (keyword-positive but classifier said not a claim) -> negatives
    rej = tagged[~tagged["classifier_confirmed"]][["company", "claim"]].copy()
    rej = rej.sample(min(len(rej), 48), random_state=SEED)
    rej["source"] = "rejected_candidate"

    sample = pd.concat([claims, rej], ignore_index=True)
    sample["gold_is_claim"] = ""       # 1 = genuine environmental claim, 0 = incidental / not a claim
    sample["gold_specificity"] = ""    # high / medium / low   (leave blank if gold_is_claim=0)
    sample["gold_sentiment"] = ""      # positive / neutral / negative
    sample["gold_esg_topic"] = ""      # E / S / G / none
    sample.to_csv(GOLD_TEMPLATE, index=False)
    print(f"[C] wrote {GOLD_TEMPLATE}  "
          f"({len(claims)} claims + {len(rej)} non-claims = {len(sample)} rows to label)")
    print("    Fill gold_* columns, save as Results/nlp_gold_labeled.csv,")
    print("    then: python scripts/model_comparison.py --evaluate\n")


# ------------------------------------------------------- evaluate filled gold
def _acc_prf(pred, gold, positive):
    pred, gold = pd.Series(list(pred)), pd.Series(list(gold))
    mask = gold.notna() & (gold != "")
    pred, gold = pred[mask], gold[mask]
    acc = (pred == gold).mean()
    tp = ((pred == positive) & (gold == positive)).sum()
    fp = ((pred == positive) & (gold != positive)).sum()
    fn = ((pred != positive) & (gold == positive)).sum()
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    f = 2 * p * r / (p + r) if p + r else 0.0
    return round(acc, 3), round(p, 3), round(r, 3), round(f, 3), int(mask.sum())


def _multiclass_prf(pred, gold):
    """Compute overall accuracy and macro-averaged precision, recall, and F1."""
    pred, gold = pd.Series(list(pred)), pd.Series(list(gold))
    mask = gold.notna() & (gold != "") & pred.notna() & (pred != "")
    pred, gold = pred[mask].astype(str), gold[mask].astype(str)
    acc = (pred == gold).mean()
    classes = sorted(list(set(gold.unique()) | set(pred.unique())))
    p_list, r_list, f_list = [], [], []
    for c in classes:
        tp = ((pred == c) & (gold == c)).sum()
        fp = ((pred == c) & (gold != c)).sum()
        fn = ((pred != c) & (gold == c)).sum()
        p = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        r = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f = 2 * p * r / (p + r) if (p + r) > 0 else 0.0
        p_list.append(p)
        r_list.append(r)
        f_list.append(f)
    macro_p = sum(p_list) / len(p_list) if p_list else 0.0
    macro_r = sum(r_list) / len(r_list) if r_list else 0.0
    macro_f = sum(f_list) / len(f_list) if f_list else 0.0
    return round(acc, 3), round(macro_p, 3), round(macro_r, 3), round(macro_f, 3), int(len(pred))


def evaluate_gold():
    if not os.path.exists(GOLD_FILLED):
        sys.exit(f"missing {GOLD_FILLED} -- fill {GOLD_TEMPLATE} and rename it to that")
    g = pd.read_csv(GOLD_FILLED)
    enr = pd.read_csv(ENRICHED)
    tagged = load_tagged_corpus()

    rows = []

    # ---- claim detection: model vs keyword ----
    gi = g[g["gold_is_claim"].astype(str).isin(["0", "1", "0.0", "1.0"])].copy()
    if len(gi):
        gi["gold_is_claim"] = gi["gold_is_claim"].astype(float).astype(int).astype(str)
        merged = gi.merge(tagged[["company", "claim", "classifier_confirmed"]],
                          on=["company", "claim"], how="left")
        model_pred = merged["classifier_confirmed"].fillna(False).map({True: "1", False: "0"})
        kw_pred = pd.Series(["1"] * len(merged))   # keyword filter accepts everything it tagged
        for name, pred in [("environmental-claims model", model_pred), ("keyword filter (baseline)", kw_pred)]:
            a, p, r, f, n = _acc_prf(pred, merged["gold_is_claim"], "1")
            rows.append(dict(task="claim detection", model=name, accuracy=a,
                             precision=p, recall=r, f1=f, n=n))

    # ---- specificity: model vs rule, 3-way high/medium/low ----
    gs = g[g["gold_specificity"].astype(str).str.lower().isin(["high", "medium", "low"])].copy()
    if len(gs):
        gs["gold_specificity"] = gs["gold_specificity"].str.lower()
        m = gs.merge(enr[["company", "claim", "specificity_score"]], on=["company", "claim"], how="left")
        # tertile cutpoints from the full 403-claim corpus, not just the labeled subset,
        # so thresholds don't shift if the gold sample happens to skew high or low
        q1, q2 = enr["specificity_score"].quantile([1 / 3, 2 / 3])
        model_pred = pd.cut(m["specificity_score"], [-1, q1, q2, 2], labels=["low", "medium", "high"]).astype(str)
        rule_pred = m["claim"].map(lambda t: "high" if rule_specificity(t) == "spec" else "low")
        for name, pred in [("climate-specificity model", model_pred), ("number/date/% rule (baseline)", rule_pred)]:
            a, p, r, f, n = _multiclass_prf(pred, m["gold_specificity"])
            rows.append(dict(task="specificity", model=name, accuracy=a,
                             precision=p, recall=r, f1=f, n=n))

    # ---- sentiment: FinBERT vs climate-sentiment ----
    gse = g[g["gold_sentiment"].astype(str).str.lower().isin(["positive", "neutral", "negative"])].copy()
    if len(gse):
        gse["gold_sentiment"] = gse["gold_sentiment"].str.lower()
        m = gse.merge(enr[["company", "claim", "sentiment_score", "climate_sentiment"]],
                      on=["company", "claim"], how="left")
        fin = pd.cut(m["sentiment_score"], [-1, 0.45, 0.55, 2],
                     labels=["negative", "neutral", "positive"]).astype(str)
        clim = m["climate_sentiment"].map(CLIMATE_MAP)
        for name, pred in [("FinBERT", fin), ("climate-sentiment", clim)]:
            a, p, r, f, n = _multiclass_prf(pred, m["gold_sentiment"])
            rows.append(dict(task="sentiment", model=name, accuracy=a,
                             precision=p, recall=r, f1=f, n=n))

    # ---- ESG topic: ESG-BERT vs keyword tags, E/S/G/none ----
    gt = g[g["gold_esg_topic"].astype(str).str.upper().isin(["E", "S", "G", "NONE"])].copy()
    if len(gt):
        gt["gold_esg_topic"] = gt["gold_esg_topic"].str.upper()
        m = gt.merge(enr[["company", "claim", "esg_category"] + KEYWORD_TOPIC_COLS],
                     on=["company", "claim"], how="left")
        esg_pred = m["esg_category"].str.lower().map(lambda x: ESG_TO_EGS.get(x, "NONE"))
        kw_pred = m.apply(keyword_topic, axis=1).map(lambda x: KEYWORD_TO_EGS.get(x, "NONE"))
        for name, pred in [("ESG-BERT (E/S/G)", esg_pred), ("keyword tags (baseline)", kw_pred)]:
            a, p, r, f, n = _multiclass_prf(pred, m["gold_esg_topic"])
            rows.append(dict(task="ESG topic", model=name, accuracy=a,
                             precision=p, recall=r, f1=f, n=n))

    out = pd.DataFrame(rows)
    out.to_csv(COMPARISON_OUT, index=False)
    print(out.to_string(index=False))
    print(f"\n[evaluate] wrote {COMPARISON_OUT}")
    print("Per task, the higher-accuracy row is the method to trust for palm-oil claims.")


def main():
    if "--evaluate" in sys.argv:
        evaluate_gold()
        return
    if not os.path.exists(ENRICHED):
        sys.exit(f"missing {ENRICHED} -- run scripts/enrich_claims_models.py first")
    enr = pd.read_csv(ENRICHED)
    tagged = load_tagged_corpus()
    os.makedirs(RESULTS_DIR, exist_ok=True)
    build_benchmarks()
    build_agreement(enr)
    build_baseline_agreement(enr, tagged)
    build_gold_template(enr, tagged)


if __name__ == "__main__":
    main()
