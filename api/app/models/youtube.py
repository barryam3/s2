from app.database import db, CRUDMixin

class Youtube(CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, nullable=False)
    source = db.Column(db.String(20), nullable=False)

    def __init__(self, **kwargs):
        super(Youtube, self).__init__(**kwargs)

    def __repr__(self):
        return '<Youtube #%s: on %r>' % (self.id, self.song_id)
