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
    None

def check_volunteer_exists(signup: Signup, volunteers: List) -> bool:
    None


def handler(event, context):

    payload = event.payload
    signup = Signup(payload)
    # get action from an
    action = signup.get_action()

    if not action:
        # this is not a signup from an action
        return False
    
    # check that the signup is for a just cause event by looking
    # for the magic string in the description

    key = os.getenv('AIRTABLE_API_KEY')
    events = pyairtable.Table(key, 'applfZpncSpD2xDJK', 'Events')
    volunteers = pyairtable.Table(key, 'applfZpncSpD2xDJK', 'Volunteers')
    rsvps = pyairtable.Table(key, 'applfZpncSpD2xDJK', 'RSVPs')

    # check that the event exists, if not create it
    if not check_event_exists(action, events):
        None
        
    # if volunteer doesnt exist, create it
    if not check_volunteer_exists(payload, volunteers):
        None

    # insert into event signups
    
    return { "statusCode": 200, }