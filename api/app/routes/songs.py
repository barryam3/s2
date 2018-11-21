from flask import Blueprint, request
from flask_login import login_required

from app.extensions import mysql
from app.utils import res

songs = Blueprint('songs', __name__)

@songs.route('/', methods=['GET'])
@login_required
def list_songs():
    start_page = request.args.get('page', 0)
    page_size = request.args.get('size', 10)
    start_row = int(start_page) * int(page_size)
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM song LIMIT %s, %s", (start_row, page_size))
    query_result = cursor.fetchall()
    return res(query_result)
