from flask import Blueprint, request

from ..db import db
from ..models.goal import Goal
from constants import TITLE, GOAL, DETAILS
from .route_utilities import (
    get_and_validate_query_params, filter_and_sort_query, validate_model
    )

bp = Blueprint('goals_bp', __name__, url_prefix='/goals')

@bp.post('')
def create_goal():
    request_body = request.get_json()

    if TITLE not in request_body:
        return {DETAILS: 'Invalid data'}, 400
    
    new_goal = Goal.from_dict(request_body)
    db.session.add(new_goal)
    db.session.commit()

    return {GOAL: new_goal.to_dict()}, 201

@bp.get('')
def get_all_goals():
    query_params = get_and_validate_query_params()

    query = db.select(Goal)

    query = filter_and_sort_query(query, query_params, Goal)

    goals = db.session.scalars(query)

    return [goal.to_dict() for goal in goals]

@bp.get('/<int:goal_id>')
def get_one_goal(goal_id):
    return {GOAL: validate_model(Goal, (goal_id)).to_dict()}

@bp.put('/<int:goal_id>')
def update_goal(goal_id):
    goal = validate_model(Goal, (goal_id))
    request_body = request.get_json()

    goal.title = request_body[TITLE]

    db.session.commit()

    return {GOAL: goal.to_dict()}

@bp.delete('/<int:goal_id>')
def delete_goal(goal_id):
    goal = validate_model(Goal, (goal_id))

    db.session.delete(goal)
    db.session.commit()

    return {DETAILS: f'Goal {goal_id} "{goal.title}" successfully deleted'}