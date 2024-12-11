import json
import boto3
import stripe
from datetime import datetime

# Initialize Stripe with the secret key
stripe.api_key = 'your-stripe-secret-key'  # Replace with your actual secret key

# Initialize DynamoDB DocumentClient
dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    try:
        # Step 1: Parse the incoming request
        body = json.loads(event['body'])
        user_id = body.get('userId')
        payment_method_id = body.get('paymentMethodId')

        # Check for required parameters
        if not user_id or not payment_method_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Invalid input'}),
            }

        # Step 2: Attach the payment method with Stripe
        payment_method = stripe.PaymentMethod.attach(
            payment_method_id,
            customer=user_id  # assuming userId is the Stripe customer ID
        )

        # Step 3: Update the default payment method for the customer (if needed)
        stripe.Customer.modify(
            user_id,
            invoice_settings={'default_payment_method': payment_method.id}
        )

        # Step 4: Save or update payment method information in DynamoDB
        table_name = 'Users'  # Your DynamoDB table name
        params = {
            'TableName': table_name,
            'Key': {'userId': {'S': user_id}},  # Primary key
            'UpdateExpression': 'SET paymentMethodId = :paymentMethodId, paymentMethodDetails = :paymentMethodDetails, lastUpdated = :lastUpdated',
            'ExpressionAttributeValues': {
                ':paymentMethodId': {'S': payment_method.id},
                ':paymentMethodDetails': {'S': json.dumps(payment_method)},  # Store the whole payment method or just relevant details
                ':lastUpdated': {'S': datetime.utcnow().isoformat()},
            },
            'ReturnValues': 'ALL_NEW'  # Optionally return the updated item
        }

        # Step 5: Perform the update in DynamoDB
        result = dynamodb.update_item(**params)

        # Step 6: Return a success response
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Payment method updated successfully',
                'data': result.get('Attributes')  # Optionally return the updated item
            }),
        }

    except Exception as error:
        # Handle any errors that occurred during the process
        print('Error updating payment method:', error)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error updating payment method'})
        }
