import pandas as pd
import pytest

from mill_matching import COMPANY_KEYWORDS, clean_columns, match_mills, normalize_text


def _uml(rows):
    return pd.DataFrame(rows, columns=["Group Name", "Parent Company", "Mill Name", "GPS coordinates"])


def test_match_by_group_name():
    uml = _uml([
        ["WILMAR INTERNATIONAL", "", "Mill A", "1.5, 103.2"],
        ["OTHER CO", "", "Mill B", "2.0, 104.0"],
    ])
    out = match_mills(uml, "WILMAR")
    assert list(out["Mill Name"]) == ["Mill A"]


def test_match_by_parent_company_only():
    """Subsidiary mills only linked via Parent Company must still match."""
    uml = _uml([
        ["LOCAL OPERATOR SDN BHD", "SIME DARBY PLANTATION", "Mill C", "3.1, 101.5"],
    ])
    out = match_mills(uml, "SIME DARBY|GUTHRIE")
    assert list(out["Mill Name"]) == ["Mill C"]


def test_case_insensitive_regex():
    uml = _uml([["sipef group", "", "Mill D", "-1.2, 110.0"]])
    out = match_mills(uml, "SIPEF")
    assert len(out) == 1


def test_drops_rows_with_missing_coordinates():
    uml = _uml([
        ["WILMAR", "", "Mill E", ""],
        ["WILMAR", "", "Mill F", "1.0, 2.0"],
    ])
    out = match_mills(uml, "WILMAR")
    assert list(out["Mill Name"]) == ["Mill F"]


def test_drops_rows_with_malformed_coordinates():
    uml = _uml([
        ["WILMAR", "", "Mill G", "not-a-coordinate"],
        ["WILMAR", "", "Mill H", "1.0, 2.0"],
    ])
    out = match_mills(uml, "WILMAR")
    assert list(out["Mill Name"]) == ["Mill H"]


def test_no_match_returns_empty_frame():
    uml = _uml([["WILMAR", "", "Mill I", "1.0, 2.0"]])
    out = match_mills(uml, "NONEXISTENT_COMPANY")
    assert len(out) == 0


def test_clean_columns_strips_bom_and_whitespace():
    df = pd.DataFrame(columns=["﻿Group  Name", " Mill Name "])
    out = clean_columns(df)
    assert list(out.columns) == ["Group Name", "Mill Name"]


def test_gar_keyword_matches_sinar_mas_trading_name():
    """Regression: GAR's UML Group Name is "SINAR MAS", not "GOLDEN AGRI" or "SMART".

    An earlier keyword ("GOLDEN AGRI|SMART") silently matched almost nothing (3 of 50
    real mills) because "SMART" never appears as a literal substring in the UML data
    ("SINAR MAS AGRO RESOURCES AND TECHNOLOGY" contains no contiguous "SMART"). Any
    future keyword change must keep catching Sinar Mas mills.
    """
    uml = _uml([
        ["SINAR MAS", "SINAR MAS AGRO RESOURCES AND TECHNOLOGY", "Mill X", "0.5, 101.0"],
        ["ROYAL GOLDEN EAGLE", "INTI INDOSAWIT SUBUR", "Mill Y", "0.6, 101.1"],
    ])
    out = match_mills(uml, COMPANY_KEYWORDS["gar"])
    assert list(out["Mill Name"]) == ["Mill X"]


def test_normalize_text_collapses_nonbreaking_space():
    """Regression: ~95 UML rows use \\xa0 (non-breaking space) inside Group Name /
    Parent Company, e.g. "SIME\\xa0DARBY" -- 64 of 65 Sime Darby rows used this, and a
    literal-space keyword silently matched only 1 of them (42 mills instead of 66)."""
    s = pd.Series(["SIME\xa0DARBY", "GENTING\xa0PLANTATIONS", None])
    out = normalize_text(s)
    assert out.tolist() == ["SIME DARBY", "GENTING PLANTATIONS", ""]


def test_match_mills_finds_nonbreaking_space_variant():
    uml = _uml([
        ["SIME\xa0DARBY", "", "Mill NBSP", "1.0, 2.0"],
        ["SIME DARBY", "", "Mill Regular", "1.1, 2.1"],
    ])
    out = match_mills(uml, "SIME DARBY")
    assert set(out["Mill Name"]) == {"Mill NBSP", "Mill Regular"}


def test_royal_golden_eagle_is_not_matched_as_gar():
    """Royal Golden Eagle (Tanoto family / APRIL) is a different company from
    Golden Agri-Resources (Widjaja family / GAR) despite the similar-sounding name."""
    uml = _uml([["ROYAL GOLDEN EAGLE", "INTI INDOSAWIT SUBUR", "Mill Z", "1.0, 102.0"]])
    out = match_mills(uml, COMPANY_KEYWORDS["gar"])
    assert len(out) == 0
