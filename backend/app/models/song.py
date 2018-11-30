from sqlalchemy import func
from calendar import timegm
from datetime import datetime

from app.extensions import db

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    lyrics = db.Column(db.Text(), nullable=False, default='')
    arranged = db.Column(db.Boolean(), nullable=False, default=False)
    edited = db.Column(db.DateTime(), nullable=False, default=func.now(), onupdate=func.now())

    user_id =  db.Column(db.Integer, db.ForeignKey('user.id'))

    comments = db.relationship('Comment', cascade="all,delete", backref=db.backref('song', lazy=True))
    links = db.relationship('Link', cascade="all,delete", backref=db.backref('song', lazy=True))
    views = db.relationship('View', cascade="all,delete", backref=db.backref('song', lazy=True))

    def __init__(self, **kwargs):
        super(Song, self).__init__(**kwargs)

    def __repr__(self):
        return '<Song #%s: %r by %r>' % (self.id, self.title, self.artist)

    def touch(self):
      self.edited = datetime.utcnow()

    def to_dict(self, view_datetime=None, rating=None, full=False):
        song = {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "lyrics": self.lyrics,
            "arranged": self.arranged,
            "lastEdited": timegm(self.edited.timetuple()),
            "suggestor": self.user.username if self.user else None,
            "myRating": rating,
            "lastViewed": timegm(view_datetime.timetuple()) if view_datetime else 0
        }
        if full:
            song['comments'] = [c.to_dict() for c in self.comments]
            song['links'] = [l.to_dict() for l in self.links]
        return song
