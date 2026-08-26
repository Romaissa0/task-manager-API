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


def create_task(title, description):
    connection = get_db_connection()

    cursor = connection.execute(
        "INSERT INTO tasks (title, description) VALUES (?, ?)",
        (title, description)
    )

    connection.commit()

    task_id = cursor.lastrowid

    connection.close()

    return task_id


def update_task(task_id, title, description, completed):
    connection = get_db_connection()

    connection.execute(
        """
        UPDATE tasks
        SET title = ?, description = ?, completed = ?
        WHERE id = ?
        """,
        (title, description, completed, task_id)
    )

    connection.commit()
    connection.close()

    return {
        "message": "Task updated"
    }

def delete_task(task_id):
    connection = get_db_connection()

    connection.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()

    return {
        "message": "Task deleted"
    }

def patch_task(task_id, updates):  
    connection = get_db_connection()

    task = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if task is None:
        connection.close()
        return {"error": "Task not found"}, 404

    for field, value in updates.items():
        connection.execute(
            f"UPDATE tasks SET {field} = ? WHERE id = ?",
            (value, task_id)
        )

    connection.commit()
    connection.close()

    return {"message": "Task partially updated"}