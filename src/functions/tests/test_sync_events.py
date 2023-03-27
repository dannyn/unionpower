import json
import requests_mock
import unittest
from unittest import mock

from src.lib.action_network import Action, Signup
from src.functions.sync_events import handler, sync_new_actions


class TestAction(unittest.TestCase):

    @mock.patch("src.lib.action_network.Action.all")
    @mock.patch("pyairtable.Table.create")
    @mock.patch("pyairtable.Table.all")
    def test_sync_action(self, mock_table_all, mock_create, mock_action_all):
        actions = [
            Action({
                'browser_url': 'https://eventurl.com',
                'start_date': '09/11/2001',
                'title': 'title',
                'description': 'magicstring',
            }),
        ]
        mock_action_all.return_value = actions

        # already existing event
        mock_table_all.return_value = [
            {'fields': {'Url': 'https://eventurl.com'}}]
        resp = sync_new_actions('1234', 'magicstring')
        self.assertEqual(len(resp), 0)

        # new event
        mock_table_all.return_value = [
            {'fields': {'Url': 'https://eventurl.comm'}}]
        resp = sync_new_actions('1234', 'magicstring')
        self.assertEqual(len(resp), 1)

        # bad magic string
        mock_table_all.return_value = [
            {'fields': {'Url': 'https://eventurl.comm'}}]
        resp = sync_new_actions('1234', 'magicstringg')
        self.assertEqual(len(resp), 0)

    @mock.patch("src.functions.sync_events.sync_new_actions")
    def test_handler(self, mock_sync):
        jo = ['event1', 'event2']
        #do = ['event3', 'event4']
        do = []

        expected = {
            'justcause': jo,
            'districtorganizing': do,
        }

        mock_sync.side_effect = [jo, do]

        resp = handler(None, None)
        jbody = json.loads(resp['body'])
        self.assertEqual(jbody, expected)
