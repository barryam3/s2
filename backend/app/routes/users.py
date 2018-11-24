from flask import Blueprint, request
from flask_login import current_user

from app.extensions import mysql, bcrypt
from app.utils import res, login_required, pitch_required

users = Blueprint('users', __name__)

"""
@typedef User
@prop {int} id
@prop {str} athena
@prop {bool} current
@prop {bool} pitch
"""

@users.route('/', methods=['GET'])
@pitch_required
def list_users():
    """Enumerate all users.
    
    @return {User[]} - all users' info
    @throws {401} - if you are not logged in
    @throws {403} - if you are not a pitch
    """

    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT id, athena, current, pitch FROM user")
    query_result = cursor.fetchall()
    return res(query_result)

@users.route('/me', methods=['GET'])
@login_required
def get_active_user():
    """Get your info.
    
    @return {User} - your info
    @throws {401} - if you are not logged in
    """

    return res(current_user.to_dict())

@users.route('/me/password', methods=['PUT'])
@login_required
def update_password():
    """Change your password.

    @param {str} oldPassword - your current password
    @param {str} newPassword - your new password
    
    @return {boolean} - success
    @return {400} - if the new password is not at least six characters long
    @return {401} - if your current password is not correct
    @throws {401} - if you are not logged in
    """

    req_body = request.get_json()
    old_pass = req_body.get('oldPassword', '')
    new_pass = req_body.get('newPassword', '')

    if not bcrypt.check_password_hash(current_user.password, old_pass):
        return res("Incorrect current password.", 401)

    if len(new_pass) < 6:
        return res("Password must be at least six characters.", 400)

    db = mysql.get_db()
    cursor = db.cursor()
    query = "UPDATE user SET password = %s WHERE id = %s"
    params = (bcrypt.generate_password_hash(new_pass), current_user.id)
    cursor.execute(query, params)
    db.commit()
    if cursor.rowcount != 1:
        return res("Something went wrong.", 500)        

    return res(True)

@users.route("/<id>/password", methods=["DELETE"])
@pitch_required
def reset_password(id):
    """Reset a user's password to "xprod05".
    
    @return {boolean} - success
    @throws {401} - if you are not logged in
    @throws {403} - if you are not a pitch
    """

    db = mysql.get_db()
    cursor = db.cursor()
    query = "UPDATE user SET password = %s WHERE id = %s"
    params = (bcrypt.generate_password_hash("xprod05"), id)
    cursor.execute(query, params)
    db.commit()
    if cursor.rowcount == 0:
        return res("User not found.", 404)
    return res(True)

@users.route("/", methods=["POST"])
@pitch_required
def add_user():
    """Add a user.
    
    @param {str} athena - the member's kerberos
    @return {int} - id of the new user
    @throws {400} if athena is not a valid kerberos
    @throws {401} - if you are not logged in
    @throws {403} - if you are not a pitch
    """

    req_body = request.get_json()
    athena = req_body.get('athena')
    if not (isinstance(athena, str) and (3 <= len(athena) <= 8) and athena.isalnum()):
        return res("You must supply a valid kerberos.", 400)

    # create the new user
    db = mysql.get_db()
    cursor = db.cursor()
    query = "INSERT INTO user (athena, name, password) VALUES (%s, %s, %s)"
    params = (athena, athena, bcrypt.generate_password_hash("xprod05"))
    cursor.execute(query, params)
    db.commit()

    # create data for the new user
    new_user_id = cursor.lastrowid
    query = "INSERT INTO vote (user_id, song_id, order) VALUES (%s, 0, %s)"
    params = [(new_user_id, i) for i in range(1,11)]
    cursor.executemany(query, params)

    # TODO: remove once s1 is fully replaced
    cursor.execute("SELECT id FROM song WHERE current = 1")
    song_ids = [d['id'] for d in cursor.fetchall()]
    query = "INSERT INTO song_user (song_id, user_id, rating) VALUES (%s, %s, 0)"
    params = [(song_id, new_user_id) for song_id in song_ids]
    cursor.executemany(query, params)

    db.commit()

    return res(new_user_id)

