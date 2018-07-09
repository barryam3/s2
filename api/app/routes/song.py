from flask import Blueprint, current_app, request, abort
from flask_login import login_required

from app.models.song import Song
from app.utils import send_success_response, send_error_response

song = Blueprint('song', __name__)

@song.route('/', methods=['GET'])
@login_required
def get_songs():
    songs = [s.to_dict() for s in Song.query.filter(**request.args).all()]
    return send_success_response(songs)
