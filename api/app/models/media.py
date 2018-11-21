from app.database import db, CRUDMixin

class Media(CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, nullable=False)
    source = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(200))

    def __init__(self, **kwargs):
        super(Media, self).__init__(**kwargs)

    def __repr__(self):
        return '<Media #%s: on %r>' % (self.id, self.song_id)
