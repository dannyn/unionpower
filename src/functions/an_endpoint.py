import json
import os
from pyairtable import Table

from src.lib.action_network import Action, Signup

"""
    An action refers to an action in action network. Once it is in 
    the airtable it is called an event.
"""
key = os.getenv('AIRTABLE_API_KEY')
justcause_id = os.getenv('JUSTCAUSE_TABLE_ID')
districtorganizing_id = os.getenv('DISTRICT_ORGANIZING_TABLE_ID')


def create_event_if_not_exist(action: Action, table_name: str) -> str:
    """ Creates the event in airtable if it doesnt exist. Returns
        id either way.
    """
    events_table = Table(key, table_name, 'Events')
    url = action.get_url()
    formula = f"{{Url}} = '{url}'"
    event = events_table.first(formula=formula)
    if event:
        return event['id']
    else:
        event = action.get_event()
        resp = events_table.create(event)
        return resp['id']


def create_volunteer_if_not_exist(signup: Signup, table_name: str) -> str:
    """ Creates the event in airtable if it doesnt exist. Returns
        id either way.
    """
    volunteers_table = Table(key, table_name, 'Volunteers')
    email = signup.get_email()
    formula = f"{{Email}} = '{email}'"
    vol = volunteers_table.first(formula=formula)
    if vol:
        return vol['id']
    else:
        volunteer = signup.get_volunteer()
        resp = volunteers_table.create(volunteer)
        return resp['id']


def handle_campaign(signup: Signup, action: Action, table_name: str):
    event_id = create_event_if_not_exist(action, table_name)
    vol_id = create_volunteer_if_not_exist(signup, table_name)

    # insert into rsvps with correct ids for linking
    rsvps_table = Table(key, table_name, 'RSVPs')
    rsvp = signup.get_rsvp()
    rsvp['Event'] = [event_id]
    rsvp['Volunteer'] = [vol_id]

    # dont make duplicates, action network will keep sending it sometimes
    formula = f"{{Id}} = '{rsvp['Id']}'"
    if not rsvps_table.first(formula=formula):
        rsvps_table.create(rsvp)
        return True
    return False


def handle_onboarding(signup: Signup, table_name: str):
    None


def handler(event, context):
    payload = json.loads(event['body'])
    signup = Signup(payload)
    action = signup.get_action()

    # check that this signup is from an action
    if not action:
        return {"statusCode": 200, "body": '{"message": "not from an action"}'}

    body = {}
    if action.magic_string('justcausecampaign'):
        if handle_campaign(signup, action, justcause_id):
            body['justcausecampaign'] = True
    elif action.magic_string('districtorganizingcampaign'):
        if handle_campaign(signup, action, districtorganizing_id):
            body['districtorganizingcampaign'] = True

    handle_onboarding(signup, 'onboardingtablename')

    return {"statusCode": 200, "body": body}
