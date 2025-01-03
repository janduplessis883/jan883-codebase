import pytest
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.exceptions import NotFittedError
import os
import joblib

# Import your function here
from data_preprocessing.eda import (
    scale_X_train_X_test,
    define_X_y,
    sample_df,
    individual_t_test_classification,
)


def test_scale_X_train_X_test_standard():
    # Create sample data
    X_train = pd.DataFrame({"feature1": [1, 2, 3], "feature2": [4, 5, 6]})
    X_test = pd.DataFrame({"feature1": [7, 8, 9], "feature2": [10, 11, 12]})

    # Call the function
    scaled_X_train, scaled_X_test = scale_X_train_X_test(
        X_train, X_test, scaler="standard"
    )

    # Check that the data is scaled correctly using StandardScaler
    scaler = StandardScaler().fit(X_train)
    expected_scaled_X_train = pd.DataFrame(
        scaler.transform(X_train), columns=X_train.columns
    )
    expected_scaled_X_test = pd.DataFrame(
        scaler.transform(X_test), columns=X_test.columns
    )

    pd.testing.assert_frame_equal(scaled_X_train, expected_scaled_X_train)
    pd.testing.assert_frame_equal(scaled_X_test, expected_scaled_X_test)


def test_scale_X_train_X_test_minmax():
    # Create sample data
    X_train = pd.DataFrame({"feature1": [1, 2, 3], "feature2": [4, 5, 6]})
    X_test = pd.DataFrame({"feature1": [7, 8, 9], "feature2": [10, 11, 12]})

    # Call the function
    scaled_X_train, scaled_X_test = scale_X_train_X_test(
        X_train, X_test, scaler="minmax"
    )

    # Check that the data is scaled correctly using MinMaxScaler
    scaler = MinMaxScaler().fit(X_train)
    expected_scaled_X_train = pd.DataFrame(
        scaler.transform(X_train), columns=X_train.columns
    )
    expected_scaled_X_test = pd.DataFrame(
        scaler.transform(X_test), columns=X_test.columns
    )

    pd.testing.assert_frame_equal(scaled_X_train, expected_scaled_X_train)
    pd.testing.assert_frame_equal(scaled_X_test, expected_scaled_X_test)


def test_scale_X_train_X_test_robust():
    # Create sample data
    X_train = pd.DataFrame({"feature1": [1, 2, 3], "feature2": [4, 5, 6]})
    X_test = pd.DataFrame({"feature1": [7, 8, 9], "feature2": [10, 11, 12]})

    # Call the function
    scaled_X_train, scaled_X_test = scale_X_train_X_test(
        X_train, X_test, scaler="robust"
    )

    # Check that the data is scaled correctly using RobustScaler
    scaler = RobustScaler().fit(X_train)
    expected_scaled_X_train = pd.DataFrame(
        scaler.transform(X_train), columns=X_train.columns
    )
    expected_scaled_X_test = pd.DataFrame(
        scaler.transform(X_test), columns=X_test.columns
    )

    pd.testing.assert_frame_equal(scaled_X_train, expected_scaled_X_train)
    pd.testing.assert_frame_equal(scaled_X_test, expected_scaled_X_test)


def test_invalid_scaler_type():
    # Create sample data
    X_train = pd.DataFrame({"feature1": [1, 2, 3], "feature2": [4, 5, 6]})
    X_test = pd.DataFrame({"feature1": [7, 8, 9], "feature2": [10, 11, 12]})

    # Check that ValueError is raised with an invalid scaler type
    with pytest.raises(
        ValueError,
        match='Invalid scaler type. Choose "standard", "minmax", or "robust".',
    ):
        scale_X_train_X_test(X_train, X_test, scaler="invalid")


def test_output_shapes():
    # Create sample data
    X_train = pd.DataFrame({"feature1": [1, 2, 3], "feature2": [4, 5, 6]})
    X_test = pd.DataFrame({"feature1": [7, 8, 9], "feature2": [10, 11, 12]})

    # Call the function
    scaled_X_train, scaled_X_test = scale_X_train_X_test(
        X_train, X_test, scaler="standard"
    )

    # Check that the output DataFrames have the same shape as the input DataFrames
    assert scaled_X_train.shape == X_train.shape
    assert scaled_X_test.shape == X_test.shape


def test_save_scaler():
    # Create sample data
    X_train = pd.DataFrame({"feature1": [1, 2, 3], "feature2": [4, 5, 6]})
    X_test = pd.DataFrame({"feature1": [7, 8, 9], "feature2": [10, 11, 12]})

    # Call the function with save_scaler=True
    scaled_X_train, scaled_X_test = scale_X_train_X_test(
        X_train, X_test, scaler="standard", save_scaler=True
    )

    # Check that a scaler file is saved
    saved_files = [
        f for f in os.listdir(".") if f.startswith("scaler_") and f.endswith(".pkl")
    ]
    assert len(saved_files) > 0

    # Clean up: remove the saved scaler file
    for file in saved_files:
        os.remove(file)


def test_define_X_y_basic():
    # Create a simple DataFrame
    df = pd.DataFrame(
        {"feature1": [1, 2, 3], "feature2": [4, 5, 6], "target": [7, 8, 9]}
    )

    # Call the function
    X, y = define_X_y(df, "target")

    # Check if X and y are correctly defined
    expected_X = pd.DataFrame({"feature1": [1, 2, 3], "feature2": [4, 5, 6]})
    expected_y = pd.Series([7, 8, 9], name="target")

    pd.testing.assert_frame_equal(X, expected_X)
    pd.testing.assert_series_equal(y, expected_y)


def test_define_X_y_single_value_target():
    # Test with a target column that has only one value
    df = pd.DataFrame(
        {"feature1": [1, 2, 3], "feature2": [4, 5, 6], "target": [1, 1, 1]}
    )

    # Call the function
    X, y = define_X_y(df, "target")

    # Check if X and y are correctly defined
    expected_X = pd.DataFrame({"feature1": [1, 2, 3], "feature2": [4, 5, 6]})
    expected_y = pd.Series([1, 1, 1], name="target")

    pd.testing.assert_frame_equal(X, expected_X)
    pd.testing.assert_series_equal(y, expected_y)


def test_define_X_y_single_column():
    # Test with a DataFrame that has only the target column
    df = pd.DataFrame({"target": [7, 8, 9]})

    # Call the function
    X, y = define_X_y(df, "target")

    # Check if X is empty and y is correct
    expected_X = pd.DataFrame(index=[0, 1, 2])  # An empty DataFrame with the same index
    expected_y = pd.Series([7, 8, 9], name="target")

    pd.testing.assert_frame_equal(X, expected_X)
    pd.testing.assert_series_equal(y, expected_y)


def test_define_X_y_invalid_target():
    # Test with a non-existent target column
    df = pd.DataFrame({"feature1": [1, 2, 3], "feature2": [4, 5, 6]})

    # Check that KeyError is raised when target column does not exist
    with pytest.raises(KeyError):
        define_X_y(df, "target")


def test_define_X_y_empty_dataframe():
    # Test with an empty DataFrame
    df = pd.DataFrame()

    # Check that KeyError is raised when target column does not exist in an empty DataFrame
    with pytest.raises(KeyError):
        define_X_y(df, "target")


def test_sample_df_basic():
    # Test with a basic DataFrame
    df = pd.DataFrame({"feature1": [1, 2, 3, 4, 5], "feature2": [5, 4, 3, 2, 1]})

    # Sample 3 rows
    sampled_df = sample_df(df, 3)

    # Check if the resulting DataFrame has the correct number of rows
    assert sampled_df.shape[0] == 3
    # Check if the sampled DataFrame is a subset of the original DataFrame
    assert sampled_df.isin(df).all().all()


def test_sample_df_more_samples_than_rows(capsys):
    # Test when requesting more samples than the number of rows
    df = pd.DataFrame({"feature1": [1, 2, 3], "feature2": [4, 5, 6]})

    # Request more samples than the DataFrame has rows
    sampled_df = sample_df(df, 5)

    # Check if the function returns None
    assert sampled_df is None

    # Capture the printed output
    captured = capsys.readouterr()
    assert (
        "The number of samples is greater than the number of rows in the dataframe."
        in captured.out
    )


def test_sample_df_zero_samples():
    # Test when requesting zero samples
    df = pd.DataFrame({"feature1": [1, 2, 3], "feature2": [4, 5, 6]})

    # Request zero samples
    sampled_df = sample_df(df, 0)

    # Check if the resulting DataFrame is empty
    assert sampled_df.shape[0] == 0


def test_sample_df_empty_dataframe():
    # Test with an empty DataFrame
    df = pd.DataFrame()

    # Request any number of samples from an empty DataFrame
    sampled_df = sample_df(df, 1)

    # Check if the function returns None
    assert sampled_df is None


def test_sample_df_random_seed():
    # Test if the sampling is consistent given a fixed random seed
    df = pd.DataFrame({"feature1": [1, 2, 3, 4, 5], "feature2": [5, 4, 3, 2, 1]})

    # Sample 3 rows twice with the same seed
    sampled_df1 = sample_df(df, 3)
    sampled_df2 = sample_df(df, 3)

    # Check if both sampled DataFrames are the same
    pd.testing.assert_frame_equal(sampled_df1, sampled_df2)


def test_individual_t_test_classification_basic():
    # Create a simple DataFrame
    df = pd.DataFrame(
        {
            "feature1": [1, 2, 3, 4, 5, 6],
            "feature2": [10, 20, 30, 40, 50, 60],
            "target": [0, 0, 1, 1, 0, 1],
        }
    )

    # Call the function
    result = individual_t_test_classification(
        df, "target", 0, 1, ["feature1", "feature2"]
    )

    # Check if the resulting DataFrame has the correct structure
    assert list(result.columns) == ["feature", "t_stat", "p_value", "significance"]
    assert len(result) == 2  # Two features tested

    # Check if the t-test results are as expected
    expected = pd.DataFrame(
        {
            "feature": ["feature1", "feature2"],
            "t_stat": ["-1.1180339887498947", "-1.118033988749895"],
            "p_value": ["0.33135200535486165", "0.3313520053548614"],
            "significance": ["Insignificant", "Insignificant"],
        }
    )

    pd.testing.assert_frame_equal(result, expected)


def test_individual_t_test_classification_with_alpha():
    # Create a DataFrame with different values
    df = pd.DataFrame(
        {
            "feature1": [1, 1, 1, 5, 5, 5],
            "feature2": [1, 2, 1, 2, 1, 2],
            "target": [0, 0, 0, 1, 1, 1],
        }
    )

    # Call the function with a different alpha value
    result = individual_t_test_classification(
        df, "target", 0, 1, ["feature1", "feature2"], alpha_val=0.1
    )

    # Check if the significance is correctly identified
    assert (
        result[result["feature"] == "feature1"]["significance"].values[0]
        == "Significant"
    )
    assert (
        result[result["feature"] == "feature2"]["significance"].values[0]
        == "Insignificant"
    )


def test_individual_t_test_classification_sampling():
    # Create a DataFrame with different group sizes
    df = pd.DataFrame(
        {
            "feature1": [1, 1, 1, 5, 5, 5],
            "feature2": [1, 2, 1, 2, 1, 2],
            "target": [0, 0, 0, 1, 1, 1],
        }
    )

    # Call the function with sampling
    result = individual_t_test_classification(
        df, "target", 0, 1, ["feature1", "feature2"], sample_frac=0.5, random_state=42
    )

    # Check if sampling was done correctly
    assert len(result) == 2  # Two features tested
    assert "feature1" in result["feature"].values
    assert "feature2" in result["feature"].values


def test_individual_t_test_classification_empty_features():
    # Create a simple DataFrame
    df = pd.DataFrame(
        {
            "feature1": [1, 2, 3, 4, 5, 6],
            "feature2": [10, 20, 30, 40, 50, 60],
            "target": [0, 0, 1, 1, 0, 1],
        }
    )

    # Call the function with an empty feature list
    result = individual_t_test_classification(df, "target", 0, 1, [])

    # Check if the resulting DataFrame is empty
    assert result.empty


def test_individual_t_test_classification_invalid_y_column():
    # Create a simple DataFrame
    df = pd.DataFrame(
        {
            "feature1": [1, 2, 3, 4, 5, 6],
            "feature2": [10, 20, 30, 40, 50, 60],
            "target": [0, 0, 1, 1, 0, 1],
        }
    )

    # Call the function with an invalid y_column
    with pytest.raises(KeyError):
        individual_t_test_classification(df, "nonexistent_column", 0, 1, ["feature1"])


def test_individual_t_test_classification_invalid_y_values():
    # Create a simple DataFrame
    df = pd.DataFrame(
        {
            "feature1": [1, 2, 3, 4, 5, 6],
            "feature2": [10, 20, 30, 40, 50, 60],
            "target": [0, 0, 1, 1, 0, 1],
        }
    )

    # Call the function with an invalid y_value_1
    result = individual_t_test_classification(df, "target", 2, 1, ["feature1"])

    # Check if the resulting DataFrame is empty
    assert result.empty
