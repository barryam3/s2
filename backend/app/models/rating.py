from app.extensions import db

class Rating(db.Model):
    mysql_engine='InnoDB',

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)

    suggestion_id = db.Column(db.Integer, db.ForeignKey('suggestion.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    __table_args__ = (db.UniqueConstraint('suggestion_id', 'user_id', name='_rating'),)

    def __init__(self, **kwargs):
        super(Rating, self).__init__(**kwargs)

    def __repr__(self):
        return '<Rating #%s: on %r by %r>' % (self.id, self.suggestion, self.user)

    def to_dict(self):
        return {
            'value': self.value,
            'suggestion': self.suggestion.to_dict(),
            'user': self.user.to_dict()
        }
