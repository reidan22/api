import os

from app.utils.utils import read_parquet_to_df


current_file_dir = os.path.dirname(__file__)
election_parquet_file_dir = os.path.join(current_file_dir, "../../src/election_data")
parquet_file_path = os.path.join(election_parquet_file_dir, "summarized_data.parquet")

ELECTIONS_DF = read_parquet_to_df(parquet_file_path)
# export PYTHONPATH=$PYTHONPATH:.
