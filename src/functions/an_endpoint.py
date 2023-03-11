import json
import os

from typing import List
from pyairtable import Table

from src.lib.action_network import Action, Signup

"""
    An action refers to an action in action network. Once it is in 
    the airtable it is called an event.
"""


def check_event_exists(action: Action, events: List) -> bool:
    url = action.get_url()
    for event in events:
        if event['fields']['Url'] == url:
            return True
    return False


def check_volunteer_exists(signup: Signup, volunteers: List) -> bool:
    email = signup.get_email()
    for v in volunteers:
        if v['fields']['Email'] == email:
            return True
    return False


def handler(event, context):
    key = os.getenv('AIRTABLE_API_KEY')
    events_table = Table(key, 'applfZpncSpD2xDJK', 'Events')
    volunteers_table = Table(key, 'applfZpncSpD2xDJK', 'Volunteers')
    rsvps_table = Table(key, 'applfZpncSpD2xDJK', 'RSVPs')

    events = events_table.all()
    volunteers = volunteers_table.all()

    payload = event.payload
    signup = Signup(payload)
    # get action from an
    action = signup.get_action()

    # check that this signup is from an action
    if not action:
        return {"statusCode": 200, }

    # check that the signup is for a just cause event by looking
    # for the magic string in the description
    if not action.magic_string('justcausecampaign'):
        return {"statusCode": 200, }

    # check that the event exists, if not create it
    if not check_event_exists(action, events):
        new_event = action.get_event()
        events_table.create(new_event)

    # if volunteer doesnt exist, create it
    if not check_volunteer_exists(payload, volunteers):
        new_vol = signup.get_volunteer()
        volunteers_table.create(new_vol)

    # insert into rsvps
    rsvp = signup.get_rsvp()
    rsvps_table.create(rsvp)

    return {"statusCode": 200, }
