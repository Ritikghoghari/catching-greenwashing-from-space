import pandas as pd
import ee

ee.Initialize(project='thesis-greenwashing')

LAT, LON = 5.179162, 118.405246
BUFFER_M = 10000

gfc = ee.Image("UMD/hansen/global_forest_change_2025_v1_13")
lossyear = gfc.select("lossyear")
pixel_ha = ee.Image.pixelArea().divide(10000)
region = ee.Geometry.Point([LON, LAT]).buffer(BUFFER_M)

results = []
for yr in range(2021, 2026):
    code = yr - 2000
    mask = lossyear.eq(code).multiply(pixel_ha)
    val = mask.reduceRegion(ee.Reducer.sum(), region, 30, maxPixels=1e10).getInfo()
    ha = val.get("lossyear", 0) or 0
    results.append({"year": yr, "loss_ha": round(ha, 2)})
    print(f"{yr}: {ha:.2f} ha")

out = pd.DataFrame(results)
out.to_csv("Results/wilmar_sabahmas_yearly_loss.csv", index=False)
print(out)
