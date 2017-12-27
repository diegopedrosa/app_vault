from __future__ import print_function
import sys
import os
import json
import boto3
from secret import secret


#############Return Handle################
def respond(status, res=''):
    return {'statusCode': status ,
        'body': json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }
#######################################

#############Call Secret################
def exec_secret(event):
    secobject = secret()

    if event['httpMethod'] == 'PUT':
        result = secobject.create(event)

    if event['httpMethod'] == 'GET':
        result = secobject.get(event) 

    return respond(result['status'] , result['message']) 

#######################################

def exec_secrets_app(event):
    secobject = secret()
    result = secobject.get_data_by_type(event)
    print(result['message'])
    return respond(result['status'] , result['message']) 

#############Route Rule################
def choice(event):

    return {
        '/{environment}/{application}/{type}/{data}':exec_secret,
        '/{environment}/{application}/{type}':exec_secrets_app,
        '/{environment}/{application}':exec_secrets_app
    }[event['resource']]

#######################################


def lambda_handler(event, context):
    
    return choice(event)(event)
    sys.exit(0)

