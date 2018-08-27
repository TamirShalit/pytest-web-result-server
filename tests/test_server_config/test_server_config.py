import os

import pytest

from web_result_server import app_factory
from web_result_server.app_factory import DB_URI_CONFIG_KEY

_CURRENT_DIRECTORY = os.path.dirname(__file__)

_TEST_CONFIG_LOCATION = os.path.join(_CURRENT_DIRECTORY, 'test_config.json')
_EMPTY_CONFIG_LOCATION = os.path.join(_CURRENT_DIRECTORY, 'empty_config.json')


@pytest.fixture
def use_config():
    def _use_config(location):
        os.environ[app_factory.CONFIG_LOCATION_ENVIRONMENT_VARIABLE] = location

    yield _use_config
    del os.environ[app_factory.CONFIG_LOCATION_ENVIRONMENT_VARIABLE]


def test_load_config(use_config):
    use_config(_TEST_CONFIG_LOCATION)
    app = app_factory.create_app(__name__)
    assert app.config[DB_URI_CONFIG_KEY] == 'sqlite:///not_exist'


def test_exception_raised_when_no_db_uri(use_config):
    use_config(_EMPTY_CONFIG_LOCATION)
    with pytest.raises(ValueError):
        app_factory.create_app(__name__)
