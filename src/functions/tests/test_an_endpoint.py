import json
import unittest
from unittest import mock

import requests_mock

from src.lib.action_network import get_action

"""
    Need test data from an actual event signup
"""
payload = [
    {
        "osdi:attendance": {
            "created_date": "2023-03-06T00:56:04Z",
            "modified_date": "2023-03-06T00:56:04Z",
            "identifiers": [
                "action_network:3a532d8d-80d7-406c-8580-43a3fed1f3e2"
            ],
            "person": {
                "created_date": "2017-12-16T16:32:47Z",
                "modified_date": "2023-03-06T00:56:05Z",
                "family_name": "Malone",
                "given_name": "Jason",
                "postal_addresses": [
                    {
                        "primary": True,
                        "region": "New York",
                        "postal_code": "11218",
                        "country": "US",
                        "location": {
                            "latitude": 40.6424,
                            "longitude": -73.9758,
                            "accuracy": "Approximate"
                        }
                    }
                ],
                "email_addresses": [
                    {
                        "primary": True,
                        "address": "jasonericmalone@gmail.com"
                    }
                ],
                "phone_numbers": [
                    {
                        "primary": True,
                        "number": "15619066622",
                        "number_type": "Mobile"
                    }
                ],
                "languages_spoken": [
                    "en"
                ]
            },
            "action_network:referrer_data": {},
            "_links": {
                "self": {
                    "href": "https://actionnetwork.org/api/v2/events/87a34885-6ad0-42e0-81af-e38cea2f7548/attendances/3a532d8d-80d7-406c-8580-43a3fed1f3e2"
                },
                "osdi:event": {
                    "href": "https://actionnetwork.org/api/v2/events/87a34885-6ad0-42e0-81af-e38cea2f7548"
                },
                "osdi:person": {
                    "href": "https://actionnetwork.org/api/v2/people/90dbdade-a710-48b7-b525-0ff724b9316f"
                }
            },
            "status": "accepted"
        },
        "action_network:sponsor": {
            "title": "NYC-DSA Union Power",
            "url": "https://actionnetwork.org/groups/nyc-dsa-union-power"
        },
        "idempotency_key": "2bc9d1f649f3c4291041a4ad53e3c889"
    }
]


# mock requests.get
class TestGetAction(unittest.TestCase):
    def test_get_action(self):
        expectedAction = {
            'worked': True
        }

        with requests_mock.Mocker() as m:
            m.get('https://actionnetwork.org/api/v2/events/87a34885-6ad0-42e0-81af-e38cea2f7548',
                  json=expectedAction)
            action = get_action(payload)
            self.assertEqual(action, expectedAction)
