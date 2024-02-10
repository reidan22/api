import os
from collections import defaultdict

from app.ph2022.constants import PH2022_ELECTION_PARQUET_FILE_PATH
from app.ph2022.models import VoteData
from app.utils.utils import df_rows_to_json, read_parquet_to_df


def get_vote_data():
    json_object = df_rows_to_json(read_parquet_to_df(PH2022_ELECTION_PARQUET_FILE_PATH))
    vote_data = []
    for data in json_object:
        if "ncr -" in data["province"]:
            data["province"] = "ncr"
        vote_data.append(VoteData(**data))
    return vote_data


VOTE_DATA_LIST = get_vote_data()
PROVINCE_BY_REGION_DICT = defaultdict(set)
for vote_data in VOTE_DATA_LIST:
    PROVINCE_BY_REGION_DICT[vote_data.region].add(vote_data.province)


def get_data_per_position():
    agg_data = defaultdict(lambda: defaultdict(int))
    for vote_data in VOTE_DATA_LIST:
        agg_data[vote_data.position][vote_data.full_name] += vote_data.votes

    return agg_data


def get_data_per_candidate():
    agg_data = defaultdict(lambda: defaultdict(dict))
    for vote_data in VOTE_DATA_LIST:
        if vote_data.full_name not in agg_data:
            agg_data[vote_data.full_name]["position"] = vote_data.position
            agg_data[vote_data.full_name]["first_name"] = vote_data.first_name
            agg_data[vote_data.full_name]["last_name"] = vote_data.last_name
            agg_data[vote_data.full_name]["party"] = vote_data.party
            agg_data[vote_data.full_name]["total_votes"] = 0

        agg_data[vote_data.full_name]["regions"][vote_data.region] = vote_data.votes
        agg_data[vote_data.full_name]["total_votes"] += vote_data.votes
    return agg_data


def get_data_per_region():
    agg_data = defaultdict(lambda: defaultdict(dict))
    for vote_data in VOTE_DATA_LIST:
        agg_data[vote_data.region][vote_data.position][
            vote_data.full_name
        ] = vote_data.votes

    return agg_data


def get_data_per_category_keys():
    agg_data = defaultdict(set)
    for vote_data in VOTE_DATA_LIST:
        agg_data["region"].add(vote_data.region)
        agg_data["province"].add(vote_data.province)
        agg_data["position"].add(vote_data.position)
        agg_data["full_name"].add(vote_data.full_name)
        agg_data["party"].add(vote_data.party)

    agg_data["region"] = list(agg_data["region"])
    agg_data["province"] = list(agg_data["province"])
    agg_data["position"] = list(agg_data["position"])
    agg_data["full_name"] = list(agg_data["full_name"])
    agg_data["party"] = list(agg_data["party"])

    return agg_data
