"""

Tests for blacklist and token revoking

"""

import json
from .util import make_token_header

#
# TEST DATA
#


def test_revoke_token(client, auth):

    response = client.get('/api/v1/auth/tokens')
    assert response.status_code == 401

    # create a new user
    auth.signup()
    access_token = auth.access_token
    token_header = make_token_header(access_token)
 
    response = client.get('/api/v1/auth/tokens', headers=token_header)
    assert response.status_code == 200
    assert b'data' in response.data
    data = json.loads(response.data.decode('utf-8'))['data'][0]
    assert data['token_type'] == 'access'
    assert data['revoked'] == False
    assert data['expires']
    assert data['user_identity']
    assert data['jti']

    token_id = data['token_id']

    # Revoke token
    path = '/api/v1/auth/tokens/{}'.format(token_id)
    response = client.put(path)
    assert response.status_code == 401

    response = client.put(path, headers=token_header)
    assert response.status_code == 400

    response = client.put(path, headers=token_header, data={'revoke': True})
    assert response.status_code == 200
    assert b'status' in response.data
    assert b'message' in response.data
    
    # check revocation is successful
    response = client.put(path, headers=token_header)
    assert response.status_code == 401