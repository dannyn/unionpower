Lambda functions for Union Power


https://betterprogramming.pub/set-up-a-ci-cd-pipeline-for-aws-lambda-with-github-actions-and-serverless-in-under-5-minutes-fd070da9d143


Create a new function
=====================



Set up environment
==================

You will need the serverless cli installed. 

```
    $ npm install -g serverless
```

Create a new function.

```
    $ serverless create --template aws-python3 --path <functionName>
    $ cd <functionName>
```

We need a plugin.

```
    $ serverless plugin install -n serverless-python-requirements

```

Edit `serverless.yaml` for your function. A baseline configuration is as follows.

```
service: aneventstoat

provider:
  name: aws
  runtime: python3.8
  region: us-east-1

custom:
  pythonRequirements:
    dockerizePip: true

package:
  individually: false
  exclude:
    - package.json
    - package-log.json
    - node_modules/**

functions:
  hello:
    handler: handler.hello
    events:
      - http:
          path: joke
          method: get
    environment:
      variable2: value2

plugins:
  - serverless-python-requirements
```

You will also need to modify `package.json` to suit your needs.

```
{
  "name": "union-power-aneventstoat",
  "description": "",
  "version": "0.1.0",
  "dependencies": {},
  "scripts": {
    "deploy": "serverless deploy"
  },
  "devDependencies": {
    "serverless": "^1.67.0",
    "serverless-python-requirements": "^6.0.0"
  }
}
```

In a function we create and activate a virtual environment to work in.

```
    $ python3 -m  venv venv
    $ . venv/bin/activate
```

Install deps.

```
    $ pip -r requirements.txt
```

You can use pip to install more deps or freeze them in the usual way.

```
    $ pip install parsons[all
    $ pip freeze > requirements.txt
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
          ACTION_NETWORK_APIKEY: ${ssm:/an-api-key}
```


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
