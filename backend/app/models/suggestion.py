from app.extensions import db

class Suggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chosen = db.Column(db.Boolean(), nullable=False, default=False)

    setlist_id = db.Column(db.Integer, db.ForeignKey('setlist.id'), nullable=False)
    setlist = db.relationship('Setlist', backref=db.backref('suggestions', lazy=True))

    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    song = db.relationship('Song', backref=db.backref('suggestions', lazy=True))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('suggestions', lazy=True))

    __table_args__ = (db.UniqueConstraint('setlist_id', 'song_id', name='_suggestion'),)

    def __init__(self, **kwargs):
        super(Suggestion, self).__init__(**kwargs)

    def __repr__(self):
        return '<Suggestion: of %r for %r>' % (self.song, self.setlist)

    def to_dict(self):
        return {
            "id": self.id,
            "suggestor": self.user.username,
            "setlist": self.setlist.title,
            "song": self.song.to_dict()
        }
