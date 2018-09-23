import http
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
    def post(self, session_id, nodeid):
        self._ensure_item_not_exist(nodeid, session_id)
        new_test_item = TestItem(session_id=session_id,
                                 nodeid=nodeid,
                                 state=ItemState.DID_NOT_START)
        db.session.add(new_test_item)
        db.session.commit()
        return new_test_item.id

    def _ensure_item_not_exist(self, nodeid, session_id):
        if db.session.query(db.exists().where(db.and_(TestItem.session_id == session_id,
                                                      TestItem.nodeid == nodeid))):
            error_message = 'nodeid "{nodeid}" already exists in session {session_id}'.format(
                nodeid=nodeid, session_id=session_id)
            flask_restful.abort(http.HTTPStatus.BAD_REQUEST, error_message=error_message)


api.add_resource(PytestSessionResource, '/session')
api.add_resource(TestItemResource, '/test_item/<int:session_id>/<string:nodeid>')
