# function.py:
import json
import os

def lambda_handler(event, context):

    return {
        'statusCode': 200,
        'body': '[]',
        'headers': {
            "Content-Type": "application/json"
        }
    }
