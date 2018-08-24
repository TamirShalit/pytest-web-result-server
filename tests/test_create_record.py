from datetime import datetime

import pytest

from web_result_server.models import item, pytest_session

INITIAL_PYTEST_SESSION = pytest_session.PytestSession(duration=2.6, start_time=datetime.now())


@pytest.mark.parametrize('init_arguments', [
    dict(nodeid='tests/test_foo.py::test_foo', state=item.ItemState.DID_NOT_START),
    dict(nodeid='tests/sanity/test_bar.py::test_bar', state=item.ItemState.PASSED, duration=0.132)
])
def test_create_pytest_item(session, init_arguments):
    session.add(INITIAL_PYTEST_SESSION)
    record = item.TestItem(session=INITIAL_PYTEST_SESSION, **init_arguments)
    session.add(record)
    session.commit()
    row_from_db = item.TestItem.query.filter_by(**init_arguments).first()
    for column_name, element_value in init_arguments.items():
        assert getattr(row_from_db, column_name) == element_value


@pytest.mark.parametrize('init_arguments', [
    dict(duration=21.01, start_time=datetime.now())
])
def test_create_pytest_session(session, init_arguments):
    """
    :param dict init_arguments: Keyword arguments for the construction of the record.
                                This is basically the column names and their corresponding values.
    """
    record = pytest_session.PytestSession(**init_arguments)
    session.add(record)
    session.commit()
    row_from_db = pytest_session.PytestSession.query.filter_by(**init_arguments).first()
    for column_name, element_value in init_arguments.items():
        assert getattr(row_from_db, column_name) == element_value
