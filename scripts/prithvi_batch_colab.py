"""Prithvi-EO-2.0 batch change-detection across all 290 mills -- COLAB / GPU ONLY.

This does NOT run on the thesis laptop: terratorch is not installed, torch is
CPU-only, and 290 mills of foundation-model inference on CPU is impractical.
Run it on Google Colab (free T4 GPU is enough) or any CUDA machine.

What it produces
----------------
Results/prithvi_batch_290.csv -- one row per mill:
    company, mill_name, lat, lon,
    spearman_rho, spearman_p,      # Prithvi change score vs Hansen post-2020 loss fraction
    precision, recall, iou,        # Prithvi change mask vs Hansen loss mask (thresholded)
    n_tiles
plus a company-level summary printed at the end.

This scales the single-mill POC (Results/prithvi_poc_readme.md, SYARIMO,
Spearman 0.597) to the full network, so the thesis can report whether a frozen
geospatial foundation model's change signal generalises beyond one site.

--------------------------------------------------------------------------------
COLAB SETUP (first cell)
--------------------------------------------------------------------------------
    !pip install -q terratorch earthengine-api rasterio scikit-learn
    import ee
    ee.Authenticate()                       # fresh browser auth, Colab handles it
    ee.Initialize(project="thesis-greenwashing")

Then upload data/mills/all_mills_forest_loss.csv to the Colab session (or read
it from Drive) and run the cells below.
--------------------------------------------------------------------------------
"""
import io
import time

import numpy as np
import pandas as pd
import requests
from scipy import stats
from sklearn.metrics import precision_score, recall_score, jaccard_score

import ee

MILLS_CSV = "all_mills_forest_loss.csv"
OUT_CSV = "prithvi_batch_290.csv"

BUFFER_M = 10000
TILE_PX = 224                 # Prithvi-EO-2.0 native patch grid
SCALE_M = 30
BEFORE = ("2019-01-01", "2019-12-31")
AFTER = ("2024-01-01", "2024-12-31")
S2_BANDS = ["B2", "B3", "B4", "B8", "B11", "B12"]   # Prithvi HLS-style 6-band order
CHANGE_THRESHOLD_PCTL = 80    # top 20% of change scores -> "changed"


# ---------------------------------------------------------------- Earth Engine
def s2_composite(region, start, end):
    coll = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
            .filterBounds(region).filterDate(start, end)
            .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 40)))
    return coll.median().select(S2_BANDS)


def hansen_loss_mask(region):
    g = ee.Image("UMD/hansen/global_forest_change_2025_v1_13")
    return g.select("lossyear").gte(21).And(g.select("treecover2000").gt(30))


def fetch_array(image, region, bands, scale=SCALE_M):
    """Download a small region as a numpy array via getDownloadURL (GeoTIFF)."""
    url = image.clip(region).getDownloadURL({
        "region": region, "scale": scale, "format": "GEO_TIFF", "bands": bands,
    })
    import rasterio
    for attempt in range(4):
        try:
            r = requests.get(url, timeout=120)
            r.raise_for_status()
            with rasterio.open(io.BytesIO(r.content)) as ds:
                return ds.read().astype("float32")     # (bands, H, W)
        except Exception:
            if attempt == 3:
                raise
            time.sleep(3)


# ---------------------------------------------------------------- Prithvi
_MODEL = None


def load_prithvi():
    global _MODEL
    if _MODEL is None:
        from terratorch.registry import BACKBONE_REGISTRY
        import torch
        _MODEL = BACKBONE_REGISTRY.build(
            "prithvi_eo_v2_300", pretrained=True, num_frames=1
        ).eval().cuda()
    return _MODEL


def embed(chip):
    """chip: (6, H, W) float32 -> (D, h, w) patch embeddings."""
    import torch
    model = load_prithvi()
    x = torch.from_numpy(chip).unsqueeze(0).unsqueeze(2).cuda()   # (1,6,1,H,W)
    x = (x - x.mean()) / (x.std() + 1e-6)
    with torch.no_grad():
        feats = model(x)
    if isinstance(feats, (list, tuple)):
        feats = [x for x in feats if x is not None]
        f = feats[-1] if feats else None
    else:
        f = feats
    if f is None:
        raise ValueError("Model returned no embeddings")
    return f.squeeze(0).float().cpu().numpy()


def change_score_map(before_chip, after_chip):
    eb, ea = embed(before_chip), embed(after_chip)
    if eb.ndim == 1:
        # flat embedding — return scalar-like 1x1
        cos = float((eb * ea).sum() / (np.linalg.norm(eb) * np.linalg.norm(ea) + 1e-6))
        return np.array([[1.0 - cos]])
    d = eb.shape[0]
    spatial_shape = eb.shape[1:]          # (h, w) patch grid
    eb = eb.reshape(d, -1); ea = ea.reshape(d, -1)
    cos = (eb * ea).sum(0) / (np.linalg.norm(eb, axis=0) * np.linalg.norm(ea, axis=0) + 1e-6)
    return (1.0 - cos).reshape(spatial_shape)   # (h, w) — was 1D, caused IndexError


# ---------------------------------------------------------------- per mill
def run_mill(lat, lon):
    region = ee.Geometry.Point([lon, lat]).buffer(BUFFER_M).bounds()
    before = fetch_array(s2_composite(region, *BEFORE), region, S2_BANDS)
    after = fetch_array(s2_composite(region, *AFTER), region, S2_BANDS)
    loss = fetch_array(hansen_loss_mask(region).rename("loss"), region, ["loss"])[0]

    h = min(before.shape[1], after.shape[1], loss.shape[0])
    w = min(before.shape[2], after.shape[2], loss.shape[1])
    before, after, loss = before[:, :h, :w], after[:, :h, :w], loss[:h, :w]

    change = change_score_map(before, after)                 # (h', w') coarse
    # upsample change to loss grid
    from scipy.ndimage import zoom
    change_full = zoom(change, (h / change.shape[0], w / change.shape[1]), order=1)

    # per-tile aggregation for the correlation
    ph = pw = 16
    rows = []
    for i in range(0, h - ph, ph):
        for j in range(0, w - pw, pw):
            rows.append((change_full[i:i+ph, j:j+pw].mean(),
                         loss[i:i+ph, j:j+pw].mean()))
    if len(rows) < 5:
        raise ValueError(f"Too few tiles ({len(rows)})")
    rows = np.array(rows)
    rho, p = stats.spearmanr(rows[:, 0], rows[:, 1])

    thr = np.percentile(change_full, CHANGE_THRESHOLD_PCTL)
    pred = (change_full >= thr).ravel().astype(int)
    gold = (loss >= 0.5).ravel().astype(int)
    prec = precision_score(gold, pred, zero_division=0)
    rec = recall_score(gold, pred, zero_division=0)
    iou = jaccard_score(gold, pred, zero_division=0)
    return dict(spearman_rho=round(rho, 3), spearman_p=round(p, 5),
                precision=round(prec, 3), recall=round(rec, 3), iou=round(iou, 3),
                n_tiles=len(rows))


def main():
    mills = pd.read_csv(MILLS_CSV)
    out = []
    for i, m in mills.iterrows():
        try:
            r = run_mill(m["latitude"], m["longitude"])
            print(f"[{i+1}/{len(mills)}] {m['company']:15} {str(m['mill_name'])[:22]:22} "
                  f"rho={r['spearman_rho']:+.3f} iou={r['iou']:.3f}", flush=True)
        except Exception as e:
            print(f"[{i+1}/{len(mills)}] {m['company']} {m['mill_name']}: FAIL {e}", flush=True)
            r = dict(spearman_rho=None, spearman_p=None, precision=None,
                     recall=None, iou=None, n_tiles=0)
        out.append({"company": m["company"], "mill_name": m["mill_name"],
                    "lat": m["latitude"], "lon": m["longitude"], **r})
        if (i + 1) % 20 == 0:
            pd.DataFrame(out).to_csv(OUT_CSV, index=False)
    df = pd.DataFrame(out)
    df.to_csv(OUT_CSV, index=False)
    ok = df.dropna(subset=["spearman_rho"])
    print(f"\n{len(ok)}/{len(df)} mills scored")
    print(f"mean Spearman rho : {ok['spearman_rho'].mean():.3f}")
    print(f"mean IoU vs Hansen: {ok['iou'].mean():.3f}")
    print(ok.groupby("company")[["spearman_rho", "iou"]].mean().round(3).to_string())


if __name__ == "__main__":
    main()
