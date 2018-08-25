import os

from web_result_server import app_factory


_TEST_CONFIG_LOCATION = os.path.join(os.path.dirname(__file__), 'test_config.json')


def test_load_config():
    os.environ[app_factory.CONFIG_LOCATION_ENVIRONMENT_VARIABLE] = _TEST_CONFIG_LOCATION
    app = app_factory.create_app(__name__)
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///not_exist'
