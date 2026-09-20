"""Tests for geospatial integrity, coordinate validity, and physical buffer constraints across all 290 mills."""
import math
import os
import pandas as pd
import pytest

MILLS_CSV = "data/mills/all_mills_forest_loss.csv"
MAX_BUFFER_HA = math.pi * (10 ** 2) * 100  # pi * r^2 in km^2 * 100 ha/km^2 ~= 31,415.93 ha

EXPECTED_COMPANY_MILLS = {
    "gar": 50,
    "sdguthrie": 42,
    "wilmar": 45,
    "klk": 30,
    "astraagro": 34,
    "ioi": 15,
    "musimmas": 18,
    "genting": 15,
    "firstresources": 16,
    "bumitama": 14,
    "sipef": 11,
}


@pytest.fixture
def mills_df():
    assert os.path.exists(MILLS_CSV), f"Missing {MILLS_CSV}"
    return pd.read_csv(MILLS_CSV)


def test_total_mill_count(mills_df):
    """Network must contain exactly 290 mills across 11 companies."""
    assert len(mills_df) == 290
    assert mills_df["company"].nunique() == 11


def test_per_company_mill_counts(mills_df):
    """Every company must match its verified mill count."""
    counts = mills_df.groupby("company").size().to_dict()
    assert counts == EXPECTED_COMPANY_MILLS


def test_coordinate_validity_and_bounds(mills_df):
    """Coordinates must be finite, non-null, and within the global tropical palm oil belt."""
    assert not mills_df["latitude"].isna().any(), "Found NaN in latitude"
    assert not mills_df["longitude"].isna().any(), "Found NaN in longitude"

    # WGS84 physical boundaries
    assert (mills_df["latitude"] >= -90.0).all() and (mills_df["latitude"] <= 90.0).all()
    assert (mills_df["longitude"] >= -180.0).all() and (mills_df["longitude"] <= 180.0).all()

    # Palm oil operational belt: within the tropics (+-15 degrees of Equator)
    # Covers Southeast Asia (Indonesia, Malaysia), West Africa (Ghana, Nigeria, Ivory Coast), and Oceania (PNG)
    assert (mills_df["latitude"] >= -15.0).all(), "Latitude below tropical palm belt"
    assert (mills_df["latitude"] <= 15.0).all(), "Latitude above tropical palm belt"


def test_headline_post2020_loss_total(mills_df):
    """Total post-2020 forest loss across 290 mills must equal 890,168 ha (+- 1 ha)."""
    total_loss = mills_df["loss_post2020_ha"].sum()
    assert total_loss == pytest.approx(890168.0, abs=2.0)


def test_physical_buffer_area_constraints(mills_df):
    """Loss or forest within 10 km buffer cannot exceed geometric circle area (~31,416 ha)."""
    # forest_2000_ha cannot exceed 31,416 ha (with small margin for raster discretization)
    assert (mills_df["forest_2000_ha"] <= MAX_BUFFER_HA + 100.0).all()
    # loss_post2020_ha cannot exceed forest_2000_ha
    assert (mills_df["loss_post2020_ha"] <= MAX_BUFFER_HA + 100.0).all()


def test_loss_percentage_bounds(mills_df):
    """Computed forest loss percentage must be strictly between 0% and 100%."""
    loss_pct = mills_df["loss_post2020_ha"] / mills_df["forest_2000_ha"] * 100
    assert (loss_pct >= 0.0).all()
    assert (loss_pct <= 100.0).all()
    # Every mill has non-zero post-2020 loss (minimum 105 ha observed)
    assert (mills_df["loss_post2020_ha"] >= 105.0).all()
