'''Route hanlders beginning with /songs.'''

from flask import Blueprint, request, g
from flask_login import current_user
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime

from app.extensions import db
from app.utils import res, login_required
from app.models.song import Song
from app.models.setlist import Setlist
from app.models.suggestion import Suggestion


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
    @param {int} autosuggest
    @return {Song} - the new song
    @throws {401} - autosuggest & the deadline has passed
    @throws {401} - if you are not logged in
    @throws {404} - autosuggest & the setlist does not exist

    '''

    req_body = request.get_json()
    title = req_body.get('title', '')
    artist = req_body.get('artist', '')
    autosuggest = req_body.get('autosuggest')

    if not title or not artist:
        return res('Song must have a title and artist.', 400)

    # create the new song
    song = Song(title=title, artist=artist)
    db.session.add(song)

    if autosuggest:
        try:
            setlist = Setlist.query.filter_by(id=autosuggest).one()
        except NoResultFound:
            return ('Setlist not found.', 404)
        if setlist.sdeadline < datetime.utcnow():
            return ('Nope! The deadline has passed.', 400)
        db.session.flush() # needed to get song id
        suggestion = Suggestion(setlist_id=setlist.id, song_id=song.id, user_id=current_user.id)
        db.session.add(suggestion)
    
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
