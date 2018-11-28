'''Route hanlders beginning with /groups.'''

from flask import Blueprint, request
from datetime import datetime

from app.extensions import db
from app.utils import res, admin_required
from app.models.group import Group
from app.models.song import Song


groups = Blueprint('groups', __name__)


# there is only one group
@groups.route('/1/deadlines', methods=['PATCH'])
@admin_required
def update_deadlines(group_id):
    '''Update the deadline(s).

    @param {int} suggestDeadline - unix seconds
    @param {int} voteDeadline - unix seconds
    @return {bool} success
    @throws {401} - if you are not logged in
    @throws {403} - if you are not an admin
    '''

    req_body = request.get_json()
    sdeadline = req_body.get('suggestDeadline')
    vdeadline = req_body.get('voteDeadline')
    group = Group.query.one()

    if sdeadline is not None:
        try:
            setlist.sdeadline = datetime.utcfromtimestamp(int(sdeadline))
        except (ValueError, TypeError) as e:
            return res('Invalid deadline.', 400)

    if vdeadline is not None:
        try:
            setlist.vdeadline = datetime.utcfromtimestamp(int(vdeadline))
        except (ValueError, AttributeError) as e:
            return res('Invalid deadline.', 400)

    db.session.commit()

    return res(True)


@groups.route('/1/suggestions', methods=['DELETE'])
@admin_required
def delete_suggestions(group_id):
    '''Reset the site.

    @return {bool} success
    @throws {401} - if you are not logged in
    @throws {403} - if you are not an admin
    '''

    for song in Song.query.all():
        song.user_id = None
    db.session.commit()

    return res(True)
