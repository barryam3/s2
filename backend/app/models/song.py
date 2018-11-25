from sqlalchemy import func

from app.extensions import db

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    lyrics = db.Column(db.Text(), nullable=False, default='')
    arranged = db.Column(db.Boolean(), nullable=False, default=False)
    edited = db.Column(db.DateTime(), nullable=False, default=func.now(), onupdate=func.now())

    def __init__(self, **kwargs):
        super(Song, self).__init__(**kwargs)

    def __repr__(self):
        return '<Song #%s: %r by %r>' % (self.id, self.title, self.artist)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "lyrics": self.lyrics,
            "arranged": self.arranged,
            "edited": self.edited
        }
