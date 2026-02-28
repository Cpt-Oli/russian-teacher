import json
import os
from flask import Flask, render_template, jsonify

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def load_lessons():
    with open(os.path.join(DATA_DIR, "lessons.json"), "r", encoding="utf-8") as f:
        return json.load(f)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/levels")
def get_levels():
    data = load_lessons()
    return jsonify(data["levels"])


@app.route("/api/lessons/<level_id>")
def get_lessons_for_level(level_id):
    data = load_lessons()
    lessons = [s for s in data["solar_systems"] if s["level"] == level_id]
    lessons.sort(key=lambda x: x["order"])
    return jsonify(lessons)


@app.route("/api/lesson/<level_id>/<int:order>")
def get_lesson(level_id, order):
    data = load_lessons()
    for s in data["solar_systems"]:
        if s["level"] == level_id and s["order"] == order:
            return jsonify(s)
    return jsonify({"error": "Lesson not found"}), 404


if __name__ == "__main__":
    app.run(debug=True, port=5000)
