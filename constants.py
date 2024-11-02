'''
Constants for the Task List API
'''

# Constants for query parameter keys
ID = 'id'
TITLE = 'title'
DESCRIPTION = 'description'
COMPLETED_AT = 'completed_at'
IS_COMPLETE = 'is_complete'
ORDER_BY = 'order_by'

# Sort options
ASC = 'asc'
DESC = 'desc'

# Default values
DEFAULT_ORDER_BY = TITLE
DEFAULT_SORT_ORDER = ASC

# Response body keys
GOAL = 'goal'
TASK = 'task'
DETAILS = 'details'
SORT = 'sort'
MESSAGE = 'message'