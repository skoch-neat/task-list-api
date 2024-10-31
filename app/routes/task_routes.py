from flask import Blueprint, abort, make_response, request, Response
from constants import ID, TITLE, DESCRIPTION, COMPLETED_AT, ORDER_BY, MESSAGE, MIMETYPE_JSON
from app.db import db
from app.models.task import Task

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()

    if TITLE not in request_body or DESCRIPTION not in request_body:
        return {"details": "Invalid data"}, 400

    new_task = Task(
        title=request_body[TITLE],
        description=request_body[DESCRIPTION],
        completed_at=request_body.get(COMPLETED_AT)
    )

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201

@tasks_bp.get('')
def get_all_tasks():
    query_params = get_query_params()
    query = db.select(Task)
    query = filter_query(query, query_params)

    order_by_param = request.args.get(ORDER_BY)
    if order_by_param:
        query = validate_order_by_param(query, order_by_param)
    else:
        query = query.order_by(Task.id)

    tasks = db.session.scalars(query)

    return [task.to_dict() for task in tasks]

@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    return {"task": validate_task(task_id).to_dict()}

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body[TITLE]
    task.description = request_body[DESCRIPTION]
    task.completed_at = request_body.get(COMPLETED_AT)

    db.session.commit()

    return {"task": task.to_dict()}, 200

def get_query_params():
    return {
        ID: request.args.get(ID),
        TITLE: request.args.get(TITLE),
        DESCRIPTION: request.args.get(DESCRIPTION),
        COMPLETED_AT: request.args.get(COMPLETED_AT)
    }

def filter_query(query, params):
    if params[ID]:
        query = query.where(Task.id == validate_cast_type(params[ID], int, ID))

    if params[TITLE]:
        query = query.where(Task.title == params[TITLE])

    if params[DESCRIPTION]:
        query = query.where(Task.description.ilike(f"%{params[DESCRIPTION]}%"))

    if params.get(COMPLETED_AT):
        query = query.where(Task.completed_at == params[COMPLETED_AT])

    return query

def validate_cast_type(value, target_type, param_TITLE):
    try:
        return target_type(value)
    except (ValueError, TypeError):
        abort(make_response({MESSAGE: f"{param_TITLE} '{value}' invalid"}, 400))

def validate_order_by_param(query, order_by_param):
    try:
        return query.order_by(getattr(Task, order_by_param))
    except AttributeError:
        abort(make_response({MESSAGE: f"{ORDER_BY} '{order_by_param}' invalid"}, 400))

def validate_task(task_id):
    task_id = validate_cast_type(task_id, int, ID)

    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)

    if not task:
        abort(make_response({MESSAGE: f"{ID} '{task_id}' not found"}, 404))
    
    return task