import json
import os
from pyairtable import Table
from typing import List

from src.lib.action_network import Action

key = os.getenv('AIRTABLE_API_KEY')
justcause_id = os.getenv('JUSTCAUSE_TABLE_ID')
districtorganizing_id = os.getenv('DISTRICT_ORGANIZING_TABLE_ID')


def sync_new_actions(table_id: str, magic_string: str):
    table = Table(key, table_id, 'Events')
    events = table.all()
    actions = Action.all()

    # get rid of actions which dont have the magic string in the description
    actions = list(filter(lambda x: x.magic_string(magic_string), actions))
    synced = []
    for action in actions:
        e = action.get_event()
        # remove already existing events
        f = list(filter(lambda x: e['Url'] == x['fields']['Url'], events))
        if not f:
            table.create(e)
            synced.append(e['Name'])
    return synced


def handler(event, context):
    jc = sync_new_actions(justcause_id, 'justcausecampaign')
    #do = sync_new_actions(districtorganizing_id, 'districtorganizingcampaign')
    synced = {
        "justcause": jc,
        "districtorganizing": [], #do,
    }
    return {"statusCode": 200, "body": json.dumps(synced)}
