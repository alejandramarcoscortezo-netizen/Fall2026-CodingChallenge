from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

collections = []

@app.route("/")
def home():
    return jsonify({
        "message": "Image Collection API is running!"
    })

@app.route("/collections", methods=["GET"])
def get_collections():
    return jsonify(collections)

@app.route("/collections", methods=["POST"])
def create_collections():
    data = request.get_json()

    if not data or not data.get("name"):
        return jsonify({
            "error": "Collection name is required"
        }), 400

    collection = {
        "id": len(collections) + 1,
        "name": data["name"],
        "images": []
    }

    collections.append(collection)

    return jsonify(collection), 201


if __name__ == "__main__":
    app.run(debug=True)