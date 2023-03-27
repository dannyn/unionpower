import json
import requests_mock
import unittest
from unittest import mock

from src.lib.action_network import Action, Signup
from src.functions.an_endpoint import handler, create_event_if_not_exist, create_volunteer_if_not_exist


class TestAction(unittest.TestCase):
    @mock.patch("pyairtable.Table.first")
    @mock.patch("pyairtable.Table.create")
    def test_create_event_if_not_exist(self, mock_create, mock_first):
        action = Action({
            'browser_url': 'https://eventurl.com',
            'start_date': '09/11/2001',
            'title': 'title',
        })
        mock_first.return_value = {'id': '1234'}
        self.assertEqual(create_event_if_not_exist(action, 'table_name'), '1234')

        mock_first.return_value = None
        mock_create.return_value = {'id': '12345'}
        self.assertEqual(create_event_if_not_exist(action, 'table_name'), '12345')


    @mock.patch("pyairtable.Table.first")
    @mock.patch("pyairtable.Table.create")
    def test_create_volunteer_if_not_exist(self, mock_create, mock_first):
        signup = Signup([
            {
                'osdi:attendance': {
                    'person': {
                        'given_name': 'name',
                        'family_name': 'lastname',
                        'email_addresses': [
                            {'address': 'c@d.com'}
                        ],
                        'phone_numbers': [
                            {'number': '2125551212'}
                        ],
                        'postal_addresses': [
                            {'postal_code': '11101'}
                        ]
                    }
                }
            }
        ])
        mock_first.return_value = {'id': '5678'}
        self.assertEqual(create_volunteer_if_not_exist(signup, 'table_name'), '5678')

        mock_first.return_value = None
        mock_create.return_value = {'id': '123456'}
        self.assertEqual(create_volunteer_if_not_exist(signup, 'table_name'), '123456')

    @mock.patch("src.lib.action_network.Signup.get_action")
    @mock.patch("src.functions.an_endpoint.create_volunteer_if_not_exist")
    @mock.patch("src.functions.an_endpoint.create_event_if_not_exist")
    @mock.patch("pyairtable.Table.create")
    def test_handler(self, mock_create, mock_event, mock_volunteer, mock_get_action):

        # check for not an event
        event = {
            'body': '{"some_nonsense": "sure"}'
        }
        mock_get_action.return_value = None
        resp = handler(event, None)
        self.assertEqual(resp['body'], '{"message": "not from an action"}')

        # full run through for just cause
        f = open("src/functions/tests/data/an_endpoint_jc_campaign.json")
        j = json.load(f)
        event = {"body": json.dumps(j['body'])}
        mock_event.return_value = '1234'
        mock_volunteer.return_value = '5678'
        mock_get_action.return_value = Action({'description': 'justcausecampaign'})
        resp = handler(event, None)
        self.assertEqual(resp, {"statusCode": 200, "body": {"justcausecampaign": True}})
