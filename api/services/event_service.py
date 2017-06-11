"""Event Service"""

import logging
from google.appengine.ext import ndb
from google.appengine.api import memcache
from api.models.event import Event
from api.services import user_service as UserService


def create_event(event):
    logging.info('[SERVICE]: Creating a new event')
    try:
        event.put()
        memcache.set(str(event.id), event)
        memcache.delete('events_ids')
    except Exception as e:
        raise e
    return event

def get_events(query_filter=None):
    logging.info('[SERVICE]: Getting events')
    events_ids = memcache.get('events_ids')
    if events_ids is not None:
        events = memcache.get_multi(events_ids)
        if events is not None:
            return events.values()
        else:
            memcache.delete('events_ids')
            return get_events()
    else:
        if not query_filter:
            events = Event.query()
        else:
            events = Event.query().filter(query_filter)
        events_ids = events.map(lambda event: str(event.id))
        memcache.add('events_ids', events_ids, 3600)
        event_mapping = {}
        for event in events:
            event_mapping[str(event.id)] = event
        memcache.add_multi(event_mapping, 3600)
        return events

@ndb.transactional
def add_going(key, user_id):
    logging.info('[DB]: Transactional')
    event = key.get()
    if user_id not in event.going:
        event.going.append(user_id)
        event.put()
        memcache.set(str(event.id), event)

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
