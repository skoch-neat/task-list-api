from flask import Blueprint, request, abort, make_response
from constants import ID, TITLE, GOAL, ORDER_BY, DEFAULT_ORDER_BY, SORT, ASC, DESC, DEFAULT_SORT_ORDER, MESSAGE, DETAILS
from app.db import db
from app.models.goal import Goal

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
    query_params = validate_query_params(get_query_params())
    query = db.select(Goal)

    query = filter_query(query, query_params)
    query = sort_query(query, query_params)

    goals = db.session.scalars(query)

    return [goal.to_dict() for goal in goals]

@bp.get('/<int:goal_id>')
def get_one_goal(goal_id):
    return {GOAL: validate_goal(goal_id).to_dict()}

@bp.put('/<int:goal_id>')
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    goal.title = request_body[TITLE]

    db.session.commit()

    return {GOAL: goal.to_dict()}

@bp.delete('/<int:goal_id>')
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {DETAILS: f'Goal {goal_id} "{goal.title}" successfully deleted'}

def get_query_params():
    return {
        ID: request.args.get(ID),
        TITLE: request.args.get(TITLE),
        ORDER_BY: request.args.get(ORDER_BY, DEFAULT_ORDER_BY),
        SORT: request.args.get(SORT, DEFAULT_SORT_ORDER).lower()
    }

def filter_query(query, params):
    if params[ID]:
        query = query.where(Goal.id == params[ID])

    if params[TITLE]:
        query = query.where(Goal.title == params[TITLE])

    return query

def sort_query(query, params):
    order_by_param = params.get(ORDER_BY, DEFAULT_ORDER_BY)
    sort_order = params.get(SORT, DEFAULT_SORT_ORDER)

    if sort_order not in [ASC, DESC]:
        abort(make_response({MESSAGE: f'Sort order {sort_order} invalid'}, 400))

    try:
        order_column = getattr(Goal, order_by_param)
    except AttributeError:
        abort(make_response({MESSAGE: f'Order by {order_by_param} invalid'}, 400))

    if sort_order == ASC:
        query = query.order_by(order_column.asc())
    else:
        query = query.order_by(order_column.desc())

    return query

def validate_cast_type(value, target_type, param_name):
    try:
        return target_type(value)
    except (ValueError, TypeError):
        abort(make_response({MESSAGE: f'{param_name} {value} invalid'}, 400))

def validate_goal(goal_id):
    goal_id = validate_cast_type(goal_id, int, ID)
    query = db.select(Goal).where(Goal.id == goal_id)
    goal = db.session.scalar(query)

    if not goal:
        abort(make_response({DETAILS: f'Goal {goal_id} not found'}, 404))

    return goal

def validate_query_params(params):
    for key, value in params.items():
        if key == ID and value:
            params[key] = validate_cast_type(value, int, ID)

    return params