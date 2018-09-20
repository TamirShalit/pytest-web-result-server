from datetime import datetime

import flask_restful

from webresultserver.database import db
from webresultserver.models.pytest_session import PytestSession


class PytestSessionResource(flask_restful.Resource):
    def post(self):
        new_pytest_session = PytestSession(start_time=datetime.now())
        db.session.add(new_pytest_session)
        db.session.commit()
        return new_pytest_session.id
