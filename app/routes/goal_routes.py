from flask import Blueprint, request

from app.models.task import Task

from ..db import db
from ..models.goal import Goal
from constants import DETAILS, GOAL, ID, TASK_IDS, TASKS, TITLE
from .route_utilities import create_model, get_models_with_filters, validate_model

bp = Blueprint('goals_bp', __name__, url_prefix='/goals')

@bp.post('')
def create_goal():
    request_body = request.get_json()
    return create_model(Goal, request_body)

@bp.post('/<goal_id>/tasks')
def create_task_with_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    task_ids = request_body.get(TASK_IDS, [])
    tasks = [validate_model(Task, task_id) for task_id in task_ids]
    goal.tasks.extend(tasks)

    db.session.commit()

    return {
        ID: goal.id,
        TASK_IDS: task_ids
    }

@bp.get('')
def get_all_goals():
    return get_models_with_filters(Goal, request.args)

@bp.get('/<goal_id>')
def get_one_goal(goal_id):
    return {GOAL: validate_model(Goal, (goal_id)).to_dict()}

@bp.get('/<goal_id>/tasks')
def get_tasks_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return {
        ID: goal.id,
        TITLE: goal.title,
        TASKS: [task.to_dict() for task in goal.tasks]
    }

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