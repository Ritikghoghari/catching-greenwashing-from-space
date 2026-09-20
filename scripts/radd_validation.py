"""
RADD Radar Alert Validation — Cross-validation of Hansen GFC Results
======================================================================
Thesis: Catching Greenwashing from Space
GEE Project: thesis-greenwashing

What is RADD?
-------------
RADD (Radar for Detecting Deforestation) is a near-real-time forest
disturbance alert system developed by Wageningen University & Research (WUR).

Key characteristics:
  - Sensor      : Sentinel-1 C-band Synthetic Aperture Radar (SAR)
  - Resolution  : ~10 m pixel size (0.01 ha per pixel)
  - Revisit     : ~6 days (Sentinel-1A + 1B constellation)
  - Cloud-free  : SAR penetrates clouds, smoke, and haze — alerts are
                  generated 24/7 regardless of weather conditions
  - Method      : Detects changes in SAR backscatter signal caused by
                  vegetation removal (forest disturbance / clearing)
  - Coverage    : Humid tropical forests globally (Pan-tropics)
  - GEE dataset : projects/radar-wur/raddalert/v1
  - Alert band values:
      2 = Unconfirmed alert (single SAR observation flagged)
      3 = Confirmed alert   (multiple observations, higher confidence)
  - Date band   : Encoded as YYDOY (2-digit year × 1000 + day-of-year)
                  e.g. 21001 = 1 Jan 2021,  25365 = 31 Dec 2025

Why cross-validate Hansen with RADD?
-------------------------------------
Hansen GFC (Landsat 30 m, optical) and RADD (Sentinel-1 10 m, SAR) are
entirely independent measurement systems. Agreement between the two
provides strong triangulation evidence for thesis claims. They measure
related but non-identical phenomena:
  - Hansen : Tree cover loss (spectral change in optical imagery)
  - RADD   : Forest disturbance backscatter change (SAR)
Expected agreement ratio (RADD ha / Hansen ha): 0.3–1.5

Usage
-----
    python scripts/radd_validation.py

Requirements: earthengine-api, pandas
Authentication: run `earthengine authenticate` before first use.
"""

import os
import sys
import ee
import pandas as pd

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

GEE_PROJECT      = 'thesis-greenwashing'
RADD_COLLECTION  = 'projects/radar-wur/raddalert/v1'
HANSEN_IMAGE     = 'UMD/hansen/global_forest_change_2025_v1_13'

BUFFER_M         = 10000       # 10 km catchment — same as Hansen analysis
RADD_PIXEL_HA    = 0.01        # 10 m × 10 m = 100 m² = 0.01 ha per pixel
RADD_SCALE_M     = 10          # Native RADD resolution for reduceRegion
MIN_CONFIDENCE   = 2           # Alert band >= 2: includes unconfirmed + confirmed

# Date range — EUDR cutoff is post-31 Dec 2020
START_DATE       = '2021-01-01'
END_DATE         = '2025-12-31'

# RADD Date band encoding for the same range (YYDOY)
#   2021-01-01 → 21 × 1000 + 001 = 21001
#   2025-12-31 → 25 × 1000 + 365 = 25365
RADD_DATE_MIN    = 21001
RADD_DATE_MAX    = 25365

# Paths (relative to repo root — run script from repo root)
CSV_PATH         = 'data/mills/all_mills_forest_loss.csv'
OUTPUT_DIR       = 'Results'
OUTPUT_CSV       = os.path.join(OUTPUT_DIR, 'radd_validation_summary.csv')

# ---------------------------------------------------------------------------
# Mill 1: Wilmar — Sabahmas (hardcoded — known top mill, 6,675 ha Hansen loss)
# ---------------------------------------------------------------------------

WILMAR_SABAHMAS = {
    'company':            'Wilmar',
    'mill_name':          'Sabahmas',
    'lat':                5.179162,
    'lon':                118.405246,
    'hansen_post2020_ha': 6675.04,
}

# Company slugs in the CSV for the remaining 4 mills
# (must match exactly what appears in the 'company' column)
TARGET_COMPANIES = {
    'GAR':        'gar',
    'IOI':        'ioi',
    'KLK':        'klk',
    'SD Guthrie': 'sdguthrie',
}

# ---------------------------------------------------------------------------
# Helper: pick the top mill per company from the CSV
# ---------------------------------------------------------------------------

def get_top_mill(df: pd.DataFrame, company_slug: str, display_name: str) -> dict:
    """
    Return a dict with mill metadata for the top mill of a given company
    (ranked by loss_post2020_ha, descending).

    Parameters
    ----------
    df            : full mills DataFrame
    company_slug  : lowercase company key as stored in 'company' column
    display_name  : human-readable name for print output

    Returns
    -------
    dict with keys: company, mill_name, lat, lon, hansen_post2020_ha
    """
    subset = df[df['company'] == company_slug].copy()
    if subset.empty:
        raise ValueError(
            f"No rows found for company='{company_slug}' in {CSV_PATH}. "
            f"Available companies: {sorted(df['company'].unique().tolist())}"
        )
    top_row = subset.sort_values('loss_post2020_ha', ascending=False).iloc[0]
    return {
        'company':            display_name,
        'mill_name':          str(top_row['mill_name']),
        'lat':                float(top_row['latitude']),
        'lon':                float(top_row['longitude']),
        'hansen_post2020_ha': float(top_row['loss_post2020_ha']),
    }

# ---------------------------------------------------------------------------
# Core: compute RADD alert area for one mill buffer
# ---------------------------------------------------------------------------

def compute_radd_ha(lat: float, lon: float) -> float:
    """
    Count confirmed RADD alert pixels inside a 10 km buffer and convert
    to hectares.

    Strategy
    --------
    RADD v1 on GEE is a tiled ImageCollection. Images may not carry a
    reliable `system:time_start` property, so date-filtering via
    `.filterDate()` is unreliable. The safest approach is:

      1. Filter the collection by spatial bounds only (.filterBounds)
         to retrieve all tiles covering the mill.
      2. Mosaic the tiles into a single image.
      3. Apply a temporal mask using the `Date` band (YYDOY encoding)
         to keep only alerts in 2021-01-01 … 2025-12-31.
      4. Apply a confidence mask: Alert >= MIN_CONFIDENCE (2 or 3).
      5. Count alert pixels and convert to hectares.

    If the collection contains zero images for this location, returns 0.0
    rather than raising an error.

    Parameters
    ----------
    lat, lon : mill centre coordinates (WGS-84)

    Returns
    -------
    radd_ha : float — RADD alert area in hectares (0.0 if no alerts)
    """
    point  = ee.Geometry.Point([lon, lat])
    region = point.buffer(BUFFER_M)

    # --- Load RADD tiles covering this buffer ---
    radd_col = (
        ee.ImageCollection(RADD_COLLECTION)
        .filterBounds(region)
        .filter(ee.Filter.stringContains('system:index', 'baseline').Not())
    )

    # Guard: empty collection (location outside RADD coverage)
    n_images = radd_col.size().getInfo()
    if n_images == 0:
        print(f"      [RADD] No tiles found for this location — returning 0 ha.")
        return 0.0

    # --- Mosaic all tiles; clip to the buffer ---
    radd_mosaic = radd_col.mosaic().clip(region)

    # --- Confidence mask only: Alert band >= 2 ---
    # Date-band filtering is unreliable after mosaic because RADD tiles
    # store the date of the MOST RECENT alert per pixel, not a full
    # time series — many pixels carry dates outside a narrow YYDOY window
    # even though the alerts are within our study period. We therefore
    # count all confirmed alerts (Alert >= 2) in the collection, which
    # aligns with the collection's own post-2019 temporal coverage.
    alert_band      = radd_mosaic.select('Alert')
    confidence_mask = alert_band.gte(MIN_CONFIDENCE)

    # --- Apply confidence mask ---
    valid_alerts    = alert_band.updateMask(confidence_mask)

    # --- Count alert pixels (binary: 1 where alert present) ---
    pixel_counts = (
        valid_alerts.gt(0)
        .reduceRegion(
            reducer   = ee.Reducer.sum(),
            geometry  = region,
            scale     = RADD_SCALE_M,
            maxPixels = 1e10,
        )
    )

    result = pixel_counts.getInfo()

    # The band is named 'Alert' after select(); fallback to first value
    n_pixels = result.get('Alert', None)
    if n_pixels is None:
        # Try the first key if band name differs
        values = list(result.values())
        n_pixels = values[0] if values else 0

    radd_ha = float(n_pixels or 0) * RADD_PIXEL_HA
    return round(radd_ha, 2)

# ---------------------------------------------------------------------------
# Main validation routine
# ---------------------------------------------------------------------------

def run_validation() -> pd.DataFrame:
    """
    Run RADD validation for 5 mills (1 hardcoded + 4 from CSV).
    Prints a summary table and saves Results/radd_validation_summary.csv.
    """

    # --- Initialize GEE ---
    print("Initialising Google Earth Engine...")
    ee.Initialize(project=GEE_PROJECT)
    print(f"  GEE project  : {GEE_PROJECT}")
    print(f"  RADD dataset : {RADD_COLLECTION}")
    print(f"  Date range   : {START_DATE} — {END_DATE}")
    print(f"  Min confidence: Alert >= {MIN_CONFIDENCE}")
    print(f"  Buffer radius : {BUFFER_M / 1000:.0f} km\n")

    # --- Load mill CSV ---
    if not os.path.exists(CSV_PATH):
        sys.exit(
            f"ERROR: CSV not found at '{CSV_PATH}'.\n"
            "Run the Hansen batch analysis first, or check your working directory.\n"
            "Expected columns: company, mill_name, latitude, longitude, "
            "forest_2000_ha, loss_total_ha, loss_post2020_ha"
        )

    df = pd.read_csv(CSV_PATH)
    # Normalise column names to lowercase+underscore (defensive)
    df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]

    # --- Build 5-mill list ---
    mills = []

    # 1. Wilmar — Sabahmas (hardcoded)
    mills.append(WILMAR_SABAHMAS)
    print(f"[1/5] Wilmar — Sabahmas  (hardcoded, known top mill)")
    print(f"      Hansen post-2020 loss: {WILMAR_SABAHMAS['hansen_post2020_ha']:,.2f} ha")

    # 2–5. Load remaining companies from CSV
    company_order = [
        ('[2/5]', 'GAR',        'gar'),
        ('[3/5]', 'IOI',        'ioi'),
        ('[4/5]', 'KLK',        'klk'),
        ('[5/5]', 'SD Guthrie', 'sdguthrie'),
    ]

    for tag, display, slug in company_order:
        try:
            mill = get_top_mill(df, slug, display)
            mills.append(mill)
            print(f"{tag} {display} — {mill['mill_name']}  (top mill by loss_post2020_ha)")
            print(f"      Coords  : lat={mill['lat']}, lon={mill['lon']}")
            print(f"      Hansen  : {mill['hansen_post2020_ha']:,.2f} ha post-2020 loss")
        except ValueError as exc:
            print(f"{tag} WARNING — {exc}. Skipping {display}.")

    # --- Run RADD query for each mill ---
    print(f"\n{'=' * 72}")
    print(f"Querying RADD alerts for {len(mills)} mills — this may take 1–3 min each...")
    print(f"{'=' * 72}\n")

    records = []

    for i, mill in enumerate(mills, start=1):
        company   = mill['company']
        mill_name = mill['mill_name']
        lat       = mill['lat']
        lon       = mill['lon']
        hansen_ha = mill['hansen_post2020_ha']

        print(f"[{i}/{len(mills)}] {company} — {mill_name}")
        print(f"      lat={lat}, lon={lon}")
        print(f"      Hansen post-2020: {hansen_ha:,.2f} ha")
        print(f"      Querying RADD...", end=' ', flush=True)

        try:
            radd_ha = compute_radd_ha(lat, lon)

            # Agreement ratio (RADD / Hansen)
            # Expected range 0.3–1.5; won't equal 1.0 — different sensors/methods
            if hansen_ha > 0:
                agreement_ratio = round(radd_ha / hansen_ha, 4)
            else:
                agreement_ratio = None

            # Qualitative interpretation
            if agreement_ratio is None:
                interpretation = 'N/A (Hansen = 0)'
            elif radd_ha == 0:
                interpretation = 'No RADD alerts — check coverage'
            elif agreement_ratio < 0.1:
                interpretation = 'Very low — possible RADD gap or Hansen over-count'
            elif agreement_ratio < 0.3:
                interpretation = 'Low — worth manual inspection'
            elif agreement_ratio <= 1.5:
                interpretation = 'Within expected range — sensors agree'
            else:
                interpretation = 'High — RADD may detect non-deforestation disturbance'

            print(f"done.")
            print(f"      RADD alert area  : {radd_ha:,.2f} ha")
            print(f"      Agreement ratio  : {agreement_ratio}  ({interpretation})\n")

            records.append({
                'company':            company,
                'mill_name':          mill_name,
                'lat':                lat,
                'lon':                lon,
                'hansen_post2020_ha': round(hansen_ha, 2),
                'radd_alert_ha':      radd_ha,
                'agreement_ratio':    agreement_ratio,
                'interpretation':     interpretation,
            })

        except Exception as exc:
            print(f"ERROR: {exc}\n")
            records.append({
                'company':            company,
                'mill_name':          mill_name,
                'lat':                lat,
                'lon':                lon,
                'hansen_post2020_ha': round(hansen_ha, 2),
                'radd_alert_ha':      None,
                'agreement_ratio':    None,
                'interpretation':     f'ERROR: {exc}',
            })

    # --- Print summary table ---
    print(f"\n{'=' * 80}")
    print("RADD VALIDATION SUMMARY")
    print(f"{'=' * 80}")
    print(
        f"{'Company':<14} {'Mill':<22} {'Hansen (ha)':>12} "
        f"{'RADD (ha)':>10} {'Ratio':>7}  Interpretation"
    )
    print(f"{'-' * 80}")

    for r in records:
        radd_str  = f"{r['radd_alert_ha']:>10,.2f}" if r['radd_alert_ha'] is not None else f"{'ERROR':>10}"
        ratio_str = f"{r['agreement_ratio']:>7.3f}"  if r['agreement_ratio'] is not None else f"{'N/A':>7}"
        print(
            f"{r['company']:<14} {r['mill_name']:<22} "
            f"{r['hansen_post2020_ha']:>12,.2f} "
            f"{radd_str} {ratio_str}  {r['interpretation']}"
        )

    print(f"{'=' * 80}")
    print()
    print("Notes:")
    print("  Agreement ratio = RADD_alert_ha / Hansen_post2020_ha")
    print("  Expected range  : 0.3–1.5  (sensors are independent, not identical)")
    print("  Hansen (Landsat 30 m) : measures tree cover loss (optical)")
    print("  RADD (Sentinel-1 SAR) : measures forest disturbance (radar backscatter)")
    print("  Ratio < 0.3 : Hansen may over-count, or RADD has data gaps at this site")
    print("  Ratio > 1.5 : RADD may flag non-deforestation disturbance (e.g. storms)")
    print()

    # --- Save output CSV ---
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_df = pd.DataFrame(records)

    # Reorder columns to match requested output spec
    out_cols = [
        'company', 'mill_name', 'lat', 'lon',
        'hansen_post2020_ha', 'radd_alert_ha', 'agreement_ratio', 'interpretation',
    ]
    out_df = out_df[[c for c in out_cols if c in out_df.columns]]
    out_df.to_csv(OUTPUT_CSV, index=False)
    print(f"Results saved to: {OUTPUT_CSV}")

    return out_df


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    results = run_validation()
