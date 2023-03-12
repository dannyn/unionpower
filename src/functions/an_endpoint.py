import os

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
    payload = event['body']
    signup = Signup(payload)
    action = signup.get_action()

    # check that this signup is from an action
    if not action:
        return {"statusCode": 200, "body": '{"message": "not from an action"}'}

    # check that the signup is for a just cause event by looking
    # for the magic string in the description
    if not action.magic_string('justcausecampaign'):
        return {"statusCode": 200, "body": '{"message": "not just cause"}'}

    create_event_if_not_exist(action)
    create_volunteer_if_not_exist(signup)

    # insert into rsvps
    rsvp = signup.get_rsvp()
    rsvp['Event'] = [get_event_id(action)]
    rsvp['Volunteer'] = [get_volunteer_id(signup)]
    rsvps_table.create(rsvp)

    return {"statusCode": 200, }
