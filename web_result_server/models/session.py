from web_result_server.database import db


class Session(db.Model):
    """Represents a Pytest session."""
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)
    duration = db.Column(db.Float)
