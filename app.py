import json
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, url_for
from pymongo import MongoClient

# Load MONGO_URI from the .env file
load_dotenv()

app = Flask(__name__)

# Connect to MongoDB Atlas (5 second timeout so errors show quickly)
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client["flask_assignment"]
collection = db["submissions"]

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")


# ---------- Task 1: JSON API route ----------
@app.route("/api")
def api():
    with open(DATA_FILE, "r") as file:
        data = json.load(file)
    return jsonify(data)


# ---------- Task 2: Form that saves to MongoDB Atlas ----------
@app.route("/", methods=["GET", "POST"])
def index():
    error = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email:
            error = "Name and Email are required."
        else:
            try:
                collection.insert_one({"name": name, "email": email, "message": message})
                return redirect(url_for("success"))
            except Exception as e:
                error = f"Database error: {e}"

    # On GET, or on error: show the same page (with the error, if any)
    return render_template("index.html", error=error, form=request.form)


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
