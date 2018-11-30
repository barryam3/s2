user_1 = {
    'username': 'crossp',
    'password': 'xprod05'
}

song_1 = {
    'title': 'The Reason We Sing',
    'artist': 'Dick & Melodie Tunney'
}

link_1 = {
    'url': 'https://www.youtube.com/watch?v=18Szu0agQeU',
    'description': 'First Call Video'
}

def test_links(client):
    client.post('/auth/login', json=user_1)
    client.post('/songs', json=song_1)

    # should be able to add a link
    rv = client.post('/songs/1/links', json=link_1)
    assert rv.status_code == 200
    json = rv.get_json()
    assert json['url'] == link_1['url']
    assert json['description'] == link_1['description']

    # should be able to get song's links
    rv = client.get('/songs/1')
    json = rv.get_json()
    assert json['links'][0]['url'] == link_1['url']
    assert json['links'][0]['description'] == link_1['description']

    # should be able to delete a link
    rv = client.delete('/links/1')
    assert rv.status_code == 200
    assert rv.get_json() == True
    rv = client.get('/songs/1')
    assert rv.get_json()['links'] == []

    # should not be able to add a link to a nonexistant song
    rv = client.post('/songs/2/links', json=link_1)
    assert rv.status_code == 404

    # should not be able to add a link if not signed in
    client.post('/auth/logout')
    rv = client.post('/songs/1/links', json=link_1)
    assert rv.status_code == 401