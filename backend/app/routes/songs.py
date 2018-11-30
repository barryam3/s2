'''Route hanlders beginning with /songs.'''

from flask import Blueprint, request
from flask_login import current_user
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime

from app.extensions import db
from app.utils import res, get_arg, login_required, active_required, query_to_bool
from app.models.user import User
from app.models.song import Song
from app.models.rating import Rating
from app.models.group import Group


songs = Blueprint('songs', __name__)


@songs.route('/<song_id>', methods=['GET'])
@login_required
def get_song(song_id):
    '''Get a song's info.

    @return {Song} - success
    @throws {401} - if you are not logged in
    @throws {404} - if the song is not found
    '''

    try:
        song_id = int(song_id)
        song = Song.query.filter_by(id=song_id).one()
    except (TypeError, NoResultFound) as e:
        return res('Song not found.', 404)

    rating = Rating.query.filter_by(song_id=song_id, user_id=current_user.id).first()

    return res(song.to_dict(rating.value if rating else None, True))


@songs.route('', methods=['GET'])
@login_required
def list_songs():
    '''List all songs.
    
    @query {0|1} suggested
    @return {Song[]} - in order of edits, most recent first
    @throws {401} - if you are not logged in
    '''

    try:
        suggested = query_to_bool(get_arg(request.args, 'suggested', str, None))
    except (TypeError, ValueError) as e:
        return res(status=400)

    my_ratings = db.session.query(Rating).with_entities(Rating.value, Rating.song_id).filter(Rating.user_id==current_user.id).subquery()
    query = db.session.query(Song, my_ratings).options(joinedload('user')).outerjoin(my_ratings)
    if suggested == True:
        query = query.filter(Song.user_id!=None)
    if suggested == False:
        query = query.filter(Song.user_id==None)
    query = query.order_by(Song.edited.desc())

    return res([s.to_dict(r) for s,r,u in query.all()])


@songs.route('', methods=['POST'])
@login_required
def add_song():
    '''Add a song.

    @param {str} title
    @param {str} artist
    @return {Song} - the new song
    @throws {401} - if you are not logged in
    @throws {403} - the deadline has passed
    '''

    req_body = request.get_json()
    try:
        title = get_arg(req_body, 'title', str)
        artist = get_arg(req_body, 'artist', str)
    except TypeError:
        return res(status=400)

    if not title or not artist:
        return res('Song must have a title and artist.', 400)

    group = Group.query.one()
    if group.sdeadline and (datetime.utcnow() > group.sdeadline):
        return ('Nope! The deadline has passed.', 403)

    song = Song(title=title, artist=artist, user_id=current_user.id)
    db.session.add(song)
    db.session.commit()

    return res(song.to_dict())


@songs.route('/<song_id>', methods=['PATCH'])
@login_required
def edit_song(song_id):
    '''Edit a song's basic info.

    @param {str} [title]
    @param {str} [artist]
    @param {str} [lyrics]
    @param {bool} [arranged]
    @param {bool} [suggested]
    @return {bool} - success
    @throws {401} - if you are not logged in
    @throws {403} - if you are trying to modify the suggestion of a song you did not suggest
    @throws {404} - if the song is not found
    '''

    try:
        song_id = int(song_id)
    except ValueError:
        return res('Song not found.', 404)
    
    req_body = request.get_json()
    try:
        title = get_arg(req_body, 'title', str, None)
        artist = get_arg(req_body, 'artist', str, None)
        lyrics = get_arg(req_body, 'lyrics', str, None)
        arranged = get_arg(req_body, 'arranged', bool, None)
        suggested = get_arg(req_body, 'suggested', bool, None)
    except TypeError:
        return res(status=400)

    try:
        song = Song.query.filter_by(id=song_id).one()
    except NoResultFound:
        return res('Song not found.', 404)

    if suggested is not None:
        if song.user_id and song.user_id != current_user.id:
            return res("You cannot unsuggest somebody else's song.", 403)
        group = Group.query.one()
        if group.sdeadline and (datetime.utcnow() > group.sdeadline):
            return ('Nope! The deadline has passed.', 403)

    if title:
        song.title = title
    if artist:
        song.artist = artist
    if lyrics is not None:
        song.lyrics = lyrics
    if arranged is not None:
        song.arranged = arranged
    if suggested == True:
        song.user_id = current_user.id
    if suggested == False:
        song.user_id = None
        for rating in Rating.query.filter_by(song_id=song.id).all():
            db.session.delete(rating)

    db.session.commit()

    return res(True)


@songs.route('/<song_id>', methods=['DELETE'])
@login_required
def delete_song(song_id):
    '''Delete a song.

    @return {bool} - success
    @throws {401} - if you are not logged in
    @throws {404} - if the song is not found
    '''

    try:
        song_id = int(song_id)
    except ValueError:
        return res('Song not found.', 404)

    try:
        song = Song.query.filter_by(id=song_id).one()
    except NoResultFound:
        return res('Song not found.', 404)

    db.session.delete(song)
    db.session.commit()
    return res(True)


@songs.route('/<song_id>/ratings/mine', methods=['PUT'])
@active_required
def rate_song(song_id):
    '''Rate a song.

    @param {int} rating - numerical rating
    @return {bool} - success
    @throws {400} - if rating is not in range [1,7]
    @throws {401} - if you are not logged in
    @throws {403} - if you are not an active member
    @throws {403} - if the deadline has passed
    @thorws {404} - if song is not found
    '''

    try:
        song_id = int(song_id)
    except ValueError:
        return res('Song not found.', 404)

    try:
        value = get_arg(request.get_json(), 'rating', int)
    except TypeError:
        return res(status=400)

    if not (1 <= value <= 7):
        return('Rating must be an integer in [1,7].', 400)

    group = Group.query.one()
    if group.vdeadline and (datetime.utcnow() > group.vdeadline):
        return ('Nope! The deadline has passed.', 403)

    try:
        song = Song.query.filter_by(id=song_id).one()
    except NoResultFound:
        return res('Song not found.', 404)

    try:
        rating = Rating.query.filter_by(user_id=current_user.id, song_id=song_id).one()
        rating.value = value
    except NoResultFound:
        rating = Rating(user_id=current_user.id, song_id=song_id, value=value)
        db.session.add(rating)

    db.session.commit()

    return res(True)
