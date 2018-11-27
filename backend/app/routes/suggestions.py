'''Suggestion route handlers'''

from flask import Blueprint, request
from flask_login import current_user
from sqlalchemy.orm.exc import NoResultFound

from app.extensions import db
from app.utils import res, login_required
from app.models.suggestion import Suggestion
from app.models.rating import Rating

suggestions = Blueprint('suggestions', __name__)

@suggestions.route('/<suggestion_id>/ratings/mine', methods=['PUT'])
@login_required
def rate_suggestion(suggestion_id):
    '''Rate a suggestion.

    @param {int} - numerical rating
    @return {Rating}
    @throws {400} - if rating is not in range [1,7]
    @thorws {404} - if suggestion is not found
    '''

    value = request.get_json()
    if not (isinstance(value, int) and (1 <= value <= 7)):
        return('Rating must be an integer in [1,7].', 400)

    try:
        suggestion = Suggestion.query.filter_by(id=suggestion_id).one()
    except NoResultFound:
        return res('Suggestion not found.', 404)

    try:
        rating = Rating.query.filter_by(user_id=current_user.id, suggestion_id=suggestion_id).one()
        rating.value = value
    except NoResultFound:
        rating = Rating(user_id=current_user.id, suggestion_id=suggestion_id, value=value)
        db.session.add(rating)

    db.session.commit()

    return res(suggestion.song.to_dict(suggestion.to_dict(rating.value)))
