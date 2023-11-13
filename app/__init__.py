from dataclasses import dataclass
from flask import Flask


CUSTOM_URL_HEADER = "api"


class FlaskAPIApp(Flask):
    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        if CUSTOM_URL_HEADER not in rule:
            rule = "/" + CUSTOM_URL_HEADER + rule
        return super(FlaskAPIApp, self).add_url_rule(
            rule, endpoint, view_func, **options
        )


app = FlaskAPIApp(__name__)

@dataclass
class ToolInfo():
    version = "0.0.1a"
    author = "Danny"

    def json_info(self):
        info = {
            "version": self.version,
            "author": self.author
        }
        return jsonify(info) 

@app.route("/info", methods=["GET"])
def get_api_info():
    info = ToolInfo()
    response = info.json_info()
    return response, 200

from app.ph2022.read import *
