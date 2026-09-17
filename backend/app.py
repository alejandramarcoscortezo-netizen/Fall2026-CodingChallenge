from flask import Flask, jsonify, request
from flask_cors import CORS
from database import get_connection, initialize_database

app = Flask(__name__)
CORS(app)

initialize_database()

@app.route("/")
def home():
    return jsonify({
        "message": "Image Collection API is running!"
    })

@app.route("/collections", methods=["GET"])
def get_collections():
    connection = get_connection()

    rows = connection.execute(
        "SELECT * FROM collections"
    ).fetchall()

    connection.close()

    collections = [
        dict(row)
        for row in rows
    ]
    return jsonify(collections)

@app.route("/collections", methods=["POST"])
def create_collections():
    data = request.get_json()

    if not data or not data.get("name"):
        return jsonify({
            "error": "Collection name is required"
        }), 400

    connection = get_connection()

    cursor = connection.execute(
        "INSERT INTO collections (name) VALUES (?)",
        (data["name"],)
    )

    connection.commit()

    collection_id = cursor.lastrowid

    connection.close()

    return jsonify({
        "id": collection_id,
        "name": data["name"]
    }), 201


if __name__ == "__main__":
    app.run(debug=True)