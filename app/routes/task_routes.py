import os
import requests
from datetime import datetime, timezone
from flask import Blueprint, abort, make_response, request
from constants import ID, TITLE, DESCRIPTION, COMPLETED_AT, ORDER_BY, ASC, DESC, DEFAULT_ORDER_BY, DEFAULT_SORT_ORDER, TASK, DETAILS, SORT, MESSAGE
from app.db import db
from app.models.task import Task
from dotenv import load_dotenv

load_dotenv()

tasks_bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')

SLACKBOT_TOKEN = os.getenv('SLACKBOT_TOKEN')

@tasks_bp.post('')
def create_task():
    request_body = request.get_json()

    if TITLE not in request_body or DESCRIPTION not in request_body:
        return {DETAILS: 'Invalid data'}, 400

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return {TASK: new_task.to_dict()}, 201

@tasks_bp.get('')
def get_all_tasks():
    query_params = validate_query_params(get_query_params())
    query = db.select(Task)
    
    query = filter_query(query, query_params)
    query = sort_query(query, query_params)

    tasks = db.session.scalars(query)

    return [task.to_dict() for task in tasks]

@tasks_bp.get('/<task_id>')
def get_one_task(task_id):
    return {TASK: validate_task(task_id).to_dict()}

@tasks_bp.put('/<task_id>')
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body[TITLE]
    task.description = request_body[DESCRIPTION]
    task.completed_at = request_body.get(COMPLETED_AT)

    db.session.commit()

    return {TASK: task.to_dict()}

@tasks_bp.patch('/<task_id>/mark_complete')
def update_task_complete(task_id):
    task = validate_task(task_id)

    task.completed_at = datetime.now(timezone.utc)
    db.session.commit()

    channel = 'task-notifications'
    message = f'Someone just completed the task {task.title}'
    send_slack_message(channel, message)

    return {TASK: task.to_dict()}

@tasks_bp.patch('/<task_id>/mark_incomplete')
def update_task_incomplete(task_id):
    task = validate_task(task_id)

    task.completed_at = None

    db.session.commit()

    return {TASK: task.to_dict()}

@tasks_bp.delete('/<task_id>')
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return {DETAILS: f'Task {task_id} "{task.title}" successfully deleted'}

def get_query_params():
    return {
        ID: request.args.get(ID),
        TITLE: request.args.get(TITLE),
        DESCRIPTION: request.args.get(DESCRIPTION),
        COMPLETED_AT: request.args.get(COMPLETED_AT),
        ORDER_BY: request.args.get(ORDER_BY, DEFAULT_ORDER_BY),
        SORT: request.args.get(SORT, DEFAULT_SORT_ORDER).lower()
    }

def filter_query(query, params):
    if params[ID]:
        query = query.where(Task.id == params[ID])

    if params[TITLE]:
        query = query.where(Task.title == params[TITLE])

    if params[DESCRIPTION]:
        query = query.where(Task.description.ilike(f'%{params[DESCRIPTION]}%'))

    if params.get(COMPLETED_AT):
        query = query.where(Task.completed_at == params[COMPLETED_AT])

    return query

def sort_query(query, params):
    order_by_param = params.get(ORDER_BY, DEFAULT_ORDER_BY)
    sort_order = params.get(SORT, DEFAULT_SORT_ORDER)

    if sort_order not in [ASC, DESC]:
        abort(make_response({MESSAGE: f'Sort order {sort_order} invalid'}, 400))

    try:
        order_column = getattr(Task, order_by_param)
    except AttributeError:
        abort(make_response({MESSAGE: f'Order by {order_by_param} invalid'}, 400))

    if sort_order == ASC:
        query = query.order_by(order_column.asc())
    else:
        query = query.order_by(order_column.desc())

    return query

def send_slack_message(channel, message):
    url = 'https://slack.com/api/chat.postMessage'
    headers = {
        'Authorization': f'Bearer {SLACKBOT_TOKEN}'
    }
    body = {
    'channel': channel,
    'text': message
    }

    response = requests.post(url, json=body, headers=headers)    
    if response.json().get('ok') is True:
        return response.json()
    else:
        print(f"Error sending message: {response.json()}")

def validate_cast_type(value, target_type, param_name):
    try:
        return target_type(value)
    except (ValueError, TypeError):
        abort(make_response({MESSAGE: f'{param_name} {value} invalid'}, 400))

def validate_query_params(params):
    for key, value in params.items():
        if key == ID and value:
            params[key] = validate_cast_type(value, int, ID)
        elif key == COMPLETED_AT and value:
            params[key] = validate_cast_type(value, str, COMPLETED_AT)

    return params

def validate_task(task_id):
    task_id = validate_cast_type(task_id, int, ID)
    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)

    if not task:
        abort(make_response({DETAILS: f'Task {task_id} not found'}, 404))
    
    return task