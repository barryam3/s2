import datetime
from calendar import timegm

def test_setlists(client):
    now = datetime.datetime.utcnow().replace(microsecond=0)
    one_month_from_now = (now + datetime.timedelta(365/12))
    now = timegm(now.timetuple())
    one_month_from_now = timegm(one_month_from_now.timetuple())
    setlist_1 = {
        'title': 'Fall 2001',
        'suggestDeadline': now,
        'voteDeadline': now
    }
    setlist_2 = {
        'title': 'Fall 2002',
        'suggestDeadline': one_month_from_now,
        'voteDeadline': one_month_from_now
    }
    song_1 = {
        'title': 'The Reason We Sing',
        'artist': 'Dick & Melodie Tunney'
    }
    song_2 = {
        'title': 'When the Mountains Fall',
        'artist': 'Mark Schultz'
    }
    song_3 = {
        'title': 'Never Change',
        'artist': 'AMP'
    }

    rv = client.post('/auth/login', json={
        'username': 'crossp',
        'password': 'xprod05'
    })
    assert rv.status_code == 200

    rv = client.post('/songs', json=song_1)
    assert rv.status_code == 200
    song_1 = rv.get_json()

    rv = client.post('/songs', json=song_2)
    assert rv.status_code == 200
    song_2 = rv.get_json()

    rv = client.post('/setlists', json=setlist_1)
    assert rv.status_code == 200
    setlist_1 = rv.get_json()

    rv = client.post('/setlists', json=setlist_2)
    assert rv.status_code == 200
    setlist_2 = rv.get_json()

    # Should be able to suggest a song.
    rv = client.post('/setlists/%d/suggestions' % setlist_2['id'], json={
        'songID': song_1['id']
    })
    assert rv.status_code == 200
    assert rv.get_json()['id'] == song_1['id']

    # Should not be able to suggest if deadline is passed.
    rv = client.post('/setlists/%d/suggestions' % setlist_1['id'], json={
        'songID': song_1['id'],
    })
    assert rv.status_code == 403

    # Should be able to suggest after deadline is moved later.
    rv = client.patch('/setlists/%d' % setlist_1['id'], json={
        'suggestDeadline': one_month_from_now
    })
    assert rv.status_code == 200

    rv = client.post('/setlists/%d/suggestions' % setlist_1['id'], json={
        'songID': song_1['id'],
    })
    assert rv.status_code == 200

    # Should not be able to suggest to a nonexistant setlist.
    rv = client.post('/setlists/0/suggestions', json={
        'songID': song_1['id'],
    })
    assert rv.status_code == 404

    # Should not be able to suggest the same song twice for a setlist.
    rv = client.post('/setlists/%d/suggestions' % setlist_2['id'], json={
        'songID': song_1['id']
    })
    assert rv.status_code == 400

    # Should not be able to suggest a nonexistant song.
    rv = client.post('/setlists/%d/suggestions' % setlist_2['id'], json={
        'songID': 0
    })
    assert rv.status_code == 404

    # Should autosuggest an added song if possible
    rv = client.post('/songs', json={
        'title': song_3['title'],
        'artist': song_3['artist'],
        'autosuggest': setlist_2['id']
    })
    assert rv.status_code == 200

    # Should not be able to suggest a song when not logged in.
    rv = client.post('/auth/logout')
    assert rv.status_code == 200

    rv = client.post('/setlists/%d/suggestions' % setlist_2['id'], json={
        'songID': song_2['id']
    })
    assert rv.status_code == 401
