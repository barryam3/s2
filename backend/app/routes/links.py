from flask import Blueprint, request
from sqlalchemy.orm.exc import NoResultFound

from app.extensions import db
from app.utils import res, get_arg, login_required
from app.models.link import Link

links = Blueprint('links', __name__)


@links.route('/<link_id>', methods=['DELETE'])
@login_required
def delete_link(link_id):
    '''Delete link.

    @return {bool} success
    '''

    try:
        link_id = int(link_id)
    except ValueError:
        return res('Link not found.', 404)

    try:
        link = Link.query.filter_by(id=link_id).one()
    except NoResultFound:
        return res('Link not found.', 404)
    
    db.session.delete(link)
    db.session.commit()

    return res(True)
