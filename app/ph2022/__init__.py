import os

from app.utils.utils import read_parquet_to_df


current_file_dir = os.path.dirname(__file__)
election_parquet_file_dir = os.path.join(current_file_dir, "../../src/election_data")
parquet_file_path = os.path.join(election_parquet_file_dir, "summarized_data.parquet")

ELECTIONS_DF = read_parquet_to_df(parquet_file_path)
# export PYTHONPATH=$PYTHONPATH:.

POSITIONS = ELECTIONS_DF.position.unique()
REGIONS = ELECTIONS_DF.region.unique()
PROVINCES = ELECTIONS_DF.province.unique()
PARTIES = ELECTIONS_DF.party.unique()
FIRST_NAMES = ELECTIONS_DF.first_name.unique()
LAST_NAMES = ELECTIONS_DF.last_name.unique()

RAW_DATA_DICT = {
        "position": list(POSITIONS),
        "region": list(REGIONS),
        "province": list(PROVINCES),
        "party": list(PARTIES),
        "first_name": list(FIRST_NAMES),
        "last_name": list(LAST_NAMES)
    }