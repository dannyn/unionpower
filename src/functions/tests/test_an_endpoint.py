import json
import unittest
from unittest import mock

import requests_mock

from src.lib.action_network import Action, Signup

from src.functions.an_endpoint import check_event_exists, check_volunteer_exists


class TestAction(unittest.TestCase):
    def test_check_event_exists(self):
        events = [{
            'fields': {
                'Url': 'https://otherevent.com'
            }
        }]

        action = Action({'browser_url': 'https://eventurl.com'})

        self.assertFalse(check_event_exists(action, events))
        events.append({
            'fields': {
                'Url': 'https://eventurl.com'
            }
        })
        self.assertTrue(check_event_exists(action, events))

    def test_check_volunteer_exists(self):
        vols = [{
            'fields': {
                'Email': 'a@b.com'
            }
        }]

        signup = Signup([
            {
                'osdi:attendance': {
                    'person': {
                        'email_addresses': [
                            {'address': 'c@d.com'}
                        ]
                    }
                }
            }
        ])

        self.assertFalse(check_volunteer_exists(signup, vols))
        vols.append({
            'fields': {
                'Email': 'c@d.com'
            }
        })
        self.assertTrue(check_volunteer_exists(signup, vols))
