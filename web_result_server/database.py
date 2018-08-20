import flask_sqlalchemy

from web_result_server.app import app

db = flask_sqlalchemy.SQLAlchemy(app)