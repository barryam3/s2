'''Various functions used throughout the app.'''

from functools import wraps
from flask import Response, json, g

from flask_login import current_user

def res(body, status=200):
    '''Create a JSON response.'''
    json_body = json.dumps(body)
    return Response(json_body, status=status, mimetype='application/json')

def query_to_bool(string):
    '''Convert 0 to False and 1 to True, leaving None as is.'''
    if string is None:
        return None
    return bool(int(string))

def login_required(func):
    '''Verify that a user is authenticated.'''
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return res('Authentication required.', 401)
        return func(*args, **kwargs)
    return decorated_function

def active_required(func):
    '''Verify that the authenticated user is a current member.'''
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return res('Authentication required.', 401)
        if not current_user.active:
            return res('Active membership required.', 403)
        return func(*args, **kwargs)
    return decorated_function

def admin_required(func):
    '''Verify that the authenticated user is a pitch.'''
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return res('Authentication required.', 401)
        if not current_user.admin:
            return res('Admin priviliges required.', 403)
        return func(*args, **kwargs)
    return decorated_function

def login_required(func):
    '''Verify that a user is authenticated.'''
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return res('Authentication required.', 401)
        return func(*args, **kwargs)
    return decorated_function
