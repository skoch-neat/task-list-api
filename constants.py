'''
Constants for the Task List API
'''

# Model attribute keys
ID = 'id'
TITLE = 'title'
DESCRIPTION = 'description'
COMPLETED_AT = 'completed_at'
IS_COMPLETE = 'is_complete'
GOAL_ID = 'goal_id'
TASK_ID = 'task_id'

#  keys
GOAL = 'goal'
TASK = 'task'
DETAILS = 'details'
SORT = 'sort'
MESSAGE = 'message'

# Query params
ORDER_BY = 'order_by'
ASC = 'asc'
DESC = 'desc'
DEFAULT_ORDER_BY = TITLE
DEFAULT_SORT_ORDER = ASC
QUERY_PARAMS_AND_TYPES = {
    ORDER_BY: type(ORDER_BY),
    SORT: type(SORT)
}