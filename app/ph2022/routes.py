from copy import deepcopy
import copy
import json
import random
from app.ph2022.constants import PH2022_ELECTION_PARQUET_FILE_PATH
from app.ph2022.models import JSONObject
from app.ph2022.query import (
    PROVINCE_BY_REGION_DICT,
    VOTE_DATA_LIST,
    get_data_per_candidate,
    get_data_per_category_keys,
    get_data_per_position,
    get_data_per_region,
    get_vote_data,
)
from app.utils.utils import find_root_dir
from flask import jsonify, request
from app import app


@app.route("/ph2022/hello_world", methods=["GET"])
def hello_world():
    return "hello world!", 200


@app.route("/ph2022/all", methods=["GET"])
def get_all():
    data = [vote_data.json_object for vote_data in VOTE_DATA_LIST]
    response = JSONObject(data=data, desc="ph2022 data - all")
    return response.json_object, 200


@app.route("/ph2022/position", methods=["GET"])
# api/ph2022/position?position=president&to_percent=True
def get_per_position():
    position = (
        request.args.get("position").lower() if request.args.get("position") else None
    )
    to_percent = (
        json.loads(request.args.get("to_percent").lower())
        if request.args.get("to_percent")
        else None
    )
    to_sort = (
        json.loads(request.args.get("to_sort").lower())
        if request.args.get("to_sort")
        else None
    )
    reverse = (
        json.loads(request.args.get("reverse").lower())
        if request.args.get("reverse")
        else None
    )

    vote_data = get_data_per_position()

    if position is None:
        response = JSONObject(
            data=get_data_per_position(), desc="ph2022 data - total votes per position"
        ).json_object

    elif position in vote_data.keys():
        data = get_data_per_position()[position]
        total_votes = sum(data.values())
        response = JSONObject(
            data=data, desc=f"ph2022 data - total votes per position ({position})"
        ).json_object
        if to_percent:
            response["data"] = {
                candidate: round(100 * votes / total_votes, 4)
                for candidate, votes in response["data"].items()
            }
        if to_sort:
            response["data"] = {
                k: v
                for k, v in sorted(
                    response["data"].items(), key=lambda x: x[1], reverse=reverse
                )
            }
        response.update({"total_votes": total_votes})
    else:
        data = {}
        desc = f"{position} is not a valid position."
        response = JSONObject(data=data, desc=desc).json_object

    return response, 200


@app.route("/ph2022/candidate", methods=["GET"])
def get_per_candidate():
    first_names = request.args.getlist("first_name", None)
    last_names = request.args.getlist("last_name", None)

    vote_data = get_data_per_candidate()
    if not first_names and not last_names:
        response = JSONObject(data=vote_data, desc="ph2022 data - data per candidate")
        return response.json_object, 200

    filtered_data_by_name = {}
    for first_name in first_names:
        for name, data in vote_data.items():
            if first_name:
                if first_name.lower() in data["first_name"]:
                    filtered_data_by_name[name] = data
    for last_name in last_names:
        for name, data in vote_data.items():
            if last_name:
                if last_name.lower() in data["last_name"]:
                    filtered_data_by_name[name] = data

    response = JSONObject(
        data=filtered_data_by_name, desc="ph2022 data - data per candidate"
    )
    return response.json_object, 200


@app.route("/ph2022/region", methods=["GET"])
def get_per_region():
    region = request.args.get("region", None)
    vote_data = get_data_per_region()
    if not region:
        return (
            JSONObject(
                data=vote_data, desc="ph2022 data - data per region"
            ).json_object,
            200,
        )

    region = region.replace("_", " ").lower()
    if region not in vote_data:
        data = {}
        desc = f"{region} is not a valid region."
        return JSONObject(data=data, desc=desc).json_object, 200

    data = copy.deepcopy(vote_data[region])
    for position, candidates in vote_data[region].items():
        max_key, max_value = max(candidates.items(), key=lambda x: x[1])
        min_key, min_value = min(candidates.items(), key=lambda x: x[1])

        data["max"][position] = {max_key: max_value}
        data["min"][position] = {min_key: min_value}
        data["provinces"] = list(PROVINCE_BY_REGION_DICT[region])

    return JSONObject(data=data, desc="ph2022 data - data per region").json_object, 200


@app.route("/ph2022/keys", methods=["GET"])
def get_keys_per_category():
    _key = request.args.get("key", None)

    vote_data = get_data_per_category_keys()
    if not _key:
        return (
            JSONObject(
                data=vote_data, desc="ph2022 data - data per category keys"
            ).json_object,
            200,
        )
    if _key in vote_data.keys():
        data = vote_data[_key]
        desc = f"ph2022 data - data per category key ({_key})"
    else:
        data = {}
        desc = "ph2022 data - data per category keys"

    return JSONObject(data=data, desc=desc).json_object, 200

@app.route("/ph2022/colors_by_region", methods=["GET"])
def get_colors_by_region():
    regions = PROVINCE_BY_REGION_DICT.keys()
    data = {}
    for region in regions:
        colors = []
        random.seed()
        for _ in range(3):
            colors.append(random.randint(0,255))
        data[region] = colors
    return JSONObject(data=data, desc="Testing for setting colors.").json_object


