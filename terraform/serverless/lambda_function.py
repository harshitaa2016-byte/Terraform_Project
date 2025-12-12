import json

def lambda_handler(event, context):
    """
    Simple Lambda function that returns a welcome message
    """
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'message': 'Hello from AWS Lambda! Your serverless function is working.',
            'timestamp': '2024-01-01T00:00:00Z',
            'status': 'success'
        })
    }
