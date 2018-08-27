import os

import pytest

from webresultserver import app_factory


@pytest.fixture(scope='session', autouse=True)
def ensure_no_config_in_default_location():
    if os.path.exists(app_factory.DEFAULT_CONFIG_LOCATION):
        raise RuntimeError(
            'Cannot run tests when default config is found.\n'
            'Please move or delete file in {default_config_path} before running tests.\n'
            'To use new config location, set environment variable '
            '"{config_location_environment_variable}" to the new location'.format(
                default_config_path=app_factory.DEFAULT_CONFIG_LOCATION,
                config_location_environment_variable=
                app_factory.CONFIG_LOCATION_ENVIRONMENT_VARIABLE
            ))
