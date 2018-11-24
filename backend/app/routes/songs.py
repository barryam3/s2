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

    start_page = int(request.args.get('page', 0))
    page_size = int(request.args.get('size', 10))
    start_row = start_page * page_size

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
        args.append(1 if int(request.args.get("current", 0)) else 0)

    if request.args.get("arranged") != None:
        query += " AND song.arranged = %s"
        args.append(1 if int(request.args.get("arranged", 0)) else 0)
  
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
    query += " ASC" if int(request.args.get("asc", 0)) else " DESC"
    query += " LIMIT %s, %s"

    args.extend([start_row, page_size])

    cursor = mysql.get_db().cursor()
    cursor.execute(query, args)
    query_result = cursor.fetchall()
    for song in query_result:
        song['current'] = bool(song['current'])
        song['arranged'] = bool(song['arranged'])
        song['updated'] = song['last_view'] < song['last_edit']
        del song['last_view']
        del song['last_edit']
    return res(query_result)

@songs.route('/', methods=['POST'])
@login_required
def add_song():
    """Add a song.
    
    @param {str} title
    @param {str} artist
    @param {Solo} solo
    @return {int} - id of the new song
    @throws {401} - if you are not logged in
    """

    req_body = request.get_json()
    title = req_body.get('title', '')
    artist = req_body.get('artist', '')
    solo = req_body.get('solo', '')

    if len(title) == 0 or len(artist) == 0:
        return send("Song must have a title and artist.", 400)

    if solo not in ["Male", "Female", "Both", "Either", "None"]:
        return send("Invalid solo type.", 400)

    # create the new song
    db = mysql.get_db()
    cursor = db.cursor()
    query = "INSERT INTO song (title, artist, solo, suggestor, genre) VALUES (%s, %s, %s, %s, '')"
    params = (title, artist, solo, current_user.id)
    cursor.execute(query, params)
    db.commit()

    # create data for the new song

    # TODO: make lyrics be column of song table
    new_song_id = cursor.lastrowid
    cursor.execute("INSERT INTO lyrics (song_id, lyrics) VALUES (%s, '')", new_song_id)

    # TODO: remove once s1 is fully replaced
    cursor.execute("SELECT id FROM user")
    user_ids = [u['id'] for u in cursor.fetchall()]
    query = "INSERT INTO song_user (song_id, user_id, rating) VALUES (%s, %s, 0)"
    params = [(new_song_id, user_id) for user_id in user_ids]
    cursor.executemany(query, params)

    db.commit()

    return res(new_song_id)

@songs.route('/<song_id>', methods=['DELETE'])
@login_required
def delete_song(song_id):
    """Delete a song.
    
    @return {bool} - success
    @throws {401} - if you are not logged in
    @throws {404} - if the song is not found
    """

    # delete the song
    db = mysql.get_db()
    cursor = db.cursor()
    # TODO: use foreign keys so we can use cascade
    cursor.execute("DELETE FROM song WHERE id = %s", song_id)
    found = cursor.rowcount > 0
    cursor.execute("DELETE FROM comment WHERE song_id = %s", song_id)
    cursor.execute("DELETE FROM links WHERE song_id = %s", song_id)
    cursor.execute("DELETE FROM lyrics WHERE song_id = %s", song_id)
    cursor.execute("DELETE FROM media WHERE song_id = %s", song_id)
    cursor.execute("DELETE FROM song_user WHERE song_id = %s", song_id)
    cursor.execute("DELETE FROM uploads WHERE song_id = %s", song_id)
    cursor.execute("DELETE FROM vote WHERE song_id = %s", song_id)
    cursor.execute("DELETE FROM youtube WHERE song_id = %s", song_id)
    db.commit()

    if not found:
        return res("Song not found.", 404)
    return res(True)
