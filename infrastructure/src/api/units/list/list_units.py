import simplejson as json
import os
import boto3
from aws_lambda_powertools import Logger

logger = Logger()

logger.info("List units")

# Globals
units_table = os.getenv('UNITS_TABLE_NAME')
dynamodb = boto3.resource('dynamodb')

def list_units(event):

    table = dynamodb.Table(units_table)
    response = table.scan(Select='ALL_ATTRIBUTES')
    print(response)
    logger.info("Got response")
    logger.info(response)

    units = [item for item in response['Items']]

    return units

def lambda_handler(event, context):
    
    try:
        units = list_units(event)
        response = {
            "statusCode": 200,
            "headers": {},
            "body": json.dumps({
                "units": units
            })
        }
        return response
    except Exception as err:
        raise


def update_unit_status(event, context):
    """
    Lambda function to update the status of a storage unit.
    """
    body = json.loads(event["body"])
    facility_id = body["facilityId"]
    unit_id = body["unitId"]
    new_status = body["status"]

    table = dynamodb.Table(units_table)

    table.update_item(
        Key={"facilityId": facility_id, "unitId": unit_id},
        UpdateExpression="SET #s = :new_status",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":new_status": new_status},
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Status updated successfully!"}),
        "headers": {"Content-Type": "application/json"},
    }    