'''Route hanlders beginning with /songs.'''

from flask import Blueprint, request, g
from flask_login import current_user
from sqlalchemy.orm.exc import NoResultFound

from app.extensions import db
from app.utils import res, login_required
from app.models.song import Song


songs = Blueprint('songs', __name__)


@songs.route('', methods=['GET'])
@login_required
def list_songs():
    '''List all songs.
    
    @return {Song[]}
    @throws {401} - if you are not logged in
    '''

    return res([s.to_dict() for s in Song.query.all()])


@songs.route('', methods=['POST'])
@login_required
def add_song():
    '''Add a song.

    @param {str} title
    @param {str} artist
    @return {Song} - the new song
    @throws {401} - if you are not logged in
    '''

    req_body = request.get_json()
    title = req_body.get('title', '')
    artist = req_body.get('artist', '')

    if not title or not artist:
        return res('Song must have a title and artist.', 400)

    # create the new song
    song = Song(title=title, artist=artist)
    db.session.add(song)
    db.session.commit()

    return res(song.to_dict())


@songs.route('/<song_id>', methods=['DELETE'])
@login_required
def delete_song(song_id):
    '''Delete a song.

    @return {bool} - success
    @throws {401} - if you are not logged in
    @throws {404} - if the song is not found
    '''

    song_id = int(song_id)

    try:
        song = Song.query.filter_by(id=song_id).one()
    except NoResultFound:
        return res('Song not found.', 404)

    db.session.delete(song)
    db.session.commit()
    return res(True)
