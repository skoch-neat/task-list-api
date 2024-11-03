import os
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv
from flask import Blueprint, abort, make_response, request

from ..db import db
from ..models.task import Task
from constants import (
    TITLE, DESCRIPTION, COMPLETED_AT, TASK, DETAILS,
    )
from .route_utilities import (
    get_and_validate_query_params, filter_and_sort_query, validate_model
    )

load_dotenv()

bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')

SLACKBOT_TOKEN = os.getenv('SLACKBOT_TOKEN')

@bp.post('')
def create_task():
    request_body = request.get_json()

    try:
        new_task = Task.from_dict(request_body)
    except KeyError:
        response = {DETAILS: "Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_task)
    db.session.commit()

    return {TASK: new_task.to_dict()}, 201

@bp.get('')
def get_all_tasks():
    query_params = get_and_validate_query_params()

    query = db.select(Task)
    
    query = filter_and_sort_query(query, query_params, Task)

    tasks = db.session.scalars(query)

    return [task.to_dict() for task in tasks]

@bp.get('/<task_id>')
def get_one_task(task_id):
    return {TASK: validate_model(Task, (task_id)).to_dict()}

@bp.put('/<task_id>')
def update_task(task_id):
    task = validate_model(Task, (task_id))
    request_body = request.get_json()

    task.title = request_body[TITLE]
    task.description = request_body[DESCRIPTION]
    task.completed_at = request_body.get(COMPLETED_AT)

    db.session.commit()

    return {TASK: task.to_dict()}

@bp.patch('/<task_id>/mark_complete')
def update_task_complete(task_id):
    task = validate_model(Task, (task_id))

    task.completed_at = datetime.now(timezone.utc)
    db.session.commit()

    channel = 'api-test-channel'
    message = f'Someone just completed the task {task.title}'
    send_slack_message(channel, message)

    return {TASK: task.to_dict()}

@bp.patch('/<task_id>/mark_incomplete')
def update_task_incomplete(task_id):
    task = validate_model(Task, (task_id))

    task.completed_at = None

    db.session.commit()

    return {TASK: task.to_dict()}

@bp.delete('/<task_id>')
def delete_task(task_id):
    task = validate_model(Task, (task_id))

    db.session.delete(task)
    db.session.commit()

    return {DETAILS: f'Task {task_id} "{task.title}" successfully deleted'}

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