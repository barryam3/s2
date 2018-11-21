from flask_login import UserMixin
from base64 import b64encode
from os import urandom

from app.database import db, CRUDMixin
from app.extensions import bcrypt


class User(CRUDMixin, UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False) # display name
    athena = db.Column(db.String(40), nullable=False, unique=True) # username
    password = db.Column(db.String(60), nullable=False) # hashed with a salt
    current = db.Column(db.Boolean(), nullable=False, default=True)
    explanation = db.Column(db.Text(), nullable=True)
    hash = db.Column(db.String(60), nullable=False) # unsure what used for
    pitch = db.Column(db.Boolean(), nullable=False, default=False)

    def __init__(self, password, **kwargs):
        super(User, self).__init__(**kwargs)
        self.set_password(password)

    def __repr__(self):
        return '<User #%s:%r>' % (self.id, self.athena)

    # bcyrpt stores the salt in the password
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "id": self.get_id(),
            "username": self.athena,
        }
