import flask_restless

from web_result_server import app_factory
from web_result_server.database import db
from web_result_server.models.item import TestItem
from web_result_server.models.pytest_session import PytestSession


def main():
    app = app_factory.create_app(__name__)
    with app.app_context():
        db.init_app(app)
        db.create_all()
        _create_rest_api(app)
    app.run()


def _create_rest_api(flask_app):
    rest_api_manager = flask_restless.APIManager(flask_app, flask_sqlalchemy_db=db)
    rest_api_manager.create_api(TestItem, methods=['GET', 'POST', 'DELETE', 'PUT'])
    rest_api_manager.create_api(PytestSession, methods=['GET', 'POST', 'PUT'])


if __name__ == '__main__':
    main()
