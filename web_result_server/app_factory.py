from flask import Flask


CONFIG_LOCATION_ENVIRONMENT_VARIABLE = 'WEB_RESULTS_SERVER_CONFIG'


def create_app(name):
    app = Flask(name)
    # SQLALCHEMY_TRACK_MODIFICATIONS is to suppress warning in flask-sqlalchemy
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app
