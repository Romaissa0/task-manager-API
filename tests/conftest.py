import os

# Tell the application to use a test database
os.environ["DATABASE_PATH"] = "test_tasks.db"
os.environ["FLASK_DEBUG"] = "False"
os.environ["JWT_SECRET_KEY"] = "test-secret-key"

import pytest
from app import app
from database import get_db_connection


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


@pytest.fixture
def test_db():
    connection = get_db_connection()

    # Start each test with an empty tasks table
    connection.execute("DELETE FROM tasks")
    connection.commit()

    yield connection

    connection.close()