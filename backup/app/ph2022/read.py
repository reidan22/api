from flask import jsonify

from app import app
from app.ph2022 import (
    CANDIDATE_INFOS,
    ELECTIONS_DF,
    FIRST_NAMES,
    LAST_NAMES,
    PARTIES,
    POSITIONS,
    PROVINCES,
    RAW_DATA_DICT,
    REGIONS,
)
from app.utils.utils import df_rows_to_json


def get_summarized_data_per_person():
    target_columns = ["last_name", "first_name", "position", "party"]
    df = ELECTIONS_DF.groupby(target_columns, as_index=False)["votes"].sum()
    json_obj = df_rows_to_json(df)
    return json_obj


@app.route("/ph2022/all", methods=["GET"])
def get_all():
    response = RAW_DATA_DICT
    return response, 200


@app.route("/ph2022/all/<key>", methods=["GET"])
def get_by_key(key=None):
    response = RAW_DATA_DICT.get(key, None)
    if not response:
        return jsonify({"error": f"{key} is not listed."}), 500
    return response, 200


@app.route("/ph2022/position/<position>", methods=["GET"])
def get_per_position(position=None):
    response = get_summarized_data_per_person()
    if position in POSITIONS:
        response = [data for data in response if data["position"] == position], 200
    else:
        response = jsonify({"error": "position not listed."}), 500
    return response


@app.route("/ph2022/candidate/<candidate>", methods=["GET"])
def get_per_name(candidate=None):
    response = get_summarized_data_per_person()
    if candidate in FIRST_NAMES:
        response = (
            [data for data in response if candidate in data["first_name"]][0],
            200,
        )
    elif candidate in LAST_NAMES:
        response = [data for data in response if candidate in data["last_name"]][0], 200
    else:
        response = jsonify({"error": "name is not in the list."}), 500
    return response


@app.route("/ph2022/candidate/all/<candidate>", methods=["GET"])
def get_all_per_name(candidate=None):
    response = CANDIDATE_INFOS
    if candidate in FIRST_NAMES or candidate in LAST_NAMES:
        for candidate_info in CANDIDATE_INFOS.values():
            if candidate in candidate_info.full_name:
                response = candidate_info
                break
        response = response.to_json(), 200
    else:
        response = jsonify({"error": "name is not in the list."}), 500
    return response


@app.route("/danny", methods=["GET"])
def danny1():
    response = {"message": "Hello, This is Danny!"}
    return jsonify(response)
