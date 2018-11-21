from sqlalchemy import func

from app.database import db, CRUDMixin

class Song(CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    artist = db.Column(db.String(40), nullable=False)
    genre = db.Column(db.String(40), nullable=False)
    solo = db.Column(db.String(40), nullable=False)
    suggestor = db.Column(db.Integer, nullable=False)
    last_edit = db.Column(db.DateTime(), nullable=False, default=func.now(), onupdate=func.now())
    current = db.Column(db.Boolean(), nullable=False, default=True)
    arranged = db.Column(db.Boolean(), nullable=False, default=False)

    def __init__(self, **kwargs):
        super(Song, self).__init__(**kwargs)

    def __repr__(self):
        return '<Song #%s: %r by %r>' % (self.id, self.title, self.artist)
