from flask import Flask, request

from database import get_db_connection
from database import get_db_connection
app = Flask(__name__)


@app.route("/")
def home():
    return {"message": "Task Manager API is running!"}


@app.route("/tasks", methods=["GET"])
def get_tasks():
    connection = get_db_connection()

    tasks = connection.execute(
        "SELECT * FROM tasks"
    ).fetchall()

    connection.close()
    return {"tasks": [dict(task) for task in tasks]}


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    connection = get_db_connection()

    cursor = connection.execute(
        "INSERT INTO tasks (title, description) VALUES (?, ?)",
        (data["title"], data.get("description"))
    )

    connection.commit()

    task_id = cursor.lastrowid

    connection.close()

    return {
        "message": "Task created",
        "task_id": task_id
    }, 201

if __name__ == "__main__":
    app.run(debug=True)