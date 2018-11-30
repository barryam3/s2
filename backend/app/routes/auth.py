'''Authentication route handlers'''

from flask import Blueprint, request
from flask_login import login_user, logout_user, UserMixin
from sqlalchemy.orm.exc import NoResultFound

from app.extensions import lm, bcrypt
from app.utils import res, get_arg, login_required
from app.models.user import User

auth = Blueprint('auth', __name__)

@lm.user_loader
def load_user(user_id):
    '''Get User object by id.

    Required for flask_login.'''

    return User.query.filter_by(id=user_id).one()


@auth.route('/login', methods=['POST'])
def login():
    '''Start a session.

    @param {str} username
    @param {str} password
    @return {User} - logged-in user
    @throws {401} - if your athena & password are not correct
    '''

    req_body = request.get_json()
    try:
        username = get_arg(req_body, 'username', str)
        password = get_arg(req_body, 'password', str)
    except TypeError:
        return res(status=400)

    try:
        user = User.query.filter_by(username=username).one()
        if user.check_password(password):
            login_user(user)
            return res(user.to_dict())
    except NoResultFound:
        pass

    return res('Incorrect login.', 401)


@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    '''End your session.

    @return {bool} - success
    @throws {401} - if you are not logged in
    '''

    logout_user()
    return res(True)
