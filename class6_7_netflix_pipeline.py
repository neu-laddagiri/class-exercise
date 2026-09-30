import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

from class6_7_netflix_utils import (
    drop_missing_rows,
    remove_duplicates,
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

    # TODO 4: load the CSV
    input_path = Path(args.input)

    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        logger.error("Input file not found: %s", input_path)
        sys.exit(1)

    logger.info("Loaded %d rows and %d columns", df.shape[0], df.shape[1])

    # TODO 5: show the overview
    show_overview(df)
    logger.info("Displayed DataFrame overview")

    # TODO 6: basic cleaning
    before = len(df)
    df = remove_duplicates(df)
    logger.info("Removed %d duplicate row(s)", before - len(df))

    before = len(df)
    df = drop_missing_rows(df)
    logger.info("Dropped %d rows with missing values", before - len(df))


if __name__ == "__main__":
    main()