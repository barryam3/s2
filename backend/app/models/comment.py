from sqlalchemy import func
from calendar import timegm

from app.extensions import db

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text(), nullable=False)
    timestamp = db.Column(db.DateTime(), nullable=False, default=func.now())

    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, **kwargs):
        super(Comment, self).__init__(**kwargs)

    def __repr__(self):
        return '<Comment #%s: on %r by %r>' % (self.id, self.song, self.user)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'timestamp': timegm(self.timestamp.timetuple()),
            'author': self.user.username
        }
