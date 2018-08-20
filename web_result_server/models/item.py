import enum

import sqlalchemy
import sqlalchemy_utils

from web_result_server.models.base import Base


class ItemState(enum.Enum):
    DID_NOT_START = 0
    RUNNING = 1
    PASSED = 2
    FAILED = 3
    SKIPPED = 4
    XFAILED = 5
    XPASSED = 6


class TestItem(Base):
    """Represents a single test item."""
    __tablename__ = 'items'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    nodeid = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    state = sqlalchemy.Column(sqlalchemy_utils.ChoiceType(ItemState, impl=sqlalchemy.Integer()),
                              nullable=False)
    duration = sqlalchemy.Column(sqlalchemy.Float)
