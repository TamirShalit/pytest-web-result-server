from web_result_server.database import db


class PytestSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)
    duration = db.Column(db.Float)