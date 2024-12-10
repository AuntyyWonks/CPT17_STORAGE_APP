import json
import os
import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime, timedelta
from botocore.exceptions import ClientError
import time

# Custom exception
class OrderStatusError(Exception):
    status_code = 400
    
    def __init__(self, message):
        super().__init__(message)

# Globals
orders_table_env = os.getenv('Booking_TABLE_NAME')
unit_table_env = os.getenv('UnitsTable') 
dynamodb = boto3.resource('dynamodb')

def cancel_order(event):
    user_id = event['requestContext']['authorizer']['claims']['sub']
    booking_id = event['pathParameters']['bookingId']
    
    current_time = datetime.now()
    
    try:
        # Access the booking table and update the order status
        table = dynamodb.Table(orders_table_env)
        response = table.update_item(
            Key={'userId': user_id, 'bookingId': booking_id},
            UpdateExpression="set #data.#status = :new_status",
            ConditionExpression="(#data.#status = :current_status) AND (#data.bookingTime > :minBookingTime)",
            ExpressionAttributeNames={
                "#data": "data",
                "#status": "status"
            },
            ExpressionAttributeValues={
                ":current_status": "Booked",
                ":minBookingTime": current_time - 600,  # 10 minutes in the past
                ":new_status": "CANCELED"
            },
            ReturnValues="ALL_NEW"
        )

        # Check if the update was successful
        if 'Attributes' not in response:
            raise OrderStatusError(f"Order {booking_id} could not be found or updated.")

        # Update the unit status to Available
        unit_table_obj = dynamodb.Table(unit_table_env)
        unit_table_obj.update_item(
            Key={'unitId': response['Attributes']['data']['unitId']},
            UpdateExpression="set #status = :status",
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={':status': 'Available'},
            ConditionExpression='attribute_exists(unitId)'
        )
        
    except ClientError as exc:
        if exc.response['Error']['Code'] == 'ConditionalCheckFailedException':
            raise OrderStatusError(f"Order {booking_id} cannot be cancelled. Make sure the status of this order is 'Booked' and it was created less than 10 minutes ago.")
        else:
            raise OrderStatusError(f"Error occurred: {exc.response['Error']['Code']}: {exc.response['Error']['Message']}")
    except Exception as e:
        raise OrderStatusError(f"An unexpected error occurred: {e}")

    return response['Attributes']['data']

def lambda_handler(event, context):
    try:
        updated = cancel_order(event)
        response = {
            "statusCode": 200,
            "headers": {},
            "body": json.dumps(updated)
        }
        return response
    except OrderStatusError as oe:
        return {
            "statusCode": oe.status_code,
            "body": str(oe)
        }
    except Exception as err:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(err)})
        }
