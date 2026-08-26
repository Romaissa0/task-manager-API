from database import get_db_connection


def get_all_tasks():
    connection = get_db_connection()

    tasks = connection.execute(
        "SELECT * FROM tasks"
    ).fetchall()

    connection.close()

    return [dict(task) for task in tasks]

def get_tasks():
    tasks = get_all_tasks()

    return {"tasks": tasks}


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


def get_task_by_id(task_id):
    connection = get_db_connection()

    task = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    connection.close()

    if task is None:
        return None

    return dict(task)