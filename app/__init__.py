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

from app.ph2022.read import *
