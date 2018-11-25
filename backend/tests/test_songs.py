def test_songs(client):
    # Should not be able to create a song if not signed in.
    song = {
        'title': 'The Reason We Sing',
        'artist': 'Dick & Melodie Tunney'
    }

    rv = client.post('/songs', json=song)
    assert rv.status_code == 401

    rv = client.post('/auth/login', json={
        'username': 'crossp',
        'password': 'xprod05'
    })
    assert rv.status_code == 200

    rv = client.post('/songs', json=song)
    assert rv.status_code == 200
    json = rv.get_json()
    assert json['id'] == 1
    assert json['title'] == song['title']
    assert json['artist'] == song['artist']
    song = json

    rv = client.get('/songs')
    assert rv.status_code == 200
    json = rv.get_json()
    assert len(json) == 1
    assert json[0] == song

    rv = client.delete('/songs/%d' % (song['id']))
    assert rv.status_code == 200

    rv = client.get('/songs')
    assert rv.status_code == 200
    assert rv.get_json() == []

    client.post('/auth/logout')
    assert rv.status_code == 200
