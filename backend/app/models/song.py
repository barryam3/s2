from sqlalchemy import func

from app.extensions import db

lyr = '''
I used to rule the world
Seas would rise when I gave the word
Now in the morning, I sleep alone
Sweep the streets I used to own

I used to roll the dice
Feel the fear in my enemy's eyes
Listen as the crowd would sing
Now the old king is dead! Long live the king!
One minute I held the key
Next the walls were closed on me
And I discovered that my castles stand
Upon pillars of salt and pillars of sand

I hear Jerusalem bells are ringing
Roman Cavalry choirs are singing
Be my mirror, my sword and shield
My missionaries in a foreign field
For some reason I can't explain
Once you go there was never, never a honest word
And that was when I ruled the world

It was a wicked and wild wind
Blew down the doors to let me in
Shattered windows and the sound of drums
People couldn't believe what I'd become
Revolutionaries wait
For my head on a silver plate
Just a puppet on a lonely string
Oh, who would ever want to be king?

I hear Jerusalem bells are ringing
Roman Calvary choirs are singing
Be my mirror, my sword and shield
My missionaries in a foreign field
For some reason I can't explain
I know Saint Peter won't call my name
Never an honest word
But that was when I ruled the world

Oh, oh, oh, oh, oh

I hear Jerusalem bells are ringing
Roman Calvary choirs are singing
Be my mirror, my sword and shield
My missionaries in a foreign field
For some reason I can't explain
I know Saint Peter won't call my name
Never an honest word
But that was when I ruled the world
'''

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    lyrics = db.Column(db.Text(), nullable=False, default='')
    arranged = db.Column(db.Boolean(), nullable=False, default=False)
    edited = db.Column(db.DateTime(), nullable=False, default=func.now(), onupdate=func.now())

    comments = db.relationship('Comment', cascade="all,delete", backref=db.backref('song', lazy=True))
    suggestions = db.relationship('Suggestion', cascade="all,delete", backref=db.backref('song', lazy=True))
    links = db.relationship('Link', cascade="all,delete", backref=db.backref('song', lazy=True))

    def __init__(self, **kwargs):
        super(Song, self).__init__(**kwargs)

    def __repr__(self):
        return '<Song #%s: %r by %r>' % (self.id, self.title, self.artist)

    def to_dict(self, suggestion_dict=None):
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "lyrics": self.lyrics,
            "arranged": self.arranged,
            "edited": self.edited,
            "suggestion": suggestion_dict
        }
