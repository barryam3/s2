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

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'active': self.active,
            'admin': self.admin
        }
