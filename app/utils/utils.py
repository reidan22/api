import json
import pyarrow.parquet as pq


def read_parquet_to_df(file_path):
    return pq.read_table(file_path).to_pandas()


def df_rows_to_json(df):
    json_objects = []
    for index, row in df.iterrows():
        json_string = row.to_json()
        json_object = json.loads(json_string)
        json_objects.append(json_object)
    return json_objects
