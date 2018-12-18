'''Route hanlders beginning with /users.'''

from flask import Blueprint, request
from flask_login import current_user
from sqlalchemy.orm.exc import NoResultFound

from app.extensions import db
from app.utils import res, get_arg, login_required, admin_required
from app.models.user import User


users = Blueprint('users', __name__)


@users.route('', methods=['GET'])
@admin_required
def list_users():
    '''Enumerate all users.

    @return {User[]} - all users' info
    @throws {401} - if you are not logged in
    @throws {403} - if you are not a pitch
    '''

    return res([u.to_dict() for u in User.query.all()])


@users.route('/me', methods=['GET'])
@login_required
def get_active_user():
    '''Get your info.

    @return {User} - your info
    @throws {401} - if you are not logged in
    '''

    return res(current_user.to_dict(True))


@users.route('/me/password', methods=['PUT'])
@login_required
def update_password():
    '''Change your password.

    @param {str} oldPassword - your current password
    @param {str} newPassword - your new password

    @return {boolean} - success
    @return {400} - if the new password is not at least six characters long
    @return {401} - if your current password is not correct
    @throws {401} - if you are not logged in
    '''

    req_body = request.get_json()
    try:
        old_pass = get_arg(req_body, 'oldPassword', str)
        new_pass = get_arg(req_body, 'newPassword', str)
    except TypeError:
        return res(status=400)

    if not current_user.check_password(old_pass):
        return res('Incorrect current password.', 401)

    if len(new_pass) < 6:
        return res('Password must be at least six characters.', 400)

    current_user.set_password(new_pass)
    return res(True)


@users.route('/<user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    '''Delete a user.

    @return {boolean} - success
    @throws {401} - if you are not logged in
    @throws {403} - if you are not a pitch
    @throws {403} - if you are trying to delete yourself
    @throws {404} - if the user is not found
    '''

    try:
        user_id = int(user_id)
    except ValueError:
        return res('User not found.', 404)

    if user_id == current_user.id:
        return res('You cannot delete yourself.', 403)

    try:
        user = User.query.filter_by(id=user_id).one()
    except NoResultFound:
        return res('User not found.', 404)

    db.session.delete(user)
    db.session.commit()
    return res(True)


@users.route('/<user_id>/password', methods=['DELETE'])
@admin_required
def reset_password(user_id):
    '''Reset a user's password to 'xprod05'.

    @return {boolean} - success
    @throws {401} - if you are not logged in
    @throws {403} - if you are not a pitch
    @throws {404} - if the user is not found
    '''

    try:
        user_id = int(user_id)
        user = User.query.filter_by(id=user_id).one()
    except (ValueError, NoResultFound) as e:
        return res('User not found.', 404)

    user.set_password('xprod05')
    return res(True)


@users.route('/<user_id>', methods=['PATCH'])
@admin_required
def set_active(user_id):
    '''Give/remove active member / admin powers.

    @param {bool} active
    @param {bool} admin
    @return {bool} - success
    @throws {401} - if you are not logged in
    @throws {403} - if you are not a pitch
    @throws {403} - if you are trying to change your own priviliges
    @throws {404} - if the user is not found
    '''

    try:
        user_id = int(user_id)
    except ValueError:
        return res('User not found.', 404)

    req_body = request.get_json()
    try:
        active = get_arg(req_body, 'active', bool, None)
        admin = get_arg(req_body, 'admin', bool, None)
    except TypeError:
        return res(status=400)

    if user_id == current_user.id:
        return res('You cannot change your own priviliges.', 403)

    try:
        user = User.query.filter_by(id=user_id).one()
    except NoResultFound:
        return res('User not found.', 404)
    
    if active is not None:
        user.active = active
    if admin is not None:
        user.admin = admin

    db.session.commit()
    return res(True)


@users.route('', methods=['POST'])
@admin_required
def add_user():
    '''Add a user.

    @param {str} username - the member's kerberos
    @return {int} - id of the new user
    @throws {400} if athena is not a valid kerberos
    @throws {401} - if you are not logged in
    @throws {403} - if you are not a pitch
    '''

    req_body = request.get_json()
    try:
        username = get_arg(req_body, 'username', str)
    except TypeError:
        return res(status=400)

    if not ((3 <= len(username) <= 8) and username.isalnum()):
        return res('You must supply a valid kerberos.', 400)

    # create the new user
    user = User(username, 'xprod05')
    db.session.add(user)
    db.session.commit()

    return res(user.to_dict())
