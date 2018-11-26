from datetime import datetime
from calendar import timegm

def test_songquery(client):
    deadline = timegm(datetime.utcnow().timetuple()) + 10000
    rv = client.post('/auth/login', json={
        'username': 'crossp',
        'password': 'xprod05'
    })
    assert rv.status_code == 200

    rv = client.post('/setlists', json={
        'title': 'Fall 2001',
        'suggestDeadline': deadline,
        'voteDeadline': deadline
    })
    assert rv.status_code == 200
    setlist_1 = rv.get_json()

    rv = client.post('/setlists', json={
        'title': 'Fall 2002',
        'suggestDeadline': deadline,
        'voteDeadline': deadline
    })
    assert rv.status_code == 200
    setlist_2 = rv.get_json()

    rv = client.post('/songs', json={
        'title': 'The Reason We Sing',
        'artist': 'Dick & Melodie Tunney',
    })
    assert rv.status_code == 200
    song_1 = rv.get_json()

    rv = client.post('/songs', json={
        'title': 'When the Mountains Fall',
        'artist': 'Mark Schultz',
    })
    assert rv.status_code == 200
    song_2 = rv.get_json()

    rv = client.post('/setlists/%s/suggestions' % setlist_1['id'], json={
        'songID': song_1['id']
    })
    assert rv.status_code == 200
    suggestion_1 = rv.get_json()

    rv = client.post('/setlists/%s/suggestions' % setlist_2['id'], json={
        'songID': song_2['id']
    })
    assert rv.status_code == 200
    suggestion_2 = rv.get_json()

    rv = client.put('/suggestions/%s/ratings/mine' % suggestion_1['id'], json=5)
    assert rv.status_code == 200
    suggestion_1 = rv.get_json()

    # should get all songs with no suggestion context
    rv = client.get('/songs')
    assert rv.status_code == 200
    assert rv.get_json() == [song_1, song_2]

    # should get all songs with suggestion context if available
    rv = client.get('/songs?setlist=%s' % setlist_1['id'])
    assert rv.status_code == 200
    assert rv.get_json() == [suggestion_1, song_2]

    # should get only suggested songs with suggestion context
    rv = client.get('/songs?setlist=%s&suggested=1' % setlist_2['id'])
    assert rv.status_code == 200
    assert rv.get_json() == [suggestion_2]

    # should get only non-suggested songs without suggestion context
    rv = client.get('/songs?setlist=%s&suggested=0' % setlist_2['id'])
    assert rv.status_code == 200
    assert rv.get_json() == [song_1]

    rv = client.post('/auth/logout')
    assert rv.status_code == 200

