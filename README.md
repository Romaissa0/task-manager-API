# Task Manager API

A RESTful Task Manager API built with Python and Flask.

The project demonstrates backend development fundamentals including REST APIs,
CRUD operations, SQLite database integration, input validation, JWT-based
authentication, user ownership, error handling, and automated testing.

**Live API:** task-manager-api-fmom.onrender.com  
**Tests:** 18 passed

## Features

- User registration and login
- JWT-based authentication
- Create tasks
- View tasks
- Update tasks
- Partially update tasks
- Delete tasks
- User-specific task ownership
- Pydantic request validation
- Error handling
- Automated API tests

## Technologies

- Python
- Flask
- SQLite
- Pydantic
- Flask-JWT-Extended
- Pytest
- python-dotenv

## Project Structure

```text
task-manager-API/
│
├── routes/
│   ├── auth.py
│   ├── tasks.py
│   └── __init__.py
│
├── services/
│   ├── auth_service.py
│   ├── task_service.py
│   └── __init__.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── __init__.py
│
├── app.py
├── database.py
├── schemas.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md

Authentication

The API uses JSON Web Tokens (JWT) to authenticate users.

Protected task endpoints require an access token:

Authorization: Bearer <access_token>

Each user can only access and modify their own tasks.
API Endpoints
Authentication
| Method | Endpoint         | Description              | Authentication |
| ------ | ---------------- | ------------------------ | -------------- |
| POST   | `/auth/register` | Register a new user      | No             |
| POST   | `/auth/login`    | Log in and receive a JWT | No             |
Tasks
| Method | Endpoint      | Description             | Authentication |
| ------ | ------------- | ----------------------- | -------------- |
| GET    | `/tasks`      | Get all user's tasks    | Yes            |
| POST   | `/tasks`      | Create a task           | Yes            |
| GET    | `/tasks/<id>` | Get a specific task     | Yes            |
| PUT    | `/tasks/<id>` | Replace a task          | Yes            |
| PATCH  | `/tasks/<id>` | Partially update a task | Yes            |
| DELETE | `/tasks/<id>` | Delete a task           | Yes            |
Example
Create a task

Request:
POST /tasks
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "title": "Study Complex Analysis",
    "description": "Review MMP and Liouville"
}
Response:
{
    "message": "Task created",
    "task_id": 1
}
Validation

Task requests are validated using Pydantic schemas.

Invalid input returns a structured error response instead of being passed
directly to the database.

Error Handling

The API handles common errors including:

400 Bad Request
401 Unauthorized
404 Not Found
500 Internal Server Error

Responses are returned as JSON.

Testing

The project uses Pytest for automated API testing.

Run the test suite with:

pytest -v

Current test result:

18 passed

The tests cover authentication, task CRUD operations, validation,
authentication requirements, user ownership, and error cases.

Setup
1. Clone the repository
git clone <your-repository-url>
cd task-manager-API
2. Create a virtual environment
python -m venv .venv
3. Activate the virtual environment

Windows PowerShell:

.venv\Scripts\Activate.ps1
4. Install dependencies
pip install -r requirements.txt
5. Configure environment variables

Create a .env file:

FLASK_DEBUG=True
JWT_SECRET_KEY=your-secret-key

Do not commit .env to Git.

6. Run the application
python app.py

The API will be available at:

http://127.0.0.1:5000
Project Goal

This project was built as a practical way to learn backend development
and understand how authentication, databases, validation, API design,
security, and automated testing work together in a real application.
