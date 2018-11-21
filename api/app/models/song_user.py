from sqlalchemy import func

from app.database import db, CRUDMixin

class SongUser(CRUDMixin, db.Model):
    __tablename__ = 'song_user'
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    last_view = db.Column(db.DateTime(), nullable=False, default=0, onupdate=func.now())
    rating = db.Column(Integer)

    def __init__(self, **kwargs):
        super(SongUser, self).__init__(**kwargs)

    def __repr__(self):
        return '<SongUser #%s: on %r by %r>' % (self.id, self.song_id, self.user_id)
