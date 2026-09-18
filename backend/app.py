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

@app.route(
    "/collections/<int:collection_id>",
    methods=["DELETE"]
)
def delete_collection(collection_id):
    connection = get_connection()

    cursor =connection.execute(
        "DELETE FROM images WHERE collection_id = ?",
        (collection_id,)
    )

    cursor =connection.execute(
        "DELETE FROM collections WHERE id = ?",
        (collection_id,)
    )

    connection.commit()
    if cursor.rowcount == 0:
        connection.close()

        return jsonify({
            "error": "Collection not found"
        }), 404

    connection.close()

    return jsonify({
        "message": "Collection deleted successfully"
    })

@app.route(
    "/collections/<int:collection_id>/images",
    methods=["POST"])

def save_image(collection_id):
    data = request.get_json()

    image_url = data.get("image_url")
    title = data.get("title", "")

    if not image_url:
        return jsonify({
            "error": "Image URL is required"
        }), 400

    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO images
        (collection_id, title, image_url)
        VALUES (?, ?, ?)
        """,
        (
            collection_id,
            title,
            image_url
        )
    )

    connection.commit()

    image_id = cursor.lastrowid

    connection.close()

    return jsonify({
        "id": image_id,
        "collection_id": collection_id,
        "title": title,
        "image_url": image_url
    }), 201

@app.route(
    "/collections/<int:collection_id>/images/<int:image_id>",
    methods=["PUT"]
)
def edit_image(collection_id, image_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No information was provided"
        }), 400

    new_title = data.get("title")

    if new_title is None:
        return jsonify({
            "error": "Title is required"
        }), 400

    connection = get_connection()

    cursor = connection.execute(
        """
        UPDATE images
        SET title = ?
        WHERE id = ? AND collection_id = ?
        """,
        (
            new_title,
            image_id,
            collection_id
        )
    )

    connection.commit()

    if cursor.rowcount == 0:

        connection.close()

        return jsonify({
            "error": "Image not found"
        }), 404

    connection.close()

    return jsonify({
        "message": "Image updated successfully",
        "id": image_id,
        "collection_id": collection_id,
        "title": new_title
    }), 200

@app.route(
    "/collections/<int:collection_id>/images/<int:image_id>",
    methods=["DELETE"]
)
def delete_image(collection_id, image_id):
    connection = get_connection()

    connection.execute(
        """
        DELETE FROM images
        WHERE id = ? AND collection_id = ?
        """,
        (
            image_id,
            collection_id
        )
    )

    connection.commit()

    connection.close()

    return jsonify({
        "message": "Image deleted"
    })