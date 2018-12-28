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

song_3 = {
    'title': 'And Can It Be',
    'artist': 'GLAD'
}


def test_user_engagement(client):
    client.post('/auth/login', json=user_1)
    client.post('/users', json=user_2)
    client.post('/songs', json=song_1)
    client.post('/songs', json=song_2)
    client.post('/auth/logout')
    client.post('/auth/login', json=user_2)
    client.post('/songs', json=song_3)
    client.put('/songs/1/ratings/mine', json={ 'rating': 1 })
    client.put('/songs/1/ratings/mine', json={ 'rating': 2 })
    client.post('/auth/logout')
    client.post('/auth/login', json=user_1)
    client.patch('/songs/2', json={ 'suggested': False })
    rv = client.get('/users?active=1')
    assert rv.status_code == 200
    json = rv.get_json()
    assert len(json) == 2
    assert json[0]['id'] == 1
    assert json[0]['numSuggestions'] == 1
    assert json[0]['numRatings'] == 0
    assert json[1]['id'] == 2
    assert json[1]['numSuggestions'] == 1
    assert json[1]['numRatings'] == 1
