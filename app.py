from flask import Flask, request
from database import get_db_connection
from schemas import TaskCreate, TaskUpdate
from pydantic import ValidationError

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

@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    connection = get_db_connection()

    task = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    connection.close()

    if task is None:
        return {"error": "Task not found"}, 404

    return {"task": dict(task)}

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    try:
        task = TaskCreate.model_validate(data)
    except ValidationError as e:
        return {"error": "Invalid task data",
                "details": e.errors()}, 400

    connection = get_db_connection()

    cursor = connection.execute(
        "INSERT INTO tasks (title, description) VALUES (?, ?)",
        (task.title, task.description)
    )

    connection.commit()

    task_id = cursor.lastrowid

    connection.close()

    return {
        "message": "Task created",
        "task_id": task_id
    }, 201



@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    try:
        task_update = TaskUpdate.model_validate(data)
    except ValidationError as e:
        return {"error": "Invalid task data",
                "details": e.errors()}, 400

    connection = get_db_connection()

    task = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if task is None:
        connection.close()
        return {"error": "Task not found"}, 404

    connection.execute(
        """
        UPDATE tasks
        SET title = ?, description = ?, completed = ?
        WHERE id = ?
        """,
        (
            task_update.title,
            task_update.description,
            task_update.completed,
            task_id
        )
    )

    connection.commit()
    connection.close()

    return {
        "message": "Task updated"
    }

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    connection = get_db_connection()

    task = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if task is None:
        connection.close()
        return {"error": "Task not found"}, 404

    connection.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()

    return {"message": "Task deleted"}

if __name__ == "__main__":
    app.run(debug=True)



