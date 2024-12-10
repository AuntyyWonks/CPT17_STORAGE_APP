import json
import boto3
import stripe
from datetime import datetime


dynamoDb = boto3.client('dynamodb') 
stripe.api_key = 'your_stripe_secret_key' 

def lambda_handler(event, context):
    try:
        # Step 1: Parse the incoming request
        body = json.loads(event['body'])  # Assuming JSON body
        user_id = body.get('userId')
        payment_method_id = body.get('paymentMethodId')

        if not user_id or not payment_method_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Invalid input'})
            }

        # Step 2: Update the payment method with the external provider (Stripe)
        payment_method = stripe.PaymentMethod.attach(
            payment_method_id,
            customer=user_id  # Assuming user_id is the Stripe customer ID
        )

        # Step 3: Update the default payment method for the customer (if needed)
        stripe.Customer.modify(
            user_id,
            invoice_settings={'default_payment_method': payment_method.id}
        )

        # Step 4: Save or update payment method information in DynamoDB
        params = {
            'TableName': 'Users',  # Your DynamoDB table name
            'Key': {
                'userId': {'S': user_id}  # Primary key: userId
            },
            'UpdateExpression': 'SET paymentMethodId = :paymentMethodId, paymentMethodDetails = :paymentMethodDetails, lastUpdated = :lastUpdated',
            'ExpressionAttributeValues': {
                ':paymentMethodId': {'S': payment_method.id},
                ':paymentMethodDetails': {'S': json.dumps(payment_method)},  # Store the whole payment method or just relevant details
                ':lastUpdated': {'S': datetime.utcnow().isoformat()}
            },
            'ReturnValues': 'ALL_NEW'  # Optionally, return the updated item
        }

        # Step 5: Perform the update in DynamoDB
        result = dynamoDb.update_item(**params)

        # Step 6: Return a success response
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Payment method updated successfully',
                'data': result.get('Attributes', {})  # Optionally return the updated item
            })
        }

    except Exception as error:
        print(f'Error updating payment method: {error}')
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error updating payment method'})
        }
