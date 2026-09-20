"""UML mill matching + coordinate parsing. Pure functions, no I/O, no Earth Engine."""
import pandas as pd

COMPANY_KEYWORDS = {
    "wilmar": "WILMAR",
    "gar": "GOLDEN AGRI|SINAR MAS",
    "sdguthrie": "SIME DARBY|GUTHRIE",
    "musimmas": "MUSIM MAS",
    "ioi": "IOI CORPORATION|IOI GROUP",
    "klk": "KUALA.?LUMPUR.?KEPONG",
    "bumitama": "BUMITAMA",
    "astraagro": "ASTRA AGRO",
    "gentingplantations": "GENTING PLANTATIONS",
    "sipef": "SIPEF",
    "firstresources": "FIRST RESOURCES",
    # "apical" skipped: no mills in UML (trading/refining arm, not a grower)
}


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [" ".join(str(c).replace("﻿", "").split()) for c in df.columns]
    return df


def normalize_text(series: pd.Series) -> pd.Series:
    """Collapse all whitespace variants (incl. non-breaking space \\xa0) to a single
    regular space. The UML has ~95 rows with \\xa0 inside Group Name / Parent Company
    (e.g. "GENTING\\xa0PLANTATIONS"), which silently fails a literal-space regex match.

    Uses an explicit \\xa0 -> space replace (regex=False) because pandas' str.replace
    with a raw r"\\s+" pattern string does NOT treat \\xa0 as whitespace here (unlike
    Python's own re.sub) -- only a precompiled regex does. Explicit replace sidesteps
    that pandas quirk entirely.
    """
    cleaned = series.fillna("").str.replace("\xa0", " ", regex=False)
    return cleaned.str.replace(r" +", " ", regex=True).str.strip()


def match_mills(uml: pd.DataFrame, company_keyword: str, group_col="Group Name",
                 parent_col="Parent Company") -> pd.DataFrame:
    """Rows whose Group Name OR Parent Company matches the keyword, with numeric lat/lon.

    Matching against both columns catches subsidiaries only linked via Parent
    Company (e.g. Sime Darby mills listed under local operator names).
    Rows with missing/unparseable GPS coordinates are dropped.
    """
    group_norm = normalize_text(uml[group_col])
    parent_norm = normalize_text(uml[parent_col])
    mask = (
        group_norm.str.contains(company_keyword, case=False, na=False, regex=True) |
        parent_norm.str.contains(company_keyword, case=False, na=False, regex=True)
    )
    matched = uml[mask].reset_index(drop=True)
    coords = matched["GPS coordinates"].str.split(",", expand=True)
    mill_coords = matched[[group_col, "Mill Name"]].copy()
    if coords.shape[1] >= 2:
        mill_coords["latitude"] = pd.to_numeric(coords[0].str.strip(), errors="coerce")
        mill_coords["longitude"] = pd.to_numeric(coords[1].str.strip(), errors="coerce")
    else:
        mill_coords["latitude"] = pd.NA
        mill_coords["longitude"] = pd.NA
    mill_coords = mill_coords.dropna(subset=["latitude", "longitude"]).reset_index(drop=True)
    return mill_coords
