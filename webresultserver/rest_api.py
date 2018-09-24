import http
from datetime import datetime

import flask
import flask_restful
from flask_restful import Resource

from webresultserver.database import db
from webresultserver.models.item import TestItem, ItemState
from webresultserver.models.pytest_session import PytestSession

api_blueprint = flask.Blueprint('api', __name__)
api = flask_restful.Api(api_blueprint)


class AddPytestSession(flask_restful.Resource):
    @staticmethod
    def post():
        new_pytest_session = PytestSession(start_time=datetime.now())
        db.session.add(new_pytest_session)
        db.session.commit()
        return new_pytest_session.id


class AddTestItem(flask_restful.Resource):
    @classmethod
    def post(cls, session_id, nodeid):
        cls._ensure_item_not_exist(nodeid, session_id)
        new_test_item = TestItem(session_id=session_id,
                                 nodeid=nodeid,
                                 state=ItemState.DID_NOT_START)
        db.session.add(new_test_item)
        db.session.commit()
        return new_test_item.id

    @staticmethod
    def _ensure_item_not_exist(nodeid, session_id):
        if db.session.query(db.exists().where(db.and_(TestItem.session_id == session_id,
                                                      TestItem.nodeid == nodeid))).scalar():
            error_message = 'nodeid "{nodeid}" already exists in session {session_id}'.format(
                nodeid=nodeid, session_id=session_id)
            flask_restful.abort(http.HTTPStatus.BAD_REQUEST, error_message=error_message)


class ModifyTestItemReource(Resource):
    @staticmethod
    def _get_existing_test_item(item_id):
        """
        :rtype: TestItem
        """
        test_item = db.session.query(TestItem).filter_by(id=item_id).first()
        if test_item is None:
            error_message = 'Item with ID {id} does not exist.'.format(id=item_id)
            flask_restful.abort(http.HTTPStatus.BAD_REQUEST, error_message=error_message)
        return test_item


class ChangeTestItemState(ModifyTestItemReource):
    @classmethod
    def put(cls, item_id, state_name):
        state_name = state_name.upper()
        cls._ensure_valid_state_name(state_name)
        test_item = cls._get_existing_test_item(item_id)
        test_item.state = getattr(ItemState, state_name)
        db.session.commit()
        return {'id': item_id, 'state': state_name}

    @staticmethod
    def _ensure_valid_state_name(state_name):
        if not hasattr(ItemState, state_name):
            error_message = 'No item state named "{state_name}"'.format(state_name=state_name)
            flask_restful.abort(http.HTTPStatus.BAD_REQUEST, error_message=error_message)


class GetTestItemState(ModifyTestItemReource):
    @classmethod
    def get(cls, item_id):
        test_item = cls._get_existing_test_item(item_id)
        return test_item.state.name


api.add_resource(AddPytestSession, '/add_session')
api.add_resource(AddTestItem, '/add_test_item/<int:session_id>/<string:nodeid>')
api.add_resource(ChangeTestItemState, '/change_test_state/<int:item_id>/<string:state_name>')
api.add_resource(GetTestItemState, '/get_test_state/<int:item_id>')
