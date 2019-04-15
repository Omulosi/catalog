"""
tests.v1.conftest
~~~~~~~~~~~~~~~~~~

setup functions to be used by test modules
"""

import json
import pytest
from app import create_app, db
from config import TestConfig

@pytest.fixture
def app():

    app = create_app(TestConfig)

    with app.app_context():
        db.drop_all()
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

class AuthActions(object):
    """
    This class provides methods for authenticating users.
    """

    DEFAULT_USER_LOGINS = {'email':'user@example.com', 'password':'r@78hy'}

    def __init__(self, client):
        self._client = client
        self.access_token = None
        self.refresh_token = None

    def signup(self, **kwargs):
        user_data = kwargs
        if not kwargs:
            user_data = self.DEFAULT_USER_LOGINS
        response =  self._client.post('/api/v1/auth/signup', data=user_data)
        data = json.loads(response.data.decode('utf-8'))
        self.access_token = data['data'][0]['access_token']
        self.refresh_token = data['data'][0]['refresh_token']

        return response

    def login(self, **kwargs):
        user_data = kwargs
        if not kwargs:
            user_data = self.DEFAULT_USER_LOGINS
        response =  self._client.post('/api/v1/auth/signin', data=user_data)
        data = json.loads(response.data.decode('utf-8'))
        self.access_token = data['data'][0]['access_token']
        self.refresh_token = data['data'][0]['refresh_token']

        return response


    def logout(self, **kwargs):
        return self._client.delete('/api/v1/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)
