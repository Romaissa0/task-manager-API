import os

os.environ["DATABASE_PATH"] = "test_tasks.db"
os.environ["FLASK_DEBUG"] = "False"
os.environ["JWT_SECRET_KEY"] = "test-secret-key-that-is-at-least-32-bytes-long"

import pytest
from app import app
from database import get_db_connection


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def test_db():
    connection = get_db_connection()

    # Start each test with empty tables
    connection.execute("DELETE FROM tasks")
    connection.execute("DELETE FROM users")
    connection.commit()

    yield connection

    connection.close()