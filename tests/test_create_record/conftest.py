import os

import pytest

from tests import utils
from webresultserver import app_factory
from webresultserver.database import db as _db

TEST_DB_PATH = os.path.join(os.path.dirname(__file__), 'test.db')
CONFIG_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'test_config.template')


def _create_config(tmpdir_factory):
    with open(CONFIG_TEMPLATE_PATH) as config_template:
        config_text = config_template.read().format(db_location=TEST_DB_PATH)
    config_path_object = tmpdir_factory.getbasetemp().join('test_config.json')
    config_path_object.write(config_text)
    return config_path_object


@pytest.fixture(scope='session')
def app(tmpdir_factory):
    config_path_object = _create_config(tmpdir_factory)
    with utils.use_config(config_path_object.strpath):
        flask_app = app_factory.create_app(__name__)
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
def db_session(db):
    """DB session which renews every test and rolles back changes after test has finished."""
    with db.engine.connect() as connection:
        transaction = connection.begin()
        db.session = db.create_scoped_session(options=(dict(bind=connection, binds={})))
        yield db.session
        transaction.rollback()
        db.session.remove()


def _remove_test_db_file():
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
