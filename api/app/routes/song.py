from flask import Blueprint, current_app, request, abort
from flask_login import login_required, current_user

from app.models.song import Song
from app.utils import send_success_response, send_error_response

song = Blueprint('song', __name__)

@song.route('/', methods=['GET'])
@login_required
def get_songs():
    query_results = Song.query.filter_by(**request.args.to_dict()).all()
    songs = [s.to_dict() for s in query_results]
    return send_success_response(songs)

@song.route('/', methods=['POST'])
@login_required
def create_song():
    data = request.get_json()
    song = Song.create(
      title=data['title'],
      artist=data['artist'],
      genre='N/A',
      solo='Any',
      suggestor=current_user.id
    )
    return send_success_response(song.to_dict())
