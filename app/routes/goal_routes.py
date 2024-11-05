from flask import Blueprint, abort, make_response, request

from app.models.task import Task

from ..db import db
from ..models.goal import Goal
from constants import TITLE, GOAL, DETAILS
from .route_utilities import create_model, get_models_with_filters, validate_model

bp = Blueprint('goals_bp', __name__, url_prefix='/goals')

@bp.post('')
def create_goal():
    request_body = request.get_json()
    return create_model(Goal, request_body)

@bp.get('')
def get_all_goals():
    return get_models_with_filters(Goal, request.args)

@bp.get('/<goal_id>')
def get_one_goal(goal_id):
    return {GOAL: validate_model(Goal, (goal_id)).to_dict()}

@bp.put('/<goal_id>')
def update_goal(goal_id):
    goal = validate_model(Goal, (goal_id))
    request_body = request.get_json()

    goal.title = request_body[TITLE]

    db.session.commit()

    return {GOAL: goal.to_dict()}

@bp.delete('/<goal_id>')
def delete_goal(goal_id):
    goal = validate_model(Goal, (goal_id))

    db.session.delete(goal)
    db.session.commit()

    return {DETAILS: f'Goal {goal_id} "{goal.title}" successfully deleted'}

@bp.get('/<goal_id>/tasks')
def get_tasks_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return {
        'id': goal.id,
        'title': goal.title,
        'tasks': [task.to_dict() for task in goal.tasks]
    }
    
@bp.post('/<goal_id>/tasks')
def create_task_with_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    request_body = request.get_json()

    if 'task_ids' not in request_body:
        abort(make_response({'details': 'Missing task_ids'}, 400))
    
    task_ids = request_body['task_ids']

    if not isinstance(task_ids, list):
        abort(make_response({'details': 'task_ids must be a list'}), 400)
    
    tasks = []
    for task_id in task_ids:
        task = validate_model(Task, task_id)
        task.goal_id = goal.id
        tasks.append(task)

    db.session.add_all(tasks)
    db.session.commit()

    return make_response({
        'id': goal.id,
        'task_ids': task_ids
    }, 200)