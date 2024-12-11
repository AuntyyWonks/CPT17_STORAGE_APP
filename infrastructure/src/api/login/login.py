# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import json
import os
import boto3

USERS_POOL = os.getenv('USER_POOL_ID', None)
USER_CLIENT_ID = os.getenv('USER_CLIENT_ID', None)

def lambda_handler(event, context):
    
    request_json = json.loads(event['body'])
    cognito_client = boto3.client('cognito-idp')
    Username=request_json['username']
    Password=request_json['password']

    response_body = {'Message': 'Unsupported route'}
    status_code = 400
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, PUT',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        }

    """Handles the lambda method invocation"""
    try:
        response = cognito_client.admin_initiate_auth(
            UserPoolId=USERS_POOL,
            ClientId=USER_CLIENT_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': Username,
                'PASSWORD': Password,
            },
        )

        status_code = 200
        response_body = {
            'message': 'Sign-in successful!',
            'id_token': response['AuthenticationResult']['IdToken'],
            'access_token': response['AuthenticationResult']['AccessToken'],
            'refresh_token': response['AuthenticationResult']['RefreshToken']
        }
    except cognito_client.exceptions.NotAuthorizedException:
        status_code = 400
        response_body = {'error':'Invalid username or password.'}
    except Exception as err:
        status_code = 400
        response_body = {'error': str(err)}
        print(str(err))
        raise
    return {
        'statusCode': status_code,
        'body': json.dumps(response_body),
        'headers': headers
    }