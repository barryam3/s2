from flask import Blueprint, request
from flask_login import current_user

from app.extensions import mysql
from app.utils import res, login_required

songs = Blueprint('songs', __name__)

"""
@typedef {("Male" | "Female" | "Both" | "Either" | "None")} Solo
"""

"""
@typedef SongOverview
@prop {int} id
@prop {string} title
@prop {str} artist
@prop {bool} current
@prop {bool} arranged
@prop {Solo} solo
@prop {str} genre
@prop {str} last_edit
@prop {str} last_view
@prop {int} rating
@prop {str} suggestor
"""

@songs.route('/', methods=['GET'])
@login_required
def list_songs():
    """List all songs.

    @query {int} size - number of songs per "page"
    @query {int} page - "page" to get
    @query {str} title - get songs with a title matching this string
    @query {str} artist - get songs with an artist matching this string
    @query {bool} current - get only suggested/notsuggested songs
    @query {bool} arranged - get only arranged/notarranged songs
    @query {Solo} solo - get only songs with a certain solo type
    @query {("title" | "artist" | "suggestor")} sort -  sort by
    @query {bool} asc - sort ascending / descending
    @return {SongOverview[]}
    @throws {401} - if you are not logged in
    """

    start_page = request.args.get('page', 0)
    page_size = request.args.get('size', 10)
    start_row = int(start_page) * int(page_size)

    cols = [
      "song.id",
      "song.title",
      "song.artist",
      "song.current",
      "song.arranged",
      "song.genre",
      "song.solo",
      "song.last_edit",
      "song_user.last_view",
      "song_user.rating",
      "user.name AS suggestor"
    ]
    query = "SELECT " + ", ".join(cols) + " FROM song, song_user, user"
    
    query += " WHERE user.id = suggestor AND song.id = song_id AND user_id = %s"
    args = [current_user.id]

    if request.args.get('title'):
      query += " AND song.title LIKE %s"
      args.append('%' + request.args.get("title") + '%')

    if request.args.get("artist"):
      query += " AND song.artist LIKE %s"
      args.append('%' + request.args.get("artist") + '%')

    if request.args.get("current") != None:
      query += " AND song.current = %s"
      args.append(1 if request.args.get("current") else 0)

    if request.args.get("arranged") != None:
      query += " AND song.arranged = %s"
      args.append(1 if request.args.get("arranged") else 0)
  
    if request.args.get("solo") != None:
      query += " AND song.solo = %s"
      args.append(request.args.get("solo"))

    if request.args.get("sort") == "title":
      query += " ORDER BY song.title"
    elif request.args.get("sort") == "artist":
      query += " ORDER BY song.artist"
    elif request.args.get("sort") == "suggestor":
      query += " ORDER BY suggestor"
    else:
      query += " ORDER BY song.last_edit"
    query += " ASC" if request.args.get("asc") else " DESC"
    query += " LIMIT %s, %s"

    args.extend([start_row, page_size])

    cursor = mysql.get_db().cursor()
    cursor.execute(query, args)
    query_result = cursor.fetchall()
    return res(query_result)
