from flask import Flask


def create_app(name):
    app = Flask(name)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    return app
