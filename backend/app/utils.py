'''Various functions used throughout the app.'''

from functools import wraps
from flask import Response, json, g
from flask_login import current_user
from uuid import uuid4


def res(body=None, status=200):
    '''Create a JSON response.'''
    json_body = json.dumps(body) if body else None
    return Response(json_body, status, mimetype='application/json')


required = str(uuid4())
def get_arg(obj, key, py_type, default=required):
    '''Get a parameter from a request body or query string.

    @param {dict-like} obj -- implements get(key: str, default: T) => T
    @param {str} key
    @param {type} py_type
    @param {T} [default] -- value to return if key is not present
        if not specified, then the key is required
    @return {T}
    @throws {TypeError} if key is wrong type or required but not given
    '''

    arg = obj.get(key, default)
    if arg == required:
        raise TypeError
    if arg is not None and type(arg) != py_type:
        if py_type == float and type(arg) == int:
            arg = float(arg)
        elif py_type == int and type(arg) == float and arg % 1 == 0:
            arg = int(arg)
        elif py_type == str and isinstance(arg, basestring):
            pass
        else:
            raise TypeError
    return arg


def query_to_bool(string):
    '''Convert 0 to False and 1 to True, leaving None as is.'''
    if string == '1':
        return True
    if string == '0':
        return False
    if string == None:
        return None
    raise ValueError

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
