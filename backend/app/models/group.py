from calendar import timegm

from app.extensions import db

# there is only one group
# if we were to ever share this app with others
# then we would connect this to the rest of the db
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sdeadline = db.Column(db.DateTime())
    vdeadline = db.Column(db.DateTime())

    def __init__(self, **kwargs):
        super(Group, self).__init__(**kwargs)

    def __repr__(self):
        return '<Group #%s>' % (self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'suggestDeadline': timegm(self.sdeadline.timetuple()) if self.sdeadline else None,
            'voteDeadline': timegm(self.vdeadline.timetuple()) if self.vdeadline else None
        }
