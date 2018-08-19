import sqlalchemy

from web_result_server.models.base import Base


class TestItem(Base):
    """Represents a result for a single test item."""
    __tablename__ = 'items'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
