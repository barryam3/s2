from flask import Blueprint, request
from flask_login import current_user
from sqlalchemy.orm.exc import NoResultFound

from app.extensions import db
from app.utils import res, get_arg, login_required
from app.models.comment import Comment

comments = Blueprint('comments', __name__)

@comments.route('/<comment_id>', methods=['PATCH'])
@login_required
def edit_comment(comment_id):
    '''Edit comment.

    @param {str} text
    @return {bool} success
    '''

    try:
        comment_id = int(comment_id)
    except ValueError:
        return res('Comment not found.', 404)

    try:
        text = get_arg(request.get_json(), 'text', str)
    except TypeError:
        return res(status=400)

    if not text:
        return res('Comment cannot be empty.', 400)

    try:
        comment = Comment.query.filter_by(id=comment_id).one()
    except NoResultFound:
        return res('Comment not found.', 404)

    if comment.user_id != current_user.id:
        return res("You can't edit somebody else's comment", 403)
    
    comment.text = text
    db.session.commit()

    return res(True)


@comments.route('/<comment_id>', methods=['DELETE'])
@login_required
def delete_comment(comment_id):
    '''Delete comment.

    @return {bool} success
    '''

    try:
        comment_id = int(comment_id)
    except ValueError:
        return res('Comment not found.', 404)

    try:
        comment = Comment.query.filter_by(id=comment_id).one()
    except NoResultFound:
        return res('Comment not found.', 404)

    if comment.user_id != current_user.id:
        return res("You can't delete somebody else's comment", 403)
        
    db.session.delete(comment)
    db.session.commit()

    return res(True)
