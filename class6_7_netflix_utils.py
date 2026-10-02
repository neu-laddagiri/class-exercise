import logging
import re

import pandas as pd

logger = logging.getLogger(__name__)


def show_overview(df):
    """Display basic information about a DataFrame."""
    logger.debug("DataFrame shape: %s", df.shape)

    print(f"\nShape: {df.shape}")
    print("\nFirst five rows:")
    print(df.head())
    print("\nColumns:")
    print(list(df.columns))
    print("\nData types:")
    print(df.dtypes)


def remove_duplicates(df):
    """Remove exact duplicate rows."""
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)

    logger.debug("Duplicate removal: %d rows before, %d rows after", before, after)

    return df


def drop_missing_rows(df):
    """Remove rows containing missing values."""
    before = len(df)
    df = df.dropna()
    after = len(df)

    logger.debug("Missing-row removal: %d rows before, %d rows after", before, after)

    return df


def clean_text(value):
    """Normalize one text value."""
    if pd.isna(value):
        return value

    text = str(value)
    text = text.strip()
    text = text.lower()
    text = re.sub(r"\s+", " ", text)

    return text


def remove_iqr_outliers(df, column, threshold):
    """Remove IQR outliers from one column."""
    if column not in df.columns:
        logger.error("Column not found: %s", column)
        raise ValueError(f"Column not found: {column}")

    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1

    lower = q1 - threshold * iqr
    upper = q3 + threshold * iqr

    before = len(df)
    df = df[(df[column] >= lower) & (df[column] <= upper)].copy()
    removed = before - len(df)

    logger.debug(
        "IQR on %s: lower=%.2f, upper=%.2f, removed %d row(s)",
        column, lower, upper, removed
    )

    return df