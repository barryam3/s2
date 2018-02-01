from datetime import datetime

from app.database import db, CRUDMixin

class Song(CRUDMixin, db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    artist = db.Column(db.String(40), nullable=False)
    genre = db.Column(db.String(40), nullable=False)
    solo = db.Column(db.String(40), nullable=False)
    suggestor = db.Column(db.Integer, nullable=False)
    last_edit = db.Column(db.DateTime, nullable=False, \
        default=datetime.utcnow, onupdate=datetime.utcnow)
    current = db.Column(db.Integer, nullable=False, default=1)
    arranged = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, password, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return '<Song #%s: %r by %r>' % (self.id, self.title, self.artist)
