import json

from functions import hello


def hello_handler(event, context):
    j = json.dumps(event)

    response = {
        "statusCode": 200,
        "body": hello(j)
    }

    return response