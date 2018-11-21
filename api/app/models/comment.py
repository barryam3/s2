from sqlalchemy import func

from app.database import db, CRUDMixin

class Comment(CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime(), nullable=False, default=func.now(), onupdate=func.now())

    def __init__(self, **kwargs):
        super(Comment, self).__init__(**kwargs)

    def __repr__(self):
        return '<Comment #%s: on %r by %r>' % (self.id, self.song_id, self.user_id)
