'''Route hanlders beginning with /songs.'''

from flask import Blueprint, request, g
from flask_login import current_user
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime

from app.extensions import db
from app.utils import res, login_required, query_to_int, query_to_bool
from app.models.user import User
from app.models.song import Song
from app.models.setlist import Setlist
from app.models.suggestion import Suggestion
from app.models.rating import Rating


songs = Blueprint('songs', __name__)


@songs.route('/<song_id>', methods=['GET'])
@login_required
def get_song(song_id):
    '''Get a song's info.

    @return {Song} - success
    @throws {401} - if you are not logged in
    @throws {404} - if the song is not found
    '''

    song_id = query_to_int(song_id)
    setlist_id = query_to_int(request.args.get('setlist'))
    
    try:
        song = Song.query.filter_by(id=song_id).one()
    except NoResultFound:
        return res('Song not found.', 404)

    suggestion = Suggestion.query.filter_by(song_id=song_id, setlist_id=setlist_id).one_or_none()
    rating = None
    if suggestion:
        rating = Rating.query.filter_by(suggestion_id=suggestion.id, user_id=current_user.id).one_or_none()

    return res(song.to_dict(suggestion.to_dict(rating.value if rating else None) if suggestion else None)) # TODO: full info


@songs.route('', methods=['GET'])
@login_required
def list_songs():
    '''List all songs.
    
    @return {Song[]}
    @throws {401} - if you are not logged in
    '''

    setlist_id = query_to_int(request.args.get('setlist'))
    suggested = query_to_bool(request.args.get('suggested'))

    trio_query = setlist_id and suggested != False
    # with setlist context (Song + Suggestion + Rating query)
    if trio_query:
        suggestions = Suggestion.query.with_entities(Suggestion.id, Suggestion.user_id, Suggestion.song_id).filter_by(setlist_id=setlist_id).subquery()
        ratings = Rating.query.with_entities(Rating.value, Rating.suggestion_id).filter_by(user_id=current_user.id).subquery()
        suggestion_ratings=db.session.query(suggestions, User.username, ratings).join(User).outerjoin(ratings).subquery()
        query = db.session.query(Song, suggestion_ratings).join(suggestion_ratings, isouter=(suggested is None))

    # without setlist context (Song query)
    else:
        query = Song.query
        # not suggested
        if setlist_id:
            subquery = Suggestion.query.filter_by(setlist_id=setlist_id).with_entities(Suggestion.song_id)
            query = query.filter(~Song.id.in_(subquery))
        # suggested or not

    result = query.all()

    if trio_query:
        songs_array = [r[0].to_dict({
            'id': r[1],
            'suggestor': r[4],
            'myRating': r[5],
            'setlistID': setlist_id
        } if r[1] is not None else None) for r in result]
    else:
        songs_array = [s.to_dict() for s in result]
    return res(songs_array)


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

    suggestion = None
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

    return res(song.to_dict(suggestion.to_dict() if suggestion else None))


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


@songs.route('/<song_id>', methods=['PATCH'])
@login_required
def edit_song(song_id):
    '''Edit a song's basic info.

    @param {str} [title]
    @param {str} [artist]
    @param {str} [lyrics]
    @param {bool} [arranged]
    @return {bool} - success
    @throws {401} - if you are not logged in
    @throws {404} - if the song is not found
    '''
    song_id = int(song_id)
    req_body = request.get_json()
    title = req_body.get('title')
    artist = req_body.get('artist')
    lyrics = req_body.get('lyrics')
    arranged = req_body.get('arranged')

    try:
        song = Song.query.filter_by(id=song_id).one()
    except NoResultFound:
        return res('Song not found.', 404)

    if title:
        song.title = title
    if artist:
        song.artist = artist
    if lyrics is not None:
        song.lyrics = lyrics
    if arranged is not None:
        song.arranged = arranged

    db.session.commit()

    return res(song.to_dict())
