# Prithvi-EO-2.0 Proof-of-Concept — handoff notes

Professor-approved appendix add-on: compare IBM/NASA's **Prithvi-EO-2.0-300M**
geospatial foundation model against the thesis's primary Hansen Global Forest
Change pipeline, for one representative mill. This doc explains what's already
done, what you do in Colab, and what counts as success vs an honest fallback.

## What's already done (this machine, no GPU needed)

1. **Mill selected:** IOI / SYARIMO, Malaysia — lat 5.334037, lon 117.781334.
   Picked automatically as IOI's single highest post-2020 Hansen loss mill
   (12,317.8 ha of IOI's 15 mills, see `data/mills/ioi_mills.csv`), same
   "worst mill" selection convention already used in
   `scripts/generate_before_after_comparisons.py`.

2. **Region:** 10 km buffer around the mill point (`BUFFER_M = 10000`), matching
   every other Earth Engine script in this repo (`run_forestloss_batch.py`,
   `all_companies_yearly_loss.py`, etc.).

3. **Earth Engine exports started:** `scripts/export_prithvi_poc.py` ran
   against the `thesis-greenwashing` EE project and started three Drive export
   tasks (Google Drive folder **`thesis_prithvi_poc`**):
   - `sentinel2_before_2019.tif` — Sentinel-2 SR harmonized, cloud-masked
     median composite, 2019, 6 bands (B2,B3,B4,B8,B11,B12 = Blue, Green, Red,
     NIR, SWIR1, SWIR2 — Prithvi-EO-2.0's expected band order), 10 m, clipped
     to the 10 km bbox. Built from 21 low-cloud S2 scenes.
   - `sentinel2_after_2024.tif` — same recipe, 2023-06 to 2024-12 (6 scenes;
     the window was widened from a first 2024-only attempt that only found 2
     scenes, to reduce cloud-gap risk).
   - `hansen_groundtruth.tif` — 2-band reference (`treecover2000 > 30%` mask,
     `lossyear >= 21` post-2020 loss mask), 30 m, same bbox — this is the
     ground truth the Prithvi output gets compared against.

   Exports run server-side on Earth Engine (2-10 min typical) and land
   directly in Google Drive under `My Drive/thesis_prithvi_poc/` — no local
   download step needed. Check progress any time at
   https://code.earthengine.google.com/tasks.

4. **Config written:** `data/mills/prithvi_poc_config.json` — mill metadata,
   region bbox, band order, date ranges, and the three export task ids, so the
   notebook doesn't need to guess anything.

5. **Colab notebook written:** `notebooks/prithvi_poc.ipynb` — fully self
   contained, installs its own dependencies, mounts Drive, loads the three
   GeoTIFFs, runs frozen Prithvi-EO-2.0-300M inference tiled over the region,
   computes an unsupervised change score (embedding cosine distance, before vs
   after), compares it against the Hansen loss mask tile-by-tile (Spearman
   correlation + precision/recall/IoU), and saves a 4-panel comparison figure
   back to Drive.

## Exactly what you do in Colab (the one manual step)

1. Open `notebooks/prithvi_poc.ipynb` in Google Colab (upload it, or open from
   Drive/GitHub — whatever's fastest).
2. **Runtime > Change runtime type > T4 GPU** (free tier — try this first).
   If Colab keeps disconnecting the free T4, switch to **Colab Pro** and pick
   any available GPU there; nothing else in the notebook changes.
3. **Runtime > Run all.**
4. Click through two permission prompts as they appear:
   - **Google Drive mount** (early cell) — use the same Google account the
     `thesis-greenwashing` Earth Engine project / Drive exports are tied to.
   - Only if the notebook reports any of the three files as `MISSING` (exports
     still finishing, or wrong account), a fallback cell will prompt one more
     **Earth Engine OAuth** click and re-pull the same imagery directly into
     Colab instead of Drive.
5. Walk away. Everything downstream — model download, tiled inference,
   metrics, figure — runs unattended. Total time ~3-6 minutes on a T4.
6. When it finishes, `prithvi_vs_hansen_comparison.png` is saved back into
   `My Drive/thesis_prithvi_poc/` and also shown inline in the notebook. Pull
   that PNG plus the printed Spearman rho / precision / recall / IoU numbers
   for the thesis appendix.

## What "success" looks like

- The notebook runs end to end without errors.
- Spearman correlation between Prithvi's per-tile change score and Hansen's
  per-tile post-2020 loss fraction is meaningfully positive (rho > ~0.3 is a
  reasonable bar) — i.e. the frozen foundation model's embeddings shift more
  in tiles where Hansen recorded actual forest loss.
- The 4-panel figure visually shows the Prithvi change heatmap lighting up in
  roughly the same places as the Hansen red loss mask.

This would support a modest, honestly-scoped appendix claim: *"a general-purpose
geospatial foundation model, used purely for embeddings with no
deforestation-specific fine-tuning, shows some correlation with the Hansen-based
loss signal for this mill"* — useful corroborating evidence, explicitly **not**
a claim that Prithvi replaces or outperforms the Hansen pipeline that the rest
of the thesis is built on.

## What "honest attempt fallback" looks like (per the 3-day hard-stop rule)

If, after reasonable troubleshooting (checking band order, reflectance
scaling, `terratorch` install/model-loading errors, tile alignment — the
notebook's Cell 5 already tries three different registry key spellings and
prints the full backbone list if all fail), one of these happens:

- `terratorch`/model loading never succeeds in Colab, or
- Colab disconnects repeatedly even on Pro, or
- the correlation comes back near zero / noisy with no fixable cause,

then **stop after 3 days of attempts** and report it as an honest attempt in
the thesis: *"A Prithvi-EO-2.0 proof-of-concept was attempted for IOI/SYARIMO
using the frozen 300M encoder on Sentinel-2 imagery; exact setup and observed
failure mode are documented in `Results/prithvi_poc_readme.md`."* That is a
legitimate, defensible outcome for an appendix POC. The Hansen-based analysis
across all 290 mills remains the thesis's primary, load-bearing methodology
regardless of how this side experiment turns out.

## Files involved

- `scripts/export_prithvi_poc.py` — local script, already run, started the EE
  Drive exports (re-runnable if you ever need a different mill/region).
- `data/mills/prithvi_poc_config.json` — generated config (mill, region, bands,
  task ids).
- `notebooks/prithvi_poc.ipynb` — the Colab notebook, run this.
- `Results/prithvi_poc_readme.md` — this file.
- Output (after running the notebook): Google Drive
  `My Drive/thesis_prithvi_poc/prithvi_vs_hansen_comparison.png`.
