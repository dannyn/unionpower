import json

def hello(event):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": json.dumps(event)
    }

    return body