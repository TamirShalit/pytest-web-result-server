import enum

import sqlalchemy_utils

from web_result_server.database import db


class ItemState(enum.Enum):
    DID_NOT_START = 0
    RUNNING = 1
    PASSED = 2
    FAILED = 3
    SKIPPED = 4
    XFAILED = 5
    XPASSED = 6


class TestItem(db.Model):
    """Represents a single PyTest test item."""
    id = db.Column(db.Integer, primary_key=True)
    nodeid = db.Column(db.String(255), nullable=False)
    state = db.Column(sqlalchemy_utils.ChoiceType(ItemState, impl=db.Integer()),
                      nullable=False)
    duration = db.Column(db.Float)
    session_id = db.Column(db.Integer, db.ForeignKey('pytest_session.id'), nullable=False)
