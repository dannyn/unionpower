import json

from functions import an_endpoint

def an_endpoint_handler(event, context):
    
    payload = event.payload
    
    an_endpoint(payload) 

    return { "statusCode": 200, }
