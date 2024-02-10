import json
import os

import pandas as pd


def find_root_dir():
    # Start from the current directory
    current_dir = os.path.abspath(os.path.dirname(__file__))

    # Traverse upwards until a known marker is found (e.g., a file named "README.md" or a directory named "src")
    while not os.path.exists(
        os.path.join(current_dir, "README.md")
    ) and not os.path.exists(os.path.join(current_dir, "src")):
        parent_dir = os.path.dirname(current_dir)

        # Break if we reach the root directory
        if parent_dir == current_dir:
            raise FileNotFoundError("Could not find the root directory of the project")

        current_dir = parent_dir

    return current_dir


def read_parquet_to_df(file_path):
    df = pd.read_parquet(file_path, engine="fastparquet")
    return df


def df_rows_to_json(df):
    json_objects = []
    for index, row in df.iterrows():
        json_string = row.to_json()
        json_object = json.loads(json_string)
        json_objects.append(json_object)
    return json_objects
