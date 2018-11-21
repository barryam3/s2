from flask import Blueprint
from flask_login import current_user, login_required

from app.extensions import mysql
from app.utils import res

users = Blueprint('users', __name__)

@users.route('/', methods=['GET'])
def list_users():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT id, athena, current, pitch FROM user")
    query_result = cursor.fetchall()
    return res(query_result)

@users.route('/me', methods=['GET'])
@login_required
def get_active_user():
    return res(current_user.to_dict())

