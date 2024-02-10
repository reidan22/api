from dataclasses import dataclass

from flask import Flask
from flask_cors import CORS

from constants import AUTHOR, CUSTOM_URL_HEADER, LATEST_UPDATE, VERSION


class FlaskAPIApp(Flask):
    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        if CUSTOM_URL_HEADER not in rule:
            rule = "/" + CUSTOM_URL_HEADER + rule
        return super(FlaskAPIApp, self).add_url_rule(
            rule, endpoint, view_func, **options
        )

app = FlaskAPIApp(__name__)
CORS(app)  # Enable CORS for all routes


@dataclass
class ToolInfo:
    version = VERSION
    author = AUTHOR
    latest_update = LATEST_UPDATE

    def json_info(self):
        info = {
            "version": self.version,
            "author": self.author,
            "latest_update": self.latest_update,
        }
        return jsonify(info)


@app.route("/info", methods=["GET"])
def get_api_info():
    info = ToolInfo()
    response = info.json_info()
    return response, 200


app.json.sort_keys = False

from app.ph2022.routes import *
