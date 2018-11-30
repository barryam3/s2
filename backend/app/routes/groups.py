'''Route hanlders beginning with /groups.'''

from flask import Blueprint, request
from datetime import datetime

from app.extensions import db
from app.utils import res, get_arg, admin_required
from app.models.group import Group
from app.models.song import Song


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
    db.session.commit()

    return res(True)
