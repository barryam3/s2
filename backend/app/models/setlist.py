from app.extensions import db

class Setlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text(), nullable=False)
    sdeadline = db.Column(db.DateTime(), nullable=False)
    vdeadline = db.Column(db.DateTime(), nullable=False)

    def __init__(self, **kwargs):
        super(Setlist, self).__init__(**kwargs)

    def __repr__(self):
        return '<Setlist #%s: %r>' % (self.id, self.title)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'suggestDeadline': self.sdeadline.isoformat(),
            'voteDeadline': self.vdeadline.isoformat()
        }
