Lambda functions for Union Power


https://betterprogramming.pub/set-up-a-ci-cd-pipeline-for-aws-lambda-with-github-actions-and-serverless-in-under-5-minutes-fd070da9d143





Set up environment
==================

You will need the serverless cli installed. 

```
    $ npm install -g serverless
```

Create a virtual environment.

```
    $ python3 -m  venv venv
    $ . venv/bin/activate
```

Install deps.

```
    $ pip -r requirements.txt
```

You can use pip to install more deps or freeze them in the usual way. But be careful,
the size of a deploy cannot exceed 250M, which is surprisingly and shockingly easy
to do.

```
    $ pip install airtable
    $ pip freeze > requirements.txt
```


Create a new function
=====================

Edit `serverless.yaml` for your function. A baseline configuration is as follows. Note that
`path` is the path in the Api-Gateway that this will create.

```
functions:
  hello:
    handler: handler.hello
    events:
      - http:
          path: joke
          method: get
    environment:
      variable2: value2
```


Create and Run Tests
====================


Secrets
=======

Your functions may need acess to secret values, such as API keys.  For this you should store your secrets as
AWS SSM parameters. Then you can access it in your `serverless.yaml` file to have them set as environment 
variables.

```
    functions:
      syncToAn:
        handler: handler.run
        environment: 
          ACTION_NETWORK_APIKEY: ${ssm:/an-api-key~true}
```

Don't forget to add the `~true` at the end.


Deploy locally
==============

You will need to have docker running for this to work.

```
    $ serverless --aws-profile <profile to use> deploy
```


Deploy Automaticaly
===================

You will need to have your AWS credentials set as github secrets.

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
```

This will automatically deploy your functions to AWS upon merges to master.
