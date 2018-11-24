from functools import wraps
from flask import Response, json
from app.extensions import mysql

from flask_login import current_user

def res(body={}, status=200):
    json_body = json.dumps(body)
    return Response(json_body, status=status, mimetype='application/json')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return res("Authentication required.", 401)
        return f(*args, **kwargs)
    return decorated_function

def current_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return res("Authentication required.", 401)
        if not current_user.current:
            return res("Singing membership required.", 403)
        return f(*args, **kwargs)
    return decorated_function

def pitch_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return res("Authentication required.", 401)
        if not current_user.pitch:
            return res("Pitch priviliges required.", 403)
        return f(*args, **kwargs)
    return decorated_function