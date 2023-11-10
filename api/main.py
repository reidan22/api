from flask import Flask, jsonify

app = Flask(__name__)

# Define a simple endpoint
@app.route('/api/hello', methods=['GET'])
def hello():
    response = {'message': 'Hello, Flask API!'}
    return jsonify(response)

@app.route('/api/danny', methods=['GET'])
def danny1():
    response = {'message': 'Hello, This is Danny!'}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)