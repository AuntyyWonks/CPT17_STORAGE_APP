import os
import boto3
from decimal import Decimal
import json
import uuid
from datetime import datetime
from aws_lambda_powertools import Logger

logger = Logger()

# Globals
booking_table_env = os.getenv('BOOKING_TABLE_NAME')
unit_table_env = os.getenv('UNITS_TABLE_NAME')

dynamodb = boto3.resource('dynamodb')

def book_unit(event: dict):
    logger.info("Booking a new unit")
    logger.info("event: "+ event)

    detail = json.loads(event['body'])
    unit_id = str(uuid.uuid1())
    # total_amount = detail['totalAmount']
    user_id = event['requestContext']['authorizer']['claims']['sub']
    booking_time = datetime.strftime(datetime.utcnow(), '%Y-%m-%dT%H:%M:%SZ')
    # generate unique id if it isn't present in the request
    if 'booking_id' not in detail:
        detail['booking_id'] = str(uuid.uuid1())
    booking_id = detail['booking_id']
    townId = detail['townId']
    unitSize = detail['unitSize']
    ddb_item = {
        'bookingId': booking_id,
        'userId': user_id,
        'data': {
            'bookingId': booking_id,
            'userId': user_id,
            'unitId': unit_id,
            'townId': townId,
            'unitSize': unitSize,
            'status': 'Booked',
            'bookingTime': booking_time,
        }
    }
    ddb_item = json.loads(json.dumps(ddb_item), parse_float=Decimal)
    table = dynamodb.Table(booking_table_env)
    table.put_item(Item=ddb_item, ConditionExpression='attribute_not_exists(bookingId) AND attribute_not_exists(userId)')
    
    # Update units table
    # unit_table = dynamodb.Table(unit_table_env)
    # unit_table.update_item(
    #     Key={'unitId': unit_id},
    #     UpdateExpression="set #status = :status",
    #     ExpressionAttributeNames={'#status': 'status'},
    #     ExpressionAttributeValues={':status': 'Booked'},
    #     ConditionExpression='attribute_exists(unitId)'
    # )

    detail['bookingTime'] = booking_time
    detail['status'] = 'Booked'
    return detail

def lambda_handler(event, context):
    """Handles the lambda method invocation"""
    try:
        booking_detail = book_unit(event=event)
        response = {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, PUT',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization'
            },
            "body": json.dumps(booking_detail)
        }
        return response
    except Exception as err:
        raise