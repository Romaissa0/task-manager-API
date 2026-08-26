from flask import Flask, request
from database import get_db_connection
from schemas import TaskCreate, TaskUpdate, TaskPatch
from pydantic import ValidationError
from routes.tasks import tasks_bp


app = Flask(__name__)

@app.route("/")
def home():
    return {"message": "Task Manager API is running!"}



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

@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def patch_task(task_id):
    data = request.get_json()

    try:
        task_data = TaskPatch.model_validate(data)
    except ValidationError as e:
        return {
            "error": "Invalid task data",
            "details": e.errors()
        }, 400

    connection = get_db_connection()

    task = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if task is None:
        connection.close()
        return {"error": "Task not found"}, 404

    updates = task_data.model_dump(exclude_unset=True)

    if not updates:
        connection.close()
        return {"error": "No fields to update"}, 400

    for field, value in updates.items():
        connection.execute(
            f"UPDATE tasks SET {field} = ? WHERE id = ?",
            (value, task_id)
        )

    connection.commit()
    connection.close()

    return {"message": "Task partially updated"}


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

app.register_blueprint(tasks_bp)

if __name__ == "__main__":
    app.run(debug=True)



