from flask import abort, make_response, request

from ..db import db
from constants import (
    ID, TITLE, DESCRIPTION, ORDER_BY, DEFAULT_ORDER_BY, SORT,
    DEFAULT_SORT_ORDER, ASC, DESC, DETAILS, MESSAGE, 
    QUERY_PARAMS_AND_TYPES
)

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    except KeyError:
        response = {'details': 'Invalid data'}
        abort(make_response(response, 400))

    db.session.add(new_model)
    db.session.commit()

    return {cls.__name__.lower(): new_model.to_dict()}, 201

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

def get_models_with_filters(cls, filters=None):
    query = db.select(cls)

    if filters:
        for attribute, value in filters.items():
            if hasattr(cls, attribute):
                query = query.where(getattr(cls, attribute).ilike(f'%{value}%'))

    query = sort_query(cls, query, filters)

    models = db.session.scalars(query.order_by(cls.id))

    return [model.to_dict() for model in models]

def sort_query(cls, query, filters=None):
    order_by_param = filters.get(ORDER_BY, DEFAULT_ORDER_BY)
    sort_order = filters.get(SORT, DEFAULT_SORT_ORDER)

    if sort_order not in [ASC, DESC]:
        response = {MESSAGE: f'Sort order {sort_order} invalid'}
        abort(make_response(response, 400))

    try:
        order_column = getattr(cls, order_by_param)
    except AttributeError:
        response = {MESSAGE: f'Order by {order_by_param} invalid'}
        abort(make_response(response, 400))

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
        response = {DETAILS: f'{value_name} {value} invalid'}
        abort(make_response(response, 400))

def validate_model(cls, model_id):
    model_id = validate_cast_type(model_id, int)

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        response = {DETAILS: f'{cls.__name__} {model_id} not found'}
        abort(make_response(response, 404))

    return model

def validate_query_params(params, expected_types):
    validated_params = {}

    for param, expected_type in zip(params.keys(), expected_types):
        value = params.get(param)
        if value is not None:
            validated_params[param] = validate_cast_type(value, expected_type)

    return validated_params