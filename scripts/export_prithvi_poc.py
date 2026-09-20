"""Prithvi-EO-2.0 proof-of-concept: prep exports for one IOI mill.

Prepares everything the Colab notebook (notebooks/prithvi_poc.ipynb) needs so
Prithvi-EO-2.0 inference can run with zero friction:

  1. Picks the IOI mill with the highest post-2020 Hansen loss
     (SYARIMO, Malaysia — 12,317.76 ha, see data/mills/ioi_mills.csv), matching
     this project's existing "worst mill" selection convention
     (scripts/generate_before_after_comparisons.py::run_company_top_mills).
  2. Builds the same 10 km buffer region used everywhere else in this repo
     (BUFFER_M = 10000, matching run_forestloss_batch.py / all_companies_yearly_loss.py).
  3. Exports THREE GeoTIFFs to Google Drive (folder "thesis_prithvi_poc"),
     all clipped to the identical bounding box so every pixel lines up:
       a. sentinel2_before_2019.tif  — Sentinel-2 SR harmonized, least-cloud
          median composite, 2019 (pre-loss baseline), 6 bands matching
          Prithvi-EO-2.0's expected HLS-style channels: Blue, Green, Red,
          NIR, SWIR1, SWIR2 (S2 bands B2,B3,B4,B8,B11,B12).
       b. sentinel2_after_2024.tif   — same composite recipe, 2024 (post-loss).
       c. hansen_groundtruth.tif     — 2-band Hansen reference: treecover2000
          (>30% mask) and post-2020 loss (lossyear >= 21), for the agreement
          metric in the notebook.
  4. Writes data/mills/prithvi_poc_config.json with the mill metadata, region
     bbox, band order, and export task ids/descriptions, so the Colab notebook
     can locate the files in Drive without guessing.

This script only STARTS the EE batch export tasks (task.start()) — it does not
wait for them. Exports typically take 2-10 minutes to appear in Drive. Check
progress at https://code.earthengine.google.com/tasks or by polling
ee.data.getTaskStatus in a follow-up call.
"""
import json
import os

import ee
import pandas as pd

ee.Initialize(project="thesis-greenwashing")

MILLS_CSV = "data/mills/ioi_mills.csv"
BUFFER_M = 10000
SCALE_S2 = 10  # Sentinel-2 native resolution for the 3 visual/NIR/SWIR bands used
SCALE_HANSEN = 30
DRIVE_FOLDER = "thesis_prithvi_poc"
CONFIG_OUT = "data/mills/prithvi_poc_config.json"

# Prithvi-EO-2.0 default 6-band HLS-style order: Blue, Green, Red, NIR, SWIR1, SWIR2
S2_BANDS = ["B2", "B3", "B4", "B8", "B11", "B12"]
S2_BAND_LABELS = ["Blue", "Green", "Red", "NIR", "SWIR1", "SWIR2"]

BEFORE_RANGE = ("2019-01-01", "2019-12-31")
AFTER_RANGE = ("2023-06-01", "2024-12-31")


def pick_mill():
    mills = pd.read_csv(MILLS_CSV)
    top = mills.sort_values("loss_post2020_ha", ascending=False).iloc[0]
    return top


def s2_composite(region, date_start, date_end, cloud_pct=20):
    def mask_clouds(img):
        scl = img.select("SCL")
        # Sentinel-2 SR Harmonized Scene Classification: keep vegetation(4),
        # bare soil(5), water(6), unclassified(7) — drop cloud/shadow/snow/cirrus.
        mask = scl.eq(4).Or(scl.eq(5)).Or(scl.eq(6)).Or(scl.eq(7))
        return img.updateMask(mask)

    coll = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterDate(date_start, date_end)
        .filterBounds(region)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", cloud_pct))
        .map(mask_clouds)
        .select(S2_BANDS)
    )
    n = coll.size().getInfo()
    if n == 0:
        # relax cloud filter if nothing matches
        coll = (
            ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
            .filterDate(date_start, date_end)
            .filterBounds(region)
            .map(mask_clouds)
            .select(S2_BANDS)
        )
        n = coll.size().getInfo()
    composite = coll.median().multiply(0.0001)  # scale reflectance to 0-1
    return composite.clip(region), n


def export_image(image, description, region, scale, bands=None):
    params = dict(
        image=image,
        description=description,
        folder=DRIVE_FOLDER,
        fileNamePrefix=description,
        region=region,
        scale=scale,
        maxPixels=1e10,
        fileFormat="GeoTIFF",
    )
    task = ee.batch.Export.image.toDrive(**params)
    task.start()
    return task


if __name__ == "__main__":
    mill = pick_mill()
    print(f"Selected mill: IOI / {mill['mill_name']} ({mill['country']})")
    print(f"  lat={mill['latitude']}, lon={mill['longitude']}")
    print(f"  post-2020 Hansen loss: {mill['loss_post2020_ha']:,.1f} ha (highest of IOI's 15 mills)")

    point = ee.Geometry.Point([float(mill["longitude"]), float(mill["latitude"])])
    region = point.buffer(BUFFER_M).bounds()
    region_info = region.getInfo()

    print("\nBuilding Sentinel-2 composites (least-cloud, median)...")
    before_img, n_before = s2_composite(region, *BEFORE_RANGE)
    after_img, n_after = s2_composite(region, *AFTER_RANGE)
    print(f"  before ({BEFORE_RANGE[0]}..{BEFORE_RANGE[1]}): {n_before} S2 scenes")
    print(f"  after  ({AFTER_RANGE[0]}..{AFTER_RANGE[1]}): {n_after} S2 scenes")

    gfc = ee.Image("UMD/hansen/global_forest_change_2025_v1_13")
    forest2000 = gfc.select("treecover2000").gt(30).rename("forest2000")
    loss_post2020 = gfc.select("lossyear").gte(21).rename("loss_post2020")
    hansen_ref = forest2000.addBands(loss_post2020).clip(region)

    print(f"\nStarting Drive exports to folder '{DRIVE_FOLDER}' ...")
    tasks = {}
    tasks["sentinel2_before_2019"] = export_image(
        before_img, "sentinel2_before_2019", region, SCALE_S2
    )
    tasks["sentinel2_after_2024"] = export_image(
        after_img, "sentinel2_after_2024", region, SCALE_S2
    )
    tasks["hansen_groundtruth"] = export_image(
        hansen_ref, "hansen_groundtruth", region, SCALE_HANSEN
    )

    for name, task in tasks.items():
        print(f"  task started: {name} -> id={task.id}")

    config = {
        "company": "ioi",
        "mill_name": mill["mill_name"],
        "country": mill["country"],
        "latitude": float(mill["latitude"]),
        "longitude": float(mill["longitude"]),
        "loss_post2020_ha": float(mill["loss_post2020_ha"]),
        "buffer_m": BUFFER_M,
        "region_bbox_geojson": region_info,
        "hansen_dataset": "UMD/hansen/global_forest_change_2025_v1_13",
        "eudr_cutoff": "lossyear >= 21 (post 31 Dec 2020)",
        "s2_bands": S2_BANDS,
        "s2_band_labels": S2_BAND_LABELS,
        "before_date_range": BEFORE_RANGE,
        "after_date_range": AFTER_RANGE,
        "scale_s2_m": SCALE_S2,
        "scale_hansen_m": SCALE_HANSEN,
        "drive_folder": DRIVE_FOLDER,
        "exports": {
            "sentinel2_before_2019": {
                "filename": "sentinel2_before_2019.tif",
                "task_id": tasks["sentinel2_before_2019"].id,
                "n_scenes": n_before,
                "bands": S2_BANDS,
            },
            "sentinel2_after_2024": {
                "filename": "sentinel2_after_2024.tif",
                "task_id": tasks["sentinel2_after_2024"].id,
                "n_scenes": n_after,
                "bands": S2_BANDS,
            },
            "hansen_groundtruth": {
                "filename": "hansen_groundtruth.tif",
                "task_id": tasks["hansen_groundtruth"].id,
                "bands": ["forest2000", "loss_post2020"],
            },
        },
    }
    os.makedirs(os.path.dirname(CONFIG_OUT), exist_ok=True)
    with open(CONFIG_OUT, "w") as f:
        json.dump(config, f, indent=2)
    print(f"\nConfig written: {CONFIG_OUT}")
    print("\nExports are running server-side on Earth Engine. Check progress:")
    print("  https://code.earthengine.google.com/tasks")
    print(f"Files will land in Google Drive under a folder named '{DRIVE_FOLDER}' when done")
    print("(usually 2-10 minutes). DONE.")
