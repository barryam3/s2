"""Various functions used throughout the app."""

from functools import wraps
from flask import Response, json

from flask_login import current_user

def res(body, status=200):
    """Create a JSON response."""
    json_body = json.dumps(body)
    return Response(json_body, status=status, mimetype='application/json')

def login_required(func):
    """Verify that a user is authenticated."""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return res("Authentication required.", 401)
        return func(*args, **kwargs)
    return decorated_function

def current_required(func):
    """Verify that the authenticated user is a current member."""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return res("Authentication required.", 401)
        if not current_user.current:
            return res("Singing membership required.", 403)
        return func(*args, **kwargs)
    return decorated_function

def pitch_required(func):
    """Verify that the authenticated user is a pitch."""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return res("Authentication required.", 401)
        if not current_user.pitch:
            return res("Pitch priviliges required.", 403)
        return func(*args, **kwargs)
    return decorated_function
