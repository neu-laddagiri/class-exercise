import logging

logger = logging.getLogger(__name__)


def require_columns(df, required_columns):
    """Check that all required columns exist."""
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        logger.error("Missing required columns: %s", missing)
        raise ValueError(f"Missing required columns: {missing}")
    logger.info("Validation completed")
    return df