from app.database import db, CRUDMixin

class Uploads(CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, nullable=False)
    source = db.Column(db.String(100), nullable=False)
    extension = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(140))

    def __init__(self, **kwargs):
        super(Uploads, self).__init__(**kwargs)

    def __repr__(self):
        return '<Upload #%s: on %r>' % (self.id, self.song_id)
