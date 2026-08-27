from flask import Blueprint, request
from pydantic import ValidationError
from schemas import TaskCreate, TaskUpdate, TaskPatch
from services.task_service import get_all_tasks, get_task_by_id , create_task, update_task, patch_task, delete_task
from flask_jwt_extended import jwt_required, get_jwt_identity

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    tasks = get_all_tasks()

    return {"tasks": tasks}

@tasks_bp.route("/tasks", methods=["POST"])
@jwt_required()
def create_task_route():
    data = request.get_json()

    try:
        task = TaskCreate.model_validate(data)
    except ValidationError as e:
        return {
            "error": "Invalid task data",
            "details": e.errors()
        }, 400
    task_id = create_task(
        task.title,
        task.description
    )

    return {
        "message": "Task created",
        "task_id": task_id
    }, 201

@tasks_bp.route("/tasks/<int:task_id>", methods=["GET"])
@jwt_required()
def get_task(task_id):
    task = get_task_by_id(task_id)

    if task is None:
        return {"error": "Task not found"}, 404

    return {"task":task}


@tasks_bp.route("/tasks/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task_route(task_id):
    data = request.get_json()
    try:
        task_update = TaskUpdate.model_validate(data)
    except ValidationError as e:
        return {"error": "Invalid task data",
                "details": e.errors()}, 400

    task = get_task_by_id(task_id)

    if task is None:
        return {"error": "Task not found"}, 404

    update_task(task_id, task_update.title, task_update.description, task_update.completed)

    return {
        "message": "Task updated"
    }




@tasks_bp.route("/tasks/<int:task_id>", methods=["PATCH"])
@jwt_required()
def patch_task_route(task_id):
    data = request.get_json()

    try:
        task_data = TaskPatch.model_validate(data)
    except ValidationError as e:
        return {
            "error": "Invalid task data",
            "details": e.errors()
        }, 400

    task = get_task_by_id(task_id)

    if task is None:
        return {"error": "Task not found"}, 404

    updates = task_data.model_dump(exclude_unset=True)

    patch_task(task_id, updates)

    return {
        "message": "Task updated"
    }


@tasks_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    task = get_task_by_id(task_id)

    if task is None:
        return {"error": "Task not found"}, 404

    delete_task(task_id)

    return {"message": "Task deleted"}
