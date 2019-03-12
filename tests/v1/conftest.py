"""
tests.v1.conftest
~~~~~~~~~~~~~~~~~~

setup functions to be used by test modules
"""

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
    def __init__(self, client):
        self._client = client

    def signup(self, **kwargs):
        return self._client.post('/api/v1/auth/signup', data=kwargs)

    def login(self, **kwargs):
        return self._client.post('/api/v1/auth/signin', data=kwargs)

    def logout(self, **kwargs):
        return self._client.post('/api/v1/auth/logout', data=kwargs)

@pytest.fixture
def auth(client):
    return AuthActions(client)
