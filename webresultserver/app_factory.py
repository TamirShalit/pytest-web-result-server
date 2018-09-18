import os

import flask_restless
from flask import Flask

from webresultserver.database import db
from webresultserver.models.item import TestItem
from webresultserver.models.pytest_session import PytestSession

DEFAULT_CONFIG_LOCATION = os.path.expanduser('~/web_results_server.json')
CONFIG_LOCATION_ENVIRONMENT_VARIABLE = 'WEB_RESULTS_SERVER_CONFIG'
DB_URI_CONFIG_KEY = 'SQLALCHEMY_DATABASE_URI'


def create_app(name):
    app = Flask(name)
    # SQLALCHEMY_TRACK_MODIFICATIONS is to suppress warning in flask-sqlalchemy
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    config_location = os.getenv(CONFIG_LOCATION_ENVIRONMENT_VARIABLE, DEFAULT_CONFIG_LOCATION)
    app.config.from_json(config_location)
    if DB_URI_CONFIG_KEY not in app.config:
        raise ValueError(
            'DB not specified. Please specify SQLAlchemy URI in config key "{0}"'.format(
                DB_URI_CONFIG_KEY))
    return app


def create_db(flask_app):
    db.init_app(flask_app)
    db.create_all()


def create_rest_api(flask_app):
    rest_api_manager = flask_restless.APIManager(flask_app, flask_sqlalchemy_db=db)
    rest_api_manager.create_api(TestItem, methods=['GET', 'POST', 'DELETE', 'PUT'])
    rest_api_manager.create_api(PytestSession, methods=['GET', 'POST', 'PUT'])
