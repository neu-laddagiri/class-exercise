import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

from class6_7_netflix_utils import (
    clean_text,
    drop_missing_rows,
    remove_duplicates,
    remove_iqr_outliers,
    show_overview,
)

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Explore Netflix titles"
    )
    parser.add_argument(
        "--input",
        default="data/messy_netflix_titles.csv",
        help="Path to the Netflix CSV file"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show debug messages"
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S"
    )

    # TODO 4 (Class 6): load the CSV
    input_path = Path(args.input)

    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        logger.error("Input file not found: %s", input_path)
        sys.exit(1)

    logger.info("Loaded %d rows and %d columns", df.shape[0], df.shape[1])

    # Save a copy before any cleaning
    df_original = df.copy()

    # TODO 5 (Class 6): show the overview
    show_overview(df)
    logger.info("Displayed DataFrame overview")

    # TODO 6 (Class 6): basic cleaning
    before = len(df)
    df = remove_duplicates(df)
    logger.info("Removed %d duplicate row(s)", before - len(df))

    before = len(df)
    df = drop_missing_rows(df)
    logger.info("Dropped %d rows with missing values", before - len(df))

    # TODO 3 (Class 7): remove runtime_minutes outliers
    before = len(df)

    try:
        df = remove_iqr_outliers(df, "runtime_minutes", 1.5)
    except ValueError:
        sys.exit(1)

    logger.info("Removed %d runtime_minutes outlier(s)", before - len(df))

    # TODO 4 (Class 7): clean the text columns
    for column in ["title", "type", "country"]:
        df[column] = df[column].apply(clean_text)
        logger.info("Cleaned text column: %s", column)

    # TODO 5 (Class 7): cleaning report
    report = {
        "rows_before": len(df_original),
        "rows_after": len(df),
        "rows_removed": len(df_original) - len(df),
        "columns": df.shape[1],
    }

    logger.info("Cleaning complete: %s", report)


if __name__ == "__main__":
    main()