"""api router"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from flask import Blueprint, jsonify
from api.routes.api import error
from api.validators import requires_auth, requires_admin, validate_event_creation
from api.services import event_service as EventService
from api.schemas import EventSchema
from api.responders import EventResponder

event_endpoints_v1 = Blueprint('event_endpoints_v1', __name__)

@event_endpoints_v1.route('/', strict_slashes=False, methods=['POST'])
@requires_auth
@requires_admin
@validate_event_creation
def create_event(event):
    """-"""
    logging.info('[ROUTER]: Creating event')
    try:
        # Creating
        event = EventService.create_event(event)
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')
    # Serialize
    event = EventSchema().dump(event).data
    response = EventResponder(event).serialize
    return jsonify(data=response), 200

@event_endpoints_v1.route('/', strict_slashes=False, methods=['GET'])
@requires_auth
def get_events(auth_user):
    """-"""
    logging.info('[ROUTER]: Getting events')
    # Getting
    events = EventService.get_events()
    # Serialize
    events = EventSchema(many=True).dump(events).data
    response = EventResponder(events).serialize
    return jsonify(data=response), 200

@event_endpoints_v1.route('/<event_id>/going', strict_slashes=False, methods=['GET'])
@requires_auth
def event_going(event_id, auth_user):
    """-"""
    logging.info('[ROUTER]: Going to Event')
    # Like new
    EventService.going_to_event(event_id, auth_user)
    return jsonify(data='OK'), 200
