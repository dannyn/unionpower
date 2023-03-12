import json
import os

from typing import List
from pyairtable import Table

from src.lib.action_network import Action, Signup

"""
    An action refers to an action in action network. Once it is in 
    the airtable it is called an event.
"""
key = os.getenv('AIRTABLE_API_KEY')
events_table = Table(key, 'applfZpncSpD2xDJK', 'Events')
volunteers_table = Table(key, 'applfZpncSpD2xDJK', 'Volunteers')
rsvps_table = Table(key, 'applfZpncSpD2xDJK', 'RSVPs')


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


def get_event_id(action: Action) -> str:
    url = action.get_url()
    formula = f"{{Url}} = '{url}'"
    event = events_table.first(formula=formula)
    return event['id']


def get_volunteer_id(signup: Signup) -> str:
    email = signup.get_email()
    formula = f"{{Email}} = '{email}'"
    volunteer = volunteers_table.first(formula=formula)
    return volunteer['id']


def create_event_if_not_exist(action: Action) -> str:
    """ Creates the event in airtable if it doesnt exist. Returns
        id either way.
    """
    url = action.get_url()
    formula = f"{{Url}} = '{url}'"
    event = events_table.first(formula=formula)
    if event:
        return event['id']
    else:
        event = action.get_event()
        resp = events_table.create(event)
        return resp['id']


def create_volunteer_if_not_exist(signup: Signup) -> str:
    """ Creates the event in airtable if it doesnt exist. Returns
        id either way.
    """
    email = signup.get_email()
    formula = f"{{Email}} = '{email}'"
    vol = volunteers_table.first(formula=formula)
    if vol:
        return vol['id']
    else:
        volunteer = signup.get_volunteer()
        resp = volunteers_table.create(volunteer)
        return resp['id']


def handler(event, context):
    events = events_table.all()
    volunteers = volunteers_table.all()

    payload = event['body']
    signup = Signup(payload)
    # get action from an
    action = signup.get_action()

    # check that this signup is from an action
    if not action:
        return {"statusCode": 200, "body": '{"message": "not from an action"}'}

    # check that the signup is for a just cause event by looking
    # for the magic string in the description
    if not action.magic_string('justcausecampaign'):
        return {"statusCode": 200, "body": '{"message": "not just cause"}'}

    # check that the event exists, if not create it
    #if not check_event_exists(action, events):
    #    new_event = action.get_event()
    #    events_table.create(new_event)
    create_event_if_not_exist(action)
    create_volunteer_if_not_exist(signup)

    # if volunteer doesnt exist, create it
    #if not check_volunteer_exists(signup, volunteers):
    #    new_vol = signup.get_volunteer()
    #    volunteers_table.create(new_vol)

    # insert into rsvps
    rsvp = signup.get_rsvp()
    rsvp['Event'] = [get_event_id(action)]
    rsvp['Volunteer'] = [get_volunteer_id(signup)]
    rsvps_table.create(rsvp)

    return {"statusCode": 200, }
