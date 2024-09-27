import os
import pandas as pd
import glob
from tqdm import tqdm

tqdm.pandas()

def list_csv_files(directory):
    """
    Return all files in the given directory with a .csv extension.

    Parameters:
    directory (str): The directory path where to search for .csv files.

    Returns:
    list: A list of all .csv files in the directory.
    """
    # Ensure the directory exists
    if not os.path.exists(directory):
        raise ValueError(f"The directory {directory} does not exist.")

    # Use glob to find all .csv files in the directory
    csv_files = glob.glob(os.path.join(directory, "*.csv"))

    return csv_files



def load_csv_files_into_dict(directory):
    """
    Load all .csv files from the given directory into a dictionary of DataFrames.

    Parameters:
    directory (str): The directory path where to search for .csv files.

    Returns:
    dict: A dictionary with filenames (without extensions) as keys and DataFrames as values.
    """
    # Get the list of all CSV files in the directory
    csv_files = list_csv_files(directory)
    csv_files.sort()

    # Dictionary to hold DataFrames
    dataframes_dict = {}

    # Loop through each file and load it into a DataFrame
    for csv_file in tqdm(csv_files, "Loading csv to dataframe", total=len(csv_files)):
        # Extract the base filename without the directory and extension
        file_name = os.path.basename(csv_file).replace('.csv', '')
    # Loop through each file and load it into a DataFrame
    for csv_file in csv_files:
        # Extract the base filename without the directory and extension
        file_name = os.path.basename(csv_file).replace('.csv', '')

        # Attempt to load the CSV with UTF-8 encoding
        try:
            df = pd.read_csv(csv_file, encoding='utf-8')
        except UnicodeDecodeError:
            print(f"Error reading {csv_file} with UTF-8 encoding, trying with ISO-8859-1 (latin1) encoding.")
            # If UTF-8 fails, try reading with 'ISO-8859-1' encoding
            try:
                df = pd.read_csv(csv_file, encoding='ISO-8859-1')
            except Exception as e:
                print(f"Failed to load {csv_file} with ISO-8859-1 encoding as well. Skipping file. Error: {e}")
                continue  # Skip this file and move on to the next

        # Add the DataFrame to the dictionary with the filename as the key
        dataframes_dict[file_name] = df

    return dataframes_dict
