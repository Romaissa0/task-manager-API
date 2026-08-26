from flask import Blueprint
from database import get_db_connection
tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/tasks", methods=["GET"])
def get_tasks():
    connection = get_db_connection()

    tasks = connection.execute(
        "SELECT * FROM tasks"
    ).fetchall()

    connection.close()
    return {"tasks": [dict(task) for task in tasks]}