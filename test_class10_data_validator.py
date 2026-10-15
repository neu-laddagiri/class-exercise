import pandas as pd
import pytest

from class10_data_validator import validate_columns


@pytest.fixture
def sample_df():
    """Create a small DataFrame for testing."""
    return pd.DataFrame(
        {
            "title": ["Movie A", "Movie B"],
            "type": ["Movie", "Movie"],
            "release_year": [2020, 2021],
        }
    )


def test_validate_columns_with_valid_columns(sample_df):
    # Arrange: every required column exists in sample_df
    required_columns = ["title", "type", "release_year"]

    # Act
    result = validate_columns(sample_df, required_columns)

    # Assert: we get a DataFrame back with the expected columns
    assert isinstance(result, pd.DataFrame)
    assert result.columns.tolist() == ["title", "type", "release_year"]


def test_validate_columns_with_missing_column(sample_df):
    # Arrange: "rating" is required but sample_df doesn't have it
    required_columns = ["title", "type", "release_year", "rating"]

    # Act + Assert: the call must raise ValueError
    with pytest.raises(ValueError) as excinfo:
        validate_columns(sample_df, required_columns)

    # Check the message OUTSIDE the with block -- lines after the raise inside it never run
    assert "Missing required columns" in str(excinfo.value)
    assert "rating" in str(excinfo.value)