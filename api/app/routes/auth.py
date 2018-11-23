from flask import Blueprint, request
from flask_login import login_user, login_required, logout_user, UserMixin

from app.extensions import lm, mysql, bcrypt
from app.utils import res

class User(UserMixin):
    def __init__(self, id, athena, current, pitch, password):
        self.id = id
        self.username = athena
        self.current = current
        self.pitch = pitch
        self.password = password

    @classmethod
    def from_dict(cls, d):
        return cls(d['id'], d['athena'], d['current'], d['pitch'], d['password'])

    def to_dict(self):
        return {
            "id": self.id,
            "athena": self.username,
            "current": self.current,
            "pitch": self.pitch
        }

auth = Blueprint('auth', __name__)

@lm.user_loader
def load_user(id):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT id, athena, current, pitch, password FROM user WHERE id = %s", id)
    user = cursor.fetchone()
    return User.from_dict(user)

@auth.route('/login', methods=['POST'])
def login():
    """Start a session.
    
    @param {str} athena
    @param {str} password
    @return {bool} - success
    @throws {401} - if your athena & password are not correct
    """

    body = request.get_json()
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT id, athena, current, pitch, password FROM user WHERE athena = %s", body['athena'])
    user_data = cursor.fetchone()
    if user_data and bcrypt.check_password_hash(user_data['password'], body.get('password', '')):
        login_user(User.from_dict(user_data))
        return res(True)
    return res('Incorrect login.', 401)

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    """End your session.
    
    @return {bool} - success
    @throws {401} - if you are not logged in
    """

    logout_user()
    return res(True)
