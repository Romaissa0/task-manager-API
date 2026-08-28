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