import logging

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