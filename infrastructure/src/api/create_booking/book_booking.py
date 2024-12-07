import os
import boto3
from decimal import Decimal
import json
import uuid
from datetime import datetime

# Globals
orders_table = os.getenv('my_table_name')
dynamodb = boto3.resource('dynamodb')
# this is used to book the unit which the user has selected.
def book_unit(event: dict):
    detail = json.loads(event['body'])
    unit_id = detail['unit_id']
    total_amount = detail['totalAmount']
    order_unit = detail['order_unit']
    user_id = event['requestContext']['authorizer']['claims']['sub']
    order_time = datetime.strftime(datetime.utcnow(), '%Y-%m-%dT%H:%M:%SZ')
    order_id = detail['orderId']

    ddb_item = {
        'orderId': order_id,
        'userId': user_id,
        'data': {
            'orderId': order_id,
            'userId': user_id,
            'unitid': unit_id,
            'totalAmount': total_amount,
            'orderunits': order_unit,
            'status': 'Booked',
            'orderTime': order_time,
        }
    }
    ddb_item = json.loads(json.dumps(ddb_item), parse_float=Decimal)

    table = dynamodb.Table(orders_table)
    # We must use conditional expression, otherwise put_item will always replace the original order and will never fail
    table.put_item(Item=ddb_item, ConditionExpression='attribute_not_exists(orderId) AND attribute_not_exists(userId)')

    detail['orderId'] = order_id
    detail['orderTime'] = order_time
    detail['status'] = 'Available'

    return detail


def lambda_handler(event, context):
    """Handles the lambda method invocation"""
    try:
        order_detail = book_unit(event=event)
        response = {
            "statusCode": 200,
            "headers": {},
            "body": json.dumps(order_detail)
        }
        return response
    except Exception as err:
        raise
