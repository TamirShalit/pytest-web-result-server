import flask_restless

from webresultserver import app_factory
from webresultserver.database import db
from webresultserver.models.item import TestItem
from webresultserver.models.pytest_session import PytestSession


def main():
    flask_app = app_factory.create_app(__name__)
    with flask_app.app_context():
        _create_db(flask_app)
        _create_rest_api(flask_app)
    flask_app.run()


def _create_db(flask_app):
    db.init_app(flask_app)
    db.create_all()


def _create_rest_api(flask_app):
    rest_api_manager = flask_restless.APIManager(flask_app, flask_sqlalchemy_db=db)
    rest_api_manager.create_api(TestItem, methods=['GET', 'POST', 'DELETE', 'PUT'])
    rest_api_manager.create_api(PytestSession, methods=['GET', 'POST', 'PUT'])


if __name__ == '__main__':
    main()
