import json
import requests_mock
import unittest
from unittest import mock

from src.lib.action_network import Action, Signup
from src.functions.an_endpoint import create_event_if_not_exist, create_volunteer_if_not_exist


class TestAction(unittest.TestCase):
    @mock.patch("src.functions.an_endpoint.events_table.first")
    @mock.patch("src.functions.an_endpoint.events_table.create")
    def test_create_event_if_not_exist(self, mock_create, mock_first):
        action = Action({
            'browser_url': 'https://eventurl.com',
            'start_date': '09/11/2001',
            'title': 'title',
        })
        mock_first.return_value = {'id': '1234'}
        self.assertEqual(create_event_if_not_exist(action), '1234')

        mock_first.return_value = None
        mock_create.return_value = {'id': '12345'}
        self.assertEqual(create_event_if_not_exist(action), '12345')

    @mock.patch("src.functions.an_endpoint.volunteers_table.first")
    @mock.patch("src.functions.an_endpoint.volunteers_table.create")
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
        self.assertEqual(create_volunteer_if_not_exist(signup), '5678')

        mock_first.return_value = None
        mock_create.return_value = {'id': '123456'}
        self.assertEqual(create_volunteer_if_not_exist(signup), '123456')

    def test_handler(self):
        self.assertTrue(True)
