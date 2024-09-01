import pytest
import pandas as pd

from data_preprocessing.eda import *

def test_convert_to_datetime_basic():
    # Test the basic functionality of converting columns to datetime
    df = pd.DataFrame({
        'date_col1': ['01/02/2023', '02/03/2023', '03/04/2023'],
        'date_col2': ['2023-01-02', '2023-02-03', '2023-03-04']
    })
    expected_date_col1 = pd.to_datetime(df['date_col1'], dayfirst=True)
    expected_date_col2 = pd.to_datetime(df['date_col2'])

    # Run the function
    result = convert_to_datetime(df.copy(), ['date_col1', 'date_col2'], day_first=True)

    # Assertions
    pd.testing.assert_series_equal(result['date_col1'], expected_date_col1)
    pd.testing.assert_series_equal(result['date_col2'], expected_date_col2)

def test_convert_to_datetime_nonexistent_column():
    # Test that the function raises a ValueError when a column doesn't exist
    df = pd.DataFrame({'date_col1': ['01/02/2023', '02/03/2023']})

    with pytest.raises(ValueError, match="Column 'nonexistent_col' not found in DataFrame."):
        convert_to_datetime(df, ['nonexistent_col'], day_first=True)

def test_convert_to_datetime_dayfirst():
    # Test the day_first parameter functionality
    df = pd.DataFrame({
        'date_col': ['01/02/2023', '02/03/2023', '03/04/2023']
    })
    expected_date_day_first = pd.to_datetime(df['date_col'], dayfirst=True)
    expected_date_month_first = pd.to_datetime(df['date_col'], dayfirst=False)

    # Run the function with day_first=True
    result_day_first = convert_to_datetime(df.copy(), ['date_col'], day_first=True)
    pd.testing.assert_series_equal(result_day_first['date_col'], expected_date_day_first)

    # Run the function with day_first=False
    result_month_first = convert_to_datetime(df.copy(), ['date_col'], day_first=False)
    pd.testing.assert_series_equal(result_month_first['date_col'], expected_date_month_first)

# To run the tests, use the command: pytest -v <test_file_name>.py

def test_column_summary_basic():
    df = pd.DataFrame({
        'int_col': [1, 2, 3, 4, 5],
        'float_col': [1.0, 2.0, 3.0, 4.0, 5.0],
        'str_col': ['a', 'b', 'c', 'd', 'e'],
        'bool_col': [True, False, True, False, True]
    })

    result = column_summary(df)

    expected_columns = ['col_name', 'col_dtype', 'num_of_nulls', 'num_of_non_nulls', 'num_of_distinct_values', 'distinct_values_counts']
    assert all(col in result.columns for col in expected_columns)

    # Check basic types
    assert result[result['col_name'] == 'int_col']['col_dtype'].values[0] == 'int64'
    assert result[result['col_name'] == 'float_col']['col_dtype'].values[0] == 'float64'
    assert result[result['col_name'] == 'str_col']['col_dtype'].values[0] == 'object'
    assert result[result['col_name'] == 'bool_col']['col_dtype'].values[0] == 'bool'

def test_column_summary_with_nulls():
    df = pd.DataFrame({
        'col_with_nulls': [1, 2, None, 4, None],
    })

    result = column_summary(df)

    assert result[result['col_name'] == 'col_with_nulls']['num_of_nulls'].values[0] == 2
    assert result[result['col_name'] == 'col_with_nulls']['num_of_non_nulls'].values[0] == 3

def test_column_summary_distinct_values():
    df = pd.DataFrame({
        'col_distinct_values': ['a', 'b', 'b', 'c', 'c', 'c', 'd']
    })

    result = column_summary(df)

    assert result[result['col_name'] == 'col_distinct_values']['num_of_distinct_values'].values[0] == 4
    assert result[result['col_name'] == 'col_distinct_values']['distinct_values_counts'].values[0] == {'c': 3, 'b': 2, 'a': 1, 'd': 1}

def test_column_summary_more_than_10_distinct_values():
    df = pd.DataFrame({
        'col_many_distinct_values': list(range(15))
    })

    result = column_summary(df)

    assert result[result['col_name'] == 'col_many_distinct_values']['num_of_distinct_values'].values[0] == 15
    # Check if it captures only the top 10 values
    assert len(result[result['col_name'] == 'col_many_distinct_values']['distinct_values_counts'].values[0]) == 10

def test_column_summary_empty_dataframe():
    df = pd.DataFrame()

    result = column_summary(df)

    assert result.empty


def test_column_summary_plus_basic():
    # Test basic functionality with different data types
    df = pd.DataFrame({
        'int_col': [1, 2, 3, 4, 5],
        'float_col': [1.0, 2.0, 3.0, 4.0, 5.0],
        'str_col': ['a', 'b', 'a', 'a', 'b'],
        'bool_col': [True, False, True, False, True]
    })

    result = column_summary_plus(df)

    assert result[result['col_name'] == 'int_col']['num_distinct_values'].values[0] == 5
    assert result[result['col_name'] == 'int_col']['min_value'].values[0] == 1
    assert result[result['col_name'] == 'int_col']['max_value'].values[0] == 5

    assert result[result['col_name'] == 'float_col']['average_no_na'].values[0] == 3.0
    assert result[result['col_name'] == 'float_col']['median_no_na'].values[0] == 3.0

    assert result[result['col_name'] == 'str_col']['num_distinct_values'].values[0] == 2
    assert result[result['col_name'] == 'str_col']['distinct_values'].values[0] == {'a': 3, 'b': 2}

    assert result[result['col_name'] == 'bool_col']['num_distinct_values'].values[0] == 2
    assert result[result['col_name'] == 'bool_col']['distinct_values'].values[0] == {True: 3, False: 2}

def test_column_summary_plus_with_nulls():
    # Test handling of null values
    df = pd.DataFrame({
        'col_with_nulls': [1, 2, None, 4, None],
    })

    result = column_summary_plus(df)

    assert result[result['col_name'] == 'col_with_nulls']['null_present'].values[0] == 1
    assert result[result['col_name'] == 'col_with_nulls']['nulls_num'].values[0] == 2
    assert result[result['col_name'] == 'col_with_nulls']['non_nulls_num'].values[0] == 3

def test_column_summary_plus_more_than_10_distinct_values():
    # Test columns with more than 10 distinct values
    df = pd.DataFrame({
        'many_distinct': list(range(20))
    })

    result = column_summary_plus(df)

    assert result[result['col_name'] == 'many_distinct']['num_distinct_values'].values[0] == 20
    # Check only top 10 values are reported
    assert len(result[result['col_name'] == 'many_distinct']['distinct_values'].values[0]) == 10

def test_column_summary_plus_empty_dataframe():
    # Test with an empty DataFrame
    df = pd.DataFrame()

    result = column_summary_plus(df)

    assert result.empty

def test_column_summary_plus_edge_cases():
    # Test edge cases like all nulls or a single unique value
    df = pd.DataFrame({
        'all_nulls': [None, None, None],
        'single_value': [42, 42, 42],
        'mixed_values': [np.nan, 1, np.nan]
    })

    result = column_summary_plus(df)

    # All nulls
    assert result[result['col_name'] == 'all_nulls']['nulls_num'].values[0] == 3
    assert result[result['col_name'] == 'all_nulls']['non_nulls_num'].values[0] == 0  # Corrected this line
    assert np.isnan(result[result['col_name'] == 'all_nulls']['min_value'].values[0])

    # Single unique value
    assert result[result['col_name'] == 'single_value']['num_distinct_values'].values[0] == 1
    assert result[result['col_name'] == 'single_value']['min_value'].values[0] == 42
    assert result[result['col_name'] == 'single_value']['max_value'].values[0] == 42

    # Mixed values with NaN
    assert result[result['col_name'] == 'mixed_values']['non_nulls_num'].values[0] == 1  # Corrected this line

# To run the tests, use the command: pytest -v <test_file_name>.py
def test_inspect_df_basic(capsys):
    # Create a simple DataFrame
    df = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [5.0, 6.1, 7.2, 8.3, 9.4],
        'C': ['foo', 'bar', 'baz', 'qux', 'quux']
    })

    # Call the function
    inspect_df(df)

    # Capture the output
    captured = capsys.readouterr()

    # Assert basic output checks
    assert "df.head()" in captured.out
    assert "df.shape" in captured.out
    assert "df.describe()" in captured.out
    assert "NaN Values" in captured.out
    assert "Duplicate Rows" in captured.out

def test_inspect_df_with_nans_and_duplicates(capsys):
    # Create a DataFrame with NaNs and duplicate rows
    df = pd.DataFrame({
        'A': [1, 2, 2, 4, 5, None],
        'B': [5.0, None, 7.2, 8.3, 9.4, 5.0],
        'C': ['foo', 'bar', 'bar', 'qux', 'quux', 'foo']
    })

    # Call the function
    inspect_df(df)

    # Capture the output
    captured = capsys.readouterr()

    # Check the printed output for NaN and duplicate counts
    assert "NaN Values" in captured.out
    assert "2" in captured.out  # Checking for the presence of NaN count
    assert "Duplicate Rows" in captured.out
    assert "1" in captured.out  # Checking for the presence of duplicate count

def test_inspect_df_empty(capsys):
    # Create an empty DataFrame
    df = pd.DataFrame()

    # Call the function
    inspect_df(df)

    # Capture the output
    captured = capsys.readouterr()

    # Check output for empty DataFrame handling
    assert "df.head()" in captured.out
    assert "df.shape" in captured.out
    assert "df.describe()" in captured.out
    assert "NaN Values" in captured.out
    assert "Duplicate Rows" in captured.out


def test_update_column_names_basic():
    # Test the basic functionality
    df = pd.DataFrame({
        'First Name': [1, 2, 3],
        'Last Name': ['A', 'B', 'C']
    })

    updated_df = update_column_names(df)

    # Check if the columns have been updated correctly
    assert list(updated_df.columns) == ['first_name', 'last_name']

def test_update_column_names_edge_cases():
    # Test with column names already lowercase or without spaces
    df = pd.DataFrame({
        'firstname': [1, 2, 3],
        'LastName': ['A', 'B', 'C'],
        'City': ['New York', 'Los Angeles', 'Chicago']
    })

    updated_df = update_column_names(df)

    # Check if the columns have been updated correctly
    assert list(updated_df.columns) == ['firstname', 'lastname', 'city']

def test_update_column_names_empty_df():
    # Test with an empty DataFrame
    df = pd.DataFrame()

    updated_df = update_column_names(df)

    # Check that the DataFrame is still empty and has no columns
    assert updated_df.empty
    assert len(updated_df.columns) == 0

def test_update_column_names_special_characters():
    # Test with columns containing special characters
    df = pd.DataFrame({
        'First-Name': [1, 2, 3],
        'Last@Name': ['A', 'B', 'C'],
        'City&State': ['New York', 'Los Angeles', 'Chicago']
    })

    updated_df = update_column_names(df)

    # Check if the columns have been updated correctly
    assert list(updated_df.columns) == ['first-name', 'last@name', 'city&state']

def test_update_column_names_mixed_spaces():
    # Test with mixed spaces and uppercase letters
    df = pd.DataFrame({
        '  LeadingSpaces': [1, 2, 3],
        'TrailingSpaces  ': ['A', 'B', 'C'],
        'Mixed CASE Spaces': ['New York', 'Los Angeles', 'Chicago']
    })

    updated_df = update_column_names(df)

    # Check if the columns have been updated correctly
    assert list(updated_df.columns) == ['__leadingspaces', 'trailingspaces__', 'mixed_case_spaces']
