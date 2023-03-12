
import requests_mock
import unittest

from src.lib.action_network import Signup, Action


class TestSignup(unittest.TestCase):
    def test_get_action(self):
        signup = Signup.from_file("src/lib/tests/data/event_signup.json")
        expectedAction = Action({'worked': True})

        with requests_mock.Mocker() as m:
            m.get('https://actionnetwork.org/api/v2/events/87a34885-6ad0-42e0-81af-e38cea2f7548',
                  json={'worked': True})
            action = signup.get_action()
            self.assertEqual(action.data, expectedAction.data)

    def test_get_email(self):
        signup = Signup.from_file("src/lib/tests/data/event_signup.json")
        self.assertEqual(signup.get_email(), 'personperson@gmail.com')

    def test_get_id(self):
        signup = Signup.from_file("src/lib/tests/data/event_signup.json")
        self.assertEqual(signup.get_id(), '3a532d8d-80d7-406c-8580-43a3fed1f3e2')

    def test_get_volunteer(self):
        signup = Signup.from_file("src/lib/tests/data/event_signup.json")

        expected = {
            "Email": 'personperson@gmail.com',
            "First Name": 'PersonName',
            "Last Name": 'FamilyName',
            "Phone": '12125551212',
            "Zip Code": '11218',
        }

        self.assertEqual(signup.get_volunteer(), expected)

    def test_get_rsvp(self):
        signup = Signup.from_file("src/lib/tests/data/event_signup.json")

        expected = {
            "Event": 'https://actionnetwork.org/api/v2/events/87a34885-6ad0-42e0-81af-e38cea2f7548',
            "Volunteer": 'personperson@gmail.com',
            "Id": '3a532d8d-80d7-406c-8580-43a3fed1f3e2',
            "RSVP'd At": '2023-03-06T00:56:04Z',
        }

        self.assertEqual(signup.get_rsvp(), expected)


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

    def test_url(self):
        action = Action.from_file("src/lib/tests/data/single_event.json")
        expected = 'https://actionnetwork.org/events/union-power-district-organizing-canvas-central-brooklyn'
        self.assertEqual(action.get_url(), expected)

    def test_all(self):
        page1 = {
            '_embedded': {
                'osdi:events': [1, 2, 3]
            },
            '_links': {
                'next':  {
                    'href': 'https://actionnetwork.org/api/v2/events2'
                }
            }
        }
        page2 = {
            '_embedded': {
                'osdi:events': [4, 5, 6]
            },
            '_links': {
                'next':  {
                    'href': 'https://actionnetwork.org/api/v2/events3'
                }
            }
        }
        page3 = {
            '_embedded': {
                'osdi:events': [7, 8, 9]
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
