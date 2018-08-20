import flask_sqlalchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = flask_sqlalchemy.SQLAlchemy(app)
