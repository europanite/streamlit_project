from pathlib import Path

import pandas as pd
import pytest

from app.main import (
    apply_numeric_range_filter,
    apply_text_filter,
    dataframe_to_csv_bytes,
    load_csv_from_text,
    load_sample_csv,
    numeric_columns,
    profile_as_dataframe,
    profile_columns,
)


def test_load_csv_from_text_returns_dataframe():
    df = load_csv_from_text("name,score\nalpha,10\nbeta,20\n")

    assert list(df.columns) == ["name", "score"]
    assert len(df) == 2


def test_load_csv_from_text_rejects_empty_text():
    with pytest.raises(ValueError):
        load_csv_from_text("   ")


def test_load_sample_csv():
    df = load_sample_csv(Path("/data/sample.csv"))

    assert not df.empty
    assert "revenue" in df.columns


def test_profile_columns_reports_missing_values():
    df = pd.DataFrame({"a": [1, None], "b": ["x", "x"]})

    profiles = profile_columns(df)

    assert profiles[0].name == "a"
    assert profiles[0].missing_count == 1
    assert profiles[0].missing_rate == 0.5
    assert profiles[1].unique_count == 1


def test_profile_as_dataframe_has_expected_columns():
    df = pd.DataFrame({"a": [1, 2]})

    profile_df = profile_as_dataframe(df)

    assert list(profile_df.columns) == [
        "column",
        "dtype",
        "missing_count",
        "missing_rate",
        "unique_count",
    ]


def test_numeric_columns_returns_only_numbers():
    df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})

    assert numeric_columns(df) == ["a"]


def test_apply_text_filter_is_case_insensitive():
    df = pd.DataFrame({"city": ["Yokosuka", "Miura", "Kamakura"]})

    filtered = apply_text_filter(df, "city", "yoko")

    assert filtered["city"].tolist() == ["Yokosuka"]


def test_apply_numeric_range_filter():
    df = pd.DataFrame({"score": [10, 20, 30]})

    filtered = apply_numeric_range_filter(df, "score", 15, 25)

    assert filtered["score"].tolist() == [20]


def test_dataframe_to_csv_bytes():
    df = pd.DataFrame({"a": [1]})

    assert dataframe_to_csv_bytes(df) == b"a\n1\n"
