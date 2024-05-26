from flask import Flask, request, jsonify
from model import tasks

app = Flask(__name__)

try:
    tasks = tasks()
except Exception as e:
    print(f"Failed to initialize tasks: {e}")

@app.route("/tasks/all", methods=["GET"])
def get_all_tasks():
    result = tasks.get_all_tasks()
    return jsonify(result), 200

@app.route("/tasks/<id>", methods=["GET"])
def get_task(id):
    result = tasks.get_task(id)
    return jsonify(result), 200

@app.route("/task/add", methods=["POST"])
def add_task():
    data = request.get_json()
    result = tasks.add_task(data)
    return jsonify(result), 200

@app.route("/task/update", methods=["PATCH"])
def update_task():
    data = request.get_json()
    result = tasks.update_task(data)
    return jsonify(result), 200

@app.route("/task/delete/<id>", methods=["DELETE"])
def delete_task(id):
    result = tasks.delete_task(id)
    return jsonify(result), 200

if __name__ == "__main__":
    app.run(debug=True)
