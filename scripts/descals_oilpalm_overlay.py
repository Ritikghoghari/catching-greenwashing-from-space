"""Descals oil-palm overlay — what did the cleared land near each mill become?

Thesis: Catching Greenwashing from Space
GEE Project: thesis-greenwashing

Why
---
The 10 km buffer method (Section 3.3.2) measures forest loss NEAR a mill, not
loss CAUSED by that mill -- the central attribution limitation of this thesis.
This script narrows the gap on the "what happened" side: of the post-2020
Hansen forest loss inside each mill's 10 km buffer, how much of that cleared
land is classified as oil palm (industrial or smallholder) by an independent
land-cover product?

If most post-2020 loss near a company's mills is now oil palm, the loss is
much more plausibly connected to the palm supply chain than if it is bare
ground, regrowth, or other crops. This does not prove the mill sourced from
that land, but it removes the "the clearing was for something unrelated to
palm" counter-argument for the fraction that is palm.

Dataset
-------
Descals et al. (2021), "Detecting industrial oil palm plantations":
  GEE : ee.ImageCollection("BIOPAMA/GlobalOilPalm/v1")
  band: classification   1 = industrial closed-canopy oil palm
                         2 = smallholder oil palm
                         3 = other land covers / not oil palm
  ~10 m, pan-tropical, nominal epoch ~2019.
  Descals, A., Wich, S., Meijaard, E., Gaveau, D. L. A., Lowe, S., &
  Hansen, M. C. (2021). Earth System Science Data, 13(3), 1211-1231.

Method (per mill)
-----------------
  buffer         = mill point .buffer(10 km)
  post2020_loss  = Hansen lossyear >= 21  AND  treecover2000 > 30
  palm           = Descals classification in {1, 2}
  loss_on_palm   = post2020_loss AND palm
  pct_to_palm    = area(loss_on_palm) / area(post2020_loss) * 100

Output
------
  Results/descals_oilpalm_overlay_per_mill.csv   (290 rows)
  Results/descals_oilpalm_overlay_by_company.csv (11 rows)

Usage
-----
    earthengine authenticate     # first time only
    python scripts/descals_oilpalm_overlay.py
    python scripts/descals_oilpalm_overlay.py --limit 5   # smoke test
"""
import os
import sys
import time

import ee
import pandas as pd

GEE_PROJECT = "thesis-greenwashing"
HANSEN_IMAGE = "UMD/hansen/global_forest_change_2025_v1_13"
DESCALS_COLLECTION = "BIOPAMA/GlobalOilPalm/v1"

MILLS_CSV = "data/mills/all_mills_forest_loss.csv"
OUT_PER_MILL = "Results/descals_oilpalm_overlay_per_mill.csv"
OUT_BY_COMPANY = "Results/descals_oilpalm_overlay_by_company.csv"

BUFFER_M = 10000
TREECOVER_THRESHOLD = 30       # % canopy in 2000 to count a pixel as forest
LOSSYEAR_MIN = 21             # lossyear >= 21  ->  post-31-Dec-2020 (EUDR cutoff)
SCALE_M = 30                  # Hansen native resolution
MAX_PIXELS = 1e10
RETRIES = 3


def init_ee():
    try:
        ee.Initialize(project=GEE_PROJECT)
    except Exception:
        ee.Authenticate()
        ee.Initialize(project=GEE_PROJECT)
    # touch an asset to fail fast on auth/project problems
    ee.Image(HANSEN_IMAGE).bandNames().getInfo()


def build_images():
    hansen = ee.Image(HANSEN_IMAGE)
    forest = hansen.select("treecover2000").gt(TREECOVER_THRESHOLD)
    post2020_loss = hansen.select("lossyear").gte(LOSSYEAR_MIN).And(forest)

    descals = ee.ImageCollection(DESCALS_COLLECTION).mosaic().select("classification")
    palm = descals.eq(1).Or(descals.eq(2))          # industrial OR smallholder
    industrial = descals.eq(1)

    area_ha = ee.Image.pixelArea().divide(10000)
    stack = (area_ha.rename("px_ha")
             .addBands(area_ha.updateMask(post2020_loss).rename("loss_ha"))
             .addBands(area_ha.updateMask(post2020_loss.And(palm)).rename("loss_palm_ha"))
             .addBands(area_ha.updateMask(post2020_loss.And(industrial)).rename("loss_industrial_ha")))
    return stack


def measure_mill(stack, lat, lon):
    geom = ee.Geometry.Point([lon, lat]).buffer(BUFFER_M)
    for attempt in range(1, RETRIES + 1):
        try:
            d = stack.reduceRegion(
                reducer=ee.Reducer.sum(),
                geometry=geom,
                scale=SCALE_M,
                maxPixels=MAX_PIXELS,
                bestEffort=True,
            ).getInfo()
            return {
                "loss_post2020_ha_gee": d.get("loss_ha", 0.0) or 0.0,
                "loss_on_palm_ha": d.get("loss_palm_ha", 0.0) or 0.0,
                "loss_on_industrial_ha": d.get("loss_industrial_ha", 0.0) or 0.0,
            }
        except ee.EEException as exc:
            if attempt == RETRIES:
                raise
            wait = 2 ** attempt
            print(f"    EE error (attempt {attempt}/{RETRIES}): {exc} -- retrying in {wait}s", file=sys.stderr)
            time.sleep(wait)


def main():
    limit = None
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])

    mills = pd.read_csv(MILLS_CSV)
    if limit:
        mills = mills.head(limit)
    print(f"[descals] {len(mills)} mills, 10 km buffers, Hansen post-2020 x Descals oil palm")

    init_ee()
    stack = build_images()

    # resume support: keep previously-computed rows, skip those mills
    prev_rows = []
    done = set()
    if os.path.exists(OUT_PER_MILL) and not limit:
        try:
            prev = pd.read_csv(OUT_PER_MILL)
            prev_rows = prev.to_dict("records")
            done = set(zip(prev["company"], prev["mill_name"]))
            print(f"[descals] resuming -- {len(done)} mills already done")
        except Exception as exc:
            print(f"[descals] existing output unreadable ({exc}) -- starting fresh")

    rows = list(prev_rows)
    n_new = 0
    for i, m in mills.reset_index(drop=True).iterrows():
        key = (m["company"], m["mill_name"])
        if key in done:
            continue
        try:
            r = measure_mill(stack, m["latitude"], m["longitude"])
        except Exception as exc:
            print(f"  [{i+1}/{len(mills)}] {m['company']:15} {str(m['mill_name'])[:25]:25} FAILED: {exc}",
                  file=sys.stderr)
            r = {"loss_post2020_ha_gee": None, "loss_on_palm_ha": None, "loss_on_industrial_ha": None}

        loss = r["loss_post2020_ha_gee"] or 0.0
        pct = (r["loss_on_palm_ha"] / loss * 100) if loss else 0.0
        row = {
            "company": m["company"], "mill_name": m["mill_name"], "country": m.get("country"),
            "loss_post2020_ha_csv": m["loss_post2020_ha"],
            **r,
            "pct_loss_to_palm": round(pct, 1),
        }
        rows.append(row)
        n_new += 1
        print(f"  [{i+1}/{len(mills)}] {m['company']:15} {str(m['mill_name'])[:25]:25} "
              f"loss={loss:9.0f} ha  ->  palm {pct:5.1f}%", flush=True)

        # checkpoint every 10 new mills -- single writer, full rewrite, no re-read
        if n_new % 10 == 0:
            _flush(rows)

    _flush(rows)
    _summarise()


def _flush(rows):
    if not rows:
        return
    os.makedirs("Results", exist_ok=True)
    df = pd.DataFrame(rows).drop_duplicates(subset=["company", "mill_name"], keep="last")
    tmp = OUT_PER_MILL + ".tmp"
    df.to_csv(tmp, index=False)
    os.replace(tmp, OUT_PER_MILL)   # atomic, avoids partial-file reads


def _summarise():
    df = pd.read_csv(OUT_PER_MILL)
    g = df.groupby("company").agg(
        n_mills=("mill_name", "size"),
        loss_post2020_ha=("loss_post2020_ha_gee", "sum"),
        loss_on_palm_ha=("loss_on_palm_ha", "sum"),
        loss_on_industrial_ha=("loss_on_industrial_ha", "sum"),
    ).reset_index()
    g["pct_loss_to_palm"] = (g["loss_on_palm_ha"] / g["loss_post2020_ha"] * 100).round(1)
    g["pct_loss_to_industrial"] = (g["loss_on_industrial_ha"] / g["loss_post2020_ha"] * 100).round(1)
    g = g.sort_values("pct_loss_to_palm", ascending=False)
    g.to_csv(OUT_BY_COMPANY, index=False)

    total_loss = g["loss_post2020_ha"].sum()
    total_palm = g["loss_on_palm_ha"].sum()
    print(f"\n[descals] wrote {OUT_PER_MILL} and {OUT_BY_COMPANY}")
    print(g[["company", "n_mills", "loss_post2020_ha", "pct_loss_to_palm", "pct_loss_to_industrial"]]
          .to_string(index=False))
    print(f"\n[descals] ALL COMPANIES: {total_palm/total_loss*100:.1f}% of post-2020 loss "
          f"near mills is classified oil palm by Descals et al. (2021)")


if __name__ == "__main__":
    main()
