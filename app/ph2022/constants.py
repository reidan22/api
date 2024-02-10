import os

from constants import ROOT_DIR

PH2022_ELECTION_PARQUET_FILE_NAME = "ph2022_election_data.parquet"
PH2022_ELECTION_PARQUET_FILE_PATH = os.path.join(
    ROOT_DIR, "src/election_data", PH2022_ELECTION_PARQUET_FILE_NAME
)
