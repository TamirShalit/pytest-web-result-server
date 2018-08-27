import contextlib
import os

from webresultserver import app_factory


@contextlib.contextmanager
def use_config(config_location):
    try:
        os.environ[app_factory.CONFIG_LOCATION_ENVIRONMENT_VARIABLE] = config_location
        yield
    finally:
        if app_factory.CONFIG_LOCATION_ENVIRONMENT_VARIABLE in os.environ:
            del os.environ[app_factory.CONFIG_LOCATION_ENVIRONMENT_VARIABLE]
