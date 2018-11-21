from app.database import db, CRUDMixin

class Lyrics(CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, nullable=False)
    lyrics = db.Column(db.String())

    def __init__(self, **kwargs):
        super(Lyrics, self).__init__(**kwargs)

    def __repr__(self):
        return '<Lyrics #%s: on %r>' % (self.id, self.song_id)
