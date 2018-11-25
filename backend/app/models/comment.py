from sqlalchemy import func

from app.extensions import db

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text(), nullable=False)
    timestamp = db.Column(db.DateTime(), nullable=False, default=func.now())

    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    song = db.relationship('Song', backref=db.backref('comments', lazy=True))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('comments', lazy=True))

    def __init__(self, **kwargs):
        super(Comment, self).__init__(**kwargs)

    def __repr__(self):
        return '<Comment #%s: on %r by %r>' % (self.id, self.song, self.user)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'timestamp': self.timestamp.isoformat(),
            'author': self.user.username
        }
