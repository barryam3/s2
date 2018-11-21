from flask import Blueprint, request
from flask_login import login_user, login_required, logout_user, UserMixin

from app.extensions import lm, mysql, bcrypt
from app.utils import res

from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, current, pitch):
        self.id = id
        self.username = username
        self.current = current
        self.pitch = pitch

    @classmethod
    def from_dict(cls, d):
        return cls(d['id'], d['athena'], d['current'], d['pitch'])

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "current": self.current,
            "pitch": self.pitch
        }

auth = Blueprint('auth', __name__)

@lm.user_loader
def load_user(id):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT id, athena, current, pitch FROM user WHERE id = %s", id)
    user = cursor.fetchone()
    return User.from_dict(user)

@auth.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT id, athena, current, pitch, password FROM user WHERE athena = %s", body['username'])
    user_data = cursor.fetchone()
    if bcrypt.check_password_hash(user_data['password'], body['password']):
        login_user(User.from_dict(user_data))
        return res(True)
    return res('Incorrect login.', 403)

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return res(True)
