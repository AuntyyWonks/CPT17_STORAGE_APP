import os
import boto3
import json
from boto3.dynamodb.conditions import Key, Attr

# Globals
orders_table = os.getenv("Booking_TABLE_NAME")
dynamodb = boto3.resource('dynamodb')

def list_bookings(event):
    # Retrieve user ID from the request context
    user_id = event['requestContext']['authorizer']['claims']['sub']
    
    # Access the DynamoDB table
    table = dynamodb.Table(orders_table)
    
    # Set up query parameters
    query_params = {
        'KeyConditionExpression': Key('userId').eq(user_id)
    }
    
    # List to store all user orders
    all_user_bookings = []
    last_evaluated_key = None
    
    # Loop to handle pagination if necessary
    while True:
        if last_evaluated_key:
            query_params['ExclusiveStartKey'] = last_evaluated_key
        
        # Execute the query
        response = table.query(**query_params)
        
        # Add the retrieved orders to the list
        all_user_bookings.extend([item['data'] for item in response['Items']])
        
        # Check for pagination and update the last evaluated key
        last_evaluated_key = response.get('LastEvaluatedKey')
        
        # If there are no more items, break the loop
        if not last_evaluated_key:
            break
    
    return all_user_bookings

def lambda_handler(event, context):
    try:
        # Get the orders for the user
        orders = list_bookings(event)
        
        # Construct the response
        response = {
            "statusCode": 200,
            "headers": {},
            "body": json.dumps({
                "orders": orders
            })
        }
        return response
    except Exception as err:
        # If an error occurs, raise a 500 response with error details
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(err)})
        }
