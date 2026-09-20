"""Generate publication-grade analytical charts for the thesis.

Produces charts saved to latex/figures/ and Results/:
1. dual_track_quadrant.png: Satellite Track vs NLP Track scatter plot (Dual-Track Verification Architecture Results)
2. dual_track_comparison.png: Side-by-side comparison of Satellite Track, NLP Track, and Composite Mismatch Score
3. mismatch_score_decomposition.png: Stacked component decomposition (Forest Loss, Specificity, Sentiment, Spatial Match)
4. annual_forest_loss_trends.png: Annual post-2020 forest loss trends (2021-2025)
5. descals_landcover_conversion.png: Oil palm land cover conversion breakdown (Descals overlay)
6. buffer_sensitivity_curves.png: Forest loss % across buffer distances (5-30 km)
7. nlp_model_evaluation.png: Domain evaluation metrics across NLP models and baselines
8. prithvi_foundation_model.png: Prithvi-EO-2.0-300M Spearman rho and IoU across 11 companies
"""

import os
import shutil
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.patches import Rectangle

# Setup clean academic style
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9.5,
    'ytick.labelsize': 9.5,
    'legend.fontsize': 9.5,
    'figure.titlesize': 13,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': True,
    'grid.alpha': 0.25,
    'grid.linestyle': '--',
})

# Company display names mapping
COMPANY_NAMES = {
    'klk': 'KLK',
    'gar': 'GAR',
    'musimmas': 'Musim Mas',
    'ioi': 'IOI',
    'sdguthrie': 'SD Guthrie',
    'wilmar': 'Wilmar',
    'firstresources': 'First Resources',
    'genting': 'Genting',
    'bumitama': 'Bumitama',
    'sipef': 'SIPEF',
    'astraagro': 'Astra Agro',
    'KLK': 'KLK',
    'GAR': 'GAR',
    'Musim Mas': 'Musim Mas',
    'IOI': 'IOI',
    'SD Guthrie': 'SD Guthrie',
    'Wilmar': 'Wilmar',
    'First Resources': 'First Resources',
    'Genting': 'Genting',
    'Bumitama': 'Bumitama',
    'SIPEF': 'SIPEF',
    'Astra Agro': 'Astra Agro',
}

OUTPUT_DIR = "latex/figures"
RESULTS_DIR = "Results"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_master_scores():
    df = pd.read_csv(os.path.join(RESULTS_DIR, "master_scores.csv"))
    df['company_display'] = df['company'].map(COMPANY_NAMES).fillna(df['company'])
    # Calculate Dual Tracks (each on 0-100 scale)
    # Track 1 (Satellite Remote Sensing): 0.35 loss + 0.15 spatial = 0.50 max -> scale to 100
    df['satellite_track'] = (0.35 * df['forest_loss_score'] + 0.15 * df['spatial_match_score']) / 0.50
    # Track 2 (NLP Corporate Disclosures): 0.35 spec + 0.15 sent = 0.50 max -> scale to 100
    df['nlp_track'] = (0.35 * df['specificity_score'] + 0.15 * df['sentiment_score_norm']) / 0.50
    # Weighted contribution points (sum = mismatch_score)
    df['contrib_loss'] = 0.35 * df['forest_loss_score']
    df['contrib_spec'] = 0.35 * df['specificity_score']
    df['contrib_sent'] = 0.15 * df['sentiment_score_norm']
    df['contrib_spatial'] = 0.15 * df['spatial_match_score']
    return df


def plot_dual_track_quadrant(df):
    """Figure 1: Dual-Track Verification Architecture Quadrant (Scatter Matrix)."""
    fig, ax = plt.subplots(figsize=(9, 6.5))
    
    # Quadrant background shading
    ax.axhspan(50, 100, xmin=0.5, xmax=1.0, color='#fee2e2', alpha=0.3, zorder=0) # High Mismatch / Greenwashing
    ax.axhspan(0, 50, xmin=0.5, xmax=1.0, color='#fed7aa', alpha=0.25, zorder=0)  # High Deforestation, Low Claims
    ax.axhspan(50, 100, xmin=0.0, xmax=0.5, color='#e0e7ff', alpha=0.25, zorder=0) # High Claims, Lower Loss
    ax.axhspan(0, 50, xmin=0.0, xmax=0.5, color='#dcfce7', alpha=0.3, zorder=0)  # Low Relative Mismatch

    # Midpoint dividing lines
    ax.axvline(50, color='#94a3b8', linestyle=':', linewidth=1.2, zorder=1)
    ax.axhline(50, color='#94a3b8', linestyle=':', linewidth=1.2, zorder=1)

    # Bubble sizes based on post-2020 forest loss ha
    sizes = df['loss_post2020_ha'] / 400

    # Scatter points colored by mismatch score
    scatter = ax.scatter(
        df['satellite_track'],
        df['nlp_track'],
        s=sizes,
        c=df['mismatch_score'],
        cmap='YlOrRd',
        edgecolors='#1e293b',
        linewidth=1.5,
        alpha=0.9,
        zorder=3
    )

    # Colorbar
    cbar = plt.colorbar(scatter, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Composite Mismatch Score (0-100)', fontsize=10, fontweight='bold')

    # Quadrant category text watermarks placed cleanly in corners
    ax.text(75, 98, "QUADRANT I: HIGH MISMATCH\nStrong Claims vs Severe Satellite Loss\n(Active Greenwashing Hotspot)",
            fontsize=8.5, fontweight='bold', color='#991b1b', ha='center', va='top', alpha=0.75)
    ax.text(75, 2, "QUADRANT IV: CHEAP TALK / UNCHECKABLE\nSevere Satellite Loss vs Vague Commitments\n(High Loss, Low Specificity)",
            fontsize=8.5, fontweight='bold', color='#9a3412', ha='center', va='bottom', alpha=0.75)
    ax.text(16, 98, "QUADRANT II: COMMITTED / MODERATE LOSS\nStrong Commitments, Moderate Catchment Loss",
            fontsize=8.5, fontweight='bold', color='#3730a3', ha='center', va='top', alpha=0.75)
    ax.text(16, 2, "QUADRANT III: LOWER RELATIVE MISMATCH\nModerate Loss, Neutral / Procedural Disclosures",
            fontsize=8.5, fontweight='bold', color='#166534', ha='center', va='bottom', alpha=0.75)

    # Label points with company and rank
    # Manual offsets to prevent overlaps
    offsets = {
        'KLK': (12, 4),
        'GAR': (14, 6),
        'Musim Mas': (-110, 8),
        'IOI': (-112, 8),
        'SD Guthrie': (14, -4),
        'Wilmar': (12, -4),
        'First Resources': (12, -12),
        'Genting': (12, -8),
        'Bumitama': (12, 6),
        'SIPEF': (12, 4),
        'Astra Agro': (12, 8),
    }

    for _, row in df.iterrows():
        comp = row['company_display']
        dx, dy = offsets.get(comp, (8, 8))
        ax.annotate(
            f"{comp} (#{int(row['rank'])}, {row['mismatch_score']:.1f})",
            (row['satellite_track'], row['nlp_track']),
            xytext=(dx, dy),
            textcoords='offset points',
            fontsize=8.5,
            fontweight='bold',
            color='#0f172a',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='white', alpha=0.85, edgecolor='#cbd5e1', lw=0.6),
            zorder=4
        )

    ax.set_xlim(-2, 104)
    ax.set_ylim(-2, 105)
    ax.set_xlabel('Track 1: Satellite Remote Sensing Score (Physical Forest Loss Evidence, 0-100)', fontweight='bold')
    ax.set_ylabel('Track 2: NLP Corporate Claims Score (Specificity & Tone Ambition, 0-100)', fontweight='bold')
    ax.set_title('Dual-Track Verification Architecture: Empirical Results Across 11 Companies\nBubble area represents post-2020 forest loss footprint (ha); Rank #1 to #11',
                 fontweight='bold', pad=12)

    # Legend for bubble sizes
    for area, label in [(40000, '40k ha'), (100000, '100k ha'), (170000, '170k ha')]:
        ax.scatter([], [], s=area / 400, c='#94a3b8', edgecolors='#1e293b', alpha=0.6, label=label)
    ax.legend(title='Post-2020 Forest Loss', loc='center left', frameon=True, fontsize=8.5, title_fontsize=9)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "dual_track_quadrant.png"))
    plt.close()
    print("Saved dual_track_quadrant.png")


def plot_dual_track_comparison(df):
    """Figure 2: Dual-Track Side-by-Side Comparison & Mismatch Score."""
    df_sorted = df.sort_values('mismatch_score', ascending=True)
    
    y = np.arange(len(df_sorted))
    height = 0.28

    fig, ax = plt.subplots(figsize=(10, 7))

    bars1 = ax.barh(y + height, df_sorted['satellite_track'], height, label='Track 1: Satellite Remote Sensing (Physical)',
                    color='#0284c7', edgecolor='#0369a1', alpha=0.9, zorder=3)
    bars2 = ax.barh(y, df_sorted['nlp_track'], height, label='Track 2: NLP Claims Disclosure (Textual)',
                    color='#d97706', edgecolor='#b45309', alpha=0.9, zorder=3)
    bars3 = ax.barh(y - height, df_sorted['mismatch_score'], height, label='Composite Mismatch Score (Weighted 50/50)',
                    color='#dc2626', edgecolor='#991b1b', alpha=0.95, zorder=3)

    ax.set_yticks(y)
    ax.set_yticklabels([f"{row['company_display']} (#{int(row['rank'])})" for _, row in df_sorted.iterrows()],
                       fontweight='bold')
    ax.set_xlabel('Normalized Score (0-100)', fontweight='bold')
    ax.set_xlim(0, 110)
    ax.set_title('Dual-Track Verification: Satellite Evidence vs Corporate Claims vs Mismatch Score\nComparing Physical Remote Sensing Track and Textual Disclosure Track',
                 fontweight='bold', pad=12)
    ax.legend(loc='lower right', frameon=True, framealpha=0.95)

    # Value annotations on the Mismatch Score bars
    for i, (_, row) in enumerate(df_sorted.iterrows()):
        ax.text(row['mismatch_score'] + 1.2, i - height, f"{row['mismatch_score']:.1f}",
                va='center', fontsize=8.5, fontweight='bold', color='#991b1b')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "dual_track_comparison.png"))
    plt.close()
    print("Saved dual_track_comparison.png")


def plot_mismatch_decomposition(df):
    """Figure 3: Stacked Component Decomposition of Mismatch Score."""
    df_sorted = df.sort_values('mismatch_score', ascending=True)
    
    y = np.arange(len(df_sorted))
    height = 0.55

    fig, ax = plt.subplots(figsize=(10, 6.5))

    p1 = ax.barh(y, df_sorted['contrib_loss'], height, label='Forest Loss (35% weight)',
                 color='#dc2626', edgecolor='#991b1b', zorder=3)
    p2 = ax.barh(y, df_sorted['contrib_spec'], height, left=df_sorted['contrib_loss'],
                 label='Claim Specificity (35% weight)', color='#2563eb', edgecolor='#1d4ed8', zorder=3)
    p3 = ax.barh(y, df_sorted['contrib_sent'], height,
                 left=df_sorted['contrib_loss'] + df_sorted['contrib_spec'],
                 label='Claim Sentiment (15% weight)', color='#d97706', edgecolor='#b45309', zorder=3)
    p4 = ax.barh(y, df_sorted['contrib_spatial'], height,
                 left=df_sorted['contrib_loss'] + df_sorted['contrib_spec'] + df_sorted['contrib_sent'],
                 label='Spatial Severity Match (15% weight)', color='#059669', edgecolor='#047857', zorder=3)

    ax.set_yticks(y)
    ax.set_yticklabels([f"{row['company_display']} (#{int(row['rank'])})" for _, row in df_sorted.iterrows()],
                       fontweight='bold')
    ax.set_xlabel('Score Points Contributed (Sum = Mismatch Score, 0-100)', fontweight='bold')
    ax.set_xlim(0, 75)
    ax.set_title('Mismatch Score Component Decomposition Across 11 Companies\nExact breakdown of physical and textual formula contributions (Table 4.2)',
                 fontweight='bold', pad=12)
    ax.legend(loc='lower right', frameon=True, framealpha=0.95)

    for i, (_, row) in enumerate(df_sorted.iterrows()):
        ax.text(row['mismatch_score'] + 0.8, i, f"Score: {row['mismatch_score']:.1f}",
                va='center', fontsize=9, fontweight='bold', color='#0f172a')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "mismatch_score_decomposition.png"))
    plt.close()
    print("Saved mismatch_score_decomposition.png")


def plot_annual_forest_loss():
    """Figure 4: Annual Forest Loss Trends (2021-2025)."""
    df = pd.read_csv(os.path.join(RESULTS_DIR, "all_companies_yearly_loss_summary.csv"))
    df['company_display'] = df['company'].map(COMPANY_NAMES).fillna(df['company'])
    df = df.sort_values('sum_2021_2025', ascending=False)

    years = ['2021', '2022', '2023', '2024', '2025']
    yearly_totals = [df[yr].sum() for yr in years]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.2), gridspec_kw={'width_ratios': [1.2, 1.8]})

    # Left: Total sector post-2020 annual loss
    bars = ax1.bar(years, [val / 1000 for val in yearly_totals], color='#1b4d3e', edgecolor='#0f2922', width=0.55, zorder=3)
    ax1.set_ylabel('Total Post-2020 Forest Loss (Thousand Hectares)', fontweight='bold')
    ax1.set_xlabel('Monitoring Year', fontweight='bold')
    ax1.set_title('Sector Annual Total Loss\nSpike in 2023 across 290 Mills', fontweight='bold')
    ax1.set_ylim(0, 250)

    for bar, val in zip(bars, yearly_totals):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 4,
                 f"{val:,.0f} ha", ha='center', fontsize=8.5, fontweight='bold')

    # Right: Company-by-company trajectory
    colors = ['#dc2626', '#ea580c', '#d97706', '#ca8a04', '#65a30d', '#16a34a',
              '#059669', '#0d9488', '#0284c7', '#2563eb', '#7c3aed']
    for idx, (_, row) in enumerate(df.iterrows()):
        values = [row[yr] / 1000 for yr in years]
        comp = row['company_display']
        lw = 2.4 if comp in ['GAR', 'IOI', 'Wilmar', 'SD Guthrie'] else 1.2
        alpha = 1.0 if comp in ['GAR', 'IOI', 'Wilmar', 'SD Guthrie'] else 0.65
        ax2.plot(years, values, marker='o', markersize=4, label=f"{comp}", color=colors[idx % len(colors)],
                 linewidth=lw, alpha=alpha, zorder=3)

    ax2.set_ylabel('Annual Forest Loss (Thousand Hectares)', fontweight='bold')
    ax2.set_xlabel('Monitoring Year', fontweight='bold')
    ax2.set_title('Annual Forest Loss Trajectory by Company\nPersistent clearing at Wilmar, Peak at GAR & SD Guthrie', fontweight='bold')
    ax2.legend(loc='upper right', bbox_to_anchor=(1.35, 1.0), frameon=True, fontsize=8.5)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "annual_forest_loss_trends.png"))
    plt.close()
    print("Saved annual_forest_loss_trends.png")


def plot_descals_landcover():
    """Figure 5: Descals Oil Palm Land Cover Overlay."""
    df = pd.read_csv(os.path.join(RESULTS_DIR, "descals_oilpalm_overlay_by_company.csv"))
    df['company_display'] = df['company'].map(COMPANY_NAMES).fillna(df['company'])
    df = df.sort_values('pct_loss_to_palm', ascending=True)

    # Compute breakdown percentages
    pct_industrial = df['pct_loss_to_industrial']
    pct_smallholder = df['pct_loss_to_palm'] - df['pct_loss_to_industrial']
    pct_non_palm = 100.0 - df['pct_loss_to_palm']

    y = np.arange(len(df))
    height = 0.55

    fig, ax = plt.subplots(figsize=(9.5, 6))

    ax.barh(y, pct_industrial, height, label='Industrial Closed-Canopy Palm', color='#15803d', edgecolor='#166534', zorder=3)
    ax.barh(y, pct_smallholder, height, left=pct_industrial, label='Smallholder / Other Oil Palm', color='#84cc16', edgecolor='#65a30d', zorder=3)
    ax.barh(y, pct_non_palm, height, left=pct_industrial + pct_smallholder, label='Other Land Cover / Not Planted', color='#cbd5e1', edgecolor='#94a3b8', zorder=3)

    # Vertical line at network mean (56.0%)
    ax.axvline(56.0, color='#b91c1c', linestyle='--', linewidth=1.5, label='Sector Mean Palm Conversion (56.0%)', zorder=4)

    ax.set_yticks(y)
    ax.set_yticklabels(df['company_display'], fontweight='bold')
    ax.set_xlabel('Percentage of Post-2020 Forest Loss Area (%)', fontweight='bold')
    ax.set_xlim(0, 100)
    ax.set_title('Land Cover of Cleared Forest Areas in 10 km Mill Catchments\nOverlay with Descals et al. (2021) 10 m Oil Palm Map (Table 4.6)',
                 fontweight='bold', pad=12)
    ax.legend(loc='lower right', frameon=True, framealpha=0.95)

    for i, (_, row) in enumerate(df.iterrows()):
        ax.text(row['pct_loss_to_palm'] + 1.2, i, f"{row['pct_loss_to_palm']:.1f}%",
                va='center', fontsize=8.5, fontweight='bold', color='#14532d')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "descals_landcover_conversion.png"))
    plt.close()
    print("Saved descals_landcover_conversion.png")


def plot_buffer_sensitivity():
    """Figure 6: Buffer Sensitivity Analysis (5 km to 30 km)."""
    df = pd.read_csv(os.path.join(RESULTS_DIR, "buffer_sensitivity.csv"))
    df['company_display'] = df['company'].map(COMPANY_NAMES).fillna(df['company'])

    fig, ax = plt.subplots(figsize=(9, 5.8))
    buffers = [5, 10, 15, 20, 30]

    colors = ['#dc2626', '#ea580c', '#d97706', '#ca8a04', '#65a30d', '#16a34a',
              '#059669', '#0d9488', '#0284c7', '#2563eb', '#7c3aed']

    # Highlight canonical 10 km buffer
    ax.axvspan(9.2, 10.8, color='#dbeafe', alpha=0.5, label='Canonical Buffer (10 km)', zorder=1)

    for idx, comp in enumerate(df['company_display'].unique()):
        comp_df = df[df['company_display'] == comp].sort_values('buffer_km')
        ax.plot(comp_df['buffer_km'], comp_df['loss_pct'], marker='o', markersize=5,
                label=comp, color=colors[idx % len(colors)], linewidth=1.8, zorder=3)

    ax.set_xticks(buffers)
    ax.set_xlabel('Buffer Radius around Mill (km)', fontweight='bold')
    ax.set_ylabel('Forest Loss (% of Year-2000 Forest Baseline)', fontweight='bold')
    ax.set_title('Sensitivity of Forest Loss Percentage to Catchment Buffer Radius\nRepresentative Mills across 11 Companies (5 km to 30 km; Table 4.7)',
                 fontweight='bold', pad=12)
    ax.legend(loc='upper right', bbox_to_anchor=(1.25, 1.0), frameon=True, fontsize=8.5)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "buffer_sensitivity_curves.png"))
    plt.close()
    print("Saved buffer_sensitivity_curves.png")


def plot_nlp_model_evaluation():
    """Figure 7: NLP Model Domain Evaluation Benchmarks."""
    # Data from Table 4.8 / nlp_model_comparison.csv
    tasks = [
        'Claim Detection\n(F1 Score)',
        'Specificity\n(Accuracy)',
        'Sentiment\n(Accuracy)',
        'ESG Topic\n(Accuracy)'
    ]
    models = ['Primary Fine-Tuned Model', 'Baseline / Alternative']
    
    primary_scores = [0.981, 0.538, 0.811, 0.802]
    baseline_scores = [0.828, 0.613, 0.509, 0.189]
    primary_labels = ['Environmental-Claims', 'ClimateBERT Spec.', 'FinBERT', 'ESG-BERT']
    baseline_labels = ['Keyword Filter', 'Regex Num/Date', 'Climate-Sentiment', 'Keyword Tags']

    x = np.arange(len(tasks))
    width = 0.35

    fig, ax = plt.subplots(figsize=(9, 5.5))

    b1 = ax.bar(x - width/2, primary_scores, width, label='Primary Model / Architecture',
                color='#1b4d3e', edgecolor='#0f2922', zorder=3)
    b2 = ax.bar(x + width/2, baseline_scores, width, label='Baseline / Comparative Alternative',
                color='#94a3b8', edgecolor='#64748b', zorder=3)

    ax.set_ylabel('Evaluation Score (0.0 to 1.0)', fontweight='bold')
    ax.set_title('NLP Model Evaluation on Gold-Labeled Palm Oil Disclosure Corpus\nStratified domain sample (n=150 claim detection; n=106 claim-level tasks; Table 4.8)',
                 fontweight='bold', pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(tasks, fontweight='bold')
    ax.set_ylim(0, 1.15)
    ax.legend(loc='upper right', frameon=True)

    # Label values and model names above bars
    for i in range(len(tasks)):
        ax.text(x[i] - width/2, primary_scores[i] + 0.02, f"{primary_scores[i]:.3f}\n({primary_labels[i]})",
                ha='center', va='bottom', fontsize=8, fontweight='bold', color='#1b4d3e')
        ax.text(x[i] + width/2, baseline_scores[i] + 0.02, f"{baseline_scores[i]:.3f}\n({baseline_labels[i]})",
                ha='center', va='bottom', fontsize=8, color='#475569')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "nlp_model_evaluation.png"))
    plt.close()
    print("Saved nlp_model_evaluation.png")


def plot_prithvi_evaluation():
    """Figure 8: Prithvi Foundation Model Change Detection Metrics."""
    # Table 4.4 data
    companies = ['Bumitama', 'First Res.', 'KLK', 'IOI', 'GAR', 'Musim Mas',
                 'Astra Agro', 'Wilmar', 'SD Guthrie', 'SIPEF', 'Genting']
    spearman_rho = [0.216, 0.188, 0.188, 0.182, 0.174, 0.173, 0.168, 0.163, 0.159, 0.153, 0.152]
    iou = [0.068, 0.095, 0.093, 0.119, 0.089, 0.077, 0.078, 0.084, 0.096, 0.066, 0.068]

    x = np.arange(len(companies))
    width = 0.38

    fig, ax1 = plt.subplots(figsize=(10, 5.5))

    color1 = '#0284c7'
    color2 = '#d97706'

    b1 = ax1.bar(x - width/2, spearman_rho, width, label='Spearman Rank Correlation (rho)',
                 color=color1, edgecolor='#0369a1', zorder=3)
    ax1.set_ylabel('Spearman Correlation (rho) vs Hansen Loss', color=color1, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.set_ylim(0, 0.28)

    ax2 = ax1.twinx()
    b2 = ax2.bar(x + width/2, iou, width, label='Intersection-over-Union (IoU)',
                 color=color2, edgecolor='#b45309', zorder=3)
    ax2.set_ylabel('Mean IoU Overlap', color=color2, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.set_ylim(0, 0.16)
    ax2.spines['right'].set_visible(True)

    # Sector mean horizontal lines
    ax1.axhline(0.172, color=color1, linestyle='--', linewidth=1.2, alpha=0.7, label='Network Mean rho (0.172)')
    ax2.axhline(0.086, color=color2, linestyle=':', linewidth=1.2, alpha=0.7, label='Network Mean IoU (0.086)')

    ax1.set_xticks(x)
    ax1.set_xticklabels(companies, rotation=25, ha='right', fontweight='bold')
    ax1.set_title('IBM/NASA Prithvi-EO-2.0 Foundation Model Change Detection Across 290 Mills\nTemporal Cosine Dissimilarity vs Hansen Global Forest Change Mask (Table 4.4)',
                  fontweight='bold', pad=12)

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', frameon=True, fontsize=8.5)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "prithvi_foundation_model.png"))
    plt.close()
    print("Saved prithvi_foundation_model.png")


def copy_architecture_diagram():
    """Copy system architecture diagram to latex figures."""
    src = "diagrams/thesis_architecture.visual-check.2048x1320.light.png"
    dst = os.path.join(OUTPUT_DIR, "system_architecture.png")
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"Copied architecture diagram from {src} to {dst}")
    else:
        print(f"Warning: {src} not found")


def main():
    print("Generating all thesis publication charts...")
    copy_architecture_diagram()
    df = load_master_scores()
    plot_dual_track_quadrant(df)
    plot_dual_track_comparison(df)
    plot_mismatch_decomposition(df)
    plot_annual_forest_loss()
    plot_descals_landcover()
    plot_buffer_sensitivity()
    plot_nlp_model_evaluation()
    plot_prithvi_evaluation()
    print("Successfully generated all 8 publication charts and copied architecture diagram!")


if __name__ == "__main__":
    main()
