import os

import pytest

from web_result_server import app_factory
from web_result_server.database import db as _db

TEST_DB_PATH = os.path.join(os.path.dirname(__file__), 'tests.db')
TEST_DB_URI = 'sqlite:///{db_path}'.format(db_path=TEST_DB_PATH)

TEST_APP_CONFIGURATION = {'TESTING': True, 'SQLALCHEMY_DATABASE_URI': TEST_DB_URI,
                          'SERVER_NAME': None, 'DEBUG': False}


@pytest.fixture(scope='session')
def app():
    flask_app = app_factory.create_app(__name__)
    flask_app.config = TEST_APP_CONFIGURATION
    with flask_app.app_context():
        yield flask_app


@pytest.fixture(scope='session')
def db(app):
    _remove_test_db_file()
    _db.init_app(app)
    _db.create_all()
    yield _db
    _remove_test_db_file()


@pytest.fixture
def session(db):
    """DB session which renews every test and rolles back changes after test has finished."""
    connection = db.engine.connect()
    transaction = connection.begin()
    db.session = db.create_scoped_session(options=(dict(bind=connection, binds={})))
    yield db.session
    transaction.rollback()
    connection.close()
    db.session.remove()


def _remove_test_db_file():
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
