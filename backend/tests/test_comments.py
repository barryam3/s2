user_1 = {
    'username': 'crossp',
    'password': 'xprod05'
}

user_2 = {
    'username': 'craigtho',
    'password': 'xprod05'
}

song_1 = {
    'title': 'The Reason We Sing',
    'artist': 'Dick & Melodie Tunney'
}

comment_1 = {
    'text': 'Down with butterflies; up with moths!'
}

comment_2 = {
    'text': 'Just go for it! You never know what might happen!'
}

def test_links(client):
    client.post('/auth/login', json=user_1)
    client.post('/songs', json=song_1)
    client.post('/users', json=user_2)

    # should be able to add a comment
    rv = client.post('/songs/1/comments', json=comment_1)
    assert rv.status_code == 200
    json = rv.get_json()
    assert json['text'] == comment_1['text']
    assert json['timestamp'] % 1 == 0

    # should be able to get song's comments
    rv = client.get('/songs/1')
    json = rv.get_json()
    assert json['comments'][0]['id'] == 1
    assert json['comments'][0]['text'] == comment_1['text']
    assert len(json['comments']) == 1

    # should be able to edit a comment
    rv = client.patch('/comments/1', json=comment_2)
    assert rv.status_code == 200
    assert rv.get_json() == True
    rv = client.get('/songs/1')
    json = rv.get_json()
    assert json['comments'][0]['id'] == 1
    assert json['comments'][0]['text'] == comment_2['text']
    assert len(json['comments']) == 1

    # should be able to add a second comment
    client.post('/songs/1/comments', json=comment_1)
    rv = client.get('/songs/1')
    assert len(rv.get_json()['comments']) == 2

    # should be able to delete a comment
    rv = client.delete('/comments/1')
    assert rv.status_code == 200
    assert rv.get_json() == True
    rv = client.delete('/comments/2')
    assert rv.status_code == 200
    rv = client.get('/songs/1')
    assert rv.get_json()['comments'] == []

    # should not be able to add a comment to a nonexistant song
    rv = client.post('/songs/2/comments', json=comment_1)
    assert rv.status_code == 404

    client.post('/songs/1/comments', json=comment_2)

    # should not be able to add a comment if not signed in
    client.post('/auth/logout')
    rv = client.post('/songs/1/comments', json=comment_1)
    assert rv.status_code == 401

    # should not be able to modify somebody else's comment
    client.post('/auth/login', json=user_2)
    rv = client.patch('/comments/3', json=comment_1)
    assert rv.status_code == 403

    # should not be able to delete somebody else's comment
    rv = client.delete('/comments/3')
    assert rv.status_code == 403
