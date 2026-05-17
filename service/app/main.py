from __future__ import annotations

from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import Iterable

import pandas as pd


SAMPLE_CSV_PATH = Path("/data/sample.csv")


@dataclass(frozen=True)
class ColumnProfile:
    name: str
    dtype: str
    missing_count: int
    missing_rate: float
    unique_count: int


def load_csv_from_text(csv_text: str) -> pd.DataFrame:
    """Load CSV text into a DataFrame.

    This function is intentionally independent from Streamlit so it can be tested
    in a normal pytest environment.
    """
    if not csv_text.strip():
        raise ValueError("CSV text is empty.")

    return pd.read_csv(StringIO(csv_text))


def load_sample_csv(path: Path = SAMPLE_CSV_PATH) -> pd.DataFrame:
    """Load the bundled sample CSV."""
    return pd.read_csv(path)


def profile_columns(df: pd.DataFrame) -> list[ColumnProfile]:
    """Return a compact profile for every column."""
    if df.empty:
        return []

    row_count = len(df)
    profiles: list[ColumnProfile] = []

    for column in df.columns:
        missing_count = int(df[column].isna().sum())
        profiles.append(
            ColumnProfile(
                name=str(column),
                dtype=str(df[column].dtype),
                missing_count=missing_count,
                missing_rate=missing_count / row_count,
                unique_count=int(df[column].nunique(dropna=True)),
            )
        )

    return profiles


def profile_as_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Return column profiles as a display-ready DataFrame."""
    return pd.DataFrame(
        [
            {
                "column": item.name,
                "dtype": item.dtype,
                "missing_count": item.missing_count,
                "missing_rate": round(item.missing_rate, 4),
                "unique_count": item.unique_count,
            }
            for item in profile_columns(df)
        ]
    )


def numeric_columns(df: pd.DataFrame) -> list[str]:
    """Return numeric column names."""
    return [str(column) for column in df.select_dtypes(include="number").columns]


def categorical_columns(df: pd.DataFrame) -> list[str]:
    """Return non-numeric column names."""
    return [str(column) for column in df.select_dtypes(exclude="number").columns]


def apply_text_filter(df: pd.DataFrame, column: str, query: str) -> pd.DataFrame:
    """Filter rows by case-insensitive substring match."""
    if not query:
        return df

    if column not in df.columns:
        raise KeyError(f"Column not found: {column}")

    mask = df[column].astype(str).str.contains(query, case=False, na=False)
    return df[mask]


def apply_numeric_range_filter(
    df: pd.DataFrame,
    column: str,
    minimum: float | None,
    maximum: float | None,
) -> pd.DataFrame:
    """Filter rows by numeric range."""
    if column not in df.columns:
        raise KeyError(f"Column not found: {column}")

    filtered = df
    if minimum is not None:
        filtered = filtered[filtered[column] >= minimum]
    if maximum is not None:
        filtered = filtered[filtered[column] <= maximum]
    return filtered


def dataframe_to_csv_bytes(df: pd.DataFrame) -> bytes:
    """Serialize a DataFrame to UTF-8 CSV bytes."""
    return df.to_csv(index=False).encode("utf-8")


def _first(items: Iterable[str]) -> str | None:
    for item in items:
        return item
    return None


def run_app() -> None:
    """Run the Streamlit UI."""
    import streamlit as st

    st.set_page_config(page_title="Streamlit CSV Explorer", page_icon="📊", layout="wide")
    st.title("📊 Streamlit CSV Explorer")
    st.caption("Upload a CSV file, inspect its structure, filter rows, and export the result.")

    with st.sidebar:
        st.header("Data source")
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
        use_sample = st.checkbox("Use bundled sample CSV", value=uploaded_file is None)

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        source_label = uploaded_file.name
    elif use_sample:
        df = load_sample_csv()
        source_label = str(SAMPLE_CSV_PATH)
    else:
        st.info("Upload a CSV file or enable the sample CSV.")
        return

    st.subheader("Overview")
    metric_cols = st.columns(4)
    metric_cols[0].metric("Rows", f"{len(df):,}")
    metric_cols[1].metric("Columns", f"{len(df.columns):,}")
    metric_cols[2].metric("Missing cells", f"{int(df.isna().sum().sum()):,}")
    metric_cols[3].metric("Source", source_label)

    st.subheader("Preview")
    st.dataframe(df.head(200), use_container_width=True)

    st.subheader("Column profile")
    st.dataframe(profile_as_dataframe(df), use_container_width=True)

    st.subheader("Filters")
    filtered_df = df.copy()

    text_columns = categorical_columns(filtered_df)
    selected_text_column = _first(text_columns)
    if selected_text_column is not None:
        selected_text_column = st.selectbox("Text column", text_columns)
        query = st.text_input("Contains text")
        filtered_df = apply_text_filter(filtered_df, selected_text_column, query)

    num_columns = numeric_columns(filtered_df)
    selected_number_column = _first(num_columns)
    if selected_number_column is not None:
        selected_number_column = st.selectbox("Numeric column", num_columns)
        min_value = float(df[selected_number_column].min())
        max_value = float(df[selected_number_column].max())
        selected_range = st.slider(
            "Numeric range",
            min_value=min_value,
            max_value=max_value,
            value=(min_value, max_value),
        )
        filtered_df = apply_numeric_range_filter(
            filtered_df,
            selected_number_column,
            selected_range[0],
            selected_range[1],
        )

    st.subheader("Filtered result")
    st.write(f"{len(filtered_df):,} rows")
    st.dataframe(filtered_df, use_container_width=True)

    st.download_button(
        "Download filtered CSV",
        data=dataframe_to_csv_bytes(filtered_df),
        file_name="filtered.csv",
        mime="text/csv",
    )

    st.subheader("Statistics")
    if numeric_columns(df):
        st.dataframe(df[numeric_columns(df)].describe().transpose(), use_container_width=True)
    else:
        st.info("No numeric columns found.")

    st.subheader("Chart")
    chart_column = _first(numeric_columns(filtered_df))
    if chart_column is not None:
        st.bar_chart(filtered_df[chart_column])
    else:
        st.info("No numeric column is available for charting.")


if __name__ == "__main__":
    run_app()
