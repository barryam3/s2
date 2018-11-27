from app.extensions import db

class Suggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chosen = db.Column(db.Boolean(), nullable=False, default=False)

    setlist_id = db.Column(db.Integer, db.ForeignKey('setlist.id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    ratings = db.relationship('Rating', cascade="all,delete", backref=db.backref('suggestion', lazy=True))

    __table_args__ = (db.UniqueConstraint('setlist_id', 'song_id', name='_suggestion'),)

    def __init__(self, **kwargs):
        super(Suggestion, self).__init__(**kwargs)

    def __repr__(self):
        return '<Suggestion: of %r for %r>' % (self.song, self.setlist)

    def to_dict(self, rating_num=None):
        return {
            'id': self.id,
            'suggestor': self.user.username,
            'setlistID': self.setlist.id,
            'myRating': rating_num
        }
