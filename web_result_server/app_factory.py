from flask import Flask


def create_app(name):
    app = Flask(name)
    # SQLALCHEMY_TRACK_MODIFICATIONS is to suppress warning in flask-sqlalchemy
    app.config = {'SERVER_NAME': None, 'DEBUG': False, 'SQLALCHEMY_TRACK_MODIFICATIONS': False}
    return app
