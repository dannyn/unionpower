import json
import os

from pyairtable import Table

from src.lib.action_network import Action

def handler(event, context):
    key = os.getenv('AIRTABLE_API_KEY')
    table = Table(key, 'applfZpncSpD2xDJK', 'Events')
    events = table.all()
    actions = Action.all()

    # check that this is just cause
    actions = list(filter(lambda x: x.magic_string('justcausecampaign'), actions))
    for action in actions:
        e = action.get_event()
        # remove existing events
        f = list(filter(lambda x: e['Url'] == x['fields']['Url'], events))
        if not f:
            table.create(e)

    return { "statusCode": 200, }