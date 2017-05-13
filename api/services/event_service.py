"""Event Service"""

import logging
from google.appengine.ext import ndb
from api.models.event import Event
from api.services import user_service as UserService


def create_event(event):
    logging.info('[SERVICE]: Creating a new event')
    try:
        event.put()
    except Exception as e:
        raise e
    return event

def get_events(query_filter=None):
    logging.info('[SERVICE]: Getting events')
    if not query_filter:
        event = Event.query()
    else:
        event = Event.query().filter(query_filter)
    return event

@ndb.transactional
def add_going(key, user_id):
    logging.info('[DB]: Transactional')
    event = key.get()
    if user_id not in event.going:
        event.going.append(user_id)
        event.put()

def going_to_event(event_id, auth_user):
    logging.info('[SERVICE]: Going to event')
    try:
        event_id = int(event_id)
        user = UserService.get_user_by_email(auth_user['email'])
        key = ndb.Key('Event', event_id)
        add_going(key, user.id)
        UserService.add_event_going(user.id, event_id)
    except Exception as e:
        return 'OK'
    return 'OK'
