from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def home():
    return {"message": "Task Manager API is running!"}


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return {"tasks": []}


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    return {
        "message": "Task created",
        "task": data
    }

if __name__ == "__main__":
    app.run(debug=True)