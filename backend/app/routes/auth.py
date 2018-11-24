"""Authentication route handlers"""

from flask import Blueprint, request
from flask_login import login_user, logout_user, UserMixin

from app.extensions import LM, MYSQL, BCRYPT
from app.utils import res, login_required

class User(UserMixin):
    """A class representing a user.

    Required for flask_login."""

    def __init__(self, user_info_dict):
        self.id = user_info_dict['id'] # pylint: disable=C0103
        self.username = user_info_dict['athena']
        self.password = user_info_dict['password']
        self.current = bool(user_info_dict['current'])
        self.pitch = bool(user_info_dict['pitch'])

    def to_dict(self):
        """Return a dictionary representation of the user."""

        return {
            "id": self.id,
            "athena": self.username,
            "current": self.current,
            "pitch": self.pitch
        }

AUTH = Blueprint('auth', __name__)

@LM.user_loader
def load_user(user_id):
    """Get User object by id.

    Required for flask_login."""

    cursor = MYSQL.get_db().cursor()
    query = "SELECT id, athena, current, pitch, password FROM user WHERE id = %s"
    cursor.execute(query, user_id)
    user = cursor.fetchone()
    return User(user)

@AUTH.route('/login', methods=['POST'])
def login():
    """Start a session.

    @param {str} athena
    @param {str} password
    @return {bool} - success
    @throws {401} - if your athena & password are not correct
    """

    body = request.get_json()
    cursor = MYSQL.get_db().cursor()
    query = "SELECT id, athena, current, pitch, password FROM user WHERE athena = %s"
    cursor.execute(query, body.get('athena', ''))
    user_data = cursor.fetchone()
    if user_data and BCRYPT.check_password_hash(user_data['password'], body.get('password', '')):
        user_obj = User(user_data)
        login_user(user_obj)
        return res(user_obj.to_dict())
    return res('Incorrect login.', 401)

@AUTH.route('/logout', methods=['POST'])
@login_required
def logout():
    """End your session.

    @return {bool} - success
    @throws {401} - if you are not logged in
    """

    logout_user()
    return res(True)
