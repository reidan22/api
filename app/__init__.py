from flask import Flask

app = Flask(__name__)

from app.elections.ph2022.read import *