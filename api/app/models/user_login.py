from sqlalchemy import func

from app.database import db, CRUDMixin

class UserLogin(CRUDMixin, db.Model):
    __tablename__ = 'user_login'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime(), nullable=False, default=func.now(), onupdate=func.now())
    token = db.Column(db.String(64), nullable=False)

    def __init__(self, **kwargs):
        super(UserLogin, self).__init__(**kwargs)

    def __repr__(self):
        return '<UserLogin #%s: by %r>' % (self.id, self.user_id)
