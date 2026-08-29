from database import get_db_connection


def get_all_tasks(user_id):
    connection = get_db_connection()

    tasks = connection.execute(
        "SELECT * FROM tasks WHERE user_id = ?",
        (user_id,)
    ).fetchall()

    connection.close()

    return [dict(task) for task in tasks]

def get_tasks(user_id):
    tasks = get_all_tasks(user_id)

    return {"tasks": tasks}




def get_task_by_id(task_id, user_id):
    connection = get_db_connection()

    task = connection.execute(
        "SELECT * FROM tasks WHERE id = ? AND user_id = ?",
        (task_id, user_id)
    ).fetchone()

    connection.close()

    if task is None:
        return None

    return dict(task)


def create_task(user_id, title, description):
    connection = get_db_connection()

    cursor = connection.execute(
        "INSERT INTO tasks (user_id, title, description) VALUES (?, ?, ?)",
        (user_id, title, description)
    )

    connection.commit()

    task_id = cursor.lastrowid

    connection.close()

    return task_id

def update_task(task_id, title, description, completed, user_id):
    connection = get_db_connection()

    connection.execute(
        """
        UPDATE tasks
        SET title = ?, description = ?, completed = ?
        WHERE id = ? AND user_id = ?
        """,
        (title, description, completed, task_id, user_id)
    )

    connection.commit()
    connection.close()

    return {
        "message": "Task updated"
    }

def delete_task(task_id, user_id):
    connection = get_db_connection()

    connection.execute(
        "DELETE FROM tasks WHERE id = ? AND user_id = ?",
        (task_id, user_id)
    )

    connection.commit()
    connection.close()

    return {
        "message": "Task deleted"
    }

def patch_task(user_id,task_id, updates):  
    connection = get_db_connection()

    task = connection.execute(
        "SELECT * FROM tasks WHERE id = ? AND user_id = ?",
        (task_id, user_id)
    ).fetchone()

    if task is None:
        connection.close()
        return {"error": "Task not found"}, 404

    for field, value in updates.items():
        connection.execute(
            f"UPDATE tasks SET {field} = ? WHERE id = ? AND user_id = ?",
            (value, task_id, user_id)
        )

    connection.commit()
    connection.close()

    return {"message": "Task partially updated"}