from flask import Blueprint, current_app, request, abort
from flask_login import login_user, login_required, logout_user

from app.extensions import lm
from app.models.user import User
from app.utils import send_success_response, send_error_response

auth = Blueprint('auth', __name__)

@lm.user_loader
def load_user(id):
    return User.get_by_id(int(id))

@auth.route('/login', methods=['POST'])
def login():
    user_data = request.get_json()
    user = User.query.filter_by(athena=user_data['username']).first()
    if user and user.check_password(user_data['password']):
        login_user(user)
        return send_success_response(user.to_dict())
    return send_error_response(403, 'Incorrect login.')

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return send_success_response(True)
