import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

COLOR_DARK_GREEN = RGBColor(26, 60, 31)     # #1A3C1F - Primary Brand
COLOR_FOREST_GREEN = RGBColor(46, 107, 53)  # #2E6B35 - Secondary Brand
COLOR_CHARCOAL = RGBColor(40, 40, 40)       # #282828 - Body Text
COLOR_MUTED_GRAY = RGBColor(110, 110, 110)  # Captions / Footers
HEX_DARK_GREEN = "1A3C1F"
HEX_FOREST_GREEN = "2E6B35"
HEX_LIGHT_BG = "F4F7F4"
HEX_BORDER = "CCCCCC"
HEX_CALLOUT_BG = "EBF3EC"

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=90, bottom=90, left=130, right=130):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_table_borders(table, border_color=HEX_BORDER):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>'
        f'<w:bottom w:val="single" w:sz="8" w:space="0" w:color="{border_color}"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>'
        f'<w:insideV w:val="none"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def format_cell(cell, text, bold=False, color=COLOR_CHARCOAL, font_size=9.0, align=WD_ALIGN_PARAGRAPH.LEFT):
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(text)
    run.bold = bold
    run.font.name = "Calibri"
    run.font.size = Pt(font_size)
    run.font.color.rgb = color

def add_callout(doc, text, bold_prefix="Key Takeaway: "):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, HEX_CALLOUT_BG)
    set_cell_margins(cell, top=110, bottom=110, left=150, right=130)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{HEX_FOREST_GREEN}"/>'
        f'<w:top w:val="none"/>'
        f'<w:bottom w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    
    run_pre = p.add_run(bold_prefix)
    run_pre.bold = True
    run_pre.font.color.rgb = COLOR_DARK_GREEN
    run_pre.font.size = Pt(10.0)
    run_pre.font.name = "Calibri"
    
    run_text = p.add_run(text)
    run_text.font.size = Pt(10.0)
    run_text.font.name = "Calibri"
    run_text.font.color.rgb = COLOR_CHARCOAL
    
    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(4)

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.bold = True
    run.font.name = "Calibri"
    run.font.size = Pt(15)
    run.font.color.rgb = COLOR_DARK_GREEN
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.bold = True
    run.font.name = "Calibri"
    run.font.size = Pt(12.5)
    run.font.color.rgb = COLOR_FOREST_GREEN
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.bold = True
    run.font.name = "Calibri"
    run.font.size = Pt(11)
    run.font.color.rgb = COLOR_CHARCOAL
    return p

def add_body_p(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(10.5)
    run.font.color.rgb = COLOR_CHARCOAL
    return p

def add_bullet_item(doc, bold_lead, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    run_b = p.add_run(bold_lead + ": ")
    run_b.bold = True
    run_b.font.name = "Calibri"
    run_b.font.size = Pt(10.0)
    run_b.font.color.rgb = COLOR_DARK_GREEN
    run_t = p.add_run(text)
    run_t.font.name = "Calibri"
    run_t.font.size = Pt(10.0)
    run_t.font.color.rgb = COLOR_CHARCOAL
    return p

def add_caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run(text)
    run.italic = True
    run.font.name = "Calibri"
    run.font.size = Pt(9.0)
    run.font.color.rgb = COLOR_MUTED_GRAY
    return p

def add_image_safe(doc, img_path, caption_text, width_inches=5.8):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(2)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(width_inches))
        add_caption(doc, caption_text)

def build_full_document(output_path):
    doc = Document()
    
    # Configure 1-inch margins on US Letter / A4
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)
        
        # Header setup
        header = section.header
        hp = header.paragraphs[0]
        hp.text = "Catching Greenwashing from Space | Master Thesis Overview | Ritik Ghoghari"
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hp.style.font.name = "Calibri"
        hp.style.font.size = Pt(8.5)
        hp.style.font.color.rgb = COLOR_MUTED_GRAY

    # Title Block
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    run_title = title_p.add_run("Catching Greenwashing from Space")
    run_title.bold = True
    run_title.font.name = "Calibri"
    run_title.font.size = Pt(22)
    run_title.font.color.rgb = COLOR_DARK_GREEN

    subtitle_p = doc.add_paragraph()
    subtitle_p.paragraph_format.space_before = Pt(0)
    subtitle_p.paragraph_format.space_after = Pt(14)
    run_sub = subtitle_p.add_run("Verifying Palm Oil Zero-Deforestation Claims Using Satellite Data and Natural Language Processing")
    run_sub.italic = True
    run_sub.font.name = "Calibri"
    run_sub.font.size = Pt(12)
    run_sub.font.color.rgb = COLOR_FOREST_GREEN

    # Metadata Summary Box
    meta_table = doc.add_table(rows=5, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False
    col_widths = [Inches(1.8), Inches(4.7)]
    
    meta_data = [
        ("Author / Candidate", "Ritik Ghoghari (M.Sc. Data Science, AI & Digital Business)"),
        ("Institution", "GISMA University of Applied Sciences, Berlin"),
        ("Academic Supervisor", "Professor Mohamad Hoseini"),
        ("Submission Date", "September 2026"),
        ("Document Classification", "Master Thesis Overview and Technical Reference Guide")
    ]
    for row_idx, (label, val) in enumerate(meta_data):
        row = meta_table.rows[row_idx]
        for c_idx, cell in enumerate(row.cells):
            cell.width = col_widths[c_idx]
            set_cell_background(cell, HEX_LIGHT_BG if row_idx % 2 == 0 else "FFFFFF")
            set_cell_margins(cell, top=55, bottom=55, left=90, right=90)
            if c_idx == 0:
                format_cell(cell, label, bold=True, color=COLOR_DARK_GREEN, font_size=9.5)
            else:
                format_cell(cell, val, bold=False, color=COLOR_CHARCOAL, font_size=9.5)
    set_table_borders(meta_table)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # --- SECTION 1: EXECUTIVE SUMMARY ---
    add_heading_1(doc, "1. Executive Summary and Thesis Identity")
    
    add_body_p(doc, 
        "Corporate sustainability reports in the palm oil sector routinely feature ambitious commitments to zero deforestation, "
        "protecting peatlands, and eliminating exploitation (NDPE). However, independent verification of these corporate statements "
        "against physical ground reality has remained an open challenge in data science and environmental accounting. "
        "Prior academic literature either scores corporate disclosures for linguistic ambiguity without checking physical ground truth, "
        "or measures regional deforestation by satellite without linking measured clearings to specific corporate statements. "
        "This master's thesis closes that verification gap by developing an empirical pipeline that compares corporate sustainability claims "
        "directly against independent satellite observations across eleven major palm oil conglomerates."
    )
    add_body_p(doc,
        "The methodological framework integrates two independent, decoupled evidence streams. The textual stream extracts and analyzes 55 specific "
        "deforestation claims from corporate sustainability reports using domain-adapted transformer models (ClimateBERT and FinBERT). "
        "The physical remote sensing stream measures annual tree cover loss from the Hansen Global Forest Change dataset across 290 geolocated palm oil "
        "mills matched through the Universal Mill List, applying a 10 km radial catchment buffer and anchored to the EU Deforestation Regulation "
        "(Regulation EU 2023/1115) cutoff date of 31 December 2020. These two streams combine only at a final scoring stage into a four-component "
        "mismatch score, ensuring that neither layer biases or influences the other."
    )
    
    add_callout(doc,
        "Across all 11 companies and 290 matched mills, the satellite record reveals 890,168 hectares of post-2020 forest loss. "
        "Every single mill in the dataset (100% universality) recorded measurable forest loss inside its 10 km catchment, with a minimum single-mill loss of 105 ha. "
        "The mismatch score separates firms along a gradient (KLK rank 1 at 65.6 down to Astra Agro rank 11 at 17.6), revealing that corporate greenwashing "
        "in palm oil is not an isolated anomaly of rogue actors, but an industry-wide structural continuum.",
        bold_prefix="Core Headline Finding: "
    )

    # Key Statistics Cards Table
    stat_table = doc.add_table(rows=2, cols=4)
    stat_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    stat_table.autofit = False
    stat_widths = [Inches(1.625)] * 4
    
    stat_headers = ["Total Post-2020 Loss", "Matched Mills", "Sampled Companies", "Score Range"]
    stat_values = ["890,168 ha", "290 Mills", "11 Conglomerates", "17.6 to 65.6"]
    
    for c_idx, cell in enumerate(stat_table.rows[0].cells):
        cell.width = stat_widths[c_idx]
        set_cell_background(cell, HEX_DARK_GREEN)
        set_cell_margins(cell, top=70, bottom=70, left=50, right=50)
        format_cell(cell, stat_headers[c_idx], bold=True, color=RGBColor(255, 255, 255), font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER)
        
    for c_idx, cell in enumerate(stat_table.rows[1].cells):
        cell.width = stat_widths[c_idx]
        set_cell_background(cell, HEX_CALLOUT_BG)
        set_cell_margins(cell, top=90, bottom=90, left=50, right=50)
        format_cell(cell, stat_values[c_idx], bold=True, color=COLOR_FOREST_GREEN, font_size=11.0, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_table_borders(stat_table)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # --- SECTION 2: RESEARCH CONTEXT & THE VERIFICATION GAP ---
    add_heading_1(doc, "2. Research Context, Conceptual Framework, and the Verification Gap")
    
    add_heading_2(doc, "2.1 The Greenwashing Problem and Cheap Talk")
    add_body_p(doc,
        "Palm oil production is one of the primary drivers of tropical forest conversion across Indonesia, Malaysia, and Papua New Guinea. "
        "In response to sustained consumer boycotts, NGO campaigns, and international supply chain scrutiny, major palm oil producers now routinely "
        "publish group-wide No Deforestation, No Peat, No Exploitation (NDPE) policies. However, a public commitment is not factual proof of compliance. "
        "Bingler, Kraus, and Leippold (2022) categorize non-binding corporate commitments as 'cheap talk': assertions that appear substantive but "
        "commit an organization to nothing measurable, lacking clear operational targets, concrete completion dates, and independent verification mechanisms. "
        "Furthermore, Bingler et al. demonstrate that disclosure vagueness is not an accidental stylistic trait, but an intentional corporate communication "
        "strategy that correlates with weaker underlying ESG performance."
    )
    
    add_heading_2(doc, "2.2 The Missing Verification Gap in the Literature")
    add_body_p(doc,
        "Recent scholarly literature surveys explicitly identify the absence of external physical verification as the primary bottleneck in computational "
        "greenwashing research. Two independent literature surveys define this exact gap:"
    )
    add_bullet_item(doc, "Calamai et al. (2025)",
        "Reviewing NLP techniques in sustainability disclosure, Calamai et al. emphasize that no verified benchmark dataset of real-world greenwashing "
        "cases currently exists. Consequently, language models can be trained to detect linguistic hedging or vague wording, but cannot be evaluated against "
        "ground-truth evidence determining whether the underlying company actually engaged in deforestation."
    )
    add_bullet_item(doc, "Ong et al. (2025)",
        "Surveying automated greenwashing detection systems from the tool architecture perspective, Ong et al. find that existing tools evaluate text solely "
        "against other textual cues (e.g., sentiment, tone, or semantic consistency). No existing system connects a specific corporate claim to an external, "
        "non-textual, independent observational data stream."
    )
    add_body_p(doc,
        "This thesis directly closes the gap identified by Calamai et al. and Ong et al. by substituting satellite remote sensing observations for the missing "
        "ground-truth labels. Rather than requiring machine learning models to learn greenwashing from non-existent text labels, each company's claims are "
        "audited directly against independently measured physical forest change."
    )
    
    add_heading_2(doc, "2.3 The Regulatory Anchor: EU Deforestation Regulation (EUDR)")
    add_body_p(doc,
        "A critical strength of this research design is its grounding in European Union trade legislation. Regulation (EU) 2023/1115 (EUDR) mandates that "
        "palm oil entering the EU market must be proven deforestation-free. Crucially, the regulation establishes 31 December 2020 as a strict cutoff date: "
        "any commodity linked to land deforested after this date is legally barred from the EU market, irrespective of whether the clearing was permitted under "
        "local domestic law. Anchoring this thesis to the 2020 cutoff establishes an objective, externally mandated benchmark that separates historical land clearing "
        "from ongoing clearing conducted while modern zero-deforestation commitments were actively advertised."
    )

    # --- SECTION 3: SYSTEM ARCHITECTURE & METHODOLOGY ---
    add_heading_1(doc, "3. System Architecture and Methodology")
    
    add_body_p(doc,
        "The auditing pipeline is structured into three distinct stages executed sequentially. The textual claim extraction layer (Layer 1) and the physical "
        "satellite detection layer (Layer 2) operate entirely independently, preventing cross-stream contamination. They converge solely at Layer 3 to compute "
        "the final mismatch score."
    )
    
    # Pipeline Overview Table
    pipe_table = doc.add_table(rows=4, cols=4)
    pipe_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    pipe_table.autofit = False
    pipe_widths = [Inches(1.2), Inches(1.8), Inches(2.0), Inches(1.5)]
    
    pipe_headers = ["Layer", "Input Data", "Methodology / Model", "Output Generated"]
    pipe_rows = [
        ("Layer 1: Claim Extraction", "Corporate Sustainability Reports (PDFs across 11 firms)", "ClimateBERT environmental-claims, specificity classifier, FinBERT", "55 verified claims, continuous specificity & sentiment"),
        ("Layer 2: Forest Loss Detection", "Universal Mill List (UML) coordinates for 290 mills", "Hansen Global Forest Change v1.13, 10 km radial buffer, GEE", "Post-2020 forest loss (ha) and loss % of forest 2000 per mill"),
        ("Layer 3: Mismatch Scoring", "Layer 1 + Layer 2 outputs", "4-Component composite formula weighted to 1.0", "Company mismatch score (0-100) and relative rank (1 to 11)")
    ]
    
    for c_idx, cell in enumerate(pipe_table.rows[0].cells):
        cell.width = pipe_widths[c_idx]
        set_cell_background(cell, HEX_DARK_GREEN)
        set_cell_margins(cell, top=65, bottom=65, left=70, right=70)
        format_cell(cell, pipe_headers[c_idx], bold=True, color=RGBColor(255, 255, 255), font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER)
        
    for r_idx, (l, inp, mth, out) in enumerate(pipe_rows):
        row = pipe_table.rows[r_idx + 1]
        for c_idx, val in enumerate([l, inp, mth, out]):
            cell = row.cells[c_idx]
            cell.width = pipe_widths[c_idx]
            set_cell_background(cell, HEX_LIGHT_BG if r_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, top=60, bottom=60, left=70, right=70)
            format_cell(cell, val, bold=(c_idx == 0), font_size=8.5)
    set_table_borders(pipe_table)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_heading_2(doc, "3.1 Natural Language Processing Pipeline (Layer 1)")
    add_body_p(doc,
        "Sustainability reports from 11 market-leading palm oil conglomerates were processed through a multi-stage NLP pipeline. "
        "Following sentence segmentation and tokenization, candidate sentences were identified using domain-targeted keyword matching "
        "(deforestation, zero-deforestation, peat, land clearing, high conservation value, NDPE, and traceability). "
        "Candidate sentences were then verified using ClimateBERT (climatebert/environmental-claims), a transformer model fine-tuned on the "
        "environmental claims taxonomy of Stammbach et al. (2022). This taxonomy strictly separates genuine corporate assertions from incidental "
        "topical mentions."
    )
    add_body_p(doc,
        "Verified claims were scored along two quantitative dimensions:"
    )
    add_bullet_item(doc, "Claim Specificity",
        "Scored on a continuous 0.0 to 1.0 scale using climatebert/distilroberta-base-climate-specificity. Claims referencing verifiable targets, "
        "precise milestone years, audited mill counts, or spatial monitoring protocols receive high scores (hard commitments), whereas generic "
        "statements of aspiration receive low scores (soft commitments)."
    )
    add_bullet_item(doc, "Claim Sentiment / Promotional Tone",
        "Scored using FinBERT (ProsusAI/finbert). Because sustainability disclosures are framed to persuade financial markets, FinBERT measures "
        "corporate confidence, promotional optimism, and positive self-presentation, directly capturing the rhetorical strength of cheap talk."
    )
    add_body_p(doc,
        "Two descriptive models supplement the pipeline: nbroad/ESG-BERT classifies claims into SASB sustainability categories (confirming that "
        "GHG Emissions and Ecological Impacts dominate the corpus), while ClimateBERT climate-sentiment classifies risk versus opportunity framing."
    )

    add_heading_2(doc, "3.2 Satellite Remote Sensing Pipeline (Layer 2)")
    add_body_p(doc,
        "Physical deforestation monitoring was executed in Google Earth Engine (project thesis-greenwashing) using the Hansen Global Forest Change "
        "dataset, version 1.13 (Hansen et al., 2013). Hansen GFC provides 30-meter pixel resolution derived from Landsat multi-spectral time series, "
        "with each loss pixel assigned an explicit detection year (lossyear)."
    )
    add_body_p(doc,
        "For each of the 290 mills, a 10 km radial buffer was constructed around its verified coordinates. The 10 km buffer approximates a mill's "
        "operational Fresh Fruit Bunch (FFB) sourcing catchment, following the established methodology of PalmWatch (Inclusive Development International). "
        "Within each catchment, tree cover loss was segmented at the EUDR cutoff: loss occurring between 2001 and 2020 (lossyear 1 to 20) was classified "
        "as baseline historical clearing, while loss occurring from 2021 through 2025 (lossyear >= 21) was measured as post-2020 deforestation."
    )

    add_heading_2(doc, "3.3 Supply Chain Mill Matching and Coordinate Integrity")
    add_body_p(doc,
        "Connecting company-level claims to satellite catchments required geolocating processing mills through the Universal Mill List (UML). "
        "Matching conglomerate reporting against public registries revealed critical data engineering challenges that were systematically resolved:"
    )
    add_bullet_item(doc, "UML Coordinate Column Corruption",
        "Raw UML exports contained truncated floating-point values in numeric latitude and longitude columns, shifting mills into the open ocean. "
        "A parsing routine was developed to extract coordinates from the uncorrupted composite 'GPS coordinates' text string, discarding invalid bounds."
    )
    add_bullet_item(doc, "Corporate Ownership Hierarchies (SD Guthrie Correction)",
        "UML records ownership across two fields: 'Group Name' and 'Parent Company'. Searching only Group Name matched only 2 mills for SD Guthrie. "
        "Refactoring the query to search both columns across trading names and subsidiaries expanded the matched set to 42 mills, recovering 142,131 ha "
        "of previously omitted forest loss."
    )
    add_bullet_item(doc, "Unicode Whitespace Standardisation",
        "Non-breaking space characters (\\u00a0) in PDF text caused silent join failures. A regex normalisation routine was deployed alongside "
        "strict regex=False pandas filtering to ensure stable matching across all 11 companies."
    )

    add_heading_2(doc, "3.4 The Canonical Mismatch Scoring Formula")
    add_body_p(doc,
        "The mismatch score operationalizes the divergence between corporate rhetoric and physical reality into a standardized 0 to 100 metric. "
        "The composite score combines four normalized components using weights verified across scripts, unit tests, and thesis chapters:"
    )
    
    add_callout(doc,
        "Mismatch Score = (0.35 * Forest Loss Score) + (0.35 * Specificity Score) + (0.15 * Sentiment Score) + (0.15 * Spatial Match Score)\n\n"
        "Where each component is rescaled to [0, 100] across the 11 companies prior to weighting:\n"
        "• Forest Loss Score (35%): Post-2020 loss as a percentage of year-2000 forest baseline, normalized across companies.\n"
        "• Specificity Score (35%): Mean specificity of extracted claims, where concrete dates, targets, and methods score highest.\n"
        "• Sentiment Score (15%): Mean FinBERT promotional positivity, capturing corporate confidence and self-congratulatory tone.\n"
        "• Spatial Match Score (15%): Percentage of a company's mills exceeding the dataset-wide median loss (2,653 ha per mill).",
        bold_prefix="Canonical Scoring Formula: "
    )

    add_heading_3(doc, "Worked Mathematical Example: Kuala Lumpur Kepong (KLK)")
    add_body_p(doc,
        "To illustrate the exact arithmetic, consider KLK (Rank 1). Across 30 matched mills, KLK recorded 92,209 ha of post-2020 loss, representing "
        "12.18% of its baseline forest cover. Normalized across the company range, its Forest Loss Score is 33.9. KLK published 8 extracted claims "
        "that scored exceptionally high on specificity, yielding a normalized Specificity Score of 100.0. Its claims were phrased with strong promotional "
        "confidence, yielding a normalized Sentiment Score of 68.4. Spatially, 17 of its 30 mills (56.7%) exceeded the dataset median loss, yielding "
        "a Spatial Match Score of 56.7. Applying the canonical equation:"
    )
    add_body_p(doc,
        "Score_KLK = (0.35 * 33.9) + (0.35 * 100.0) + (0.15 * 68.4) + (0.15 * 56.7) = 11.9 + 35.0 + 10.3 + 8.5 = 65.6 (Rank 1)."
    )

    # --- SECTION 4: COMPLETE EMPIRICAL RESULTS ---
    add_heading_1(doc, "4. Complete Empirical Findings and Master Rankings")
    
    add_heading_2(doc, "4.1 Satellite Forest Loss Findings Across 11 Companies")
    add_body_p(doc,
        "Across the 290 matched mills, satellite observation recorded 890,168 hectares of forest clearing between 2021 and 2025. "
        "Golden Agri-Resources (GAR) recorded the largest total loss footprint (171,236 ha across 50 mills), while IOI Corporation recorded the "
        "highest clearing intensity (19.04% of baseline forest lost, averaging 4,959 ha per mill). Table 1 presents the full physical breakdown."
    )
    
    # Table 1: Satellite Loss
    sat_table = doc.add_table(rows=13, cols=6)
    sat_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sat_table.autofit = False
    sat_widths = [Inches(1.5), Inches(0.9), Inches(1.1), Inches(1.1), Inches(0.9), Inches(1.0)]
    
    sat_headers = ["Company", "Mills", "Post-2020 Loss (ha)", "Baseline 2000 (ha)", "Loss %", "Ha / Mill"]
    sat_rows = [
        ("GAR", "50", "171,236", "1,234,420", "13.87%", "3,425"),
        ("SD Guthrie", "42", "142,131", "986,520", "14.41%", "3,384"),
        ("Wilmar", "45", "127,606", "1,119,350", "11.40%", "2,836"),
        ("KLK", "30", "92,209", "757,052", "12.18%", "3,074"),
        ("Astra Agro", "34", "87,198", "810,390", "10.76%", "2,565"),
        ("IOI", "15", "74,385", "390,678", "19.04%", "4,959"),
        ("Musim Mas", "18", "53,060", "463,406", "11.45%", "2,948"),
        ("Genting", "15", "44,362", "382,102", "11.61%", "2,957"),
        ("First Resources", "16", "40,090", "389,602", "10.29%", "2,506"),
        ("Bumitama", "14", "30,549", "352,760", "8.66%", "2,182"),
        ("SIPEF", "11", "27,341", "262,389", "10.42%", "2,486"),
        ("Total / Average", "290", "890,168", "7,148,669", "12.45%", "3,070")
    ]
    
    for c_idx, cell in enumerate(sat_table.rows[0].cells):
        cell.width = sat_widths[c_idx]
        set_cell_background(cell, HEX_DARK_GREEN)
        set_cell_margins(cell, top=60, bottom=60, left=60, right=60)
        align = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.RIGHT
        format_cell(cell, sat_headers[c_idx], bold=True, color=RGBColor(255, 255, 255), font_size=8.5, align=align)
        
    for r_idx, r_data in enumerate(sat_rows):
        row = sat_table.rows[r_idx + 1]
        is_total = (r_idx == len(sat_rows) - 1)
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            cell.width = sat_widths[c_idx]
            bg = HEX_CALLOUT_BG if is_total else (HEX_LIGHT_BG if r_idx % 2 == 1 else "FFFFFF")
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=50, bottom=50, left=60, right=60)
            align = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.RIGHT
            format_cell(cell, val, bold=is_total or (c_idx == 0), font_size=8.5, align=align)
    set_table_borders(sat_table)
    add_caption(doc, "Table 1: Post-2020 forest loss by company within 10 km mill buffers (Hansen GFC v1.13, 2021-2025).")

    add_body_p(doc,
        "Annual aggregation reveals a notable temporal trajectory across the 11 companies: 150,321 ha in 2021; 148,677 ha in 2022; "
        "a severe spike to 217,827 ha in 2023; 198,104 ha in 2024; and 175,239 ha in 2025 (reflecting partial-year data for certain regions). "
        "The 2023 spike was observed across nearly all company catchments, demonstrating that macroeconomic and regional climatic factors "
        "drove elevated clearing even as companies intensified their public marketing of zero-deforestation compliance."
    )

    add_heading_2(doc, "4.2 The Master Mismatch Score Ranking")
    add_body_p(doc,
        "Table 2 provides the final mismatch score ranking alongside all four normalized subcomponents. The results demonstrate that the composite score "
        "is not merely a reflection of raw forest loss or corporate disclosure volume, but captures the specific tension between ambitious claims and physical loss."
    )
    
    # Table 2: Master Mismatch Ranking
    rank_table = doc.add_table(rows=12, cols=7)
    rank_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    rank_table.autofit = False
    rank_widths = [Inches(0.6), Inches(1.6), Inches(1.0), Inches(0.9), Inches(0.8), Inches(0.8), Inches(0.8)]
    
    rank_headers = ["Rank", "Company", "Mismatch", "Forest Loss", "Claim Spec.", "Claim Sent.", "Spatial"]
    rank_rows = [
        ("1", "KLK", "65.6", "33.9", "100.0", "68.4", "56.7"),
        ("2", "GAR", "63.1", "50.2", "67.6", "91.6", "54.0"),
        ("3", "Musim Mas", "56.2", "26.9", "85.1", "63.6", "50.0"),
        ("4", "IOI", "56.1", "100.0", "0.0", "60.3", "80.0"),
        ("5", "SD Guthrie", "55.2", "55.4", "32.9", "100.0", "61.9"),
        ("6", "Wilmar", "50.3", "26.4", "67.2", "70.0", "46.7"),
        ("7", "First Resources", "41.7", "15.7", "75.6", "27.8", "37.5"),
        ("8", "Genting", "39.5", "28.4", "46.6", "41.4", "46.7"),
        ("9", "Bumitama", "38.5", "0.0", "67.1", "71.4", "28.6"),
        ("10", "SIPEF", "26.1", "17.0", "28.3", "41.0", "27.3"),
        ("11", "Astra Agro", "17.6", "20.2", "13.8", "0.0", "38.2")
    ]
    
    for c_idx, cell in enumerate(rank_table.rows[0].cells):
        cell.width = rank_widths[c_idx]
        set_cell_background(cell, HEX_DARK_GREEN)
        set_cell_margins(cell, top=60, bottom=60, left=50, right=50)
        align = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 2] else (WD_ALIGN_PARAGRAPH.LEFT if c_idx == 1 else WD_ALIGN_PARAGRAPH.RIGHT)
        format_cell(cell, rank_headers[c_idx], bold=True, color=RGBColor(255, 255, 255), font_size=8.5, align=align)
        
    for r_idx, r_data in enumerate(rank_rows):
        row = rank_table.rows[r_idx + 1]
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            cell.width = rank_widths[c_idx]
            set_cell_background(cell, HEX_LIGHT_BG if r_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, top=50, bottom=50, left=50, right=50)
            align = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 2] else (WD_ALIGN_PARAGRAPH.LEFT if c_idx == 1 else WD_ALIGN_PARAGRAPH.RIGHT)
            bold = (c_idx in [0, 1, 2])
            format_cell(cell, val, bold=bold, font_size=8.5, align=align)
    set_table_borders(rank_table)
    add_caption(doc, "Table 2: Master Mismatch Score ranking across 11 palm oil companies (normalized subscores 0-100).")

    # --- SECTION 5: IN-DEPTH COMPANY CASE STUDIES ---
    add_heading_1(doc, "5. In-Depth Company Case Studies")
    
    add_heading_2(doc, "5.1 Golden Agri-Resources (GAR) : The Textbook Disconnect (Rank 2, Score 63.1)")
    add_body_p(doc,
        "GAR exemplifies the primary dynamic the mismatch score was engineered to flag. Operating the largest mill network in the study (50 mills), "
        "GAR recorded 171,236 ha of post-2020 forest loss (13.87% of baseline forest), resulting in a high Forest Loss score of 50.2. "
        "Over half of its mills (54.0%) exceed the dataset severity median. In its sustainability disclosures, GAR published 40 extracted claims "
        "featuring the highest promotional sentiment score in the entire industry (91.6), advertising 99.8% traceability to plantation and explicit NDPE "
        "compliance targets. The direct juxtaposition of glowing corporate confidence with the largest physical deforestation footprint in the sector "
        "positions GAR at Rank 2."
    )
    
    img_gar_map = r"C:\Users\Allah o akbar\thesis\latex\figures\gar_nagasakti_clearing_map.png"
    add_image_safe(doc, img_gar_map, "Figure 1: High-resolution Sentinel-2 comparative clearing map for GAR's highest-loss mill, NAGA SAKTI in Riau (10,197 ha post-2020 loss). Left: 2019 baseline; Right: 2024 composite with Hansen loss overlays.")

    img_gar_loss = r"C:\Users\Allah o akbar\thesis\latex\figures\gar_forestloss.png"
    add_image_safe(doc, img_gar_loss, "Figure 2: Forest loss distribution across GAR's 50 matched mill catchments. Green indicates 2000 forest baseline; red indicates post-2020 loss.")

    add_heading_2(doc, "5.2 IOI Corporation : The Severe Clearing Hotspot Masked by Vague Language (Rank 4, Score 56.1)")
    add_body_p(doc,
        "IOI Corporation presents the most intense physical deforestation footprint in the dataset. Across its 15 mills in Sabah and Kalimantan, "
        "IOI lost 74,385 ha of forest, averaging an extraordinary 4,959 ha per mill and 19.04% of its baseline forest, earning a maximum Forest Loss "
        "Score of 100.0. Spatially, 80% of IOI's mills exceed the severity threshold. Furthermore, IOI's clearing escalated continuously from 10,115 ha "
        "in 2021 to 20,359 ha in 2024, doubling over four years."
    )
    add_body_p(doc,
        "Despite having the worst physical record, IOI ranks 4th rather than 1st. The explanation lies in its textual claims: while IOI published 66 claims "
        "(the highest count in the study), its language was completely devoid of specific dates, mill targets, or audit figures, assigning it a Specificity "
        "Score of 0.0. Under the four-component formula, vague reporting limits the degree of verifiable contradiction. Had IOI claimed specific targets "
        "with a specificity score of 100, its composite mismatch score would have reached 91.1."
    )
    
    img_ioi_map = r"C:\Users\Allah o akbar\thesis\latex\figures\ioi_syarimo_clearing_map.png"
    add_image_safe(doc, img_ioi_map, "Figure 3: Sentinel-2 clearing map for IOI's SYARIMO mill in Sabah, Malaysia (12,318 ha post-2020 loss, the highest single-mill loss in the study).")

    img_ioi_loss = r"C:\Users\Allah o akbar\thesis\latex\figures\ioi_forestloss.png"
    add_image_safe(doc, img_ioi_loss, "Figure 4: Post-2020 forest loss across IOI's 15 matched mill catchments in Sabah and Kalimantan (4,959 ha per mill average).")

    add_heading_2(doc, "5.3 Astra Agro Lestari : The Paradox of Strategic Silence (Rank 11, Score 17.6)")
    add_body_p(doc,
        "Astra Agro Lestari ranks last on the mismatch score (17.6), yet it accounts for the 5th-largest physical loss footprint in the dataset "
        "(87,198 ha across 34 mills, exceeding Musim Mas, Genting, First Resources, Bumitama, and SIPEF). External investigations by Mongabay and "
        "Genesis Bengkulu document severe real-world violations, including 17,664 ha of subsidiary concessions overlapping state forest zones, operations "
        "without required permits, and contested land conflicts covering 6,700 ha."
    )
    add_body_p(doc,
        "Astra Agro's low score stems from its disclosure strategy: its claims have near-floor specificity (13.8) and the lowest sentiment score in the "
        "industry (0.0). Astra Agro adopts a stance of strategic silence, publishing flat, legalistic, minimal statements. Because the mismatch score "
        "specifically measures the contradiction between claims and physical outcomes, a company that makes minimal commitments provides little for the "
        "satellite data to contradict. This exposes a vital structural insight: the mismatch score measures claim-evidence divergence, not absolute environmental harm."
    )

    img_astra_map = r"C:\Users\Allah o akbar\thesis\latex\figures\astraagro_gunungsejahtera_clearing_map.png"
    add_image_safe(doc, img_astra_map, "Figure 5: Sentinel-2 clearing map for Astra Agro's GUNUNG SEJAHTERA IBU PERTIWI mill (6,806 ha post-2020 loss).")

    img_astra_loss = r"C:\Users\Allah o akbar\thesis\latex\figures\astraagro_forestloss.png"
    add_image_safe(doc, img_astra_loss, "Figure 6: Forest loss across Astra Agro's 34 matched mill catchments, concentrated primarily in Sulawesi.")

    add_heading_2(doc, "5.4 Wilmar International : Sustained Annual Clearing at Sabahmas (Rank 6, Score 50.3)")
    add_body_p(doc,
        "Wilmar, the world's largest palm oil processor, recorded 127,606 ha of post-2020 loss across 45 mills. At its Sabahmas mill in Sabah, Malaysia, "
        "the satellite pipeline identified continuous clearing across all five monitoring years (2021-2025), totaling 6,675 ha. Unlike mills characterized "
        "by single clearing pulses, Sabahmas exhibits unbroken industrial clearing postdating Wilmar's public zero-deforestation commitments."
    )

    img_wilmar_map = r"C:\Users\Allah o akbar\thesis\latex\figures\wilmar_sabahmas_clearing_map.png"
    add_image_safe(doc, img_wilmar_map, "Figure 7: Sentinel-2 clearing map for Wilmar's SABAHMAS mill in Sabah, Malaysia (6,675 ha post-2020 loss across 2021-2025).")

    add_heading_2(doc, "5.5 Kuala Lumpur Kepong (KLK) : The High-Specificity Divergence (Rank 1, Score 65.6)")
    add_body_p(doc,
        "KLK tops the mismatch ranking at 65.6. Across 30 matched mills, KLK recorded 92,209 ha of post-2020 loss (12.18% of forest baseline). "
        "Its top ranking is driven by its textual profile: its 8 extracted claims scored a perfect 100.0 on normalized specificity, featuring explicit "
        "third-party satellite audit commitments and precise NDPE benchmarks. Positioning such explicit commitments against 92,209 ha of loss triggers "
        "the highest mismatch penalty in the model."
    )

    img_klk_map = r"C:\Users\Allah o akbar\thesis\latex\figures\klk_bornion_clearing_map.png"
    add_image_safe(doc, img_klk_map, "Figure 8: Sentinel-2 clearing map for KLK's BORNION mill in Sabah, Malaysia (6,768 ha post-2020 loss).")

    img_klk_loss = r"C:\Users\Allah o akbar\thesis\latex\figures\klk_forestloss.png"
    add_image_safe(doc, img_klk_loss, "Figure 9: Forest loss across KLK's 30 matched mill catchments in Peninsular Malaysia, Sabah, and Kalimantan.")

    add_heading_2(doc, "5.6 Profiles of Remaining Sampled Conglomerates")
    add_bullet_item(doc, "Musim Mas (Rank 3, Score 56.2)",
        "Recorded 53,060 ha of loss across 18 mills (11.45% of forest baseline). Musim Mas combined high claim specificity (85.1) with moderate "
        "promotional sentiment (63.6), placing third overall."
    )
    add_bullet_item(doc, "SD Guthrie (Rank 5, Score 55.2)",
        "Formerly Sime Darby Plantation, SD Guthrie operates 42 mills with 142,131 ha of post-2020 loss (14.41% of forest baseline, the second-largest "
        "loss total). SD Guthrie recorded the highest raw sentiment score (100.0) but moderate specificity (32.9), placing fifth."
    )
    add_bullet_item(doc, "First Resources (Rank 7, Score 41.7)",
        "Recorded 40,090 ha across 16 mills (10.29% of forest baseline). High claim specificity (75.6) was balanced by low sentiment (27.8) and low "
        "forest loss scores (15.7)."
    )
    add_bullet_item(doc, "Genting Plantations (Rank 8, Score 39.5)",
        "Recorded 44,362 ha across 15 mills (11.61% of forest baseline). Genting displayed balanced, mid-tier scores across all four components."
    )
    add_bullet_item(doc, "Bumitama Agri (Rank 9, Score 38.5)",
        "Recorded 30,549 ha across 14 mills (8.66% of forest baseline, the lowest loss percentage in the study, earning 0.0 on normalized loss). "
        "Its mismatch score was driven primarily by high claim specificity (67.1) and sentiment (71.4)."
    )
    add_bullet_item(doc, "SIPEF (Rank 10, Score 26.1)",
        "Recorded 27,341 ha across 11 mills in Sumatra and Papua New Guinea (10.42% of baseline). SIPEF recorded low claim specificity (28.3) "
        "and low spatial severity (27.3%), placing 10th."
    )

    # --- SECTION 6: SUPPLEMENTARY VALIDATIONS ---
    add_heading_1(doc, "6. Multi-Sensor Cross-Validations and External Benchmarks")
    
    add_heading_2(doc, "6.1 RADD SAR Radar Disturbance Cross-Validation")
    add_body_p(doc,
        "To validate optical Hansen detections against sensor technologies unaffected by persistent tropical clouds, Sentinel-1 Synthetic Aperture "
        "Radar (SAR) disturbance alerts from Wageningen University's RADD system were queried for the highest-loss mill across five companies. "
        "RADD confirmed radar disturbance anomalies at 4 of the 5 mills tested (GAR Naga Sakti: 6.72 ha; IOI Syarimo: 12.45 ha; KLK Bornion: 39.55 ha; "
        "SD Guthrie Giram Sou 29: 15.37 ha). At Wilmar's Sabahmas mill, zero RADD alerts were registered despite 6,675 ha of Hansen loss, reflecting "
        "RADD's calibration toward rapid clear-cut events rather than the gradual canopy thinning observed at Sabahmas."
    )

    add_heading_2(doc, "6.2 Land Cover Conversion to Oil Palm (Descals et al., 2021)")
    add_body_p(doc,
        "A critical defense raised by mill operators is that near-mill forest loss might stem from external activities unrelated to oil palm. "
        "To test this, the 10-meter global oil palm classification map of Descals et al. (2021) was overlaid onto post-2020 loss pixels across all 290 mills. "
        "Across the entire dataset, 56.0% of post-2020 forest loss inside the 10 km buffers was classified as oil palm (44.0% industrial plantation). "
        "For IOI Corporation, an astonishing 89.8% of buffer loss was converted to oil palm (87.3% industrial), conclusively refuting alternative explanations."
    )

    add_heading_2(doc, "6.3 Buffer Distance Sensitivity Analysis (5 km to 30 km)")
    add_body_p(doc,
        "To test whether the 10 km buffer distance arbitrary influences company rankings, loss was evaluated across five radial distances (5, 10, 15, 20, "
        "and 30 km) for representative mills. Company rank correlations between adjacent buffers remained exceptionally stable (Spearman rho = 0.80 between "
        "10 and 15 km; 0.90 between 15 and 20 km; 0.96 between 20 and 30 km). At 30 km, the catchment encompasses 2,827 sq km, introducing unrelated "
        "third-party landscape noise, confirming 10 km as the optimal balance between operational catchment capture and spatial attribution."
    )

    add_heading_2(doc, "6.4 Foundation Model Evaluation: IBM-NASA Prithvi-EO-2.0 Across 290 Mills")
    add_body_p(doc,
        "To evaluate emerging AI foundation models, the 300M-parameter Prithvi-EO-2.0 vision transformer was deployed across all 290 mills without "
        "deforestation fine-tuning. Sentinel-2 temporal patch embeddings (2019 baseline vs 2024 composite) were compared via cosine dissimilarity. "
        "Across the network, Prithvi achieved a positive mean rank correlation of rho = 0.172 and mean IoU of 0.086 against Hansen loss masks, "
        "demonstrating that self-supervised geospatial representations capture directional deforestation patterns zero-shot across varied tropical biomes."
    )

    add_heading_2(doc, "6.5 NLP Model Domain Benchmarking (150-Sentence Gold Set)")
    add_body_p(doc,
        "Evaluation against 150 manually annotated domain sentences confirmed the technical superiority of fine-tuned transformers over baselines. "
        "The environmental-claims model achieved 97.3% accuracy and 0.981 F1 (vs 70.7% accuracy for keyword filtering). FinBERT achieved 81.1% accuracy "
        "for promotional tone (vs 50.9% for ClimateBERT climate-sentiment, which classified 99.8% of sentences as neutral/opportunity). "
        "ESG-BERT achieved 80.2% accuracy in SASB topic classification (vs 18.9% for keyword tagging)."
    )

    # --- SECTION 7: DATA ENGINEERING & PIPELINE OBSTACLES ---
    add_heading_1(doc, "7. Data Engineering Challenges and Problem Resolutions (108 Hours Audit)")
    add_body_p(doc,
        "Constructing this empirical pipeline required resolving complex data corruptions and computational bottlenecks across geospatial clouds "
        "and corporate disclosures. Table 3 documents the technical problem log, root causes, implemented fixes, and engineering effort (108 hours total)."
    )
    
    # Table 3: Engineering Log
    eng_table = doc.add_table(rows=12, cols=4)
    eng_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    eng_table.autofit = False
    eng_widths = [Inches(1.5), Inches(2.2), Inches(2.0), Inches(0.8)]
    
    eng_headers = ["Pipeline Area", "Problem Encountered", "Technical Resolution", "Hours"]
    eng_rows = [
        ("UML Mill Coordinates", "Numeric lat/lon columns corrupted in raw CSV export", "Parsed uncorrupted composite string and enforced bounding box", "4"),
        ("Corporate Matching", "SD Guthrie undercounted at 2 mills (subsidiary masking)", "Engineered dual-column search across Group Name and Parent Company", "5"),
        ("Text Normalisation", "Non-breaking spaces (\\u00a0) caused silent join failures", "Implemented regex whitespace collapsing and regex=False filtering", "3"),
        ("GEE Spatial Extraction", "10^7 pixel quota exceeded; headless OAuth timeouts", "Configured maxPixels=10^10, scale=30m, dedicated venv, disk caching", "12"),
        ("NLP Model Divergence", "FinBERT and ClimateBERT agreed on only 53.1% (kappa=0.08)", "Analyzed distributions; retained FinBERT for tone; documented divergence", "6"),
        ("Gold Evaluation Set", "No domain-specific palm oil claim benchmark existed", "Stratified manual labeling of 150 sentences across 4 tasks", "10"),
        ("Production Metrics", "Inconsistent corporate reporting (CPO vs FFB vs sales)", "Formally dropped production theory to eliminate defense vulnerability", "8"),
        ("Sentinel-2 Maps", "Tropical cloud and haze degradation across 290 mills", "Applied dynamic percentile contrast stretching (1.5% to 98.5%)", "14"),
        ("Prithvi Scaling", "Local CPU constraints for 300M parameter model", "Engineered Google Colab GPU batch pipeline for all 290 mills", "12"),
        ("Cross-Validations", "Attribution gap in circular mill buffers", "Executed Descals 10m overlay, RADD SAR, and buffer sensitivity", "10"),
        ("Scoring & Regression", "Asserted sum of weights = 1.0; zero-division safety", "Developed 23-test regression suite under pytest (all passing)", "4"),
    ]
    
    for c_idx, cell in enumerate(eng_table.rows[0].cells):
        cell.width = eng_widths[c_idx]
        set_cell_background(cell, HEX_DARK_GREEN)
        set_cell_margins(cell, top=60, bottom=60, left=50, right=50)
        align = WD_ALIGN_PARAGRAPH.RIGHT if c_idx == 3 else WD_ALIGN_PARAGRAPH.LEFT
        format_cell(cell, eng_headers[c_idx], bold=True, color=RGBColor(255, 255, 255), font_size=8.5, align=align)
        
    for r_idx, r_data in enumerate(eng_rows):
        row = eng_table.rows[r_idx + 1]
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            cell.width = eng_widths[c_idx]
            set_cell_background(cell, HEX_LIGHT_BG if r_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, top=50, bottom=50, left=50, right=50)
            align = WD_ALIGN_PARAGRAPH.RIGHT if c_idx == 3 else WD_ALIGN_PARAGRAPH.LEFT
            format_cell(cell, val, bold=(c_idx == 0), font_size=8.5, align=align)
    set_table_borders(eng_table)
    add_caption(doc, "Table 3: Technical engineering problem log, corrective actions, and invested development hours (108 hours total).")

    # --- SECTION 8: DISCUSSION & POLICY IMPLICATIONS ---
    add_heading_1(doc, "8. Critical Discussion and Policy Implications")
    
    add_heading_2(doc, "8.1 Universality of Loss and EUDR Due-Diligence Enforcement")
    add_body_p(doc,
        "A foundational finding of this thesis is the universality of near-mill forest loss: 100% of the 290 mills in the dataset recorded post-2020 loss. "
        "This carries profound implications for European Union Deforestation Regulation (EUDR) enforcement. Regulatory compliance strategies that focus "
        "on blacklisting an isolated handful of 'bad actors' are built on a fundamentally flawed premise. Near-mill deforestation is an industry-wide "
        "structural condition. Compliance enforcement must require full supply chain traceability back to the specific plot of cultivation rather than "
        "relying on company-level certifications or brand declarations."
    )

    add_heading_2(doc, "8.2 Corporate Disclosure Volume as an Unreliable Proxy")
    add_body_p(doc,
        "The empirical findings demonstrate that corporate claim volume and rhetorical confidence are virtually uncorrelated with physical compliance. "
        "Companies publishing high-volume, highly optimistic reports (e.g., GAR and SD Guthrie) operate mill catchments characterized by severe, widespread "
        "deforestation. Conversely, firms exhibiting minimal disclosure (e.g., Astra Agro) often conceal extensive operational violations. "
        "Regulators and ESG rating agencies that treat voluntary sustainability disclosures as evidence of risk mitigation risk reinforcing corporate greenwashing."
    )

    # --- SECTION 9: LIMITATIONS & REPRODUCIBILITY ---
    add_heading_1(doc, "9. Methodological Limitations and Reproducibility")
    
    add_heading_2(doc, "9.1 Methodological Limitations")
    add_bullet_item(doc, "Proximity vs Causal Attribution",
        "A 10 km buffer measures spatial proximity, not direct causal legal attribution. Forest clearing within a catchment may be conducted by third-party "
        "smallholders, neighboring concessions, or infrastructure developers. While Descals land cover confirms 56% conversion to oil palm, parcel-level "
        "cadastral maps are required for legal liability determination."
    )
    add_bullet_item(doc, "Variable Claim Sample Sizes",
        "Extracted claim counts range from 4 (Wilmar) and 8 (KLK) to 66 (IOI). Smaller samples are more sensitive to individual sentence formulations. "
        "Low sample flags are explicitly preserved in the data pipeline."
    )
    add_bullet_item(doc, "Structural Vulnerability to Low Disclosure",
        "Because the mismatch score measures contradiction between language and evidence, quiet firms (Astra Agro) receive lower mismatch scores despite "
        "severe physical clearing, requiring raw loss tables to be reviewed alongside composite rankings."
    )

    add_heading_2(doc, "9.2 Software Stack, Reproducibility, and Regression Suite")
    add_body_p(doc,
        "The entire thesis codebase is automated, modular, and fully reproducible. All satellite reductions are scripted in Google Earth Engine "
        "API v1.5.0, NLP inference runs via PyTorch and Hugging Face transformers, and statistical scoring scripts execute synchronously. "
        "A 23-test regression suite under pytest asserts image integrity, mill matching disjunctions, coordinate bounds, and scoring weight sums (sum = 1.0). "
        "All 23 tests pass synchronously in under three seconds on local hardware."
    )

    # Save Document
    doc.save(output_path)
    print(f"Document successfully created and saved at: {output_path}")

if __name__ == "__main__":
    out_file = r"C:\Users\Allah o akbar\thesis\Catching_Greenwashing_from_Space_Thesis_Overview.docx"
    build_full_document(out_file)
