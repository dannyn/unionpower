
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

