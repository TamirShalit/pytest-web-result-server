import sqlalchemy
import sqlalchemy_utils
import enum

from web_result_server.models.base import Base


class PytestResult(enum.Enum):
    PASSED = 1
    FAILED = 2
    SKIPPED = 3
    XFAILED = 4
    XPASSED = 5


class TestItem(Base):
    """Represents a single test item."""
    __tablename__ = 'items'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    nodeid = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    result = sqlalchemy.Column(sqlalchemy_utils.ChoiceType(PytestResult), nullable=False)
    duration = sqlalchemy.Column(sqlalchemy.Float)
