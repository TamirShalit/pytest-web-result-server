from flask import Flask


def create_app(name):
    app = Flask(name)
    app.config = {'SERVER_NAME': None, 'DEBUG': False}
    return app
