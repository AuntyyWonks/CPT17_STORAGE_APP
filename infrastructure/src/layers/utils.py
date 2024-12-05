from boto3.dynamodb.conditions import Key
import boto3
import os

units_table = os.getenv('UNITS_TABLE_NAME')
dynamodb = boto3.resource('dynamodb')

def get_unit(unit_id):
    table = dynamodb.Table(units_table)
    response = table.query(
        KeyConditionExpression=(Key('unitId').eq(unit_id))
    )
    
    units = []
    for item in response['Items']:
      units.append(item['data'])
      
    return units[0]