import json

from src.functions.hello import hello


def hello_handler(event, context):

    response = {
        "statusCode": 200,
        "body": json.dumps(hello(event))
    }

    return response


def an_endpoint_handler(event, context):
    
    
    response = {
        "statusCode": 200,
        "body": "here"
    }

    return response