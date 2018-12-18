from calendar import timegm

from app.extensions import db

# there is only one group
# group is connected to user for convenience
# if we were to ever share this app with others
# then we would connect group to song as well
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sdeadline = db.Column(db.DateTime())
    rdeadline = db.Column(db.DateTime())

    users = db.relationship('User', cascade="all,delete", backref=db.backref('group', lazy=True))

    def __init__(self, **kwargs):
        super(Group, self).__init__(**kwargs)

    def __repr__(self):
        return '<Group #%s>' % (self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'suggestDeadline': timegm(self.sdeadline.timetuple()) if self.sdeadline else None,
            'rateDeadline': timegm(self.rdeadline.timetuple()) if self.rdeadline else None
        }
