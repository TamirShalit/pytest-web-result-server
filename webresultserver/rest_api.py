from datetime import datetime

import flask
import flask_restful

from webresultserver.database import db
from webresultserver.models.item import TestItem, ItemState
from webresultserver.models.pytest_session import PytestSession

api_blueprint = flask.Blueprint('api', __name__)
api = flask_restful.Api(api_blueprint)


class PytestSessionResource(flask_restful.Resource):
    def post(self):
        new_pytest_session = PytestSession(start_time=datetime.now())
        db.session.add(new_pytest_session)
        db.session.commit()
        return new_pytest_session.id


class TestItemResource(flask_restful.Resource):
    def post(self, nodeid):
        new_test_item = TestItem(nodeid=nodeid, state=ItemState.DID_NOT_START)
        db.session.add(new_test_item)
        db.session.commit()
        return new_test_item


api.add_resource(PytestSessionResource, '/session')
api.add_resource(TestItemResource, '/<string:nodeid>')
