from flask import Blueprint, request
from pydantic import ValidationError

from database import get_db_connection
from schemas import UserRegister, UserLogin
from services.auth_service import hash_password, verify_password
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = UserRegister(**request.get_json())
    except ValidationError as e:
        return {"errors": e.errors()}, 400

    password_hash = hash_password(data.password)

    connection = get_db_connection()

    try:
        connection.execute(
            """
            INSERT INTO users (email, password_hash)
            VALUES (?, ?)
            """,
            (data.email, password_hash)
        )

        connection.commit()

    except Exception:
        connection.close()
        return {"error": "Email already exists"}, 409

    connection.close()

    return {
        "message": "User registered successfully"
    }, 201

@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = UserLogin(**request.get_json())
    except ValidationError as e:
        return {"errors": e.errors()}, 400

    connection = get_db_connection()

    user = connection.execute(
        """
        SELECT * FROM users
        WHERE email = ?
        """,
        (data.email,)
    ).fetchone()

    connection.close()

    if user is None:
        return {"error": "Invalid email or password"}, 401

    if not verify_password(data.password, user["password_hash"]):
        return {"error": "Invalid email or password"}, 401
    access_token = create_access_token(identity=str(user["id"]))

    return {
        "message": "Login successful",
        "user_id": user["id"],
        "access_token": access_token
    }, 200