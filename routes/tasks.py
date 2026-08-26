from flask import Blueprint, request
from database import get_db_connection
from pydantic import ValidationError
from schemas import TaskCreate
tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/tasks", methods=["GET"])
def get_tasks():
    connection = get_db_connection()

    tasks = connection.execute(
        "SELECT * FROM tasks"
    ).fetchall()

    connection.close()
    return {"tasks": [dict(task) for task in tasks]}

@tasks_bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    try:
        task = TaskCreate.model_validate(data)
    except ValidationError as e:
        return {
            "error": "Invalid task data",
            "details": e.errors()
        }, 400

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

@tasks_bp.route("/tasks/<int:task_id>", methods=["GET"])
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