from flask_login import UserMixin
from base64 import b64encode
from os import urandom

from app.database import db, CRUDMixin
from app.extensions import bcrypt


class User(CRUDMixin, UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False) # display name
    athena = db.Column(db.String(40), nullable=False, unique=True) # username
    password = db.Column(db.String(60), nullable=False) # hash
    current = db.Column(db.Boolean)
    explanation = db.Column(db.Text(), nullable=True)
    hash = db.Column(db.String(60), nullable=False) # unsure what used for
    salt = db.Column(db.String(60), nullable=False) # for pw security
    pitch = db.column(db.Boolean)

    def __init__(self, password, **kwargs):
        super(User, self).__init__(**kwargs)
        self.set_password(password)

    def __repr__(self):
        return '<User #%s:%r>' % (self.id, self.athena)

    def set_password(self, password):
        salt = b64encode(urandom(44)).decode('utf-8')
        pw_s = password + salt
        hash_pw_s = bcrypt.generate_password_hash(pw_s, 10).decode('utf-8')
        self.password = hash_pw_s
        self.salt = salt

    def check_password(self, password):
        pw_s = password + self.salt
        return bcrypt.check_password_hash(self.password, pw_s)

    def to_dict(self):
        return {
            "id": self.get_id(),
            "username": self.athena,
        }
