import http
from datetime import datetime

import flask
import flask_restful

from webresultserver.database import db
from webresultserver.models.item import TestItem, ItemState
from webresultserver.models.pytest_session import PytestSession

api_blueprint = flask.Blueprint('api', __name__)
api = flask_restful.Api(api_blueprint)


class AddPytestSession(flask_restful.Resource):
    def post(self):
        new_pytest_session = PytestSession(start_time=datetime.now())
        db.session.add(new_pytest_session)
        db.session.commit()
        return new_pytest_session.id


class AddTestItem(flask_restful.Resource):
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
                                                      TestItem.nodeid == nodeid))).scalar():
            error_message = 'nodeid "{nodeid}" already exists in session {session_id}'.format(
                nodeid=nodeid, session_id=session_id)
            flask_restful.abort(http.HTTPStatus.BAD_REQUEST, error_message=error_message)


class ChangeTestItemState(flask_restful.Resource):
    def put(self, item_id, state_name):
        state_name = state_name.upper()
        self._ensure_valid_state_name(state_name)
        test_item = db.session.query(TestItem).first()
        self._ensure_test_item_exists(item_id, test_item)
        test_item.state = getattr(ItemState, state_name)
        db.session.commit()
        return {'id': item_id, 'state': state_name}

    def _ensure_valid_state_name(self, state_name):
        if not hasattr(ItemState, state_name):
            error_message = 'No item state named "{state_name}"'.format(state_name=state_name)
            flask_restful.abort(http.HTTPStatus.BAD_REQUEST, error_message=error_message)

    def _ensure_test_item_exists(self, item_id, test_item):
        if test_item is None:
            error_message = 'Item with ID {id} does not exist.'.format(id=item_id)
            flask_restful.abort(http.HTTPStatus.BAD_REQUEST, error_message=error_message)


api.add_resource(AddPytestSession, '/add_session')
api.add_resource(AddTestItem, '/add_test_item/<int:session_id>/<string:nodeid>')
api.add_resource(ChangeTestItemState, '/change_test_state/<int:item_id>/<string:state_name>')
