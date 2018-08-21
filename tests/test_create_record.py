from datetime import datetime

import pytest

from web_result_server.models import item, session


@pytest.mark.parametrize('record_class, init_arguments', [
    (item.TestItem, dict(nodeid='tests/test_foo.py::test_foo',
                         state=item.ItemState.DID_NOT_START)),
    (item.TestItem, dict(nodeid='tests/sanity/test_bar.py::test_bar',
                         state=item.ItemState.PASSED,
                         duration=0.132)),
    (session.Session, dict(duration=21.01, start_time=datetime.now()))
])
def test_create_record(session, record_class, init_arguments):
    """
    :param db.Model record_class: SQLAlchemy class of the record.
    :param dict init_arguments: Keyword arguments for the construction of the record.
                                This is basically the column names and their corresponding values.
    """
    record = record_class(**init_arguments)
    session.add(record)
    session.commit()
    row_from_db = record_class.query.first()
    for column_name, element_value in init_arguments.items():
        assert getattr(row_from_db, column_name) == element_value
