from functools import wraps
from flask import Response, json
from extensions import mysql

from flask_login import current_user, login_required

def res(body={}, status=200):
    json_body = json.dumps(body)
    return Response(json_body, status=status, mimetype='application/json')

@login_required
def pitch_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.pitch:
            return res("Only a pitch can complete this action.", 403)
        return f(*args, **kwargs)
    return decorated_function