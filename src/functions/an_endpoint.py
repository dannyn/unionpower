from pyairtable import Table
import json
import os

def an_endpoint(payload):

    # get event from an
    # check that the signup is for a just cause event

    key = ''
    os.getenv('AIRTABLE_API_KEY')
    events = pyairtable.Table(key, 'applfZpncSpD2xDJK', 'Events')
    volunteers = pyairtable.Table(key, 'applfZpncSpD2xDJK', 'Volunteers')
    rsvps = pyairtable.Table(key, 'applfZpncSpD2xDJK', 'RSVPs')

    # check that the event exists, if not create it
    # if volunteer doesnt exist, create it
    # insert into event signups
    
    return True