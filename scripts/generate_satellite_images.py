import os
import urllib.request

import ee
import pandas as pd

MILLS_DIR = "data/mills"
COMPANIES = [
    "gar", "sdguthrie", "wilmar", "klk", "astraagro", "ioi",
    "musimmas", "genting", "firstresources", "bumitama", "sipef",
]

ee.Initialize(project='thesis-greenwashing')

gfc = ee.Image("UMD/hansen/global_forest_change_2025_v1_13")
# 0 = no forest / no loss, 1 = forest still standing (green), 2-3 = lost after 2020 (red)
vis_image = (
    gfc.select("treecover2000").gt(30).multiply(1)
    .add(gfc.select("lossyear").gte(21).multiply(2))
)
VIS_PARAMS = {"min": 0, "max": 3, "palette": ["ffffff", "1a7a3c", "1a7a3c", "d1442e"], "dimensions": 2048}

OUT_DIR = "Results/satellite_images"
os.makedirs(OUT_DIR, exist_ok=True)


def company_region(mills, pad_deg=0.08):
    lon_min, lon_max = mills["longitude"].min() - pad_deg, mills["longitude"].max() + pad_deg
    lat_min, lat_max = mills["latitude"].min() - pad_deg, mills["latitude"].max() + pad_deg
    return ee.Geometry.BBox(lon_min, lat_min, lon_max, lat_max)


if __name__ == "__main__":
    for company in COMPANIES:
        mill_file = os.path.join(MILLS_DIR, f"{company}_mills.csv")
        if not os.path.exists(mill_file):
            print(f"{company}: mill file not found, skipped")
            continue
        mills = pd.read_csv(mill_file)
        if len(mills) == 0:
            print(f"{company}: no mills, skipped")
            continue
        region = company_region(mills)
        params = dict(VIS_PARAMS)
        params["region"] = region
        url = vis_image.getThumbURL(params)
        out_path = os.path.join(OUT_DIR, f"{company}_forestloss.png")
        urllib.request.urlretrieve(url, out_path)
        print(f"{company}: saved {out_path} ({len(mills)} mills in frame)")
