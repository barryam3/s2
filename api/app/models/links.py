from app.database import db, CRUDMixin

class Links(CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(140), nullable=False)
    description = db.Column(db.String(140))

    def __init__(self, **kwargs):
        super(Links, self).__init__(**kwargs)

    def __repr__(self):
        return '<Link #%s: on %r>' % (self.id, self.song_id)
