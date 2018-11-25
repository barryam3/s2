def test_auth(client):
    '''Test of authentication.'''

    # Should be able to log in as default user
    rv = client.post('/auth/login', json={
        'username': 'crossp',
        'password': 'xprod05'
    })
    assert rv.status_code == 200

    # Should be able to get your info
    rv = client.get('/users/me')
    assert rv.get_json()['id'] == 1

    # Should be able to create user accounts.
    rv = client.post('/users', json={
        'username': 'heread'
    })
    assert rv.status_code == 200
    rv = client.post('/users', json={
        'username': 'dcrenter'
    })
    assert rv.status_code == 200
    rv = client.post('/users', json={
        'username': 'msegado'
    })
    assert rv.status_code == 200

    # Should not be able to delete self.
    rv = client.delete('/users/1')
    assert rv.status_code == 403

    # Should be able to promote a user to admin.
    rv = client.put('/users/2/admin', json=True)
    assert rv.status_code == 200

    # Should be able to set a user as inactive.
    rv = client.put('/users/4/active', json=False)
    assert rv.status_code == 200

    # Should not be able to change admin or active of self.
    rv = client.put('/users/1/admin', json=False)
    assert rv.status_code == 403
    rv = client.put('/users/1/active', json=False)
    assert rv.status_code == 403

    # Should be able to sign out.
    rv = client.post('/auth/logout')
    assert rv.status_code == 200

    # Should not be able to get self when signed out.
    rv = client.get('/users/me')
    assert 'id' not in rv.get_json()

    # Should be able to sign in as new active user.
    rv = client.post('/auth/login', json={
        'username': 'dcrenter',
        'password': 'xprod05'
    })
    assert rv.status_code == 200

    # Non-admin should not be able to complete admin actions.
    rv = client.put('/users/1/admin', json=False)
    assert rv.status_code == 403
    rv = client.put('/users/1/active', json=False)
    assert rv.status_code == 403
    rv = client.delete('/users/1')
    assert rv.status_code == 403

    # Should be able to change own password.
    rv = client.put('/users/me/password', json={
        'oldPassword': 'xprod05',
        'newPassword': 'xprod06'
    })
    assert rv.status_code == 200

    # Change password should fail on incorrect old password
    rv = client.put('/users/me/password', json={
        'oldPassword': 'xprod05',
        'newPassword': 'xprod07'
    })
    assert rv.status_code == 401

    rv = client.post('/auth/logout')
    assert rv.status_code == 200

    # Should not be able to sign in with old password.
    rv = client.post('/auth/login', json={
        'username': 'dcrenter',
        'password': 'xprod05'
    })
    assert rv.status_code == 401

    # Should be able to sign in with new password.
    rv = client.post('/auth/login', json={
        'username': 'dcrenter',
        'password': 'xprod06'
    })
    assert rv.status_code == 200

    rv = client.post('/auth/logout')
    assert rv.status_code == 200

    # Should be able to sign in as new admin.
    rv = client.post('/auth/login', json={
        'username': 'heread',
        'password': 'xprod05'
    })

    # Should be able to delete other users.
    rv = client.delete('/users/1')
    assert rv.status_code == 200

    # Should be able to reset other users' passwords.
    rv = client.delete('/users/3/password')
    assert rv.status_code == 200

    rv = client.post('/auth/logout')
    assert rv.status_code == 200

    # Should not be able to sign in as deleted user.
    rv = client.post('/auth/login', json={
        'username': 'crossp',
        'password': 'xprod05'
    })
    assert rv.status_code == 401

    # Should not be able to sign in with password before reset.
    rv = client.post('/auth/login', json={
        'username': 'dcrenter',
        'password': 'xprod06'
    })
    assert rv.status_code == 401

    # Should be able to sign in with default password after reset.
    rv = client.post('/auth/login', json={
        'username': 'dcrenter',
        'password': 'xprod05'
    })
    assert rv.status_code == 200

    rv = client.post('/auth/logout')
    assert rv.status_code == 200
