from app.extensions import db

class Link(db.Model):
    mysql_engine='InnoDB',

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)

    def __init__(self, **kwargs):
        super(Link, self).__init__(**kwargs)

    def __repr__(self):
        return '<Link #%s: for %r>' % (self.id, self.song)

    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'description': self.description
        }
