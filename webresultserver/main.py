from webresultserver import app_factory
from webresultserver.app_factory import create_db, create_rest_api


def main():
    flask_app = app_factory.create_app(__name__)
    with flask_app.app_context():
        create_db(flask_app)
        create_rest_api(flask_app)
    flask_app.run()


if __name__ == '__main__':
    main()
