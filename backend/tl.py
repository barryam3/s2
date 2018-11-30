from app import create_app, initialize_database
from app.realconfig import Config
app = create_app(Config)
initialize_database(app)
from app.extensions import db
from app.models.song import Song
import csv
with open('lyrics.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        lyr = row[2] if row[2] else ''
        song = Song.query.filter_by(id=int(row[1])).first()
        if song:
            song.lyrics = lyr
    db.session.commit()
