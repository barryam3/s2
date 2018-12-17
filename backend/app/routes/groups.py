'''Route hanlders beginning with /groups.'''

from flask import Blueprint, request
from datetime import datetime
from sqlalchemy import func

from app.extensions import db
from app.utils import res, get_arg, admin_required
from app.models.group import Group
from app.models.song import Song
from app.models.rating import Rating


groups = Blueprint('groups', __name__)


# there is only one group
@groups.route('/1/deadlines', methods=['PUT'])
@admin_required
def update_deadlines():
    '''Update the deadline(s).

    @param {int} suggestDeadline - unix seconds
    @param {int} voteDeadline - unix seconds
    @return {bool} success
    @throws {401} - if you are not logged in
    @throws {403} - if you are not an admin
    '''

    req_body = request.get_json()
    try:
        sdeadline = get_arg(req_body, 'suggestDeadline', int, None)
        vdeadline = get_arg(req_body, 'voteDeadline', int, None)
    except TypeError:
        return res(status=400)

    group = Group.query.one()
    if sdeadline is not None:
        group.sdeadline = datetime.utcfromtimestamp(sdeadline)
    if vdeadline is not None:
        group.vdeadline = datetime.utcfromtimestamp(vdeadline)
    db.session.commit()

    return res(True)


@groups.route('/1', methods=['GET'])
@admin_required
def get_group():
    '''Get the group info.

    @return {Group} success
    @throws {401} - if you are not logged in
    @throws {403} - if you are not an admin
    '''

    return res(Group.query.one().to_dict())


@groups.route('/1/suggestions', methods=['DELETE'])
@admin_required
def delete_suggestions():
    '''Unsuggest all songs.

    @return {bool} success
    @throws {401} - if you are not logged in
    @throws {403} - if you are not an admin
    '''

    for song in Song.query.all():
        song.user_id = None
    for rating in Rating.query.all():
        db.session.delete(rating)
    db.session.commit()

    return res(True)

@groups.route('/1/ratings', methods=['GET'])
@admin_required
def get_average_ratings():
    '''Get average ratings for all songs.

    @return {[title, artist, avgRating][]} success
    @throws {401} - if you are not logged in
    @throws {403} - if you are not an admin
    '''

    group = Group.query.one()
    if group.vdeadline and (datetime.utcnow() <= group.vdeadline):
        return ('Nope! The deadline has not passed.', 403)

    avgRating = func.avg(Rating.value).label('avgRating')
    query = db.session.query(Song.title, Song.artist, avgRating)
    query = query.outerjoin(Rating)
    query = query.filter(Song.user_id!=None)
    query = query.group_by(Song.id)
    query = query.order_by(avgRating.desc())

    return res([[t, a, float(r) if r else None] for t, a, r in query.all()])
