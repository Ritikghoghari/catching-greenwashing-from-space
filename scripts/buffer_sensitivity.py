"""
buffer_sensitivity.py
---------------------
Buffer sensitivity analysis for palm oil mill forest loss.

Thesis: "Catching Greenwashing from Space"
GEE project: thesis-greenwashing
Hansen dataset: UMD/hansen/global_forest_change_2025_v1_13

For each of 11 companies and 5 buffer radii (5, 10, 15, 20, 30 km),
computes forest loss metrics around ONE representative mill per company.

Goal: show that company RANKING is stable across buffer sizes,
validating the 10 km buffer choice used in the main pipeline.

Output: Results/buffer_sensitivity.csv
Columns: company, buffer_km, loss_post2020_ha, forest_2000_ha, loss_pct

Run: python scripts/buffer_sensitivity.py
"""

import os
import time

import ee
import pandas as pd
from scipy import stats

# ---------------------------------------------------------------------------
# Initialise Earth Engine
# ---------------------------------------------------------------------------
ee.Initialize(project="thesis-greenwashing")

# ---------------------------------------------------------------------------
# Hansen GFC image layers
# ---------------------------------------------------------------------------
GFC = ee.Image("UMD/hansen/global_forest_change_2025_v1_13")

# lossyear band: value = last 2 digits of year (e.g. 21 = 2021)
LOSSYEAR = GFC.select("lossyear")

# treecover2000 band: canopy cover percentage in year 2000
TREECOVER = GFC.select("treecover2000")

# Pixel area in hectares
PIXEL_HA = ee.Image.pixelArea().divide(10000)

# Post-2020 loss mask (lossyear >= 21 = after 31 Dec 2020, i.e. EUDR cutoff)
LOSS_POST2020 = LOSSYEAR.gte(21).multiply(PIXEL_HA)

# Forest baseline: treecover2000 > 30 % canopy cover
FOREST_2000 = TREECOVER.gt(30).multiply(PIXEL_HA)

# ---------------------------------------------------------------------------
# Representative mills — ONE per company (main mill from existing pipeline)
# ---------------------------------------------------------------------------
REPRESENTATIVE_MILLS = {
    "GAR":             {"lon": 110.5158,   "lat": -2.1404},
    "SD Guthrie":      {"lon": 118.060186, "lat":  4.704457},
    "Wilmar":          {"lon": 118.405246, "lat":  5.179162},
    "KLK":             {"lon": 103.270394, "lat":  2.204546},
    "Astra Agro":      {"lon": 121.484959, "lat": -2.129894},
    "IOI":             {"lon": 117.398389, "lat":  6.002431},
    "Musim Mas":       {"lon": 102.030838, "lat":  0.077043},
    "Genting":         {"lon": 103.209291, "lat":  1.856092},
    "First Resources": {"lon": 100.926111, "lat":  0.580556},
    "Bumitama":        {"lon": 113.060706, "lat": -1.993167},
    "SIPEF":           {"lon": 151.01097,  "lat": -5.311111},
}

# Buffer radii to test
BUFFER_RADII_KM = [5, 10, 15, 20, 30]

# ---------------------------------------------------------------------------
# Core analysis function
# ---------------------------------------------------------------------------

def compute_forest_loss(lon: float, lat: float, buffer_km: float) -> dict:
    """
    Compute forest loss metrics within a circular buffer around a point.

    Parameters
    ----------
    lon : float
        Mill longitude (WGS84)
    lat : float
        Mill latitude (WGS84)
    buffer_km : float
        Buffer radius in kilometres

    Returns
    -------
    dict with keys: loss_post2020_ha, forest_2000_ha, loss_pct
    """
    buffer_m = buffer_km * 1000
    region = ee.Geometry.Point([lon, lat]).buffer(buffer_m)

    # Sum pixels within buffer — scale=30 m, maxPixels=1e10 required
    loss_result = LOSS_POST2020.reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=region,
        scale=30,
        maxPixels=1e10,
    ).getInfo()

    forest_result = FOREST_2000.reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=region,
        scale=30,
        maxPixels=1e10,
    ).getInfo()

    loss_ha   = loss_result.get("lossyear", 0) or 0.0
    forest_ha = forest_result.get("treecover2000", 0) or 0.0

    # Avoid division by zero for mills with no recorded forest baseline
    if forest_ha > 0:
        loss_pct = (loss_ha / forest_ha) * 100
    else:
        loss_pct = 0.0

    return {
        "loss_post2020_ha": round(loss_ha, 2),
        "forest_2000_ha":   round(forest_ha, 2),
        "loss_pct":         round(loss_pct, 4),
    }


# ---------------------------------------------------------------------------
# Main analysis loop
# ---------------------------------------------------------------------------

def run_sensitivity() -> pd.DataFrame:
    """
    Iterate over all companies and all buffer sizes.
    Returns a DataFrame with one row per (company, buffer_km) combination.
    """
    records = []
    total = len(REPRESENTATIVE_MILLS) * len(BUFFER_RADII_KM)
    done = 0

    for company, coords in REPRESENTATIVE_MILLS.items():
        lon, lat = coords["lon"], coords["lat"]
        print(f"\n--- {company} (lon={lon}, lat={lat}) ---")

        for buffer_km in BUFFER_RADII_KM:
            print(f"  Buffer {buffer_km:>2} km ... ", end="", flush=True)
            t0 = time.time()

            try:
                metrics = compute_forest_loss(lon, lat, buffer_km)
                elapsed = time.time() - t0
                print(
                    f"loss={metrics['loss_post2020_ha']:>8.1f} ha  "
                    f"forest={metrics['forest_2000_ha']:>9.1f} ha  "
                    f"pct={metrics['loss_pct']:>6.2f}%  "
                    f"({elapsed:.1f}s)"
                )
            except Exception as exc:
                elapsed = time.time() - t0
                print(f"ERROR after {elapsed:.1f}s: {exc}")
                metrics = {
                    "loss_post2020_ha": None,
                    "forest_2000_ha":   None,
                    "loss_pct":         None,
                }

            records.append({
                "company":         company,
                "buffer_km":       buffer_km,
                "loss_post2020_ha": metrics["loss_post2020_ha"],
                "forest_2000_ha":   metrics["forest_2000_ha"],
                "loss_pct":         metrics["loss_pct"],
            })
            done += 1

    print(f"\nCompleted {done}/{total} cells.")
    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# Summary: ranking stability at 10 km vs 30 km
# ---------------------------------------------------------------------------

def print_ranking_summary(df: pd.DataFrame) -> None:
    """
    Compare company rankings by loss_pct at 10 km vs 30 km buffer.
    Prints ranked tables and Spearman correlation.
    """
    print("\n" + "=" * 60)
    print("RANKING STABILITY: 10 km vs 30 km buffer (by loss_pct)")
    print("=" * 60)

    def ranked(df_sub):
        """Return companies ranked by loss_pct descending (higher = worse)."""
        valid = df_sub.dropna(subset=["loss_pct"]).copy()
        valid["rank"] = valid["loss_pct"].rank(ascending=False).astype(int)
        return valid.sort_values("rank")[["rank", "company", "loss_pct"]]

    r10 = ranked(df[df["buffer_km"] == 10].copy())
    r30 = ranked(df[df["buffer_km"] == 30].copy())

    # Print side-by-side
    print(f"\n{'Rank':<5} {'Company (10 km)':<18} {'loss_pct':>8}   "
          f"{'Company (30 km)':<18} {'loss_pct':>8}")
    print("-" * 68)
    for i in range(max(len(r10), len(r30))):
        row10 = r10.iloc[i] if i < len(r10) else None
        row30 = r30.iloc[i] if i < len(r30) else None
        col10 = (f"{row10['company']:<18} {row10['loss_pct']:>8.2f}%"
                 if row10 is not None else f"{'—':<18} {'—':>8}")
        col30 = (f"{row30['company']:<18} {row30['loss_pct']:>8.2f}%"
                 if row30 is not None else f"{'—':<18} {'—':>8}")
        print(f"{i+1:<5} {col10}   {col30}")

    # Spearman correlation between rank vectors
    merged = r10[["company", "rank"]].rename(columns={"rank": "rank_10"}).merge(
        r30[["company", "rank"]].rename(columns={"rank": "rank_30"}),
        on="company",
        how="inner",
    )
    if len(merged) >= 3:
        rho, pval = stats.spearmanr(merged["rank_10"], merged["rank_30"])
        print(f"\nSpearman rho (10 km vs 30 km ranks): {rho:.4f}  "
              f"(p={pval:.4f})")
        if rho >= 0.90:
            verdict = "STABLE — 10 km buffer choice is well-validated."
        elif rho >= 0.70:
            verdict = "MODERATE — some rank shifts; interpret 10 km cautiously."
        else:
            verdict = "UNSTABLE — rankings change significantly with buffer size."
        print(f"Verdict: {verdict}")
    else:
        print("Not enough data for Spearman correlation.")

    print()

    # Also print Spearman for all adjacent pairs
    print("Spearman rho between adjacent buffer sizes (loss_pct):")
    print(f"  {'Pair':<15}  {'rho':>6}  {'p-value':>8}")
    pairs = list(zip(BUFFER_RADII_KM, BUFFER_RADII_KM[1:]))
    for b1, b2 in pairs:
        d1 = df[df["buffer_km"] == b1][["company", "loss_pct"]].rename(
            columns={"loss_pct": "p1"})
        d2 = df[df["buffer_km"] == b2][["company", "loss_pct"]].rename(
            columns={"loss_pct": "p2"})
        m = d1.merge(d2, on="company").dropna()
        if len(m) >= 3:
            rho, pval = stats.spearmanr(m["p1"], m["p2"])
            print(f"  {b1} km vs {b2} km  :  {rho:>6.4f}  {pval:>8.4f}")
        else:
            print(f"  {b1} km vs {b2} km  :  insufficient data")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Buffer Sensitivity Analysis — 'Catching Greenwashing from Space'")
    print(f"Buffers: {BUFFER_RADII_KM} km")
    print(f"Companies: {list(REPRESENTATIVE_MILLS.keys())}")
    print(f"Hansen EUDR cutoff: lossyear >= 21 (post-31 Dec 2020)")
    print()

    # Run the GEE queries
    results_df = run_sensitivity()

    # Save to CSV
    out_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "Results", "buffer_sensitivity.csv"
    )
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    results_df.to_csv(out_path, index=False)
    print(f"\nSaved: {out_path}")

    # Print the full table
    print("\nFull results table:")
    print(results_df.to_string(index=False))

    # Print ranking stability summary
    print_ranking_summary(results_df)
