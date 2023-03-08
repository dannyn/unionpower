import json
import os

from pyairtable import Table

from src.lib.action_network import Action

def handler(event, context):

    key = os.getenv('AIRTABLE_API_KEY')
    events = Table(key, 'applfZpncSpD2xDJK', 'Events').all()
    actions = Action.all()

    for action in actions:
        e = action.get_event()
        # remove existing events
        f = list(filter(lambda x: e['Url'] == x['Url'], events['fields']))
        if not f:
            events.create(e)

    return { "statusCode": 200, }
