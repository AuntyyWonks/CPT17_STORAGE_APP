import os
import boto3
from decimal import Decimal
import json
import uuid

# Globals
units_table = os.getenv('UNITS_TABLE_NAME')
dynamodb = boto3.resource('dynamodb')

def add_unit(event: dict):
    detail = json.loads(event['body'])
    town_id = detail['townId']
    unit_size = detail['unitSize']
    if 'unitId' not in detail:
        detail['unitId'] = str(uuid.uuid1())
    unit_id = detail['unitId']

    ddb_item = {
        'unitId': unit_id,
        'data': {
            'unitId': unit_id,
            'townId': town_id,
            'unitSize': unit_size,
            'status': 'Available',
        }
    }
    ddb_item = json.loads(json.dumps(ddb_item), parse_float=Decimal)

    table = dynamodb.Table(units_table)
    # We must use conditional expression, otherwise put_item will always replace the original order and will never fail
    table.put_item(Item=ddb_item, ConditionExpression='attribute_not_exists(unitId)')

    detail['unitId'] = unit_id
    detail['townId'] = town_id
    detail['unitSize'] = unit_size
    detail['status'] = 'Available'

    return detail


def lambda_handler(event, context):
    """Handles the lambda method invocation"""
    try:
        unit_detail = add_unit(event=event)
        status_code = 200
        headers = {}
        response_body = json.dumps(unit_detail)
    except Exception as err:
        status_code = 400
        response_body = {'Error:': str(err)}
        print(str(err))
        raise
    return {
        'statusCode': status_code,
        'body': json.dumps(response_body),
        'headers': headers
    }
