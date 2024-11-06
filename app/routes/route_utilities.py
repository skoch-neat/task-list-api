from flask import abort, make_response, request

from ..db import db
from constants import (
    ORDER_BY, DEFAULT_ORDER_BY, SORT, DEFAULT_SORT_ORDER, ASC, DESC, DETAILS, MESSAGE, QUERY_PARAMS_AND_TYPES
)

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    except KeyError:
        abort(make_response({DETAILS: 'Invalid data'}, 400))

    db.session.add(new_model)
    db.session.commit()

    model_name = cls.__name__.lower()
    return {model_name: new_model.to_dict()}, 201

def get_and_validate_query_params():
    expected_params = list(QUERY_PARAMS_AND_TYPES.keys())
    expected_types = list(QUERY_PARAMS_AND_TYPES.values())

    query_params = get_query_params(expected_params)
    return validate_query_params(query_params, expected_types)

def get_query_params(expected_params):
    return {attribute: request.args.get(attribute) for attribute in expected_params}

def filter_and_sort_query(cls, query, filters):
    query = filter_query(cls, query, filters)
    return sort_query(cls, query, filters)

def filter_query(cls, query, filters):
    if filters:
        for attribute, value in filters.items():
            if hasattr(cls, attribute):
                query = query.where(getattr(cls, attribute).ilike(f'%{value}%'))
    return query

def get_models_with_filters(cls, filters):
    query = db.select(cls)
    query = filter_and_sort_query(cls, query, filters)
    models = db.session.scalars(query.order_by(cls.id))
    return [model.to_dict() for model in models]

def sort_query(cls, query, filters):
    order_by_param = filters.get(ORDER_BY, DEFAULT_ORDER_BY)
    sort_order = filters.get(SORT, DEFAULT_SORT_ORDER).casefold()

    if sort_order not in {ASC.casefold(), DESC.casefold()}:
        abort(make_response({MESSAGE: f'Sort order {sort_order} invalid'}, 400))

    try:
        order_column = getattr(cls, order_by_param)
    except AttributeError:
        abort(make_response({MESSAGE: f'Order by {order_by_param} invalid'}, 400))

    return query.order_by(order_column.asc()
            if sort_order == ASC.casefold() else order_column.desc())

def update_model(cls, instance, model_data):
    for attribute, value in model_data.items():
        if hasattr(cls, attribute):
            setattr(instance, attribute, value)
    db.session.commit()
    return instance

def validate_cast_type(value, target_type):
    value_name = type(value).__name__
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