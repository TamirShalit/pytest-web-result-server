import os

from flask import Flask

DEFAULT_CONFIG_LOCATION = os.path.expanduser('~/web_results_server.json')
CONFIG_LOCATION_ENVIRONMENT_VARIABLE = 'WEB_RESULTS_SERVER_CONFIG'
DB_URI_CONFIG_KEY = 'SQLALCHEMY_DATABASE_URI'


def create_app(name):
    app = Flask(name)
    # SQLALCHEMY_TRACK_MODIFICATIONS is to suppress warning in flask-sqlalchemy
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    config_location = os.getenv(CONFIG_LOCATION_ENVIRONMENT_VARIABLE, DEFAULT_CONFIG_LOCATION)
    app.config.from_json(config_location)
    return app
