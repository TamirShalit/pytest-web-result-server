import os

import pytest

from web_result_server import app_factory

TEST_DB_PATH = os.path.join(os.path.dirname(__file__), 'tests.db')
TEST_DB_URI = 'sqlite:///{db_path}'.format(db_path=TEST_DB_PATH)

TEST_APP_CONFIGURATION = {'TESTING': True, 'SQLALCHEMY_DATABASE_URI': TEST_DB_URI}


@pytest.fixture(scope='session')
def app():
    flask_app = app_factory.create_app(__name__)
    flask_app.config = TEST_APP_CONFIGURATION
    with flask_app.app_context():
        yield flask_app
