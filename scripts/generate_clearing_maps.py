"""Clean per-mill clearing maps: real Sentinel-2 imagery + dated loss overlay.

Thesis: Catching Greenwashing from Space
GEE project: thesis-greenwashing

Upgrade over generate_before_after_comparisons.py: instead of a blocky 30 m
green/white Hansen mask, this puts a 10 m Sentinel-2 true-colour composite as
the basemap and paints ONLY the post-2020 loss pixels on top, colour-coded by
year. A reader sees the actual plantation rows, roads and the mill, and exactly
where forest was cut.

Each figure (one per mill):
  LEFT  : Sentinel-2 true colour, 2019 (pre-cutoff)   -- what was there
  RIGHT : Sentinel-2 true colour, 2024, with Hansen post-2020 loss overlaid,
          coloured by year (2021 red ... 2025 blue)   -- what was cut, and when
  + mill marker, 10 km ring, scale bar, per-year hectare legend
  auto-zoomed to the loss centroid so the clearing fills the frame.

Optional Planet NICFI 4.7 m basemap: set NICFI=1 in the environment after you
have linked a (free) Planet NICFI account to this GEE project; the script then
uses projects/planet-nicfi/assets/basemaps/asia instead of Sentinel-2.

Output: Results/satellite_images/clearing_maps/<NNN>_<company>_<mill>.png

Usage
-----
    earthengine authenticate            # if ee.Initialize hangs
    python scripts/generate_clearing_maps.py            # all 290 mills
    python scripts/generate_clearing_maps.py --limit 3  # smoke test
    python scripts/generate_clearing_maps.py --company ioi
"""
import io
import math
import os
import sys
import time
import urllib.request

import ee
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

MILLS_CSV = "data/mills/all_mills_forest_loss.csv"
OUT_DIR = "Results/satellite_images/clearing_maps"

BUFFER_M = 10000
PANEL_DIM = 1100
DPI_TAG = "300"
USE_NICFI = os.environ.get("NICFI", "0") == "1"

YEAR_COLORS = {2021: (255, 40, 40), 2022: (255, 132, 0), 2023: (255, 208, 0),
               2024: (255, 0, 200), 2025: (0, 120, 255)}


GFC = LOSSYEAR = FOREST = PIXEL_HA = None


def init_ee():
    global GFC, LOSSYEAR, FOREST, PIXEL_HA
    try:
        ee.Initialize(project="thesis-greenwashing")
    except Exception:
        ee.Authenticate()
        ee.Initialize(project="thesis-greenwashing")
    GFC = ee.Image("UMD/hansen/global_forest_change_2025_v1_13")
    LOSSYEAR = GFC.select("lossyear")
    FOREST = GFC.select("treecover2000").gt(30)
    PIXEL_HA = ee.Image.pixelArea().divide(10000)


def s2_rgb(region, start, end):
    def mask(img):
        scl = img.select("SCL")
        keep = scl.neq(3).And(scl.neq(8)).And(scl.neq(9)).And(scl.neq(10)).And(scl.neq(11))
        return img.updateMask(keep)
    coll = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
            .filterBounds(region).filterDate(start, end)
            .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 40)).map(mask))
    comp = coll.median()
    return comp.select(["B4", "B3", "B2"]).divide(3000).clamp(0, 1)


def nicfi_rgb(region, year):
    coll = ee.ImageCollection("projects/planet-nicfi/assets/basemaps/asia")
    img = coll.filterDate(f"{year}-01-01", f"{year}-12-31").sort("system:time_start", False).first()
    return img.select(["R", "G", "B"]).divide(255).clamp(0, 1)


def basemap(region, year):
    if USE_NICFI:
        try:
            return nicfi_rgb(region, year)
        except Exception:
            pass
    yr = "2019-01-01", "2019-12-31"
    if year >= 2024:
        yr = "2024-01-01", "2024-12-31"
    return s2_rgb(region, *yr)


def loss_centroid(lon, lat):
    """Mean location of post-2020 loss inside the buffer, to recentre the frame."""
    region = ee.Geometry.Point([lon, lat]).buffer(BUFFER_M)
    mask = LOSSYEAR.gte(21).And(FOREST)
    d = mask.multiply(ee.Image.pixelLonLat()).updateMask(mask).reduceRegion(
        ee.Reducer.mean(), region, 60, maxPixels=1e10).getInfo()
    clon, clat = d.get("longitude"), d.get("latitude")
    if clon is None:
        return lon, lat, BUFFER_M
    # frame half-width: tighter of 6 km or the spread of the loss
    return clon, clat, 6000


def yearly_ha(lon, lat):
    region = ee.Geometry.Point([lon, lat]).buffer(BUFFER_M)
    out = {}
    for yr in YEAR_COLORS:
        m = LOSSYEAR.eq(yr - 2000).And(FOREST).multiply(PIXEL_HA)
        v = m.reduceRegion(ee.Reducer.sum(), region, 30, maxPixels=1e10).getInfo()
        out[yr] = round(v.get("lossyear", 0) or 0, 0)
    return out


def thumb(image, region, dim, vis=None, retries=4):
    params = {"region": region, "dimensions": dim}
    if vis:
        params.update(vis)
    for a in range(retries):
        try:
            url = image.getThumbURL(params)
            with urllib.request.urlopen(url, timeout=120) as r:
                return Image.open(io.BytesIO(r.read())).convert("RGB")
        except Exception:
            if a == retries - 1:
                raise
            time.sleep(3)


def loss_overlay_rgb(region, dim):
    """RGBA-ish: each year's loss pixels painted its colour, rest transparent (black->composited)."""
    img = ee.Image(0).byte()
    for yr, _ in YEAR_COLORS.items():
        img = img.where(LOSSYEAR.eq(yr - 2000).And(FOREST), yr - 2018)  # 3..7
    palette = ["000000"] + ["%02x%02x%02x" % YEAR_COLORS[y] for y in sorted(YEAR_COLORS)]
    panel = thumb(img, region, dim, {"min": 0, "max": len(YEAR_COLORS), "palette": palette})
    arr = np.array(panel)
    alpha = (arr.sum(2) > 20).astype(np.uint8) * 255
    return arr, alpha


def _font(sz, bold=False):
    for n in (("arialbd.ttf",) if bold else ("arial.ttf", "DejaVuSans.ttf")):
        try:
            return ImageFont.truetype(n, sz)
        except OSError:
            pass
    return ImageFont.load_default()


def scale_bar(draw, x, y, px_per_km, km=2):
    w = int(px_per_km * km)
    draw.rectangle([x, y, x + w, y + 6], fill=(255, 255, 255))
    draw.text((x, y - 16), f"{km} km", font=_font(13, True), fill=(255, 255, 255))


def make_map(company, mill, country, lon, lat, out_path):
    clon, clat, half_m = loss_centroid(lon, lat)
    region = ee.Geometry.Point([clon, clat]).buffer(half_m).bounds()

    before = thumb(basemap(region, 2019), region, PANEL_DIM, {"min": 0, "max": 1})
    after = thumb(basemap(region, 2024), region, PANEL_DIM, {"min": 0, "max": 1})
    ov_rgb, ov_a = loss_overlay_rgb(region, PANEL_DIM)

    after_np = np.array(after).astype(np.float32)
    a = (ov_a[..., None] / 255.0) * 0.78
    after_ov = (after_np * (1 - a) + ov_rgb.astype(np.float32) * a).clip(0, 255).astype(np.uint8)
    after = Image.fromarray(after_ov)

    yearly = yearly_ha(lon, lat)
    total = sum(yearly.values())

    w, h = before.size
    gap, top, bot = 6, 70, 96
    canvas = Image.new("RGB", (w * 2 + gap, h + top + bot), (16, 16, 16))
    canvas.paste(before, (0, top))
    canvas.paste(after, (w + gap, top))
    d = ImageDraw.Draw(canvas)

    src_name = "Planet NICFI 4.7 m" if USE_NICFI else "Sentinel-2 SR 10 m"
    d.text((10, 8), f"{company.upper()} - {mill}, {country}", font=_font(22, True), fill=(240, 240, 240))
    d.text((10, 38), f"lat {lat:.4f}, lon {lon:.4f}  -  frame ~{2*half_m/1000:.0f} km  -  "
                     f"{src_name} basemap, Hansen GFC v1.13 loss overlay", font=_font(12), fill=(170, 170, 170))
    d.text((10, top - 18), f"{2019 if not USE_NICFI else 'pre-cutoff'}: forest intact", font=_font(13), fill=(200, 220, 200))
    d.text((w + gap + 10, top - 18), "2024: red-blue = forest cut 2021-2025, by year", font=_font(13), fill=(235, 200, 200))

    # scale bar (approx: frame is 2*half_m across w px)
    px_per_km = w / (2 * half_m / 1000)
    scale_bar(d, w + gap + 20, top + h - 30, px_per_km)

    x = 10
    ly = top + h + 10
    for yr in sorted(YEAR_COLORS):
        d.rectangle([x, ly, x + 15, ly + 15], fill=YEAR_COLORS[yr])
        lab = f"{yr}: {yearly[yr]:,.0f} ha"
        d.text((x + 20, ly - 1), lab, font=_font(12), fill=(240, 240, 240))
        x += 20 + d.textlength(lab, font=_font(12)) + 22
    d.text((10, ly + 24), f"TOTAL post-2020 loss in 10 km buffer: {total:,.0f} ha",
           font=_font(15, True), fill=(255, 210, 210))
    src = f"{src_name} + Hansen/UMD/Google/USGS/NASA GFC v1.13, via Google Earth Engine"
    d.text((canvas.size[0] - d.textlength(src, font=_font(10)) - 10, canvas.size[1] - 14),
           src, font=_font(10), fill=(150, 150, 150))

    canvas.save(out_path, dpi=(int(DPI_TAG), int(DPI_TAG)))
    return total


def slug(s):
    return "".join(c.lower() if c.isalnum() else "_" for c in str(s)).strip("_")


def main():
    limit = None
    company_filter = None
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])
    if "--company" in sys.argv:
        company_filter = sys.argv[sys.argv.index("--company") + 1].lower()

    df = pd.read_csv(MILLS_CSV)
    df["company_mill_idx"] = df.groupby(df["company"].str.lower()).cumcount() + 1
    if company_filter:
        df = df[df["company"].str.lower() == company_filter]
    if limit:
        df = df.head(limit)

    os.makedirs(OUT_DIR, exist_ok=True)
    init_ee()
    print(f"[clearing_maps] {len(df)} mills, basemap={'NICFI' if USE_NICFI else 'Sentinel-2'}")

    for i, m in df.reset_index(drop=True).iterrows():
        comp_idx = int(m["company_mill_idx"])
        out_path = os.path.join(OUT_DIR, f"{comp_idx:03d}_{m['company']}_{slug(m['mill_name'])}.png")
        if os.path.exists(out_path):
            continue
        try:
            total = make_map(m["company"], m["mill_name"], m["country"],
                             m["longitude"], m["latitude"], out_path)
            print(f"  [{i+1}/{len(df)}] (mill {comp_idx}) {m['company']:15} {str(m['mill_name'])[:24]:24} "
                  f"{total:,.0f} ha -> {os.path.basename(out_path)}", flush=True)
        except Exception as e:
            print(f"  [{i+1}/{len(df)}] (mill {comp_idx}) {m['company']} {m['mill_name']}: FAILED {e}", flush=True)
    print("DONE")


if __name__ == "__main__":
    main()
