from datetime import datetime
from sqlalchemy import func

from app.extensions import db

class View(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(), nullable=False, default=func.now(), onupdate=func.now())

    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    __table_args__ = (db.UniqueConstraint('song_id', 'user_id', name='_view'),)

    def __init__(self, **kwargs):
        super(View, self).__init__(**kwargs)

    def __repr__(self):
        return '<View #%s: on %r by %r>' % (self.id, self.song, self.user)

    def touch(self):
      self.timestamp = datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': timegm(self.timestamp.timetuple()),
            'song': self.song.to_dict(),
            'user': self.user.to_dict()
        }
