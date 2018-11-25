import pytest
import os

from app import create_app, initialize_database
from app.extensions import db

class TestConfig(object):
    SECRET_KEY = os.environ.get('S2_TEST_SECRET_KEY')
    MYSQL_HOST = os.environ.get('S2_TEST_HOST')
    MYSQL_USER = os.environ.get('S2_TEST_USER')
    MYSQL_PASSWORD = os.environ.get('S2_TEST_PASSWORD')
    MYSQL_DB = os.environ.get('S2_TEST_DB')

@pytest.fixture
def app():
    app = create_app(TestConfig)
    assert app.config['MYSQL_USER'] != 'crossp' # just in case
    db.session.commit() # it seems there may possibly be one open
    db.drop_all()
    initialize_database(app)
    return app
