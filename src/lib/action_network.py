import json
import os
import requests


class Signup:
    """ This is a really gross and strange wrapper
    around the mess of json that AN sends for a signup"""

    def __init__(self, data):
        self.data = data

    def get_action_url(self):
        try:
            url = self.data[0]['osdi:attendance']['_links']['osdi:event']['href']
        except KeyError:
            # Not every signup comes from an event
            url = None
        return url

    def get_email(self) -> str:
        person = self.get_person()
        return person['email_addresses'][0]['address']

    def get_person(self):
        return self.data[0]['osdi:attendance']['person']

    def get_action(self):
        url = self.get_action_url()
        if url:
            resp = get(url)
            return Action(resp)
        else:
            return None

    def get_id(self) -> str:
        return self.data[0]['osdi:attendance']['identifiers'][0].split(':')[1]

    def get_rsvp(self):
        """ Pulls out the info needed for an at rsvp
        """
        return {
            "Id": self.get_id(),
            "Event": self.get_action_url(),
            "Volunteer": self.get_email(),
            "RSVP'd At": self.data[0]['osdi:attendance']['created_date'],
        }

    def get_volunteer(self):
        """ Pulls out the info needed for an at volunteer
        """
        person = self.get_person()
        return {
            "Email": self.get_email(),
            "First Name": person['given_name'],
            "Last Name": person['family_name'],
            "Phone": person['phone_numbers'][0]['number'],
            "Zip Code": person['postal_addresses'][0]['postal_code'],
        }

    @staticmethod
    def from_file(filename):
        f = open(filename)
        data = json.load(f)
        return Signup(data)


class Action:
    """ Wrapper around an action
    """

    def __init__(self, data):
        self.data = data

    def get_event(self):
        """ Pulls out the info needed for an at event
        """
        return {
            'Url': self.data['browser_url'],
            'Start At': self.data['start_date'],
            'Name': self.data['title']
        }

    def get_url(self) -> str:
        """ Returns the url of the action 
        """
        return self.data['browser_url']

    def magic_string(self, ms: str) -> bool:
        """ Check for presence of magic string in description
        """
        return ms in self.data.get("description", "")

    @staticmethod
    def from_file(filename):
        f = open(filename)
        data = json.load(f)
        return Action(data)

    @staticmethod
    def all():
        """ Get all actions from action network
        """
        url = 'https://actionnetwork.org/api/v2/events'
        actions = []
        while True:
            resp = get(url)
            for action in resp['_embedded']['osdi:events']:
                a = Action(action)
                actions.append(Action(action))
            if 'next' in resp['_links']:
                url = resp['_links']['next']['href']
            else:
                break
        return actions


def get(url):
    """ Wrapper to make AN get calls with auth
    """
    key = os.getenv('ACTION_NETWORK_API_KEY')
    headers = {
        'OSDI-API-Token': key,
    }

    resp = requests.get(url, headers=headers)

    return resp.json()
