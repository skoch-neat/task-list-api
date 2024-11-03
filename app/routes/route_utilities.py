from flask import abort, make_response, request

from ..db import db
from constants import (
    ID, TITLE, DESCRIPTION, ORDER_BY, DEFAULT_ORDER_BY, SORT,
    DEFAULT_SORT_ORDER, ASC, DESC, DETAILS, MESSAGE, 
    QUERY_PARAMS_AND_TYPES
)

def get_and_validate_query_params():
    expected_params = list(QUERY_PARAMS_AND_TYPES.keys())
    expected_types = list(QUERY_PARAMS_AND_TYPES.values())

    query_params = get_query_params(expected_params)
    return validate_query_params(query_params, expected_types)

def get_query_params(expected_params):
    return {key: request.args.get(key) for key in expected_params}

def filter_and_sort_query(query, params, cls):
    query = filter_query(query, params, cls)
    return sort_query(query, params, cls)

def filter_query(query, params, cls):
    if params.get(ID):
        query = query.where(cls.id == params[ID])

    if params.get(TITLE):
        query = query.where(cls.title == params[TITLE])

    if params.get(DESCRIPTION):
        query = query.where(cls.description.ilike(f'%{params[DESCRIPTION]}%'))

    return query

def sort_query(query, params, cls):
    order_by_param = params.get(ORDER_BY, DEFAULT_ORDER_BY)
    sort_order = params.get(SORT, DEFAULT_SORT_ORDER)

    if sort_order not in [ASC, DESC]:
        abort(make_response({MESSAGE: f'Sort order {sort_order} invalid'}, 400))

    try:
        order_column = getattr(cls, order_by_param)
    except AttributeError:
        abort(make_response({MESSAGE: f'Order by {order_by_param} invalid'}, 400))

    if sort_order == ASC:
        query = query.order_by(order_column.asc())
    else:
        query = query.order_by(order_column.desc())

    return query

def validate_cast_type(value, target_type):
    value_name = value.__class__.__name__
    try:
        return target_type(value)
    except (ValueError, TypeError):
        abort(make_response({DETAILS: f'{value_name} {value} invalid'}, 400))

def validate_model(cls, model_id):
    model_id = validate_cast_type(model_id, int)

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        abort(make_response({DETAILS: f'{cls.__name__} {model_id} not found'}, 404))

    return model

def validate_query_params(params, expected_types):
    validated_params = {}
    for param, expected_type in zip(params.keys(), expected_types):
        value = params.get(param)
        if value is not None:
            validated_params[param] = validate_cast_type(value, expected_type)
    return validated_params