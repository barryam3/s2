'''Route hanlders beginning with /setlists.'''

from flask import Blueprint, request
from flask_login import current_user
from dateutil.parser import parse as parse_date
from datetime import datetime
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound

from app.extensions import db
from app.utils import res, login_required, admin_required
from app.models.setlist import Setlist
from app.models.song import Song
from app.models.suggestion import Suggestion


setlists = Blueprint('setlists', __name__)


@setlists.route('', methods=['POST'])
@admin_required
def add_setlist():
    '''Add a setlist.

    @param {str} title
    @param {str} suggestDeadline - ISO Date
    @param {str} voteDeadline - ISO Date
    @return {Setlist} - the new setlist
    @throws {401} - if you are not logged in
    @throws {403} - if you are not an admin
    '''

    req_body = request.get_json()
    title = req_body.get('title')
    if not title:
        return res('Setlist must have a title.', 400)

    try:
        sdeadline = parse_date(req_body.get('suggestDeadline'))
        vdeadline = parse_date(req_body.get('voteDeadline'))
    except (ValueError, AttributeError) as e:
        return res('Invalid deadline.', 400)

    setlist = Setlist(title=title, sdeadline=sdeadline, vdeadline=vdeadline)
    db.session.add(setlist)
    db.session.commit()

    return res(setlist.to_dict())


@setlists.route('', methods=['GET'])
@login_required
def get_setlists():
    '''Get setlists beginning with the most recent.

    For now, limit is fixed to one.
    @return {Setlist[]}
    @throws {401} - if you are not logged in
    '''

    setlist = Setlist.query.order_by(Setlist.id.desc()).first()
    setlists = []
    if setlist is not None:
        setlists.append(setlist.to_dict())
    return res(setlists)


@setlists.route('/<setlist_id>/suggestions', methods=['POST'])
@login_required
def suggest_song(setlist_id):
    '''Suggest a song for a setlist.

    @param {int} songID
    @return {Suggestion}
    @throws {400} - if the song is already suggested
    @throws {401} - if you are not logged in
    @throws {403} - if the suggestion deadline for the setlist has passed
    @throws {404} - if the setlist or song is not found
    '''

    setlist_id = int(setlist_id)

    req_body = request.get_json()
    song_id = req_body.get('songID', 0)

    try:
        deadline = Setlist.query.with_entities(Setlist.sdeadline).filter_by(id=setlist_id).one()[0]
    except NoResultFound:
        return res('Setlist not found.', 404)

    if deadline < datetime.utcnow():
        return res('Nope! The deadline has passed.', 403)

    try:
        Song.query.filter_by(id=song_id).one()
    except NoResultFound:
        return res('Song not found.', 404)
    
    if Suggestion.query.filter_by(setlist_id=setlist_id, song_id=song_id).first() is not None:
        return res('Song already suggested for this setlist.', 400)

    suggestion = Suggestion(setlist_id=setlist_id, song_id=song_id, user_id=current_user.id)
    db.session.add(suggestion)
    db.session.commit()

    return res(suggestion.to_dict())


@setlists.route('/<setlist_id>/suggestions', methods=['GET'])
@login_required
def list_suggestions(setlist_id):
    '''List the songs suggested for a setlist.

    @return {Suggestion[]}
    @throws {401} - if you are not logged in
    @throws {404} - if the setlist is not found
    '''

    setlist_id = int(setlist_id)

    try:
        deadline = Setlist.query.filter_by(id=setlist_id).one()
    except NoResultFound:
        return res('Setlist not found.', 404)

    suggestions = Suggestion.query.options(joinedload(Suggestion.song)).filter_by(setlist_id=setlist_id).all()
    return res([s.to_dict() for s in suggestions])
