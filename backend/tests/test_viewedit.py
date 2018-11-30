# timestamps are in seconds so it is necessary to slow this test down
from time import sleep

user_1 = {
    'username': 'crossp',
    'password': 'xprod05'
}

song_1 = {
    'title': 'The Reason We Sing',
    'artist': 'Dick & Melodie Tunney'
}


def test_views(client):
    client.post('/auth/login', json=user_1)
    client.post('/songs', json=song_1)

    # view should start at zero
    client.post('/songs', json=song_1)
    rv = client.get('/songs')
    assert rv.get_json()[0]['lastViewed'] == 0

    # view should update when viewing song
    rv = client.get('/songs/1', json=song_1)
    json = rv.get_json()
    assert json['lastViewed'] > 0
    last_edited = json['lastEdited']

    # edit should update when song is modified
    sleep(1)
    rv = client.patch('/songs/1', json={ 'title': 'foo' })
    assert rv.status_code == 200
    rv = client.get('/songs/1')
    new_last_edited = rv.get_json()['lastEdited']
    assert new_last_edited > last_edited
    last_edited = new_last_edited

    # edit should update when song is commented on
    sleep(1)
    rv = client.post('/songs/1/comments', json={ 'text': 'foo' })
    assert rv.status_code == 200
    rv = client.get('/songs/1')
    new_last_edited = rv.get_json()['lastEdited']
    assert new_last_edited > last_edited
    last_edited = new_last_edited

    # edit should update when song is linked to
    sleep(1)
    rv = client.post('/songs/1/links', json={
        'url': 'http://google.com',
        'description': 'google'
    })
    assert rv.status_code == 200
    rv = client.get('/songs/1')
    new_last_edited = rv.get_json()['lastEdited']
    assert new_last_edited > last_edited
    last_edited = new_last_edited
