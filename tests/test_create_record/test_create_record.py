from datetime import datetime

import pytest

from webresultserver.models import item, pytest_session

_INITIAL_SESSION_INIT_ARGUMENTS = dict(duration=2.6, start_time=datetime.now())


@pytest.mark.parametrize('init_arguments', [
    dict(nodeid='tests/test_foo.py::test_foo', state=item.ItemState.DID_NOT_START),
    dict(nodeid='tests/sanity/test_bar.py::test_bar', state=item.ItemState.PASSED, duration=0.132)
])
def test_create_pytest_item(db_session, init_arguments):
    initial_session = pytest_session.PytestSession(**_INITIAL_SESSION_INIT_ARGUMENTS)
    db_session.add(initial_session)
    record = item.TestItem(session=initial_session, **init_arguments)
    db_session.add(record)
    db_session.commit()
    row_from_db = item.TestItem.query.filter_by(**init_arguments).first()
    for column_name, element_value in init_arguments.items():
        assert getattr(row_from_db, column_name) == element_value


@pytest.mark.parametrize('init_arguments', [
    dict(duration=21.01, start_time=datetime.now())
])
def test_create_pytest_session(db_session, init_arguments):
    """
    :param dict init_arguments: Keyword arguments for the construction of the record.
                                This is basically the column names and their corresponding values.
    """
    record = pytest_session.PytestSession(**init_arguments)
    db_session.add(record)
    db_session.commit()
    row_from_db = pytest_session.PytestSession.query.filter_by(**init_arguments).first()
    for column_name, element_value in init_arguments.items():
        assert getattr(row_from_db, column_name) == element_value
