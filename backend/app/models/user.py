from flask_login import UserMixin
from base64 import b64encode
from os import urandom

from app.extensions import db, bcrypt

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(8), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    active = db.Column(db.Boolean(), nullable=False, default=True)
    admin = db.Column(db.Boolean(), nullable=False, default=False)
    
    group_id =  db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False, default=1)

    comments = db.relationship('Comment', cascade="all,delete", backref=db.backref('user', lazy=True))
    songs = db.relationship('Song', backref=db.backref('user', lazy=True))
    ratings = db.relationship('Rating', cascade="all,delete", backref=db.backref('user', lazy=True))
    views = db.relationship('View', cascade="all,delete", backref=db.backref('user', lazy=True))

    def __init__(self, username, password, **kwargs):
        super(User, self).__init__(**kwargs)
        self.username = username
        self.set_password(password)

    def __repr__(self):
        return '<User #%s: %r>' % (self.id, self.username)

    # bcyrpt stores the salt in the password
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)
        db.session.commit()

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self, with_group=False, with_engagement=False):
        user =  {
            'id': self.id,
            'username': self.username,
            'active': self.active,
            'admin': self.admin
        }
        if with_group:
            user['group'] = self.group.to_dict()
        if with_engagement:
            user['numSuggestions'] = len(self.songs)
            rated_suggested_songs = [r for r in self.ratings if r.song.user_id != None]
            user['numRatings'] = len(rated_suggested_songs)
        return user
