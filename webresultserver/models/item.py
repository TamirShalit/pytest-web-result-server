import enum

import sqlalchemy_utils

from webresultserver.database import db


class ItemState(enum.IntEnum):
    DID_NOT_START = 0
    RUNNING_SETUP = 1
    RUNNING_TEST = 2
    RUNNING_TEARDOWN = 3
    PASSED = 4
    FAILED = 5
    SKIPPED = 6
    XFAILED = 7
    XPASSED = 8


class TestItem(db.Model):
    """Represents a single PyTest test item."""
    id = db.Column(db.Integer, primary_key=True)
    nodeid = db.Column(db.String(255), nullable=False)
    state = db.Column(sqlalchemy_utils.ChoiceType(ItemState, impl=db.Integer()),
                      nullable=False)
    duration = db.Column(db.Float)
    session_id = db.Column(db.Integer, db.ForeignKey('pytest_session.id'), nullable=False)

    __table_args__ = (db.UniqueConstraint('nodeid', 'session_id'),)
