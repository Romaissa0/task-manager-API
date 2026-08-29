def get_auth_token(client):
    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    return response.get_json()["access_token"]



def test_register(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 201

def test_register_existing_user(client):
    # First, register the user
    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    # Then, try to register the same user again
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 409
    data = response.get_json()

    assert data["error"] == "Email already exists"


def test_login(client):
    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Login successful"
    assert "access_token" in data
    assert "user_id" in data



def test_login_wrong_password(client):
    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401

    data = response.get_json()

    assert data["error"] == "Invalid email or password"


def test_get_tasks_without_token(client):
    response = client.get("/tasks")

    assert response.status_code == 401

   
def test_create_task(client):
    token = get_auth_token(client)

    response = client.post(
        "/tasks",
        json={
            "title": "Study Complex Analysis",
            "description": "Review the fundamental theorems"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["message"] == "Task created"
    assert "task_id" in data



def test_get_tasks(client):
    token = get_auth_token(client)

    # Create a task first
    client.post(
        "/tasks",
        json={
            "title": "Study Complex Analysis",
            "description": "Review MMP and Liouville"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    # Get all tasks
    response = client.get(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "tasks" in data
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["title"] == "Study Complex Analysis"

def test_get_task(client):
    token = get_auth_token(client)

    # Create a task
    response = client.post(
        "/tasks",
        json={
            "title": "Study Complex Analysis",
            "description": "Review MMP and Liouville"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 201

    task_id = response.get_json()["task_id"]

    # Get the task
    response = client.get(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "task" in data
    assert data["task"]["id"] == task_id
    assert data["task"]["title"] == "Study Complex Analysis"
    assert data["task"]["description"] == "Review MMP and Liouville"

def test_get_nonexistent_task(client):
    token = get_auth_token(client)

    response = client.get(
        "/tasks/9999",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Task not found"



def test_update_task(client):
    token = get_auth_token(client)

    # Create a task
    response = client.post(
        "/tasks",
        json={
            "title": "Old title",
            "description": "Old description"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 201

    task_id = response.get_json()["task_id"]

    # Update the task
    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "New title",
            "description": "New description",
            "completed": True
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Task updated"

    # Verify the update
    response = client.get(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    task = response.get_json()["task"]

    assert task["title"] == "New title"
    assert task["description"] == "New description"
    assert task["completed"] == 1




def test_patch_task(client):
    token = get_auth_token(client)

    response = client.post(
        "/tasks",
        json={
            "title": "Study Complex Analysis",
            "description": "Review MMP"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 201

    task_id = response.get_json()["task_id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={
            "completed": True
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    response = client.get(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    task = response.get_json()["task"]

    assert task["title"] == "Study Complex Analysis"
    assert task["description"] == "Review MMP"
    assert task["completed"] == 1




def test_delete_task(client):
    token = get_auth_token(client)

    response = client.post(
        "/tasks",
        json={
            "title": "Task to delete",
            "description": "Temporary task"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    task_id = response.get_json()["task_id"]

    response = client.delete(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Task deleted"



def test_delete_nonexistent_task(client):
    token = get_auth_token(client)

    response = client.delete(
        "/tasks/9999",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Task not found"


def test_create_task_invalid_data(client):
    token = get_auth_token(client)

    response = client.post(
        "/tasks",
        json={
            "description": "No title provided"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Invalid task data"


def test_user_cannot_access_other_users_task(client):
    # User A
    token_a = get_auth_token(client)

    # User A creates a task
    response = client.post(
        "/tasks",
        json={
            "title": "User A task",
            "description": "Private"
        },
        headers={
            "Authorization": f"Bearer {token_a}"
        }
    )

    task_id = response.get_json()["task_id"]

    # Register User B
    client.post(
        "/auth/register",
        json={
            "email": "userb@example.com",
            "password": "password123"
        }
    )

    # Login User B
    response = client.post(
        "/auth/login",
        json={
            "email": "userb@example.com",
            "password": "password123"
        }
    )

    token_b = response.get_json()["access_token"]

    # User B tries to access User A's task
    response = client.get(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token_b}"
        }
    )

    assert response.status_code == 404

def test_user_cannot_update_other_users_task(client):
    token_a = get_auth_token(client)

    response = client.post(
        "/tasks",
        json={
            "title": "User A task",
            "description": "Private"
        },
        headers={
            "Authorization": f"Bearer {token_a}"
        }
    )

    task_id = response.get_json()["task_id"]

    # Register User B
    client.post(
        "/auth/register",
        json={
            "email": "userb@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "userb@example.com",
            "password": "password123"
        }
    )

    token_b = response.get_json()["access_token"]

    # User B tries to update User A's task
    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "HACKED",
            "description": "Changed",
            "completed": True
        },
        headers={
            "Authorization": f"Bearer {token_b}"
        }
    )

    assert response.status_code == 404


def test_user_cannot_delete_other_users_task(client):
    token_a = get_auth_token(client)

    response = client.post(
        "/tasks",
        json={
            "title": "User A task",
            "description": "Private"
        },
        headers={
            "Authorization": f"Bearer {token_a}"
        }
    )

    task_id = response.get_json()["task_id"]

    # Register User B
    client.post(
        "/auth/register",
        json={
            "email": "userb@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "userb@example.com",
            "password": "password123"
        }
    )

    token_b = response.get_json()["access_token"]

    # User B tries to delete User A's task
    response = client.delete(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token_b}"
        }
    )

    assert response.status_code == 404

def test_create_task_invalid_json(client):
    token = get_auth_token(client)

    response = client.post(
        "/tasks",
        data='{"title": "Test"',
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )

    assert response.status_code == 400