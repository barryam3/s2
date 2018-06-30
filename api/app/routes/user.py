from flask import Blueprint, current_app, request, abort
from flask_login import login_required, current_user

from app.models.user import User
from app.utils import send_success_response, send_error_response

user = Blueprint('user', __name__)

@user.route('/<id>/password', methods=['PUT', 'DELETE'])
@login_required
def change_password(id):
    newPassword = 'xprod05'
    if request.method == 'DELETE' and not current_user.pitch:
        return send_error_response(403, 'Only a pitch can reset passwords.')
    if request.method == 'PUT':
        data = request.get_json()
        oldPassword = data['oldPassword']
        newPassword = data['newPassword']
        if not current_user.get_id() == id:
            msg = "You cannot change another user's password."
            return send_error_response(403, msg)
        if not current_user.check_password(oldPassword):
            return send_error_response(403, "Incorrect current password.")
    user = User.query.filter_by(id=id).first()
    user.set_password(newPassword)
    user.save()
    return send_success_response(True)

@user.route('/', methods=['GET'])
@login_required
def get_users():
    if not current_user.pitch:
        return send_error_response(403, "Only a pitch can enumerate users.")
    users = User.query.with_entities(User.id, User.name).all()
    users_list = [{"id": u[0], "name": u[1]} for u in users]
    return send_success_response(users_list)

@user.route('/current', methods=['GET'])
@login_required
def get_current_user():
    return send_success_response(current_user.to_dict())
