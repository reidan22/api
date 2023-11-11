from flask import jsonify
from app.utils.utils import df_rows_to_json
from app.ph2022 import ELECTIONS_DF
from app import app


def get_summarized_data_per_person():
    target_columns = ["last_name", "first_name", "position", "party"]
    df = ELECTIONS_DF.groupby(target_columns, as_index=False)["votes"].sum()
    json_obj = df_rows_to_json(df)
    return json_obj


@app.route("/ph2022/all", methods=["GET"])
def get_all():
    response = get_summarized_data_per_person()
    return response, 200


@app.route("/ph2022/all/<position>", methods=["GET"])
def get_all_per_position(position=None):
    position = position.lower().replace(" ", "_")
    response = get_summarized_data_per_person()
    if position in ["president", "vice_president", "senator"]:
        response = [
            data
            for data in response
            if data["position"].lower().replace(" ", "_") == position
        ], 200
    else:
        response = jsonify({"error": "position not listed."}), 500
    return response


@app.route("/danny", methods=["GET"])
def danny1():
    response = {"message": "Hello, This is Danny!"}
    return jsonify(response)
