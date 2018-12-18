from calendar import timegm
from datetime import datetime

now = timegm(datetime.utcnow().timetuple())

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


def test_set_deadlines(client):
    client.post('/auth/login', json=user_1)
    client.post('/users', json=user_2)
    client.post('/songs', json=song_1)
    client.post('/songs', json=song_2)
    client.patch('/songs/2', json={ 'suggested': False })

    # deadlines should start unset
    rv = client.get('/groups/1')
    assert rv.status_code == 200
    json = rv.get_json()
    assert json['suggestDeadline'] == None
    assert json['rateDeadline'] == None

    # should be able to update deadlines
    rv = client.put('/groups/1/deadlines', json={
        'suggestDeadline': now + 1000,
        'rateDeadline': now + 1000
    })
    assert rv.status_code == 200
    assert rv.get_json() == True

    # should be able to get the deadlines
    rv = client.get('/groups/1')
    assert rv.status_code == 200
    json = rv.get_json()
    assert json['suggestDeadline'] == now + 1000
    assert json['rateDeadline'] == now + 1000

    # should be able to add song if the deadline has not passed
    rv = client.post('/songs', json=song_1)
    assert rv.status_code == 200

    # should be able to rate if the deadline has not passed
    rv = client.put('/songs/1/ratings/mine', json={ 'rating': 6 })
    assert rv.status_code == 200

    # should be able to unsuggest if the deadline has not passed
    rv = client.patch('/songs/1', json={
        'suggested': False
    })
    assert rv.status_code == 200

    # should be able to suggest if the deadline has not passed
    rv = client.patch('/songs/1', json={
        'suggested': True
    })
    assert rv.status_code == 200

    client.put('/groups/1/deadlines', json={
        'suggestDeadline': now - 1000,
        'rateDeadline': now - 1000
    })

    # should not be able to rate if the deadline has passed
    rv = client.put('/songs/1/ratings/mine', json={ 'rating': 5 })
    assert rv.status_code == 403

    # should not be able to suggest if the deadline has passed
    rv = client.patch('/songs/2', json={
        'suggested': True
    })
    assert rv.status_code == 403

    # should not be able to unsuggest if the deadline has passed
    rv = client.patch('/songs/1', json={
        'suggested': False
    })
    assert rv.status_code == 403

    # should not be able to add song if the deadline has passed
    rv = client.post('/songs', json=song_3)
    assert rv.status_code == 403

    # should be able to unset deadlines
    rv = client.put('/groups/1/deadlines', json={
        'suggestDeadline': None,
        'rateDeadline': None
    })
    assert rv.status_code == 200

    # should not be able to change deadlines if not logged in
    client.post('/auth/logout')
    rv = client.put('/groups/1/deadlines', json={
        'suggestDeadline': now + 500,
        'rateDeadline': now + 500
    })
    assert rv.status_code == 401

    # should not be able to get deadlines if not logged in
    rv = client.get('/groups/1')
    assert rv.status_code == 401

    # should not be able to change deadlines if not admin
    client.post('/auth/login', json=user_2)
    rv = client.put('/groups/1/deadlines', json={
        'suggestDeadline': now + 750,
        'rateDeadline': now + 750
    })
    assert rv.status_code == 403

    # should not be able to get deadlines if not admin
    rv = client.get('/groups/1')
    assert rv.status_code == 403

# TODO: reset site test

# TODO: get ratings test