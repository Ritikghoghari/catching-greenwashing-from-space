"""Per-year (2021-2025) post-2020 forest loss for all 11 palm oil companies' mills.

Generalizes ioi_yearly_loss.py / sabahmas_yearly_loss.py to loop over every
company mill list in data/mills/*_mills.csv (already has resolved lat/lon and
an aggregate loss_post2020_ha per mill from run_forestloss_batch.py).

Methodology (unchanged from the IOI pilot):
  - Hansen Global Forest Change v1.13 (UMD/hansen/global_forest_change_2025_v1_13)
  - 10 km buffer around each mill's point coordinates
  - scale=30, maxPixels=1e10
  - lossyear band, one mask per year via .eq(year - 2000)
  - years 2021-2025 (2025 is a partial year in the Hansen product)

Outputs:
  - Results/all_companies_yearly_loss_summary.csv   (company x year matrix, ha)
  - Results/all_companies_yearly_loss_per_mill.csv   (company, mill_name, year, loss_ha)

Sanity check: for each company, sum(2021..2025) is compared against
loss_post2020_ha in data/mills/master_forest_loss.csv (tolerance 1 ha, to
absorb rounding in the per-mill vs per-year reduceRegion calls).
"""
import pandas as pd
import ee

ee.Initialize(project='thesis-greenwashing')

MILLS_DIR = "data/mills"
COMPANIES = [
    "gar", "sdguthrie", "wilmar", "klk", "astraagro", "ioi",
    "musimmas", "genting", "firstresources", "bumitama", "sipef",
]
YEARS = range(2021, 2026)
BUFFER_M = 10000
SCALE = 30

gfc = ee.Image("UMD/hansen/global_forest_change_2025_v1_13")
lossyear = gfc.select("lossyear")
pixel_ha = ee.Image.pixelArea().divide(10000)


def mill_yearly_loss(lon, lat, buffer_m=BUFFER_M):
    """Return dict {year: hectares} for one mill's buffer."""
    region = ee.Geometry.Point([lon, lat]).buffer(buffer_m)
    out = {}
    for yr in YEARS:
        code = yr - 2000
        mask = lossyear.eq(code).multiply(pixel_ha)
        val = mask.reduceRegion(ee.Reducer.sum(), region, SCALE, maxPixels=1e10).getInfo()
        out[yr] = val.get("lossyear", 0) or 0
    return out


if __name__ == "__main__":
    per_mill_rows = []
    summary_rows = []

    for company in COMPANIES:
        mills = pd.read_csv(f"{MILLS_DIR}/{company}_mills.csv")
        print(f"=== {company}: {len(mills)} mills ===")
        year_totals = {yr: 0.0 for yr in YEARS}

        for _, row in mills.iterrows():
            yearly = mill_yearly_loss(row["longitude"], row["latitude"])
            for yr, ha in yearly.items():
                per_mill_rows.append({
                    "company": company,
                    "mill_name": row["mill_name"],
                    "year": yr,
                    "loss_ha": round(ha, 4),
                })
                year_totals[yr] += ha

        row_summary = {"company": company}
        row_summary.update({str(yr): round(year_totals[yr], 2) for yr in YEARS})
        row_summary["sum_2021_2025"] = round(sum(year_totals.values()), 2)
        summary_rows.append(row_summary)
        print(f"{company}: " + ", ".join(f"{yr}={year_totals[yr]:.1f}" for yr in YEARS)
              + f", sum={sum(year_totals.values()):.1f}")

    per_mill_df = pd.DataFrame(per_mill_rows)
    summary_df = pd.DataFrame(summary_rows)

    per_mill_df.to_csv("Results/all_companies_yearly_loss_per_mill.csv", index=False)
    summary_df.to_csv("Results/all_companies_yearly_loss_summary.csv", index=False)

    # Sanity check against master_forest_loss.csv
    master = pd.read_csv(f"{MILLS_DIR}/master_forest_loss.csv")
    check = summary_df.merge(master[["company", "loss_post2020_ha"]], on="company", how="left")
    check["diff_ha"] = (check["sum_2021_2025"] - check["loss_post2020_ha"]).round(2)
    check["match"] = check["diff_ha"].abs() < 1.0

    print("\n=== Sanity check vs master_forest_loss.csv ===")
    print(check[["company", "sum_2021_2025", "loss_post2020_ha", "diff_ha", "match"]]
          .to_string(index=False))

    failed = check[~check["match"]]
    if len(failed):
        print(f"\nFAILED sanity check: {list(failed['company'])}")
    else:
        print("\nAll 11 companies matched master_forest_loss.csv within 1 ha.")

    print("\nSaved:")
    print(" - Results/all_companies_yearly_loss_summary.csv")
    print(" - Results/all_companies_yearly_loss_per_mill.csv")
