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
