"""
tests.v1.test_auth
~~~~~~~~~~~~~~~~~~

Tests for authentication
"""

import json
import pytest

#
# SAMPLE INPUT DATA
#

VALID_USER_DATA = {'email': 'user@example.com', 'password': 'youcantguess#4'}
# email should not be empty
INVALID_USER_EMAIL_1 = {'email': '', 'password': 'youcantguess#4'}
# email should not be blank
INVALID_USER_EMAIL_2 = {'email': '  ', 'password': 'youcantguess#4'}
# email should have correct format
INVALID_USER_EMAIL_3 = {'email': 'example.com', 'password': 'youcantguess#4'}
# email field should be present
INVALID_USER_EMAIL_4 = {'password': 'youcantguess#4'}

# password should not be empty
INVALID_USER_PASSWORD_1 = {'email': 'user@example.com', 'password': ''}
# password should not be blank
INVALID_USER_PASSWORD_2 = {'email': 'user@example.com', 'password': '  '}
# password should be at least 3 characters long
INVALID_USER_PASSWORD_3 = {'email': 'user@example.com', 'password': 'abc'}
# password should include a number and a special character
INVALID_USER_PASSWORD_4 = {'email': 'user@example.com', 'password': 'secret'}
INVALID_USER_PASSWORD_5 = {'email': 'user@example.com', 'password': '93secret'}
INVALID_USER_PASSWORD_6 = {'email': 'user@example.com', 'password': '#sec%ret'}
# password field should be present
INVALID_USER_PASSWORD_7 = {'email': 'user@example.com',}

# user should be unique
USER_ALREADY_EXISTS = {'email': 'user@example.com', 'password':
        'youcantguess#4'}
# user should have valid credentials, if email and password both have the
# correct format
INVALID_USER_CREDENTIALS = {'email': 'sneakyuser@example.com', 'password':
        'iamsneaky#9'}

@pytest.mark.parametrize(('path'), (
    ('/api/v1/auth/signup'),
    ('/api/v1/auth/signin')))
def test_authentication_with_valid_data(client, path, auth):
    """
    Tests for the signup and signin endpoints when valid and correctly
    formatted data is supplied.

    args:
        - client - application client for making requests
        - path - URI for signin/signup.
    """

    if 'signup' in path:
        response = client.post(path, data=VALID_USER_DATA)
        assert response.status_code == 201
    if 'signin' in path:
        create_user_response = auth.signup(**VALID_USER_DATA)
        assert create_user_response.status_code == 201
        # user now exists in the test database, okay to query
        response = client.post(path, data=VALID_USER_DATA)
        assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert 'data' in data
    assert 'access_token' in data['data'][0]
    assert 'user' in data['data'][0]

@pytest.mark.parametrize(('invalid_user_data', 'message'),(
                        # user signup
                        (INVALID_USER_EMAIL_1, 'Invalid email format'),
                        (INVALID_USER_EMAIL_2, 'Invalid email format'),
                        (INVALID_USER_EMAIL_3, 'Invalid email format'),
                        (INVALID_USER_EMAIL_4, 'Invalid email format'),
                        (INVALID_USER_PASSWORD_1, 'Invalid password. Should be'
                            ' at least 5 characters long and include a number'
                            ' and a special character'),
                        (INVALID_USER_PASSWORD_2, 'Invalid password. Should be'
                            ' at least 5 characters long and include a number'
                            ' and a special character'),
                        (INVALID_USER_PASSWORD_3, 'Invalid password. Should be'
                            ' at least 5 characters long and include a number'
                            ' and a special character'),
                        (INVALID_USER_PASSWORD_4, 'Invalid password. Should be'
                            ' at least 5 characters long and include a number'
                            ' and a special character'),
                        (INVALID_USER_PASSWORD_5, 'Invalid password. Should be'
                            ' at least 5 characters long and include a number'
                            ' and a special character'),
                        (INVALID_USER_PASSWORD_6, 'Invalid password. Should be'
                            ' at least 5 characters long and include a number'
                            ' and a special character'),
                        (INVALID_USER_PASSWORD_7, 'Invalid password. Should be'
                            ' at least 5 characters long and include a number'
                            ' and a special character'),
                        (USER_ALREADY_EXISTS, 'User already exists'),
                        ))
def test_signup_with_invalid_data(client, auth, invalid_user_data, message):
    # pre-create a user to test user already exists fucntionality
    auth.signup(**VALID_USER_DATA)
    # Invalid signup
    response = client.post('/api/v1/auth/signup', data=invalid_user_data)
    assert response.status_code == 400
    data = json.loads(response.data.decode('utf-8'))
    # check that response has correct format
    assert 'status' in data
    assert 'error' in data
    assert message in data['error']


@pytest.mark.parametrize(('invalid_user_data', 'message'),(
                        # user signin
                        (INVALID_USER_EMAIL_1, 'Invalid email format'),
                        (INVALID_USER_EMAIL_2, 'Invalid email format'),
                        (INVALID_USER_EMAIL_3, 'Invalid email format'),
                        (INVALID_USER_EMAIL_4, 'Invalid email format'),
                        (INVALID_USER_PASSWORD_1, 'Invalid password. Should be'
                            ' at least 5 characters long and include a number'
                            ' and a special character'),
                        (INVALID_USER_PASSWORD_2, 'Invalid password. Should be'
                            ' at least 5 characters long and include a number'
                            ' and a special character'),
                        (INVALID_USER_PASSWORD_3, 'Invalid password. Should be'
                            ' at least 5 characters long and include a number'
                            ' and a special character'),
                        (INVALID_USER_PASSWORD_4, 'Invalid password. Should be'
                            ' at least 5 characters long and include a number'
                            ' and a special character'),
                        (INVALID_USER_PASSWORD_5, 'Invalid password. Should be'
                            ' at least 5 characters long and include a number'
                            ' and a special character'),
                        (INVALID_USER_PASSWORD_6, 'Invalid password. Should be'
                            ' at least 5 characters long and include a number'
                            ' and a special character'),
                        (INVALID_USER_PASSWORD_7, 'Invalid password. Should be'
                            ' at least 5 characters long and include a number'
                            ' and a special character'),
                        ))
def test_signin_with_invalid_data(client, auth, invalid_user_data, message):
    # create a user before proceeding
    auth.signup(**VALID_USER_DATA)

    # Invalid signin
    response = client.post('/api/v1/auth/signin', data=invalid_user_data)
    assert response.status_code == 400
    data = json.loads(response.data.decode('utf-8'))
    # check that response has correct format
    assert 'status' in data
    assert 'error' in data
    assert message in data['error']

def test_signin_with_invalid_credentials(client, auth):
    # create a user before proceeding
    auth.signup(**VALID_USER_DATA)

    # signin with invalid credentials
    response = client.post('/api/v1/auth/signin', data=INVALID_USER_CREDENTIALS)
    assert response.status_code == 401
    assert b'status' in response.data
    assert b'error' in response.data
