
import requests_mock
import unittest

from src.lib.action_network import Signup, Action

class TestSignup(unittest.TestCase):
    def test_get_action(self):
        signup = Signup.from_file("src/lib/tests/data/event_signup.json")
        expectedAction = {
            'worked': True
        }

        with requests_mock.Mocker() as m:
            m.get('https://actionnetwork.org/api/v2/events/87a34885-6ad0-42e0-81af-e38cea2f7548',
                  json=expectedAction)
            action = signup.get_action()
            self.assertEqual(action, expectedAction)

    def test_get_email(self):
        signup = Signup.from_file("src/lib/tests/data/event_signup.json")
        self.assertEqual(signup.get_email(), 'personperson@gmail.com')


class TestAction(unittest.TestCase):
    def test_magic_string(self):
        action = Action.from_file("src/lib/tests/data/single_event.json")
        self.assertTrue(action.magic_string("Jabari Brisport"))
        self.assertFalse(action.magic_string("Andrew Cuomo"))

    def test_get_event(self):
        action = Action.from_file("src/lib/tests/data/single_event.json")

        expected = {
            'Url': 'https://actionnetwork.org/events/union-power-district-organizing-canvas-central-brooklyn',
            'Start At': '2023-03-12T14:00:00Z',
            'Name': 'Union Power District Organizing Canvas - Central Brooklyn',
        }

        self.assertEqual(action.get_event(), expected)

    def test_all(self):
        page1 = {
            '_embedded': {
                'osdi:events': [1,2,3]
            },
            '_links': {
                'next':  {
                    'href': 'https://actionnetwork.org/api/v2/events2'
                }
            }
        }
        page2 = {
            '_embedded': {
                'osdi:events': [4,5,6]
            },
            '_links': {
                'next':  {
                    'href': 'https://actionnetwork.org/api/v2/events3'
                }
            }
        }
        page3 = {
            '_embedded': {
                'osdi:events': [7,8,9]
            },
            '_links': {
            }
        }

        with requests_mock.Mocker() as m:
            m.get('https://actionnetwork.org/api/v2/events', json=page1)
            m.get('https://actionnetwork.org/api/v2/events2', json=page2)
            m.get('https://actionnetwork.org/api/v2/events3', json=page3)
            actions = Action.all()

            self.assertEqual(len(actions), 9)
