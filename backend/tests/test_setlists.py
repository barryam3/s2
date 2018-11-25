import datetime

def test_setlists(client):
    now = datetime.datetime.utcnow().replace(microsecond=0)
    one_month_from_now = (now + datetime.timedelta(365/12)).isoformat()
    two_months_from_now = (now + datetime.timedelta(2*365/12)).isoformat()
    setlist_1 = {
        'title': 'Fall 2001',
        'suggestDeadline': now.isoformat(),
        'voteDeadline': one_month_from_now,
    }
    setlist_2 = {
        'title': 'Fall 2002',
        'suggestDeadline': one_month_from_now,
        'voteDeadline': two_months_from_now
    }

    # Should not be able to create a setlist if not signed in.
    rv = client.post('/setlists', json=setlist_1)
    assert rv.status_code == 401

    rv = client.post('/auth/login', json={
        'username': 'crossp',
        'password': 'xprod05'
    })
    assert rv.status_code == 200

    # Admin should be able to create a setlist.
    rv = client.post('/setlists', json=setlist_1)
    assert rv.status_code == 200
    json = rv.get_json()
    assert json['id'] == 1
    assert json['title'] == setlist_1['title']
    assert json['suggestDeadline'] == setlist_1['suggestDeadline']
    assert json['voteDeadline'] == setlist_1['voteDeadline']
    setlist_1 = json

    # Should be able to get setlist.
    rv = client.get('/setlists')
    assert rv.status_code == 200
    json = rv.get_json()
    assert len(json) == 1
    assert json[0] == setlist_1

    # Should always get newest setlist.
    rv = client.post('/setlists', json=setlist_2)
    assert rv.status_code == 200
    json = rv.get_json()
    assert json['id'] == 2
    assert json['title'] == setlist_2['title']
    assert json['suggestDeadline'] == setlist_2['suggestDeadline']
    assert json['voteDeadline'] == setlist_2['voteDeadline']
    setlist_2 = json
  
    rv = client.get('/setlists')
    assert rv.status_code == 200
    json = rv.get_json()
    assert len(json) == 1
    assert json[0] == setlist_2

    # Non-admin should not be able to create a setlist.
    rv = client.post('/users', json={
        'username': 'barryam3'
    })
    assert rv.status_code == 200

    rv = client.post('/auth/logout')
    assert rv.status_code == 200

    rv = client.post('/auth/login', json={
        'username': 'barryam3',
        'password': 'xprod05'
    })
    assert rv.status_code == 200

    rv = client.post('/setlists', json=setlist_1)
    assert rv.status_code == 403

    rv = client.post('/auth/logout')
    assert rv.status_code == 200
