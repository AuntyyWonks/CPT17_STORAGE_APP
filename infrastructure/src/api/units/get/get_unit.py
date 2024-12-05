import simplejson as json
from utils import get_unit

def lambda_handler(event, context):
    unit_id = event['pathParameters']['unitId']

    try:
        units = get_unit(unit_id)
        response = {
            "statusCode": 200,
            "headers": {},
            "body": json.dumps(units)
        }
        return response
    except Exception as err:
        raise