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
treecover = gfc.select("treecover2000").gt(30)
lossyear = gfc.select("lossyear")

# encode: 0 = no data/no forest, 1 = forest standing,
# 2-8 = loss year 2019(19)/2020(20)/2021(21).../2025(25), clipped to 2019-2025 for legend simplicity
year_code = lossyear.subtract(18).clamp(0, 7)  # 19->1 ... 25->7
class_img = treecover.multiply(1).where(lossyear.gte(19), year_code.add(1))
# 0 = no forest, 1 = forest standing, 2..8 = lost in 2019..2025

PALETTE = [
    "f2f0e9",  # 0 no forest
    "1a7a3c",  # 1 forest standing (green)
    "fff59d",  # 2 lost 2019 (pale yellow)
    "ffd54f",  # 3 lost 2020
    "ffb300",  # 4 lost 2021
    "fb8c00",  # 5 lost 2022
    "f4511e",  # 6 lost 2023
    "e53935",  # 7 lost 2024
    "b71c1c",  # 8 lost 2025 (deep red)
]
VIS_PARAMS = {"min": 0, "max": 8, "palette": PALETTE, "dimensions": 2048}

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
        url = class_img.getThumbURL(params)
        out_path = os.path.join(OUT_DIR, f"{company}_forestloss_yearly.png")
        urllib.request.urlretrieve(url, out_path)
        print(f"{company}: saved {out_path} ({len(mills)} mills in frame)")
