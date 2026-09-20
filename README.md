# Catching Greenwashing from Space: Verifying Palm Oil Zero-Deforestation Claims Using Satellite Data and Natural Language Processing

**Master of Science Thesis**  
**Author:** Ritik Ghoghari  
**Institution:** GISMA University of Applied Sciences, Berlin  
**Degree:** M.Sc. Data Science, AI & Digital Business  
**Supervisor:** Professor Mohamad Hoseini  
**Submission Deadline:** 26 September 2026  

---

## Executive Summary

This research establishes an empirical, multi-modal auditing framework that confronts corporate sustainability disclosures against physical earth observation data. By integrating NLP-driven claim extraction and sentiment analysis across sustainability reports with high-resolution Google Earth Engine satellite imagery and Hansen Global Forest Change (GFC) data, the pipeline detects discrepancies between corporate zero-deforestation commitments and actual on-the-ground forest clearance.

### Core Metrics & Canonical Facts
- **Scope**: 11 major palm oil companies across 290 supply chain mills.
- **Physical Loss**: **890,168 ha** post-2020 tree cover loss detected within 10 km mill catchments.
- **Highest Mismatch**: **KLK** (Score: 65.6, Rank 1) due to highly assertive zero-deforestation claims contrasted with 92,209 ha loss across 30 mills.
- **Lowest Mismatch**: **Astra Agro** (Score: 17.6, Rank 11) due to highly cautious language and procedurally neutral reporting despite 87,198 ha absolute loss.
- **Formula**:
  $$\text{Mismatch Score} = 0.35 \times \text{Forest Loss} + 0.35 \times \text{Specificity} + 0.15 \times \text{Sentiment} + 0.15 \times \text{Spatial Match}$$
- **Master Status Audit**: See [`docs/TASK_COMPLETION_STATUS.md`](docs/TASK_COMPLETION_STATUS.md) for the 100% completion report across all components.

---

## Project Structure

```
├── .agents/                    # Antigravity agent configurations & skills
├── .claude/                    # Claude agent configurations
├── Reports/                    # 21 official PDF sustainability reports (11 companies)
├── Results/                    # All generated empirical outputs & metrics
│   ├── master_scores.csv       # Canonical mismatch scores and rankings
│   ├── nlp_model_comparison.csv# Benchmark & gold-label evaluation metrics
│   ├── descals_oilpalm_...csv  # Oil palm overlay validation
│   └── satellite_images/
│       └── clearing_maps/      # 290 high-resolution (300 DPI) Sentinel-2 maps (100% complete)
├── data/                       # Structured inputs and datasets
│   ├── mills/                  # Per-company mill coordinates & UML-Jan-2026.csv
│   └── nlp/                    # Enriched corporate claims corpora
├── docs/                       # Project documentation, plans, and session logs
│   ├── HANDOFF_for_next_agent.md
│   ├── TASK_COMPLETION_STATUS.md
│   ├── SESSION_SUMMARY_*.md
│   └── archive/                # Historical plans and Markdown chapter drafts
├── latex/                      # Complete LaTeX thesis draft
│   ├── chapters/               # Chapters 00 (Abstract) through 08 (Conclusion)
│   ├── figures/                # Figures embedded in the thesis
│   ├── main.tex                # Root LaTeX compilation document
│   └── thesis_latex.zip        # Pre-packaged archive ready for Overleaf compilation
├── notebooks/                  # Interactive Jupyter notebooks (main.ipynb, prithvi_poc.ipynb)
├── outputs/                    # Interactive visual outputs (mills_map.html)
├── scripts/                    # Core Python pipeline, scoring, and test suites
│   ├── build_scores_v2.py      # Mismatch scoring engine
│   ├── generate_clearing_maps.py # High-res Sentinel-2 + Hansen GFC map generator
│   ├── model_comparison.py     # NLP benchmarking and evaluation script
│   └── test_*.py               # Automated test suite (23 tests)
├── requirements.txt            # Python dependencies
├── GEMINI.md                   # Antigravity instructions and workspace ground truth
└── CLAUDE.md                   # Claude assistant reference
```

---

## Environment & Quickstart

### 1. Python Environment
All scripts require the dedicated virtual environment with Google Earth Engine (`ee`) and PyTorch:
```powershell
.\venv\Scripts\python.exe <script_path>
```

### 2. Run Test Suite
Confirm pipeline integrity (all 23 tests must pass):
```powershell
.\venv\Scripts\python.exe -m pytest scripts/ -q
```

### 3. Recompute Mismatch Scores
```powershell
.\venv\Scripts\python.exe scripts/build_scores_v2.py
```

### 4. Overleaf Compilation
Upload `latex/thesis_latex.zip` directly to [Overleaf](https://www.overleaf.com) to compile the thesis PDF.
