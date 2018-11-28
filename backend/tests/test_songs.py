import time

user_1 = {
    'username': 'crossp',
    'password': 'xprod05'
}
user_2 = {
    'username': 'barryam3',
    'password': 'xprod05'
}

song_1 = {
    'title': 'The Reason We Sing',
    'artist': 'Dick & Melodie Tunney'
}
song_2 = {
    'title': 'When the Mountains Fall',
    'artist': 'Mark Schultz'
}


def test_add_song(client):
    # should not be able to suggest if not signed in
    rv = client.post('/songs', json=song_1)
    assert rv.status_code == 401

    # should be able to suggest song
    client.post('/auth/login', json=user_1)
    rv = client.post('/songs', json=song_1)
    assert rv.status_code == 200
    json = rv.get_json()
    assert json['id'] == 1
    assert json['title'] == song_1['title']
    assert json['artist'] == song_1['artist']
    assert json['lyrics'] == ''
    assert json['edited'] % 1 == 0
    assert json['suggestor'] == 'crossp'
    assert json['myRating'] == None


def test_get_song(client):
    client.post('/auth/login', json=user_1)
    client.post('/songs', json=song_1)

    # should be able to get song
    rv = client.get('/songs/1')
    assert rv.status_code == 200
    json = rv.get_json()
    assert json['id'] == 1
    assert json['title'] == song_1['title']
    assert json['artist'] == song_1['artist']
    assert json['lyrics'] == ''
    assert json['edited'] % 1 == 0
    assert json['suggestor'] == 'crossp'
    assert json['myRating'] == None
    assert json['comments'] == []
    assert json['links'] == []
    # TODO: make sure these lists are not always empty

    # should not be able to get nonexistant song
    rv = client.get('/songs/2')
    assert rv.status_code == 404

    # should not be able to get song when not logged in
    client.post('/auth/logout')
    rv = client.get('/songs/1')
    assert rv.status_code == 401


def test_edit_song(client):
    client.post('/auth/login', json=user_1)
    client.post('/songs', json=song_1)
    client.post('/users', json=user_2)
    client.post('/auth/logout')
    client.post('/auth/login', json=user_2)
    client.post('/songs', json=song_2)
    client.post('/auth/logout')
    client.post('/auth/login', json=user_1)

    # should be able to change title, artist, and lyrics
    rv = client.patch('/songs/1', json={
        'title': 'Reason',
        'artist': 'D&M T',
        'lyrics': 'He has brought us together...',
        'arranged': True
    })
    assert rv.status_code == 200
    assert rv.get_json() == True
    rv = client.get('/songs/1')
    json = rv.get_json()
    assert json['title'] == 'Reason'
    assert json['artist'] == 'D&M T'
    assert json['lyrics'] == 'He has brought us together...'
    assert json['arranged'] == True

    # should be able to unsuggest a song you suggested
    rv = client.patch('/songs/1', json={
        'suggested': False
    })
    assert rv.status_code == 200
    rv = client.get('/songs/1')
    assert rv.get_json()['suggestor'] == None

    # should be able to re-suggest a song that is not suggested
    rv = client.patch('/songs/1', json={
        'suggested': True
    })
    assert rv.status_code == 200
    rv = client.get('/songs/1')
    assert rv.get_json()['suggestor'] == 'crossp'
    
    # should not be able to re-suggest a song that is already suggested
    rv = client.patch('/songs/2', json={
        'title': 'Mountains',
        'suggested': True
    })
    assert rv.status_code == 403
    rv = client.get('/songs/2')
    json = rv.get_json()
    assert json['suggestor'] == 'barryam3'
    assert json['title'] == song_2['title']

    # should not be able to un-suggest somebody else's suggestion
    rv = client.patch('/songs/2', json={
        'title': 'Mountains',
        'suggested': False
    })
    assert rv.status_code == 403
    rv = client.get('/songs/2')
    json = rv.get_json()
    assert json['suggestor'] == 'barryam3'
    assert json['title'] == song_2['title']

    # should not be able to edit nonexistant song
    rv = client.patch('/songs/3', json={})
    assert rv.status_code == 404

    # should not be able to get song when not logged in
    client.post('/auth/logout', json={})
    rv = client.patch('/songs/1')
    assert rv.status_code == 401


def test_delete_song(client):
    client.post('/auth/login', json=user_1)
    client.post('/songs', json=song_1)
    client.post('/songs', json=song_2)

    # should be able to delete song
    rv = client.delete('/songs/1')
    assert rv.status_code == 200
    assert rv.get_json() == True
    rv = client.get('/songs/1')
    assert rv.status_code == 404

    # should not be able to delete nonexistant song
    rv = client.delete('/songs/3')
    assert rv.status_code == 404

    # should not be able to delete song if not logged in
    client.post('/auth/logout')
    rv = client.delete('/songs/2')
    assert rv.status_code == 401

def test_list_songs(client):
    client.post('/auth/login', json=user_1)
    client.post('/songs', json=song_1)
    client.post('/songs', json=song_2)
    client.patch('/songs/1', json={
        'suggested': False
    })
    expected_1 = client.get('/songs/1').get_json()
    del expected_1['links']
    del expected_1['comments']
    expected_2 = client.get('/songs/2').get_json()
    del expected_2['links']
    del expected_2['comments']

    # should be able to list all songs
    rv = client.get('/songs')
    assert rv.status_code == 200
    assert rv.get_json() == [expected_2, expected_1] # TODO: why is this the order?

    # should be able to list all suggested songs
    rv = client.get('/songs?suggested=1')
    assert rv.status_code == 200
    assert rv.get_json() == [expected_2]

    # should be able to list all not-suggested songs
    rv = client.get('/songs?suggested=0')
    assert rv.status_code == 200
    assert rv.get_json() == [expected_1]
