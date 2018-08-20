from flask import Flask


def create_app(name):
    app = Flask(name)
    return app
