import datetime
from calendar import timegm

def test_ratings(client):
    now = datetime.datetime.utcnow().replace(microsecond=0)
    one_month_from_now = (now + datetime.timedelta(365/12))
    now = timegm(now.timetuple())
    one_month_from_now = timegm(one_month_from_now.timetuple())
    setlist = {
        'title': 'Fall 20XX',
        'suggestDeadline': one_month_from_now,
        'voteDeadline': one_month_from_now
    }
    song = {
        'title': 'The Reason We Sing',
        'artist': 'Dick & Melodie Tunney'
    }

    rv = client.post('/auth/login', json={
        'username': 'crossp',
        'password': 'xprod05'
    })
    assert rv.status_code == 200

    rv = client.post('/setlists', json=setlist)
    assert rv.status_code == 200
    setlist = rv.get_json()

    rv = client.post('/songs', json=song)
    assert rv.status_code == 200
    song = rv.get_json()

    rv = client.post('/setlists/%d/suggestions' % setlist['id'], json={
        'songID': song['id']
    })
    assert rv.status_code == 200
    suggestion = rv.get_json()

    # Should be able to rate a song.
    rv = client.put('/suggestions/%d/ratings/mine' % suggestion['id'], json=3)
    assert rv.status_code == 200
    assert rv.get_json()['suggestion']['myRating'] == 3

    # Should be able to re-rate a song.
    rv = client.put('/suggestions/%d/ratings/mine' % suggestion['id'], json=4)
    assert rv.status_code == 200
    assert rv.get_json()['suggestion']['myRating'] == 4

    # Should not be able rate a nonexistent suggestion.
    rv = client.put('/suggestions/0/ratings/mine', json=1)
    assert rv.status_code == 404

    # Should not be able to rate a song when not logged in.
    rv = client.post('/auth/logout')
    assert rv.status_code == 200

    rv = client.put('/suggestions/%d/ratings/mine' % suggestion['id'], json=5)
    assert rv.status_code == 401
