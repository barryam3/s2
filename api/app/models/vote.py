from app.database import db, CRUDMixin

class Vote(CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    song_id = db.Column(db.Integer, nullable=False)
    order = db.Column(db.Integer, nullable=False)
    def __init__(self, **kwargs):
        super(Vote, self).__init__(**kwargs)

    def __repr__(self):
        return '<Vote #%s: on %r by %r>' % (self.id, self.song_id, self.user_id)
