from webresultserver.database import db


class PytestSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)
    duration = db.Column(db.Float)
    items = db.relationship('TestItem', backref='session', lazy=True)
