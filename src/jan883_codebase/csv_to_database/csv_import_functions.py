import os
import numpy as np
import pandas as pd
import pymysql


def csv_files():
    """Get names of only CSV files."""
    csv_files = [file for file in os.listdir(os.getcwd()) if file.endswith(".csv")]
    return csv_files


def configure_dataset_directory(csv_files, dataset_dir):
    """Move CSV files to a dataset directory."""
    # Create dataset folder to process CSV files
    os.makedirs(dataset_dir, exist_ok=True)

    # Move CSV files to dataset folder
    for csv in csv_files:
        mv_file = f"mv '{csv}' {dataset_dir}"
        os.system(mv_file)

    return


def create_df(dataset_dir, csv_files):
    """Create DataFrame from CSV files."""
    data_path = os.path.join(os.getcwd(), dataset_dir)

    # Loop through the files and create the DataFrame
    df = {}
    for file in csv_files:
        try:
            df[file] = pd.read_csv(os.path.join(data_path, file))
        except UnicodeDecodeError:
            df[file] = pd.read_csv(
                os.path.join(data_path, file), encoding="ISO-8859-1"
            )  # if utf-8 encoding error
        print(file)

    return df


def clean_tbl_name(filename):
    """Clean table name to be MySQL-compatible."""
    clean_tbl_name = (
        filename.lower()
        .replace(" ", "")
        .replace("-", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace("$", "")
        .replace("%", "")
    )
    tbl_name = f"{clean_tbl_name.split('.')[0]}"
    return tbl_name


def clean_colname(dataframe):
    """Clean column names and prepare MySQL-compatible schema."""
    # Force column names to be lower case, no spaces, no dashes
    dataframe.columns = [
        x.lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace(".", "_")
        .replace("$", "")
        .replace("%", "")
        for x in dataframe.columns
    ]

    # Processing data types for MySQL
    replacements = {
        "timedelta64[ns]": "VARCHAR(255)",
        "object": "TEXT",
        "float64": "DOUBLE",
        "int64": "INT",
        "datetime64": "DATETIME",
    }

    col_str = ", ".join(
        f"`{n}` {d}"
        for n, d in zip(dataframe.columns, dataframe.dtypes.replace(replacements))
    )

    return col_str, dataframe.columns


def upload_to_db(
    host,
    port,
    dbname,
    user,
    password,
    tbl_name,
    col_str,
    file,
    dataframe,
    dataframe_columns,
):
    """Upload DataFrame to MySQL database."""
    # Connect to MySQL
    conn = pymysql.connect(
        host=host, port=int(port), user=user, password=password, database=dbname
    )
    cursor = conn.cursor()
    print("Opened MySQL database successfully")

    # Drop table with same name if it exists
    cursor.execute(f"DROP TABLE IF EXISTS `{tbl_name}`;")

    # Create table
    cursor.execute(f"CREATE TABLE `{tbl_name}` ({col_str});")
    print(f"Table {tbl_name} was created successfully")

    # Save DataFrame to CSV
    dataframe.to_csv(file, header=dataframe_columns, index=False, encoding="utf-8")

    # Open the CSV file
    with open(file, "r") as my_file:
        # Skip the header row
        next(my_file)
        # Insert rows into the table
        for line in my_file:
            values = line.strip().split(",")
            placeholders = ", ".join(["%s"] * len(values))
            insert_query = f"INSERT INTO `{tbl_name}` VALUES ({placeholders})"
            cursor.execute(insert_query, values)

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Table {tbl_name} imported to database successfully")

    return
