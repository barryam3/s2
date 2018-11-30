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
from app.models.comment import Comment
from app.models.link import Link
from app.models.view import View


songs = Blueprint('songs', __name__)


def update_view(song_id):
    try:
        view = View.query.filter_by(user_id=current_user.id, song_id=song_id).one()
        view.touch()
    except NoResultFound:
        view = View(user_id=current_user.id, song_id=song_id)
        db.session.add(view)
    return view


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

    view =update_view(song_id)

    db.session.commit()

    return res(song.to_dict(view.timestamp, rating.value if rating else None, True))


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
        title = get_arg(request.args, 'title', str, None)
        artist = get_arg(request.args, 'artist', str, None)
        arranged = query_to_bool(get_arg(request.args, 'arranged', str, None))
        suggestor = get_arg(request.args, 'suggestor', str, None)

    except (TypeError, ValueError) as e:
        return res(status=400)

    my_ratings = db.session.query(Rating).with_entities(Rating.value, Rating.song_id).filter(Rating.user_id==current_user.id).subquery()
    my_views = db.session.query(View).with_entities(View.timestamp, View.song_id).filter(View.user_id==current_user.id).subquery()
    query = db.session.query(Song, my_ratings, my_views).options(joinedload('user')).outerjoin(my_ratings).outerjoin(my_views)
    if suggested == True:
        query = query.filter(Song.user_id!=None)
    if suggested == False:
        query = query.filter(Song.user_id==None)
    if title is not None:
        query = query.filter(Song.title.like('%' + title + '%'))
    if artist is not None:
        query = query.filter(Song.artist.like('%' + artist + '%'))
    if arranged is not None:
        query = query.filter(Song.arranged==arranged)
    if suggestor is not None:
        try:
            suggestor = User.query.filter_by(username=suggestor).one()
            query = query.filter(Song.user_id==suggestor.id)
        except NoResultFound:
            return res('User not found.', 404)
    query = query.order_by(Song.edited.desc())
    
    songs = query.all()

    return res([s.to_dict(v,r) for s,r,u1,v,u2 in songs])


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

    song.touch()
    update_view(song_id)
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


@songs.route('/<song_id>/comments', methods=['POST'])
@login_required
def add_comment(song_id):
    '''Add a comment.

    @param {str} text
    @return {Comment}
    '''
    try:
        song_id = int(song_id)
    except ValueError:
        return res('Song not found.', 404)

    try:
        text = get_arg(request.get_json(), 'text', str)
    except TypeError:
        return res(status=400)

    try:
        song = Song.query.filter_by(id=song_id).one()
    except NoResultFound:
        return res('Song not found.', 404)

    comment = Comment(text=text, song_id=song.id, user_id=current_user.id)
    db.session.add(comment)
    song.touch()
    update_view(song_id)
    db.session.commit()

    return res(comment.to_dict())


@songs.route('/<song_id>/links', methods=['POST'])
@login_required
def add_link(song_id):
    '''Add link.

    @param {str} url
    @param {str} description
    @return {Link}
    '''

    try:
        song_id = int(song_id)
    except ValueError:
        return res('Song not found.', 404)

    req_body = request.get_json()
    try:
        url = get_arg(req_body, 'url', str)
        description = get_arg(req_body, 'description', str)
    except TypeError:
        return res(status=400)

    if not url or not description:
        return res('URL and description are required.', 400)

    try:
        song = Song.query.filter_by(id=song_id).one()
    except NoResultFound:
        return res('Song not found.', 404)
    
    link = Link(url=url, description=description, song_id=song.id)
    db.session.add(link)
    song.touch()
    update_view(song_id)
    db.session.commit()

    return res(link.to_dict())
