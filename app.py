import os
from datetime import datetime

from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)


MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
MONGO_PORT = int(os.environ.get("MONGO_PORT", "27017"))
MONGO_USERNAME = os.environ.get("MONGO_USERNAME")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")




client = MongoClient(
    host=MONGO_HOST,
    port=MONGO_PORT,
    username=MONGO_USERNAME,
    password=MONGO_PASSWORD,
    authSource="admin",
    serverSelectionTimeoutMS=5000,
)


db = client.flask_db
collection = db.data




@app.route("/")
def index():
    return f"Welcome to the Flask app! The current time is: {datetime.now()}"


@app.route("/data", methods=["GET", "POST"])
def data():
    if request.method == "POST":
        payload = request.get_json(silent=True)
        if payload is None:
            return jsonify({"error": "Request body must be valid JSON"}), 400
        collection.insert_one(payload)
        return jsonify({"status": "Data inserted"}), 201

    documents = list(collection.find({}, {"_id": 0}))
    return jsonify(documents), 200



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)