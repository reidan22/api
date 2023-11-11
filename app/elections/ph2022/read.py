from flask import jsonify
from app import app


# Define a simple endpoint
@app.route('/api/hello', methods=['GET'])
def hello():
    response = {'message': 'Hello, Flask API!'}
    return jsonify(response)

@app.route('/api/danny', methods=['GET'])
def danny1():
    response = {'message': 'Hello, This is Danny!'}
    return jsonify(response)
